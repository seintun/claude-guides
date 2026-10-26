"""Critical content pins: the meaning-bearing sentences the guide stands on.

Added after the second review round, whose 56 adversarial edits found these could be flipped or
dropped while every other test stayed green. Each pin is an exact phrase or a small fixed set.
Changing one on purpose means changing its pin in the same commit, where a reviewer sees both.

Run: python3 -I tests/test_critical.py   (or the whole suite: tests/run.sh)
"""
import json
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import section  # noqa: E402

PB_LINES, PB = section.index(section.PLAYBOOK)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def body(sid):
    _, start, end = PB[sid]
    return "\n".join(PB_LINES[start:end])


def router_rows():
    block = read("ENTRY.md").split("## Scenario router", 1)[1].split("\n## ", 1)[0]
    return {int(m.group(1)): [c.strip() for c in m.group(2).split("|")]
            for m in re.finditer(r"^\| (\d+) \|(.*)\|\s*$", block, re.M)}


class RouterMeaning(unittest.TestCase):
    ROWS = router_rows()
    # Row number -> a word its scenario label must keep, so two rows can't swap meanings.
    LABELS = {1: "Vague idea", 2: "New feature", 3: "Bug fix", 4: "Refactor", 5: "Migration", 6: "harness",
              7: "hooks", 8: "Overnight", 9: "Code review", 10: "Research", 11: "Stuck agent", 12: "Cost",
              13: "several repos", 14: "Onboard", 15: "agent-ready issue", 16: "Retro", 17: "Security", 18: "Several writers", 19: "prompt"}
    # Rows whose core section is the reason they exist.
    CORE_IDS = {1: ["5.1", "5.2"], 7: ["9.5", "F"], 8: ["11.3"], 9: ["law-7"], 11: ["14", "cs:3"], 16: ["13"], 17: ["10.1"]}

    def test_each_row_keeps_its_scenario(self):
        """Two router rows swap labels, so a request lands on the wrong advice."""
        for n, word in self.LABELS.items():
            self.assertIn(word.lower(), self.ROWS[n][0].lower(), f"row {n} label no longer names '{word}'")

    def test_core_rows_keep_their_core_sections(self):
        """A row drops the section it exists for, together with its test scenario."""
        for n, ids in self.CORE_IDS.items():
            for sid in ids:
                self.assertRegex(self.ROWS[n][1], rf"(?<![\w.:-]){re.escape(sid)}(?![\w.])", f"row {n} dropped {sid}")

    def test_review_never_approves_and_loops_keep_caps(self):
        """Row outputs flip: an agent review approves the PR, or a loop loses its caps."""
        self.assertIn("never approves", self.ROWS[9][4], "row 9 must say the agent review never approves")
        for phrase in ("stop condition", "retry cap", "cost ceiling"):
            self.assertIn(phrase, self.ROWS[8][4], f"row 8 output dropped '{phrase}'")


class PlaybookMeaning(unittest.TestCase):
    def test_law_7_keeps_the_reviewer_away_from_the_authors_reasoning(self):
        """Law 7's body is flipped so the builder reviews its own work."""
        b = body("law-7")
        self.assertIn("reviewers get the artifact and the criteria, never the author's reasoning", b)
        self.assertNotRegex(b, r"(?i)builder (reviews|checks|grades) its own", "Law 7 now lets the builder check itself")

    def test_law_9_keeps_controls_in_code(self):
        """Law 9's body is weakened to say prose is enough."""
        b = body("law-9")
        self.assertIn("lives in hooks, CI, permissions or the sandbox, not only in prose", b)
        self.assertIn("Prompt-level guardrails are not reliable", b)

    def test_guardrails_block_keeps_every_deny(self):
        """Template F's guardrails block loses deny rules for destructive commands."""
        f = body("F")
        for rule in ["Bash(git push --force:*)", "Bash(git push -f:*)", "Bash(git push --force-with-lease:*)", "Bash(rm -rf:*)",
                     "Bash(terraform apply:*)", "Bash(kubectl delete:*)", "Bash(vercel --prod:*)"]:
            self.assertIn(f'"{rule}"', f, f"Template F's guardrails block no longer denies {rule}")
        self.assertIn('"ask": ["Bash(git push:*)"]', f)

    def test_evidence_tags_are_not_stripped(self):
        """Evidence grades are stripped from many claims, a few at a time below the global floor."""
        base = json.loads(read("tests/baselines/playbook.json"))["evidence_tags"]
        sys.path.insert(0, str(ROOT / "tests"))
        import update_baselines  # the same counting rule the baseline uses
        counts = update_baselines.evidence_tags(read("playbook/agent-harness-playbook.md"))
        for g, was in base.items():
            now = counts.get(g, 0)
            self.assertGreaterEqual(now, was - 3, f"[{g}] tags fell from {was} to {now}; restore them, or run "
                                    "tests/update_baselines.py --allow-shrink if the removal is intended")


