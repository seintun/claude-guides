# /prompt battle test: results (2026-10-24)

Every run was a fresh `claude -p` session (Sonnet) in a throwaway project outside the repository. The project held only a README: a Node 20 service on Postgres, tested with `npm test`. Six scenarios ([scenarios.json](scenarios.json)). Baseline prompt: "Write me a prompt for Claude Code to do this: <scenario>". Both arms were told to skip questions and draft now.

## Skill versions

| Version | Change | Evidence that drove it |
|---|---|---|
| v1 | First draft from cheat sheet sections 6 and 7, Templates B, C and H, Law 3, §5.3, §7 and §9.1. Saved prompts in the project | — |
| v1 + save step | Prompts saved in the guide's git-ignored `prompts/<project>/`, never the project | Owner's decision |
| v2 | One writer per set of files, with disjoint batches for mechanical work. Checks that can fail while the goal is unmet. A deliberate-break check. The same brief for helpers whose results get compared. NEEDS A HUMAN for unattended runs. A budget ceiling. No leaked house rules | Blind review 1 |
| v3 | Constraints cross-checked against the goal, steps and files. Isolation and coexistence for parallel writers. Each check inspects exactly its claim | Blind review 2 |
| v4 | An integration step for batches. At most 5 checks. Each check walked against the steps. No session-only paths | Blind review 3 and round 5's rubric misses |
| Checker trial (not shipped) | A fresh read-only checker runs the consistency pass, at most 2 rounds; drafts aim under about 100 lines; review rules only when more than one round is expected. Archived in [variants/SKILL-v5-checker-trial.md](variants/SKILL-v5-checker-trial.md) | Round 8: v5 cut contradictions only from 12 to 10 |
| v5 | A consistency pass before saving, step 8: files, helpers, time and cost, transformations, skips, targets, evidence, caps, contradictions. Deliberate breaks name the exact change; CI checks name the exact commit. The synthesis is its own numbered step | Blind review 4: contradicting constraints in 5 of 6 v4 drafts |
| v6 | v5 plus the rules of the retired `/brief`: open fact questions, every figure traced or marked `ASSUMED` or `UNKNOWN`, absolute dates, `check_prompt.py` (step 9) and a fresh review before saving (step 10) | The grill-then-prompt dry runs ([../grill-prompt/results.md](../grill-prompt/results.md)) |
| v7 | Each value the writer chooses is listed once as `ASSUMED` at the top. Step 1 finds where the work lives. A fallback for missing input still meets the GOAL. Each STOP AND ASK line is tested against what is known now. The fresh review answers three questions: zero cases or a fallback that skips the GOAL, a stop condition that already holds, files or records with no location. `check_prompt.py` adds c-7 (a figure marked twice) and c-8 (a check resting on an UNKNOWN) | Dry-run round 4's four misses, and round 10's reviewers calling inline `ASSUMED` tags noise |
| v8 (not shipped) | A risk line (low, normal, high) sets which parts a prompt needs, enforced by `check_prompt.py`; batch, helper and loop rules in a file read on demand; GOAL first, assumptions after REPORT; a 20-line example; the playbook rules v7 lacked. Archived in [variants/](variants/README.md) | The sourced review in [research/prompt-skill-review.md](../../../research/prompt-skill-review.md) |
| v9 (not shipped) | v8's gains with Templates B and L's sizes (`trivial`, `normal`, `high`, set by a rule), Template B's trivial form, a rule that each check names the likeliest way the result could be faked and fails on it, length set by risk, and three rules aimed at v8's dry-run failures. Archived in [variants/](variants/README.md) | v8's failed gates ([docs/plans/prompt-v9.md](../../../docs/plans/prompt-v9.md)) |

## Blind pairwise reviews

A fresh Opus reviewer saw each pair as X and Y in random order, with neutral criteria: outcome clarity, whether the checks prove the claim, safety, fit and consistency, and delegation. It never knew which draft came from the skill. Each review compared a different baseline set.

