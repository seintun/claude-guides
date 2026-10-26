"""Tests that test the test machinery, so the suite cannot be switched off without a failure.

A guard that nobody checks can be deleted, weakened or bypassed in a quiet edit. These tests cover
four ways that happens:
  1. A checker (tools/check_links.py, check_privacy.py, check_entry.py) stops failing on bad input.
     Each one is run on a known-bad file and must exit 1, and on a good file and must exit 0.
  2. Tests disappear. tests/baselines/suite.json lists the test files and the minimum number of
     test cases. Lowering `min_test_cases` or removing a file from `files` is a deliberate, reviewed
     change: make it in the same commit as the removal, and say why in the message.
  3. tests/run.sh or .githooks/pre-commit stops running a step, ignores a failure or exits 0 early.
     The static checks here read their text. tests/run.sh also runs RunnerIntegrityTests as its own
     step, so dropping the unittest step still fails: the two paths cover each other.
  4. The runner stops failing when something is broken. The canary copies the repository, plants one
     failure and expects `bash tests/run.sh` to exit 1 with a "FAIL privacy" line. A control copy,
     with nothing planted, must exit 0.

Run all tests:  python3 -I -m unittest discover -s tests -p 'test_*.py'
Run this file:  python3 -I tests/test_harness.py [-v] [RunnerIntegrityTests]
Where the default temp folder is not writable, set TEST_TMP to a writable folder (tests/run.sh does).
The canary starts tests/run.sh with GUIDE_SELFTEST=1 so that the copy skips the canary and does not
recurse. tests/run.sh must never set or clear that variable; a test below checks it.
"""
import ast
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
TESTS = ROOT / "tests"
RUN_SH = TESTS / "run.sh"
PRE_COMMIT = ROOT / ".githooks" / "pre-commit"
SUITE = TESTS / "baselines" / "suite.json"
IN_CANARY_COPY = os.environ.get("GUIDE_SELFTEST") == "1"

# One personal path planted into a copy of the repository. The marker lets the real scan skip this line.
PLANTED_PATH = "Notes in /Users/someone/private.md"  # privacy: allow
BAD_PATH_LINE = "See /Users/someone/x for details."  # privacy: allow
BAD_EMAIL_LINE = "Write to someone@private-corp.net."  # privacy: allow


def make_tmp(case):
    """A fresh temp dir under TEST_TMP (if set), removed when the test ends."""
    base = os.environ.get("TEST_TMP") or None
    if base:
        os.makedirs(base, exist_ok=True)
    path = tempfile.mkdtemp(prefix="harness-", dir=base)
    case.addCleanup(shutil.rmtree, path, True)
    return pathlib.Path(path)


def run_tool(name, *args):
    """Run one of the repository's tools the way tests/run.sh does, from the repository root."""
    cmd = [sys.executable, "-I", str(ROOT / "tools" / name), *map(str, args)]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=ROOT)


def code_lines(path):
    """The non-blank, non-comment lines of a shell script, stripped."""
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.lstrip().startswith("#")]


