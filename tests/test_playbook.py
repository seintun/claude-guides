"""Guards on the playbook, the repository's guiding star: a careless or catastrophic edit fails loudly.

Three kinds of guard:
  Invariants   hard rules that never move: sections 0 to 20 plus 3A and 17A, Laws 1 to 10,
               Templates A to M, a Version line, a Sources section.
  Baseline     the playbook may grow but not shrink: tests/baselines/playbook.json records its
               headings, source URLs, evidence-tag counts, line count and version.
  Hygiene      in-file links resolve, and no personal path leaks into this public file.

Run: python3 -I tests/test_playbook.py   (or the whole suite: python3 -I -m unittest discover -s tests -p 'test_*.py')
"""
import json
import pathlib
import re
import sys
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))
import section  # noqa: E402
import update_baselines as ub  # noqa: E402

TEXT = ub.PLAYBOOK.read_text(encoding="utf-8")
HEADS = ub.headings(TEXT)  # (line index, level, title)
INTENDED = "If the change is intended, run python3 -I tests/update_baselines.py and commit the new baseline."

# Section ids in the order they appear in the file. 3A is a level-2 section, 17A a level-3 one.
SECTION_IDS = [str(n) for n in range(0, 18)] + ["17A", "18", "19", "20"]
SECTION_IDS.insert(SECTION_IDS.index("4"), "3A")
LEVEL = {sid: (3 if sid == "17A" else 2) for sid in SECTION_IDS}
TEMPLATES = list("ABCDEFGHIJKLM")


def first_heading(pattern, level):
    """Line index of the first heading at this level whose title matches, or None."""
    for i, lvl, title in HEADS:
        if lvl == level and re.match(pattern, title):
            return i
    return None


def short(items, limit=15):
    items = list(items)
    extra = f" ... and {len(items) - limit} more" if len(items) > limit else ""
    return "\n  " + "\n  ".join(str(x) for x in items[:limit]) + extra


class Invariants(unittest.TestCase):
    def test_numbered_sections_exist_in_order(self):
        """A playbook section is deleted, renumbered or swapped with another."""
        at = {sid: first_heading(rf"{sid}\. ", LEVEL[sid]) for sid in SECTION_IDS}
        missing = [f"§{sid} (a level-{LEVEL[sid]} heading that starts \"{sid}. \")" for sid, i in at.items() if i is None]
        self.assertFalse(missing, "playbook sections are missing or renumbered:" + short(missing) +
                         "\nSection numbers are stable: ENTRY.md, the wiki, the teaching page and tools/section.py all cite them. "
                         "Restore the heading. If you renumbered on purpose, fix every citation first and then update SECTION_IDS in tests/test_playbook.py.")
        order = [at[sid] for sid in SECTION_IDS]
        swapped = [f"§{SECTION_IDS[n]} comes before §{SECTION_IDS[n - 1]}" for n in range(1, len(order)) if order[n] < order[n - 1]]
        self.assertFalse(swapped, "playbook sections are out of order:" + short(swapped) +
                         "\nPut the sections back in numeric order (3A after 3, 17A inside 17 before 18).")

    def test_ten_laws_live_in_section_two(self):
        """A law is deleted, renumbered, duplicated or moved out of section 2."""
        laws = [(int(m.group(1)), i) for i, lvl, t in HEADS if lvl == 3 and (m := re.match(r"Law (\d+)\. ", t))]
        numbers = [n for n, _ in laws]
        self.assertEqual(numbers, list(range(1, 11)),
                         f"the laws found are {numbers}, expected exactly Law 1 to Law 10, once each, in order. "
                         "ENTRY.md and the wiki cite laws by number (law-7): restore the missing heading \"### Law N. <title>\".")
        start, end = first_heading(r"2\. ", 2), first_heading(r"3\. ", 2)
        if start is None or end is None:
            self.fail("the §2 or §3 heading is missing; see test_numbered_sections_exist_in_order")
        outside = [n for n, i in laws if not (start < i < end)]
        self.assertFalse(outside, f"Laws {outside} sit outside §2. Move them back under \"## 2. Ten laws\".")

    def test_templates_a_to_m_live_in_section_sixteen(self):
        """A template is deleted, renamed, reordered or moved out of section 16."""
        start, end = first_heading(r"16\. ", 2), first_heading(r"17\. ", 2)
        if start is None or end is None:
            self.fail("the §16 or §17 heading is missing; see test_numbered_sections_exist_in_order")
        found = [m.group(1) for i, lvl, t in HEADS if lvl == 3 and start < i < end and (m := re.match(r"([A-Z])\. ", t))]
        self.assertEqual(found, TEMPLATES,
                         f"the templates under §16 are {found}, expected A to M in order. "
                         "README.md, ENTRY.md and the wiki link to them by letter and anchor: restore the heading \"### X. <title>\".")

    def test_version_line_near_the_top(self):
        """The Version line is lost, so nobody can tell which playbook a session read."""
        self.assertIsNotNone(ub.version(TEXT),
                             "no line that starts \"Version X.Y\" in the first 10 lines of the playbook. Restore it, and bump it when you change the playbook.")

    def test_sources_section_has_urls(self):
        """The Sources section is deleted or emptied, leaving every graded claim without a source."""
        self.assertIsNotNone(first_heading(r"20\. Sources", 2), "no \"## 20. Sources\" heading. Restore section 20.")
        self.assertTrue(ub.source_urls(TEXT), "§20 holds no http(s) URL. Restore the source list; every graded claim points at it.")

    def test_section_tool_resolves_every_id(self):
        """The playbook changes shape and tools/section.py stops serving an id the router cites."""
        _, found = section.index(ub.PLAYBOOK)
        want = SECTION_IDS + [f"law-{n}" for n in range(1, 11)] + TEMPLATES
        missing = [k for k in want if k not in found]
        self.assertFalse(missing, "tools/section.py cannot resolve these ids:" + short(missing) +
                         "\nA heading no longer matches the shape section.py reads (\"N. \", \"Law N. \", \"X. \"). Restore the heading, or fix tools/section.py key_of.")


class Baseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not ub.BASELINE.exists():
            raise AssertionError("tests/baselines/playbook.json is missing. Run python3 -I tests/update_baselines.py and commit it.")
        cls.base = json.loads(ub.BASELINE.read_text(encoding="utf-8"))
        cls.now = ub.measure(TEXT)

    def test_no_heading_removed_or_renamed(self):
        """A playbook heading is removed or renamed, and every link and citation to it dies."""
        gone = list((Counter(self.base["headings"]) - Counter(self.now["headings"])).elements())
        added = list((Counter(self.now["headings"]) - Counter(self.base["headings"])).elements())
        hint = ("\nHeadings now present that are not in the baseline (a rename shows up here):" + short(added)) if added else ""
        self.assertFalse(gone, "baselined headings are gone from the playbook:" + short(gone) + hint +
                         "\nRestore them. " + INTENDED)

    def test_headings_keep_their_order(self):
        """Playbook sections are shuffled out of their order."""
        present = set(self.now["headings"])
        want = [h for h in self.base["headings"] if h in present]
        have = iter(self.now["headings"])
        moved = []
        for n, h in enumerate(want):
            if not any(h == x for x in have):
                moved.append(f"{h!r} now comes before {want[n - 1]!r}" if n else f"{h!r} now comes first")
                have = iter(self.now["headings"])  # resync so one move reports once
                for x in have:
                    if x == h:
                        break
        self.assertFalse(moved, "headings are out of their baseline order:" + short(moved) + "\nMove them back. " + INTENDED)

    def test_no_source_url_removed(self):
        """A source URL is deleted from section 20, so the claims it backed lose their citation."""
        gone = sorted(set(self.base["source_urls"]) - set(self.now["source_urls"]))
        self.assertFalse(gone, f"{len(gone)} baselined source URL(s) are gone from §20:" + short(gone) +
                         "\nRestore them (AGENTS.md: every evidence-tag URL must stay). " + INTENDED)

    def test_evidence_tag_counts_do_not_collapse(self):
        """Graded claims are mass-deleted or their [P] [S] [R] [D] grades are stripped."""
        low = []
        for g in ub.GRADES:
            was, now = self.base["evidence_tags"][g], self.now["evidence_tags"][g]
            if now * 10 < was * 9:
                low.append(f"[{g}] fell from {was} to {now} (floor {-(-was * 9 // 10)})")
        self.assertFalse(low, "evidence tags dropped by more than 10%:" + short(low) +
                         "\nEvery claim keeps its grade. Restore the deleted claims or grades. " + INTENDED)

    def test_line_count_does_not_collapse(self):
        """The playbook is truncated or half of it is deleted."""
        was, now = self.base["line_count"], self.now["line_count"]
        self.assertGreaterEqual(now * 10, was * 9,
                                f"the playbook has {now} lines, down from {was} (floor {-(-was * 9 // 10)}). "
                                "Restore what was cut. " + INTENDED)

    def test_version_does_not_go_backwards(self):
        """A playbook edit lowers or loses the version number."""
        def tup(v):
            return tuple(int(p) for p in v.split(".")) if v else ()
        was, now = self.base["version"], self.now["version"]
        self.assertGreaterEqual(tup(now), tup(was),
                                f"the playbook version is {now}, below the baseline {was}. Versions only go up. "
                                "Restore the Version line, or bump it. " + INTENDED)


class Hygiene(unittest.TestCase):
    def test_in_file_anchor_links_resolve(self):
        """A heading is renamed and a link inside the playbook silently dies."""
        slugs = ub.slug_set(TEXT)
        broken, fence = [], False
        for no, line in enumerate(TEXT.splitlines(), 1):
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            for target in re.findall(r"\]\(#([^)\s]+)\)", re.sub(r"`[^`]*`", "", line)):
                if target not in slugs:
                    broken.append(f"line {no}: (#{target})")
        self.assertFalse(broken, "links inside the playbook point at no heading:" + short(broken) +
                         "\nFix the link, or restore the heading it names (GitHub slug: lowercase, punctuation dropped, spaces to hyphens).")

    def test_no_personal_absolute_paths(self):
        """A personal absolute path (a home directory) leaks into the public playbook."""
        path = re.compile(r"(?<![\w.~:/-])/(?:Users|home)/")  # a URL such as https://host/home/x does not count
        hits = [f"line {no}: {line.strip()[:80]}" for no, line in enumerate(TEXT.splitlines(), 1) if path.search(line)]
        self.assertFalse(hits, "the playbook contains a /Users/ or /home/ path:" + short(hits) +
                         "\nThis repository is public. Use a repo-relative path or a placeholder such as /path/to/project, then run python3 -I tools/check_privacy.py.")


if __name__ == "__main__":
    unittest.main()
