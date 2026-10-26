# /prompt v10 Implementation Plan

> **For agentic workers:** Implement this plan phase by phase, in order. Before you claim a phase is done, run its gate and record the result. NOT RUN is not PASS.

**Goal:** Ship `/prompt` v10 as v7 plus every playbook-required item (R1 to R6), and D3 only if it beats the bundle by more than measured noise, such that blind review shows no regression against v7 beyond that noise and two executed v10 prompts report no false PASS.

**Risk:** high. It changes the skill, its check, tests and guarded files, and spends up to 100 subagent runs.

**Status:** approved by the user on 2026-10-25, after two critic rounds.

**Source:** the prompt `prompts/claude-guides/2026-10-25-prompt-v10.md` (git-ignored). This plan is written before any evidence; every margin rule below is fixed now and is not changed after a reviewer file is read.

## Why v10 is shaped this way

v8 and v9 each bundled about 15 changes and lost blind review to v7 ([results.md](../../tests/live/prompt/results.md) rounds 12 and 13; [grill-prompt results](../../tests/live/grill-prompt/results.md) rounds 6 and 7). Both folded v7's nine-bullet consistency pass into five bullets, and contradictions rose both times. Rubric scores rose while blind preference fell (§9.3: an LLM judge is never the only gate).

v10 therefore:
- keeps v7's `skills/prompt/SKILL.md` unchanged except for the sentences each required item changes. Step 8 keeps all nine bullets; only R6 changes one sentence in its Files bullet.
- lands each item as its own commit, so any one can be reverted alone.
- measures noise first (phase 0), because judges and audits of the same v7 material have disagreed widely: two judges gave the same v7 dry runs 2 and 6 failures (rounds 6 and 7), and audits of the same v7 drafts counted 11, 4 and 8 contradictions (rounds 11, 12 and 13).

Not in v10 (the v11 backlog, already archived in [variants/](../../tests/live/prompt/variants/README.md)): `example.md`, input tags, the delegation split, "stop when done", v9's D7 rules, c-10 (GOAL first), any word cap, any compression of step 8.

## Models

| Role | Model | Agent tool value |
|---|---|---|
| Drafters, step-10 reviewers, dry-run runners, end-to-end drafter and executors | `claude-sonnet-5-5` | `model: "sonnet"` |
| Pairwise reviewers, audit, must-haves reviewer, dry-run judges, plan critic, end-to-end grader, final diff reviewer | `claude-opus-5-5` | `model: "opus"` (the critic and final reviewer are `adversarial-reviewer`, whose frontmatter pins Opus) |

Each run's reviewer file records the model it ran on. Rounds 11 and 5 ran on 2026-10-24 and 2026-10-25, so model drift against v7's frozen material is likely near zero; any that exists widens the margin and is reported as such.

**Battle method matches round 11.** Round 11 reviewed a draft only where the skill's step 10 triggers ("several slices, high risk, or a decision log"); its feature and research drafters judged their prompts one slice, so those two were not reviewed. Reviewing every new draft would make T1 and T2 differ by method in 2 of 6 scenarios, and `M_scen` would measure that method effect, not noise. So every battle draft in phases 3, 5 and 6 gets step 9's check, and step 10's review only where the skill under test triggers it; the results record which drafts were reviewed. The prompt's HOW TO WORK step 3 says "each through step 9's check and one step-10 review"; the user approved this method at sign-off.

## The required items: exact text, pins and review edits

Each item edits v7's text only in the sentence it changes. Text comes from [SKILL-v9.md](../../tests/live/prompt/variants/SKILL-v9.md), [check_prompt-v9.py](../../tests/live/prompt/variants/check_prompt-v9.py) and [delegation-v8.md](../../tests/live/prompt/variants/delegation-v8.md), reworded to v7's voice. Items land in order R1 to R6; R2, R3 and R6 also edit step 3, so each is written below as the full step 3 after that item.

v7's step 3 today:

> 3. **Size it by risk** (§5.3). Trivial or one slice: goal, checks, receipt, no plan file. Several slices: add a plan file of slices, each with its test and rollback. High risk: add a research step, a fresh critic on the plan and human sign-off.

### R1. Risk line, Template L's rule, Template B's trivial form, c-9 (Templates B and L, §5.3, Law 9)

Step 3 becomes:

