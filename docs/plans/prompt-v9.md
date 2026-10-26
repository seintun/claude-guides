# /prompt v9 Implementation Plan

> **Outcome (2026-10-25):** built and measured as planned, then rolled back. v9 failed five gates: v7 won 7 of 12 blind pairs (7.7 against 7.2), feature and bugfix fell more than 1 point, the research draft lost must-have R2, the audit found 12 contradictions against 8, and the dry run gave 13 failures in 60 against 6. The wave 3 probe, the size gate and both scores passed. v9 is archived in [tests/live/prompt/variants/](../../tests/live/prompt/variants/README.md), its three commits were reverted together, and v7 stays shipped. Results: [tests/live/prompt/results.md](../../tests/live/prompt/results.md) round 13 and [tests/live/grill-prompt/results.md](../../tests/live/grill-prompt/results.md) round 7.

> **For agentic workers:** Implement this plan wave by wave, in order. Before you claim a wave is done, run its gate and record the result. NOT RUN is not PASS.

**Goal:** Ship `/prompt` v9: the v8 changes the playbook supports, plus the decisive checks v8 dropped. v9 passes every gate in [prompt-v8.md](prompt-v8.md) Task 5 against v7, under the measurement frozen at commit d445060. If it fails one, v7 stays shipped.

**Risk:** high. It changes the skill, its check, its tests and guarded files, and spends up to 42 subagent runs.

**Why v8 failed, and what v9 changes.** v8 raised the rubric scores and cut draft words by 31%, but it failed four gates ([results.md](../../tests/live/prompt/results.md) round 12, [grill-prompt results](../../tests/live/grill-prompt/results.md) round 6):
- **Pairs:** blind reviewers preferred v7 in 11 of 12.
- **Must-haves:** v8 lost one in 5 of 6 scenarios.
- **Audit:** 6 contradictions against v7's 4 in one audit run, and one v8 draft missing something essential.
- **Dry run:** 7 failures in 60 against v7's 2. v8's were R6 twice (small task, report), R1 and R5 (report), and R7 three times: once on the small task and twice on the large project.

v9 starts from the archived v8 ([variants/SKILL-v8.md](../../tests/live/prompt/variants/SKILL-v8.md)) and fixes the four causes the prompt names (D1 to D4), plus D7, which the user added at sign-off after the dry-run gate was found to be the likeliest to fail. D7 came after both critic rounds, so no critic has read it:

| Finding | Cause in v8 | v9 change | Playbook |
|---|---|---|---|
| D1 | Its own scale: `low` meant "one slice, easy to undo", so the CSV-export feature was sized low and lost its review and its filter check | `Risk: trivial \| normal \| high`, set by Template L's rule: what the work touches, new dependencies, schema or auth. A change to user-visible behaviour is never trivial. When the rule and a person disagree, the higher wins | Templates B and L |
| D2 | The low form dropped BUDGET, STOP AND ASK and HOW TO WORK | The trivial form keeps every Template B part: GOAL, RISK, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT. Only CONTEXT is optional | Template B, §5.3 |
| D3 | No rule protected the check that made each longer draft win | Each DONE WHEN check names the likeliest way the result could be faked or fall short, and fails on it. The step-10 reviewer gets a fourth question: which check could pass while the GOAL is unmet? | §9.3, Law 3 |
| D4 | A 20-line example and "start minimal" steered every draft shorter | Length follows risk, and no check is cut to save lines. The example is linked for trivial prompts only | G4 in [prompt-skill-sources.md](../../research/prompt-skill-sources.md) |
| D7 | v8's dry-run failures that count under the R7 rule: a problem's cost left unmarked (R7, twice, large project), a DONE WHEN check whose scope differs from the decision log (R6, twice), an invented example figure in a check (R1) | Any part of CONTEXT you can't fill is an `UNKNOWN` line. The consistency pass checks every DONE WHEN line, not only CONSTRAINT and BUDGET, against the GOAL and the decision log, and matches each check's scope to the log's. An example inside a check uses a placeholder, not an invented value | Law 3, §9.3 (R5's undefined term is already covered by "No check rests on ... an undefined term") |

