"""Regression tests for the /guide and /grill skills (/prompt has its own file, test_prompt_skill.py).

Run all tests:  python3 -I -m unittest discover -s tests -p 'test_*.py'
Run this file:  python3 -I tests/test_skills.py
Where the default temp folder is not writable, set TEST_TMP to a writable folder.
A missing optional tool (shellcheck) skips its test with "NOT RUN", never a silent pass.
"""
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
GUIDE_DIR = ROOT / "skills" / "guide"
GRILL_DIR = ROOT / "skills" / "grill"
FIXTURES = ROOT / "tests" / "fixtures" / "grill"
SKILLS = {  # command name -> SKILL.md
    "guide": GUIDE_DIR / "SKILL.md",
    "grill": GRILL_DIR / "SKILL.md",
}


def read(path):
    return pathlib.Path(path).read_text(encoding="utf-8")


def frontmatter(path):
    """Return (fields, body) for a SKILL.md whose frontmatter sits between two --- lines."""
    text = read(path)
    m = re.match(r"---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not m:
        raise AssertionError(f"{path}: no frontmatter between --- lines. Start the file with --- and end the block with ---.")
    fields = {}
    for line in m.group(1).splitlines():
        k = re.match(r"([A-Za-z][\w-]*):\s*(.*)$", line)
        if k:
            fields[k.group(1)] = k.group(2).strip()
    return fields, m.group(2)


def make_tmp(case):
    """A fresh temp dir under TEST_TMP (if set), removed when the test ends."""
    path = tempfile.mkdtemp(prefix="skilltest-", dir=os.environ.get("TEST_TMP") or None)
    case.addCleanup(shutil.rmtree, path, True)
    return pathlib.Path(path)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)


def need_shellcheck(case):
    exe = shutil.which("shellcheck")
    if not exe:
        case.skipTest("NOT RUN: shellcheck not installed")
    return exe


class Frontmatter(unittest.TestCase):
    def test_each_skill_has_name_and_description(self):
        """Each SKILL.md names its own command and has a non-empty description, so it lists in the / menu."""
        for command, path in SKILLS.items():
            with self.subTest(skill=command):
                self.assertTrue(path.is_file(), f"{path} is missing. Restore the skill's SKILL.md.")
                fields, _ = frontmatter(path)
                self.assertEqual(fields.get("name"), command,
                                 f"{path}: frontmatter name must be '{command}' (the slash command). Fix the name line.")
                self.assertEqual(path.parent.name, command,
                                 f"{path}: the skill's folder must be named '{command}', or the symlink install links the wrong name.")
                self.assertTrue(fields.get("description"),
                                f"{path}: description is empty. Claude Code uses it to decide when to load the skill.")

    def test_frontmatter_values_are_valid_plain_yaml(self):
        """No unquoted frontmatter value contains ': ' or ' #', which strict YAML parsers reject or truncate."""
        for command, path in SKILLS.items():
            fields, _ = frontmatter(path)
            for key, value in fields.items():
                with self.subTest(skill=command, key=key):
                    if value[:1] in "\"'":
                        continue
                    self.assertNotIn(": ", value, f"{path}: '{key}' has ': ' in an unquoted value. Quote the value or reword it.")
                    self.assertNotIn(" #", value, f"{path}: '{key}' has ' #' in an unquoted value. Quote the value or reword it.")