> 3. **Size it by risk** (§5.3), and write the result above the title as `Risk: trivial`, `Risk: normal` or `Risk: high`. Set it by a rule, not by feel (Template L). High: the work touches a schema, auth, payments, data deletion, a public API, infrastructure or production, adds a dependency, or runs unattended. Trivial: a small fix in one place, easy to undo, with no helpers or loop, such as a typo or a wrong comment. A change to user-visible behaviour is never trivial. Normal: everything else. When two sizes apply, or the rule and a person disagree, the higher wins. Trivial: GOAL, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT; CONTEXT is optional; no plan file. One slice: no plan file. Several slices: add a plan file of slices, each with its test and rollback. High risk: add a research step, a fresh critic on the plan and human sign-off; an unattended run is signed off once, before it first starts.

Step 5's lead-in "Draft the prompt** from these parts, in this order:" becomes "Draft the prompt** from these parts, in this order (a trivial prompt may leave out CONTEXT):", so step 5 agrees with step 3.

`check_prompt.py` takes v9's `RISK`, `TRIVIAL_PARTS`, the risk-aware c-1 and c-9, and nothing else from v9 (no c-10, no fix hints that point at an ASSUMPTIONS part). Its docstring gains the c-1 and c-9 lines from v9.

Tests first (`tests/test_prompt_skill.py`):
- `SkillRules.test_keeps_every_rule` gains: "write the result above the title as `Risk: trivial`, `Risk: normal` or `Risk: high`"; "Set it by a rule, not by feel (Template L)."; "High: the work touches a schema, auth, payments, data deletion, a public API, infrastructure or production, adds a dependency, or runs unattended."; "Trivial: a small fix in one place, easy to undo, with no helpers or loop"; "Normal: everything else."; "A change to user-visible behaviour is never trivial."; "When two sizes apply, or the rule and a person disagree, the higher wins."; `Trivial: GOAL, DONE WHEN, CONSTRAINTS, BUDGET, STOP AND ASK IF, HOW TO WORK ("build, verify, report") and REPORT`; "an unattended run is signed off once, before it first starts".
- `SkillRules.test_skill_and_check_change_together`: "`Risk: trivial`" is in SKILL.md exactly when "c-9" is in `check_prompt.py`.
- `PromptCheck`: `test_trivial_may_leave_out_context`, `test_trivial_keeps_template_b_parts` (BUDGET, STOP AND ASK IF, HOW TO WORK each removed in turn fails c-1 and names the part), `test_missing_risk_line_fails_c9`, `test_old_low_label_fails_c9`, `test_risk_line_ignores_case_bold_and_bullets`, as v9's plan specified them.
- The good fixture (`tests/fixtures/prompt-check/good.md`) gains `Risk: normal` above its title, and the tests that count PASS lines go from 8 to 9. This follows the check's new wording; it weakens nothing.

Review edits (`tests/mutation/review_edits.py`, each must be CAUGHT):
- 64: SKILL.md's risk-line clause (", and write the result above the title as … `Risk: high`") deleted.
- 65: c-9 always PASS in `check_prompt.py`.
- 66: `needed = TRIVIAL_PARTS if risk == "trivial" else PARTS` becomes v8's short form `["GOAL", "DONE WHEN", "CONSTRAINTS", "REPORT"]` for trivial.
- 72: the rule's three definitions ("High: … runs unattended. Trivial: … a wrong comment. A change to user-visible behaviour is never trivial. Normal: everything else.") deleted, leaving the risk line with no rule behind it. (D3's edit, if kept, is 73.)

Commit: "Make /prompt size by Template L's rule and keep Template B's trivial form (R1)".

### R2. A fresh reviewer reads the diff at normal risk (§9.3, Template B step 7)

Step 3 gains, after "each with its test and rollback.": "At normal or high risk, HOW TO WORK ends with a fresh reviewer that reads the diff against DONE WHEN, even when the tests pass."

Pin: "HOW TO WORK ends with a fresh reviewer that reads the diff against DONE WHEN, even when the tests pass". Review edit 67 deletes that sentence. Commit: "Make /prompt end normal and high prompts with a fresh diff review (R2)".

### R3. Each hard constraint at high risk names its gate (Law 9)

Step 3 gains, after "signed off once, before it first starts.": "At high risk, also name for each hard constraint the gate that enforces it (a hook, CI, a permission); a constraint written only in prose is a request, not a control."

Pin: "At high risk, also name for each hard constraint the gate that enforces it (a hook, CI, a permission); a constraint written only in prose is a request, not a control". Review edit 68 deletes that sentence. Commit: "Make /prompt name the gate behind each hard constraint at high risk (R3)".

