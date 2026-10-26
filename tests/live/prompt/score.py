"""Score a drafted prompt against the playbook's rubric (Law 3, Law 6, §5.3, §7, §9.1, §9.4, Templates B, C, H).

Usage: python3 -I score.py <scenarios.json> <scenario id> <prompt text file> [--lenient]
--lenient counts a "Requirements" list as the criteria and passes p-1 (goal label), so a draft
is not marked down for format alone; the rest of the rubric is unchanged.
Prints one PASS/FAIL line per applicable check and a final "SCORE passed/applicable".
"""
import json
import re
import sys

scenarios = {s["id"]: s for s in json.load(open(sys.argv[1]))}
needs = scenarios[sys.argv[2]]["needs"]
text = open(sys.argv[3], encoding="utf-8").read()
low = text.lower()


def block(name):
    """Text after a heading/label like 'DONE WHEN' up to the next ALL-CAPS label or heading."""
    m = re.search(rf"(?:^|\n)[#*\s]*{name}[^\n]*\n(.*?)(?=\n[#*\s]*[A-Z][A-Z &/-]{{3,}}[:*]*\s*\n|\n#+ |\Z)", text, re.S | re.I)
    return m.group(1) if m else ""


checks = []


def check(name, ok):
    checks.append((name, bool(ok)))


lenient = "--lenient" in sys.argv
done = block(r"done when") or block(r"acceptance criteria") or block(r"success criteria") or (block(r"requirements") if lenient else "")
items = [l for l in done.splitlines() if re.match(r"\s*(?:[-*]|\d+[.)]|\[ \])\s+\S", l)]
check("p-1 Has a one-sentence GOAL", lenient or re.search(r"(?:^|\n)[#*\s]*(goal|objective)\b", text, re.I))
check("p-2 DONE WHEN has 2 to 5 checks", 2 <= len(items) <= 5)
# A bare number is not a check ("done within 2 days"); a counted, observable result is ("exactly 2 rows").
counted = r"\b(exactly|at least|at most|no more than|equals?|equal to|matches)\b[^.\n]{0,25}\d|\b\d+\s*(rows?|files?|tests?|items?|issues?|prs?|errors?|failures?|lines?)\b"
# An observable outcome is checkable ("fails on the unfixed code", "the file says near tie"); "done" or "works" is not.
observable = r"\b(fails?|passes|go(es)? (red|green)|runs?|exits?|returns?|lists?|reports?|says|shows?|prints?|contains?|is empty)\b"
checkable = [i for i in items if re.search(r"`|\bgiven\b|\bnpm\b|\bpytest\b|\bexit (?:code )?\d\b|" + counted + "|" + observable, i, re.I)]
check("p-3 Every check is runnable (command, scenario or counted result)", items and len(checkable) == len(items))
# A clean git status or working tree is an observable state, not a vague adjective.
states = re.sub(r"(git status`?|working tree|work tree)\s+(is|stays|shows|reports)\s+(a\s+)?clean|clean (working|work) tree", "", done, flags=re.I)
check("p-4 No vague adjectives in the checks", items and not re.search(r"works? (well|correctly|properly)|\bfast\b|\brobust\b|\bclean\b(?! install)|\bproperly\b", states, re.I))
check("p-5 Stop-and-ask list", re.search(r"stop and ask|ask (me|the user) (before|if|when)|stop and report", low))
check("p-6 Receipt: PASS, FAIL or NOT RUN with the command", re.search(r"not run", low) and "pass" in low and "fail" in low)
check("p-7 Budget or limit", re.search(r"budget|\$\d|max(imum)? \d|at most \d|\d+ (hours?|minutes?|iterations?|helpers?|attempts?|tries)", low))
check("p-8 Outcome, not micromanaged steps (under 120 lines)", len(text.splitlines()) < 120)
if "tests" in needs:
    check("p-9 Tests first or tests kept green", re.search(r"failing test first|red.{0,20}green|tests? first|characteri[sz]ation tests?|green at the end of|(both|fully|suite is|run is|stays|is) green|green between|failing regression test|turns? (the full run )?red is reverted|write (a|the) (failing |regression )?test|tests? (stay|stays|remain|still) (green|pass)|green (after|on|before) (every|each)|stays? green|keep[^.\n]{0,40}green", low))
    check("p-10 Forbids editing or deleting tests to pass", re.search(r"tests?,? unedited|no (existing )?test[^.\n]{0,60}(was |is )?(changed|edited|modified)", low) or re.search(r"(do not|don't|never|must not|no test may)[^\n]{0,90}(edit|delet|disabl|skip|weaken|modif|loosen|chang)[^\n]{0,90}(tests?|assertions?)", low))
if "helpers" in needs:
    check("p-11 One writer; helpers read-only", re.search(r"read-only|read only|do not edit|one writer|single writer", low))
    check("p-12 Helpers write to a file and return the path", re.search(r"(write|save)[^.\n]{0,80}(\.md|file|path)", low) and re.search(r"path", low))
    check("p-13 Helper output has a length cap", re.search(r"under \d+ words|\d+ words|word limit|\d+ lines", low))
    check("p-14 A synthesis step that reconciles findings", re.search(r"synthes|reconcil|combine|merge (the )?findings|compare (the )?findings", low))
if "writers" in needs:
    check("p-19 Writers get disjoint sets of files", re.search(r"disjoint|no file in two|one writer per (set|batch)|own (batch|worktree)", low))
    check("p-20 Every batch passes its own gate", re.search(r"(each|every) batch[^.\n]{0,80}(gate|pass|test)|per-batch gate|batch gate|(each|every|a) writer[^.\n]{0,80}runs? (only )?(its|those|their) (own )?(files|tests|batch)", low))
    check("p-21 The lead integrates one batch at a time", re.search(r"(merge|merges|integrat)[^.\n]{0,40}one at a time|one batch at a time|after each merged batch|merge it, and check", low))
if "loop" in needs:
    check("p-15 Loop: stop condition", re.search(r"stop (when|after|if)|stop condition|runs out, stop|, stop\b|stop merging", low))
    check("p-16 Loop: 'no change' when nothing changed", "no change" in low)
    check("p-17 Loop: failure cap", re.search(r"(2|two) failures|fails? twice|(2|two) \w+ fail with the same cause|same cause|same reason|retry at most|after \d+ failures|at most (one|1|2|two) retr", low))
    # Any "never" or "do not" passed before; the ban must name an irreversible action.
    irreversible = r"(merge|push|delete|deploy|force|revert|close|publish|pay|drop|rewrite|rebase|approve)"
    check("p-18 Loop: never does irreversible things without asking",
          re.search(r"(never|do not|don't|must not)\b[^.\n]{0,60}\b" + irreversible, low)
          or re.search(r"ask (me|a human|a person)[^.\n]{0,15}(first|before)[^.\n]{0,40}" + irreversible, low))

passed = sum(ok for _, ok in checks)
for name, ok in checks:
    print(f"{'PASS' if ok else 'FAIL'} {name}")
print(f"SCORE {passed}/{len(checks)}")