class GuideSkill(unittest.TestCase):
    def setUp(self):
        self.text = read(SKILLS["guide"])
        _, self.body = frontmatter(SKILLS["guide"])

    def test_points_at_entry_and_section_tool_and_never_reads_whole_playbook(self):
        """/guide routes through ENTRY.md and section.py and forbids reading the whole 1,480-line playbook."""
        self.assertIn("ENTRY.md", self.body, "skills/guide/SKILL.md must send the session to ENTRY.md.")
        self.assertIn("tools/section.py", self.body, "skills/guide/SKILL.md must load sections with tools/section.py.")
        self.assertRegex(self.body, re.compile(r"never read\b.{0,80}playbook.{0,80}\bwhole", re.I | re.S),
                         "skills/guide/SKILL.md must tell the session never to read the whole playbook.")

    def test_has_no_preexecuted_shell_line(self):
        """No '!`' pre-run shell line: it stalled a claude -p session at start-up (skills/guide/README.md, Cold tests)."""
        bad = [n for n, line in enumerate(self.text.splitlines(), 1) if "!`" in line or line.lstrip().startswith("```!")]
        self.assertEqual(bad, [], f"skills/guide/SKILL.md lines {bad} use a pre-run shell line. "
                                  "Tell the model to run the command in a numbered step instead.")

    def test_finds_root_with_git_rev_parse(self):
        """/guide finds the clone's root from the symlink with git, because nothing stores the path."""
        self.assertIn('git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel', self.body,
                      "skills/guide/SKILL.md must find the root with: git -C \"${CLAUDE_SKILL_DIR}\" rev-parse --show-toplevel")


class GuideSnippetAndPrompt(unittest.TestCase):
    def test_snippet_is_one_line_pointer_without_import(self):
        """snippet.md stays one line and a plain pointer, since an @ import would load a file into every session."""
        text = read(GUIDE_DIR / "snippet.md")
        lines = [l for l in text.splitlines() if l.strip()]
        self.assertEqual(len(lines), 1, f"skills/guide/snippet.md has {len(lines)} non-empty lines; it must be exactly one.")
        self.assertEqual(len(text.rstrip("\n").splitlines()), 1, "skills/guide/snippet.md has blank lines; keep it to one line.")
        for needle in ("{{GUIDE}}", "ENTRY.md", "section.py"):
            self.assertIn(needle, text, f"skills/guide/snippet.md must contain {needle}.")
        self.assertNotIn("@", text, "skills/guide/snippet.md contains '@': an @ import loads the file into every session. Use a plain path.")

    def test_prompt_has_placeholders(self):
        """prompt.md keeps {{GUIDE}} for install.sh to fill and <describe it> for the user to fill."""
        text = read(GUIDE_DIR / "prompt.md")
        self.assertIn("{{GUIDE}}", text, "skills/guide/prompt.md must contain {{GUIDE}}; install.sh fills it with the root.")
        self.assertIn("<describe it>", text, "skills/guide/prompt.md must end with a <describe it> slot for the request.")


