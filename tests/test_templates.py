"""Regression tests for the copy-paste templates in playbook section 16 (Templates F, G and M).

The tests pull each template out of playbook/agent-harness-playbook.md and check that it parses,
passes lint, behaves, and keeps the security fixes from issues/reviews/playbook-factcheck-v0.3.md.

Run all tests:  python3 -I -m unittest discover -s tests -p 'test_*.py'
Run this file:  python3 -I tests/test_templates.py
Where the default temp folder is not writable, set TEST_TMP to a writable folder.
A missing optional tool (shellcheck, a YAML parser) skips its test with "NOT RUN", never a silent pass.
"""
import functools
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "playbook" / "agent-harness-playbook.md"
SECTION_TOOL = ROOT / "tools" / "section.py"
STOP_HOOK_TEST_CMD = "TEST_CMD=(npm test --silent)"


def make_tmp(case):
    """A fresh temp dir under TEST_TMP (if set), removed when the test ends."""
    path = tempfile.mkdtemp(prefix="tpltest-", dir=os.environ.get("TEST_TMP") or None)
    case.addCleanup(shutil.rmtree, path, True)
    return pathlib.Path(path)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)


def fenced_blocks(lines):
    """Return [(lang, text, first_line_index)] for each ``` fenced block in a list of lines."""
    blocks, lang, buf, start = [], None, [], 0
    for n, line in enumerate(lines):
        if lang is None:
            m = re.match(r"```(\w*)\s*$", line)
            if m:
                lang, buf, start = m.group(1), [], n
        elif line.startswith("```"):
            blocks.append((lang, "\n".join(buf) + "\n", start))
            lang = None
        else:
            buf.append(line)
    return blocks


def only(blocks, what, where, pred):
    """The single block that satisfies pred, or a test failure that says what to update."""
    found = [text for lang, text, _ in blocks if pred(lang, text)]
    if len(found) != 1:
        raise AssertionError(f"Expected exactly one {what} in {where} of playbook/agent-harness-playbook.md, found {len(found)}. "
                             "If you restructured the template, update tests/test_templates.py to match.")
    return found[0]


@functools.lru_cache(maxsize=None)
def templates():
    """Extract Templates F, G and M from playbook section 16, using tools/section.py's heading index."""
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("guide_section_tool", SECTION_TOOL)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    lines, idx = tool.index(PLAYBOOK)
    for key in ("F", "G", "H", "M"):
        if key not in idx:
            raise AssertionError(f"tools/section.py finds no Template {key} heading in the playbook. "
                                 f"Headings in section 16 must read '### {key}. <title>'.")
    f_to_h = fenced_blocks(lines[idx["F"][1]:idx["H"][1]])
    m_blocks = fenced_blocks(lines[idx["M"][1]:idx["M"][2]])
    bash = [b for b in f_to_h if b[0] == "bash"]
    return {
        "stop_hook": only(bash, "bash block with MAX_TRIES (the Stop hook)", "Template F",
                          lambda l, t: t.startswith("#!/usr/bin/env bash") and "MAX_TRIES" in t),
        "formatter": only(bash, "bash block with prettier (the formatter)", "Template G",
                          lambda l, t: t.startswith("#!/usr/bin/env bash") and "prettier" in t),
        "json": [t for lang, t, _ in f_to_h if lang == "json"],
        "settings_f": only(f_to_h, "json block with a Stop hook (Template F settings)", "Template F",
                           lambda l, t: l == "json" and '"Stop"' in t),
        "guardrails": only(f_to_h, "json block with permissions.ask (the guardrails)", "Template F",
                           lambda l, t: l == "json" and '"ask"' in t),
        "yaml_m": only(m_blocks, "yaml block for claude-review.yml", "Template M",
                       lambda l, t: l == "yaml" and "claude-review.yml" in t),
    }


def write_script(case, name, text):
    path = make_tmp(case) / name
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)
    return path


def parse_yaml(case, text):
    """Parse YAML with PyYAML, else ruby; skip the test (NOT RUN) when neither exists."""
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        pass
    ruby = shutil.which("ruby")
    if not ruby:
        case.skipTest("NOT RUN: no YAML parser installed (PyYAML or ruby)")
    path = make_tmp(case) / "template.yml"
    path.write_text(text, encoding="utf-8")
    r = run([ruby, "-ryaml", "-rjson", "-e", "puts JSON.generate(YAML.safe_load(File.read(ARGV[0])))", str(path)])
    case.assertEqual(r.returncode, 0, f"Template M is not valid YAML:\n{r.stderr}")
    return json.loads(r.stdout)


def strip_yaml_comments(text):
    """Drop '# ...' comments (a # at line start or after a space). Template M has no # inside values."""
    return re.sub(r"(^|\s)#.*$", r"\1", text, flags=re.M).rstrip() + "\n"


