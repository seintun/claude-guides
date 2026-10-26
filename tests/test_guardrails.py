"""Content guards: pin what the guide says, not only which headings it has.

The shape tests (test_playbook.py, test_router.py, test_docs.py) pass when a heading survives. These
pass only when the advice under it survives too. Each class guards one way an edit can hollow or flip
the guiding star while every heading stays in place.

  SectionToolFidelity  tools/section.py prints the exact text of every section, so a session that loads
                       a section reads all of it and nothing else.
  SectionBaseline      no section shrinks below 70% of its baselined words, and no section's grades are
                       promoted without a new source (tests/baselines/playbook.json).
  KeyPhrases           the sentences that carry the method stay word for word: Templates B, F, H, I, K and M,
                       the receipt format, Laws 2, 7 and 9, the cheat sheet's stuck-signs table.
  EntryPins            ENTRY.md keeps its router, phase table, rules, folder rule and thin-row gaps, and never
                       tells a session to load the whole playbook.
  RulesAndRunbooks     AGENTS.md keeps its rules, every runbook keeps a real checklist and steps, and "NOT RUN
                       is not PASS" is said in every layer and contradicted nowhere.
  SkillSafety          /guide asks for no more tools than it needs, /grill cannot write or run itself, and the
                       installer touches nothing but its own symlink.
  CompendiumOffline    the compendium loads nothing from the network.

A pin is a contract. If you change one of these sentences on purpose, update the pin in this file in the same
commit and say why in the message. If a section shrinks on purpose, run
python3 -I tests/update_baselines.py --allow-shrink and commit the new baseline with the change.

Run: python3 -I tests/test_guardrails.py -v   (or the whole suite: tests/run.sh)
Temp folders go under TEST_TMP when it is set (tests/run.sh sets it).
"""
import concurrent.futures
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
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))
import section  # noqa: E402  (only to list the ids the tool claims to serve)
import update_baselines as ub  # noqa: E402

PIN_CHANGED = "If the change is intended, update the pin in tests/test_guardrails.py in the same commit."
BASELINE_CHANGED = ("If the change is intended, run python3 -I tests/update_baselines.py --allow-shrink "
                    "and commit the new baseline in the same commit.")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def short(items, limit=12):
    items = list(items)
    extra = f"\n  ... and {len(items) - limit} more" if len(items) > limit else ""
    return "\n  " + "\n  ".join(str(x) for x in items[:limit]) + extra


# ---------------------------------------------------------------------------------------------
# An independent reader of headings and sections. It does not use tools/section.py, so a bug in
# that tool cannot hide from the fidelity test, and the pins below read the file itself.
# ---------------------------------------------------------------------------------------------

