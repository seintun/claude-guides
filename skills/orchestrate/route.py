"""Reference router for /orchestrate: the routing rules in SKILL.md, written as code.

Give it the facts about a task; it returns the route, the runner-up and what the route requires.
Tests run it against every labelled case in tests/live/orchestrate/scenarios.json, and they read the
thresholds, rule order and runner-ups below out of SKILL.md, so prose and code cannot drift apart unnoticed.

Usage: python3 -I skills/orchestrate/route.py '<json facts>'
       python3 -I skills/orchestrate/route.py --explain '<json facts>'
Facts. A missing key takes the default in brackets, so an empty {} is a small, simple task:
  fits_one_context  A: one context and one writer can hold it [true]
  independent       B: the parts touch different files, have no order, and are each a task of their own [false]
  bulky_output      C: there is bulky output you only need the conclusion of [false]
  needs_judgment    D: it needs a judgment from someone who did not do the work [false]
  outlives_session  E: it spans many tickets or sessions, or must outlive this conversation [false]
  high_risk         F: schema, auth, data deletion, infrastructure, a public API or permissions [false]; makes D true
  ordered           the items have an order between them (blocked-by links) [false]
  read_only         nothing is written; the job is reading or analysis [false]
  gate_mid_run      a person must approve something partway through [false]
  comparison        the job compares options [false]
  items             how many files, tickets or items [1]
"""
import json
import math
import sys

WORKFLOW_MIN_ITEMS = 20   # "dozens of items (20 or more)"
BATCH_MIN, BATCH_MAX = 5, 30  # /batch splits one change into 5 to 30 worktree subagents
MAX_BUILDERS = 3          # builders a hub runs at once
NAMES = {
    1: "Inline",
    2: "Inline plus helper subagents",
    3: "Parallel builders in worktrees",
    4: "One session per task",
    5: "Hub plus builder sessions",
    6: "Workflow script",
}
# The nearest alternative for each route; SKILL.md states the same list.
RUNNER_UP = {1: 2, 2: 1, 3: 4, 4: 3, 5: 4, 6: 2}
DEFAULTS = {"fits_one_context": True, "items": 1}


def route(facts):
    """Return a dict: route, name, runner_up, why, requires (a list of strings)."""
    f = dict(DEFAULTS, **facts)
    get = lambda k: bool(f.get(k, False))
    items = int(f.get("items") or 1)
    judgment = get("needs_judgment") or get("high_risk")
    requires = []
    if get("high_risk"):
        requires += ["fresh critic on the plan", "adversarial review of the diff", "human sign-off"]

    if get("outlives_session") and items > 1:
        if get("ordered"):
            r, why = 5, "E yes and the items have an order"
            requires.append(f"at most {MAX_BUILDERS} builders at once")
        else:
            r, why = 4, "E yes and the items have no order"
    elif get("read_only") and items >= WORKFLOW_MIN_ITEMS and get("bulky_output") and not get("gate_mid_run"):
        r, why = 6, f"read-only fan-out over {items} items that each need reading, no gate mid-run"
    elif get("independent") and items > 1 and not get("read_only"):
        r, why = 3, "B yes: independent parts that each write"
        if items >= BATCH_MIN:
            requires.append(f"{math.ceil(items / BATCH_MAX)} /batch run(s) of at most {BATCH_MAX} parts")
        else:
            requires.append(f"{items} worktree subagents (below the {BATCH_MIN} parts /batch needs)")
    elif get("bulky_output") or judgment or not get("fits_one_context"):
        r, why = 2, "C or D yes, or too big for one context; one writer keeps the edits"
        if get("comparison"):
            requires.append("2 to 4 read-only helpers")
    else:
        r, why = 1, "A yes and C no"
    ru = RUNNER_UP[r]
    if r == 3 and items < BATCH_MIN:
        ru = 2
    return {"route": r, "name": NAMES[r], "runner_up": ru, "why": why, "requires": requires}


def main(argv):
    explain = "--explain" in argv
    args = [a for a in argv if a != "--explain"]
    if len(args) != 1:
        print(__doc__)
        return 2
    out = route(json.loads(args[0]))
    if explain:
        print(f"Route {out['route']}. {out['name']}. Why: {out['why']}")
        print(f"Runner-up: {out['runner_up']}. {NAMES[out['runner_up']]}")
        for r in out["requires"]:
            print(f"Requires: {r}")
    else:
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
