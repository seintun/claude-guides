# Review r1 of prompt-r0.md

Read only: the draft, the decision log, the skill's steps and rules.

## Per-part verdicts

- GOAL: PASS. "A new client is live within one day of their signed data agreement arriving, with the contract process unchanged and no client live without a recorded signed agreement" is one sentence of outcome. Its partial-credit clause conflicts with step 9 (see blocker 2).
- DONE WHEN: FAIL. There are 5 checks, each a command or a Given/When/Then. Checks 1 and 2 say "This check FAILs while that ... UNKNOWN is open", which the skill allows (c-8). Check 2 measures from the wrong start (blocker 3). Check 3 can be skipped away (blocker 2). Check 3's break file is chosen by the agent: "(the plan names that file before the build starts)". The skill wants the file named, but the location is UNKNOWN, so I do not count it as a blocker.
- CONTEXT: PASS. "Riskiest assumption: most of the wait after signing is manual or waiting work that software can remove. Cheapest test: the timing walk in step 3". The decision log is given as a path, and the problem and its cost are stated, with the cost listed as UNKNOWN.
- CONSTRAINTS: PASS. "Do not change the contract process: no change to its files, data or behaviour." The portal exclusion and the four failure-case requirements ("Ordering", "Repeats", "Partial failure", "Rollback") trace to the decision log and the request. No line conflicts with the GOAL.
- BUDGET: PASS. "Helpers: the 3 helper runs listed at the top. No helper writes code." This covers 1 timing helper plus 2 reviews. "Sources: the 3 completed onboardings" matches the cap in check 1.
- STOP AND ASK IF: PASS. Each line was tested against the decision log. None holds on its face (see Q2). It covers the risky and hard-to-undo cases. Its retry line conflicts with step 8 (blocker 1).
- HOW TO WORK: FAIL. Step 8 conflicts with the retry cap (blocker 1). Step 5 and step 8 leave the gate unbuilt (blocker 2). The synthesis is its own step 4, the review is bounded ("After 2 rounds, that person decides."), and step 10 is a receipt.
- REPORT: PASS. "Each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS." It also has "(zero is a FAIL)".

## The three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? Yes, three ways.
   - Check 4: "lists no file that the plan's contract-process list names." The check has no minimum for the list, unlike check 1's "at least one". It passes if the list is empty or incomplete, and it checks files only while the constraint says "files, data or behaviour". The REPORT's "(zero is a FAIL)" is the only guard.
   - Check 5: "-- <test paths named in the plan>" prints nothing if the plan names no paths. "a test count at least as high as the count the plan recorded" passes at a recorded count of 0. `--diff-filter=MD` also misses a renamed test.
   - Check 3, via the skip path: step 9 says "SKIPPED and cut slices are listed, not required." If the gate slice is cut, the GOAL's gate clause is unmet while the run can still close.
2. Does any STOP AND ASK condition already hold? No.
   - The decision log says "the project root holds no files (no README, CLAUDE.md, docs/, code, config or earlier notes)". The line "The onboarding code is not under version control, no test command can be found, or no place exists to run a test client" cannot be tested yet, because the location is UNKNOWN ("where today's onboarding lives").
   - The Start gate covers it: "If any of the four blocking UNKNOWN lines is still open, stop and report which; do nothing else."
   - "The plan's smallest slice does not fit the time ceiling" depends on two UNKNOWNs (hours and end date). The same Start gate covers it.
   - Nothing else in the draft or the log makes a stop line true today.
3. Is every file, record and system the steps need located, or listed as UNKNOWN? No.
   - Located or UNKNOWN: the onboarding code, data and records ("UNKNOWN: where today's onboarding lives"), the "live" event, the hours, the end date, and whether signing is inside the two weeks.
   - Neither: the contract process. Check 4 and step 5 need its files ("the list of files that belong to the contract process"), but step 2 only says "Locate the onboarding code, data and records, and the project's own test command".
   - Neither: the signed-data-agreement record. Checks 2 and 3 and the "Ordering" constraint depend on it. The log says only "with its own record that onboarding checks before a client goes live". The draft does not say where it lives, whether it exists today, or who records it.

## Blockers

1. The retry cap and step 8 cannot both be followed.
   - Evidence: "ASSUMED: a failure with the same cause twice stops the work (the retry cap)." and "The same failure with the same cause happens twice, or two slices in a row are reverted." against step 8: "A slice whose suite stays red after the retry cap is reverted and listed under SKIPPED with the reason."
   - Why it blocks: the cap stops the work at the second same-cause failure. Step 8 reverts that slice and carries on to the next. If the cap stops the work, the "two slices in a row are reverted" line can never be reached. If step 8 wins, the cap is not a stop. The agent has to pick one with no rule to follow.

2. The go-live gate can be cut or left unbuilt, though check 3 and the GOAL require it.
   - Evidence: step 5 orders slices "in order of the days each removes (from the timing file)" and lists "the go-live gate and the file and call its deliberate break deletes" apart from the slices. Step 5 also lists "the slices cut to fit the time ceiling". Step 8 builds only "One slice at a time". Step 9 says "Checks read the slices that stayed merged; SKIPPED and cut slices are listed, not required." The GOAL says "no client live without a recorded signed agreement".
   - Why it blocks: the gate removes no days, so it sorts last and is first to be cut. No step builds it, and the log does not say a signed-agreement check exists today (decision 2 only says onboarding "checks" the record). If the gate is cut, check 3 has nothing to test. The run can still end as "met in part" with go-live possible without a signed agreement, which is the request's failure case.

3. The one-day clock in check 2 starts at the wrong event, and the signed-agreement record is not located.
   - Evidence: the GOAL says "within one day of their signed data agreement arriving". Decision 1 says the clock starts "when the client's signed data agreement arrives". Check 2 says "whose signed data agreement is recorded at time T0 ... is recorded no later than T0 plus one day".
   - Why it blocks: T0 is when the agreement is recorded, not when it arrives. If recording is a manual or delayed step, the arrival-to-record gap is never measured. Check 2 can PASS while a client waits days after the agreement arrives, so the goal is unmet. The draft never says where the record lives, whether it exists, or whether arrival and recording are the same event. That is an unlocated record the check rests on (Q3).
