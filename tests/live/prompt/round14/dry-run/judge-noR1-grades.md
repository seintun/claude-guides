# Judge grades: /grill and /prompt dry run, J01 to J18

Standards applied the same way to every run:
- R2: a candidate figure offered inside a fact question (for example the two possible dates for "next Friday") counts as a figure in an option. Today's date alone does not.
- R3: "this quarter" left as UNKNOWN, with no absolute date, fails, even when it is honestly marked. So does a role that must act but has no name ("the named signer", "a person approves"). A deadline given as two absolute candidate dates passes. A passive reader ("the manager") passes.
- R5: a check that fails while its UNKNOWN is open, or reports NOT RUN on zero cases, passes. A zero-case path also passes when the GOAL names what that path delivers, or when other checks carry the goal.
- R6: a prompt header that says "Review: not run" after two reviews ran is a conflict between parts of the output. So is a hand-over that says nothing is unreviewed when an edit came after the last review.
- R10: a single message that asks two separate questions fails.

## J01 (Dump 3)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md CONTEXT: "copy it there from the guide if it is not in the project" (docs/discovery/customer-onboarding.md) against CONSTRAINTS: "Files you may create or change: `docs/plans/onboarding-one-day.md`, the onboarding code and its new tests, and `<scratch>` working files. Nothing else." |
| R7 | PASS | |
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
| R6 | FAIL | prompt.md line 1: "Review: not run", against handover.md: "Reviews: two fresh reviews ran." |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J03 (Dump 3)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | FAIL | prompt.md: "UNKNOWN: U4 the end date of the quarter deadline the user calls \"this quarter\"" (no absolute date), and HOW TO WORK 7: "A person approves the plan" (no name) |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
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
| R6 | FAIL | handover.md: "The fix to the deliberate-break check after the last review was the only edit made after review; nothing is unreviewed." The sentence contradicts itself: that fix came after the last review, so it is unreviewed. |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J05 (Dump 1)
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

## J06 (Dump 3)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | FAIL | prompt.md: "UNKNOWN: the last day of the quarter the request calls \"this quarter\", as an absolute date; calendar or fiscal is not stated." No date is given. |
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
| R1 | PASS | |
| R2 | PASS | |
| R3 | FAIL | prompt.md HOW TO WORK 2 and 6: "get the named signer's yes in chat" and "the named signer approves the plan", while "UNKNOWN: who signs off the plan and the finished work" |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md: "Q4 (open fact: where does onboarding code live, how are tests run?)", two questions in one message |

## J08 (Dump 2)
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

## J09 (Dump 1)
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

## J10 (Dump 2)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run" after two review rounds ran. The prompt also conflicts with its log: HOW TO WORK 1, "If the repository, the billing export or the run history is missing, report the missing inputs ... and stop; write no memo", against decision-log.md: "where that is not reachable, show cost as a formula with named inputs" |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J11 (Dump 2)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run", against handover.md: "The last review's one blocker was fixed" (two rounds ran) |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J12 (Dump 2)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q1 (fact): "\"next Friday\" could mean 2026-10-30 or 2026-11-06". The dates appear first in the question and then in the prompt's UNKNOWN line. |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J13 (Dump 2)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q1 (fact): "'Next Friday' could be 2026-10-30 or 2026-11-06. Which date do you mean?" The dates appear first in the question and then in the prompt's UNKNOWN line. |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | FAIL | transcript.md Q3: "Where do the CI billing data and the CI configuration live, and who can export them?" (the transcript notes "Two things; I asked as one") |

## J14 (Dump 2)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | FAIL | transcript.md Q2 (fact): "\"Next Friday\" from Sunday 2026-10-25 could be 2026-10-30 or 2026-11-06. Which date?" The dates appear first in the question and then in the prompt's UNKNOWN line. |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J15 (Dump 1)
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

## J16 (Dump 3)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | FAIL | prompt.md: "UNKNOWN: the end date of \"this quarter\"", and BUDGET: "the end date in the quarter-end UNKNOWN". No absolute date is given. |
| R4 | PASS | |
| R5 | PASS | |
| R6 | PASS | |
| R7 | PASS | |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J17 (Dump 1)
| Risk | Result | Evidence |
|---|---|---|
| R1 | PASS | |
| R2 | PASS | |
| R3 | PASS | |
| R4 | PASS | |
| R5 | PASS | |
| R6 | FAIL | prompt.md line 1: "Review: not run", against handover.md: "Two fresh reviews ran" |
| R7 | N/A | Dump 1 |
| R8 | PASS | |
| R9 | PASS | |
| R10 | PASS | |

## J18 (Dump 3)
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
| J01 | Dump 3 | 1 | R6 |
| J02 | Dump 1 | 1 | R6 |
| J03 | Dump 3 | 1 | R3 |
| J04 | Dump 1 | 1 | R6 |
| J05 | Dump 1 | 0 | none |
| J06 | Dump 3 | 1 | R3 |
| J07 | Dump 3 | 2 | R3, R10 |
| J08 | Dump 2 | 0 | none |
| J09 | Dump 1 | 0 | none |
| J10 | Dump 2 | 1 | R6 |
| J11 | Dump 2 | 1 | R6 |
| J12 | Dump 2 | 1 | R2 |
| J13 | Dump 2 | 2 | R2, R10 |
| J14 | Dump 2 | 1 | R2 |
| J15 | Dump 1 | 0 | none |
| J16 | Dump 3 | 1 | R3 |
| J17 | Dump 1 | 1 | R6 |
| J18 | Dump 3 | 0 | none |