def md_headings(lines):
    """(line index, level, title) for each ATX heading outside a fenced code block."""
    out, fence = [], None
    for i, line in enumerate(lines):
        opening = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence:
            if opening and opening.group(1)[0] == fence[0] and len(opening.group(1)) >= fence[1] \
                    and line.strip().strip(fence[0]) == "":
                fence = None
            continue
        if opening:
            fence = (opening.group(1)[0], len(opening.group(1)))
            continue
        m = re.match(r"(#{1,6})[ \t]+(\S.*?)[ \t]*$", line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def id_of(title, cheatsheet):
    """The id a heading answers to ("9.5", "17A", "F", "law-7", "cs:3"), or None."""
    if cheatsheet:
        m = re.match(r"(\d+)\.?\s", title)
        return f"cs:{m.group(1)}" if m else None
    m = re.match(r"Law (\d+)\.\s", title)
    if m:
        return f"law-{m.group(1)}"
    m = re.match(r"([A-M])\.\s", title)
    if m:
        return m.group(1)
    m = re.match(r"(\d+[A-Z]?(?:\.\d+)?)\.?\s", title)
    return m.group(1) if m else None


def read_sections(path, cheatsheet=False):
    """(lines, {id: (title, first line index, index after the last line)}); the first heading with an id wins."""
    lines = path.read_text(encoding="utf-8").splitlines()
    level_at = {i: level for i, level, _ in md_headings(lines)}
    ids = {}
    for i, level, title in md_headings(lines):
        sid = id_of(title, cheatsheet)
        if sid is None or sid in ids:
            continue
        end = next((j for j in range(i + 1, len(lines)) if j in level_at and level_at[j] <= level), len(lines))
        ids[sid] = (title, i, end)
    return lines, ids


PB_LINES, PB = read_sections(ub.PLAYBOOK)
CS_LINES, CS = read_sections(ub.CHEATSHEET, cheatsheet=True)


def pb_body(sid):
    """The text under a playbook heading (heading line excluded), including its subsections."""
    _, start, end = PB[sid]
    return "\n".join(PB_LINES[start + 1:end])


def cs_body(sid):
    _, start, end = CS[sid]
    return "\n".join(CS_LINES[start + 1:end])


def fenced(text, lang=None):
    """The text of each ``` block in a string, optionally only those with this language tag."""
    return [m.group(2) for m in re.finditer(r"^```(\w*)[^\n]*\n(.*?)^```", text, re.S | re.M) if lang is None or m.group(1) == lang]


class Pinned(unittest.TestCase):
    """Shared helpers for tests that pin exact phrases."""

    def need(self, text, phrase, where, why):
        self.assertIn(phrase, text, f"{where} no longer contains {phrase!r}: {why} {PIN_CHANGED}")


# ---------------------------------------------------------------------------------------------
# 1. section.py prints exactly what the file says
# ---------------------------------------------------------------------------------------------

class SectionToolFidelity(unittest.TestCase):
    TOOL = ROOT / "tools" / "section.py"

    def run_tool(self, sid):
        return subprocess.run([sys.executable, "-I", str(self.TOOL), sid], capture_output=True, text=True, timeout=60)

    def test_ids_the_tool_serves_are_the_ids_in_the_files(self):
        """section.py drops an id, or serves one the files do not have, so a router row loads the wrong text."""
        served = set(section.index(section.PLAYBOOK)[1]) | set(section.index(section.CHEATSHEET, cheatsheet=True)[1])
        have = set(PB) | set(CS)
        self.assertEqual(served, have,
                         "tools/section.py and the files disagree about the section ids.\n"
                         f"  only in the tool: {sorted(served - have)}\n  only in the files: {sorted(have - served)}\n"
                         "Fix tools/section.py key_of(), or the heading. If the id scheme changed on purpose, update id_of() in tests/test_guardrails.py.")

    def test_every_section_prints_its_exact_text(self):
        """section.py truncates, pads or mis-slices a section, so a session loads partial or wrong advice."""
        jobs = [(sid, "playbook/claude-cheat-sheet.md", CS_LINES, CS[sid]) for sid in CS] + \
               [(sid, "playbook/agent-harness-playbook.md", PB_LINES, PB[sid]) for sid in PB]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda j: self.run_tool(j[0]), jobs))
        bad = []
        for (sid, _, lines, (title, start, end)), r in zip(jobs, results):
            if r.returncode != 0:
                bad.append(f"{sid}: section.py exited {r.returncode}: {r.stderr.strip()[:100]}")
                continue
            head, _, printed = r.stdout.partition("\n")
            want = "\n".join(lines[start:end]).rstrip().split("\n")
            got = printed.rstrip().split("\n")
            span = re.search(r"lines (\d+)-(\d+)", head)
            if not head.startswith("<!--") or not span or (int(span.group(1)), int(span.group(2))) != (start + 1, end):
                bad.append(f"{sid}: the first line should be a comment naming lines {start + 1}-{end}, got {head!r}")
            if got != want:
                k = next((n for n in range(min(len(got), len(want))) if got[n] != want[n]), min(len(got), len(want)))
                at = lambda seq: repr(seq[k][:70]) if k < len(seq) else "<end of output>"
                bad.append(f"{sid}: printed {len(got)} lines, the file has {len(want)}; first difference at body line {k + 1}: "
                           f"printed {at(got)}, file {at(want)}")
        self.assertFalse(bad, f"tools/section.py prints something other than the section's exact text for {len(bad)} message(s):" + short(bad) +
                         "\nA section must run from its heading to the line before the next heading of the same or higher level, "
                         "including the last line. Fix tools/section.py. If the slicing rule changed on purpose, update read_sections() here.")


# ---------------------------------------------------------------------------------------------
# 2. Per-section baseline: hollowing and grade promotion
# ---------------------------------------------------------------------------------------------

class SectionBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(ub.BASELINE.read_text(encoding="utf-8"))
        for field in ub.SECTION_KEYS:
            if not cls.base.get(field):
                raise AssertionError(f"tests/baselines/playbook.json has no '{field}' record. Run python3 -I tests/update_baselines.py and commit it.")
        cls.now = {"sections": ub.section_stats(ub.PLAYBOOK.read_text(encoding="utf-8")),
                   "cheatsheet_sections": ub.section_stats(ub.CHEATSHEET.read_text(encoding="utf-8"))}

    def test_no_section_is_hollowed_out(self):
        """A section keeps its heading but loses most of its text, so the advice under it is gone."""
        low = []
        for field, label in (("sections", "playbook"), ("cheatsheet_sections", "cheat sheet")):
            for key, was in self.base[field].items():
                cur = self.now[field].get(key)
                if cur is not None and cur["words"] < ub.word_floor(was["words"]):
                    low.append(f"{label} {key}: {was['words']} words -> {cur['words']} (floor {ub.word_floor(was['words'])})")
        self.assertFalse(low, f"{len(low)} section(s) lost more than {100 - ub.KEEP_PERCENT}% of their words:" + short(low) +
                         "\nRestore the text under each heading. " + BASELINE_CHANGED)

    def test_no_grade_is_promoted_without_a_source(self):
        """A claim's grade is raised from [D], [S] or [R] to [P] by editing the tag, with no new primary source."""
        found = []
        for field, label in (("sections", "playbook"), ("cheatsheet_sections", "cheat sheet")):
            found += [f"{label} {m}" for m in ub.promotions(self.base[field], self.now[field])]
        self.assertFalse(found, "grades promoted without a new source:" + short(found) +
                         "\nA [P] claim needs a primary source in section 20. Put the old grade back, or add the source and get a fact check "
                         "(AGENTS.md, Facts). If the promotion is justified, run python3 -I tests/update_baselines.py and commit the baseline.")

    def test_no_cheat_sheet_heading_removed(self):
        """A cheat-sheet section is removed or renamed, and the router's cs:N ids die."""
        gone = [h for h in self.base["cheatsheet_sections"] if h not in self.now["cheatsheet_sections"]]
        self.assertFalse(gone, "baselined cheat-sheet headings are gone from playbook/claude-cheat-sheet.md:" + short(gone) +
                         "\nRestore them. " + BASELINE_CHANGED)


# ---------------------------------------------------------------------------------------------
# 3. The sentences that carry the method
# ---------------------------------------------------------------------------------------------

