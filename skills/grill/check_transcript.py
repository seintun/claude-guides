"""Check one grill session's transcript (claude -p --output-format stream-json) against the grill rules.

Usage: python3 -I skills/grill/check_transcript.py <transcript.jsonl>
Prints one PASS or FAIL line per rule and exits 1 on any FAIL.
"""
import json
import re
import sys

events = []
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        events.append(json.loads(line))
    except ValueError:
        pass

calls = [c for e in events if e.get("type") == "assistant"
         for c in e.get("message", {}).get("content", []) if c.get("type") == "tool_use"]
result = next((e for e in events if e.get("type") == "result"), {})
text = result.get("result", "") or ""
asked = [c for c in calls if c["name"] == "AskUserQuestion"]
if asked:  # the question went through the tool; check its payload instead of the text
    qs = [q for c in asked for q in c["input"].get("questions", [])]   # every question in every call
    labels = [o.get("label", "") for o in qs[0].get("options", [])] if qs else []
    question_count = len(qs)
else:
    # Option lines: A) / A. / A: / (A) / **A.** / - **A)** / Option A: / 1. ... with the label after it.
    option = re.compile(r"^\s*(?:[-*]\s+)?\**\(?(?:Option\s+)?([A-H1-9])(?:\)|\.|:)\**\s*[-–—:]?\s*(.+)$", re.M)
    labels = [m.group(2) for m in option.finditer(text)]
    question_count = len(re.findall(r"\?\s*$", text, re.M)) or (1 if "?" in text else 0)

fails = 0


def report(ok, rule, detail=""):
    global fails
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {rule}{' — ' + detail if detail else ''}")


looked = [c for c in calls if c["name"] in ("Read", "Grep", "Glob") or (c["name"] == "Bash" and re.search(r"\b(cat|ls|grep|rg|find)\b", c["input"].get("command", "")))]
report(bool(looked), "grill-1 Looked at the project before asking", f"{len(looked)} lookups")
report("postgres" in text.lower(), "grill-2 Reported a fact it found instead of asking it", "mentions PostgreSQL" if "postgres" in text.lower() else "no mention of PostgreSQL from the README")
report(not re.search(r"which (database|db)|what database|test command|how do you run (the )?tests", text, re.I),
       "grill-3 Asked no question the README answers")
report(question_count == 1, "grill-4 One question in the message", f"{question_count} question(s)")
report(2 <= len(labels) <= 4, "grill-5 Offered 2 to 4 options", f"{len(labels)} options")
report(bool(labels) and "(Recommended)" in labels[0] and sum("(Recommended)" in l for l in labels) == 1,
       "grill-6 Recommended option first, and only one", labels[0][:80] if labels else "no options")
writes = [c for c in calls if c["name"] in ("Write", "Edit", "NotebookEdit")]
report(not writes, "grill-7 Wrote no plan, spec or code", f"{len(writes)} writes")
report(not result.get("is_error"), "grill-8 Session ended without an error")
if fails:
    print("--- first message ---")
    print(text[:3000])
sys.exit(1 if fails else 0)