Two more findings are test-side and change no skill code:
- **D5, rubric R7.** [rubric.md](../../tests/live/grill-prompt/rubric.md) asks every dry run for a problem and a riskiest assumption. §5.3 and Template B ask a small fix for only a goal, checks and a receipt. Slice (a) makes R7 N/A for every run of Dump 1, the one-hour help-text fix. The rule keys on the request, not on any label in the prompt, so it applies to v7's and v9's runs alike. This is the only change to the measurement.
- **What D1 to D5 leave open.** The prompt's D5 reads v8's R7 failures as trivial-size runs, but only one of the three was on the small task. Slice (a) removes v7's only R7 failure (run 1a), so v7's regraded total is likely 1, and the dry-run gate then asks v9 for at most 1 failure in six runs. D1 to D4 target none of v8's six remaining failures (R7 twice on the large project, R6 twice, R1, R5), and run-to-run noise is about 3 (two sets of v7 scored 3 and 0 in round 5). The judge's evidence for those six is in the round-6 grades: "what it costs them is not stated" with no marker; a check covering "the export flag only" against a log that says every flag; a check counting per file against a log that rates per item; "$4,000 a month" picked by the writer; and an undefined "first page". The user chose D7 to target the first three causes, and kept the gate unchanged. The plan adds no early dry-run probe: it would need a third brief and a stop rule the prompt does not define.
- **D6, the score gates.** The scorers are LLM judges counting rules (§9.3: never the only gate). Their scores rose while quality fell, so they guard coverage only. The quality gates are the blind pairs, the must-haves, the audit and the dry run.

v8's playbook-backed gains stay: a risk line above the title, checked in code; GOAL first; each chosen figure marked once; the delegation rules in a file read on demand (G29); a fresh reviewer at normal risk (§9.3); a named enforcing gate for each hard constraint at high risk (Law 9); idempotent, least-privilege, capped loops (§11.3, Template H); plan files in `docs/plans/` (Template B); "report a wrong test" and "stop when done"; the reviewer's three questions.

## Global constraints

- The measurement is the one committed at d445060: the briefs in `tests/live/prompt/briefs/`, `rubrics/playbook.md`, `must-haves.md`, and both `baselines/v7/` folders. The only change is the R7 rule in slice (a). Any other change to the measurement stops the work and asks the user.
- Tests are immutable to the builder, apart from new pins and new review edits. A pin or review edit whose target sentence moves follows that sentence's new wording in the same commit, and still damages the same rule. Never weaken or delete a test or a review edit.
- `tests/run.sh` ends with `SUMMARY all PASS` after each slice. `python3 -I tools/check_privacy.py` passes before each commit. Stage only this plan's files; another session may share the checkout.
- Commit on `feat/guide-entry`; push nothing. No AI attribution in commits.
- `skills/prompt/SKILL.md` is at most 1,900 words (`wc -w`). The draft below measures 1,895.
- At most 42 subagent runs in all. An unread gate counts as failed.

## Review focus

1. **No teaching to the test.** The decisive-check sentence names no example, because any example drawn from D3's list would restate a must-have (B2, M1, F2). The trivial example in step 3 is "a typo or a wrong comment", not help text (dry-run Dump 1). `example.md` answers a task in neither `dumps.md` nor `scenarios.json` (a README link fix), with its own request file for the check test, so no runner reads an answer to its own request.
2. **The fourth question and the frozen reviewer brief.** `briefs/reviewer-round1.md` asks the step-10 reviewer three numbered questions and is frozen. In the evaluation the fourth question reaches the reviewer only through SKILL.md, which the brief tells it to review against. Changing the brief would be a second measurement change, so it stays as committed.
3. **The request suffix.** Every battle request ends "list your assumptions at the top" (`tests/live/prompt/run.sh`), while v8 and v9 put the ASSUMPTIONS list after REPORT and fail it above GOAL (c-10). The inputs stay unchanged, as v8's did, so v9 meets the same tension v8 met.
4. **Half a revert.** Slices (b) and (c) only work together: v7's SKILL.md writes no risk line, which the slice (b) check fails. An agreement test ties them, and a rollback reverts all three slices together.
5. **A thin margin.** SKILL.md is 5 words under its cap. A blocker fix that adds words must cut as many.

