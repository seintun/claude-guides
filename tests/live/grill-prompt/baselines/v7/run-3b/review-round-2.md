# Review r2 of prompt-r1.md

Read only: the revised draft, the decision log, the skill's steps and rules, and review-r1.md.

## First-review blockers

1. Retry cap against step 8: CLOSED.
   - The cap now says "ASSUMED: a slice gets at most 2 failed attempts with the same cause; after that it is reverted (the retry cap)." It no longer stops the work.
   - Step 8 matches it: "A slice whose suite is still red after the retry cap is reverted and listed under SKIPPED with the reason, and the next slice starts; if its cause matches an earlier reverted slice, stop and ask."
   - The stop line matches step 8: "A failure repeats across slices: a slice is reverted for a cause that already reverted an earlier slice."
   - The "two slices in a row" line is gone, so the three lines now agree.

2. Go-live gate can be cut or left unbuilt: CLOSED.
   - GOAL: "if the budget ends first, the go-live gate is still in place and the report says how far the merged slices get toward one day."
   - Step 5: "the slices, first the go-live gate, which is never cut, then the others in order of the days each removes".
   - Step 8: "in plan order (the gate first)".
   - Step 9: "SKIPPED and cut slices are listed, not required, except the gate slice, which is never cut or skipped."
   - Stop line: "The go-live gate slice is reverted, cannot be built, or does not fit the time ceiling. The gate is never cut or skipped."
   - The gate is first in the plan, built first, exempt from the skip rule, and a stop if it fails.

3. Clock starts at the wrong event, and the agreement record is not located: CLOSED.
   - Check 2: "T0 is the arrival of the agreement, not its recording, so any lag between the two counts inside the day."
   - Check 1 now measures the lag: "gives, for each onboarding, when the signed agreement arrived and when it was recorded".
   - The record is now a listed gap: "UNKNOWN: where the signed data agreement is recorded, if it is recorded at all."
   - The top line makes it blocking: "where the signed data agreement is recorded".
   - Checks 2 and 3 each read "This check FAILs while the UNKNOWN about where the signed data agreement is recorded is open."

## The three questions on the revised draft

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? No check passes on a path that skips the GOAL.
   - Check 1: "covers at least one and at most 3 completed onboardings ... it FAILs if the file gives no answer on whether signing is inside the two weeks."
   - Check 2 is a single named test client, and it fails while two UNKNOWNs are open.
   - Check 3 has two cases and a named break: "the refusal test must FAIL with the call deleted and PASS once it is restored". It fails while the record UNKNOWN is open.
   - Check 4 passes vacuously only if the plan's contract-process list is empty. The REPORT guards this: "the number of cases each check ran (zero is a FAIL)". The check also "FAILs while that UNKNOWN is open".
   - Check 5 has the same REPORT guard.
   - The one fallback path is a budget stop. The GOAL says what that path delivers: "the go-live gate is still in place and the report says how far the merged slices get toward one day". Step 9 never lets the gate slice be skipped.

2. Does any STOP AND ASK condition already hold, given the draft and the log? No.
   - The log says "the project root holds no files", and the draft's own location line is open: "UNKNOWN: where today's onboarding lives".
   - So "The onboarding code is not under version control, no test command can be found, or no place exists to run a test client" cannot be tested yet. Step 1 stops first: "If any blocking UNKNOWN line named at the top is still open, stop and report which; do nothing else."
   - "The timing walk shows that most of the time after signing is spent waiting on people" and "The timing walk cannot find ... when the signed agreement arrived" both need the walk to have run.
   - The two production-data lines read "A step would read or change production data (other than reading for the timing walk)" and "A slice would change the contract process". Nothing in the draft or the log makes either true today.

3. Is every file, record and system the steps need located, or listed as UNKNOWN? Yes.
   - Onboarding code, data and records: "UNKNOWN: where today's onboarding lives, meaning the repository, tools, data stores and records this work reads or changes."
   - Signed-agreement record: listed (see blocker 3).
   - Contract-process files: "UNKNOWN: which files, data and records make up the contract process." Check 4 and step 5 read the answer.
   - The "live" event, hours and quarter end are each an UNKNOWN line.
   - Test command: step 2 says "the project's own test command (README, CLAUDE.md or CI config)", and the stop line covers a missing one.
   - The decision log is a path in the project: `docs/discovery/customer-onboarding-rebuild.md`.
   - Working files are named under `<scratch>`.

## Considered and not counted

- Step 4 has the lead open real records: "Open the cited records yourself for every claim the plan will rest on". The constraint reads "Read real records only for the timing walk". I take step 4 as part of the timing walk, because check 1 needs "the quoted timestamp beside each step". It does not stop the run.
- Check 4 covers files only, while the constraint says "files, data or behaviour". The stop line "A slice would change the contract process" covers the rest.

## Open or new blockers

none

Open or new blocker count: 0
