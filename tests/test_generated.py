"""Generated files stay in step with their sources: site/index.html and the compendium.

Run: python3 -I tests/test_generated.py   (or the whole suite: tests/run.sh)
"""
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

    def test_compendium_works_offline(self):
        """The compendium starts loading something from the network."""
        html = (ROOT / "docs" / "orchestrating-claude-compendium.html").read_text(encoding="utf-8")
        self.assertNotRegex(html, r"<(script|link)[^>]+(src|href)=\"https?://", "the compendium must load nothing from the network")


if __name__ == "__main__":
    unittest.main()