def indent_of(line):
    return len(line) - len(line.lstrip())


def children(lines, start):
    """Lines nested deeper than lines[start], up to the next line at or above its indent."""
    out = []
    for line in lines[start + 1:]:
        if line.strip() and indent_of(line) <= indent_of(lines[start]):
            break
        out.append(line)
    return out


def action_step(lines):
    """The lines of the anthropics/claude-code-action step (its '- uses:' line first)."""
    for n, line in enumerate(lines):
        if re.match(r"\s*-\s+uses:\s*anthropics/claude-code-action@", line):
            return [line] + children(lines, n)
    raise AssertionError("Template M has no 'uses: anthropics/claude-code-action@...' step. Restore the action step.")


class ShellTemplates(unittest.TestCase):
    def check_script(self, key, name):
        text = templates()[key]
        path = write_script(self, name, text)
        r = run(["bash", "-n", str(path)])
        self.assertEqual(r.returncode, 0, f"{name} (playbook Template F/G) has a syntax error:\n{r.stderr}")
        exe = shutil.which("shellcheck")
        if not exe:
            self.skipTest("NOT RUN: shellcheck not installed (bash -n passed)")
        r = run([exe, str(path)])
        self.assertEqual(r.returncode, 0, f"shellcheck flags {name} in the playbook; fix the template:\n{r.stdout}")

    def test_stop_hook_passes_bash_n_and_shellcheck(self):
        """Template F's verify-on-stop.sh parses and lints clean, since it runs on every stop."""
        self.check_script("stop_hook", "verify-on-stop.sh")

    def test_formatter_passes_bash_n_and_shellcheck(self):
        """Template G's format.sh parses and lints clean, since it runs outside the sandbox."""
        self.check_script("formatter", "format.sh")

    def test_formatter_uses_project_prettier_and_skips_gate_files(self):
        """Template G never runs npx (it can download code) and never auto-edits .claude, .github or CODEOWNERS."""
        code = "\n".join(l for l in templates()["formatter"].splitlines() if not l.lstrip().startswith("#"))
        self.assertNotIn("npx", code, "Template G's format.sh uses npx, which can download a package outside the sandbox. Use node_modules/.bin/prettier.")
        self.assertIn("node_modules/.bin/prettier", code, "Template G's format.sh must run the project's own Prettier.")
        for gate in ("*/.claude/*", "*/.github/*", "*/CODEOWNERS"):
            self.assertIn(gate, code, f"Template G's format.sh must skip {gate} so the agent can't auto-edit its own gate.")


class JsonTemplates(unittest.TestCase):
    def test_json_blocks_in_templates_f_and_g_parse(self):
        """Every json block from Template F to Template H (settings, guardrails, formatter hook) is valid JSON."""
        blocks = templates()["json"]
        self.assertGreaterEqual(len(blocks), 3, f"Expected 3 json blocks (F settings, F guardrails, G hook), found {len(blocks)}.")
        for n, text in enumerate(blocks, 1):
            with self.subTest(block=n):
                try:
                    json.loads(text)
                except ValueError as e:
                    self.fail(f"json block {n} between '### F.' and '### H.' is not valid JSON: {e}\n{text}")


