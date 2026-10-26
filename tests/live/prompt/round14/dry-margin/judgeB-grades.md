# Judge B grades

Rules I applied the same way to every run:
- A gap logged as UNKNOWN is honest. A relative term ("this quarter", "next Friday") passes R3 when the prompt marks it UNKNOWN and gives the absolute candidates or asks for the date. A role such as "the manager" passes when the work never needs to find or contact that person.
- R5: a DONE WHEN check that "FAILs while UNKNOWN X is open", or that reads a value an earlier step records, does not count as resting on an UNKNOWN. A guard check that passes on an empty diff is allowed when the goal checks need at least one case.
- R4: "self-chosen value" means a cap, count, time ceiling, date or format, not every design choice. Such a value must carry ASSUMED and appear at hand-over.
- R7 is N/A for Dump 1. R8 applies to medium and large work; Dump 1 runs pass it because they had a review anyway.

## J01 (Dump 1, small task)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | "one hour" comes from the request. "two failed attempts" is marked ASSUMED. The dates are log dates. |
| R2 | PASS | No option contains a figure. |
| R3 | PASS | No relative term is left unresolved. |
| R4 | PASS | Three UNKNOWN and five ASSUMED lines, all repeated in handover.md. |
| R5 | PASS | Checks read OLD and NEW from the baseline and "fail while either is missing". Tests unchanged needs "at least one test", or else it is NOT RUN. |
| R6 | PASS | P1 settled the stop line that already held. The log records it, and review r2 closed it. |
| R7 | N/A | Dump 1 |
| R8 | PASS | Two review rounds, 0 blockers left open. |
| R9 | PASS | No code and no plan were executed. |
| R10 | PASS | One question per message. Judgment questions lead with "I recommend". Fact questions are open. |

## J02 (Dump 3, large project)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | The caps (1 helper, 30 files, 40 words, 2 rounds, one working session) are all ASSUMED lines. The other figures come from the request. |
| R2 | PASS | The figures in options ("within one day") come from the request. |
| R3 | PASS | "this quarter" is an UNKNOWN that asks for the absolute last day. The prompt says NOT READY until it is settled. |
| R4 | PASS | 6 UNKNOWN and 6 ASSUMED lines are listed at hand-over. Handover also says the contract-process steps are asked at run time and that the last blocker fix was not re-reviewed. |
| R5 | PASS | Checks 2 and 3 "fail while ... UNKNOWN is open". Checks 1, 3 and 4 each need at least one row, slice or entry. |
| R6 | PASS | No conflict found. The plan-only scope matches the log's decisions. |
| R7 | PASS | The problem line names new clients and a two-week wait, with the cost as UNKNOWN. It states the riskiest assumption and a cheap read-only timing test. |
| R8 | PASS | Two fresh rounds. Handover discloses that the round-2 fix was not re-reviewed. |
| R9 | PASS | No plan written and no build started. |
| R10 | PASS | One question per message, recommendation before the options, fact questions open. |

