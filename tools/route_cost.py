"""Estimate the tokens an outside session loads for one route through the guide.

A route is: the /guide skill body, ENTRY.md, the sections one router row names, and
optionally its runbook. Tokens are estimated as characters / 4, the usual rule of thumb
for English text; the exact count depends on the model's tokenizer.

Usage: python3 -I tools/route_cost.py <section ids> [--runbook wiki/<name>.md]
Example: python3 -I tools/route_cost.py 9.5 10.2 F G --runbook wiki/verify.md
"""
import contextlib
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import section  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def tokens(text):
    return round(len(text) / 4)


args = sys.argv[1:]
runbook = None
if "--runbook" in args:
    i = args.index("--runbook")
    runbook = args[i + 1]
    args = args[:i] + args[i + 2:]
if not args:
    print(__doc__.strip())
    sys.exit(1)

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    status = section.main(args)
if status:
    sys.exit(status)

parts = [
    ("skills/guide/SKILL.md", tokens((ROOT / "skills/guide/SKILL.md").read_text(encoding="utf-8"))),
    ("ENTRY.md", tokens((ROOT / "ENTRY.md").read_text(encoding="utf-8"))),
    (f"sections {' '.join(args)}", tokens(buf.getvalue())),
]
if runbook:
    parts.append((runbook, tokens((ROOT / runbook).read_text(encoding="utf-8"))))
whole = tokens((ROOT / "playbook/agent-harness-playbook.md").read_text(encoding="utf-8"))
total = sum(n for _, n in parts)
for name, n in parts:
    print(f"{n:7,}  {name}")
print(f"{total:7,}  total for this route (whole playbook: {whole:,}, so {100 * total / whole:.0f}% of it)")