## Wave 0: plan, critic, sign-off

- Write this plan from the prompt's CONTEXT.
- One fresh critic (`adversarial-reviewer`) reads this file and the files it links, not the lead's reasoning, and returns up to 3 blockers with evidence. A second round reads only the fix diff, for open and new blockers. Only a blocker with evidence reopens the plan; after two rounds the user decides. Cost: up to 2 runs.
- **Gate:** blockers answered, and the user signs off in chat. Then commit this plan on its own: "Plan /prompt v9: v8's gains plus the checks it dropped".

## Wave 1: three slices, tests first, each committed

Each slice: write the failing tests, run `tests/run.sh` and see them fail, implement, run `tests/run.sh` to `SUMMARY all PASS`, run `python3 -I tools/check_privacy.py`, commit. No subagent runs.

### Slice (a): the R7 rule and its pin

Files: `tests/live/grill-prompt/rubric.md`, `tests/test_prompt_skill.py` (`LiveKit`), `tests/baselines/suite.json` (floor +1).

- Test first, in `LiveKit`:

```python
    def test_r7_is_na_for_the_small_fix(self):
        """§5.3 and Template B ask a small fix for a goal, checks and a receipt only, so R7 can't fail it (v9 plan, D5)."""
        rubric = (ROOT / "tests" / "live" / "grill-prompt" / "rubric.md").read_text(encoding="utf-8")
        r7 = next(l for l in rubric.splitlines() if l.startswith("| R7 "))
        self.assertIn("N/A for every run of Dump 1", r7)
        self.assertIn("who struggles, what it costs", r7, "R7 must still apply to Dumps 2 and 3")
```

- Change the R7 row's PASS-when cell to: "The output states the problem (who struggles, what it costs) and the riskiest assumption with a cheap test. N/A for every run of Dump 1, the small fix that §5.3 and Template B ask only for a goal, checks and a receipt". The rule names the request, not a size label, so v7's and v9's runs are judged alike.
- Commit: "Make rubric R7 N/A for the small-fix dry run, as §5.3 and Template B size it".

### Slice (b): the check learns the trivial vocabulary and the trivial form

Files: `skills/prompt/check_prompt.py`, `skills/prompt/example.md` (new), `tests/fixtures/prompt-check/example-request.md` (new), `tests/fixtures/prompt-check/good.md`, `tests/test_prompt_skill.py` (`PromptCheck`), `tests/mutation/review_edits.py` (edits 64 to 66), `tests/README.md` (count 63 to 66), `tests/baselines/suite.json`, `skills/prompt/README.md` (example row, check description), `llms.txt` (check line, example line).

Start from v8's check ([variants/check_prompt-v8.py](../../tests/live/prompt/variants/check_prompt-v8.py)), with these changes:
- `RISK` matches `trivial|normal|high`. "Risk: low" no longer counts, so c-9 FAILs it with "add 'Risk: trivial', 'Risk: normal' or 'Risk: high' above the title".
- `TRIVIAL_PARTS = [p for p in PARTS if p != "CONTEXT"]`, and `needed = TRIVIAL_PARTS if risk == "trivial" else PARTS`. v8's `LOW_PARTS` and `HELPERS` go: the trivial form keeps BUDGET and HOW TO WORK anyway.
- The docstring's c-1 line: "every part the risk level needs is there: trivial may leave out CONTEXT; normal and high need all eight". c-9, c-10, the c-6 and c-7 fix hints and the `15 lines` skill value as in v8.