| Review | Skill | Baseline drafts | Skill wins | Average score, skill vs baseline |
|---|---|---|---|---|
| 1 | v1 (round 1) | round 1 | 3 of 6 (feature, bugfix, refactor) | 7.3 vs 7.0 |
| 2 | v2 (round 4) | round 2 | 6 of 6 | 8.0 vs 5.8 |
| 3 | v3 (round 5) | round 1 | 6 of 6 | 7.8 vs 6.0 |
| 4 | v4 (round 7) | round 7 | 6 of 6 | 8.2 vs 6.7 |
| 5 | v5 (round 8) | round 8 | 6 of 6 | 8.2 vs 6.2 |
| 6 | v5 against v4 (both round 8) | — | v5 won 4 of 6 (feature, migration, overnight, research); v4 won bugfix and refactor | 8.2 vs 7.3 |
| 7 and 8 | The checker trial (round 9) against v5 (round 8), same pairs in both position orders | — | The checker trial won 1 of 12 (research, in one order); v5 won the rest | Checker trial 7.4 vs v5 8.3 |
| 9 and 10 | v6 (round 10) against v5 (round 8), same pairs in both position orders | — | v6 won 6 of 12: overnight in both orders, and bugfix, feature, migration and research in one order each; v5 won refactor in both orders | v6 7.5 vs v5 7.6 |
| 11 and 12 | v7 (round 11) against v6 (round 10), same pairs in both position orders | — | v7 won 7 of 12: bugfix and refactor in both orders, feature and research in one order, migration in the other; v6 won overnight in both orders | v7 7.5 vs v6 7.5 |
| 13 and 14 | v8 (round 12) against v7 (round 11, frozen baselines), both position orders | — | v8 won 1 of 12 (research, in one order); v7 won the rest | v8 7.0 vs v7 8.1 |
| 15 and 16 | v9 (round 13) against v7 (round 11, frozen baselines), both position orders | — | v9 won 5 of 12: refactor and research in both orders, migration in one; v7 won bugfix, feature and overnight in both orders and migration in the other | v9 7.2 vs v7 7.7 |

Review 4 used fresh drafts for both arms (round 7), blinded the same way: the X/Y order was random, a key file the reviewer never saw held the mapping, and lines that named the guide, a save path or playbook sections were removed. v4 won every pair, by 1 to 3 points: bugfix 8 vs 7, feature 8 vs 6, migration 8 vs 7, overnight 8 vs 7, refactor 8 vs 7, research 9 vs 6. The decisive reasons were a proof that the new test fails without the fix, a check that existing tests were not edited, a deliberate-break check, per-writer database isolation, patch detection from the lockfile rather than the PR title, and runnable checks with one identical helper brief.

The reviewer also listed weaknesses in the v4 drafts. Most are constraints that contradict the goal or each other, which the skill's "check every CONSTRAINT and BUDGET line" rule should have caught:
- feature: one check wants a CSV parser to read back the original text and also wants a leading `=` neutralised;
- refactor: it writes a plan file that its own constraints forbid, and lets the agent choose the deliberate break;
- migration: a log grep that ordinary output can match stands in for database isolation; a NEEDS A HUMAN list blocks the final cutover;
- overnight: a CI query not tied to the merge commit; 5 merges with 15-minute waits overrun the 60-minute cap;
- research and bugfix: a 400-word cap for 10 sourced fields; one optional helper in the budget but a required fresh reviewer in the steps.

Round 8 was drafted by fresh subagents of one session instead of fresh `claude -p` sessions, because the command-line login had expired and the sandbox could not refresh it. All three arms (v5, v4 and the baseline) were drafted the same way, from the same project README and request, so they compare with each other; they compare less directly with rounds 1 to 7.

Reviews 5 and 6 and a contradiction audit each went to a fresh Opus reviewer with the drafts blinded as before:
- **Review 5, v5 against the baseline:** v5 won all 6, by 1 to 4 points.
- **Review 6, v5 against v4:** v5 won 4 of 6. The reviewer chose Draft X in all six pairs, so position bias may have played a part. It also counted conflicts inside each draft: 9 in the v5 drafts against 15 in the v4 drafts.
- **Contradiction audit:** a third reviewer read the 12 skill drafts one at a time, in random order, and listed every pair of lines that cannot both be followed. It found 10 in the v5 drafts (about 1.7 each) against 12 in the v4 drafts, and rated over-specification 9 against 10 (out of 18).

