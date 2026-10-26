"""Mutation tests for the guardrails: make catastrophic changes to a throwaway copy and check the suite catches each.

Each mutation copies the clone's tracked and untracked files into build/test-tmp/mutation/,
applies one damaging edit, and runs tests/run.sh there. A mutation the suite does not
fail on is NOT CAUGHT, which means a guardrail is missing. The clone itself is never edited.

Usage: python3 -I tests/mutation/mutate.py            all mutations (a few minutes)
       python3 -I tests/mutation/mutate.py 3 7        only these, by number
       add --record to write the result to tests/results/mutation.json
Exit 1 if any mutation is not caught.
"""
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
WORK = ROOT / "build" / "test-tmp" / "mutation"
# Skip the nested runner canary inside each copy; this script is the outer canary.
SELFTEST_ENV = {**os.environ, "GUIDE_SELFTEST": "1"}
PB = "playbook/agent-harness-playbook.md"


def drop_section(text, heading_prefix):
    lines = text.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.startswith(heading_prefix))
    level = len(heading_prefix) - len(heading_prefix.lstrip("#"))
    end = next((j for j in range(start + 1, len(lines)) if re.match(rf"#{{1,{level}}} ", lines[j])), len(lines))
    return "".join(lines[:start] + lines[end:])


def sub_once(pattern, repl):
    def edit(text):
        new, n = re.subn(pattern, repl, text, count=1, flags=re.M)
        if not n:
            raise ValueError(f"mutation pattern not found: {pattern}")
        return new
    return edit