Tests first. The parser fix `(c-\d)` to `(c-\d+)` in `check()`; `["PASS"] * 8` to `["PASS"] * 10` in the three tests that count; `Risk: normal` on the fixture's line after its title. New tests, each building its own copy of the fixture:
- `test_trivial_may_leave_out_context`: the fixture without CONTEXT passes c-1 at `Risk: trivial` and fails it at `Risk: normal`.
- `test_trivial_keeps_template_b_parts`: at `Risk: trivial`, removing BUDGET, STOP AND ASK IF or HOW TO WORK (each in turn) fails c-1 and names the part. This is D2.
- `test_old_low_label_fails_c9`: `Risk: low` fails c-9 only.
- `test_missing_risk_line_fails_c9`, `test_risk_line_ignores_case_bold_and_bullets` (`**Risk:** High`, `Risk: TRIVIAL`, `risk: normal`, `- Risk: trivial`, `RISK: normal`), `test_marked_line_above_goal_fails_c10`, `test_banner_review_line_and_risk_above_goal_pass_c10` and `test_skill_set_output_cap_is_not_a_guess`, as in v8.
- `test_example_prompt_passes_every_check`: `example.md` exits 0 with 10 PASS lines, says `Risk: trivial`, and stays at most 30 lines.

`skills/prompt/example.md` answers a request in neither `dumps.md` nor `scenarios.json`. Its source for the check test is a new fixture, `tests/fixtures/prompt-check/example-request.md`:

> The install link in our README still points at the old docs site and gives a 404. Point it at the current install page. Ten minutes of work.

`check()` in `PromptCheck` gains an optional `source` argument (default: the existing request fixture), so only the example test reads the new fixture. The example, which the scratch build of the v9 check passes with 10 PASS lines in 25 lines:

```markdown
Risk: trivial

# Prompt: point the README's install link at the current install page

GOAL: The install link in README.md opens the current install page.

DONE WHEN:
1. Given README.md, when you fetch the install link's URL exactly as the file writes it (`curl -sIL <url>`), then the last response is a success, not a 404. Read the URL from the file, not from your notes, so a link fixed only elsewhere can't pass.
2. Given the same file, when you search it for the old docs host, then it finds nothing.

CONSTRAINTS:
- Edit only that link in README.md.
- A test that looks wrong is reported, not edited.
- When both checks pass, stop and report; add nothing else.

BUDGET: ten minutes, no helpers.

STOP AND ASK IF: you can't find the current install page, or other files link to the old docs host.

HOW TO WORK: build, verify, report.

REPORT: each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.

ASSUMPTIONS:
- UNKNOWN: the current install page's URL; the request doesn't give it, so find it on the docs site first.
```

Review edits, each must be CAUGHT (`python3 -I tests/mutation/review_edits.py 64 65 66`):
- 64: `needed = TRIVIAL_PARTS if risk == "trivial" else PARTS` becomes `needed = ["GOAL", "DONE WHEN", "CONSTRAINTS", "REPORT"] if risk == "trivial" else PARTS`, v8's short form (D2).
- 65: c-10 always PASS. 66: c-9 always PASS.

Commit: "Teach /prompt's check the trivial size and Template B's trivial form, and add a trivial example".

### Slice (c): SKILL.md v9, delegation.md, pins and the decisive-check edit