class StopHookBehaviour(unittest.TestCase):
    def setUp(self):
        base = make_tmp(self)
        self.home, self.tmp, self.project = base / "home", base / "tmp", base / "project"
        for d in (self.home, self.tmp, self.project):
            d.mkdir()
        self.script = base / "verify-on-stop.sh"
        self.session = "t1" if shutil.which("jq") else "unknown"  # the hook reads session_id with jq

    def use_test_cmd(self, cmd):
        text = templates()["stop_hook"]
        self.assertIn(STOP_HOOK_TEST_CMD, text, f"Template F's hook no longer has the line {STOP_HOOK_TEST_CMD}; update STOP_HOOK_TEST_CMD in tests/test_templates.py.")
        self.script.write_text(text.replace(STOP_HOOK_TEST_CMD, f"TEST_CMD=({cmd})"), encoding="utf-8")

    def stop(self):
        env = dict(os.environ, HOME=str(self.home), TMPDIR=str(self.tmp), CLAUDE_PROJECT_DIR=str(self.project))
        return run(["bash", str(self.script)], input=json.dumps({"session_id": "t1"}), env=env)

    @property
    def marker(self):
        return self.project / ".gate-failed"

    @property
    def log(self):
        return self.home / ".agent-gate-logs" / "gate-failures.log"

    def test_failing_tests_block_the_first_three_stops(self):
        """While tests fail, stops 1 to 3 exit 2 with the failure on stderr and leave no .gate-failed."""
        self.use_test_cmd("false")
        for attempt in (1, 2, 3):
            r = self.stop()
            self.assertEqual(r.returncode, 2, f"Stop hook, stop {attempt}: must exit 2 (block) while tests fail. Got {r.returncode}. Fix the exit code in Template F.")
            self.assertIn(f"attempt {attempt} of 3", r.stderr, f"Stop hook, stop {attempt}: stderr must say which attempt this is.")
            self.assertFalse(self.marker.exists(), f"Stop hook, stop {attempt}: wrote .gate-failed before giving up.")

    def test_fourth_stop_gives_up_with_marker_and_one_log_line(self):
        """After MAX_TRIES blocked stops the hook lets go, writes .gate-failed and logs one line outside the repo."""
        self.use_test_cmd("false")
        for _ in range(3):
            self.stop()
        r = self.stop()
        self.assertEqual(r.returncode, 0, f"Stop hook, stop 4: must exit 0 (give up). Got {r.returncode}:\n{r.stderr}")
        self.assertTrue(self.marker.is_file(), "Stop hook, stop 4: must write .gate-failed so the stop is never silent.")
        lines = self.log.read_text(encoding="utf-8").splitlines() if self.log.exists() else []
        self.assertEqual(len(lines), 1, f"Stop hook, stop 4: expected one line in $HOME/.agent-gate-logs/gate-failures.log, found {len(lines)}.")
        self.assertIn(f"session={self.session}", lines[0], "The log line must name the session.")
        self.assertIn(str(self.project), lines[0], "The log line must name the repo.")
        self.assertEqual(list(self.tmp.glob("verify-on-stop-*")), [], "Give-up must remove the retry counter so the next session starts at 1.")

    def test_passing_run_exits_0_and_removes_gate_failed(self):
        """A passing run exits 0, removes a stale .gate-failed and clears the retry counter."""
        self.use_test_cmd("false")
        for _ in range(2):
            self.stop()
        self.marker.write_text("left by an earlier give-up\n", encoding="utf-8")
        self.use_test_cmd("true")
        r = self.stop()
        self.assertEqual(r.returncode, 0, f"Stop hook: a passing run must exit 0. Got {r.returncode}:\n{r.stderr}")
        self.assertFalse(self.marker.exists(), "Stop hook: a passing run must remove .gate-failed.")
        self.assertEqual(list(self.tmp.glob("verify-on-stop-*")), [], "Stop hook: a passing run must clear the retry counter.")
        self.use_test_cmd("false")
        self.assertEqual(self.stop().returncode, 2, "Stop hook: after a pass the next failure must block again (the count starts over).")