### R4. Helper briefs give what is ruled out and decided (Template C)

Step 6: "objective and the decision it feeds, where to look," becomes "objective and the decision it feeds, what is already ruled out and already decided, where to look,".

Pin: "what is already ruled out and already decided". Review edit 69 deletes that clause. Commit: "Make /prompt's helper briefs carry what is ruled out and decided (R4)".

### R5. Loops are idempotent, least-privilege and capped (§11.3, Template H)

Step 7's middle sentence becomes: "one small action per pass, and running twice sends, charges or creates nothing twice; "no change" when nothing changed, a stop condition, at most 2 failures with the same cause, a cap per run, and only the tools and permissions the task needs." Its last sentence's "(a ticket, a PR comment, a file outside the repository), never a new file" becomes "(a ticket, a PR comment, a file outside the repository), at most 15 lines, most important first, never a new file". `check_prompt.py`'s `SKILL_VALUES` gains `(?:at most )?15 lines`, so a prompt that repeats the skill's cap is not warned as an untraced figure.

Pins: "running twice sends, charges or creates nothing twice"; "only the tools and permissions the task needs"; "at most 15 lines, most important first". `PromptCheck.test_skill_set_output_cap_is_not_a_guess` as in v9's plan. Review edit 70 deletes all three clauses. Commit: "Make /prompt's loops idempotent, least-privilege and capped (R5)".

### R6. Plan files go to `docs/plans/<task>.md` (Template B)

Step 3's "Several slices: add a plan file of slices" becomes "Several slices: add a plan file at `docs/plans/<task>.md` of slices". Step 8's Files bullet sentence "Working files go in `<scratch>` unless the user wants them in the repository." becomes "Plan files go in `docs/plans/`; other working files go in `<scratch>` unless the user wants them in the repository." Without it, v7's drafters treat a plan as a working file (baselines `migration.md` and `refactor.md` write `<scratch>/plan.md`), and the two sentences contradict.

Pins: "add a plan file at `docs/plans/<task>.md`" and "Plan files go in `docs/plans/`; other working files go in `<scratch>`". Review edit 71 deletes both. Commit: "Make /prompt put plan files in docs/plans (R6)".

### Bookkeeping in each item's commit

`tests/README.md` (review-edit count 63 rising to 72), `tests/baselines/suite.json` (`min_test_cases` raised by the tests added), `skills/prompt/README.md` and `llms.txt` where the check's description changes (R1, R5). Each commit runs `tests/run.sh` to `SUMMARY all PASS`, `python3 -I tests/mutation/review_edits.py <its edits>` to CAUGHT, and `python3 -I tools/check_privacy.py`, and cites its playbook section in the message.

### D3 (optional, tested alone; §9.3, Law 3)

Step 5's DONE WHEN sentence "For each check, ask "could this pass while the goal is unmet?" and tighten it if so: tests can be green while the spec is broken (§9.3)." becomes "For each check, name the likeliest way the result could be faked or fall short, and make the check fail on it: tests can be green while the spec is broken (§9.3)." Step 10's "a quoted answer to three questions" becomes "four questions", and "Which check could pass while the GOAL is unmet?" follows the third.

If kept: pins "name the likeliest way the result could be faked or fall short", "and make the check fail on it" and "Which check could pass while the GOAL is unmet?"; review edit 62 retargeted to the four-question sentence (it still deletes every reviewer question, so it damages the same rule); new review edit 73 deletes the decisive-check sentence. If dropped: archived as `tests/live/prompt/variants/SKILL-v10-D3.md`, and no D3 text in `skills/prompt/`.

## Measurement

Frozen, unchanged: `tests/live/prompt/scenarios.json`, `briefs/`, `must-haves.md`, `tests/live/grill-prompt/dumps.md`, `rubrics/playbook.md`, the one-file README that `run.sh` writes ("Node 20 service with a Postgres database. Run the tests with `npm test`. Deploys from main through GitHub Actions."), and the request suffix "Skip any questions and draft the prompt now; list your assumptions at the top." v7 trial 1 is the round-11 drafts in `tests/live/prompt/baselines/v7/`; v7's dry runs are the round-5 runs in `tests/live/grill-prompt/baselines/v7/`.

Allowed changes, and nothing else:
- **M1:** rubric R7 is N/A for every Dump 1 run. `git cherry-pick 32bab0c` (it was reverted with v9 in 2e19a81).
- **M2:** a fresh v7 battle trial (phase 0).
- **M3:** two judges each grade the frozen v7 dry runs (phase 0).
- **M4:** every fix-round message to a drafter, runner or reviewer quotes step 10's rule verbatim: "After the last review, change nothing but the blockers it named: any other edit goes back for review, or is listed at hand-over as unreviewed." It never says "fix and save".
- **M5:** the end-to-end fixture and its hidden tests.