Files: `skills/prompt/SKILL.md`, `skills/prompt/delegation.md` (new, v8's text unchanged), `tests/test_prompt_skill.py` (`SkillRules`), `tests/mutation/review_edits.py` (edit 62 retargeted, edit 67 new), `tests/README.md` (66 to 67), `tests/baselines/suite.json`, `skills/prompt/README.md` (delegation row), `llms.txt` (delegation line).

SKILL.md v9 is the archived v8 with its links pointed at `example.md` and `delegation.md`, and these replacements (built and measured by a script, 1,895 words):
- **Step 3 (D1, D2, D4).** v8's sizing sentence and Low bullet become:
  > 3. **Size it by risk, and write the result above the title as `Risk: trivial`, `Risk: normal` or `Risk: high`.** Set it by a rule, not by feel (Template L). High: the work touches a schema, auth, payments, data deletion, a public API, infrastructure or production, adds a dependency, or runs unattended. Trivial: a small fix in one place, easy to undo, with no helpers or loop, such as a typo or a wrong comment. A change to user-visible behaviour is never trivial. Normal: everything else. When two sizes apply, or the rule and a person disagree, the higher wins. Length follows risk, and no check is cut to save lines.
  >    - Trivial: GOAL, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT; CONTEXT is optional. No plan file. For trivial prompts only, see `[example.md](example.md)`.
- **Step 5, DONE WHEN (D3).** `For each, ask "could this pass while the goal is unmet?" and tighten it.` becomes: "For each check, name the likeliest way the result could be faked or fall short, and make the check fail on it." It gives no examples: any drawn from D3's list would restate a must-have.
- **D7.** CONTEXT ends: "Any part you can't fill is an `UNKNOWN` line." Step 8's Contradictions bullet reads "check every DONE WHEN, CONSTRAINT and BUDGET line against the GOAL and the decision log, and match each check's scope to the log's." The figure rule adds "; an example inside a check uses a placeholder, not an invented value".
- **Step 10 (D3).** "three questions" becomes "four questions", and "Which check could pass while the GOAL is unmet?" follows the third.
- **Cuts to stay under 1,900 words**, none of them a rule: the opening names Template L; step 1 drops "so the prompt can point to a pattern to copy" (CONTEXT still asks for it); step 11 drops "Prompts stay out of the project's repository." and "That folder is git-ignored, so prompts never reach either repository."; step 3's Normal bullet drops "the source of truth"; step 12 drops "so the user confirms them knowingly"; CONTEXT says "(a grill's decision log)"; the figure rule's examples shrink to "such as a cap or a retry count"; DONE WHEN drops "more dilute attention, so"; step 11's guard reason shrinks to "which a guard may otherwise refuse"; the last rule reads "Write for the target project: name no agents, skills, environment variables or house rules it doesn't define."

Tests first, in `SkillRules`:
- `SKILL_ALL = SKILL + delegation.md` (guarded with `.exists()`), read by `test_keeps_every_rule`.
- v8's pins, with `low` read as `trivial`: user input tagged, fresh reviewer at normal risk, enforcement named at high risk, plan file in the repo, example to copy, delegation rules loaded, wrong tests reported, stop when done, briefs carry what is settled, options judged alike, idempotent loops, least privilege unattended, capped loop output, recheck after fixes, high risk ends with a person, top of the prompt ordered. "self-chosen values marked" follows its rule to "once under ASSUMPTIONS, after REPORT, as `ASSUMED: <text>`, and each gap there as `UNKNOWN: <why>`".
- New pins for D1 to D4, verbatim: "write the result above the title as `Risk: trivial`"; "Set it by a rule, not by feel (Template L)."; "A change to user-visible behaviour is never trivial."; "When two sizes apply, or the rule and a person disagree, the higher wins."; `Trivial: GOAL, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT`; "Length follows risk, and no check is cut to save lines."; `For trivial prompts only, see [example.md](example.md).`; "name the likeliest way the result could be faked or fall short"; "and make the check fail on it."; "Which check could pass while the GOAL is unmet?"; and for D7, "Any part you can't fill is an `UNKNOWN` line.", "match each check's scope to the log's" and "an example inside a check uses a placeholder, not an invented value".
- `test_runs_the_consistency_pass_before_saving` pins v8's five bullets (Files, Counts, Paths, Data, Contradictions), as v8's Task 4 did. Three v7 bullets (Targets, Evidence, Caps) live on in other sentences, so their pins follow them there rather than go: "A check on CI, a deploy or a PR reads the exact commit, run or PR the steps produced", "caps leave room for every field asked for" and "each claim the decision rests on carries quoted wording, not just a link". Each of the nine v7 bullets keeps a pin.
- `test_skill_stays_lean`: SKILL.md is at most 1,900 words.
- `test_skill_and_check_change_together`: "`Risk: trivial`" is in SKILL.md exactly when "c-9" is in `check_prompt.py`.

Review edits:
- 62 is retargeted to the four-question sentence. It still deletes every reviewer question and the stop-condition test, so it damages the same rule.
- 67 (new, the deliberate break): delete the decisive-check sentence from SKILL.md. `python3 -I tests/mutation/review_edits.py 67` must report CAUGHT.

