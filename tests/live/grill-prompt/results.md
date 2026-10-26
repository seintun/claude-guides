# Results: /grill then /prompt dry run

## Round 1 (2026-10-24): before the /brief rules moved in

Three runners took one request each through `/grill`, then `/prompt`, with a simulated user. None of them could see `/brief`. A fresh judge graded the outputs.

| Risk | Run 1 (small) | Run 2 (report) | Run 3 (large) | Failed |
|---|---|---|---|---|
| R1 Invented facts | FAIL (minor) | FAIL | FAIL | 3 of 3 |
| R2 Figures through options | PASS | FAIL | FAIL | 2 of 3 |
| R3 Unresolved relative terms | PASS | PASS | FAIL | 1 of 3 |
| R4 Hidden gaps | PASS | FAIL | PASS | 1 of 3 |
| R5 Unchecked done-when | PASS | FAIL | FAIL | 2 of 3 |
| R6 Contradictions | PASS | FAIL | FAIL | 2 of 3 |
| R7 Problem and riskiest assumption | FAIL | FAIL | PASS | 2 of 3 |
| R8 Review | PASS | PASS | PASS | 0 of 3 |
| R9 Stops before the work | PASS | PASS | PASS | 0 of 3 |
| R10 Question discipline | PASS | PASS | PASS | 0 of 3 |

In round 1, R8 passed if any review existed, including one written into the prompt for the later run. The judge noted that neither skill reviewed its own log or prompt, so R8 is stricter from round 2 on.

Worst examples:
- `/prompt` wrote "2 hours", "3 helpers", "15 sources" and "600 words" itself, and the hand-over presented them as the user's.
- "About a month in" first appeared in an answer option, then became a deadline with no date.
- The decision log and the prompt disagreed on when a clock starts.
- A stop condition already held in the project the prompt was for.

Result: 7 of the 8 rules the retired `/brief` had for these risks were needed. They moved into `/grill` (open fact questions, the problem and riskiest assumption, the `UNKNOWN` and `ASSUMED` markers, resolved dates) and `/prompt` (trace every figure, resolved dates, checkable done-when, the conflict check against the decision log, a fresh review before saving).

## Round 2 (2026-10-24): after the rules moved in

Three fresh runners and a fresh judge, with the same setup. R4 and R8 were judged more strictly: R4 also flags unknowns merged into one line to stay under the cap, and R8 needs a review of the output itself, or a run that says it could not run one.

| Risk | Round 1 failed | Round 2 failed |
|---|---|---|
| R1 Invented facts | 3 of 3 | 1 of 3 |
| R2 Figures through options | 2 of 3 | 0 of 3 |
| R3 Unresolved relative terms | 1 of 3 | 0 of 3 |
| R4 Hidden gaps (stricter) | 1 of 3 | 2 of 3 |
| R5 Unchecked done-when | 2 of 3 | 3 of 3 |
| R6 Contradictions | 2 of 3 | 3 of 3 |
| R7 Problem and riskiest assumption | 2 of 3 | 0 of 3 |
| R8 Review (stricter) | 0 of 3 | 0 of 3 |
| R9 Stops before the work | 0 of 3 | 0 of 3 |
| R10 Question discipline | 0 of 3 | 1 of 3 |

What changed:
- The rules for traced figures, open fact questions, resolved dates and the problem and riskiest assumption worked.
- The large request was handed over as "not ready to run" with its unknowns listed. In round 1 the same request was handed over as ready, with its gaps hidden.

What did not:
- R5 and R6 failed in every run. The runners could not start a subagent, so each used the self-check fallback, and no self-check caught these failures.
- To test the real step, a fresh reviewer ran on each prompt as `/prompt` step 8 specifies: only the draft, the decision log and the skill. All three reviewers found the R5 and R6 failures the judge found, such as a done-when check that conflicts with a constraint, a stop condition that already holds, and a check that assumes a git repository the log says is absent.
- So the review step works when a subagent can run it. The self-check fallback does not.

New failures the rules don't yet cover:
- Two runs merged separate unknowns into one line, and one relabelled an UNKNOWN as ASSUMED, to stay under the cap.
- One run bundled several asks into one question.
- Several questions asked for facts the request or an earlier answer already held.

Limits: three runs per round, a simulated user, and a different judge each round, so small differences are noise. A runner's project folder was empty, which makes facts about the code look unknowable.

## Round 3 (2026-10-24): three tweaks, and the real review loop

Rule changes before this round:
- One gap per `UNKNOWN` line, with no merging or relabelling to stay under the cap.
- Each question asks one thing, and never asks what the request or an earlier answer gives.
- No self-check stands in for the fresh review; an unreviewed draft is labelled "Review: not run".