# (what it simulates, file, edit). A None edit deletes the file.
MUTATIONS = [
    ("A playbook section is deleted (§9.5)", PB, lambda t: drop_section(t, "### 9.5 ")),
    ("A playbook template is deleted (Template K)", PB, lambda t: drop_section(t, "### K. ")),
    ("A law is renamed", PB, sub_once(r"^### Law 7\. .*$", "### Law 7. Let the builder check its own work")),
    ("The playbook is truncated to half", PB, lambda t: t[: len(t) // 2]),
    ("A primary source URL is removed from §20", PB, sub_once(r"^- Every, compound engineering \[P\]: .*\n", "")),
    ("A router row is deleted (row 11)", "ENTRY.md", sub_once(r"^\| 11 \|.*\n", "")),
    ("A router row points to a section that doesn't exist", "ENTRY.md", sub_once(r"`cs:3 14 4 8 11.3`", "`cs:9 14 4 8 11.3`")),
    ("ENTRY.md tells sessions to read the whole playbook", "ENTRY.md", sub_once(r"Never load the whole playbook: it is about 1,500 lines\.", "Read the whole playbook first.")),
    ("A runbook is deleted (unstick)", "wiki/unstick.md", None),
    ("A runbook loses its checklist", "wiki/verify.md", sub_once(r"^## Checklist$", "## Notes")),
    ("A wiki link breaks", "wiki/start-a-task.md", sub_once(r"#51-discovery-from-pain-point-to-issues", "#51-discovery")),
    ("A personal path is committed", "README.md", lambda t: t + "\nNotes live in /Users/someone/private/notes.md\n"),  # privacy: allow
    ("The 'playbook wins' rule is dropped from AGENTS.md", "AGENTS.md", sub_once(r"^When the playbook and another layer disagree.*\n", "")),
    ("The privacy hard rule is dropped from AGENTS.md", "AGENTS.md", sub_once(r"^\*\*Privacy \(hard rule\)\*\*\n(- .*\n)+", "")),
    ("/guide gets a pre-run shell line again", "skills/guide/SKILL.md", sub_once(r"^The guide is a separate folder", "Root: !`git rev-parse --show-toplevel`\n\nThe guide is a separate folder")),
    ("The CLAUDE.md snippet becomes an @ import", "skills/guide/snippet.md", lambda t: "@{{GUIDE}}/ENTRY.md\n"),
    ("Template M lets Bash comment on the PR", PB, sub_once(r'--allowedTools "Bash\(gh pr diff:\*\)', '--allowedTools "Bash(gh pr comment:*),Bash(gh pr diff:*)')),
    ("Template M loses the secret scrub", PB, sub_once(r'^\s+CLAUDE_CODE_SUBPROCESS_ENV_SCRUB: "1".*\n', "")),
    ("Template F's deny rule becomes a Write rule that never matches", PB, sub_once(r'"deny": \["Edit\(/\.claude/\*\*\)"\]', '"deny": ["Write(.claude/**)"]')),
    ("The Stop hook stops blocking", PB, sub_once(r"^exit 2$", "exit 0")),
    ("The page source changes without rebuilding site/index.html", "site/orchestrating-claude.html", lambda t: t.replace("<title>Orchestrating Claude</title>", "<title>Orchestrating Claude!</title>", 1)),
    ("A wiki page changes without rebuilding the compendium", "wiki/improve.md", lambda t: t + "\nOne more line.\n"),
    ("The section tool is deleted", "tools/section.py", None),
    ("A playbook edit is not rebuilt into sections/", PB, sub_once(r"^(### 9\.5 .*)$", r"\1 (edited)")),
    ("A section file agents fetch is deleted", "sections/9.5.md", None),
    ("A route bundle agents fetch is deleted", "routes/row-11.md", None),
    ("README loses the no-clone route for linked agents", "README.md", sub_once(r"^## For AI agents given this repository's link\n", "## Notes\n")),
    ("/guide loses its remote mode", "skills/guide/SKILL.md", sub_once(r" In remote mode, fetch .*$", "")),
    ("/guide loses its default repository", "skills/guide/SKILL.md", sub_once(r"environment variable, else `[^`]+`", "environment variable, else by asking the user")),
    ("ENTRY.md sends every no-clone agent to main", "ENTRY.md", sub_once(r"raw\.githubusercontent\.com/<owner>/<repo>/<branch>", "raw.githubusercontent.com/<owner>/<repo>/main")),
    ("README claims the wrong number of scenarios", "README.md", sub_once(r"a router from 19 scenarios", "a router from 18 scenarios")),
]


def copy_clone(dest):
    files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    for f in filter(None, files):
        src = ROOT / f
        if src.is_file():
            (dest / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / f)
    if (ROOT / ".privacy-terms").exists():
        shutil.copy2(ROOT / ".privacy-terms", dest / ".privacy-terms")
    # A git dir under another name: sandboxes often refuse writes to .git/config and .git/hooks.
    gitdir = dest.parent / (dest.name + ".gitdir")
    shutil.rmtree(gitdir, ignore_errors=True)
    subprocess.run(["git", "init", "-q", "--template=", f"--separate-git-dir={gitdir}"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)


def main(picks, record=False):
    caught = missed = 0
    started, results = time.time(), []
    # Control: the unmodified copy must pass, or every mutation would look caught.
    control = WORK / "control"
    shutil.rmtree(control, ignore_errors=True)
    control.mkdir(parents=True)
    copy_clone(control)
    run = subprocess.run(["bash", "tests/run.sh"], cwd=control, capture_output=True, text=True, env=SELFTEST_ENV)
    shutil.rmtree(control, ignore_errors=True)
    if run.returncode != 0:
        print("STOP the unmodified copy already fails tests/run.sh; fix that first:\n" + run.stdout)
        return 2
    print("PASS control: the unmodified copy passes")
    for n, (what, path, edit) in enumerate(MUTATIONS, 1):
        if picks and n not in picks:
            continue
        dest = WORK / f"m{n:02d}"
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        copy_clone(dest)
        target = dest / path
        if edit is None:
            target.unlink()
        else:
            target.write_text(edit(target.read_text(encoding="utf-8")), encoding="utf-8")
        run = subprocess.run(["bash", "tests/run.sh"], cwd=dest, capture_output=True, text=True, env=SELFTEST_ENV)
        failing = [l[5:] for l in run.stdout.splitlines() if l.startswith("FAIL ")]
        if run.returncode != 0:
            caught += 1
            print(f"CAUGHT     {n:2d}. {what} — {'; '.join(failing)[:150]}")
        else:
            missed += 1
            print(f"NOT CAUGHT {n:2d}. {what}")
        results.append({"n": n, "mutation": what, "caught": run.returncode != 0, "failing": failing})
        shutil.rmtree(dest, ignore_errors=True)
    took = round(time.time() - started, 1)
    print(f"SUMMARY {caught} caught, {missed} not caught, in {took}s")
    if record:
        out = ROOT / "tests" / "results" / "mutation.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"date": datetime.date.today().isoformat(), "caught": caught, "not_caught": missed,
                                   "duration_s": took, "mutations": results}, indent=1) + "\n", encoding="utf-8")
    return 1 if missed else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(main({int(a) for a in args if a.isdigit()}, record="--record" in args))