class KeyPhrases(Pinned):
    def test_template_b_keeps_its_stop_rules(self):
        """Template B (the task contract) loses the block that makes an agent stop, budget and report honestly."""
        b = pb_body("B")
        for phrase, why in [
            ("STOP AND ASK ME IF", "the list of cases where the agent must stop and ask."),
            ("NOT RUN is not PASS", "a skipped check must not read as a pass."),
            ("If the same check fails twice for the same reason, stop and ask for a second opinion", "the two-strikes rule."),
            ("BUDGET", "the cap that ends a run."),
        ]:
            with self.subTest(phrase=phrase):
                self.need(b, phrase, "Template B", why)

    def test_receipt_format_keeps_pass_fail_not_run(self):
        """The receipt format (§9.4) is emptied or loses a status, so 'done' needs no proof or hides a skipped check."""
        body = pb_body("9.4")
        for status in ("PASS", "FAIL", "NOT RUN"):
            with self.subTest(status=status):
                self.assertRegex(body, rf"\b{status}\b",
                                 f"§9.4 Receipt format no longer shows the status {status}. {PIN_CHANGED}")

    def test_not_run_is_not_pass_is_stated_in_the_playbook(self):
        """The rule 'NOT RUN is not PASS' disappears from the delivery phases and the task contract."""
        for sid in ("5.4", "B"):
            with self.subTest(section=sid):
                self.need(pb_body(sid), "NOT RUN is not PASS", f"playbook §{sid}" if sid[0].isdigit() else f"Template {sid}",
                          "a skipped check must not read as a pass. (§9.3 holds the honesty rules but never named NOT RUN; "
                          "§5.4 and Template B carry the sentence.)")

    def test_three_laws_keep_their_titles(self):
        """Law 2, 7 or 9 is reworded, so the router's law-N ids load advice that no longer matches their promise."""
        for sid, title in [("law-2", "Law 2. Verification multiplies quality"),
                           ("law-7", "Law 7. Separate the maker from the checker"),
                           ("law-9", "Law 9. Enforce with code; request with words")]:
            with self.subTest(law=sid):
                self.assertEqual(PB[sid][0], title, f"the heading for {sid} changed from {title!r} to {PB[sid][0]!r}. "
                                                    "ENTRY.md's rules cite these laws by what they say. " + PIN_CHANGED)

    def test_template_m_stays_read_only_and_pinned(self):
        """Template M (the CI review) gets write permission on the repo or floating action versions, so an injected PR can act."""
        yaml = "\n".join(l for l in "\n".join(fenced(pb_body("M"), "yaml")).splitlines() if not l.lstrip().startswith("#"))
        self.assertTrue(yaml.strip(), "Template M has no yaml block. " + PIN_CHANGED)
        self.assertRegex(yaml, r"(?m)^\s*contents:\s*read\s*(#.*)?$", "Template M must grant 'contents: read'. " + PIN_CHANGED)
        self.assertRegex(yaml, r"(?m)^\s*pull-requests:\s*write\b", "Template M must grant 'pull-requests: write' to post its review. " + PIN_CHANGED)
        self.assertNotRegex(yaml, r"(?m)^\s*contents:\s*write\b", "Template M grants 'contents: write'; a review job must never write code. " + PIN_CHANGED)
        refs = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s@]+)@(\S+)", yaml)
        self.assertGreaterEqual(len(refs), 2, "Template M should pin at least checkout and the review action with 'uses:'. " + PIN_CHANGED)
        loose = [f"{name}@{ref}" for name, ref in refs if ref != "<full-commit-sha>" and not re.fullmatch(r"[0-9a-f]{40}", ref)]
        self.assertFalse(loose, "Template M uses actions by tag or branch, not by commit:" + short(loose) +
                         "\nPin each to @<full-commit-sha> (or a real 40-character SHA): a moving tag lets a compromised release run with the job's secrets. " + PIN_CHANGED)

    def test_template_f_guardrails_deny_the_irreversible_and_ask_before_pushing(self):
        """Template F's guardrails block stops denying force-push or rm -rf, or stops asking before a push."""
        blocks = [b for b in fenced(pb_body("F"), "json") if '"ask"' in b]
        self.assertEqual(len(blocks), 1, f"Template F should hold exactly one json block with an 'ask' list, found {len(blocks)}. " + PIN_CHANGED)
        perms = json.loads(blocks[0])["permissions"]

        def commands(rules):
            return {m.group(1) for r in rules if (m := re.fullmatch(r"Bash\((.*?)(?::\*| \*)?\)", r))}

        deny, ask = commands(perms.get("deny", [])), commands(perms.get("ask", []))
        for cmd in ("git push --force", "git push -f", "rm -rf"):
            with self.subTest(deny=cmd):
                self.assertIn(cmd, deny, f"Template F's deny list no longer blocks Bash({cmd}:*); it has {sorted(deny)}. {PIN_CHANGED}")
        self.assertIn("git push", ask, f"Template F's ask list no longer asks before 'git push'; it has {sorted(ask)}. {PIN_CHANGED}")

    def test_loop_prompts_keep_their_stop_condition_and_caps(self):
        """Template H (loop and schedule prompts) loses its stop condition or its retry caps, so a loop runs forever."""
        h = pb_body("H")
        for phrase, why in [
            ("Stop when <end condition>", "every loop names how it ends."),
            ("after 2 failures with the same cause", "the failure cap on /loop."),
            ("retry at most once", "the retry cap on /schedule."),
        ]:
            with self.subTest(phrase=phrase):
                self.need(h, phrase, "Template H", why)

    def test_retro_and_grill_prompts_keep_their_core_rules(self):
        """Template I applies changes without a yes, or Template K asks several questions at once."""
        for sid, phrase, why in [
            ("I", "Don't apply anything until I say yes", "a retro proposes; it does not change the harness unasked."),
            ("I", "Propose up to 3 changes", "a retro is capped at three changes."),
            ("K", "One question per message", "a grill asks one question at a time."),
            ("K", "Do not write a plan, spec or code in this session", "a grill ends in decisions, not a plan."),
        ]:
            with self.subTest(template=sid, phrase=phrase):
                self.need(pb_body(sid), phrase, f"Template {sid}", why)

    def test_cheat_sheet_stuck_signs_keep_their_rows(self):
        """The cheat sheet's stuck-signs table (cs:3) is emptied to a heading and a few rows."""
        rows = [l for l in cs_body("cs:3").splitlines() if l.startswith("|") and not re.fullmatch(r"\|[-| :]+\|?", l)]
        data = rows[1:]  # the first row is the header
        self.assertGreaterEqual(len(data), 5, f"cheat sheet §3 has {len(data)} table rows, expected at least 5 (it had 6). " + PIN_CHANGED)