New method: each runner paused at `/prompt` step 8. The lead started a fresh reviewer that read only the draft, the decision log and the skill, then sent its findings back. Round 2 used a new reviewer that checked whether each blocker had closed.

The review loop:

| Run | Round 1 blockers | Round 2 | Result |
|---|---|---|---|
| 1 (small) | 2: a check that could not fail; the log path and the run folder disagreed | Both closed, none new | Saved, 3 UNKNOWN |
| 2 (report) | 3: stop conditions already held; a git check failed on a correct run; a check banned honest ASSUMED values | All closed, none new | Saved, marked not ready (4 UNKNOWN) |
| 3 (large) | 3: stop conditions already held; a check failed on a correct run; checks passed with zero real cases | All closed, none new | Saved, marked not ready (9 UNKNOWN) |

Judge's grades for round 3, failures out of 3 runs:

| Risk | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| R1 Invented facts | 3 | 1 | 2 |
| R2 Figures through options | 2 | 0 | 0 |
| R3 Unresolved relative terms | 1 | 0 | 1 |
| R4 Hidden gaps | 1 | 2 | 2 |
| R5 Unchecked done-when | 2 | 3 | 2 |
| R6 Contradictions | 2 | 3 | 2 |
| R7 Problem and riskiest assumption | 2 | 0 | 0 |
| R8 Review of the output | 0 | 0 | 0 |
| R9 Stops before the work | 0 | 0 | 0 |
| R10 Question discipline | 0 | 1 | 0 |
| Total | 13 | 10 | 9 |

Two of round 3's failures came from values the skill itself prescribes: a helper's 400-word return, and two review rounds. Under the clarified rubric, run 2's R1 and R4 pass, which brings the total to 7.

What round 3 found:
- Every blocker a reviewer named closed within two rounds, in all three runs.
- The remaining failures came from edits made after the last review. The lead passed the reviewers' non-blocking notes back, and the runners' unreviewed edits added new defects. Run 2's escape clause, which lets an all-UNKNOWN memo pass, is one. `/prompt` now says that after the last review, nothing changes but the named blockers. Any other edit goes back for review or is listed as unreviewed.
- Run 3, the largest request, still merged unknowns and left "recent" and "today's" unresolved. Prose rules are not always followed on long prompts.
- A runner's test script ran shell commands that fell back into the guide's worktree. The README now forbids shell and git commands for runners.

## Round 4 (2026-10-24): /prompt v6, the merged skill

`/prompt` v6 is v5 with these rules merged in. Its steps 8 to 12 run in order: the consistency pass, `check_prompt.py`, a fresh review, save, hand-over. Same three requests, simulated user and rubric as before. The rubric now names v5's helper cap, about 40 words per field, as a value the skill sets.

Method: three Sonnet runner subagents. Each could read only the two skills and `dumps.md`, and could use only Write and Edit inside its own scratch folder: no shell, no git, no subagents. Each paused before step 9. The lead ran `check_prompt.py` on the draft, with the decision log and the request as sources, and started a fresh Sonnet reviewer that read only the draft, the decision log and the skill. Round 2 used a new reviewer to check which blockers had closed. A fresh Opus judge graded the final files.

The review loop:

| Run | `check_prompt.py` on the first draft | Round 1 blockers | Round 2 | Final prompt |
|---|---|---|---|---|
| 1 (small) | no FAIL | 3 | All closed, 2 new. The runner fixed the 2 after the last review and said so at hand-over | No FAIL; 4 UNKNOWN, marked not ready |
| 2 (report) | FAIL c-5: "recent", "today" | 3 | All closed, none new | No FAIL; 3 UNKNOWN |
| 3 (large) | FAIL c-5: "recent", "after launch" | 3 | All closed, none new | No FAIL; 6 UNKNOWN, marked not ready |

Judge's grades, failures out of 3 runs:

| Risk | Round 1 | Round 2 | Round 3 | Round 4 (v6) |
|---|---|---|---|---|
| R1 Invented facts | 3 | 1 | 2 | 0 |
| R2 Figures through options | 2 | 0 | 0 | 0 |
| R3 Unresolved relative terms | 1 | 0 | 1 | 0 |
| R4 Hidden gaps | 1 | 2 | 2 | 1 |
| R5 Unchecked done-when | 2 | 3 | 2 | 1 |
| R6 Contradictions | 2 | 3 | 2 | 2 |
| R7 Problem and riskiest assumption | 2 | 0 | 0 | 0 |
| R8 Review of the output | 0 | 0 | 0 | 0 |
| R9 Stops before the work | 0 | 0 | 0 | 0 |
| R10 Question discipline | 0 | 1 | 0 | 0 |
| Total | 13 | 10 | 9 | 4 |

