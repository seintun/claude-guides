"""Adversarial edits from the independent guardrail review: 75 ways a careless or hostile editor could derail the guide.

Each edit is applied to its own throwaway copy of the clone (under build/test-tmp/review/), and tests/run.sh runs there.

Stages per mutation:
  raw        edit applied, nothing regenerated
  rebuilt    a careful editor also rebuilds the compendium and site/index.html
  rebaselined  ... and regenerates tests/baselines/playbook.json
A mutation is NOT CAUGHT as soon as a stage passes (exit 0). The first stage tells which check fires on the raw edit.
The clone itself is never edited. A control copy with no edit must pass first.
Usage: python3 -I tests/mutation/review_edits.py [n ...] [--record]   (about 5 minutes for all 75)
       --record writes the verdicts to tests/results/review-edits.json
"""
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
WORK = ROOT / "build" / "test-tmp" / "review"
PB = "playbook/agent-harness-playbook.md"
CS = "playbook/claude-cheat-sheet.md"


def rd(r, rel):
    return (r / rel).read_text(encoding="utf-8")


def wr(r, rel, text):
    (r / rel).write_text(text, encoding="utf-8")


def sub(rel, old, new, count=1):
    def edit(r):
        t = rd(r, rel)
        if old not in t:
            raise ValueError(f"{rel}: text not found: {old[:70]!r}")
        wr(r, rel, t.replace(old, new, count))
    return edit


def resub(rel, pat, repl, flags=re.M, count=1):
    def edit(r):
        t = rd(r, rel)
        new, n = re.subn(pat, repl, t, count=count, flags=flags)
        if not n:
            raise ValueError(f"{rel}: pattern not found: {pat[:70]!r}")
        wr(r, rel, new)
    return edit


def append(rel, text):
    def edit(r):
        wr(r, rel, rd(r, rel) + text)
    return edit


def hollow(rel, heading_prefix, stub):
    """Keep the heading, replace its body (up to the next heading of the same or higher level) with a stub."""
    def edit(r):
        lines = rd(r, rel).splitlines(keepends=True)
        i = next(n for n, l in enumerate(lines) if l.startswith(heading_prefix))
        level = len(heading_prefix) - len(heading_prefix.lstrip("#"))
        j = next((k for k in range(i + 1, len(lines)) if re.match(rf"#{{1,{level}}} ", lines[k])), len(lines))
        wr(r, rel, "".join(lines[:i + 1]) + "\n" + stub + "\n\n" + "".join(lines[j:]))
    return edit


def delete(rel):
    def edit(r):
        (r / rel).unlink()
    return edit


def routing_edit(fn):
    def edit(r):
        p = "tests/scenarios/routing.json"
        d = json.loads(rd(r, p))
        fn(d)
        wr(r, p, json.dumps(d, indent=2) + "\n")
    return edit


def swap_read_cells(r):
    t = rd(r, "ENTRY.md")
    a, b = "| `9.2 law-7` (add `12.3` for CI) |", "| `5.4 7` |"
    assert a in t and b in t
    wr(r, "ENTRY.md", t.replace(a, "@@A@@").replace(b, a).replace("@@A@@", b))


def swap_labels(r):
    t = rd(r, "ENTRY.md")
    a, b = '| 11 | Stuck agent (looping, false "done", lost context) |', "| 14 | Onboard a new repo |"
    assert a in t and b in t
    t = t.replace(a, '| 11 | Onboard a new repo |').replace(b, '| 14 | Stuck agent (looping, false "done", lost context) |')
    wr(r, "ENTRY.md", t)


def row14_runbook(r):
    t = rd(r, "ENTRY.md")
    lines = t.split("\n")
    n = next(i for i, l in enumerate(lines) if l.startswith("| 14 |"))
    lines[n] = lines[n].replace("[build-a-harness](wiki/build-a-harness.md)", "[unstick](wiki/unstick.md)")
    wr(r, "ENTRY.md", "\n".join(lines))


def drop_row12(r):
    resub("ENTRY.md", r"^\| 12 \|.*\n", "")(r)
    routing_edit(lambda d: d.__setitem__("scenarios", [s for s in d["scenarios"] if s["row"] != 12]))(r)


