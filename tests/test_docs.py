"""Guards on the layers around the playbook: runbooks, maps, and the rules that keep the guide the guide.

  Runbooks      each wiki runbook keeps its shape and its tie to the playbook.
  Maps          llms.txt, the README files and tools/README.md name what exists.
  Guiding star  AGENTS.md, ENTRY.md and CLAUDE.md keep stating the rules everything else rests on.

Run: python3 -I tests/test_docs.py   (or the whole suite: python3 -I -m unittest discover -s tests -p 'test_*.py')
"""
import os
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import update_baselines as ub  # noqa: E402

PLAYBOOK_REL = "playbook/agent-harness-playbook.md"
PLAYBOOK_LINK = "../" + PLAYBOOK_REL + "#"
RUNBOOKS = ["start-a-task", "grill", "orchestrate", "verify", "run-unattended",
            "guardrails", "build-a-harness", "unstick", "improve"]
REQUIRED_SECTIONS = ["Steps", "Checklist", "Templates", "Watch out for", "Go deeper"]
TOP_DIRS = ["site", "playbook", "wiki", "docs", "issues", "research", "checks", "tools", "skills", "tests"]
CHANGED_ON_PURPOSE = "If the change is intended, update the expectation in tests/test_docs.py in the same commit."


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def short(items, limit=15):
    items = list(items)
    extra = f" ... and {len(items) - limit} more" if len(items) > limit else ""
    return "\n  " + "\n  ".join(str(x) for x in items[:limit]) + extra


def md_links(text):
    """(line number, target) for each Markdown link outside code fences and inline code."""
    fence = False
    for no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            for target in re.findall(r"\]\(([^)\s]+)\)", re.sub(r"`[^`]*`", "", line)):
                yield no, target


def local_links(rel):
    """(line, target as written, path relative to the repository root, anchor) for each relative link in a file."""
    base = (ROOT / rel).parent
    out = []
    for no, target in md_links(read(rel)):
        if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I):  # http:, https:, mailto:
            continue
        file_part, _, anchor = target.partition("#")
        dest = pathlib.Path(os.path.normpath(base / file_part)) if file_part else ROOT / rel
        out.append((no, target, pathlib.Path(os.path.relpath(dest, ROOT)).as_posix(), anchor))
    return out


def broken_links(rel):
    """Messages for each relative link in a file whose target file or #anchor does not exist."""
    problems = []
    for no, target, dest, anchor in local_links(rel):
        if not (ROOT / dest).exists():
            problems.append(f"{rel}:{no}: {target} (no file {dest})")
        elif anchor and dest.endswith(".md") and anchor not in ub.slug_set(read(dest)):
            problems.append(f"{rel}:{no}: {target} (no heading #{anchor} in {dest})")
    return problems


def link_targets(rel):
    return {dest for _, _, dest, _ in local_links(rel)}