class TemplateMWorkflow(unittest.TestCase):
    def setUp(self):
        self.raw = templates()["yaml_m"]
        self.lines = strip_yaml_comments(self.raw).splitlines()

    def test_yaml_parses_and_has_the_review_job(self):
        """Template M is valid YAML with a pull_request trigger and a review job that has steps."""
        doc = parse_yaml(self, self.raw)
        self.assertIsInstance(doc, dict, "Template M did not parse to a mapping.")
        trigger = next((doc[k] for k in ("on", True, "true") if k in doc), None)  # YAML 1.1 reads `on` as true
        self.assertIn("pull_request", trigger or {}, "Template M must trigger on pull_request.")
        self.assertTrue(doc["jobs"]["review"]["steps"], "Template M's review job has no steps.")

    def test_trigger_is_not_pull_request_target(self):
        """Template M never uses pull_request_target, which would run untrusted PR code with secrets."""
        stripped = "\n".join(self.lines)
        self.assertNotIn("pull_request_target", stripped, "Template M's workflow uses pull_request_target outside a comment. Use pull_request.")
        self.assertRegex(stripped, r"(?m)^on:\s*\n\s+pull_request:", "Template M must trigger on pull_request.")

    def test_allowed_tools_cannot_write_to_the_pr(self):
        """--allowedTools holds no bare Bash and no gh command that can post to the PR (the exfiltration channel)."""
        m = re.search(r'--allowed-?[Tt]ools\s+"([^"]*)"', "\n".join(self.lines))
        self.assertIsNotNone(m, "Template M no longer passes --allowedTools \"...\". Restrict the tools of a review-only job.")
        tools = [t.strip() for t in m.group(1).split(",") if t.strip()]
        self.assertTrue(tools, "Template M's --allowedTools is empty.")
        writers = r"gh\s+(?:pr\s+(?:comment|review|edit|merge|close|reopen|ready)|issue\s+(?:comment|create|edit|close)|api)\b"
        for tool in tools:
            with self.subTest(tool=tool):
                self.assertNotIn(tool, ("Bash", "Bash(*)", "Bash(*:*)"),
                                 f"Template M allows {tool}: any shell command, including one that posts $ANTHROPIC_API_KEY to the PR. Allow only gh pr diff and gh pr view.")
                self.assertNotRegex(tool, rf"^Bash\(\s*{writers}",
                                    f"Template M allows {tool}, which can write to the PR. An injected PR body could post a secret through it. "
                                    "Post through mcp__github_comment__update_claude_comment instead.")

    def test_action_step_scrubs_subprocess_env(self):
        """The action step sets env CLAUDE_CODE_SUBPROCESS_ENV_SCRUB to 1, or Bash subprocesses inherit the API key."""
        step = action_step(self.lines)
        env_at = [n for n, l in enumerate(step) if re.fullmatch(r"\s*env:\s*", l) and indent_of(l) == indent_of(step[0]) + 2]
        self.assertTrue(env_at, "Template M's claude-code-action step has no env: block at step level. "
                                "Add env: CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: \"1\" between uses: and with:.")
        entries = [l.strip() for l in children(step, env_at[0])]
        self.assertTrue(any(re.fullmatch(r"CLAUDE_CODE_SUBPROCESS_ENV_SCRUB:\s*[\"']?1[\"']?", e) for e in entries),
                        f"Template M's action step env must set CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: \"1\". Found: {entries}")

    def test_env_scrub_is_in_the_parsed_action_step(self):
        """Parsed YAML agrees: the claude-code-action step's own env sets CLAUDE_CODE_SUBPROCESS_ENV_SCRUB to 1."""
        doc = parse_yaml(self, self.raw)
        steps = [s for s in doc["jobs"]["review"]["steps"] if str(s.get("uses", "")).startswith("anthropics/claude-code-action@")]
        self.assertEqual(len(steps), 1, "Template M must have exactly one claude-code-action step.")
        self.assertEqual(str(steps[0].get("env", {}).get("CLAUDE_CODE_SUBPROCESS_ENV_SCRUB")), "1",
                         "Template M's action step must set env CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: \"1\" (a sibling of with:, not inside it).")

    def test_prompt_marks_pr_text_as_untrusted(self):
        """The review prompt tells the model that PR title, body, comments and diff are untrusted input."""
        step = action_step(self.lines)
        at = [n for n, l in enumerate(step) if re.match(r"\s*prompt:", l)]
        self.assertTrue(at, "Template M's action step has no prompt:.")
        prompt = " ".join(l.strip() for l in children(step, at[0]))
        self.assertRegex(prompt, re.compile(r"untrusted input", re.I), "Template M's prompt must say PR text is untrusted input.")
        self.assertRegex(prompt, re.compile(r"never follow instructions", re.I), "Template M's prompt must say never to follow instructions found in PR text.")


class TemplateFSettings(unittest.TestCase):
    def setUp(self):
        self.raw = templates()["settings_f"]
        self.settings = json.loads(self.raw)

    def test_denies_editing_the_claude_directory(self):
        """Template F denies Edit(/.claude/**), so the agent can't edit its own gate (deny holds in every mode)."""
        deny = self.settings.get("permissions", {}).get("deny", [])
        self.assertIn("Edit(/.claude/**)", deny, f"Template F's permissions.deny must contain \"Edit(/.claude/**)\". Found {deny}. "
                                                 "Edit rules cover every built-in editing tool.")

    def test_has_no_write_path_rule(self):
        """Template F has no Write(...) rule: a Write path rule is accepted but never matches, so it gives false safety."""
        self.assertNotIn("Write(", self.raw, "Template F contains a Write(...) rule. Use Edit(...); a Write path rule never matches.")

    def test_stop_hook_has_no_onfailure(self):
        """The Stop hook sets no onFailure: it has no effect on Stop hooks, so it would suggest a gate that isn't there."""
        self.assertNotIn("onFailure", self.raw, "Template F's settings contain onFailure. It has no effect on Stop hooks; remove it.")
        stop = self.settings["hooks"]["Stop"]
        commands = [h["command"] for entry in stop for h in entry["hooks"]]
        self.assertTrue(any(c.endswith("/.claude/hooks/verify-on-stop.sh") for c in commands),
                        f"Template F's Stop hook must run .claude/hooks/verify-on-stop.sh. Found {commands}.")


class GuardrailsSettings(unittest.TestCase):
    def test_denies_force_push_and_rm_rf_and_asks_on_push(self):
        """The guardrails JSON denies git push --force (and -f) and rm -rf, and asks before any git push."""
        perms = json.loads(templates()["guardrails"]).get("permissions", {})
        deny, ask = perms.get("deny", []), perms.get("ask", [])
        for rule in ("Bash(git push --force:*)", "Bash(git push -f:*)", "Bash(rm -rf:*)"):
            with self.subTest(rule=rule):
                self.assertIn(rule, deny, f"The Template F guardrails must deny {rule}. Found deny: {deny}.")
        self.assertIn("Bash(git push:*)", ask, f"The Template F guardrails must ask before git push. Found ask: {ask}.")


if __name__ == "__main__":
    unittest.main()