def count_test_cases():
    """Test methods named test_* in classes across tests/test_*.py, counted from the source."""
    total = 0
    for path in sorted(TESTS.glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            total += sum(1 for n in cls.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_"))
    return total


# --- 1. Checker self-tests -------------------------------------------------------------------------

class CheckerSelfTests(unittest.TestCase):
    """Each checker must fail on a known-bad input, or a broken guide would pass."""

    def setUp(self):
        self.dir = make_tmp(self)

    def write(self, name, text):
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_links_checker_fails_on_broken_file_and_anchor(self):
        """check_links.py passes a Markdown file whose relative links and #anchors are all broken."""
        (self.dir / "other.md").write_text("# Real heading\n", encoding="utf-8")
        bad = self.write("bad.md", "# Title\n\nSee [gone](missing-file.md), [anchor](#no-such-heading) "
                                   "and [cross](other.md#no-such-heading).\n")
        run = run_tool("check_links.py", bad)
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertIn("missing file missing-file.md", run.stdout)
        self.assertEqual(run.stdout.count("no heading #no-such-heading"), 2, run.stdout)
        self.assertIn("3 checked, 3 broken", run.stdout)

    def test_links_checker_passes_good_file(self):
        """check_links.py rejects a Markdown file whose links and anchors all resolve."""
        (self.dir / "other.md").write_text("# Real heading\n", encoding="utf-8")
        good = self.write("good.md", "# Title\n\nSee [file](other.md), [anchor](other.md#real-heading) "
                                     "and [self](#title).\n")
        run = run_tool("check_links.py", good)
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertIn("3 checked, 0 broken", run.stdout)

    def test_privacy_checker_fails_on_personal_path_and_email(self):
        """check_privacy.py lets a personal home path or a non-example email address through."""
        bad = self.write("bad.txt", BAD_PATH_LINE + "\n" + BAD_EMAIL_LINE + "\n")
        run = run_tool("check_privacy.py", "--files", bad)
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertRegex(run.stdout, r"FAIL .*bad\.txt:1: home path")
        self.assertRegex(run.stdout, r"FAIL .*bad\.txt:2: email address")
        self.assertIn("FAIL privacy: 1 files scanned, 2 flagged", run.stdout)

    def test_privacy_checker_passes_clean_file(self):
        """check_privacy.py rejects a clean file, so every commit would be blocked."""
        clean = self.write("clean.txt", "Nothing private here. Ask noreply@example.com.\n")
        run = run_tool("check_privacy.py", "--files", clean)
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertIn("PASS privacy: 1 files scanned", run.stdout)

    def test_privacy_checker_fails_on_a_missing_named_file(self):
        """check_privacy.py --files passes when the file it was told to scan does not exist."""
        run = run_tool("check_privacy.py", "--files", self.dir / "no-such-file.txt")
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertIn("not a file", run.stdout)

    def entry_variant(self, edit):
        text = (ROOT / "ENTRY.md").read_text(encoding="utf-8")
        path = self.write("ENTRY.md", edit(text))
        return run_tool("check_entry.py", path)

    def test_entry_checker_fails_on_unknown_section_id(self):
        """check_entry.py passes an ENTRY.md that points at a section id that does not exist (cs:9)."""
        run = self.entry_variant(lambda t: t + "\n- Bogus pointer: `cs:9`\n")
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertRegex(run.stdout, r"FAIL Every section id resolves .*unknown: cs:9")

    def test_entry_checker_fails_with_fourteen_rows(self):
        """check_entry.py passes an ENTRY.md whose scenario router has shrunk to 14 rows."""
        def drop_rows(text):
            lines = text.splitlines(keepends=True)
            rows = [i for i, l in enumerate(lines) if re.match(r"\| \d+ \|", l)]
            self.assertGreater(len(rows), 14, "ENTRY.md has no spare router rows to drop")
            drop = set(rows[14:])
            return "".join(l for i, l in enumerate(lines) if i not in drop)
        run = self.entry_variant(drop_rows)
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertIn("FAIL Scenario router has at least 15 rows — 14 rows", run.stdout)

    def test_entry_checker_fails_when_entry_grows_past_150_lines(self):
        """check_entry.py passes an ENTRY.md that has grown into a second playbook."""
        run = self.entry_variant(lambda t: t + "\nPadding line.\n" * 150)
        self.assertEqual(run.returncode, 1, run.stdout)
        self.assertIn("FAIL ENTRY.md is under 150 lines", run.stdout)

    def test_entry_checker_passes_the_real_entry(self):
        """check_entry.py rejects the real ENTRY.md, by default and when given its path."""
        for args in ((), (ROOT / "ENTRY.md",)):
            run = run_tool("check_entry.py", *args)
            self.assertEqual(run.returncode, 0, run.stdout)
            self.assertNotIn("FAIL", run.stdout)


# --- 2. Suite floor --------------------------------------------------------------------------------

class SuiteFloorTests(unittest.TestCase):
    """Tests cannot be deleted or silently left out of discovery."""

    @classmethod
    def setUpClass(cls):
        cls.suite = json.loads(SUITE.read_text(encoding="utf-8"))

    def test_every_listed_test_file_exists(self):
        """A test file listed in baselines/suite.json was deleted or renamed, taking its tests with it."""
        files = self.suite["files"]
        self.assertTrue(files, "suite.json lists no test files")
        missing = [f for f in files if not (ROOT / f).is_file()]
        self.assertEqual(missing, [], "Listed test files are missing. If you removed them on purpose, "
                                      "update tests/baselines/suite.json in the same reviewed change.")
        for f in files:
            self.assertRegex(f, r"^tests/test_\w+\.py$", f"{f} would not be found by unittest discovery")

    def test_total_test_cases_meet_the_floor(self):
        """Test methods were deleted: fewer test_* cases than baselines/suite.json requires."""
        floor, count = self.suite["min_test_cases"], count_test_cases()
        self.assertGreaterEqual(count, floor, f"{count} test cases, below the floor of {floor}. Restore the "
                                              "tests, or lower the floor in a deliberate, reviewed change.")

    def test_unittest_discovery_collects_the_floor(self):
        """A test class stopped subclassing TestCase, so discovery runs fewer cases than the source holds."""
        suite = unittest.defaultTestLoader.discover(str(TESTS), pattern="test_*.py", top_level_dir=str(TESTS))
        collected = suite.countTestCases()
        self.assertGreaterEqual(collected, self.suite["min_test_cases"],
                                f"unittest discovery collects {collected} cases, below the floor")

    def test_every_test_file_named_in_the_readme_exists(self):
        """tests/README.md names a test file that is gone, so its description of the suite is false."""
        readme = (TESTS / "README.md").read_text(encoding="utf-8")
        named = sorted(set(re.findall(r"\btest_\w+\.py\b", readme)))
        self.assertTrue(named, "tests/README.md names no test files")
        missing = [n for n in named if not (TESTS / n).is_file()]
        self.assertEqual(missing, [], "tests/README.md names test files that do not exist")


# --- 3. Runner integrity ---------------------------------------------------------------------------

class RunnerIntegrityTests(unittest.TestCase):
    """tests/run.sh and the pre-commit hook still run every check and still report failure."""

    # Each step must be a `step "name" <command>` line, so its failure sets the exit code.
    COMMANDS = {
        "checks/static.sh": r"checks/static\.sh",
        "tools/check_links.py": r"python3 -I tools/check_links\.py",
        "tools/check_privacy.py": r"python3 -I tools/check_privacy\.py",
        "tools/check_entry.py": r"python3 -I tools/check_entry\.py",
        "the runner-integrity step": r"python3 -I tests/test_harness\.py RunnerIntegrityTests",
    }
    STEP = r'step\s+"[^"]+"\s+'
    UNITTEST = r"python3 -I -m unittest discover -s tests -p 'test_\*\.py'"
    SWALLOW = r"\|\|\s*(?:true|:)(?!\w)|;\s*true(?!\w)"

    def test_run_sh_calls_every_check_and_the_unittest_step(self):
        """tests/run.sh drops a check or the unittest step, so that part of the suite never runs."""
        lines = code_lines(RUN_SH)
        for name, command in self.COMMANDS.items():
            self.assertTrue(any(re.fullmatch(self.STEP + command, l) for l in lines), f"run.sh has no step line for {name}")
        self.assertTrue(any(re.search(self.UNITTEST, l) for l in lines), "run.sh has no unittest discover line")

    def test_run_sh_cannot_exit_zero_early_or_hide_a_failure(self):
        """tests/run.sh exits 0 early, swallows a step failure with `|| true`, or loses its EXIT trap and final exit."""
        lines = code_lines(RUN_SH)
        self.assertEqual(lines[-1], 'exit "$failed"', "run.sh must end with exit \"$failed\"")
        self.assertTrue(any(l.startswith("trap ") and "EXIT" in l and 'exit "$failed"' in l for l in lines),
                        "run.sh must keep its EXIT trap, which turns a stray exit 0 into exit \"$failed\"")
        self.assertEqual([l for l in lines if re.search(r"\bexit\s+0\b", l)], [], "run.sh contains exit 0")
        runs_a_check = re.compile("|".join([*self.COMMANDS.values(), self.UNITTEST]))
        hidden = [l for l in lines if runs_a_check.search(l) and re.search(self.SWALLOW, l)]
        self.assertEqual(hidden, [], "a step line swallows its failure")
        self.assertGreaterEqual(sum(l.count("failed=1") for l in lines), 2,
                                "run.sh must set failed=1 in the step function and after the unittest step")

    def test_run_sh_never_touches_guide_selftest(self):
        """tests/run.sh sets or clears GUIDE_SELFTEST, which would silence the canary or make it recurse."""
        lines = code_lines(RUN_SH)
        touched = [l for l in lines if "GUIDE_SELFTEST" in l or re.search(r"\benv\s+(-i|-u|--ignore|--unset)|\bunset\b", l)]
        self.assertEqual(touched, [], "run.sh must pass GUIDE_SELFTEST through to the unittest step unchanged")

    def test_pre_commit_hook_runs_the_suite_and_cannot_pass_early(self):
        """The pre-commit hook stops exec'ing tests/run.sh, exits 0, or loses its executable bit."""
        self.assertTrue(os.access(PRE_COMMIT, os.X_OK), ".githooks/pre-commit is not executable; git skips it")
        lines = code_lines(PRE_COMMIT)
        self.assertTrue(any(re.match(r"exec\s+.*tests/run\.sh", l) for l in lines), "the hook must exec tests/run.sh")
        self.assertEqual([l for l in lines if re.search(r"\bexit\s+0\b|" + self.SWALLOW, l)], [],
                         "the hook must not exit 0 or swallow a failure")


# --- 4. Runner canary ------------------------------------------------------------------------------

def copy_repo(dest):
    """Copy the tracked and untracked files (plus .privacy-terms) into dest, as the mutation suite does."""
    listed = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=ROOT,
                            capture_output=True, check=True).stdout.decode("utf-8", "replace")
    for rel in filter(None, listed.split("\0")):
        src = ROOT / rel
        if src.is_file():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / rel)
    if (ROOT / ".privacy-terms").is_file():
        shutil.copy2(ROOT / ".privacy-terms", dest / ".privacy-terms")


