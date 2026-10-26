"""Check that ENTRY.md stays a working router.

PASS lines when ENTRY.md is under 150 lines, the scenario router has at least 15 rows,
every row names sections, a template and an output, and every section id in ENTRY.md
resolves through tools/section.py. Exit code 1 on any FAIL.

Usage: python3 -I tools/check_entry.py [path/to/ENTRY.md]
With no argument it checks the repository's ENTRY.md. tests/test_harness.py passes a damaged copy
to prove this checker still fails when it should.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import section  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
entry_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "ENTRY.md"
entry = entry_path.read_text(encoding="utf-8")
lines = entry.splitlines()
fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


report(len(lines) < 150, "ENTRY.md is under 150 lines", f"{len(lines)} lines")

if "## Scenario router" not in entry:
    report(False, "ENTRY.md has a Scenario router section")
    sys.exit(1)
router = entry.split("## Scenario router", 1)[1].split("\n## ", 1)[0]
rows = [r for r in router.splitlines() if re.match(r"\| \d+ \|", r)]
report(len(rows) >= 15, "Scenario router has at least 15 rows", f"{len(rows)} rows")
bad = []
for r in rows:
    cells = [c.strip() for c in r.strip("|").split("|")]
    # number, scenario, read, runbook, template, output
    if len(cells) != 6 or not all(cells[i] for i in (1, 2, 4, 5)) or "`" not in cells[2]:
        bad.append(cells[0])
report(not bad, "Every row names sections, a template and an output", ", ".join(bad))

_, pb = section.index(section.PLAYBOOK)
_, cs = section.index(section.CHEATSHEET, cheatsheet=True)
known = set(pb) | set(cs)
ids = set()
for span in re.findall(r"`([^`]+)`", entry):
    for tok in span.split():
        if re.fullmatch(r"(cs:\d+|law-\d+|\d+[A-Z]?(\.\d+)?|[A-M])", tok):
            ids.add(tok)
unknown = sorted(i for i in ids if (i if i.startswith(("cs:", "law-")) else i.upper()) not in known)
report(not unknown, "Every section id resolves through tools/section.py", f"{len(ids)} ids" + (f"; unknown: {', '.join(unknown)}" if unknown else ""))

sys.exit(1 if fails else 0)