def drop_law7_from_row9(r):
    sub("ENTRY.md", "`9.2 law-7` (add `12.3` for CI)", "`9.2` (add `12.3` for CI)")(r)

    def fn(d):
        for s in d["scenarios"]:
            if s["row"] == 9:
                s["ids"] = [i for i in s["ids"] if i != "law-7"]
    routing_edit(fn)(r)


def unlink_test_file(name):
    def edit(r):
        delete(f"tests/{name}")(r)
        pat = re.compile(r"\[([^\]]*)\]\((?:tests/)?" + re.escape(name) + r"[^)]*\)")
        for p in r.rglob("*.md"):
            if {".git", "build"} & set(p.relative_to(r).parts):
                continue
            t = p.read_text(encoding="utf-8")
            n = pat.sub(r"\1", t)
            if n != t:
                p.write_text(n, encoding="utf-8")
    return edit


def thin_prose(rel, every):
    """Delete every Nth prose line outside code fences and headings, a slow silent decay."""
    def edit(r):
        out, fence, k = [], False, 0
        for line in rd(r, rel).splitlines(keepends=True):
            if line.lstrip().startswith("```"):
                fence = not fence
                out.append(line)
                continue
            if not fence and line.strip() and not line.startswith("#") and not line.startswith("|"):
                k += 1
                if k % every == 0:
                    continue
            out.append(line)
        wr(r, rel, "".join(out))
    return edit


def multi(*edits):
    def edit(r):
        for e in edits:
            e(r)
    return edit


