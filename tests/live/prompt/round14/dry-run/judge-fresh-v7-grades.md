# Grades: /grill + /prompt dry run

Judged against `v7dry-judge/rubric.md` only. Skill-prescribed values (about 40 words, 2 review rounds, up to 3 blockers, "more than 3 UNKNOWN", a two-failure rule) count as traced. Consistent rulings applied to every run:
- "the requester" / "the user" / "the manager" count as named roles, not unresolved relative terms (R3).
- A location UNKNOWN covers the commands found inside that location (test command, build command) (R4).
- Two distinct facts joined in one question count as two questions (R10); one fact pair (old and new name of one flag) counts as one.
- Candidate dates that first appear in a question's wording and then in the output fail R2, even though they are labelled UNKNOWN.
- A prompt top line that says "Review: not run" when two reviews ran is a conflict between parts (R6).

## J01 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J02 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | handover.md: "The fix to the deliberate-break check after the last review was the only edit made after review; nothing is unreviewed." (an edit made after the last review is unreviewed) |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J03 (Dump 3)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J04 (Dump 3)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | FAIL | decision-log.md: "Cost of the delay to clients or the business: not asked; not stated in the request." (gap not marked UNKNOWN and not listed in handover.md) |
| R5 | PASS | |
| R6 | PASS | |
| R7 | FAIL | prompt.md CONTEXT: "Who struggles and what the delay costs them is not known." |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md Q11: "Who at legal owns the data agreement, and who is the engineer?" (two questions in one message; also Q2) |

## J05 (Dump 3)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J06 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q2: "'Next Friday' from Sunday 2026-10-25 could be 2026-10-30 or 2026-11-06. Which date?" then prompt.md: "UNKNOWN: which day "next Friday" means (2026-10-30 or 2026-11-06)" |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J07 (Dump 3)

| Risk | Result | Evidence |
|---|---|---|
| R1 | FAIL | prompt.md CONTEXT: "new clients wait about two weeks to be live, of which about 10 days is waiting for the data agreement to be signed" (the request does not say the 10 days is part of the two weeks; not marked ASSUMED) |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md DONE WHEN 3: "touch the first file on the list in a scratch branch" against STOP AND ASK IF: "A step would change the contract process or any file on the contract-process list." |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md Q4: "open fact: where does onboarding code live, how are tests run?" (two questions in one message) |

## J08 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q2: "Today is Sunday 2026-10-25, so it could be 2026-10-30 or 2026-11-06." then prompt.md: "UNKNOWN: which Friday "next Friday" means (2026-10-30 or 2026-11-06)" |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" against handover.md: "Review: two fresh rounds ran" |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md Q4: "What do the monorepo builds take today, and what time would count as fast enough?" (two questions in one message) |

## J09 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" against handover.md: "Two fresh reviews ran" |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J10 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | decision-log.md: "where that is not reachable, show cost as a formula with named inputs" against prompt.md GOAL: "If the repository, the billing data or the run history cannot be reached, the run delivers a list of the missing inputs instead of a memo" (also prompt.md line 1 "Review: not run" after two reviews) |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J11 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" against handover.md: "Two fresh reviews ran" |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J12 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## Summary

| Run | Request | Failures | Failed risks |
|---|---|---|---|
| J01 | Dump 1 | 0 | none |
| J02 | Dump 1 | 1 | R6 |
| J03 | Dump 3 | 0 | none |
| J04 | Dump 3 | 3 | R4, R7, R10 |
| J05 | Dump 3 | 0 | none |
| J06 | Dump 2 | 1 | R2 |
| J07 | Dump 3 | 3 | R1, R6, R10 |
| J08 | Dump 2 | 3 | R2, R6, R10 |
| J09 | Dump 1 | 1 | R6 |
| J10 | Dump 2 | 1 | R6 |
| J11 | Dump 1 | 1 | R6 |
| J12 | Dump 2 | 0 | none |