def clean_env(**extra):
    """os.environ without GIT_* variables. A commit hook runs with GIT_INDEX_FILE and friends set, and a
    git command in the throwaway copy would otherwise write to the real repository's index."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(extra)
    return env


def init_git(dest):
    """Make dest a git checkout. The git dir lives beside it: sandboxes often refuse writes to .git/config."""
    gitdir = dest.parent / (dest.name + ".gitdir")
    subprocess.run(["git", "init", "-q", "--template=", f"--separate-git-dir={gitdir}"], cwd=dest,
                   check=True, capture_output=True, env=clean_env())
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True, capture_output=True, env=clean_env())


def run_in_copy(plant):
    """Run `bash tests/run.sh` in a throwaway copy of the repository, with one failure planted if asked."""
    base = os.environ.get("TEST_TMP") or None
    if base:
        os.makedirs(base, exist_ok=True)
    parent = pathlib.Path(tempfile.mkdtemp(prefix="harness-canary-", dir=base))
    try:
        dest = parent / "repo"
        dest.mkdir()
        copy_repo(dest)
        if plant:
            with open(dest / "README.md", "a", encoding="utf-8") as f:
                f.write("\n" + PLANTED_PATH + "\n")
        init_git(dest)
        env = clean_env(GUIDE_SELFTEST="1")
        return subprocess.run(["bash", "tests/run.sh"], cwd=dest, env=env, capture_output=True, text=True, timeout=300)
    finally:
        shutil.rmtree(parent, ignore_errors=True)


@unittest.skipIf(IN_CANARY_COPY, "NOT RUN: GUIDE_SELFTEST=1 means this is the copy a canary started; running again would recurse")
class RunnerCanaryTests(unittest.TestCase):
    """tests/run.sh must exit 1 when something is broken, and 0 when nothing is."""

    @classmethod
    def setUpClass(cls):
        # Two independent copies, run side by side to halve the wait.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            planted, control = pool.submit(run_in_copy, True), pool.submit(run_in_copy, False)
            cls.planted, cls.control = planted.result(), control.result()

    def test_planted_failure_makes_run_sh_exit_one(self):
        """tests/run.sh exits 0 or hides the FAIL line when a personal path is planted in README.md."""
        out = self.planted.stdout
        self.assertEqual(self.planted.returncode, 1, out[-2000:])
        self.assertIn("FAIL privacy", out)
        self.assertIn("SUMMARY FAIL", out)

    def test_unplanted_copy_exits_zero(self):
        """tests/run.sh fails on a clean copy of the repository, so the canary proves nothing."""
        out = self.control.stdout
        self.assertEqual(self.control.returncode, 0, "The unmodified copy already fails tests/run.sh, so the canary "
                                                     "cannot tell a working runner from a broken one. Fix these first:\n" + out[-2000:])
        self.assertIn("SUMMARY all PASS", out)
        self.assertNotIn("FAIL", out)


if __name__ == "__main__":
    unittest.main()