MUTATIONS = [
    # --- ENTRY.md rules and instructions
    (1, "ENTRY.md: delete the Receipts and Two-strikes rules", multi(
        resub("ENTRY.md", r"^- \*\*Receipts\.\*\*.*\n", ""), resub("ENTRY.md", r"^- \*\*Two strikes\.\*\*.*\n", ""))),
    (2, "ENTRY.md: 'NOT RUN is not PASS' flipped to 'NOT RUN counts as PASS'", sub("ENTRY.md", "NOT RUN is not PASS. Load `9.4`.", "NOT RUN counts as PASS when the check is slow. Load `9.4`.")),
    (3, "ENTRY.md: keep 'never load whole playbook' line, step 3 says load the whole playbook anyway", sub("ENTRY.md", "3. **Load only the row's sections:**", "3. **Load the row's sections, then the whole playbook for context:**")),
    (4, "ENTRY.md: step 3 command points at a wrong path (tool/section.py)", sub("ENTRY.md", "GUIDE/tools/section.py 9.5 F", "GUIDE/tool/section.py 9.5 F")),
    (5, "ENTRY.md: phase table replaced by a stub", resub("ENTRY.md", r"## Phase table\n\n.*?\n(?=## Rules that apply everywhere)", "## Phase table\n\nSee the index.\n\n", flags=re.S)),
    (6, "ENTRY.md: scenario labels of rows 11 and 14 swapped", swap_labels),
    (7, "ENTRY.md: row 9 output says it approves the PR", sub("ENTRY.md", "Findings most serious first: correctness bugs and missing or weakened tests. Advisory; it never approves", "Findings most serious first. Approves the PR when the checks pass")),
    (8, "ENTRY.md: row 8 output drops retry cap and cost ceiling", sub("ENTRY.md", "State files, a stop condition, retry cap and cost ceiling, one status line per pass, results in a file, ticket or PR", "State files and results in a file, ticket or PR")),
    (9, "ENTRY.md: Read cells of rows 9 and 10 swapped (control)", swap_read_cells),
    (10, "ENTRY.md row 12 and its routing scenario deleted together", drop_row12),
    (11, "ENTRY.md row 9 drops law-7 and its scenario drops it too", drop_law7_from_row9),
    (12, "ENTRY.md: row 14 runbook link swapped to unstick (control)", row14_runbook),
    (13, "ENTRY.md: step 1 says do the work inside GUIDE", sub("ENTRY.md", "The guide gives advice; your project gets the work.", "The guide gives advice; do the work inside GUIDE and commit it there.")),
    # --- playbook prose
    (14, "Template B: STOP AND ASK block removed", resub(PB, r"STOP AND ASK ME IF\n.*?\n\n(?=HOW TO WORK)", "", flags=re.S)),
    (15, "Template B: 'NOT RUN is not PASS' and 'two strikes' rules removed", sub(PB, "- NOT RUN is not PASS.\n- If the same check fails twice for the same reason, stop and ask for a second opinion.\n", "")),
    (16, "Section 9.4 receipt format emptied, heading kept", resub(PB, r"(### 9\.4 Receipt format\n\n)```text\n.*?```\n", r"\1Receipts are optional for small changes.\n", flags=re.S)),
    (17, "Law 7 body flipped: builder reviews its own work", sub(PB, "reviewers get the artifact and the criteria, never the author's reasoning. Anonymize sources when comparing candidates. [D]", "the builder reviews its own work with its reasoning in hand; a second reviewer is a waste. [D]")),
    (18, "Law 9 body weakened: prose is enough", sub(PB, "lives in hooks, CI, permissions or the sandbox, not only in prose. [D]", "can live in prose; hooks and CI are optional. [D]")),
    (19, "Five [D] grades promoted to [P]", resub(PB, r"\[D\]", "[P]", count=5)),
    (20, "Evidence grade stripped from 18 [P] claims", resub(PB, r" \[P\]$", "", count=18)),
    (21, "Template F guardrails: terraform, kubectl, vercel and force-with-lease denies removed", sub(PB, '\n      "Bash(rm -rf:*)", "Bash(terraform apply:*)", "Bash(kubectl delete:*)", "Bash(vercel --prod:*)"\n', '\n      "Bash(rm -rf:*)"\n')),
    (22, "Template M: contents:write and actions pinned to @main", multi(sub(PB, "  contents: read\n  pull-requests: write\n  id-token: write", "  contents: write\n  pull-requests: write\n  id-token: write"), sub(PB, "@<full-commit-sha>", "@main", count=2))),
    (23, "Template H: stop condition and retry cap removed", multi(sub(PB, "Stop when <end condition>, or after 2 failures with the same cause.\n", ""), sub(PB, "retry at most once", "retry until it succeeds"))),
    (24, "Sections 10.3 and 12.4 hollowed out, headings kept", multi(hollow(PB, "### 10.3 ", "- See your security team."), hollow(PB, "### 12.4 ", "- Use judgment."))),
    (25, "Template I: retro changes applied without asking", sub(PB, "Don't apply anything until I say yes.", "Apply all proposed changes immediately.")),
    (26, "Template K: grill asks all questions in one message", sub(PB, "- One question per message. Give your recommended answer and what it costs.", "- Ask all your questions in one message, as a numbered list.")),
    (27, "Cheat sheet cs:3 (stuck signs) body replaced by a stub", hollow(CS, "## 3. ", "Restart.")),
    # --- tools
    (28, "section.py prints only the heading line of every id", sub("tools/section.py", 'print("\\n".join(lines[i:end]).rstrip() + "\\n")', 'print("\\n".join(lines[i:i + 1]).rstrip() + "\\n")')),
    (29, "section.py caps every section at 25 lines", sub("tools/section.py", 'print("\\n".join(lines[i:end]).rstrip() + "\\n")', 'print("\\n".join(lines[i:min(end, i + 25)]).rstrip() + "\\n")')),
    (30, "section.py silently drops the last line of each section", sub("tools/section.py", 'print("\\n".join(lines[i:end]).rstrip() + "\\n")', 'print("\\n".join(lines[i:end - 1]).rstrip() + "\\n")')),
    (31, "check_privacy.py always exits 0, and a leak lands in README", multi(sub("tools/check_privacy.py", "sys.exit(1 if found else 0)", "sys.exit(0)"), append("README.md", "\nNotes: /Users/jane/clients/acme/notes.md, contact jane@acme-corp.com\n"))),  # privacy: allow
    (32, "check_links.py always exits 0, and a broken link lands in orchestration-index.md", multi(sub("tools/check_links.py", "sys.exit(1 if broken else 0)", "sys.exit(0)"), append("orchestration-index.md", "\nSee [the old map](old-map.md).\n"))),
    (33, "check_entry.py always exits 0, and row 2 cites a nonexistent id", multi(sub("tools/check_entry.py", "sys.exit(1 if fails else 0)", "sys.exit(0)"), sub("ENTRY.md", "`5.3 5.4 6`", "`5.3 5.4 6 99.9`"))),
    # --- meta: the test harness itself
    (34, "tests/run.sh always exits 0", sub("tests/run.sh", 'exit "$failed"', "exit 0")),
    (35, "tests/run.sh skips the unittest step", sub("tests/run.sh", "out=\"$(python3 -I -m unittest discover -s tests -p 'test_*.py' 2>&1)\"; rc=$?", 'out="$(true 2>&1)"; rc=$?')),
    (36, "tests/test_templates.py deleted and unlinked from the README", unlink_test_file("test_templates.py")),
    (37, "tests/test_router.py deleted and unlinked from the README", unlink_test_file("test_router.py")),
    (38, ".githooks/pre-commit replaced by exit 0", lambda r: wr(r, ".githooks/pre-commit", "#!/usr/bin/env bash\nexit 0\n")),
    # --- AGENTS.md, wiki, skills, maps
    (39, "AGENTS.md: tests optional, weakening tests allowed", multi(sub("AGENTS.md", "Run it before every commit; it must end with SUMMARY all PASS:", "Running it is optional; commit without running it if it is slow:"), sub("AGENTS.md", "Never weaken or delete a test to make it pass.", "Weaken or delete any test that blocks you."))),
    (40, "AGENTS.md: facts rule replaced by 'add claims freely'", sub("AGENTS.md", "- Add no new factual claim without a primary source. Run a fact check, such as the `doc-checker` agent, before a claim lands.\n- Keep the evidence grade on every claim.\n", "- Add claims freely; sources can come later.\n")),
    (41, "AGENTS.md: privacy bullet says the repo is private, heading and tool name kept", sub("AGENTS.md", "- This repository is public. Never commit client or employer names, personal paths, email addresses, session ids or personal harness details.", "- This repository is private to the team. Commit client names, paths and harness details freely.")),
    (42, "wiki/grill.md: checklist emptied, heading kept", hollow("wiki/grill.md", "## Checklist", "- [ ] Done.")),
    (43, "wiki/verify.md: 'NOT RUN counts as PASS'", sub("wiki/verify.md", "NOT RUN is not PASS (D)", "NOT RUN counts as PASS (D)")),
    (44, "wiki/verify.md: Stop hook exit code 2 changed to 1", multi(sub("wiki/verify.md", "Exit code 2 blocks the stop", "Exit code 1 blocks the stop"), sub("wiki/verify.md", "confirm the hook returns exit 2", "confirm the hook returns exit 1"))),
    (45, "orchestration-index.md: 'never mark PASS without evidence' reversed", sub("orchestration-index.md", "Never mark PASS without evidence.", "Mark PASS whenever it looks fine.")),
    (46, "skills/guide/SKILL.md: allowed-tools widened to unrestricted Bash, Write, Edit", sub("skills/guide/SKILL.md", "allowed-tools: Read, Bash(git -C:*), Bash(python3 -I:*)", "allowed-tools: Bash, Read, Write, Edit")),
    (47, "Drop python -I from SKILL.md, snippet, prompt and ENTRY commands", multi(
        sub("skills/guide/SKILL.md", "python3 -I GUIDE/tools/section.py", "python3 GUIDE/tools/section.py"),
        sub("skills/guide/snippet.md", "python3 -I {{GUIDE}}", "python3 {{GUIDE}}"),
        sub("skills/guide/prompt.md", "python3 -I GUIDE/", "python3 GUIDE/"),
        sub("ENTRY.md", "python3 -I GUIDE/tools/section.py 9.5 F", "python3 GUIDE/tools/section.py 9.5 F"))),
    (48, "skills/guide/SKILL.md: 'say what the playbook lacks for thin rows' removed", sub("skills/guide/SKILL.md", "   If the row is marked thin, say what the playbook lacks instead of filling the gap from memory.\n", "")),
    (49, "snippet.md points at tool/section.py (control)", sub("skills/guide/snippet.md", "{{GUIDE}}/tools/section.py", "{{GUIDE}}/tool/section.py")),
    (50, "install.sh --apply also appends the snippet to ~/.claude/CLAUDE.md", sub("skills/guide/install.sh", '    ln -sfn "$target" "$link"\n', '    ln -sfn "$target" "$link"\n    sed "s|{{GUIDE}}|$GUIDE|g" "$here/snippet.md" >> "$HOME/.claude/CLAUDE.md"\n')),
    (51, "llms.txt calls ENTRY.md deprecated and points at the whole playbook", sub("llms.txt", "[ENTRY.md](ENTRY.md): entry point for a session in any other project.", "[ENTRY.md](ENTRY.md): deprecated; read the whole playbook instead.")),
    (52, "skills/grill/SKILL.md: disable-model-invocation removed (grill can auto-trigger)", sub("skills/grill/SKILL.md", "disable-model-invocation: true\n", "")),
    (53, "skills/grill/SKILL.md: 'cover the ground' rule and plain-text fallback removed", multi(
        sub("skills/grill/SKILL.md", "4. **Cover the ground:** the problem (who struggles and when, and what it costs them), where the work lives (the code, data and records it touches), the outcome metric, the appetite (time budget), no-gos, rabbit holes, failure cases, the riskiest assumption with the cheapest test of it, and open questions.\n", ""),
        sub("skills/grill/SKILL.md", " Without it, ask in plain text with options lettered A to D, recommendation first.", ""))),
    (54, "Playbook: every 14th prose line outside code fences deleted (~7% silent decay)", thin_prose(PB, 14)),
    (55, "wiki/run-unattended.md: Steps body replaced by a stub, heading kept", hollow("wiki/run-unattended.md", "## Steps", "1. Run the loop.")),
    (56, "Compendium builder injects an <img> beacon and a fetch() to a remote host", multi(
        sub("tools/build_compendium.py", "<body>\n", '<body><img src="https://stats.example.net/p.gif" alt="" width="1" height="1"><script>fetch("https://stats.example.net/hit")</script>\n'),
    )),
    (57, "skills/grill/SKILL.md: fact questions get options again (figures can slip in through a click)", sub("skills/grill/SKILL.md",
        "   - A fact question (a number, date, duration, count or name) is asked open, with no options. No option and no question text carries a figure the user, the project or a lookup did not supply: one click would turn your guess into the user's fact.\n", "")),
    (73, 'skills/prompt/SKILL.md: step 5 no longer lets a trivial prompt leave out CONTEXT (R1)', sub('skills/prompt/SKILL.md',
        ' in this order (a trivial prompt may leave out CONTEXT):', ' in this order:')),
    (74, 'skills/prompt/check_prompt.py: c-9 accepts a risk line anywhere, not only before GOAL (R1)', sub('skills/prompt/check_prompt.py',
        'for _, l in lines[:goal_at] if (m := RISK.match(l))', 'for _, l in lines if (m := RISK.match(l))')),
    (75, 'skills/prompt/check_prompt.py: the trivial form keeps only BUDGET, STOP AND ASK IF and HOW TO WORK (R1)', sub('skills/prompt/check_prompt.py',
        'TRIVIAL_PARTS = [p for p in PARTS if p != "CONTEXT"]', 'TRIVIAL_PARTS = ["BUDGET", "STOP AND ASK IF", "HOW TO WORK"]')),
    (58, "skills/prompt/SKILL.md: trace-every-figure rule and the fresh review before saving removed", multi(
        sub("skills/prompt/SKILL.md", "- Trace every figure. ", "- "),
        sub("skills/prompt/SKILL.md", "10. **Get a fresh review before saving**", "10. **Optionally ask someone to look**"))),
    (67, 'skills/prompt/SKILL.md: normal and high prompts no longer end with a fresh diff review (R2)', sub('skills/prompt/SKILL.md',
        ' At normal or high risk, HOW TO WORK ends with a fresh reviewer that reads the diff against DONE WHEN, even when the tests pass.', '')),
    (59, "skills/prompt/SKILL.md: self-check allowed in place of the fresh review, and gaps may be merged under the cap", multi(
        sub("skills/prompt/SKILL.md", "Without a subagent, don't review your own draft in its place, because a self-check misses the conflicts a fresh reader finds. Save the draft, write \"Review: not run\" at its top, and at hand-over give the user the review request to run in a fresh session.",
            "Without a subagent, check the draft yourself against the same list."),
        sub("skills/prompt/SKILL.md", ", one gap per line. Never merge gaps, or relabel an unknown as assumed, to stay under the limit.", "."))),
    (68, 'skills/prompt/SKILL.md: high-risk prompts no longer name the gate behind each hard constraint (R3)', sub('skills/prompt/SKILL.md',
        ' At high risk, also name for each hard constraint the gate that enforces it (a hook, CI, a permission); a constraint written only in prose is a request, not a control.', '')),
    (60, "skills/prompt/check_prompt.py always exits 0 and stops flagging relative terms", multi(
        sub("skills/prompt/check_prompt.py", "sys.exit(1 if fails else 0)", "sys.exit(0)"),
        sub("skills/prompt/check_prompt.py", 'report("FAIL" if relative else "PASS"', 'report("PASS"'))),
    (69, 'skills/prompt/SKILL.md: helper briefs no longer carry what is ruled out and decided (R4)', sub('skills/prompt/SKILL.md',
        ' what is already ruled out and already decided,', '')),
    (61, "skills/prompt/SKILL.md: chosen figures tagged ASSUMED on every use again, and check_prompt.py stops flagging repeats", multi(
        sub("skills/prompt/SKILL.md", 'Elsewhere, use the value plainly or by its name ("the merge cap"); don\'t tag it again.', "Tag the value `ASSUMED` wherever it appears."),
        sub("skills/prompt/check_prompt.py", 'report("WARN" if twice else "PASS"', 'report("PASS"'))),
    (70, 'skills/prompt/SKILL.md: loops lose idempotence and least privilege (R5)', sub('skills/prompt/SKILL.md',
        'one small action per pass, and running twice sends, charges or creates nothing twice; "no change" when nothing changed, a stop condition, at most 2 failures with the same cause, a cap per run, and only the tools and permissions the task needs. Nobody', 'one small action per pass, "no change" when nothing changed, a stop condition, at most 2 failures with the same cause, a cap per run. Nobody')),
    (62, "skills/prompt/SKILL.md: the reviewer's three questions and the test of stop conditions against the current state dropped", multi(
        sub("skills/prompt/SKILL.md", ", and a quoted answer to three questions: can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? Does any STOP AND ASK condition already hold? Is every file, record and system the steps need located, or listed as UNKNOWN? Then", ", then"),
        sub("skills/prompt/SKILL.md", "Test each STOP AND ASK line against what is known now (an empty folder, no repository, a missing export): one that already holds", "A STOP AND ASK condition that already holds"))),
    (71, 'skills/prompt/SKILL.md: plan files lose their docs/plans path and go back to scratch (R6)', multi(
        sub('skills/prompt/SKILL.md', ' at `docs/plans/<task>.md`', ''),
        sub('skills/prompt/SKILL.md', 'Plan files go in `docs/plans/`; other working files go in', 'Working files go in'))),
    (63, "skills/grill and skills/prompt stop asking where the code, data and records live", multi(
        sub("skills/grill/SKILL.md", " where the work lives (the code, data and records it touches),", ""),
        sub("skills/prompt/SKILL.md", " Find where the work lives: the code, data and records the task reads or changes. If the project doesn't hold them, ask where they are, or log an `UNKNOWN`.", ""))),
    # /prompt v10 (docs/plans/prompt-v10.md): each required item's sentence or check is deleted by one edit.
    (64, 'skills/prompt/SKILL.md: the risk line above the title dropped (R1)', sub('skills/prompt/SKILL.md',
        ', and write the result above the title as `Risk: trivial`, `Risk: normal` or `Risk: high`.', '.')),
    (65, 'skills/prompt/check_prompt.py: c-9 always PASS, so a prompt with no risk line passes (R1)', sub('skills/prompt/check_prompt.py',
        'report("PASS" if risk else "FAIL", "c-9', 'report("PASS", "c-9')),
    (66, "skills/prompt/check_prompt.py: the trivial form shrinks to v8's four parts, dropping BUDGET, STOP AND ASK IF and HOW TO WORK (R1)", sub('skills/prompt/check_prompt.py',
        'needed = TRIVIAL_PARTS if risk == "trivial" else PARTS', 'needed = ["GOAL", "DONE WHEN", "CONSTRAINTS", "REPORT"] if risk == "trivial" else PARTS')),
    (72, "skills/prompt/SKILL.md: the risk rule's definitions deleted, leaving a risk line with no rule behind it (R1)", sub('skills/prompt/SKILL.md',
        ' High: the work touches a schema, auth, payments, data deletion, a public API, infrastructure or production, adds a dependency, or runs unattended. Trivial: a small fix in one place, easy to undo, with no helpers or loop, such as a typo or a wrong comment. A change to user-visible behaviour is never trivial. Normal: everything else.', '')),
]


