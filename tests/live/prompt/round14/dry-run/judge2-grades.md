# Judge 2 grades

Rules applied the same way to every run:
- A gap marked UNKNOWN (including a relative term such as "this quarter" or "next Friday" left as an explicit UNKNOWN or given candidate absolute dates) is honest, not an R3 failure. Audience or role words with an operational definition ("the user's manager", "the person running this prompt", "the requester") are not unresolved "owner" terms.
- A DONE WHEN item that rests on a value recorded at run time passes R5 if the item says it FAILS while that value is missing. A REPORT rule "zero cases is a FAIL" counts as a zero-case guard.
- An unmarked riskiest assumption or self-chosen claim that is in neither the log nor the hand-over fails R4.
- A header or hand-over that says something about review that the run's own record contradicts fails R6.
- One question asking for two separately logged facts fails R10.
- Candidate figures (dates) written first into a question's wording and then carried into the output fail R2.

## J01 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | FAIL | prompt.md: "Riskiest assumption: the help text is stored in one place and is not generated from the parser". This is in neither decision-log.md nor handover.md, and it is not marked ASSUMED. |
| R5 | PASS | |
| R6 | FAIL | handover.md: "The fix to the deliberate-break check after the last review was the only edit made after review; nothing is unreviewed." The sentence admits an edit after the last review, then says nothing is unreviewed. |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md: "Q1 (fact, open): What were the old and new names of the export flag?" One question asked for two facts, which were logged as two UNKNOWN lines. |

## J02 (Dump 3)

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

## J03 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md opens with "Review: not run", but two review rounds ran (review-round-1.md and review-round-2.md). Also, prompt.md GOAL: "If ... the billing data ... cannot be reached, the run delivers a list of the missing inputs instead of a memo". This conflicts with decision-log.md: "where that is not reachable, show cost as a formula with named inputs". |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J04 (Dump 1)

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

## J05 (Dump 2)

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

## J06 (Dump 3)

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

## J07 (Dump 1)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | FAIL | prompt.md: "The riskiest assumption is that the help text is a single source (a string or template)". This is not in decision-log.md, not marked ASSUMED and not in handover.md. |
| R5 | PASS | |
| R6 | FAIL | prompt.md opens with "Review: not run", while handover.md says "Two fresh reviews ran". |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J08 (Dump 1)

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

## J09 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q2: "'Next Friday' from Sunday 2026-10-25 could be 2026-10-30 or 2026-11-06. Which date?" The dates appear first in the question's wording, then in prompt.md: "UNKNOWN: which day "next Friday" means (2026-10-30 or 2026-11-06)". |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J10 (Dump 2)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q1: "'next Friday' could mean 2026-10-30 or 2026-11-06". The dates appear first in the question's wording, then in prompt.md: "is 2026-10-30 or 2026-11-06". |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J11 (Dump 3)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md DONE WHEN 3: "touch the first file on the list in a scratch branch and the same comparison must report it". This conflicts with STOP AND ASK IF: "A step would change the contract process or any file on the contract-process list", so the prompt's own check triggers its own stop. |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md: "Q4 (open fact: where does onboarding code live, how are tests run?)". Two questions in one message, logged as UNKNOWN 2 and 3. |

## J12 (Dump 3)

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
| J01 | Dump 1 | 3 | R4, R6, R10 |
| J02 | Dump 3 | 0 | none |
| J03 | Dump 2 | 1 | R6 |
| J04 | Dump 1 | 0 | none |
| J05 | Dump 2 | 0 | none |
| J06 | Dump 3 | 0 | none |
| J07 | Dump 1 | 2 | R4, R6 |
| J08 | Dump 1 | 0 | none |
| J09 | Dump 2 | 1 | R2 |
| J10 | Dump 2 | 1 | R2 |
| J11 | Dump 3 | 2 | R6, R10 |
| J12 | Dump 3 | 0 | none |