class Runbooks(unittest.TestCase):
    def runbook(self, name):
        rel = f"wiki/{name}.md"
        if not (ROOT / rel).exists():
            self.fail(f"{rel} does not exist. Restore it: ENTRY.md, the wiki index and llms.txt route to it.")
        return rel, read(rel)

    def test_runbook_exists(self):
        """A runbook is deleted or renamed, and the router and the index point at nothing."""
        for name in RUNBOOKS:
            with self.subTest(runbook=name):
                self.runbook(name)

    def test_runbook_keeps_its_sections(self):
        """A runbook loses Steps, Checklist, Templates, Watch out for or Go deeper."""
        for name in RUNBOOKS:
            with self.subTest(runbook=name):
                rel, text = self.runbook(name)
                titles = [t for _, lvl, t in ub.headings(text) if lvl == 2]
                # "## Checklist: validate a grill" counts as "## Checklist"; extra sections are allowed.
                missing = [s for s in REQUIRED_SECTIONS if not any(t == s or t.startswith(s + ":") for t in titles)]
                self.assertFalse(missing, f"{rel} has no \"## {'\", \"## '.join(missing)}\" heading. Restore the section (every runbook has "
                                          f"{', '.join(REQUIRED_SECTIONS)}). {CHANGED_ON_PURPOSE}")

    def test_runbook_opens_with_use_this_page_when(self):
        """A runbook opens with something other than the sentence that says when to use it."""
        for name in RUNBOOKS:
            with self.subTest(runbook=name):
                rel, text = self.runbook(name)
                after_title = text.split("\n", 1)[1] if text.startswith("# ") else text
                first = next((ln for ln in after_title.splitlines() if ln.strip()), "")
                self.assertRegex(first, r"^Use this page (when|before|after) ",
                                 f"{rel} opens with {first[:60]!r}. The first line under the title must start \"Use this page when\" "
                                 "(or \"before\" / \"after\", as run-unattended and improve do), so a reader knows in one sentence whether "
                                 "this is the page. Restore it.")

    def test_runbook_links_into_the_playbook(self):
        """A runbook stops pointing into the playbook, so it carries claims the playbook never graded."""
        for name in RUNBOOKS:
            with self.subTest(runbook=name):
                rel, text = self.runbook(name)
                self.assertIn(PLAYBOOK_LINK, text,
                              f"{rel} links no playbook anchor ({PLAYBOOK_LINK}...). A runbook adds no facts of its own: "
                              "link each step to the playbook section it summarises.")

    def test_runbook_links_resolve(self):
        """A playbook heading is renamed and a runbook's link to it dies."""
        for name in RUNBOOKS + ["case-study"]:
            with self.subTest(runbook=name):
                rel, _ = self.runbook(name)
                broken = broken_links(rel)
                self.assertFalse(broken, "broken links:" + short(broken) + "\nFix the link or restore the heading. python3 -I tools/check_links.py lists them all.")

    def test_case_study_links_the_playbook(self):
        """The case study is deleted or stops tying its story to the playbook."""
        self.assertTrue((ROOT / "wiki/case-study.md").exists(), "wiki/case-study.md does not exist. Restore it.")
        self.assertIn(PLAYBOOK_REL, read("wiki/case-study.md"),
                      "wiki/case-study.md no longer links the playbook. Each step of the story names the section it applied: restore those links.")

    def test_wiki_index_links_every_page(self):
        """A wiki page is added but the wiki index never links it, so nobody finds it."""
        linked = link_targets("wiki/README.md")
        pages = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "wiki").glob("*.md") if p.name != "README.md")
        missing = [p for p in pages if p not in linked]
        self.assertFalse(missing, "wiki/README.md does not link:" + short(missing) + "\nAdd a row for each page to the table in wiki/README.md.")


class Maps(unittest.TestCase):
    def test_llms_txt_links_resolve(self):
        """A file moves or is deleted and llms.txt, the machine-readable map, still points at it."""
        broken = broken_links("llms.txt")
        self.assertFalse(broken, "llms.txt links to missing targets:" + short(broken) + "\nFix or remove the line in llms.txt.")

    def test_llms_txt_lists_entry_runbooks_and_skills(self):
        """A runbook or skill is added but the agent map never lists it."""
        listed = link_targets("llms.txt")
        want = ["ENTRY.md"]
        want += sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "wiki").glob("*.md"))
        want += sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "skills").rglob("SKILL.md")
                       if not {"tests", "fixtures"} & set(p.relative_to(ROOT).parts))
        missing = [w for w in want if w not in listed]
        self.assertFalse(missing, "llms.txt does not list:" + short(missing) +
                         "\nAdd a one-line entry for each (AGENTS.md: when you add a file that matters to agents, add it to llms.txt).")

    def test_root_readme_links_entry_and_agents(self):
        """The README stops pointing people and agents at ENTRY.md and AGENTS.md."""
        listed = link_targets("README.md")
        missing = [f for f in ("ENTRY.md", "AGENTS.md") if f not in listed]
        self.assertFalse(missing, f"README.md does not link {missing}. Restore the links: they are the two doors into the repository.")

    def test_tools_readme_names_every_script(self):
        """A script is added to tools/ but tools/README.md never mentions it."""
        readme = read("tools/README.md")
        missing = sorted(p.name for p in (ROOT / "tools").glob("*.py") if p.name not in readme)
        self.assertFalse(missing, "tools/README.md does not name:" + short(missing) +
                         "\nAdd a row to the table in tools/README.md: what the script does and how to run it.")

    def test_top_level_folders_have_readmes(self):
        """A top-level folder is added or loses the README that lists its files."""
        tracked = set()
        try:
            names = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8", "replace")
            tracked = {n.split("/")[0] for n in names.split("\0") if "/" in n and not n.startswith(".")}
        except (OSError, subprocess.CalledProcessError):
            pass  # not a git checkout: fall back to the fixed list
        for d in sorted(set(TOP_DIRS) | tracked):
            with self.subTest(folder=d):
                if d == "tests" and not (ROOT / "tests" / "README.md").exists():
                    self.skipTest("tests/README.md does not exist yet (it is written separately); checking tests/ is skipped until it does")
                self.assertTrue((ROOT / d / "README.md").exists(),
                                f"{d}/README.md does not exist. AGENTS.md: every folder has a README.md that lists its files. Add it.")