Two filled-in briefs differ from their committed templates only in a file list, kept in `<scratch>` (the committed briefs are unchanged): the D3 probe's pairwise reviewers read two scenario files, not six; and the phase-0 must-haves reviewer reads v7 against v7. Both follow v9's wave-3 precedent, and the user accepted them at sign-off.

### Blinding

As [briefs/README.md](../../tests/live/prompt/briefs/README.md) describes, plus: every draft has its `Risk:` line, any "Review: not run" line, scratch paths and any version or run name removed before a reviewer sees it. Pairs are built by a script with a fixed seed recorded in `<scratch>/keys/`; each pair is judged in both orders by two different reviewers. Keys live only in `<scratch>/keys/`, a folder no reviewer brief names.

### Noise margins (phase 0), fixed now

From one pairwise run per order of v7 trial 1 against v7 trial 2 (12 judgments), one audit of the same 12 drafts, one must-haves review of the same 12, and two judges each grading the six frozen v7 dry runs alone:

| Margin | Definition |
|---|---|
| `M_pair` | abs(mean score of trial 1 − mean score of trial 2) over the 12 judgments |
| `M_scen` | the largest, over the 6 scenarios, of abs(trial 1's mean − trial 2's mean), each mean over the two orders |
| `M_must` | the number of must-haves PRESENT in one v7 trial and ABSENT in the other (recorded; the must-have gate below needs no margin) |
| `M_audit` | abs(contradictions in trial 1 − contradictions in trial 2) in the one audit |
| `M_dry` | abs(judge A's failures − judge B's failures) over the same six frozen v7 runs |

Each number is written into the results files with the reviewer file it came from. No margin is estimated by the lead.

**Stop and ask after phase 0** if `M_pair` ≥ 1.0 or `M_audit` ≥ 4.

### Gates for the bundle (DONE WHEN 2), fixed now

v10 trials U1 and U2; v7 trials T1 and T2. Pairs and audits run U1 against T1 and U2 against T2, each pair in both orders (24 judgments, two audits).

| Gate | Passes when | Read from |
|---|---|---|
| Pairs | v10's mean score over the 24 judgments ≥ v7's mean − `M_pair` | the four pairwise reviewer files |
| Scenarios | for every scenario, v10's mean over its 4 judgments ≥ v7's − `M_scen` | the same files |
| Must-haves | no must-have PRESENT in both v7 trials is ABSENT in both v10 trials | the two must-haves reviewer files |
| Audit | mean over the two audits of (v10 contradictions − v7 contradictions) ≤ `M_audit` | the two audit files |
| Dry run | v10's failures − v7's frozen runs' failures, under one judge grading all 12 together, ≤ `M_dry`; and no final v10 prompt has a FAIL from `check_prompt.py` | the judge file and the lead's check outputs |

A gate with no reviewer file counts as failed. R10 (questions that ask two things) is counted and reported; if v10 fails it in more runs than v7, that is the first item bisected.

### D3 gate (DONE WHEN 3), fixed now

D3 is compared with bundle trial U1. Probe on bugfix and refactor (4 judgments): if D3's mean − U1's mean ≤ `M_pair`, D3 is dropped there. Otherwise the other four scenarios are drafted and D3 ships only if its mean over all 12 judgments beats U1's by more than `M_pair` and no must-have PRESENT in U1 is ABSENT in D3.

## Phases

Every helper is a fresh subagent briefed per Template C: objective, the only files it may read, its output file in `<scratch>`, and when it stops. Helpers are read-only on the repository; drafters and runners write only in their own `<scratch>` folder, with the Write and Edit tools and no shell, as `tests/live/grill-prompt/README.md` requires. The lead is the only writer of repository files. `<scratch>` is the session scratchpad.