Commit: "Make /prompt v9: Template L's sizes, Template B's trivial form, and a decisive-check rule".

**Gate to wave 2:** `tests/run.sh` all PASS after each slice; three commits; the v9 skill folder (SKILL.md, delegation.md, example.md, check_prompt.py) copied to `<scratch>/v9/skill/`. No repository edits after this until wave 6.

## Waves 2 to 5: the evaluation

Every helper is a fresh subagent with a brief naming its objective, the only files it may read, its output file in `<scratch>` and when it stops. Helpers are read-only on the repository; drafters and runners write only in their own `<scratch>` folder. Inside a wave, helpers start together in one message. The briefs are the frozen templates in `tests/live/prompt/briefs/`, filled with paths; drafter and runner briefs follow round 12's (one-file README "Node 20 service with a Postgres database. Run the tests with `npm test`. Deploys from main through GitHub Actions.", the scenario text plus "Skip any questions and draft the prompt now; list your assumptions at the top.", and the dry-run method in `tests/live/grill-prompt/README.md`). Models as in round 12: Sonnet drafters, runners, step-10 reviewers and playbook scorer; Opus pairwise reviewers, audit, must-haves reviewer, external scorer and judge.

| Wave | Work | Gate | Runs |
|---|---|---|---|
| 2 | Both mutation suites in the background. Two probe drafters (feature, migration) with the copied v9. Each probe draft runs its full pipeline here: step 9's check, the step-10 review the skill calls for, one fix round, and the check again on the final text. The two reviews are the ones wave 4 would have run, so the total does not change. The lead continues each drafter at least once, so the continuation assumption is tested before wave 3 | Mutation suites: 0 NOT CAUGHT, 0 EDIT FAILED. Both final drafts with no FAIL from the check. A drafter that can't be continued stops the work and asks, with the extra runs it would need | 2 drafters, up to 2 reviews moved from wave 4 |
| 3 | One must-haves reviewer reads the two final, reviewed v9 probe drafts and v7's two baselines for the same scenarios, blinded D01 to D04 in random order. It uses a scratch copy of `briefs/must-haves.md` in which "the twelve files D01.md to D12.md" reads "the four files D01.md to D04.md"; the committed brief is unchanged | No must-have ABSENT in a v9 draft where v7's has it PRESENT. A loss stops the work before wave 4: archive, revert the three slices together and report, because the prompt counts the probe among the gates and v9 is the live `/prompt` while it stays committed | 1 |
| 4 | Four more drafters (bugfix, overnight, refactor, research) and six dry-run runners (two per request). The two probe drafts continue. Each new item runs its own pipeline: draft, step 9 check, step-10 review if the skill calls for one, one fix round, the check again on the final text; dry runs get a second review round | Six final battle drafts and six final dry runs, none with a FAIL from `check_prompt.py` | 4 drafters, up to 4 battle reviews, 6 runners, up to 12 dry-run reviews |
| 5 | The lead builds the blind sets (path, version, risk-line and review tells removed; keys in files no reviewer reads). Then together: two pairwise reviewers (one per order), the audit, the must-haves reviewer, the playbook and external scorers, and the dry-run judge | Every gate below read from a reviewer's file | 7 |

