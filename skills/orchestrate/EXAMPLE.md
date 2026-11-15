# /orchestrate, worked example: one codebase, four requests

The same Node service gets four requests in one week. Each needs a different shape of work, and the shape decides the token bill more than the model does. Run each step yourself with the commands shown; the outputs below are real.

## The idea in one line

Most of the cost of agent work comes from contexts: every helper, builder or session is a fresh context that must load its own brief and read its own files. Pick the fewest contexts that still give a quality result, then spend the rest on speed.

## Request 1: "Fix the flaky date test"

Answer the six questions: A yes (one test, one writer), C no (a test run sums up in one line). Nothing else applies.

```bash
python3 -I skills/orchestrate/route.py --explain '{"fits_one_context":true,"items":1}'
```

```text
Route 1. Inline. Why: rule 5: A yes and C no
Runner-up: 2. Inline plus helper subagents
```

Lesson: a subagent here would cost a second context and gain nothing, because the main agent needs every detail of the failure anyway.

## Request 2: "Migrate all 40 handlers to the new error type"

B is yes: 40 handlers touch different files, none imports another, and each has its own test.

```bash
python3 -I skills/orchestrate/route.py --explain '{"independent":true,"items":40}'
```

```text
Route 3. Parallel builders in worktrees. Why: rule 3: B yes: independent parts that each write
Runner-up: 4. One session per task
Requires: 2 /batch run(s) of at most 30 parts
```

Lesson: parallel writers are safe only because no two of them share a file. Each worktree is its own checkout, so they cannot overwrite each other. `/batch` takes 5 to 30 parts, so 40 means two runs.

## Request 3: "Work the 12 tickets in this cycle; some block others"

E is yes (days of work, many PRs) and the tickets have an order.

```bash
python3 -I skills/orchestrate/route.py --explain '{"outlives_session":true,"ordered":true,"items":12}'
```

```text
Route 5. Hub plus builder sessions. Why: rule 1: E yes and the items have an order
Runner-up: 4. One session per task
Requires: at most 3 builders at once
```

Lesson: the hub never writes code; it holds a ledger and starts builders only for tickets whose blockers are done. The cap of 3 is about you, not the agents: someone has to review every PR.

## Request 4: "Add TOTP multi-factor authentication to login"

A is yes, but F is yes (auth), and F makes D yes: a high-risk change needs a judgment from someone who did not write it. route.py applies that rule itself, so `"needs_judgment"` below is only for clarity.

```bash
python3 -I skills/orchestrate/route.py --explain '{"fits_one_context":true,"needs_judgment":true,"high_risk":true,"items":1}'
```

```text
Route 2. Inline plus helper subagents. Why: rule 4: C or D yes, or too big for one context; one writer keeps the edits
Runner-up: 1. Inline
Requires: fresh critic on the plan
Requires: adversarial review of the diff
Requires: human sign-off
```

Lesson: high risk does not mean more builders. It means one writer plus independent readers on a higher model rung, and a human at the end.

## What the skill shows you before anything starts

For request 2, the card opens with its working. Answers is every question from step 2 in one line, and Reasoning says the same thing in plain words:

```text
Route: 3. Parallel builders in worktrees. Why: B yes, 40 handlers that each write and have their own test
Answers: A no; B yes; C no; D no; E no; F no; order no; read-only no; gate no; comparison no; items 40
Reasoning: Rule 1: skipped, E no. Rule 2: skipped, the handlers are written. Rule 3: fired, B yes: 40 handlers touch different files, none imports another, and each has its own test. Cheaper routes: route 1 or 2 would leave one writer making 40 edits in sequence. Would change if: each handler needed its own reviewed PR over several days (route 4).
Runner-up: 4. One session per task. It would win if: each handler needed review as its own PR
```

You decide from Reasoning. If you disagree with one answer ("C is yes, the test output is huge"), say so, and the route follows from the corrected answers. The code makes that hold: `check_card.py` feeds the Answers line to `route.py` and fails the card (check k-12) if its route or runner-up does not follow, and fails it (k-13) if Reasoning names the wrong rule as fired, leaves out "Cheaper routes:" or "Would change if:", or runs past 150 words.

## After you say go

You do not write any prompts. The skill writes every brief the route needs (helper briefs for route 2, builder briefs for routes 3 and 4, the hub prompt for route 5, the script for route 6) and shows them as it sends them, so you can stop it there.

When the work finishes, it writes one outcome line to `docs/decisions.md`:

```text
- 2026-11-14 /orchestrate outcome: migrate handlers | route 3 (Parallel builders in worktrees) | budget 90 minutes | spent 75 minutes | checks PASS 3, FAIL 0, NOT RUN 0 | route again: yes, because no handler shared a file
```

`python3 -I skills/orchestrate/check_card.py --outcome docs/decisions.md` checks every such line. A "route again: no" names a task the rules got wrong; add it to `tests/live/orchestrate/scenarios.json` as a new case.

## Checking a card with code

The skill ends every route with a routing card. `check_card.py` decides with code whether the card is usable, so "looks fine" never counts as a pass:

```bash
python3 -I skills/orchestrate/check_card.py tests/fixtures/orchestrate/good-high-risk.txt --expect 2 --risk high
python3 -I skills/orchestrate/check_card.py tests/fixtures/orchestrate/bad-shared-scope.txt
```

The first prints PASS on every line. The second prints `FAIL k-6 writers overlap`, because two builders were given the same files.

## What to try next

Change one fact and watch the route move. Set `"ordered": false` in request 3 and it drops to route 4, because nothing has to wait. Set `"items": 3` in request 2 and route 3 asks for 3 plain worktree subagents instead, because `/batch` needs at least 5 parts; the runner-up drops to route 2. Each rule is one branch in `route.py`, and `tests/test_orchestrate_skill.py` fails if SKILL.md and the code ever disagree.