v5 reduced contradictions without removing them. A draft that checks itself against a list misses most of its own conflicts, which is the playbook's Law 7: the checker should not be the maker. Both versions are also longer and more detailed than the tasks need; the review rules, for one, get spelled out even for a single critic pass.

Round 9 tested the checker trial, a v5 variant that hands the consistency pass to a fresh read-only checker, at most 2 rounds, and aims drafts at under about 100 lines. Each checker-trial draft came from a subagent drafter. A separate checker subagent, which saw only the draft and the step 8 list, quoted conflicts, and the drafter fixed them. Three drafts were clean at once, one needed a round, and two needed both rounds. None ended with an OPEN CONFLICTS block. To avoid the position bias seen in review 6, the same six pairs went to two fresh reviewers in opposite orders (reviews 7 and 8), and a third audited all 12 drafts one at a time.
- The checker worked: the audit found 2 contradictions in the checker-trial drafts against 10 in v5 (the same v5 drafts as round 8, where the audit also found 10). Pairwise reviewers counted 8 conflicts in the checker trial against 19 in v5, and over-specification fell from 10 to 6 of 18. Checker-trial drafts ran 57 to 78 lines against 84 to 147.
- Quality fell anyway: v5 won 11 of 12 pairs across both orders. The shorter checker-trial drafts dropped checks the task needed. The migration draft compared summed test counts, not each file's test names and assertions, so weakened tests could pass, and it lost its DONE WHEN heading. The feature draft never checked that the Export button sends the filter state. The audit found nothing missing that it counted as essential, so the loss is in how hard the checks bite, not in missing sections.
- The checker trial was not shipped. The likely culprit is the length aim, not the checker; a fix that deletes a check also removes its conflict.

Round 10 tested v6, the merged skill. As in rounds 8 and 9, a subagent drafted each prompt from the same README and request, so the v6 drafts compare directly with round 8's v5 drafts; `claude -p` was not tried, because it had failed earlier the same day with an expired login. A drafter has no shell and cannot start a subagent, so the lead ran steps 9 and 10 for it: `check_prompt.py` on each draft, with the request and README as sources, and one fresh Sonnet reviewer that read only the draft, the request, the README and the skill. The feature drafter judged its prompt one slice with no decision log, so step 10 did not apply. The drafter fixed the check's findings and the reviewer's blockers once, and the check ran again on the final text.
- **The check and the review did their job.** `check_prompt.py` found a FAIL in 4 of 6 first drafts: unresolved relative terms ("the owner", "tonight", "today") in four, and two gaps on one UNKNOWN line in one. No final draft has a FAIL. The five reviews named 13 blockers, among them a merge rule that accepted any green check instead of the test job, and a NEEDS A HUMAN path that let a run merge nothing and still pass.
- **Quality tied v5.** Two fresh Opus reviewers saw the same six pairs in opposite orders. v6 won 6 of 12, 7.5 against 7.6 on average. Both reviewers chose Draft X in 5 of 6 pairs, so position decided bugfix, feature, migration and research. Only overnight (v6 both times: it requires the named test job to pass on the head SHA and parses versions as JSON) and refactor (v5 both times: it proves the move was verbatim) held in both orders. The checker trial lost 11 of 12 against the same v5 drafts.
- **Fewer contradictions, no shorter.** A third Opus reviewer audited all 12 drafts one at a time and found 3 contradictions in v6 against 7 in v5; pairwise reviewers counted 19 against 20. Neither arm left out anything essential. v6 drafts ran 85 to 137 lines against 84 to 147, so the merge did not make them shorter. The audit rated v6 more over-specified, 14 against 11 of 18, and both pairwise reviewers named inline `ASSUMED` tags on every figure as noise.