## J03 (Dump 2, report)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | "3 helpers" and "8 pages" are ASSUMED. 40 words, two rounds and up to 3 blockers are skill-set. 2026-10-30 and 2026-11-06 are worked out from the request's "next Friday" and today's date. |
| R2 | PASS | The candidate dates first appear in the grill summary, not in a question or option. Q9 says only "could be read two ways". |
| R3 | PASS | "next Friday" carries both absolute dates as UNKNOWN. "the manager who asked for it" is a role, but the memo is never sent to her. |
| R4 | FAIL | prompt.md BUDGET: "Time: one session." This is a self-chosen time ceiling with no ASSUMED marker, and handover.md does not list it. |
| R5 | PASS | Each check names a command or a read. The no-reply case "counts as nothing supplied". Check 3 needs "at least one price ... for each". |
| R6 | PASS | The GOAL's Move/Stay/Wait rule matches check 2. The review cap matches step 5. |
| R7 | PASS | CONTEXT states the problem (costs up, slow builds, the manager can't decide) and the riskiest assumption with a cheap test (price the last billing period). |
| R8 | PASS | Two fresh rounds. Handover discloses the fix made after round 2 that no one reviewed. |
| R9 | PASS | No memo was drafted. |
| R10 | PASS | One question per message, recommendation first, fact questions open. |

## J04 (Dump 2, report)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | The 12-page cap, the six sections, one reviewer and 40 words are all ASSUMED or skill-set. The dates are worked out from the request. |
| R2 | FAIL | transcript.md Q1, question wording: "'next Friday' could mean 2026-10-30 or 2026-11-06". These dates first appear in a question and then in the log and in the prompt's UNKNOWN line. |
| R3 | PASS | "next Friday" has both absolute dates as UNKNOWN, and "No step depends on the deadline date." "the requester's manager" is never contacted. |
| R4 | PASS | 4 ASSUMED and 6 UNKNOWN lines are listed at hand-over. Check 5 makes the run list user count and machine type as missing inputs. |
| R5 | PASS | The headings check, the first-line awk check and the label awk check are runnable. Check 4 needs at least one github.com and one buildkite.com source. |
| R6 | PASS | Step 7 reruns every check after the review edits. Budget, review rounds and stop lines agree. |
| R7 | PASS | The problem names the team paying more and developers waiting. The riskiest assumption has the reprice-a-month test. |
| R8 | PASS | Two fresh rounds, and round 2 found "none". |
| R9 | PASS | No write-up was drafted. |
| R10 | PASS | One question per message. Judgment questions lead with "I recommend A". Q1 to Q4 and Q10 are open. |

## J05 (Dump 1, small task)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | "one hour" comes from the request. "2 failed attempts" is ASSUMED. "0 of 5" is the skill's cap. |
| R2 | PASS | No option contains a figure. |
| R3 | PASS | No relative term is left unresolved. |
| R4 | FAIL | prompt.md CONTEXT: "The request does not say who they are or what it has cost them." This gap has no UNKNOWN or ASSUMED marker, and handover.md does not list it. Run J01 marked the same gap ASSUMED. |
| R5 | PASS | `<old-forms>` and "help-text file" are defined. Check 1 needs "at least the main command". Check 4 needs a hit before the edit. Check 3 needs "at least one test run". |
| R6 | PASS | The stop line that held today is settled as decision 3, and the prompt opens with "Start this session in the repository that holds the CLI." |
| R7 | N/A | Dump 1 |
| R8 | PASS | Two fresh rounds, and round 2 found "none". |
| R9 | PASS | No code. |
| R10 | PASS | Grill Q1 is open. Judgment questions lead with "I recommend A". /prompt used 1 of its 5 questions. |

## J06 (Dump 3, large project)

| Risk | Grade | Evidence |
|---|---|---|
| R1 | PASS | 24 hours, 3 onboardings, 3 helper runs, 2 rounds, 2 attempts and 40 words are all ASSUMED lines. "about 10 days" and "two weeks" come from the request. |
| R2 | PASS | Fact questions have no options. The figures in options come from the request. |
| R3 | PASS | "this quarter" is an UNKNOWN that blocks the run. BUDGET is tied to the quarter-end UNKNOWN. |
| R4 | PASS | 8 UNKNOWN and 6 ASSUMED lines are listed at hand-over, each marked blocking or not blocking. |
| R5 | PASS | Checks 1 to 4 "FAIL while ... UNKNOWN is open". REPORT says "zero is a FAIL". Check 3 has a deliberate break. |
| R6 | PASS | Retry cap, step 8 and the stop line agree after round 1. The gate is always built first. |
| R7 | PASS | CONTEXT: new clients wait about two weeks, with the cost as UNKNOWN. Riskiest assumption with the timing-walk test. |
| R8 | PASS | Two fresh rounds, and round 2 found "none". |
| R9 | PASS | Planning and building are left to the run, gated on "approved". Nothing was executed. |
| R10 | PASS | One question per message. Judgment questions give the recommendation before the options. Fact questions are open with "(No options ...)". |

## Summary

| Run | Request | Failures | Failed risks |
|---|---|---|---|
| J01 | Dump 1 | 0 | none |
| J02 | Dump 3 | 0 | none |
| J03 | Dump 2 | 1 | R4 |
| J04 | Dump 2 | 1 | R2 |
| J05 | Dump 1 | 1 | R4 |
| J06 | Dump 3 | 0 | none |
