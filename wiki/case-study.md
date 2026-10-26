# Case study: this repository's own work

Read this page to see the playbook applied from first request to final review, on the work that built
this repository's teaching page and playbook.

## Background

On 2026-10-24, one Claude Code session in the Claude desktop app built the "Orchestrating Claude" page
and the playbook ([session log](../docs/session-log.md)). The owner then asked for independent
reviews, and the rest of the work ran the way the playbook says to run it. Each section below names the
files that show it. The [decision log](../docs/decision-log.md) records each choice as D1 to D27.

## The steps and the playbook sections they applied

| # | Step | Rule applied | Playbook |
|---|---|---|---|
| 1 | A request becomes an issue with 13 children | Slice into issues with an outcome, a check, a boundary and dependencies; write a task contract and a plan table; scale the lifecycle to the risk | [§5.1](../playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues), [Template L](../playbook/agent-harness-playbook.md#l-agent-ready-issue), [Template B](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt), [Template D](../playbook/agent-harness-playbook.md#d-plan-file), [§5.4](../playbook/agent-harness-playbook.md#54-delivery-phases) |
| 2 | The check harness comes first | No task without a check the agent can run itself; criterion, scenario, then gate | [Law 2](../playbook/agent-harness-playbook.md#law-2-verification-multiplies-quality), [§9.1](../playbook/agent-harness-playbook.md#91-from-criterion-to-gate) |
| 3 | One writer on the page, parallel drafters | Single agent for tightly coupled edits, fan out for parallel work, one writer per set of files | [Law 10](../playbook/agent-harness-playbook.md#law-10-spend-compute-where-it-buys-accuracy), [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol), [§19.1](../playbook/agent-harness-playbook.md#191-findings-that-hold-up) |
| 4 | Reviewers who never saw the builder's report | Separate the maker from the checker; reviewers get the artifact and the criteria only | [Law 7](../playbook/agent-harness-playbook.md#law-7-separate-the-maker-from-the-checker), [§9.2](../playbook/agent-harness-playbook.md#92-trust-ladder) (rung 4), [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol) |
| 5 | A doc-checker fact-check changes a chart | Spot-check a number against its source before quoting it; a helper's report is a claim, not proof | [§19](../playbook/agent-harness-playbook.md#19-proven-orchestration-what-the-evidence-says), [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol) |
| 6 | A 30-minute launch with a written cut | Appetite is a time budget with variable scope; a budget and a stop-and-report rule; a minutes-based stop condition | [§5.1](../playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues), [Template B](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt), [§11.3](../playbook/agent-harness-playbook.md#113-guardrails-for-any-loop) |
| 7 | Gates, version by version, v12 to v16 | A receipt of PASS, FAIL or NOT RUN with the command; NOT RUN is not PASS; a test and a rollback per slice | [§9.4](../playbook/agent-harness-playbook.md#94-receipt-format), [§5.4](../playbook/agent-harness-playbook.md#54-delivery-phases), [Template D](../playbook/agent-harness-playbook.md#d-plan-file) |
| 8 | A final review catches a P1 keyboard bug | Tests can pass while the spec is still violated (S), so keep a fresh-eyes review; turn each lesson into a test | [§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest), [§13](../playbook/agent-harness-playbook.md#13-evals-and-learning) |

## 1. A request becomes an issue with 13 children

- The owner asked for independent UI/UX, learning-psychology and charting reviews, then an issue for a
  builder (session log, step 13). The reviews hold 38 findings:
  [UX-1 to UX-13](../issues/reviews/ux.md), [LX-1 to LX-11](../issues/reviews/lx.md) and
  [VZ-1 to VZ-14](../issues/reviews/vz.md).
- [The issue](../issues/orchestrating-claude-ux.md) has a parent and children 0 to 12, each a Template L
  issue with an outcome, a check, a boundary and a risk. A triage map sends every finding to a child,
  reviewer conflicts (C1 to C4) are settled in writing, and four open questions (Q1 to Q4) carry a
  recommended default.
- Severity runs from P0 (child 7) to P3 (child 12). The review tier is T1, so the gate is the check
  script plus a fresh re-review.
- The issue ends with a Template D plan table and a Template B contract: six Done-when lines, at most 3
  helpers at a time, and a stop after 2 failed attempts at one check or 13 publishes without a new PASS.

## 2. The check harness comes first

- Child 0 built `checks/static.sh`, `checks/dom-checks.js` and `checks/run-dom.js` before any page edit
  ([checks README](../checks/README.md)).
- It ran them on version 11 and saved [the baseline](../checks/baseline-v11.txt): 12 PASS, 57 FAIL.
  The failures included page overflow at 320 and 375 px, 155 SVG labels under 12px on phones, an
  evidence chart whose caption named 4 benchmarks while it drew 3, and an arrow key that moved focus
  to the wrong node.
- The run also settled a doubt: the UX review could not verify the desktop h1 overflow, and the
  baseline showed it was real.
- Template B's first two Done-when lines require the checks to print only PASS.

## 3. One writer on the page, parallel drafters

- Every page child edits one HTML file, so the plan runs them one at a time: one writer
  ([plan order note](../issues/orchestrating-claude-ux.md)). Decision D19 let subagents work in
  parallel on other files, on drafts and on reviews, with the lead splicing the output.
- The playbook navigation (child 5) ran in its own file at the same time. The glossary, takeaways and
  running example were drafted in [issues/drafts](../issues/drafts/glossary.md). Two figure agents
  redrew four diagrams, and `tools/splice_figs.py` spliced them in. The contract capped helpers at 3.

## 4. Reviewers who never saw the builder's report

- Decision D20: reviewers are fresh agents that get the files and the brief, never the builder's
  report. The session log lists them as fresh Sonnet subagents.
- The playbook-navigation reviewer ran its own scripts and was not shown the builder's report. It
  passed the change, and its low-severity notes went into a follow-up
  ([review](../issues/reviews/playbook-review.md)).
- The plan table marked child 7 (honest charts) PASS on the builder's own checks while the chart review
  was still running. The independent chart reviewer then returned FAIL with three blocking items, all
  fixed in version 15 ([review](../issues/reviews/chart-review-v12.md)).
- A fresh reviewer re-ran the three original briefs on version 12 and found 14 fixed, 22 partly fixed
  and 2 open ([review](../issues/reviews/post-launch-review-v12.md)).
- The reason appears in page Lesson 6 (Orchestration): a reviewer that reads your conclusion tends to
  agree with it.

## 5. A doc-checker fact-check changes a chart

- The chart in page Lesson 17 (Evidence) plots the Google Research scaling study. `doc-checker` checked
  its claims against the arXiv text for versions 1 and 3 and the Google Research blog
  ([fact-check](../research/google-scaling-check.md)).
- It found that the page's counts (180 configurations, 4 benchmarks) match version 1, while version 3
  reports 260 configurations and 6 benchmarks. It found that the 45% threshold is a fitted crossover,
  not an observed cliff, and that 17.2× and 4.4× are relative to a single agent.
- D11 replaced the bar chart with a dot plot: all four benchmarks, the best and worst design, exact
  baselines, a data table and the words "read the direction, not the size". D12 cites paper version 1
  (December 2025) and hedges the threshold. The chart reviewer later confirmed the numbers match the
  fact-check, and the playbook took the same correction in version 0.4.
- Template B made this a Done-when line: doc-checker confirms every number in the chart and its table.

## 6. A 30-minute launch with a written cut

- The owner set a 30-minute limit for a production launch (session log, step 16).
- Decision D21 wrote the cut down: ship children 0 to 7, 9, 10 and the takeaways; defer child 8, the rest
  of child 11, and child 12. The owner set the limit and Claude chose the cut.
- The cut kept the P0 child and every P1 child (1, 2, 3, 6, 9 and 10) and deferred only P2 and P3 work.
  Version 12 went out with 20 of 20 checks passing in 6 views, and the deferred children shipped in
  version 15.

## 7. Gates, version by version, v12 to v16

| Version | Change | Gate result |
|---|---|---|
| 12 | The 30-minute launch | 20 of 20 in 6 views |
| 13 | Phase buttons under the diagram, panel height held | Steady over 18 clicks in 3 views |
| 14 | Phase nav centered, "← Prev" and "Next →" | Steady and symmetric at 1280, 375 and 320 px |
| 15 | Review fixes, child 8, the rest of child 11, child 12 | 20 of 20 in 6 views |
| 16 | Final review fixes | 21 of 21 in 8 views |

- Source: [version history](../docs/version-history.md). Each version went to the same URL after its own
  check passed (D27), and new checks were added with each child (D26).
- The plan table holds a rollback for every slice: "republish previous version". Receipts say what did
  not run: the test-reader check is "not run" for children 2 and 3, and the scripted term count for
  child 11.

## 8. A final review catches a P1 keyboard bug

- Version 15 passed 20 of 20 checks. A fresh read-only reviewer then checked the page source against
  all 38 original findings and returned "not ready"
  ([final review](../issues/reviews/final-review-v15.md)).
- The P1: the quiz's change listener locked a question on the first arrow key, so a keyboard user could
  not choose an answer. Decision D23 fixed it with a "Check answer" button for each question.
- Version 16 added the check `quiz-1`, which asserts that arrows only select and Check answer scores,
  and ran the checks in 8 views instead of 6. The reviewer also found a P2 (figure text under 12px
  between 721 and 1230 px) and five P3 items, all fixed in version 16.
- Its tally on the 38 original findings was 27 fixed, 11 partly fixed and 0 open.

## What stayed open

- Vertical phone variants for figures were deferred, so UX-3 and VZ-3 are only partly fixed.
- The blind test-reader check was not run. The reviewer's 5 of 5 on the quiz does not count, because
  it saw the answers in the source first.
- Two reviewer proposals were declined: reordering the lessons (D4, question Q1) and tap-to-preview on
  touch screens (D2, question Q2).

## Go deeper

- Repository records: [session log](../docs/session-log.md), [decision log](../docs/decision-log.md), [version history](../docs/version-history.md), [the issue](../issues/orchestrating-claude-ux.md).
- [§0 How to use this file](../playbook/agent-harness-playbook.md#0-how-to-use-this-file): what the grade (S) means.
- Page lessons: page Lesson 3 (Idea to issues), page Lesson 6 (Orchestration), page Lesson 9 (Self-checks), page Lesson 17 (Evidence).
- Runbooks for each step: [start-a-task](start-a-task.md), [orchestrate](orchestrate.md), [verify](verify.md), [improve](improve.md).