# ---------------------------------------------------------------------------------------------
# 4. ENTRY.md
# ---------------------------------------------------------------------------------------------

ENTRY = read("ENTRY.md")
KNOWN_IDS = set(PB) | set(CS)
ID_TOKEN = re.compile(r"cs:\d+|law-\d+|\d+[A-Z]?(?:\.\d+)?|[A-M]")


def block(text, heading):
    """The text under a '## heading' up to the next '## ' heading."""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


class EntryPins(Pinned):
    def test_router_has_every_scenario_row(self):
        """Scenario rows are deleted from the router until a request no longer finds its row."""
        rows = re.findall(r"(?m)^\| (\d+) \|", block(ENTRY, "Scenario router"))
        self.assertGreaterEqual(len(rows), 18, f"the scenario router has {len(rows)} rows, expected at least 18. " + PIN_CHANGED)

    def test_phase_table_has_eight_phases_with_real_section_ids(self):
        """The phase table loses a phase or its section ids, so a stage-of-work request loads nothing or the wrong text."""
        rows = [m for m in re.finditer(r"(?m)^\| (\d+) ([^|]+)\|([^|]*)\|", block(ENTRY, "Phase table"))]
        self.assertEqual([int(m.group(1)) for m in rows], list(range(1, 9)),
                         f"the phase table should have exactly phases 1 to 8, found {[int(m.group(1)) for m in rows]}. " + PIN_CHANGED)
        for m in rows:
            with self.subTest(phase=m.group(1)):
                tokens = [t for span in re.findall(r"`([^`]+)`", m.group(3)) for t in span.split()]
                self.assertTrue(tokens, f"phase {m.group(1)} ({m.group(2).strip()}) names no section ids. " + PIN_CHANGED)
                unknown = [t for t in tokens if not ID_TOKEN.fullmatch(t) or t not in KNOWN_IDS]
                self.assertFalse(unknown, f"phase {m.group(1)} names ids that resolve to no section: {unknown}. Fix the id. " + PIN_CHANGED)

    def test_rules_that_apply_everywhere_keep_goal_first_and_the_rest(self):
        """The seven everywhere-rules lose one, lose their order, or keep their name but lose their sentence."""
        rules = re.findall(r"(?m)^- \*\*(.+?)\.\*\*\s*(.*)$", block(ENTRY, "Rules that apply everywhere"))
        names = [n for n, _ in rules]
        self.assertTrue(names and names[0] == "Goal first", f"the first rule should be 'Goal first', found {names[:1]}. " + PIN_CHANGED)
        text = dict(rules)
        for name, phrase in [
            ("Goal first", "Done-when"),
            ("One writer", "One agent edits a set of files"),
            ("Fresh review", "never your conclusion"),
            ("Receipts", "NOT RUN is not PASS"),
            ("Two strikes", "fails twice for the same reason"),
            ("Code over words", "deny rule, a hook or a gate"),
            ("Loops are bounded", "stop condition, a retry cap and a cost ceiling"),
        ]:
            with self.subTest(rule=name):
                self.assertIn(name, text, f"ENTRY.md lost the rule '{name}' from 'Rules that apply everywhere'. {PIN_CHANGED}")
                self.assertIn(phrase, text[name], f"the rule '{name}' no longer says {phrase!r}; it reads {text[name][:80]!r}. {PIN_CHANGED}")

    def test_never_load_the_whole_playbook_and_never_say_to(self):
        """ENTRY.md tells a session to read or load the whole playbook, which floods its context with 1,500 lines."""
        self.need(ENTRY, "Never load the whole playbook", "ENTRY.md", "the guide's core promise to the session that calls it.")
        self.need(ENTRY, "Load only the row's sections", "ENTRY.md (How to use it, step 3)", "step 3 must load sections, not the file.")
        self.need(ENTRY, "tools/section.py", "ENTRY.md", "section.py is how a session loads one section.")
        positive = [
            re.compile(r"\b(?:read|load|open|use|include|paste|fetch)\b[^.\n]{0,40}\b(?:whole|entire|full|all of)\b[^.\n]{0,20}\bplaybook\b", re.I),
            re.compile(r"\b(?:read|load|open|paste)\b[^.\n]{0,30}\bplaybook\b[^.\n]{0,30}\b(?:whole|in full|entire|top to bottom|end to end)\b", re.I),
        ]
        negated = re.compile(r"\b(?:never|not|don't|do not|without|instead of|avoid|no need)\b", re.I)
        hits = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", ENTRY)
                if any(p.search(s) for p in positive) and not negated.search(s)]
        self.assertFalse(hits, "ENTRY.md says to read or load the whole playbook:" + short(hits) + "\nSay 'load only the sections the row names'. " + PIN_CHANGED)

    def test_entry_says_the_work_happens_in_your_project(self):
        """ENTRY.md stops separating the guide's folder from the user's project, so a session edits GUIDE instead of its own project."""
        self.need(ENTRY, "Your project is your current directory", "ENTRY.md (Two folders)", "where the work happens.")
        self.need(ENTRY, "your project gets the work", "ENTRY.md (Two folders)", "the guide gives advice; it is never the place to edit.")

    def test_guide_paths_in_code_spans_exist(self):
        """A GUIDE/... path in ENTRY.md points at a file or folder that was renamed or deleted."""
        missing = []
        for span in re.findall(r"`([^`]+)`", ENTRY):
            for tok in span.split():
                tok = tok.rstrip(".,;:)")
                if not tok.startswith("GUIDE/"):
                    continue
                rel = tok[len("GUIDE/"):]
                if "<" in rel or "*" in rel:  # a placeholder such as wiki/<name>.md: its folder must exist
                    rel = rel.split("<")[0].split("*")[0].rstrip("/") or "."
                if not (ROOT / rel).exists():
                    missing.append(f"{tok} (no {rel})")
        self.assertFalse(missing, "ENTRY.md names GUIDE paths that do not exist:" + short(missing) + "\nFix the path or restore the file. " + PIN_CHANGED)

    def test_thin_rows_keep_naming_their_gap(self):
        """A thin router row drops its 'Gap:' line, so the session fills the playbook's hole from memory."""
        rows = {int(m.group(1)): m.group(0) for m in re.finditer(r"(?m)^\| (\d+) \|.*$", block(ENTRY, "Scenario router"))}
        known_thin = {3, 4, 5, 7, 12, 13, 18}
        for n in sorted(known_thin):
            with self.subTest(row=n):
                self.assertIn(n, rows, f"router row {n} is gone. " + PIN_CHANGED)
                self.assertRegex(rows[n].split("|")[2], r"\bthin\b", f"router row {n} is no longer marked thin. " + PIN_CHANGED)
                self.assertIn("Gap:", rows[n], f"thin router row {n} no longer says 'Gap:' (what the playbook lacks). {PIN_CHANGED}")
        for n, row in rows.items():
            if re.search(r"\bthin\b", row.split("|")[2]) and n not in known_thin:
                self.assertIn("Gap:", row, f"thin router row {n} has no 'Gap:'. Name what the playbook lacks.")