class GuidingStar(unittest.TestCase):
    def test_agents_md_says_the_playbook_wins(self):
        """AGENTS.md drops the rule that the playbook wins when the layers disagree."""
        self.assertRegex(read("AGENTS.md"), r"(?i)disagree[^.\n]*,\s*the playbook wins",
                         "AGENTS.md no longer says \"When the playbook and another layer disagree, the playbook wins.\" "
                         "That rule keeps four layers from drifting apart. Restore the sentence.")

    def test_agents_md_keeps_the_privacy_hard_rule(self):
        """AGENTS.md drops the privacy hard rule, and a public repository starts leaking personal data."""
        text = read("AGENTS.md")
        self.assertIn("Privacy (hard rule)", text, "AGENTS.md has no \"Privacy (hard rule)\" block. This repository is public: restore it.")
        self.assertIn("tools/check_privacy.py", text, "AGENTS.md no longer tells agents to run tools/check_privacy.py before every commit. Restore the line.")

    def test_entry_md_says_never_load_the_whole_playbook(self):
        """ENTRY.md stops telling outside sessions never to load the whole playbook."""
        self.assertRegex(read("ENTRY.md"), r"(?i)never load the whole playbook",
                         "ENTRY.md no longer says \"Never load the whole playbook\". The guide's point is that a session loads a few "
                         "sections, not 1,500 lines. Restore the sentence.")

    def test_claude_md_imports_agents_md(self):
        """CLAUDE.md stops importing AGENTS.md, so Claude Code sessions skip the repository rules."""
        lines = [ln.strip() for ln in read("CLAUDE.md").splitlines()]
        self.assertIn("@AGENTS.md", lines, "CLAUDE.md has no line \"@AGENTS.md\". Restore it: it is how Claude Code loads the rules in AGENTS.md.")

    def test_entry_md_links_resolve(self):
        """ENTRY.md routes a session to a file that has moved or been deleted."""
        self.assertTrue(local_links("ENTRY.md"), "ENTRY.md has no relative links at all. The router must link its runbooks.")
        broken = broken_links("ENTRY.md")
        self.assertFalse(broken, "ENTRY.md routes to missing targets:" + short(broken) + "\nFix the link. Outside sessions follow ENTRY.md blindly.")



class AgentEntry(unittest.TestCase):
    def test_scenario_counts_match_the_router(self):
        """A router row is added or removed and README or llms.txt still claims the old number of scenarios."""
        rows = len(re.findall(r"^\| \d+ \|", read("ENTRY.md"), re.M))
        wrong = [(rel, n) for rel in ("README.md", "llms.txt", "AGENTS.md", "tests/README.md")
                 for n in re.findall(r"(\d+) (?:routing )?scenarios", read(rel)) if int(n) != rows and int(n) > 10]
        self.assertFalse(wrong, f"ENTRY.md has {rows} router rows, but these files claim another count: {wrong}")

    def test_readme_tells_a_linked_agent_how_to_read_without_a_clone(self):
        """An agent given only the repository link lands on README and finds no route that works without a clone."""
        text = read("README.md")
        head = text[: text.index("## Start here")]
        for needle in ("## For AI agents given this repository's link", "raw.githubusercontent.com/<owner>/<repo>/main", "ENTRY.md", "guide-index.json", "sections/<id>.md", "npx skills add"):
            self.assertIn(needle, head, f"README.md must say, before 'Start here', how an agent without a clone reads the guide: missing {needle!r}")


if __name__ == "__main__":
    unittest.main()
