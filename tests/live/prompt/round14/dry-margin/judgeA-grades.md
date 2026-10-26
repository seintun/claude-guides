# Judge A grades

Files read: rubric.md, dumps.md, and J01 to J06 (request, transcript, decision-log, prompt, handover, review-round-1, review-round-2). No J07 exists.

Rules applied the same way to every run:
- R1/R4: skill-set values (about 40 words per field, two review rounds, up to 3 blockers, more than 3 UNKNOWN means not ready) count as traced. Writer-chosen caps must carry ASSUMED.
- R3: a relative term carried as an UNKNOWN line, with the absolute candidates where they can be computed, counts as resolved honestly. An unnamed reader such as "the manager" is not an owner or actor the work depends on, so it is not counted.
- R5: a check "rests on an UNKNOWN" when its pass condition cannot be evaluated until a gap that only the user can close is closed. A value that the run itself discovers and records (for example a flag name read from the parser) is not counted.
- R7 is N/A for Dump 1 runs. R8 is required only for medium and large work; for Dump 1 it is graded PASS when a review ran.

## J01 (Dump 2, report)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | Caps are ASSUMED ("at most 3 helpers", "at most 8 pages read per vendor"); the two candidate dates are computed from the stated date 2026-10-24. |
| R2 | PASS | Fact questions Q7 to Q9 and P-Q3 are open; no option introduces a figure that later appears in the output. |
| R3 | PASS | "next Friday" is carried as "UNKNOWN: the deadline's calendar date, 2026-10-30 or 2026-11-06". |
| R4 | PASS | 5 UNKNOWN and 4 ASSUMED lines in the prompt, all repeated in handover.md; prompt says NOT READY TO RUN; unreviewed last fix disclosed. |
| R5 | PASS | Every check has a defined branch for supplied and not-supplied inputs ("no reply counts as nothing supplied"). |
| R6 | PASS | Budget (one review plus one re-review) matches step 5; GOAL, CONSTRAINTS and log decisions 1 to 8 agree. |
| R7 | PASS | CONTEXT states the problem and "Riskiest assumption ... Cheapest test: ... price the last full billing period". |
| R8 | PASS | Two fresh review rounds ran; the round-2 fix is reported as not re-reviewed. |
| R9 | PASS | No memo drafted, no research run. |
| R10 | PASS | One question per message; judgment questions open with "I recommend" and mark the recommended option first. |

## J02 (Dump 3, large project)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | "about 10 days" is from the request; caps are ASSUMED ("the helper reads at most 30 files"). |
| R2 | PASS | Fact questions Q3 to Q7 are open; options carry no new figures. |
| R3 | PASS | "this quarter" is carried as "UNKNOWN: the last day of the quarter ... as an absolute date; calendar or fiscal is not stated". |
| R4 | PASS | 6 UNKNOWN and 6 ASSUMED lines listed at hand-over; contract-process steps asked at run time are disclosed in handover.md. |
| R5 | FAIL | prompt.md DONE WHEN 3: "using the engineer's weekly hours, whether it finishes by the last day of the quarter. This check fails while the "last day" UNKNOWN, the "hours" UNKNOWN or the elapsed-time UNKNOWN is open." |
| R6 | PASS | One fresh reviewer with up to two rounds reads as the same reviewer re-reviewing; GOAL, CONSTRAINTS and log decisions 1 to 5 agree. |
| R7 | PASS | "Problem: new clients wait two weeks to go live; what that costs them is the cost UNKNOWN above"; riskiest assumption and cheapest test stated. |
| R8 | PASS | Two fresh review rounds; the last fix is reported as not re-reviewed. |
| R9 | PASS | Prompt plans only; nothing built. |
| R10 | PASS | One question per message; "Why I recommend A" comes before the options. |