# ---------------------------------------------------------------------------------------------
# 5. AGENTS.md, the wiki, and "NOT RUN is not PASS" everywhere
# ---------------------------------------------------------------------------------------------

WIKI = sorted(p for p in (ROOT / "wiki").glob("*.md") if p.name not in ("README.md", "case-study.md"))
NOT_RUN_IS_PASS = re.compile(r"(?<!not )(?<!n't )\bNOT RUN\s+(?:counts|is|=)\s+(?:as\s+)?PASS\b", re.I)


class RulesAndRunbooks(Pinned):
    def test_agents_md_keeps_its_rules(self):
        """AGENTS.md loses the rule that the suite gates every commit, or a rule about tests, sources, privacy or precedence."""
        agents = read("AGENTS.md")
        checks = block(agents, "Checks")
        self.assertIn("tests/run.sh", checks, "AGENTS.md's Checks section no longer names tests/run.sh. " + PIN_CHANGED)
        self.assertIn("before every commit", checks, "AGENTS.md's Checks section no longer says to run the suite before every commit. " + PIN_CHANGED)
        for phrase, why in [
            ("Never weaken or delete a test", "a failing test is fixed, never silenced."),
            ("Add no new factual claim without a primary source", "the guide's facts stay sourced."),
            ("This repository is public", "the privacy rule's reason."),
            ("the playbook wins", "the precedence rule between layers."),
        ]:
            with self.subTest(phrase=phrase):
                self.need(agents, phrase, "AGENTS.md", why)

    def test_every_runbook_keeps_a_checklist_and_steps(self):
        """A runbook keeps its Steps and Checklist headings but is hollowed to a line or two under each."""
        self.assertGreaterEqual(len(WIKI), 9, f"expected at least 9 runbooks in wiki/, found {[p.name for p in WIKI]}. " + PIN_CHANGED)
        for path in WIKI:
            text = path.read_text(encoding="utf-8")
            with self.subTest(runbook=path.name):
                steps, checklist = block(text, "Steps"), block(text, "Checklist")
                items = re.findall(r"(?m)^\s*- \[ \] ", checklist)
                numbered = re.findall(r"(?m)^\d+\. ", steps)
                self.assertGreaterEqual(len(items), 3, f"wiki/{path.name}: the Checklist has {len(items)} '- [ ]' items, expected at least 3. " + PIN_CHANGED)
                self.assertGreaterEqual(len(numbered), 3, f"wiki/{path.name}: the Steps section has {len(numbered)} numbered steps, expected at least 3. " + PIN_CHANGED)

    def test_not_run_is_not_pass_is_said_in_every_layer(self):
        """One layer (entry, rules, runbook or playbook) stops saying that a skipped check is not a pass."""
        phrase = "NOT RUN is not PASS"
        for rel in ("ENTRY.md", "AGENTS.md", "wiki/verify.md", "playbook/agent-harness-playbook.md"):
            with self.subTest(file=rel):
                self.need(read(rel), phrase, rel, "every layer repeats it, because a session may read only one.")

    def test_no_layer_says_not_run_counts_as_pass(self):
        """A file is edited to say a NOT RUN check counts as PASS, which makes every receipt worthless."""
        self.assertIsNotNone(NOT_RUN_IS_PASS.search("NOT RUN counts as PASS"), "the NOT RUN detector no longer matches its own example")
        self.assertIsNone(NOT_RUN_IS_PASS.search("NOT RUN is not PASS"), "the NOT RUN detector matches the correct rule")
        files = [ROOT / "ENTRY.md", ROOT / "AGENTS.md", *sorted((ROOT / "wiki").glob("*.md")), *sorted((ROOT / "playbook").glob("*.md"))]
        hits = [f"{p.relative_to(ROOT)}:{no}: {line.strip()[:90]}" for p in files
                for no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if NOT_RUN_IS_PASS.search(line)]
        self.assertFalse(hits, "a file says NOT RUN counts as PASS:" + short(hits) + "\nA check that did not run proves nothing. Restore 'NOT RUN is not PASS'.")


