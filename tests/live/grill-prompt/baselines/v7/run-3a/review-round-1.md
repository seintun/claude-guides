# Review r1 of prompt-r0.md

Read: the draft, the decision log, the skill. Nothing else.

## Part by part

- GOAL: PASS. "A plan for rebuilding customer onboarding, signed off by the user, that shows how a new client can be live one day after signing the new data agreement and names every step that cannot fit in that day, and why." One sentence, an outcome, and the clock start matches decision 1.
- DONE WHEN: FAIL. Five checks, each a Given/When/Then, and checks 2 and 3 do "fail while ... open" for the "live", "last day" and "hours" gaps. But check 2 can pass on the only path that can run (blocker 1), and check 5 asks for a reviewer verdict on sections that do not exist yet when the reviewer runs (blocker 2).
- CONTEXT: PASS. "Riskiest assumption: once the agreement is signed, every remaining onboarding step fits in one day. Cheapest test: read-only, time each step from signature to live in the records of completed onboardings, before drafting any slice." It also gives the problem in one line and points at the log by path.
- CONSTRAINTS: PASS. "Never change the contract process, and make no slice depend on changing it." and "Count the one day from the client's signature to live." match decisions 1, 2 and 4 and the log's no-gos.
- BUDGET: PASS. "Helpers: the helper cap and the reviewer cap, and no other helper." The assumed caps (1 helper, 1 reviewer) cover what the steps start. One note: "at most 2 review rounds" with a reviewer cap of 1 leaves open who runs the second review. It is not a blocker.
- STOP AND ASK IF: PASS. "A slice would change the contract process, or needs it changed to work." and the empty "Not touched" case are covered. None already holds (question 2).
- HOW TO WORK: FAIL. Step 1 searches a folder the log says is empty, and step 7 asks the reviewer to judge "each section of the plan" (blockers 1 and 2).
- REPORT: PASS. "Each DONE WHEN item as PASS, FAIL or NOT RUN, with the command you ran or the section you read. NOT RUN is not PASS."

The skill's rule on more than 3 UNKNOWN lines is met: the draft has 6, and it opens with "NOT READY TO RUN: this prompt has 6 UNKNOWN lines, and a prompt with more than 3 is not ready."

## Three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   - Zero cases: no. Checks 1, 3 and 4 each need at least one row, slice or entry, and the sign-off in check 5 requires "the user's confirmation that no step is missing from 'Current steps'".
   - Fallback path: yes. The log says "It is empty (no code, no records, no repository)", so step 1 finds nothing and only the interview path can run. Step 2 says "on the interview path, mark it `untested` in 'Gap'". Check 1 accepts "a source tag of `records` or `reported`", and check 2 asks only that "Gap" state "the elapsed time now" with no source or `untested` condition. All five checks can pass with every row `reported` and the riskiest assumption untested, while the GOAL, "shows how a new client can be live one day after signing", is shown for nothing. The GOAL does not say what this path delivers.
2. Does any STOP AND ASK condition already hold?
   - Not on quoted evidence. The nearest, "No slice can be written that removes elapsed time from a step after the signature.", cannot be judged yet, because the steps are unknown. "The user cannot name any step or system of the contract process" is not answered anywhere in the log. The log records no refusal, no contradiction and no build request.
3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   - No, for two items. (a) The record of the client's signature date: the test reads "time each step from signature to live in the records of completed onboardings", and no line locates the signature event. The log's decision 2 says "the agreement needs its own tracking", so such records may not exist for completed onboardings. (b) The steps and systems of the contract process are not an UNKNOWN line. They are left to run time: "Ask the user, in one question, to name the steps and systems of the contract process." The rest is covered by "UNKNOWN: where onboarding happens (the code, tools, spreadsheets, tickets and records it touches)".

## Blockers

1. The only runnable path leaves the riskiest assumption untested, yet the checks and the header treat it as settled.
   - Evidence: header "the current elapsed time from signature to live (the test in step 2)" is said to be settled by the work. Step 2 says the test runs "from `records` times, or, on the interview path, mark it `untested` in 'Gap'." The log says "It is empty (no code, no records, no repository)", "user did not know" for where onboarding happens, and "today's baseline is unknown". Check 2 requires "the elapsed time now" with no source rule and no "fails while the elapsed-time UNKNOWN is open" clause.
   - Why it blocks: the "elapsed time now" UNKNOWN stays open on the path that will run, but check 2 can pass with an untraced figure. The GOAL does not say what the interview path delivers, which the skill requires of a fallback.
2. Check 5 and step 7 ask the reviewer for a verdict on sections that do not exist when it runs.
   - Evidence: check 5 says "'Review' holds a PASS or FAIL with one line of evidence for every section of the plan". Step 5 lists the sections as including "Review" and "Sign-off". Step 7 says "Ask for PASS or FAIL on each section of the plan". Step 8 says "Write their typed yes and its date in 'Sign-off'", after the review, and step 7 says "After the last review, change nothing but the blockers it named, apart from 'Sign-off'".
   - Why it blocks: the reviewer cannot give evidence for an empty "Sign-off" or for its own "Review" section. A FAIL on them, if raised as a blocker, can never be fixed before sign-off. Check 5 requires "no blocker with evidence is left open", and the stop line sends an open blocker after the round cap to the user.