Round 11 tested v7 by round 10's method: Sonnet drafters, and the lead ran `check_prompt.py` and one fresh Sonnet review for each draft that called for one, using v7's three review questions. Each drafter fixed the findings once, and the check ran again on the final text. The feature and research drafters judged their prompts one slice with no decision log, so step 10 did not apply.
- **A little shorter.** The six final drafts total 13,177 words against 14,089 for v6 (6.5% fewer) and 602 lines against 627. `ASSUMED` tags fell from 100 to 63. Four drafts got shorter (research went from 137 to 105 lines); bugfix and migration got longer, mostly from lines added to fix review blockers. The new c-7 flags a figure marked twice in 5 of 6 v6 drafts and 2 of 6 final v7 drafts.
- **Quality tied v6.** v7 won 7 of 12 across both orders, 7.5 against 7.5 on average. Draft X won 9 of 12, so position decided feature, research and migration. Bugfix (the reset's real token issuance, and a commit from before the bug) and refactor (a proof that the code moved verbatim) went to v7 in both orders, and overnight (the named test job on the head SHA) to v6 in both.
- **On contradictions the reviewers disagree.** The pairwise reviewers quoted 4 conflicts in v7 against 6 in v6. The one-at-a-time audit found 11 in v7 against 4 in v6, and rated over-specification level at 11 of 18 each. Several of v7's conflicts sit in lines added while fixing review blockers, such as wait caps that overrun the budget. Audits of the same drafts have varied by about 3 (v5: 10 in round 8, 7 in round 10); this gap is larger, and it is v7's open risk.

Round 12 tested v8 under the measurement frozen before any v8 code changed (commit d445060): the briefs in [briefs/](briefs/README.md), the playbook rubric, the [must-haves](must-haves.md) and v7's round-11 drafts as [baselines](baselines/README.md). Drafting and review followed round 11. v8 failed four of its gates, so it was archived and v7 restored, as the plan required.
- **Shorter, but weaker.** The six drafts total 9,115 words against v7's 13,177. Feature fell from 75 lines to 29. Blind reviewers preferred v7 in 11 of 12 pairs, 8.1 against 7.0, and v7 held in both orders in five scenarios. Feature fell 2.5 points and refactor 1.5.
- **Must-haves lost.** A blind reviewer checked each draft against the must-haves list. v8 lost one that v7 had in five of six scenarios: the real token path (bugfix), proof the export carries the page's filter (feature), per-file test names and assertions (migration), a verbatim-move proof (refactor) and a decision rule (research). This is round 9's failure again: a shorter draft drops the checks that made the longer one win.
- **The audit.** 6 contradictions in v8 against 4 in v7, with one v8 draft missing something essential; over-specification fell from 14 to 8 of 18. The same v7 drafts drew 11 contradictions in round 11's audit, so audit counts swing widely.
- **Scores rose anyway.** Scored blind against v7 in the same run, v8 reached 66% on the playbook rubric against 55%, and 91% on the external sources against 75%. Rubrics that count rules present do not predict which prompt a reader prefers; the blind comparison and the must-haves are what caught the drop.

Round 13 tested v9 by round 12's method, under the same frozen measurement, with one change the plan allowed: rubric R7 is N/A for the small-fix dry run (Dump 1). v9 kept v8's playbook-backed rules and restored what v8 dropped: Templates B and L's sizes, Template B's trivial form, and a rule that each check names the likeliest way the result could be faked and fails on it. It failed five gates, so it was archived and the three v9 commits were reverted together.
- **A probe passed first.** Before the full run, a blind reviewer checked the feature and migration drafts, reviewed, against v7's. v9 lost no must-have, and it gained M1 (per-file test names) on migration.
- **Readers still preferred v7.** v7 won 7 of 12 pairs, 7.7 against 7.2. Feature fell 2.0 points and bugfix 1.5, past the 1-point limit; refactor and research rose 1.0. The reviewers' reasons were mostly contradictions between a check and a constraint, such as "`npm test` exits 0" beside "do not fix those failures".
- **One must-have lost.** The research draft gave a baseline need but no rule for choosing between options that meet it (R2), which v7's draft had. F2 and O1 were missing from both versions.
- **More contradictions, not shorter.** The audit counted 12 contradictions in v9 against 8 in v7, with no draft missing anything essential; over-specification was 10 against 12 of 18. The drafts totalled 11,881 words against 13,177, 10% fewer, so length alone does not explain the loss.
- **Scores rose again.** In the same scorer runs, v9 reached 67% on the playbook rubric against 59%, and 88% on the external sources against 76%. As in round 12, coverage rose while blind preference fell.

Round 14 tested v10: v7 plus six items the playbook requires, each its own commit (R1 Template L's risk sizes and Template B's trivial form with check c-9; R2 a fresh diff review at normal and high risk; R3 a named gate for each hard constraint at high risk; R4 briefs that say what is ruled out and decided; R5 idempotent, least-privilege, capped loops; R6 plan files in `docs/plans/`). Plan: [docs/plans/prompt-v10.md](../../../docs/plans/prompt-v10.md). Measurement as in round 12, with rubric R7 N/A for Dump 1. Drafts got step 10's review only where the skill called for one, as in round 11. Every number below cites a file in [round14/](round14/README.md), which maps each one to its source.
- **Noise first.** A fresh v7 trial (T2) scored 1.54 below round 11's v7 drafts (T1) and lost 10 of 12 pairs, so the round-11 drafts were not a fair baseline. A second fresh v7 trial (T3) against T2 gave the margins the gates use: pairs 0.25, worst scenario 2.0, audit 2 contradictions, must-haves 3.
- **v10 beat v7.** Against T2 and T3, v10 won 19 of 24 judgments, 7.79 against 7.00. No scenario fell below v7's mean: bugfix 7.5 against 7.25, feature 8.0 against 6.5, migration 7.75 against 7.25, overnight 8.0 against 6.75, refactor 8.0 against 6.75, research 7.5 against 7.5.
- **Must-haves held.** No must-have present in both v7 trials was missing from both v10 trials. F2, R2, RF2 and O1 were missing from every v7 and v10 draft alike.
- **The audit was close.** 8 contradictions in U1 against 3 in T2, and 7 in U2 against 9 in T3: a mean gap of 1.5 against a margin of 2.
- **An outside judge saw a tie.** Codex (a different model family), given the same blinded pairs and frozen brief, scored v10 6.58 against v7 6.63 and gave v10 10 of 24 wins; it agreed with Claude's winner in 13 of 24 judgments, about chance. On the dry runs it gave v10 16 failures against 19 for fresh v7. Under the rule fixed before it ran, this confirms the ship (no regression) but does not support "better": the 79% win rate depends on the judge. Files: [round14/codex/](round14/README.md).
- **D3 did not ship.** A rule that each check names its likeliest fake won the bugfix and refactor probe (7.75 against 7.25) but over all six scenarios scored 7.58 against the bundle's 7.42, inside the margin. It is archived in [variants/](variants/README.md).
- **Two prompts were run.** One v10 feature prompt and one bugfix prompt were run to completion on a small Node app by fresh agents. A fresh grader ran hidden acceptance tests the agents never saw: the feature run passed H1 to H4 (header, filtered rows, empty filter, CSV escaping) and the bugfix run H5 and H6 (the reset's session stays valid; old password and older sessions end). Neither receipt claimed a PASS that failed. Both marked their review steps NOT RUN, since an executor cannot start a subagent. The bugfix agent, refused the Edit tool by a hook, made its edit through Bash instead: a guard worked around, which the run's receipt does not hide and which a real setup should deny at the shell too (Law 9).

v1 lost overnight, research and migration. The reviewer cited a self-contradicting unattended prompt that committed a report file nightly, helper briefs that left rows of their own comparison unasked, and one writer for 400 files.

## Rubric (score.py, 67 applicable checks across the six scenarios)

| Round | Skill | Skill score | Baseline score (strict) | Baseline score (lenient) | Saved in the guide, nothing in the project |
|---|---|---|---|---|---|
| 1 | v1 | 64 | 24 | 28 | (saved in the project; v1 behaviour) |
| 2 | v1 | 63 | 23 | 27 | (same) |
| 3 | v1 + save step | — | — | — | 1 of 6: the throwaway guide repo was on its default branch, and a worktree hook blocked the write. The harness was fixed to use a work branch |
| 4 | v2 | 67 | — | — | 6 of 6 |
| 5 | v3 | 65 | — | — | 6 of 6 |
| 6 | v4 | 67 | — | — | 6 of 6, and no session-only paths in any draft |
| 7 | v4 | 64, 66 after the scorer fix | 25 | 29 | 6 of 6 saved, nothing written in any project. Two of the three misses were the scorer: it read "`git status` is clean" as a vague adjective, and missed a per-writer gate worded differently. The third, no explicit step reconciling helper findings in research, is real |
| 9 | Checker trial (v5 alongside) | 60 (v5: 59) | — | — | Drafted by subagents with a separate checker. Shorter drafts; the rubric moved little |
| 10 | v6 (v5 alongside) | 62 (v5: 59) | — | — | Drafted by subagents; the lead ran steps 9 and 10. v6 gained on feature, refactor and migration and lost 2 on research |
| 11 | v7 (v6 alongside) | 60 (v6: 62) | — | — | Drafted by subagents; the lead ran steps 9 and 10. v7 gained 3 on research and lost 5 across feature, refactor and migration |
| 12 | v8 (v7 alongside) | 65 (v7: 60) | — | — | Not shipped: the rubric rose while blind reviewers and the must-haves check preferred v7 |
| 13 | v9 (v7 alongside) | 58 (v7: 60) | — | — | Not shipped: five gates failed (pairs, scenarios, must-haves, audit, dry run) |
| 8 | v5 (v4 alongside) | 59 (v4: 66) | 34 | 38 | Drafted by subagents, so nothing was saved. v5's misses are mostly format: it nests sub-bullets under DONE WHEN checks, which the regex counts as extra checks, and two drafts run past 120 lines |

The rubric is drawn from the same playbook as the skill, so read it as "the playbook's practices reached the prompt", not as an independent quality score. Its regex checks missed correct wording several times, for example "stop condition:", "fails twice" and "green between batches". Each pattern was widened, and every round and both arms were re-scored with the same scorer. A later review of the scorer found two checks too loose: p-3 counted any digit as a runnable check ("done within 2 days"), and p-18 passed on any "never" or "do not". Now p-3 needs a command, a scenario, a counted result or an observable outcome, and p-18 needs a ban that names an irreversible action. Re-scored with the tightened checks, only round 2's v1 draft changed (64 to 63), and no baseline score moved. The two misses left in round 5 were real: 6 checks instead of 5, and no integration step. v4 fixed both.

## Interview check ([interview.sh](interview.sh))

A vague request ("I want search in our notes service to be better") passed all 8 checks. The skill looked at the project first, reported PostgreSQL instead of asking about it, asked one question with 4 options and the recommended one first, and wrote nothing.

## Limits

- Six scenarios; one writer model (Sonnet) and one reviewer model (Opus), both Claude.
- Baselines differ between reviews, so part of each gap is run-to-run variation.
- The scorer was fixed after round 7: "`git status` is clean" is no longer read as a vague adjective, and a writer that runs only its own files counts as a batch gate. Round 7 was re-scored; earlier rounds were not.
- v4 has passed the rubric (rounds 6 and 7) and blind review 4. In round 7 the scratch folders sat inside a git repository, so 4 of 6 saves named the project after that repository instead of the folder; that is the test setup, not the skill.
- Only two generated prompts have been run to completion (round 14, one small app, hidden tests). A wider task suite with gates (§13) is still needed to say whether better prompts produce better code.

## Reproduce

```bash
tests/live/prompt/run.sh <work dir> <round>
```

`ARMS=skill` runs only the skill arm. Then score a draft:

```bash
python3 -I tests/live/prompt/score.py tests/live/prompt/scenarios.json <id> <draft.md>
```

`interview.sh <work dir>` runs the interview check. Each needs the `claude` CLI, signed in.
