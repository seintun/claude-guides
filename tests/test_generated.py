"""Generated files stay in step with their sources: site/index.html and the compendium.

Run: python3 -I tests/test_generated.py   (or the whole suite: tests/run.sh)
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TMP = os.environ.get("TEST_TMP") or None   # tests/run.sh sets this to build/test-tmp
if TMP:
    os.makedirs(TMP, exist_ok=True)


def build(tool, *args):
    return subprocess.run([sys.executable, "-I", str(ROOT / "tools" / tool), *args], capture_output=True, text=True)


class Generated(unittest.TestCase):
    def test_standalone_page_is_current(self):
        """The page source changes but site/index.html, the copy people open, does not."""
        with tempfile.TemporaryDirectory(dir=TMP) as d:
            out = pathlib.Path(d) / "index.html"
            r = build("build_standalone.py", str(ROOT / "site" / "orchestrating-claude.html"), str(out))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), (ROOT / "site" / "index.html").read_text(encoding="utf-8"),
                             "site/index.html is stale: run python3 -I tools/build_standalone.py and commit it")

    def test_compendium_is_current(self):
        """A source document changes but the compendium is not rebuilt."""
        with tempfile.TemporaryDirectory(dir=TMP) as d:
            out = pathlib.Path(d) / "compendium.html"
            r = build("build_compendium.py", str(out))
            self.assertEqual(r.returncode, 0, r.stderr)
            dated = re.compile(r"Built \d{4}-\d{2}-\d{2} ")
            fresh = dated.sub("Built <date> ", out.read_text(encoding="utf-8"))
            committed = dated.sub("Built <date> ", (ROOT / "docs" / "orchestrating-claude-compendium.html").read_text(encoding="utf-8"))
            self.assertTrue(fresh == committed, "docs/orchestrating-claude-compendium.html is stale: run python3 -I tools/build_compendium.py and commit it")

    def test_agent_index_is_current(self):
        """The playbook, ENTRY.md, a runbook or a skill changes but guide-index.json and sections/, which agents without a clone fetch, do not."""
        with tempfile.TemporaryDirectory(dir=TMP) as d:
            r = build("build_index.py", "--out", d)
            self.assertEqual(r.returncode, 0, r.stderr)
            fresh = {p.relative_to(d).as_posix(): p.read_text(encoding="utf-8") for p in pathlib.Path(d).rglob("*") if p.is_file()}
            committed = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
                         for p in [ROOT / "guide-index.json", *(ROOT / "sections").glob("*"), *(ROOT / "routes").glob("*")] if p.is_file()}
            stale = sorted(k for k in fresh.keys() | committed.keys() if fresh.get(k) != committed.get(k))
            self.assertFalse(stale, f"stale or extra agent files: {stale[:8]}. Run python3 -I tools/build_index.py and commit the result")

    def test_agent_index_routes_every_router_row(self):
        """A router row is lost from guide-index.json, or names a section with no file to fetch."""
        index = json.loads((ROOT / "guide-index.json").read_text(encoding="utf-8"))
        rows = re.findall(r"^\| (\d+) \|", (ROOT / "ENTRY.md").read_text(encoding="utf-8"), re.M)
        self.assertEqual([r["row"] for r in index["router"]], [int(n) for n in rows], "guide-index.json router rows differ from ENTRY.md")
        paths = {s["id"]: s["path"] for s in index["sections"]}
        missing = [(r["row"], i) for r in index["router"] + index["phases"] for i in r["read"] if i not in paths or not (ROOT / paths[i]).is_file()]
        self.assertFalse(missing, f"route ids with no sections/ file: {missing}")
        no_bundle = [r.get("bundle") for r in index["router"] + index["phases"] if not r.get("bundle") or not (ROOT / r["bundle"]).is_file()]
        self.assertFalse(no_bundle, f"routes with no routes/ bundle to fetch: {no_bundle}")

    def test_compendium_works_offline(self):
        """The compendium starts loading something from the network."""
        html = (ROOT / "docs" / "orchestrating-claude-compendium.html").read_text(encoding="utf-8")
        self.assertNotRegex(html, r"<(script|link)[^>]+(src|href)=\"https?://", "the compendium must load nothing from the network")

    def test_compendium_is_one_long_page_in_the_page_parts(self):
        """The compendium goes back to embedding the page in a frame, drops a lesson, a runbook or a mapped playbook section, or groups the lessons differently from the page."""
        html = (ROOT / "docs" / "orchestrating-claude-compendium.html").read_text(encoding="utf-8")
        self.assertNotIn("<iframe", html, "the compendium must show the lessons inline, not embed the page in a frame")
        m = re.search(r'<script type="application/json" id="compendium-map">(.*?)</script>', html, re.S)
        self.assertTrue(m, "the compendium lost its embedded map of parts, lessons and sections")
        cmap = json.loads(m.group(1))
        page = (ROOT / "site" / "orchestrating-claude.html").read_text(encoding="utf-8")
        page_parts = [(pid, re.findall(r'<li><a href="#([a-z]+)">', body))
                      for pid, body in re.findall(r'<div class="part-head" id="(part-[a-z]+)">(.*?)\n</div>', page, re.S)]
        self.assertEqual([(p["id"], [l["id"] for l in p["lessons"]]) for p in cmap["parts"]], page_parts,
                         "the compendium groups the lessons differently from the page's six parts: rebuild with python3 -I tools/build_compendium.py")
        # Every playbook section the page map names appears in its lesson, once as text and elsewhere as a pointer.
        pb = (ROOT / "playbook" / "agent-harness-playbook.md").read_text(encoding="utf-8")
        table = pb.split("**Page map: lesson to playbook section**", 1)[1].split("\n---", 1)[0]
        lessons = [l for _, ls in page_parts for l in ls]
        by_lesson = {l["id"]: l for p in cmap["parts"] for l in p["lessons"]}
        rows = re.findall(r"^\| (\d+|Sources) \| [^|]*\| ([^|]*) \|$", table, re.M)
        self.assertEqual(len(rows), len(lessons), "the playbook's page map must have one row per lesson, Sources included; the loop below would otherwise pass without checking them")
        self.assertGreaterEqual(len(rows), 18)
        for num, cell in rows:
            sid = "sources" if num == "Sources" else lessons[int(num) - 1]
            want = [(m2.group(1) or m2.group(2)).upper() for m2 in re.finditer(r"\[(?:§(\S+?)|Template (\w))\]\(#", cell)]
            got = by_lesson[sid]["pb"] + by_lesson[sid]["pb_refs"]
            self.assertEqual(sorted(want), sorted(got), f"lesson {sid}: the compendium's playbook sections differ from the playbook's page map")
            for key in want:
                self.assertEqual(html.count(f'id="pb-sec-{key}"'), 1, f"playbook section {key} must appear in the compendium exactly once")
        runbooks = sorted(w for p in cmap["parts"] for l in p["lessons"] for w in l["wiki"])
        shipped = sorted(p.stem for p in (ROOT / "wiki").glob("*.md") if p.name != "README.md")
        self.assertEqual(runbooks, shipped, "a wiki runbook is missing from the compendium, or is shown twice")
        # The banner carries the same as-of line as the page.
        asof = re.search(r"v\d+ · updated \d{4}-\d{2}-\d{2} · evidence checked \d{4}-\d{2}-\d{2} \(Claude Code v[\d.]+\)", page).group(0)
        self.assertIn(f'<p class="asof">{asof}</p>', html, "the compendium banner lacks the page's as-of line")

    def test_only_known_links_become_plain_text_in_the_compendium(self):
        """A Markdown link loses its target and the build quietly turns it into text, so a broken link ships."""
        src = (ROOT / "tools" / "build_compendium.py").read_text(encoding="utf-8")
        m = re.search(r"^KNOWN_DEGRADED = (set\(\)|\{[^}]*\})", src, re.M)
        self.assertTrue(m, "tools/build_compendium.py lost its KNOWN_DEGRADED allowlist")
        allowed = set(eval(m.group(1), {"__builtins__": {}, "set": set}))
        html = (ROOT / "docs" / "orchestrating-claude-compendium.html").read_text(encoding="utf-8")
        degraded = set(re.findall(r'<span class="file-ref" title="#([^"]+)"', html))
        self.assertEqual(degraded, allowed, "the compendium's links that became text differ from KNOWN_DEGRADED in tools/build_compendium.py")
        self.assertIn("unexpected = sorted(set(degraded) - KNOWN_DEGRADED)", src, "the build no longer stops on a link that lost its target")


if __name__ == "__main__":
    unittest.main()