class InstallScript(unittest.TestCase):
    script = GUIDE_DIR / "install.sh"

    def install(self, home, *args):
        env = dict(os.environ, HOME=str(home))
        return run(["bash", str(self.script), *args], env=env, cwd=str(home))

    def fresh_home(self):
        home = make_tmp(self)
        return home, home / ".claude" / "skills" / "guide"

    def test_syntax(self):
        """bash -n parses install.sh, so a typo can't ship."""
        r = run(["bash", "-n", str(self.script)])
        self.assertEqual(r.returncode, 0, f"skills/guide/install.sh has a syntax error:\n{r.stderr}")

    def test_shellcheck(self):
        """shellcheck finds nothing in install.sh, which writes to the user's ~/.claude."""
        r = run([need_shellcheck(self), str(self.script)])
        self.assertEqual(r.returncode, 0, f"shellcheck flags skills/guide/install.sh; fix these:\n{r.stdout}")

    def test_dry_run_prints_change_and_writes_nothing(self):
        """With no args the script only reports the symlink it would make, and creates nothing under HOME."""
        home, link = self.fresh_home()
        r = self.install(home)
        self.assertEqual(r.returncode, 0, f"dry run failed:\n{r.stderr}")
        self.assertIn(f"+ {link} -> {ROOT}/skills/guide", r.stdout.splitlines(), f"dry run must print the planned change. Got:\n{r.stdout}")
        self.assertIn("Dry run: nothing written", r.stdout)
        self.assertEqual(list(home.rglob("*")), [], "the dry run wrote files under HOME. It must write nothing.")

    def test_printed_snippet_and_prompt_have_real_root(self):
        """The printed CLAUDE.md snippet and prompt carry this clone's root, with no {{GUIDE}} left over."""
        home, _ = self.fresh_home()
        r = self.install(home)
        self.assertNotIn("{{GUIDE}}", r.stdout, "install.sh printed an unfilled {{GUIDE}}. Check the sed lines at the end.")
        self.assertIn(f"{ROOT}/ENTRY.md", r.stdout, "the printed snippet must name <root>/ENTRY.md.")
        self.assertIn(f"{ROOT}/tools/section.py", r.stdout, "the printed snippet must name <root>/tools/section.py.")
        self.assertIn(f"GUIDE = {ROOT}.", r.stdout, "the printed prompt must carry the real root.")

    def test_apply_creates_symlink_and_second_apply_is_no_change(self):
        """--apply links ~/.claude/skills/guide to this clone, and running it again changes nothing."""
        home, link = self.fresh_home()
        r = self.install(home, "--apply")
        self.assertEqual(r.returncode, 0, f"--apply failed:\n{r.stderr}")
        self.assertTrue(link.is_symlink(), f"--apply did not create the symlink {link}.")
        self.assertEqual(os.readlink(link), f"{ROOT}/skills/guide", "the symlink must point at <root>/skills/guide.")
        self.assertTrue((link / "SKILL.md").is_file(), "the symlink target has no SKILL.md.")
        again = self.install(home, "--apply")
        self.assertEqual(again.returncode, 0, f"second --apply failed:\n{again.stderr}")
        self.assertIn("No change", again.stdout, f"a second --apply must report 'No change'. Got:\n{again.stdout}")

    def test_finds_the_root_when_a_git_hook_sets_git_dir(self):
        """In a worktree, git exports GIT_DIR to hooks; install.sh then took skills/guide as the root and broke the commit hook."""
        home, link = self.fresh_home()
        git_dir = run(["git", "-C", str(ROOT), "rev-parse", "--absolute-git-dir"]).stdout.strip()
        env = dict(os.environ, HOME=str(home), GIT_DIR=git_dir)
        r = run(["bash", str(self.script)], env=env, cwd=str(home))
        self.assertEqual(r.returncode, 0, f"dry run with GIT_DIR set failed:\n{r.stderr}")
        self.assertIn(f"+ {link} -> {ROOT}/skills/guide", r.stdout.splitlines(), f"install.sh misread the root under GIT_DIR. Got:\n{r.stdout}")

    def test_apply_repoints_a_stale_symlink(self):
        """A symlink that points elsewhere is reported with a '-' line and then repointed."""
        home, link = self.fresh_home()
        link.parent.mkdir(parents=True)
        link.symlink_to(home / "old-clone")
        r = self.install(home, "--apply")
        self.assertEqual(r.returncode, 0, f"--apply over a stale symlink failed:\n{r.stderr}")
        self.assertIn(f"- {link} -> {home / 'old-clone'}", r.stdout.splitlines(), "the old target must be shown before it is replaced.")
        self.assertEqual(os.readlink(link), f"{ROOT}/skills/guide", "the stale symlink was not repointed.")

    def test_real_directory_is_never_replaced(self):
        """A real directory at ~/.claude/skills/guide stops the script with exit 1 and is left intact."""
        home, link = self.fresh_home()
        link.mkdir(parents=True)
        (link / "mine.txt").write_text("keep me", encoding="utf-8")
        for args in ((), ("--apply",)):
            with self.subTest(args=args):
                r = self.install(home, *args)
                self.assertEqual(r.returncode, 1, f"install.sh must exit 1 over a real directory. Got {r.returncode}.")
                self.assertIn("STOP", r.stderr, "install.sh must print STOP on stderr over a real directory.")
                self.assertFalse(link.is_symlink(), "install.sh replaced a real directory with a symlink.")
                self.assertEqual((link / "mine.txt").read_text(encoding="utf-8"), "keep me", "install.sh damaged the user's directory.")

    def test_logs_route_and_decisions_to_disk_when_work_follows(self):
        """/guide's routing and decisions vanish with the chat unless it logs them to docs/decisions.md (wiki/records.md)."""
        _, body = frontmatter(SKILLS["guide"])
        self.assertIn("docs/decisions.md", body, "skills/guide/SKILL.md must log the route and decisions to docs/decisions.md.")
        self.assertRegex(body, re.compile(r"dated line.{0,200}reason", re.I | re.S),
                         "skills/guide/SKILL.md must log a dated line with each decision's reason.")
        self.assertIn("wiki/records.md", body, "skills/guide/SKILL.md must point at wiki/records.md.")