def copy_clone(dest, n):
    files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    for f in filter(None, files):
        src = ROOT / f
        if src.is_file():
            (dest / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / f)
    if (ROOT / ".privacy-terms").exists():
        shutil.copy2(ROOT / ".privacy-terms", dest / ".privacy-terms")
    gitdir = dest.parent / f"{dest.name}.gitdir"
    subprocess.run(["git", "init", "-q", "--template=", f"--separate-git-dir={gitdir}"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)


def suite(d):
    # GUIDE_SELFTEST=1 skips the nested runner canary inside each copy; this script is the outer canary.
    p = subprocess.run(["bash", "tests/run.sh"], cwd=d, capture_output=True, text=True, env={**os.environ, "GUIDE_SELFTEST": "1"})
    steps = [l[5:].split(" (")[0] for l in p.stdout.splitlines() if l.startswith("FAIL ")]
    tests = [l.strip() for l in p.stdout.splitlines() if re.match(r"\s+(FAIL|ERROR): ", l)]
    return p.returncode, steps, tests


def tool(d, *args):
    subprocess.run(["python3", "-I", *args], cwd=d, capture_output=True, text=True)


def main(picks, record=False):
    results = []
    control = WORK / "control"
    shutil.rmtree(control, ignore_errors=True)
    control.mkdir(parents=True)
    copy_clone(control, 0)
    rc, steps, tests = suite(control)
    if rc != 0:
        print("STOP the unmodified copy already fails tests/run.sh: " + "; ".join(steps + tests)[:300])
        return 2
    print("PASS control: the unmodified copy passes")
    for n, what, edit in MUTATIONS:
        if picks and n not in picks:
            continue
        dest = WORK / str(n)
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        copy_clone(dest, n)
        try:
            edit(dest)
        except Exception as e:  # noqa: BLE001
            print(f"EDIT-FAILED {n:2d}. {what}: {e}")
            results.append({"n": n, "what": what, "verdict": "EDIT FAILED", "detail": str(e)})
            continue
        rc, steps, tests = suite(dest)
        stage, detail = "raw", steps + tests
        if rc != 0:
            tool(dest, "tools/build_compendium.py")
            tool(dest, "tools/build_standalone.py")
            subprocess.run(["git", "add", "-A"], cwd=dest, capture_output=True)
            rc2, steps2, tests2 = suite(dest)
            if rc2 != 0:
                tool(dest, "tests/update_baselines.py")
                subprocess.run(["git", "add", "-A"], cwd=dest, capture_output=True)
                rc3, steps3, tests3 = suite(dest)
                if rc3 != 0:
                    verdict, stage, detail = "CAUGHT", "firm", steps3 + tests3
                else:
                    verdict, stage, detail = "NOT CAUGHT", "after baseline update", steps2 + tests2
            else:
                verdict, stage, detail = "NOT CAUGHT", "after rebuilding compendium", steps + tests
        else:
            verdict = "NOT CAUGHT"
        results.append({"n": n, "what": what, "verdict": verdict, "stage": stage, "detail": detail[:6]})
        print(f"{verdict:10s} {n:2d}. {what} [{stage}] {'; '.join(detail)[:170]}")
    out = ROOT / "tests" / "results" / "review-edits.json" if record else WORK / "results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"date": datetime.date.today().isoformat(), "results": results}, indent=1) + "\n", encoding="utf-8")
    c = sum(r["verdict"] == "CAUGHT" for r in results)
    nc = sum(r["verdict"] == "NOT CAUGHT" for r in results)
    print(f"SUMMARY {c} caught, {nc} not caught, {len(results) - c - nc} edit failed")
    return 1 if nc else 0


if __name__ == "__main__":
    sys.exit(main({int(a) for a in sys.argv[1:] if a.isdigit()}, record="--record" in sys.argv))