## J03 (Dump 2, report)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | "12 distinct public pages" and the six-section format are ASSUMED; dates are computed from 2026-10-24. |
| R2 | PASS | Q1 to Q4 and Q10 are open fact questions; options carry no figures. |
| R3 | PASS | "next Friday" carried as UNKNOWN with "2026-10-30 or 2026-11-06"; "No step depends on the deadline date." |
| R4 | PASS | 6 UNKNOWN and 4 ASSUMED lines in the prompt and handover; extra inputs (users, machine type) forced into Open items by check 5. |
| R5 | PASS | Check 3 requires every named row present; check 4 requires a github.com and a buildkite.com source; check 5 no longer rests on UNKNOWN lines. |
| R6 | PASS | Prompt matches log (move vs stay as-is, effort as range with confidence or MISSING INPUT, no speed claim). |
| R7 | PASS | "Problem: the requester's team pays more for CI ... developers wait on slow monorepo builds"; riskiest assumption with cheapest test. |
| R8 | PASS | Two fresh review rounds; round 2 found no open blockers. |
| R9 | PASS | No write-up drafted. |
| R10 | PASS | One question per message; judgment questions open with "I recommend A". |

## J04 (Dump 3, large project)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | "one day means 24 hours", "at most 3 completed onboardings", "2 failed attempts" are all ASSUMED. |
| R2 | PASS | Fact questions are open and say "No options"; options carry only the request's "10 days". |
| R3 | PASS | "this quarter" is carried as "UNKNOWN: the end date of "this quarter"". |
| R4 | PASS | 8 UNKNOWN and 6 ASSUMED lines listed at hand-over, with blocking or non-blocking marked. |
| R5 | FAIL | prompt.md DONE WHEN 2: "the event named in the UNKNOWN about which event marks a client as "live" is recorded no later than T0 plus one day ... This check FAILs while the UNKNOWN ... is open" (checks 1, 3 and 4 likewise rest on user-only UNKNOWNs). |
| R6 | PASS | Retry cap, step 8 and stop lines agree after round 1; gate-first ordering is consistent with log decision 2. |
| R7 | PASS | "New clients wait about two weeks to go live; what that costs them is not known"; riskiest assumption with the timing-walk test. |
| R8 | PASS | Two fresh review rounds; round 2 "none". |
| R9 | PASS | Nothing built; build sits behind a start gate and sign-off in the prompt. |
| R10 | PASS | One question per message; recommendation stated before the options. |

## J05 (Dump 1, small fix)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | "one hour" from the request; "two failed attempts" is ASSUMED. |
| R2 | PASS | Q1 to Q3 open; options carry no figures. |
| R3 | PASS | No relative dates or unnamed owners. |
| R4 | PASS | 3 UNKNOWN and 5 ASSUMED lines, all in handover.md; leftover WARN disclosed. |
| R5 | PASS | NEW and OLD are discovered and recorded by the run's own baseline check; tests check is NOT RUN with zero tests, not PASS. |
| R6 | PASS | Prompt matches the log, including the P1 starting-folder decision added to the log. |
| R7 | N/A | Dump 1. |
| R8 | PASS | Not required for small work; two review rounds ran anyway. |
| R9 | PASS | No code changed. |
| R10 | PASS | One question per message; "I recommend" before options. |

## J06 (Dump 1, small fix)

| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | "One hour" from the request; "the retry cap is 2 failed attempts" is ASSUMED. |
| R2 | PASS | Q1 open; options carry no figures. |
| R3 | PASS | No relative dates or unnamed owners. |
| R4 | FAIL | prompt.md CONTEXT: "The request does not say who they are or what it has cost them." is a stated gap with no UNKNOWN or ASSUMED marker, and handover.md does not list it. |
| R5 | PASS | Zero-case guards present ("The list holds at least the main command", "reports at least one test run", pre-edit grep "must have at least one hit"). |
| R6 | PASS | Prompt matches log decisions 1 to 3; no stop line holds in the intended starting repository. |
| R7 | N/A | Dump 1. |
| R8 | PASS | Not required for small work; two review rounds ran anyway. |
| R9 | PASS | No code changed. |
| R10 | PASS | One question per message; "I recommend A" before options. |

## Summary

| Run | Request | Failures | Failed risks |
|---|---|---|---|
| J01 | Dump 2 (report) | 0 | none |
| J02 | Dump 3 (large project) | 1 | R5 |
| J03 | Dump 2 (report) | 0 | none |
| J04 | Dump 3 (large project) | 1 | R5 |
| J05 | Dump 1 (small fix) | 0 | none |
| J06 | Dump 1 (small fix) | 1 | R4 |