class GrillSkillRules(unittest.TestCase):
    def setUp(self):
        _, self.body = frontmatter(SKILLS["grill"])

    def rule(self, pattern, what):
        self.assertRegex(self.body, re.compile(pattern, re.I | re.S),
                         f"skills/grill/SKILL.md lost its rule: {what}. Restore it, or update this test and playbook Template K together.")

    def test_one_question_per_message(self):
        """/grill asks one question per message, so the user is never handed a list to answer."""
        self.rule(r"one question per message", "one question per message")

    def test_recommended_option_comes_first(self):
        """/grill puts the recommended option first and marks it '(Recommended)'."""
        self.assertIn('"(Recommended)"', self.body, "skills/grill/SKILL.md must name the exact '(Recommended)' label.")
        self.rule(r"recommended option comes first", "the recommended option comes first")

    def test_looks_before_asking(self):
        """/grill reads the project first and never asks a fact it can find."""
        self.rule(r"look before you ask", "look before you ask")
        self.rule(r"never ask the user a fact you can find", "never ask a fact you can find")

    def test_logs_decisions(self):
        """/grill logs every decision with its reason in docs/discovery or the plan's Decisions list."""
        self.rule(r"log every decision.{0,80}docs/discovery/", "log every decision in docs/discovery/<topic>.md")
        self.rule(r"the question, the answer and the reason", "log the question, the answer and the reason")

    def test_logs_as_it_goes_and_commits(self):
        """/grill writes each dated decision as it goes and commits it, so a compacted or new session can resume."""
        self.rule(r"the date, the question", "date every decision")
        self.rule(r"as you go, not at the end", "log as you go, not at the end")
        self.rule(r"commit it with the branch", "commit the log with the branch")

    def test_has_a_stop_rule(self):
        """/grill stops when no branch is open or at the user's question cap, then summarizes."""
        self.rule(r"\*\*stop\*\*.{0,60}no branch is open.{0,60}question cap", "stop when no branch is open or at the question cap")
        self.rule(r"summarize the decisions", "summarize the decisions for the user to confirm")

    def test_approval_is_not_a_grill_question(self):
        """A go-ahead to build, commit or publish needs an explicit yes, never a picked option."""
        self.rule(r"go-ahead is not a grill question", "a go-ahead is not a grill question")
        self.rule(r"never a picked option", "approval is never a picked option")

    def test_writes_no_plan_spec_or_code(self):
        """/grill ends before any plan, spec or code is written."""
        self.rule(r"do not write a plan, spec or code", "do not write a plan, spec or code")

    def test_fact_questions_are_open(self):
        """A figure offered in an option and picked with one click becomes an invented fact (grill-prompt dry run, R2)."""
        self.rule(r"fact question.{0,80}asked open, with no options", "ask fact questions open, with no options")
        self.rule(r"no option and no question text carries a figure", "no figure in an option or the question text")

    def test_covers_problem_and_riskiest_assumption(self):
        """The grill covers the problem and the riskiest assumption (dry run, R7)."""
        self.rule(r"the problem \(who struggles", "cover the problem: who struggles and what it costs")
        self.rule(r"riskiest assumption with the cheapest test", "cover the riskiest assumption and its cheapest test")
        self.rule(r"where the work lives \(the code, data and records", "cover where the code, data and records live (dry run round 4, R4)")

    def test_marks_unknowns_assumptions_and_relative_terms(self):
        """'I don't know' is not a decision; self-filled values are marked; relative terms are resolved (dry run, R1, R3, R4)."""
        self.rule(r"\"I don't know\" is not a decision.{0,80}UNKNOWN: <why>", "log 'I don't know' as UNKNOWN, not a decision")
        self.rule(r"ASSUMED: <text>", "mark self-filled values ASSUMED")
        self.rule(r"relative terms.{0,80}absolute dates and named people", "write relative terms as dates and names")
        self.rule(r"listing every `ASSUMED` and `UNKNOWN` line", "list every ASSUMED and UNKNOWN line in the summary")

    def test_one_gap_per_unknown_and_one_ask_per_question(self):
        """Round 2 of the dry run: runs merged unknowns to look shorter and bundled several asks into one question."""
        self.rule(r"one gap per `UNKNOWN` line: never merge gaps", "one gap per UNKNOWN line, never merged")
        self.rule(r"each question asks one thing", "each question asks one thing")
        self.rule(r"one the request or an earlier answer already gives", "never ask what the request or an earlier answer gives")