| Phase | Work | Gate | Runs (cap) |
|---|---|---|---|
| 1 | This plan; one fresh critic, a second round on the fix diff only if a blocker with evidence reopens it; user sign-off in chat; commit the plan and `docs/decisions.md` | Blockers answered; the user signs off | 2 |
| 2 | `git cherry-pick 32bab0c` (M1) | `tests/run.sh` SUMMARY all PASS | 0 |
| 3 | Phase 0: 6 v7 drafters (trial 2), each draft through step 9's check and step 10's review where v7 triggers it, one fix round (M4), the check again; 2 pairwise (both orders, T1 vs T2), 1 audit, 1 must-haves; 2 judges on the frozen v7 dry runs. Record margins; apply the stop-and-ask | Every margin from a file | 18 |
| 4 | Build R1 to R6, tests first, one commit each, `tests/run.sh` after each. Copy `skills/prompt/` to `<scratch>/v10/bundle/` | Six commits, each all PASS | 0 |
| 5 | Bundle round: 12 battle drafters (U1, U2), each with step 9 and step 10's review where v10 triggers it; 6 dry-run runners, two per request, each with two review rounds; 4 pairwise, 2 audits, 2 must-haves, 1 judge | DONE WHEN 2's gates. On a regression: bisect by reverting items one at a time in `<scratch>` and rerunning only the affected scenarios' pairs, reword the culprit's sentence once, then stop and ask | 51 |
| 6 | D3 round on a scratch copy of the bundle: probe (2 drafters, 2 reviews, 2 pairwise, 1 must-haves), then if not dropped the other 4 scenarios (4 drafters, 4 reviews, 2 pairwise over all 6, 1 must-haves). If kept, commit D3 with its pins and review edits | DONE WHEN 3 | 18 (cap 19) |
| 7 | End-to-end (below) | DONE WHEN 5 | 6 |
| 8 | Both mutation suites; a fresh `adversarial-reviewer` reads the final diff (from 17922b8 to HEAD) against DONE WHEN, even when the tests pass. Only a blocker with evidence reopens it; a re-review reads the fix diff; after two rounds the user decides | DONE WHEN 4; review closed | 2 |
| 9 | Record every number with its file in `tests/live/prompt/results.md` (round 14), `tests/live/grill-prompt/results.md` (round 8) and `tests/results/prompt-battle.json`; rebuild the compendium; `tests/run.sh`; both mutation suites with `--record`; commit | all PASS | 0 |

Total cap: 2 + 18 + 51 + 19 + 6 + 2 = 98 of 100. Phase caps assume every draft is reviewed; drafts the skill does not send to review save runs, and those savings are the only budget for a bisect in phase 5. A fix round to a still-open agent continues it and is not a new run (ASSUMED in the prompt). Phase 3 tests this on its first drafter; if an agent cannot be continued, stop and ask before going on, since phase 3 would then need up to 24 runs against its 18. When a phase's cap is reached, stop and report; every unread gate counts as failed. The scorers (`score-playbook.md`, `score-external.md`) report coverage only and are not run, since no gate reads them.

### Phase 7: end-to-end fixture (M5)

Built in `<scratch>/e2e/fixture/` before any v10 prompt is drafted, as a git repository with two commits:
- `package.json` (`"engines": {"node": ">=20"}`, `"test": "node --test"`, no dependencies, so nothing is downloaded), `README.md` ("Node 20 service. Run the tests with `npm test`."), `src/reports.js` (a reports page that renders rows after filters, plus a stub `exportCsv(rows, filter)` that throws "not implemented", so the hidden tests call a name fixed before any run), `src/auth.js` (sessions, login, password reset), and visible tests in `test/`.
- The second commit, dated seven days before the run, introduces the logout-after-reset bug: `resetPassword` issues the new session and then bumps the user's session version, so the new session is invalid at once.

Hidden acceptance tests are written before any executor starts, packed and encrypted (`openssl enc -aes-256-cbc -pbkdf2`) with a random key, and the plain copies deleted. The key is written nowhere on disk until both executors have finished; it goes only into the grader's brief, and the archive's sha256 is written into `<scratch>/keys/hidden.sha256` before the first executor starts. An executor that lists the scratch folder finds only ciphertext:
- **Feature (CSV export):** the export has a header row; its rows are exactly the rows the page shows for a given filter; a filter that matches nothing gives a header only; values with commas, quotes and newlines are quoted.
- **Bugfix:** after `resetPassword`, the session it returns stays valid; the old password fails and the new one works; a visible test that fails before the fix passes after it.

