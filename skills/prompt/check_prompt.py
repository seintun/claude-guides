"""Check a prompt written by /prompt for the mistakes prose rules miss on long prompts.

Usage: python3 -I skills/prompt/check_prompt.py <prompt.md> [--source <decision-log or request file>]...
Prints one PASS, FAIL or WARN line per check and exits 1 on any FAIL. WARN lines need a person's eye:
fix each one, or mark the figure ASSUMED.

The checks come from the grill-then-prompt dry runs (tests/live/grill-prompt/results.md):
  c-1  every part the risk level needs is there: trivial may leave out CONTEXT; normal and high need all eight
  c-2  DONE WHEN has 2 to 5 checks
  c-3  one gap per UNKNOWN line: no line joins two gaps with ", and whether", ", and what" and the like
  c-4  more than 3 UNKNOWN lines means the prompt says it is not ready to run
  c-5  no relative term ("next Friday", "this quarter", "today's", "recent") outside a quote or a marked line
  c-6  (WARN) every figure traces to a --source file, a marked line or a value the skill sets
  c-7  (WARN) each chosen figure is marked ASSUMED once, not on every line that uses it
  c-8  (WARN) no DONE WHEN check rests on an UNKNOWN: it names one, or a term an UNKNOWN line quotes
  c-9  a line before GOAL says Risk: trivial, normal or high (/prompt step 3)
A check that passes over zero items is left to the fresh review: wording alone can't tell "every client" from "breaks A, B and C".
"""
import re
import sys

PARTS = ["GOAL", "DONE WHEN", "CONTEXT", "CONSTRAINTS", "BUDGET", "STOP AND ASK IF", "HOW TO WORK", "REPORT"]
# Values /prompt itself prescribes, so they trace to the skill rather than to the user.
SKILL_VALUES = re.compile(r"\b(?:(?:about )?40 words per field|two rounds|2 rounds|(?:up to )?3 blockers|2 to 5 checks|5 questions|"
                          r"(?:at most )?2 failures|(?:more than )?3 UNKNOWN(?: lines)?|(?:at most )?15 lines)\b", re.I)
RELATIVE = re.compile(
    r"\b(?:today'?s?|tonight|tomorrow|yesterday|(?<!as )soon(?! as)|asap|recent(?:ly)?|"
    r"(?:this|next|last) (?:week|month|quarter|year|sprint|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"end of (?:the )?(?:day|week|month|quarter|year)|after launch|the owner)\b", re.I)
NUMBER_WORDS = r"two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|fifty|hundred"
# A figure with the word after it ("two records"), so "two weeks" in the request does not vouch for "two records".
FIGURE = re.compile(rf"\b(?:\d+(?:[.,]\d+)?%?|{NUMBER_WORDS})\b(?:\s+([a-z][\w-]*))?", re.I)
POINTER = r"(?:steps?|checks?|items?|rounds?|stops?|lines?|sections?|parts?|slices?|rules?|questions?|conditions?|briefs?|options?|decisions?|exits?|codes?|D|Q|P-Q)"
REFERENCE = re.compile(rf"\b{POINTER}\s*$|\b{POINTER}\s+\d+(?:\s*,\s*\d+)*\s+(?:and|or|to)\s*$", re.I)
MARKED = re.compile(r"\b(?:ASSUMED|UNKNOWN):")
GAP_LINE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)?`?UNKNOWN:\s*(.*)$")
# A part's heading or label: "## GOAL", "GOAL:", "**GOAL:**" or "GOAL: one sentence ...".
PART_LINE = re.compile(r"^(?:#+\s*)?(?:\*\*)?(" + "|".join(PARTS) + r")(?:\*\*)?(?::|\s*$)")
# Template B's trivial form: every part but CONTEXT, with HOW TO WORK as "build, verify, report".
TRIVIAL_PARTS = [p for p in PARTS if p != "CONTEXT"]
RISK = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?risk:?(?:\*\*)?:?\s*(trivial|normal|high)\b", re.I)
JOINED = re.compile(r",?\s+and (?:whether|what|where|who|how|when|which)\b", re.I)


def plain(line):
    """The line without inline code, quoted words or ISO dates: what a reader takes as the writer's own claim."""
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"\"[^\"]*\"|“[^”]*”", " ", line)
    return re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", line)


args = sys.argv[1:]
if not args or args[0].startswith("-"):
    sys.exit(__doc__)
path, sources = args[0], []
for i, a in enumerate(args):
    if a == "--source" and i + 1 < len(args):
        sources.append(open(args[i + 1], encoding="utf-8").read())
text = open(path, encoding="utf-8").read()
source_text = "\n".join(sources).lower()

lines, in_fence = [], False  # (line number, text) outside fenced code blocks
for n, line in enumerate(text.splitlines(), 1):
    if line.lstrip().startswith("```"):
        in_fence = not in_fence
        continue
    if not in_fence:
        lines.append((n, line))

fails = 0