Pass bar: 9 or fewer failures of 30, and no FAIL from `check_prompt.py` on a final prompt. Result: PASS, with 4 of 30 and no FAIL.

What round 4 found:
- `check_prompt.py` caught unresolved relative terms in 2 of 3 first drafts. None reached the judge, and R3 passed in all three runs for the first time. Every figure traced (R1, 0 of 3).
- The four failures are all ones the check cannot see, and both review rounds missed them. Run 3 never asked where the onboarding code and records live, so it logged no UNKNOWN for that gap (R4). Its main check can pass over zero clients and rests on an UNKNOWN (R5). A stop condition already holds in the empty project (R6). Run 2's GOAL promises each option's monthly cost, but the branch for a missing billing export lets every check pass without it (R6).
- Limits as before: one run per request, a simulated user, and a different judge each round, so a difference of one or two failures is noise.

## Round 5 (2026-10-25): /prompt v7, two runs per request, one blind judge

`/prompt` v7 targets round 4's four misses. Step 1 finds where the work lives, and `/grill` covers it. A fallback for missing input must still meet the GOAL. Each STOP AND ASK line is tested against what is known now. The fresh review answers three questions: can a check pass with zero cases or on a fallback that skips the GOAL, does a stop condition already hold, and does every file and record have a location or an UNKNOWN.

First, a direct test of the review change. Fresh Sonnet reviewers with v7's three questions read round 4's three final prompts, which two review rounds had passed. They named all four misses the round-4 judge found: run 2's fallback that skips the GOAL, and run 3's unasked location, check over zero clients and stop condition that already holds. They also raised three blockers the judge had not counted.

Method changes, to measure noise:
- Two independent runners per request, six runs in all, set up as in round 4, with reviewers using v7's three questions.
- One fresh Opus judge graded all nine runs together: the six v7 runs and round 4's three v6 runs, in random order, with every path that named a version or a run removed. One judge for both versions removes the judge-to-judge variation of earlier rounds.

Judge's grades, failures per set of 3 runs:

| Risk | v6 (round 4, regraded) | v7 set A | v7 set B |
|---|---|---|---|
| R1 Invented facts | 0 | 0 | 0 |
| R2 Figures through options | 1 | 1 | 0 |
| R3 Unresolved relative terms | 0 | 0 | 0 |
| R4 Hidden gaps | 1 | 1 | 0 |
| R5 Unchecked done-when | 0 | 0 | 0 |
| R6 Contradictions | 2 | 0 | 0 |
| R7 Problem and riskiest assumption | 0 | 1 | 0 |
| R8 Review of the output | 0 | 0 | 0 |
| R9 Stops before the work | 0 | 0 | 0 |
| R10 Question discipline | 0 | 0 | 0 |
| Total | 4 | 3 | 0 |

Pass bar: 9 or fewer of 30, and no FAIL from `check_prompt.py` on a final prompt. Both v7 sets pass.

What round 5 found:
- **The targeted risks are gone.** R6 failed in 2 of 3 v6 runs and in none of the 6 v7 runs. Where the work lives went unasked in v6's large run and was asked in both v7 large runs.
- **The overall gap is within noise.** v7 failed 3 of 60 and v6 4 of 30, but the two v7 sets differ by 3 (3 and 0), and two runs of one request differed by up to 2. Read it as no worse overall, with the targeted risks removed.
- The same judge again gave v6 4 failures, on different risks from round 4's judge: R5 now passes, since a check that names an UNKNOWN and fails while it is open counts as checkable, and R2 fails, because both candidate dates for "next Friday" were first written in a question. v7's run 2a repeated that R2 pattern.
- v7's run 1a never asked who reads the help or what the stale text costs (R7), and left that gap unmarked (R4).
- No final v7 prompt has a FAIL. Two first-draft FAILs were the check's own bugs, found in this round: it counted bulleted DONE WHEN checks as zero, and missed parts labelled inline ("GOAL: ..."). Both are fixed and tested. The new c-8 flagged checks resting on an UNKNOWN in three runs; the judge passed them, because each check fails while its gap is open.

## Round 6 (2026-10-25): /prompt v8 against v7's frozen runs

Six v8 runs, two per request, set up as in round 5. One fresh Opus judge graded them together with v7's six round-5 runs, kept in [baselines/v7/](baselines/README.md), in random order with every version and run tell removed.

| Request | v7 runs (round 5, regraded) | v8 runs |
|---|---|---|
| Small task | 1 (R7), 0 | 2 (R6, R7), 0 |
| Report | 0, 1 (R4) | 1 (R6), 2 (R1, R5) |
| Large project | 0, 0 | 1 (R7), 1 (R7) |
| Total | 2 of 60 | 7 of 60 |