Runs: 1 drafter writes both prompts with the final skill (continued for the second), using the scenario texts from `scenarios.json` and the fixture's README; 2 step-10 reviews; 2 executors, each a fresh Sonnet agent that reads only its prompt and works only in its own copy of the fixture; 1 grader, a fresh Opus agent that unpacks the hidden tests (after checking the sha256), runs them itself against each executor's final tree, reruns each receipt command, and lists every receipt line marked PASS whose command or matching hidden test fails. An executor cannot start subagents, so any critic or review step its prompt asks for is reported NOT RUN; that is correct and is not a false PASS. The bugfix touches auth, so under R1 its prompt is high risk and asks for sign-off. Every sign-off request or STOP AND ASK question from an executor gets one fixed reply from the lead, recorded in the results: "Signed off. Go ahead within the prompt as written; no further answers will come, so for anything else, stop and report."

Fixed now, before any run:
- **Hidden test to DONE WHEN item.** The grader maps each hidden test to the DONE WHEN item whose claim it tests, from the prompt alone, and writes the mapping before opening any receipt or running anything.
- **False PASS.** Any receipt line marked PASS whose command fails when the grader reruns it, or any DONE WHEN item marked PASS while a hidden test mapped to it fails.
- **A run that proves nothing fails.** A run that ends before REPORT, or whose REPORT marks no DONE WHEN item PASS, fails DONE WHEN 5.

DONE WHEN 5 passes when both runs reach REPORT with at least one DONE WHEN item PASS, the grader's file lists no false PASS, and `results.md` records each hidden test's result.

## Stop and ask