Wave 5 inputs:
- **Pairs and audit:** v9's six final drafts against `tests/live/prompt/baselines/v7/`, as round 12 built them. The must-haves reviewer reads the same twelve blinded drafts with `tests/live/prompt/must-haves.md`.
- **Scorers:** Skill A and Skill B at random. v7 is SKILL.md at d445060 with its baseline samples (feature, overnight, migration, and dry-run run-2a's prompt); v9 is the copied skill folder with its own four samples for the same tasks.
- **Judge:** the six v9 runs and the six v7 baseline runs, blinded J01 to J12, with `rubric.md` as committed in slice (a) and `dumps.md`. One judge regrades both versions under the R7 rule in the same run. The frozen judge brief asks for PASS or FAIL; the results record how the judge marked R7 on Dump 1 (N/A or PASS), and either counts as no failure. A FAIL on R7 for a Dump 1 run is recorded as the judge wrote it and reported to the user, since the rubric says N/A; the lead does not regrade it.

## The gates (no waivers)

| Gate | Passes when | Read from |
|---|---|---|
| Pairs | v9 wins at least 6 of 12 judgments (a tie is not a win), and v9's mean score over the 12 is at least v7's | the two pairwise reviewers' replies, saved to `<scratch>` |
| Scenarios | In each scenario, v9's mean over the two orders is no more than 1 point below v7's | the same files |
| Must-haves | No must-have PRESENT in v7's draft and ABSENT in v9's for the same scenario | the must-haves reviewer's file |
| Audit | In the one audit run, v9's contradictions are no more than v7's, and no v9 draft is marked missing something essential | the audit reply |
| Dry run | Under the one judge, v9 fails no more than v7; each set of 3 v9 runs fails at most 9 of 30; no final v9 prompt has a FAIL from `check_prompt.py` | the judge's file, and the lead's check outputs |
| Scores | In the same scorer run, v9 is at least v7 on both the playbook score and the external overall, and at least 5 points higher on one. Coverage only | the two scorers' files |
| Lean | SKILL.md at most 1,900 words; six final battle drafts, each with a GOAL and at least two DONE WHEN checks, totalling at most 13,177 words | `wc -w`, and the lead's count |

## Wave 6: apply the gates, and review the diff

- If every gate holds, keep the wave 1 commits. If any gate fails or goes unread, at any wave: archive v9 as `tests/live/prompt/variants/SKILL-v9.md`, `example-v9.md` and `check_prompt-v9.py` (delegation.md is v8's, already archived), `git revert` the three slice commits together, and report.
- A fresh agent reviews the final diff (from f517ac4 to HEAD) against the DONE WHEN list, even when the tests pass. Only a blocker with evidence reopens it, a re-review reads the fix diff for open and new blockers, only the reviewer or the user closes a blocker without a fix, and after two rounds the user decides. Cost: up to 2 runs.

## Wave 7: record and commit

- Write the numbers and reviewer quotes into `tests/live/prompt/results.md` (round 13), `tests/live/grill-prompt/results.md` (round 7) and `tests/results/prompt-battle.json`.
- Rebuild the compendium (`python3 -I tools/build_compendium.py`), run `tests/run.sh`, `python3 -I tools/check_privacy.py` and `python3 -I tools/check_links.py`, and run both mutation suites with `--record`.
- Commit "Record /prompt v9 against v7: …", with the headline numbers in the message.

## Budget

| Wave | Runs |
|---|---|
| 0 | up to 2: critic and its second round |
| 2 | 2 probe drafters and up to 2 of the battle reviews |
| 3 | 1 must-haves probe |
| 4 | 4 drafters, up to 4 battle reviews, 6 runners, up to 12 dry-run reviews: up to 26 |
| 5 | 7 |
| 6 | up to 2: diff review and its second round |
| Total | at most 42 |

A drafter's or runner's fix round continues the same agent, so it is not a new run. If an agent can't be continued, the fix round is a fresh agent and counts as a run; wave 2 tests this before wave 3. Any draft that needs no review, or no second round, saves a run. When the runs run out, stop and report; every gate not yet read counts as failed.

## Stop and ask

- The wave 3 probe shows a must-have lost against v7: archive, revert and report, as for a failed gate.
- The measurement seems to need any change beyond the R7 rule.
- A gate fails at any wave: archive, revert the three slices together, report.
- Another session's uncommitted files make `tests/run.sh` fail.
- The same check fails twice for the same reason.

## Assumptions

- ASSUMED: a fix round sent to a drafter, runner or reviewer that is still open continues that agent and is not a new run.
- ASSUMED: each role uses the model it used in round 12.
- ASSUMED: a tie in a pair counts as a win for neither version.
- UNKNOWN: whether v9's drafts keep the decisive checks; the wave 3 probe decides it before the full evaluation.
