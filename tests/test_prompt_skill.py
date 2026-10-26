"""/prompt: the skill keeps its rules, its scorer grades drafts correctly, and prompts can't be committed.

The live A/B battle test (tests/live/prompt/run.sh, interview.sh) costs model sessions and stays
opt-in; its recorded results are in tests/results/prompt-battle.json.
Run: python3 -I tests/test_prompt_skill.py   (or the whole suite: tests/run.sh)
"""
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "prompt" / "SKILL.md").read_text(encoding="utf-8")
KIT = ROOT / "tests" / "live" / "prompt"
FIX = ROOT / "tests" / "fixtures" / "prompt"


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"(?m)^([\w-]+):\s*(.*)$", m.group(1))) if m else {}


class SkillRules(unittest.TestCase):
    def test_frontmatter(self):
        """/prompt loses its name, its description, or becomes something Claude can run on its own."""
        fm = frontmatter(SKILL)
        self.assertEqual(fm.get("name"), "prompt")
        self.assertTrue(fm.get("description", "").strip(), "/prompt needs a description")
        self.assertEqual(fm.get("disable-model-invocation"), "true", "/prompt must run only when typed")
        self.assertNotIn("allowed-tools", fm, "/prompt must not pre-approve any tool")

    def test_keeps_v10_r6(self):
        """v10 R6: plan files go to docs/plans (Template B)."""
        for phrase in [
            'add a plan file at `docs/plans/<task>.md`',
            'Plan files go in `docs/plans/`; other working files go in `<scratch>`',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_keeps_every_rule(self):
        """A rule the battle tests depend on is dropped from /prompt."""
        rules = {
            "look before asking": "Look before you ask.",
            "interview cap": "Stop at 5 questions.",
            "one question per message, recommendation first": "ask one question per message, with your recommended answer first",
            "size by risk": "Size it by risk",
            "one writer": "One writer per set of files.",
            "tests immutable": "tests are immutable to the builder",
            "DONE WHEN 2 to 5": "DONE WHEN: 2 to 5 checks",
            "BUDGET": "BUDGET: a ceiling",
            "STOP AND ASK": "STOP AND ASK IF:",
            "receipt": "PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.",
            "same brief for compared helpers": "Helpers whose results will be compared get the same brief",
            "Template C briefs": "add the briefs** (Template C)",
            "Template H for loops": "use Template H:",
            "NEEDS A HUMAN": "list it under NEEDS A HUMAN",
            "writes the prompt, not the work": "You write the prompt; you do not do the task.",
            # From the grill-prompt dry run (tests/live/grill-prompt/): each one failed there before it was added.
            "facts asked open": "Ask for facts (a number, date or name) as an open question",
            "trace every figure": "Trace every figure.",
            "self-chosen values marked": "once at the top of the prompt as `ASSUMED: <text>`, and each gap there as `UNKNOWN: <why>`",
            "relative terms resolved": "Write relative terms (",
            "fresh review before saving": "**Get a fresh review before saving**",
            "deterministic check before review": 'check_prompt.py" <draft> --source <decision log>',
            # Round 2 of the dry run: self-checks missed every conflict, and gaps were merged to stay under the cap.
            "no self-review in place of the fresh one": "don't review your own draft in its place",
            "unreviewed drafts are labelled": 'write "Review: not run" at its top',
            "one gap per UNKNOWN line": "one gap per line. Never merge gaps",
            "one ask per question": "Each question asks one thing.",
            # Round 3: edits made after the last review brought defects back.
            "no unreviewed edits after the last review": "After the last review, change nothing but the blockers it named",
            # v7, from the misses in dry-run round 4 and the repeated ASSUMED tags in battle round 10.
            "ask where the work lives": "Find where the work lives: the code, data and records the task reads or changes.",
            "fallbacks meet the goal": "A fallback for missing input (no export, no access) still meets the GOAL",
            "stop conditions tested against now": "Test each STOP AND ASK line against what is known now",
            "reviewer asks about zero cases": "can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?",
            "reviewer asks about stop conditions": "Does any STOP AND ASK condition already hold?",
            "chosen figures tagged once": "Elsewhere, use the value plainly or by its name",
            # v10 R1: Template L's risk rule and Template B's trivial form (§5.3).
            "risk line above the title": "write the result above the title as `Risk: trivial`, `Risk: normal` or `Risk: high`",
            "risk set by a rule": "Set it by a rule, not by feel (Template L).",
            "high risk defined": "High: the work touches a schema, auth, payments, data deletion, a public API, infrastructure or production, adds a dependency, or runs unattended.",
            "trivial defined": "Trivial: a small fix in one place, easy to undo, with no helpers or loop",
            "normal defined": "Normal: everything else.",
            "visible behaviour never trivial": "A change to user-visible behaviour is never trivial.",
            "higher size wins": "When two sizes apply, or the rule and a person disagree, the higher wins.",
            "trivial keeps Template B's parts": 'Trivial: GOAL, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT',
            "unattended sign-off once": "an unattended run is signed off once, before it first starts",
        }
        for name, phrase in rules.items():
            self.assertIn(phrase, SKILL, f"/prompt lost its '{name}' rule: {phrase!r}")

    def test_keeps_v10_r2(self):
        """v10 R2: normal and high prompts end with a fresh diff review (§9.3, Template B step 7)."""
        for phrase in [
            'At normal or high risk, HOW TO WORK ends with a fresh reviewer that reads the diff against DONE WHEN, even when the tests pass.',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_saves_in_the_guide_never_the_project(self):
        """/prompt writes into the user's project, or works around a refused write."""
        for phrase in ['git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel', "GUIDE/prompts/<project>/",
                       "Write nothing inside the current project.", "don't work around it",
                       "save the prompt in your scratchpad and give the user the one `cp` command"]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_keeps_v10_r3(self):
        """v10 R3: each hard constraint at high risk names its gate (Law 9)."""
        for phrase in [
            'At high risk, also name for each hard constraint the gate that enforces it (a hook, CI, a permission); a constraint written only in prose is a request, not a control.',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_saves_with_the_write_tool_not_bash(self):
        """The save goes through Bash, whose sandbox refuses writes outside the project (seen in a career-ops session)."""
        body = SKILL
        self.assertIn("with the Write tool, which creates the folder", body)
        self.assertIn("Don't use Bash", body)

    def test_keeps_v10_r4(self):
        """v10 R4: helper briefs say what is already ruled out and decided (Template C)."""
        for phrase in [
            'what is already ruled out and already decided',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_runs_the_consistency_pass_before_saving(self):
        """/prompt v5's consistency pass loses a check, so contradicting constraints come back."""
        for phrase in ["**Run the consistency pass before saving.**", "- Files: list every file the steps create or change",
                       "- Helpers: count the helpers, writers and reviewers the steps require",
                       "- Time and cost: multiply the number of items", "- Transformations: where a step changes data",
                       "- Skips: where items can be skipped", "- Targets: each check on CI, a deploy or a PR names the exact commit",
                       "- Evidence: a check that a source or link exists", "- Caps: word, file and source caps leave room",
                       "- Contradictions: no two lines demand opposite things",
                       "Never save a final draft that fails the consistency pass in step 8 or has a FAIL from the check in step 9.",
                       "make the lead's synthesis its own numbered step in HOW TO WORK", "name the exact break"]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_keeps_v10_r5(self):
        """v10 R5: loops are idempotent, least-privilege and capped (§11.3, Template H)."""
        for phrase in [
            'running twice sends, charges or creates nothing twice',
            'only the tools and permissions the task needs',
            'at most 15 lines, most important first',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

    def test_checks_run_in_order_before_saving(self):
        """The /brief port and v5 both added a step 8; the merge loses the order, or keeps two conflict checks or two save rules."""
        steps = ["8. **Run the consistency pass before saving.**", "9. **Run the check.**",
                 "10. **Get a fresh review before saving**", "11. **Save it in the guide, not the project.**", "12. **Hand over.**"]
        where = [SKILL.find(s) for s in steps]
        self.assertNotIn(-1, where, f"/prompt lost a step: {dict(zip(steps, where))}")
        self.assertEqual(where, sorted(where), "/prompt steps 8 to 12 are out of order")
        self.assertLess(SKILL.find("check_prompt.py"), where[2], "check_prompt.py must run before the fresh review")
        self.assertEqual(SKILL.count("Contradictions"), 1, "/prompt has more than one conflict check")
        self.assertEqual(len(re.findall(r"(?m)^- (?:Before saving|Never save)", SKILL)), 1, "/prompt has more than one save rule")

    def test_skill_and_check_change_together(self):
        """v10 R1: the skill asks for a risk line exactly when its check enforces one (c-9), so neither ships alone."""
        check = (ROOT / "skills" / "prompt" / "check_prompt.py").read_text(encoding="utf-8")
        self.assertEqual("`Risk: trivial`" in SKILL, "c-9" in check, "SKILL.md's risk line and check_prompt.py's c-9 must change together")

    def test_no_pre_run_shell_line(self):
        """/prompt gains a pre-run shell line, which stalled a claude -p session for /guide."""
        self.assertNotIn("!`", SKILL)


    def test_keeps_v10_r1_step5(self):
        """v10 R1: step 5 agrees with the trivial form."""
        for phrase in [
            'in this order (a trivial prompt may leave out CONTEXT):',
        ]:
            self.assertIn(phrase, SKILL, f"/prompt lost: {phrase!r}")

class PromptsNeverCommitted(unittest.TestCase):
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)

    def test_saved_prompts_are_ignored(self):
        """A saved prompt could be committed to the guide's repository."""
        for path in ["prompts/demo-project/2026-10-24-add-export.md", "prompts/loose-prompt.md"]:
            self.assertEqual(self.git("check-ignore", "-q", path).returncode, 0, f"{path} is not git-ignored; fix .gitignore")

    def test_prompts_readme_stays_tracked(self):
        """The prompts folder's README stops being tracked, so the folder's purpose is lost."""
        self.assertEqual(self.git("check-ignore", "-q", "prompts/README.md").returncode, 1, "prompts/README.md must not be ignored")
        self.assertIn("prompts/README.md", self.git("ls-files", "prompts/README.md").stdout)


class Scorer(unittest.TestCase):
    """tests/live/prompt/score.py, the rubric the battle test grades drafts with."""

    def score(self, scenario, text, *flags):
        path = ROOT / "build" / "test-tmp" / "prompt-fixtures" / f"{scenario}-{abs(hash(text))}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(KIT / "score.py"), str(KIT / "scenarios.json"), scenario, str(path), *flags],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        lines = {m.group(2): m.group(1) for m in re.finditer(r"^(PASS|FAIL) (p-\d+)", out.stdout, re.M)}
        total = re.search(r"SCORE (\d+)/(\d+)", out.stdout)
        return lines, (int(total.group(1)), int(total.group(2))), out.stdout

    def fixture(self, name):
        return (FIX / name).read_text(encoding="utf-8")

    def assert_only_fails(self, lines, expected, stdout):
        fails = {k for k, v in lines.items() if v == "FAIL"}
        self.assertEqual(fails, set(expected), f"expected FAIL on exactly {sorted(expected)}:\n{stdout}")

    def test_good_migration_scores_full(self):
        """A complete migration prompt loses points: the scorer misreads a good draft."""
        lines, (got, of), out = self.score("migration", self.fixture("good-migration.md"))
        self.assertEqual((got, of), (13, 13), out)

    def test_good_overnight_scores_full(self):
        """A complete overnight-loop prompt loses points."""
        lines, (got, of), out = self.score("overnight", self.fixture("good-overnight.md"))
        self.assertEqual((got, of), (12, 12), out)

    def test_missing_done_when_fails_the_check_rows(self):
        """A draft with no DONE WHEN block still passes the checks rubric."""
        text = re.sub(r"DONE WHEN\n(.*?\n)\n", "", self.fixture("good-migration.md"), flags=re.S)
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-2", "p-3", "p-4"}, out)

    def test_missing_receipt_fails_p6(self):
        """A draft that never asks for PASS, FAIL or NOT RUN passes the receipt check."""
        text = self.fixture("good-migration.md").split("REPORT")[0] + "REPORT\nSay what you did.\n"
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-6"}, out)

    def test_missing_budget_fails_p7(self):
        """A draft with no budget or limit passes the budget check."""
        text = self.fixture("good-migration.md").replace("BUDGET\n- At most 4 writers and 6 hours; stop and report when it runs out.\n\n", "")
        text = text.replace("disjoint batches of 50", "disjoint batches").replace("across 2 batches", "across batches")
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-7"}, out)

    def test_missing_test_immutability_fails_p10(self):
        """A draft that lets the builder edit tests passes the test-immutability check."""
        text = self.fixture("good-migration.md").replace(
            "- Do not edit or delete existing tests to make them pass; change only the runner syntax.\n", "")
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-10"}, out)

    def test_missing_batch_integration_fails_p21(self):
        """A parallel-writer draft with no one-at-a-time integration passes."""
        text = self.fixture("good-migration.md").replace(
            "3. The lead merges one batch at a time and reruns the full suite; a batch that turns the full run red is reverted.\n", "")
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-21"}, out)

    def test_a_deadline_is_not_a_runnable_check_p3(self):
        """A check like "done within 2 days" passes as runnable because it contains a digit."""
        text = self.fixture("good-migration.md").replace(
            "2. `git diff --name-status main -- '*.test.js'` lists no deleted test file.\n",
            "2. The migration is done within 2 days.\n")
        lines, _, out = self.score("migration", text)
        self.assert_only_fails(lines, {"p-3"}, out)

    def test_unrelated_never_does_not_satisfy_p18(self):
        """An unattended loop with no ban on irreversible actions passes because some other line says "do not"."""
        text = self.fixture("good-overnight.md").replace(
            "- Read-only on the code: never push, merge or close an issue.\n",
            "- Read-only on the code. Do not use emojis in comments.\n")
        lines, _, out = self.score("overnight", text)
        self.assert_only_fails(lines, {"p-18"}, out)

    def test_loop_without_stop_condition_fails_p15(self):
        """An overnight loop with no stop condition passes."""
        text = self.fixture("good-overnight.md").replace(
            "2. Stop when every new issue is handled or the budget runs out.\n", "2. Work through the new issues.\n")
        lines, _, out = self.score("overnight", text)
        self.assert_only_fails(lines, {"p-15"}, out)

    def test_lenient_reads_requirements_as_checks(self):
        """--lenient stops crediting a Requirements list, or strict mode starts crediting it."""
        text = self.fixture("requirements-format.md")
        strict, _, out = self.score("feature", text)
        self.assertEqual((strict["p-1"], strict["p-2"]), ("FAIL", "FAIL"), out)
        lenient, (got, of), out = self.score("feature", text, "--lenient")
        self.assertEqual((lenient["p-1"], lenient["p-2"]), ("PASS", "PASS"), out)
        self.assertEqual(got, of, out)

    def test_clean_install_is_not_vague(self):
        """"clean install" is marked as a vague adjective, or "clean" code is not."""
        good = self.fixture("good-migration.md").replace(
            "1. `npx vitest run` exits 0 and reports 400 test files.", "1. `npm ci` on a clean install, then `npx vitest run`, exits 0.")
        lines, _, out = self.score("migration", good)
        self.assertEqual(lines["p-4"], "PASS", out)
        vague = self.fixture("good-migration.md").replace(
            "1. `npx vitest run` exits 0 and reports 400 test files.", "1. The migrated code is clean and `npx vitest run` exits 0.")
        lines, _, out = self.score("migration", vague)
        self.assertEqual(lines["p-4"], "FAIL", out)


    def test_clean_git_status_is_a_state_not_vague(self):
        """A check that `git status` is clean is marked vague, so a precise check loses a point."""
        text = self.fixture("good-migration.md").replace(
            "2. `git diff --name-status main -- '*.test.js'` lists no deleted test file.",
            "2. `git diff --name-status main -- '*.test.js'` lists no deleted test file, and `git status` is clean.")
        lines, _, out = self.score("migration", text)
        self.assertEqual(lines["p-4"], "PASS", out)

    def test_per_writer_gate_counts_as_a_batch_gate(self):
        """A writer that runs only its own files before handing back is not credited with a batch gate."""
        text = self.fixture("good-migration.md").replace(
            "2. Each batch must pass its gate: `npx vitest run <batch>` exits 0.\n",
            "2. A writer converts its files, then runs only its own files under Vitest before handing back.\n")
        lines, _, out = self.score("migration", text)
        self.assertEqual(lines["p-20"], "PASS", out)


class LiveKit(unittest.TestCase):
    def test_live_scripts_parse_and_point_at_the_skill(self):
        """The opt-in battle test stops parsing or tests a copy of the skill that isn't the real one."""
        for name in ["run.sh", "interview.sh"]:
            r = subprocess.run(["bash", "-n", str(KIT / name)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{name}: {r.stderr}")
            self.assertIn("skills/prompt/SKILL.md", (KIT / name).read_text(encoding="utf-8"), f"{name} must test skills/prompt/SKILL.md")

    def test_results_are_recorded(self):
        """The battle test's results stop being recorded."""
        self.assertTrue((ROOT / "tests" / "results" / "prompt-battle.json").exists())

    def test_evaluation_is_frozen(self):
        """v8 is measured against exactly what was committed before any code changed (Codex review, blocker 2)."""
        live = ROOT / "tests" / "live"
        briefs = live / "prompt" / "briefs"
        for name in ["reviewer-round1", "reviewer-round2", "blind-pair", "audit", "must-haves", "judge",
                     "score-playbook", "score-external"]:
            text = (briefs / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("Do not try to work out which version or run produced a file.", text, name)
        self.assertNotIn("prompt-skill-review.md", (briefs / "score-external.md").read_text(encoding="utf-8"))
        self.assertEqual(len(re.findall(r"(?m)^\| P\d+ ", (live / "prompt" / "rubrics" / "playbook.md").read_text(encoding="utf-8"))), 47)
        must = (live / "prompt" / "must-haves.md").read_text(encoding="utf-8")
        for scenario in ["bugfix", "feature", "overnight", "research", "refactor", "migration"]:
            self.assertIn(f"## {scenario}", must)
        self.assertEqual(len(list((live / "prompt" / "baselines" / "v7").glob("*.md"))), 6)
        self.assertEqual(len([d for d in (live / "grill-prompt" / "baselines" / "v7").iterdir() if d.is_dir()]), 6)

    def test_r7_is_na_for_the_small_fix(self):
        """§5.3 and Template B ask a small fix for a goal, checks and a receipt only, so R7 can't fail it (v9 plan, D5)."""
        rubric = (ROOT / "tests" / "live" / "grill-prompt" / "rubric.md").read_text(encoding="utf-8")
        r7 = next(l for l in rubric.splitlines() if l.startswith("| R7 "))
        self.assertIn("N/A for every run of Dump 1", r7)
        self.assertIn("who struggles, what it costs", r7, "R7 must still apply to Dumps 2 and 3")


class PromptCheck(unittest.TestCase):
    """skills/prompt/check_prompt.py, the deterministic check /prompt runs before its fresh review.

    Each case comes from a failure the grill-then-prompt dry runs found (tests/live/grill-prompt/results.md).
    """
    GOOD = (ROOT / "tests" / "fixtures" / "prompt-check" / "good.md").read_text(encoding="utf-8")
    REQUEST = ROOT / "tests" / "fixtures" / "prompt-check" / "request.md"

    def check(self, text):
        path = ROOT / "build" / "test-tmp" / "prompt-check" / f"{abs(hash(text))}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(ROOT / "skills" / "prompt" / "check_prompt.py"), str(path),
                              "--source", str(self.REQUEST)], capture_output=True, text=True)
        lines = {m.group(2): m.group(1) for m in re.finditer(r"^(PASS|FAIL|WARN) (c-\d)", out.stdout, re.M)}
        return out, lines

    def edited(self, old, new):
        self.assertIn(old, self.GOOD, "the good fixture changed; update this test")
        return self.GOOD.replace(old, new)

    def assert_only(self, text, check, level):
        out, lines = self.check(text)
        bad = {k: v for k, v in lines.items() if v != "PASS"}
        self.assertEqual(bad, {check: level}, out.stdout)
        self.assertEqual(out.returncode, 1 if level == "FAIL" else 0, out.stdout)

    def test_good_prompt_passes_every_check(self):
        out, lines = self.check(self.GOOD)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(sorted(lines.values()), ["PASS"] * 9, out.stdout)

    def test_missing_part_fails_c1(self):
        self.assert_only(self.edited("## BUDGET\nAbout an hour. ASSUMED: no helpers.\n\n", ""), "c-1", "FAIL")

    def test_six_done_when_checks_fail_c2(self):
        extra = "".join(f"{n}. Given the CLI, when you run it, then it exits.\n" for n in range(3, 7))
        self.assert_only(self.edited("then it finds nothing.\n", "then it finds nothing.\n" + extra), "c-2", "FAIL")

    def test_two_gaps_on_one_line_fail_c3(self):
        """Round 3: a run merged two gaps into one UNKNOWN line to stay under the cap."""
        self.assert_only(self.edited("where the help text lives;", "where the help text lives, and whether it is generated;"), "c-3", "FAIL")

    def test_four_unknowns_without_not_ready_fail_c4(self):
        """Round 3: a prompt with 4 UNKNOWN lines said 'not ready' only in chat, never in the file."""
        more = "".join(f"- UNKNOWN: gap {n}; nobody knows.\n" for n in range(2, 5))
        text = self.edited("- ASSUMED: the change stays uncommitted.\n", "- ASSUMED: the change stays uncommitted.\n" + more)
        self.assert_only(text, "c-4", "FAIL")
        out, lines = self.check(text.replace("# Prompt:", "Status: not ready to run.\n\n# Prompt:"))
        self.assertEqual(lines.get("c-4"), "PASS", out.stdout)

    def test_relative_term_fails_c5_unless_quoted_or_marked(self):
        """Rounds 1 and 3: 'about a month in', 'recent' and 'today's' reached the prompt unresolved."""
        self.assert_only(self.edited("Edit only the help file.", "Edit only the help file, by next Friday."), "c-5", "FAIL")
        for ok in ['Edit only the help file. The user said "by next Friday".', "Edit only the help file.\nASSUMED: done by next Friday.",
                   "Edit only the help file. Report as soon as it passes."]:
            out, lines = self.check(self.edited("Edit only the help file.", ok))
            self.assertEqual(lines.get("c-5"), "PASS", ok + "\n" + out.stdout)

    def test_unsourced_figure_warns_c6_but_does_not_fail(self):
        """Rounds 1 to 3: the writer picked caps such as '3 helpers' and presented them as the user's."""
        self.assert_only(self.edited("About an hour. ASSUMED: no helpers.", "About an hour, with three helpers."), "c-6", "WARN")
        for ok in ["About an hour. ASSUMED: three helpers.", "About an hour. ASSUMED: no helpers.\nEach brief returns about 40 words per field."]:
            out, lines = self.check(self.edited("About an hour. ASSUMED: no helpers.", ok))
            self.assertEqual(lines.get("c-6"), "PASS", ok + "\n" + out.stdout)

    def test_old_400_word_cap_is_not_a_skill_value(self):
        """v5 caps helper returns at about 40 words per field; a leftover "400 words" must not pass as set by the skill."""
        text = self.edited("About an hour. ASSUMED: no helpers.", "About an hour. ASSUMED: no helpers.\nEach brief returns under 400 words.")
        self.assert_only(text, "c-6", "WARN")


    def test_skill_set_output_cap_is_not_a_guess(self):
        """v10 R5: Template H caps a loop's output at 15 lines, so a prompt repeating it traces to the skill."""
        text = self.edited("About an hour. ASSUMED: no helpers.", "About an hour. ASSUMED: no helpers.\nThe report is at most 15 lines, most important first.")
        out, lines = self.check(text)
        self.assertEqual(lines.get("c-6"), "PASS", out.stdout)

    def test_a_figure_listed_once_as_assumed_traces_everywhere(self):
        """v7 lists each chosen value once; using it plainly elsewhere must not warn under c-6."""
        text = self.edited("About an hour. ASSUMED: no helpers.", "About an hour, with three helpers.")
        text = text.replace("- ASSUMED: the change stays uncommitted.", "- ASSUMED: the change stays uncommitted.\n- ASSUMED: three helpers.")
        out, lines = self.check(text)
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertEqual(sorted(lines.values()), ["PASS"] * 9, out.stdout)

    def test_a_figure_marked_twice_warns_c7(self):
        """Round 10: v6 drafts restated each cap as ASSUMED in two or three places, and reviewers called it noise."""
        text = self.edited("About an hour. ASSUMED: no helpers.", "About an hour. ASSUMED: three helpers at most.")
        self.assert_only(text.replace("- ASSUMED: the change stays uncommitted.", "- ASSUMED: three helpers."), "c-7", "WARN")

    def test_a_check_resting_on_an_unknown_warns_c8(self):
        """Round 4: a main check used "live", a term an UNKNOWN line said nobody had defined."""
        named = self.edited("names the new flag and exits 0", "names the new flag, which is UNKNOWN, and exits 0")
        self.assert_only(named, "c-8", "WARN")
        quoted = self.edited("where the help text lives;", 'what the "new flag" is called;')
        self.assert_only(quoted.replace("names the new flag", 'names the "new flag"'), "c-8", "WARN")


    def test_trivial_needs_every_other_template_b_part(self):
        """v10 R1: only CONTEXT is optional at trivial risk; GOAL, DONE WHEN, CONSTRAINTS and REPORT stay required."""
        trivial = self.GOOD.replace("Risk: normal", "Risk: trivial")
        for part in ("GOAL", "DONE WHEN", "CONSTRAINTS", "REPORT"):
            start = trivial.index(f"## {part}")
            nxt = trivial.find("## ", start + 3)
            out, lines = self.check(trivial[:start] + (trivial[nxt:] if nxt != -1 else ""))
            self.assertEqual(lines.get("c-1"), "FAIL", part + "\n" + out.stdout)
            self.assertIn(part, out.stdout)

    def test_risk_line_after_goal_fails_c9(self):
        """v10 R1: the risk line sits above the title; one written after GOAL does not count."""
        text = self.edited("Risk: normal\n\n", "").replace("## DONE WHEN", "Risk: normal\n\n## DONE WHEN", 1)
        out, lines = self.check(text)
        self.assertEqual(lines.get("c-9"), "FAIL", out.stdout)

    def test_inline_part_labels_count_as_parts(self):
        """Dry run round 5: a prompt that wrote "GOAL: <sentence>" on one line failed c-1 as if GOAL were missing."""
        text = self.GOOD
        for part in ("GOAL", "BUDGET", "REPORT"):
            text = re.sub(rf"## {part}\n", f"{part}: ", text)
        self.assertIn("GOAL: Every `--help` output", text)
        out, lines = self.check(text)
        self.assertEqual(sorted(lines.values()), ["PASS"] * 9, out.stdout)

    def test_trivial_may_leave_out_context(self):
        """v10 R1: Template B's trivial form makes CONTEXT optional, and only at trivial risk."""
        start = self.GOOD.index("## CONTEXT")
        end = self.GOOD.index("## ", start + 3)
        bare = self.GOOD[:start] + self.GOOD[end:]
        out, lines = self.check(bare.replace("Risk: normal", "Risk: trivial"))
        self.assertEqual(lines.get("c-1"), "PASS", out.stdout)
        self.assert_only(bare, "c-1", "FAIL")

    def test_trivial_keeps_template_b_parts(self):
        """v10 R1: the trivial form still needs BUDGET, STOP AND ASK IF and HOW TO WORK (v8's short form dropped them)."""
        trivial = self.GOOD.replace("Risk: normal", "Risk: trivial")
        for part in ("BUDGET", "STOP AND ASK IF", "HOW TO WORK"):
            start = trivial.index(f"## {part}")
            end = trivial.index("## ", start + 3)
            out, lines = self.check(trivial[:start] + trivial[end:])
            self.assertEqual(lines.get("c-1"), "FAIL", part + "\n" + out.stdout)
            self.assertIn(part, out.stdout)

    def test_missing_risk_line_fails_c9(self):
        self.assert_only(self.edited("Risk: normal\n\n", ""), "c-9", "FAIL")

    def test_old_low_label_fails_c9(self):
        """v8's 'low' is not one of Template L's sizes."""
        self.assert_only(self.edited("Risk: normal", "Risk: low"), "c-9", "FAIL")

    def test_risk_line_ignores_case_bold_and_bullets(self):
        for line in ["**Risk:** Normal", "Risk: NORMAL", "risk: normal", "- Risk: normal", "RISK: normal"]:
            out, lines = self.check(self.edited("Risk: normal", line))
            self.assertEqual(lines.get("c-9"), "PASS", line + "\n" + out.stdout)

    def test_bulleted_done_when_checks_are_counted(self):
        """Dry run round 5: DONE WHEN written as bullets counted 0 checks, while sub-bullets under a numbered check stay part of it."""
        bullets = self.edited("1. Given the CLI", "- Given the CLI").replace("2. Given the same", "- Given the same")
        out, lines = self.check(bullets)
        self.assertEqual(lines.get("c-2"), "PASS", out.stdout)
        self.assertIn("2 checks", out.stdout)
        nested = self.edited("then it finds nothing.\n", "then it finds nothing.\n- Run `cli --help | grep -c old`.\n- Expect 0.\n")
        out, lines = self.check(nested)
        self.assertIn("2 checks", out.stdout, "bullets under a numbered check must not count as checks")


if __name__ == "__main__":
    unittest.main()