# ---------------------------------------------------------------------------------------------
# 6. Skill safety
# ---------------------------------------------------------------------------------------------

def frontmatter(rel):
    m = re.match(r"---\n(.*?)\n---\n", read(rel), re.S)
    if not m:
        raise AssertionError(f"{rel}: no frontmatter between --- lines.")
    return {k.group(1): k.group(2).strip() for line in m.group(1).splitlines() if (k := re.match(r"([A-Za-z][\w-]*):\s*(.*)$", line))}


def tree(home):
    """Every entry under a folder, as (relative path, 'dir' | 'link' | 'file'); symlinks are not followed."""
    out = []
    for dirpath, dirnames, filenames in os.walk(home):
        for name in dirnames + filenames:
            p = pathlib.Path(dirpath) / name
            out.append((p.relative_to(home).as_posix(), "link" if p.is_symlink() else "dir" if p.is_dir() else "file"))
    return sorted(out)


class SkillSafety(Pinned):
    def test_guide_skill_asks_for_exactly_three_tools(self):
        """/guide's allowed-tools widens (Write, Edit, plain Bash), so a routing skill can change the user's project unasked."""
        got = frontmatter("skills/guide/SKILL.md").get("allowed-tools")
        self.assertEqual(got, "Read, Bash(git -C:*), Bash(python3 -I:*)",
                         f"skills/guide/SKILL.md allowed-tools is {got!r}. /guide only reads files, finds its root with git -C, and runs section.py with python3 -I. {PIN_CHANGED}")

    def test_grill_skill_cannot_write_and_stays_slash_only(self):
        """/grill is given Write or Edit, or loses disable-model-invocation, so a question-asking skill writes plans or fires on its own."""
        fields = frontmatter("skills/grill/SKILL.md")
        tools = fields.get("allowed-tools", "")
        self.assertNotRegex(tools, r"\b(?:Write|Edit|MultiEdit|NotebookEdit)\b",
                            f"skills/grill/SKILL.md allowed-tools grants a write tool: {tools!r}. A grill ends in decisions, never files. {PIN_CHANGED}")
        self.assertEqual(fields.get("disable-model-invocation"), "true",
                         "skills/grill/SKILL.md must keep 'disable-model-invocation: true' (/grill is slash-only; commit f79ad93). " + PIN_CHANGED)

    def test_installer_leaves_only_its_symlink_in_home(self):
        """install.sh --apply writes more than the one symlink into HOME (a CLAUDE.md, a settings file, a copy)."""
        home = pathlib.Path(tempfile.mkdtemp(prefix="guard-home-", dir=os.environ.get("TEST_TMP") or None))
        self.addCleanup(shutil.rmtree, home, True)
        r = subprocess.run(["bash", str(ROOT / "skills" / "guide" / "install.sh"), "--apply"],
                           env={**os.environ, "HOME": str(home)}, capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, f"install.sh --apply failed: {r.stderr}")
        found = tree(home)
        self.assertEqual(found, [(".claude", "dir"), (".claude/skills", "dir"), (".claude/skills/guide", "link")],
                         "install.sh --apply must leave exactly one entry under HOME, the symlink .claude/skills/guide "
                         f"(plus its two parent folders). Found:{short(found, 20)}\nThe snippet and prompt are printed, never written. " + PIN_CHANGED)
        self.assertEqual(os.path.realpath(home / ".claude" / "skills" / "guide"), os.path.realpath(ROOT / "skills" / "guide"),
                         "the symlink must point at this clone's skills/guide. " + PIN_CHANGED)