v8 failed the dry-run gate: 7 failures against 2 under the same judge. Its two sets scored 4 and 3, so the gap is wider than run-to-run noise. Both stop-condition and fallback failures (R6) came back, and three runs left the problem's cost or the riskiest assumption untested (R7). v8 was not shipped; see [../prompt/results.md](../prompt/results.md).

## Round 7 (2026-10-25): /prompt v9 against v7's frozen runs

Six v9 runs, two per request, set up as in round 6. One fresh Opus judge graded them together with v7's six round-5 runs, blinded and in random order. The rubric was the frozen one with the single change the v9 plan allowed: R7 is N/A for every run of Dump 1, the small fix that §5.3 and Template B ask only for a goal, checks and a receipt. The judge marked R7 N/A on all four Dump 1 runs.

| Request | v7 runs (round 5, regraded) | v9 runs |
|---|---|---|
| Small task | 0, 0 | 0, 2 (R4, R10) |
| Report | 1 (R2), 2 (R1, R4) | 3 (R2, R8, R10), 2 (R8, R10) |
| Large project | 1 (R3), 2 (R3, R5) | 3 (R3, R6, R10), 3 (R2, R5, R7) |
| Total | 6 of 60 | 13 of 60 |

v9 failed the dry-run gate: 13 failures against v7's 6 under the same judge. Its two sets scored 6 and 7 of 30, each inside the 9-of-30 bar, and no final prompt had a FAIL from `check_prompt.py`. This judge was stricter than round 6's, which gave the same v7 runs 2.
- **What v9's rules aimed at held only in part.** The cost of the large project's problem went unmarked again in one run (R7). One run's decision log was reworded after review, against the user's confirmed answer (R6).
- **Questions asked two things** in four v9 runs (R10), against none of v7's.
- **Edits after the last review.** Two report runs fixed a second-round blocker after the last review and did not say so at hand-over (R8). The lead's round-2 message told runners to fix the blockers and save; the skill's rule says such edits are listed as unreviewed, and neither runner did. Read these two failures as partly the method's.
- Dates first written in a question's option or wording (R2) and an unresolved "this quarter" (R3) failed in both versions.

v9 was not shipped; see [../prompt/results.md](../prompt/results.md), round 13.

## Round 8 (2026-10-25): /prompt v10, and the runner method

Six v10 runs, two per request (judge files in [../prompt/round14/dry-run/](../prompt/round14/README.md)), with this round's runner brief: the runner plays the user, the lead runs `check_prompt.py` and two fresh review rounds, and each fix message quotes the skill's rule on edits after the last review.
- **Against v7's frozen runs v10 looked worse.** Three judges gave v10 7, 9 and 6 failures against 1, 1 and 3 for v7's round-5 runs. Most of v10's were R6 about its own paperwork: a "Review: not run" line left after two reviews, or a hand-over that misstated what changed after the last review.
- **Removing R1 changed nothing.** The bundle without R1 failed 6, as the full bundle did, under the same judge.
- **Under the same method there was no gap.** Six fresh v7 runs made with this round's runner brief failed 7, and v10's six failed 7, under one judge. The earlier gap came from comparing runs made two different ways, as the battle round's T1 did. The dry-run gate was read against the fresh v7 runs: 0 extra failures against a margin of 0.
- **R10 is not a v10 regression.** Questions that asked two things appeared in two fresh v7 runs and one v10 run.
- No final prompt in any set had a FAIL from `check_prompt.py`.

## The deterministic check (2026-10-24)

`skills/prompt/check_prompt.py` now runs on every draft, before the fresh review. On the three round-3 prompts, with each run's decision log and the requests as sources:

| Run | FAIL lines | Judge agreed? | WARN figures |
|---|---|---|---|
| 1 | none | Yes: the judge passed R1, R3 and R4 | 3, all harmless counts |
| 2 | c-4: 4 UNKNOWN lines, and the file never says "not ready" | The judge missed it. The runner said "not ready" only in chat, so a fresh session running the file would not know | 5, including the writer-chosen "two helpers" |
| 3 | c-3: lines 78 and 80 join two gaps. c-5: "recent" three times, "today's" three times | Yes: these are the judge's R3 and R4 findings | 5, including the judge's "up to two" records |

What it cannot see: contradictions between parts, checks a stranger can't run, and stop conditions that already hold. Those stay with the fresh review.

The earlier proposal for this check: Law 9 says that what must hold should be enforced in code. A small script `/prompt` runs before hand-over could:
- count UNKNOWN lines and flag joined ones;
- flag relative terms from a fixed list;
- flag numbers that are neither marked nor found in the decision log.
It would catch the misses that prose rules leave on long prompts.