def report(level, check, detail=""):
    global fails
    fails += level == "FAIL"
    print(f"{level} {check}{' — ' + detail if detail else ''}")


def part_of(line):
    m = PART_LINE.match(line.strip())
    return m.group(1) if m else None


heads = {p for _, l in lines if (p := part_of(l))}
goal_at = next((i for i, (_, l) in enumerate(lines) if part_of(l) == "GOAL"), len(lines))
risk = next((m.group(1).lower() for _, l in lines[:goal_at] if (m := RISK.match(l))), None)
needed = TRIVIAL_PARTS if risk == "trivial" else PARTS
missing = [p for p in needed if p not in heads]
report("FAIL" if missing else "PASS", "c-1 Every part the risk level needs is there",
       "missing: " + ", ".join(missing) if missing else f"risk {risk or 'unstated'}")

numbered, bulleted, last, inside = [], [], None, False  # each DONE WHEN check with its continuation lines
for _, l in lines:
    part = part_of(l)
    if part or l.startswith("#"):
        inside, last = part == "DONE WHEN", None
    elif not inside or not l.strip():
        continue
    elif re.match(r"^\d+\.\s", l):
        numbered.append(l)
        last = numbered
    elif re.match(r"^[-*]\s", l) and not numbered:  # a bulleted list of checks; bullets under a numbered check belong to it
        bulleted.append(l)
        last = bulleted
    elif last:
        last[-1] += " " + l.strip()
done = numbered or bulleted
report("PASS" if 2 <= len(done) <= 5 else "FAIL", "c-2 DONE WHEN has 2 to 5 checks", f"{len(done)} checks")

gaps = [(n, m.group(1)) for n, l in lines if (m := GAP_LINE.match(l))]
joined = [n for n, g in gaps if JOINED.search(g.split(";")[0])]
report("FAIL" if joined else "PASS", "c-3 One gap per UNKNOWN line",
       "lines " + ", ".join(map(str, joined)) + " join two gaps; split them" if joined else f"{len(gaps)} UNKNOWN lines")

not_ready = re.search(r"not ready", text, re.I)
report("FAIL" if len(gaps) > 3 and not not_ready else "PASS", "c-4 More than 3 UNKNOWN lines says not ready",
       f"{len(gaps)} UNKNOWN lines" + ("" if len(gaps) <= 3 or not_ready else " and no 'not ready'"))

relative = [(n, m.group(0)) for n, l in lines if not MARKED.search(l) for m in RELATIVE.finditer(plain(l))]
report("FAIL" if relative else "PASS", "c-5 No unresolved relative term",
       "; ".join(f"line {n}: {t!r}" for n, t in relative[:8]) if relative else "")

def figures(line):
    """The quantities a line states, as lower-case phrases: skill values and pointers such as "step 1" left out."""
    body = SKILL_VALUES.sub(" ", plain(re.sub(r"^\s*(?:[-*]\s+|\d+\.\s+)", "", line)))
    return [re.sub(r"\s+", " ", m.group(0)).lower() for m in FIGURE.finditer(body) if not REFERENCE.search(body[:m.start()])]


traced = re.sub(r"\s+", " ", source_text)
assumed = {}  # figure -> the ASSUMED lines that state it
for n, l in lines:
    if MARKED.search(l):
        for f in set(figures(l)):
            assumed.setdefault(f, []).append(n)
loose = [(n, f) for n, l in lines if not MARKED.search(l) and not re.match(r"^\s*#", l)
         for f in figures(l) if f not in traced and f not in assumed]
report("WARN" if loose else "PASS", "c-6 Every figure traces to a source, a marked line or the skill",
       "; ".join(f"line {n}: {t!r}" for n, t in loose[:12]) + (f" (+{len(loose) - 12} more)" if len(loose) > 12 else "") if loose else "")

twice = {f: ns for f, ns in assumed.items() if len(ns) > 1 and " " in f}
report("WARN" if twice else "PASS", "c-7 Each chosen figure is marked once",
       "; ".join(f"{f!r} on lines {', '.join(map(str, ns))}" for f, ns in list(twice.items())[:8]) if twice else "")

gap_terms = {(a or b).lower() for _, g in gaps for a, b in re.findall(r"\"([^\"]+)\"|“([^”]+)”", g)}
resting = [i for i, c in enumerate(done, 1) if "UNKNOWN" in c or any(f'"{t}"' in c.lower() or f"“{t}”" in c.lower() for t in gap_terms)]
report("WARN" if resting else "PASS", "c-8 No check rests on an UNKNOWN",
       "checks " + ", ".join(map(str, resting)) + ": settle the gap first, or make the check fail while it is open" if resting else "")

report("PASS" if risk else "FAIL", "c-9 A risk line comes before GOAL",
       f"Risk: {risk}" if risk else "add 'Risk: trivial', 'Risk: normal' or 'Risk: high' above the title")

sys.exit(1 if fails else 0)