# ---------------------------------------------------------------------------------------------
# 7. The compendium works offline
# ---------------------------------------------------------------------------------------------

class CompendiumOffline(unittest.TestCase):
    PATTERNS = [
        (r"\bsrc\s*=\s*[\"']?\s*(?:https?:)?//", "an src= attribute that loads a remote file"),
        (r"\bsrcset\s*=\s*[\"'][^\"']*(?:https?:)?//", "an srcset= attribute that loads a remote file"),
        (r"<link\b[^>]*\bhref\s*=\s*[\"']?\s*(?:https?:)?//", "a <link href=...> to a remote file"),
        (r"url\(\s*[\"']?\s*(?:https?:)?//", "a CSS url() or @import url() to a remote file"),
        (r"\bfetch\(", "a fetch( call"),
        (r"XMLHttpRequest", "an XMLHttpRequest"),
        (r"sendBeacon", "a sendBeacon call"),
        (r"new\s+Image\(", "a new Image( call"),
        (r"\bWebSocket\(|\bEventSource\(", "a WebSocket or EventSource"),
    ]

    def test_compendium_makes_no_network_request(self):
        """The compendium gains an image, script, stylesheet, beacon or fetch that needs the network, so it breaks offline or tracks readers."""
        html = read("docs/orchestrating-claude-compendium.html")
        found = []
        for pattern, what in self.PATTERNS:
            for m in re.finditer(pattern, html, re.I):
                line = html.count("\n", 0, m.start()) + 1
                found.append(f"line {line}: {what}: {html[m.start():m.start() + 70]!r}")
        self.assertFalse(found, "docs/orchestrating-claude-compendium.html would load or send something over the network:" + short(found) +
                         "\nExternal URLs may appear only in <a href> links and in text. Remove the request and rebuild with python3 -I tools/build_compendium.py. " + PIN_CHANGED)


if __name__ == "__main__":
    unittest.main()