- `M_pair` ≥ 1.0 or `M_audit` ≥ 4.
- The bundle regresses past a margin, and one bisect plus one rewording of the culprit's sentence does not fix it. Required items are not dropped.
- The measurement seems to need a change beyond M1 to M5.
- The same check fails twice for the same reason.
- Another session's uncommitted files make `tests/run.sh` fail.
- An agent cannot be continued for its fix round (phase 3's first drafter tests this).
- A bisect is needed and the runs saved so far do not cover it.

## Review focus for the critic

1. **Are the margin rules fair?** Each is a single difference between two samples, so it is itself noisy. Is a gate that subtracts one such difference too lenient, or too strict, for what DONE WHEN 2 asks?
2. **Model drift.** v7 trial 1 and v7's frozen dry runs came from earlier model versions; the new trials do not. Does that bias any gate?
3. **The trivial form and v7's step 5.** R1 changes step 3 and one clause of step 5. Does any other v7 sentence now contradict a trivial prompt with no CONTEXT?
4. **The run cap.** Phase 5 uses all 51 runs with no spare for a bisect. Is the bisect budget real?

## Outside judge (Codex), fixed before any Codex output

The user asked for a judge outside Claude after v10 was built. This rule is written and committed before Codex reads anything.

- **Runs.** Codex CLI 0.164.0 (`codex exec`, read-only sandbox, ephemeral), with the frozen briefs unchanged except for their folder paths: `blind-pair.md` on the four bundle pair folders (U1 against T2 and U2 against T3, each in both orders, 24 judgments), and `judge.md` on the twelve blinded dry runs (six fresh v7, six v10). No version names, risk lines or keys reach Codex. One run per folder, five in all; no reruns to change an answer.
- **Read.** The lead unblinds Codex's replies with the same keys (`v10-a.json`, `v10-b.json`, `v7fresh-judge.json`) and computes v10's and v7's mean pair score, v10's win count, and each set's dry-run failures.
- **Confirms the ship:** Codex's v10 mean pair score is at least v7's minus 0.25 (`M_pair`), and Codex's v10 dry-run failures are no more than v7's plus 1.
- **Raises the ship score to 9 of 10:** both of the above, and Codex gives v10 more than 12 of 24 pair wins.
- **Holds the ship and goes back to the user:** Codex's v7 mean exceeds v10's by more than 0.25, or Codex gives v10 2 or more dry-run failures above v7's.
- **Agreement with Claude** is reported per judgment (same winner or not) and per gate, and does not change the rule above.
- A Codex run that fails or returns no table counts as not run; it is reported, not retried with a changed brief.

## Decisions

- 2026-10-25 Work on `feat/prompt-v10`, which was cut at `feat/guide-entry`'s tip (17922b8), so the prompt's branch assumption holds.
- 2026-10-25 Scorers are not run, because the prompt says they are not gates and the budget has no room for them.
- 2026-10-25 One end-to-end drafter writes both prompts, so phase 7 fits its cap of 6.

- 2026-10-25 Critic round 1 raised three blockers, all accepted: the end-to-end gate could pass with zero cases (fixed: false PASS defined, empty runs fail, fixed reply to sign-off, stubbed export name, encrypted hidden tests); a review-method gap against v7 trial 1 (fixed: step 10 only where the skill triggers it, pending the user's yes); and R6 and R1 contradicting step 8 and step 7 (fixed: step 8's working-files sentence, one-time sign-off for unattended runs). Its notes added a pin and review edit for R1's definitions, two stop-and-ask lines, and "At high risk" in R3.

- 2026-10-25 Critic round 2: all three blockers closed, no new ones. Its two notes were applied: the grader maps hidden tests from the prompt alone before opening any receipt, and the "step 8 stays whole" line now names R6's one-sentence change.

- 2026-10-25 The user signed off: battle drafts follow round 11's review method (step 10 only where the skill triggers it); the two brief copies that change only a file list are accepted; the prompt's ASSUMED lines 1 to 5 are confirmed.

- 2026-10-25 Phase 0 measured: M_pair 1.542 (v7 trial 1 mean 8.000, trial 2 mean 6.458; trial 1 won 10 of 12), M_scen 3.00 (overnight), M_must 3 (B2, RF2, R2 lost by trial 2), M_audit 1 (9 against 8), M_dry 0 (both judges gave v7's frozen runs 3). M_pair is at least 1.0, so the work stopped and asked, as planned. 15 of phase 0's 18 runs were used. R1 was built and committed meanwhile (e2106d8); it does not touch the measurement.

- 2026-10-25 The user decided: run a third v7 trial (T3) by trial 2's method; take every battle margin from T2 against T3; judge v10 only against T2 and T3 (U1 against T2, U2 against T3), never against the round-11 drafts. The run cap rises from 100 to 115, and phase 0's cap from 18 to 33. `M_dry` stays as measured (0), since the dry-run comparison uses the frozen runs under one judge. The DONE WHEN 2 must-have rule reads "PRESENT in both of T2 and T3".

- 2026-10-25 Phase 0 rerun on T2 against T3, the margins the gates use: M_pair 0.250 (T2 7.500, T3 7.250), M_scen 2.00 (bugfix), M_must 3 (M1, B2, O3), M_audit 2 (T2 6, T3 8), M_dry 0. No stop rule holds. Phase 0 used 31 runs in all (cap 33). R2 to R6 were built and committed meanwhile.

- 2026-10-25 Bundle round read (U1 against T2, U2 against T3). Pairs PASS: v10 mean 7.79, v7 mean 7.00, margin 0.25. Scenarios PASS: no v10 scenario mean below v7's. Must-haves PASS: no must-have present in both T2 and T3 is absent in both U1 and U2. Audit PASS at the edge: U1 − T2 = +5, U2 − T3 = −2, mean +1.5 against M_audit 2. Dry run FAIL: one judge gave v10's six runs 7 failures (R6 ×4, R2, R1, R10) against 1 for v7's frozen runs (R2), margin 0; no final v10 prompt has a FAIL from check_prompt.py. R10 came back in one v10 run (3a). Three of the four R6 failures are about a stale "Review: not run" line or a hand-over claiming nothing was edited after the last review. A bisect needs a new dry round per variant (6 runners, up to 12 reviews, 1 judge), and the bundle round has 4 runs left, so the work stopped and asked, as planned. 83 of 115 runs used.

- 2026-10-25 The user chose a second fresh judge on the same 12 blinded runs, then a bisect starting with R1 if v10 still trailed by 3 or more, with the run cap raised as needed. The second judge gave v10 9 failures (R6 ×4, R4 ×2, R10 ×2, R2) against v7's 1 (R2), so the bisect runs. The first variant is the bundle minus R1 (step 3 back to v7's sizing sentences, check without c-9), drafted as six fresh dry runs and graded by one fresh judge with v10's and v7's runs.

- 2026-10-25 Bisect step 1 read. One fresh judge graded 18 runs together, blinded: the bundle minus R1 6 failures (R6 ×3, R3, R2, R10), the full bundle 6 (R6 ×3, R3, R10, R2), v7's frozen runs 3 (R3 ×2, R2). Dropping R1 leaves the gap where it was, so R1 is not the culprit. Across the three judges, v10 and minus-R1 fail R6 eleven times and v7's frozen runs never do; most of those R6 failures are a stale "Review: not run" header or a hand-over that misstates what changed after the last review. v7's frozen runs were made under round 5's runner brief, not this round's, the same kind of method gap the battle round's T1 had. 110 of 115 runs used.

- 2026-10-25 The user chose a fresh v7 dry round (six runs, this round's runner brief, checks and two review rounds each), judged together with v10's six runs, and raised the run cap to about 135.

- 2026-10-25 Fresh v7 dry round read. One fresh judge graded six fresh v7 runs (this round's runner brief, checks, two review rounds each) with v10's six, blinded: fresh v7 7 failures (R10 ×2, R6 ×2, R2, R4, R7), v10 7 (R6 ×4, R2, R1, R10). Under the same method the gap is 0, which meets M_dry 0. The earlier 6-to-9-point gaps came from comparing v10's fresh runs with v7's round-5 runs, which were made under a different runner brief, as the battle round's T1 was. R10 shows up in fresh v7 runs too (2 runs against v10's 1), so it is not a v10 regression. No final prompt in either set has a FAIL from check_prompt.py. 130 runs used.

- 2026-10-25 The user accepted the dry-run gate as read against the fresh v7 runs (PASS), so DONE WHEN 2 passes on all five gates, and raised the run cap to about 165 for D3, the end-to-end runs and the final review.

- 2026-10-25 D3 round read, against U1. Probe (bugfix, refactor): D3 7.75, U1 7.25, a gain of 0.50 over M_pair 0.25, so the other four were drafted. Full round, 12 judgments: D3 7.583, U1 7.417, a gain of 0.17, inside M_pair, so D3 is dropped as DONE WHEN 3 requires. Must-haves: D3 lost none against U1 (it gained RF3 on refactor in the probe). The D3 migration draft still had one c-3 FAIL (two gaps on one UNKNOWN line) when it went to the reviewers. D3 is archived as `tests/live/prompt/variants/SKILL-v10-D3.md`; `skills/prompt/SKILL.md` has no D3 text. 146 runs used.

- 2026-10-25 End-to-end read. One drafter wrote both prompts with the final skill (feature: no step-10 review; bugfix: one review, one fix round). Two fresh executors ran them on copies of the fixture and both reached REPORT with DONE WHEN 1 to 5 PASS and review steps NOT RUN. The fresh grader mapped hidden tests to items from the prompts alone, then ran them: the feature repository passed H1 to H4 and the bugfix repository H5 and H6, and no receipt line claimed a false PASS. A hook refused the bugfix executor's Edit tool and it edited through Bash; this is recorded, not counted as a gate failure. Evidence: `tests/live/prompt/round14/end-to-end/`. 152 runs used.
- 2026-10-25 Mutation suites: 23 of 23 and 72 of 72 caught. The final diff review (one fresh adversarial reviewer, 153 runs) raised three blockers. (1) No number cited a committed file: fixed by committing the reviewer, judge, audit, must-haves and grader files to `tests/live/prompt/round14/` with an index from each number to its file. (2) Three R1 edits were uncaught: fixed by a pin, two tests and review edits 73 to 75, all CAUGHT (e4b1660). (3) R1, R2, R3 and R6 all edit step 3's single line, so `git revert` of R2 or R3 alone conflicts. Not fixable without rewriting history. The user chose to rewrite the unpushed branch: a first commit puts each sentence of step 3 on its own line with spare blank lines, each item's pins and review edits sit in their own place in the test files, the shared counters (test floor, review-edit counts) move to this last commit, and the generated compendium is marked `merge=ours` (each clone needs `git config merge.ours.driver true`). Each of R2 to R6 is then a `git revert` with no conflict, and R1 is one together with its guard commit ("Guard the rest of /prompt's R1"), whose tests check R1's own text. After a revert, rebuild the compendium and lower the test floor in the same commit, as `tests/baselines/suite.json` asks; the suite then passes. Checked in a scratch clone for each item.

- 2026-10-25 Outside judge read, under the rule fixed in 3e64b33. Codex (gpt-6.1-sol via Codex CLI 0.164.0, read-only, one run per folder; the first two attempts stopped on a usage limit before judging and were rerun unchanged): pairs v10 6.583 against v7 6.625 (−0.04, within 0.25), v10 10 of 24 wins; dry run v10 16 against fresh v7 19. Result: CONFIRM, not raised to 9 of 10. Codex agreed with Claude's winner in 13 of 24 judgments. Per scenario, Codex put v10 below v7 on migration (5.75 against 7.0), overnight (6.25 against 6.75) and research (6.75 against 7.75), all within M_scen 2.0, and above on feature (8.0 against 5.5). So v10 is no worse than v7 under both judges; that it is better holds only under Claude. Files: `tests/live/prompt/round14/codex/`.

## Open questions

- None. The prompt file repeats its last paragraph and its REPORT section (lines 105 to 112); this plan reads them as one.
