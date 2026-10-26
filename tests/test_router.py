"""Routing guards: ENTRY.md keeps offering every scenario its route, and section.py serves it.

Run: python3 -I tests/test_router.py   (or the whole suite: tests/run.sh)
"""
import contextlib
import io
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import section  # noqa: E402

ENTRY = (ROOT / "ENTRY.md").read_text(encoding="utf-8")
SCENARIOS = json.loads((ROOT / "tests" / "scenarios" / "routing.json").read_text(encoding="utf-8"))["scenarios"]


def router_rows():
    """Row number -> cells (scenario, read, runbook, template, output) of the ENTRY.md scenario router."""
    block = ENTRY.split("## Scenario router", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in block.splitlines():
        m = re.match(r"\| (\d+) \|(.*)\|\s*$", line)
        if m:
            rows[int(m.group(1))] = [c.strip() for c in m.group(2).split("|")]
    return rows


ROWS = router_rows()


class SectionTool(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "section.py"), *args],
                              capture_output=True, text=True)

    def test_each_id_kind_prints_one_section(self):
        """section.py stops serving a kind of id (numbered section, template, law, cheat sheet)."""
        for sid, title in [("9.5", "9.5 Hooks"), ("17A", "17A."), ("F", "F. Stop hook"), ("law-7", "Law 7."), ("cs:3", "3. Stuck")]:
            out = self.run_tool(sid)
            self.assertEqual(out.returncode, 0, f"section.py {sid} failed: {out.stderr}")
            self.assertIn(title, out.stdout.splitlines()[1], f"section.py {sid} printed the wrong section")
            self.assertEqual(out.stdout.count("<!-- "), 1, f"section.py {sid} printed more than one section")

    def test_section_stops_at_the_next_heading(self):
        """section.py leaks the rest of the playbook into one section."""
        out = self.run_tool("9.5").stdout
        self.assertNotIn("## 10. Guardrails", out, "section 9.5 ran on into §10")
        self.assertLess(len(out.splitlines()), 40, "section 9.5 is far longer than one section")

    def test_unknown_id_fails(self):
        """A typo in a router id passes silently."""
        out = self.run_tool("99.9")
        self.assertEqual(out.returncode, 1, "an unknown id must exit 1")
        self.assertIn("unknown section id", out.stderr)

    def test_list_names_every_template_and_law(self):
        """--list loses templates or laws."""
        listing = self.run_tool("--list").stdout
        for key in [f"law-{n}" for n in range(1, 11)] + list("ABCDEFGHIJKLM") + ["3A", "17A", "cs:3"]:
            self.assertRegex(listing, rf"(?m)^{re.escape(key)}\s", f"--list lost {key}")


class Router(unittest.TestCase):
    def test_every_scenario_has_its_row(self):
        """A scenario's row is deleted or renumbered in ENTRY.md."""
        for s in SCENARIOS:
            self.assertIn(s["row"], ROWS, f"{s['id']}: ENTRY.md has no row {s['row']}")

    def test_rows_still_offer_their_sections(self):
        """A row drops a section its scenario needs."""
        for s in SCENARIOS:
            read = ROWS[s["row"]][1]
            for sid in s["ids"]:
                self.assertRegex(read, rf"(?<![\w.:-]){re.escape(sid)}(?![\w.])", f"{s['id']}: row {s['row']} no longer loads {sid}")

    def test_rows_still_name_their_templates_and_runbooks(self):
        """A row loses its template or its runbook."""
        for s in SCENARIOS:
            cells = ROWS[s["row"]]
            for t in s["templates"]:
                self.assertRegex(cells[3], rf"\b{t}\b", f"{s['id']}: row {s['row']} no longer names Template {t}")
            link = s["runbook"] if "/" in s["runbook"] else f"wiki/{s['runbook']}.md"
            self.assertIn(link, cells[2], f"{s['id']}: row {s['row']} no longer links {link}")

    def test_every_row_has_a_scenario(self):
        """A router row is added without a test scenario."""
        covered = {s["row"] for s in SCENARIOS}
        self.assertEqual(set(ROWS) - covered, set(), "add a scenario to tests/scenarios/routing.json for each new row")

    def test_routes_load_sections_not_the_playbook(self):
        """A route sends a session to the whole playbook file."""
        self.assertNotRegex(ENTRY, r"\]\((\./)?playbook/agent-harness-playbook\.md\)", "ENTRY.md links the whole playbook; point to section ids instead")
        for s in SCENARIOS:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                status = section.main(s["ids"])
            self.assertEqual(status, 0, f"{s['id']}: an id does not resolve")
            self.assertLess(len(buf.getvalue()), 60_000, f"{s['id']}: its sections are close to a whole playbook")

    def test_thin_rows_name_their_gap(self):
        """A thin row stops saying what the playbook lacks."""
        for n, cells in ROWS.items():
            if "(thin" in cells[0] or "thin)" in cells[0]:
                self.assertIn("Gap:", cells[4], f"row {n} is marked thin but its output names no gap")


if __name__ == "__main__":
    unittest.main()