class GrillTranscriptChecker(unittest.TestCase):
    checker = GRILL_DIR / "check_transcript.py"

    def check(self, fixture):
        path = FIXTURES / fixture
        self.assertTrue(path.is_file(), f"{path} is missing. Restore the fixture.")
        r = run([sys.executable, "-I", str(self.checker), str(path)])
        lines = {m.group(2): m.group(1) for m in (re.match(r"(PASS|FAIL) (grill-\d)\b", l) for l in r.stdout.splitlines()) if m}
        return r, lines

    def expect_fail(self, fixture, rule):
        r, lines = self.check(fixture)
        self.assertEqual(lines.get(rule), "FAIL",
                         f"{fixture} must make {rule} FAIL, but skills/grill/check_transcript.py reported:\n{r.stdout}{r.stderr}")
        self.assertEqual(r.returncode, 1, f"check_transcript.py must exit 1 when {rule} fails. Got {r.returncode}.")

    def test_good_transcript_passes_all_eight_checks(self):
        """A transcript that looks, reports the README fact, asks one lettered question passes every check."""
        r, lines = self.check("good.jsonl")
        self.assertEqual(r.returncode, 0, f"good.jsonl must exit 0:\n{r.stdout}{r.stderr}")
        self.assertEqual(sorted(lines.values()), ["PASS"] * 8, f"good.jsonl must show 8 PASS lines:\n{r.stdout}")

    def test_good_question_through_ask_user_question_tool_passes(self):
        """A question asked through the AskUserQuestion tool, 3 options, first '(Recommended)', passes."""
        r, lines = self.check("good-tool.jsonl")
        self.assertEqual(r.returncode, 0, f"good-tool.jsonl must exit 0:\n{r.stdout}{r.stderr}")
        self.assertEqual(sorted(lines.values()), ["PASS"] * 8, f"good-tool.jsonl must show 8 PASS lines:\n{r.stdout}")

    def test_asking_the_database_fails_grill_3(self):
        """Asking 'Which database do you use?' when the README says PostgreSQL fails grill-3."""
        self.expect_fail("asks-db.jsonl", "grill-3")

    def test_no_lookup_fails_grill_1(self):
        """A session that asks without a Read, Grep or Glob call fails grill-1."""
        self.expect_fail("no-lookup.jsonl", "grill-1")

    def test_two_questions_fail_grill_4(self):
        """Two question lines in one message fail grill-4."""
        self.expect_fail("two-questions.jsonl", "grill-4")

    def test_five_options_fail_grill_5(self):
        """Five options in an AskUserQuestion call fail grill-5 (2 to 4 allowed)."""
        self.expect_fail("five-options.jsonl", "grill-5")

    def test_two_questions_in_one_tool_call_fail_grill_4(self):
        """One AskUserQuestion call that holds two questions fails grill-4."""
        self.expect_fail("two-questions-tool.jsonl", "grill-4")

    def test_five_lettered_text_options_fail_grill_5(self):
        """Five lettered options (A to E) in a plain-text question fail grill-5."""
        self.expect_fail("five-options-text.jsonl", "grill-5")

    def test_no_recommendation_fails_grill_6(self):
        """Options with no '(Recommended)' label fail grill-6."""
        self.expect_fail("no-recommendation.jsonl", "grill-6")

    def test_writing_a_plan_fails_grill_7(self):
        """A Write tool call during the grill fails grill-7."""
        self.expect_fail("writes-plan.jsonl", "grill-7")

    def test_session_error_fails_grill_8(self):
        """A result event with is_error true fails grill-8."""
        self.expect_fail("session-error.jsonl", "grill-8")