class LayersAgree(unittest.TestCase):
    def test_stop_hook_blocks_with_exit_2_everywhere(self):
        """The wiki changes the Stop hook's blocking exit code, so it no longer matches the playbook."""
        self.assertIn("exit 2", read("wiki/verify.md"))
        self.assertNotRegex(read("wiki/verify.md"), r"(?i)(returns|confirm) exit 1\b")
        self.assertIn("exits with code 2 blocks the stop", body("law-9"))

    def test_index_never_marks_pass_without_evidence(self):
        """The orchestration index's evidence rule is reversed."""
        self.assertIn("Never mark PASS without evidence.", read("orchestration-index.md"))

    def test_llms_txt_sends_outside_sessions_to_entry(self):
        """llms.txt calls ENTRY.md deprecated or points sessions at the whole playbook."""
        text = read("llms.txt")
        self.assertIn("a session in another project starts at ENTRY.md", text)
        self.assertNotRegex(text, r"(?i)ENTRY\.md[^\n]{0,40}deprecated|deprecated[^\n]{0,40}ENTRY\.md")
        self.assertNotRegex(text, r"(?i)(read|load) the whole playbook(?! when)", "llms.txt tells sessions to load the whole playbook")

    def test_every_command_runs_python_isolated(self):
        """Commands lose `python3 -I`, so a planted module in the user's project can run."""
        for path in ["skills/guide/SKILL.md", "skills/guide/snippet.md", "skills/guide/prompt.md", "ENTRY.md"]:
            bad = re.findall(r"python3 (?!-I)\S+", read(path))
            self.assertFalse(bad, f"{path} runs python3 without -I: {bad}")


class ReviewsEnd(unittest.TestCase):
    """The bounded-review rule: every needed review runs once and ends (playbook 9.2)."""

    def test_trust_ladder_keeps_the_bounded_review_rule(self):
        """Reviews lose their stop rule and loop until no finding is left."""
        b = body("9.2")
        for phrase in ["**Bounded review.**", "A finding blocks only with evidence", '"No blockers" is a valid result.',
                       "Only the reviewer that raised it, or a human, can close it any other way",
                       "whether the fix adds a new one", "A large fix gets a full re-review",
                       "reads the code, not only the plan",
                       "There is no round 3: after two rounds a human decides",
                       "never both"]:
            self.assertIn(phrase, b, f"9.2 lost: {phrase}")

    def test_template_b_bounds_its_reviews(self):
        """Template B goes back to forcing three objections or reviewing without a round cap."""
        b = body("B")
        self.assertIn("answer up to 3 blocking objections (none is a valid result)", b)
        self.assertIn("A review gets two rounds at most; after that, stop and let me decide.", b)
        self.assertNotIn("3 strongest objections", b)

    def test_rule_keeps_its_evidence(self):
        """The bounded-review rule loses the research it rests on."""
        self.assertIn("research/bounded-review-evidence.md", body("9.2"))
        self.assertIn("Reviews converge in a round or two", body("19.1"))
        note = read("research/bounded-review-evidence.md")
        for marker in ["## How the rule maps to the evidence", "## Not used, and why", "## Limits", "arxiv.org/abs/2608.27442"]:
            self.assertIn(marker, note)

    def test_entry_and_prompt_carry_the_bound(self):
        """Sessions routed by ENTRY.md or prompts written by /prompt lose the review bound."""
        self.assertIn("**Reviews end.**", read("ENTRY.md"))
        self.assertIn("after two rounds the user decides", read("skills/prompt/SKILL.md"))
        for path in ["ENTRY.md", "orchestration-index.md", "wiki/verify.md", "playbook/agent-harness-playbook.md"]:
            self.assertNotRegex(read(path), r"(?i)(3|three) strongest objections", f"{path} forces three objections again")


class SkillMeaning(unittest.TestCase):
    def test_prompt_skill_writes_prompts_not_work(self):
        """/prompt starts doing the task, writes into the user's project, or runs on its own."""
        text = read("skills/prompt/SKILL.md")
        head = text.split("---", 2)[1]
        self.assertRegex(head, r"(?m)^name: prompt$")
        self.assertRegex(head, r"(?m)^disable-model-invocation: true$", "/prompt must run only when typed")
        self.assertNotRegex(head, r"allowed-tools:.*(Write|Edit)", "/prompt must not pre-approve writes")
        for phrase in ["You write the prompt; you do not do the task.", 'git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel',
                       "GUIDE/prompts/<project>/", "Write nothing inside the current project.", "NOT RUN is not PASS.",
                       "don't work around it"]:
            self.assertIn(phrase, text, f"/prompt lost: {phrase}")

    def test_guide_names_thin_gaps(self):
        """/guide stops telling sessions to say what the playbook lacks for thin rows."""
        self.assertIn("If the row is marked thin, say what the playbook lacks", read("skills/guide/SKILL.md"))

    def test_grill_keeps_coverage_and_plain_text_fallback(self):
        """/grill loses its coverage list or its fallback when AskUserQuestion is missing."""
        text = read("skills/grill/SKILL.md")
        self.assertIn("**Cover the ground:**", text)
        self.assertIn("Without it, ask in plain text with options lettered A to D, recommendation first.", text)


if __name__ == "__main__":
    unittest.main()
