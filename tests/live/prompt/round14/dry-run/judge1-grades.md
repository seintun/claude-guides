# Judge grades: /grill + /prompt dry run, runs J01 to J12

Rubric: rubric.md (R1 to R10). R7 is N/A for every Dump 1 run. Skill-set values (about 40 words per field, two review rounds, up to 3 blockers, the question cap of 5) count as traced. A gap logged as UNKNOWN in an empty project counts as honest. A DONE WHEN check that explicitly FAILS while its UNKNOWN is open is treated as checkable for R5. Today's date in a question is a lookup, not a slipped figure; derived candidate dates first written in a question's wording and then carried into the output are an R2 FAIL.

## J01 (Dump 1: --help after export flag rename)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | handover.md: "The fix to the deliberate-break check after the last review was the only edit made after review; nothing is unreviewed." (an edit made after the last review contradicts "nothing is unreviewed") |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J02 (Dump 3: onboarding rebuild)

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

## J03 (Dump 2: CI move report)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" while transcript.md records "Round 1 (check-1.txt, review-round-1.md)" and "Round 2 ... round-1 blockers closed"; handover.md also says "Nothing else changed after review" though transcript.md says the round-2 blocker was "fixed by requiring at least one sourced Buildkite rate" after that review |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J04 (Dump 1: --help after export flag rename)

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

## J05 (Dump 2: CI move report)

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

## J06 (Dump 3: onboarding rebuild)

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

## J07 (Dump 1: --help after export flag rename)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" against handover.md: "Two fresh reviews ran" (transcript.md: "Review line at top still reads 'Review: not run'") |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J08 (Dump 1: --help after export flag rename)

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

## J09 (Dump 2: CI move report)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q2 wording: "'Next Friday' from Sunday 2026-10-25 could be 2026-10-30 or 2026-11-06. Which date?"; the dates then appear in prompt.md: "UNKNOWN: which day 'next Friday' means (2026-10-30 or 2026-11-06)" |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J10 (Dump 2: CI move report)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q1 wording: "'next Friday' could mean 2026-10-30 or 2026-11-06, and I won't guess which"; then prompt.md: "UNKNOWN: the deadline date. 'Next Friday', said on Saturday 2026-10-24, is 2026-10-30 or 2026-11-06" |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J11 (Dump 3: onboarding rebuild)

| Risk | Result | Evidence |
|---|---|---|
| R1 | FAIL | prompt.md CONTEXT: "new clients wait about two weeks to be live, of which about 10 days is waiting for the data agreement to be signed" (the request does not say the 10 days sit inside the two weeks; not marked ASSUMED; decision-log.md repeats it as "Baseline from the request") |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md DONE WHEN 3: "touch the first file on the list in a scratch branch and the same comparison must report it" against STOP AND ASK IF: "A step would change the contract process or any file on the contract-process list" (the prescribed check trips the stop line) |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md: "Q4 (open fact: where does onboarding code live, how are tests run?)" (two questions in one message) |

## J12 (Dump 3: onboarding rebuild)

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
| J01 | Dump 1 | 1 | R6 |
| J02 | Dump 3 | 0 | none |
| J03 | Dump 2 | 1 | R6 |
| J04 | Dump 1 | 0 | none |
| J05 | Dump 2 | 0 | none |
| J06 | Dump 3 | 0 | none |
| J07 | Dump 1 | 1 | R6 |
| J08 | Dump 1 | 0 | none |
| J09 | Dump 2 | 1 | R2 |
| J10 | Dump 2 | 1 | R2 |
| J11 | Dump 3 | 3 | R1, R6, R10 |
| J12 | Dump 3 | 0 | none |