class GrillColdTestScript(unittest.TestCase):
    script = GRILL_DIR / "test.sh"

    def test_syntax(self):
        """bash -n parses skills/grill/test.sh."""
        r = run(["bash", "-n", str(self.script)])
        self.assertEqual(r.returncode, 0, f"skills/grill/test.sh has a syntax error:\n{r.stderr}")

    def test_shellcheck(self):
        """shellcheck finds nothing in skills/grill/test.sh, which runs rm -rf in a trap."""
        r = run([need_shellcheck(self), str(self.script)])
        self.assertEqual(r.returncode, 0, f"shellcheck flags skills/grill/test.sh; fix these:\n{r.stdout}")

    def test_trap_removes_only_the_work_subfolder(self):
        """Statically: the only rm target is "$work", and work is "$GRILL_TEST_DIR/grill-test.$$" when the variable is set."""
        text = read(self.script)
        self.assertIn('work="$GRILL_TEST_DIR/grill-test.$$"', text,
                      "skills/grill/test.sh must work in a subfolder named \"$GRILL_TEST_DIR/grill-test.$$\", never in GRILL_TEST_DIR itself.")
        self.assertRegex(text, r"""(?m)^trap 'rm -rf "\$work"' EXIT""", "skills/grill/test.sh must clean up with: trap 'rm -rf \"$work\"' EXIT")
        targets = re.findall(r"\brm\s+-\w+\s+(\S+)", text)
        self.assertTrue(targets, "skills/grill/test.sh no longer cleans up after itself.")
        for target in targets:
            self.assertEqual(target.strip("'"), '"$work"',
                             f"skills/grill/test.sh runs rm on {target}. It may delete only \"$work\", never GRILL_TEST_DIR.")

    def test_runs_with_a_stub_claude_and_deletes_only_its_subfolder(self):
        """Run test.sh with a stub claude: GRILL_TEST_DIR and its other files survive, the subfolder goes, the prompt is sent."""
        tmp = make_tmp(self)
        bin_dir, base = tmp / "bin", tmp / "grill-base"
        bin_dir.mkdir()
        base.mkdir()
        (base / "keep.txt").write_text("keep me", encoding="utf-8")
        stub = bin_dir / "claude"
        stub.write_text('#!/bin/sh\nprintf \'%s\\0\' "$@" > "$STUB_ARGS"\ncat "$STUB_TRANSCRIPT"\n', encoding="utf-8")
        stub.chmod(0o755)
        env = dict(os.environ, GRILL_TEST_DIR=str(base), PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                   STUB_ARGS=str(tmp / "args"), STUB_TRANSCRIPT=str(FIXTURES / "good.jsonl"), TMPDIR=str(tmp))
        r = run(["bash", str(self.script)], env=env, cwd=str(tmp))
        self.assertEqual(r.returncode, 0, f"skills/grill/test.sh failed against a stub claude:\n{r.stdout}{r.stderr}")
        self.assertTrue(base.is_dir(), "test.sh deleted GRILL_TEST_DIR itself. It may delete only its own subfolder.")
        self.assertEqual((base / "keep.txt").read_text(encoding="utf-8"), "keep me", "test.sh deleted files in GRILL_TEST_DIR it did not create.")
        self.assertEqual(list(base.glob("grill-test.*")), [], "test.sh left its work subfolder behind; the trap did not run.")
        args = (tmp / "args").read_text(encoding="utf-8").split("\0")
        self.assertEqual(args[0], "-p", "test.sh must call claude with -p.")
        self.assertIn("full-text search", args[1], "the prompt must carry the request.")
        self.assertNotIn("$ARGUMENTS", args[1], "the prompt still holds a literal $ARGUMENTS; the substitution broke.")
        self.assertIn("stream-json", args, "test.sh must ask for --output-format stream-json; check_transcript.py parses it.")
        allowed = args[args.index("--allowedTools") + 1]
        for tool in ("Write", "Edit", "NotebookEdit"):
            self.assertNotIn(tool, allowed, f"the grill test session was allowed {tool}; a grill session may only read.")


if __name__ == "__main__":
    unittest.main()
