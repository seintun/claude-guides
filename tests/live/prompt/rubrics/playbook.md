# Playbook rubric for /prompt

The 47 recommendations the playbook makes about writing a prompt for an agent: how the prompt-writer behaves, and what the finished prompt contains. Drawn on 2026-10-25 from the sections `/prompt` cites, and frozen for the v7 against v8 comparison. It holds no grades.

A scorer grades each item PASS, PARTIAL, MISSING, CONFLICT or N/A against the skill under review, reading the playbook section named in the last column with `python3 -I tools/section.py <id>`. See `../briefs/score-playbook.md`.

| ID | Group | Recommendation | Playbook sections |
|---|---|---|---|
| P1 | Laws | Every task has a DONE WHEN list of checks a command or person can run; no "done" without the check's output | law-2, law-3, 9.1 |
| P2 | Laws | Right altitude; start minimal; add instructions for failures | law-3, 15 |
| P3 | Laws | Context is a budget: paths not dumps, heavy reading in subagents, compact on purpose | law-4, 8 |
| P4 | Laws | Plan file of slices, each naming its test | law-6 |
| P5 | Laws | Reviewers get the artifact and criteria, never the author's reasoning | law-7, 7, 9.2, 15 |
| P6 | Laws | Anonymize sources when comparing candidates | law-7 |
| P7 | Laws | Must-happen checks live in hooks, CI, permissions or the sandbox, not only prose | law-9; 9.2 rung 3; 9.3 hook or CODEOWNERS on test paths; 14 "declares victory early" |
| P8 | Laws | Fan out only for parallel, read-heavy or judgment work; single agent for coupled edits; autonomy by risk | law-10, 19.1 item 1 |
| P9 | Lifecycle and delegation | Scale spec weight to risk and novelty; large change gets research doc, ADR, critic, sign-off; humans approve the plan | 5.3, law-6 |
| P10 | Lifecycle and delegation | Keep state in files so a session can resume: plan file is the source of truth and kept current; JSON for structured state | 5.3, 7, 8, B |
| P11 | Lifecycle and delegation | Brief core: objective, output format, sources, boundaries | 7, C |
| P12 | Lifecycle and delegation | Brief says what is already ruled out and already decided | 7, C |
| P13 | Lifecycle and delegation | Return schema: findings with evidence, confidence, unknowns | 7, C |
| P14 | Lifecycle and delegation | Helpers write to files and return paths; a report is a claim the lead re-checks; no raw transcripts | 7 |
| P15 | Lifecycle and delegation | One writer per set of files; a worktree per builder | 7, 19.3 |
| P16 | Lifecycle and delegation | Scale agent count to task size; spawn helpers in parallel | 7 |
| P17 | Verification | Normal risk: a fresh reviewer reads the diff against the criteria, kept even when tests are green | 9.2 rung 4, 9.3 |
| P18 | Verification | High risk: adversary, then a human | 9.2 rungs 5 and 6 |
| P19 | Verification | Bounded review: a blocker needs evidence; only a fix, the reviewer or a human closes it; two rounds, then a human decides | 9.2, 19.1 item 10 |
| P20 | Verification | Round-2 detail: large fix gets full re-review; rerun reviewers the fix touches; advisory findings to a follow-up list; "no blockers" valid; log closures and who closed | 9.2 |
| P21 | Verification | High risk: one security pass reads the code against an application checklist | 9.2 |
| P22 | Verification | Tests first | red, green, refactor); tests immutable to the builder; reviewer inspects test diffs (5.3, 9.3 |
| P23 | Verification | UI and full-flow checks go through a real browser | 9.3 |
| P24 | Verification | Prefer code checks; an LLM judge needs a rubric and is never the only gate | 9.3, 19.1 item 9 |
| P25 | Verification | Receipt per criterion: PASS, FAIL or NOT RUN with command; NOT RUN is not PASS; list what is not done and the next step | 9.4 |
| P26 | Guardrails and loops | Every loop has a stop condition and an iteration, time or cost cap | 11.3, 10.3 item 7, 15 |
| P27 | Guardrails and loops | Retry cap: two failures with the same cause, stop and report; get a second opinion from a fresh agent | 11.3, 14, B rules |
| P28 | Guardrails and loops | Idempotent actions: running twice must not send, charge or create twice | 11.3 |
| P29 | Guardrails and loops | Results sink outside the chat; cloud scheduled tasks keep state in a ticket, PR comment or branch, not files | 11.3 |
| P30 | Guardrails and loops | Per-pass hygiene: one-line status, "no change", fresh context per iteration or deliberate compaction | 11.3, H |
| P31 | Guardrails and loops | Explicit stop-and-ask list, including hard-to-undo actions; open questions the agent asks about; unattended runs leave a note | 14, B, L, H |
| P32 | Guardrails and loops | Counter overbuilding: diff-size budget, simplifier pass, reviewer flags scope creep | 14 |
| P33 | Guardrails and loops | Upfront specs miss edge cases: run a QA loop whose findings become new issues | 14, 5.2 |
| P34 | Templates | Prompt parts: one-sentence outcome GOAL; CONTEXT of files, links, prior decisions; CONSTRAINTS and no-gos | B, L, cs:6 |
| P35 | Templates | BUDGET with helper cap; stop and report when it runs out | B, law-10, 10.3 |
| P36 | Templates | A RISK line set by a rule | paths, new dependencies, schema, auth); take the higher when person and rule disagree (B, L |
| P37 | Templates | Explore with read-only helpers, then synthesize a brief of facts, unknowns, options before planning | B 1 to 2, law-6, 14 |
| P38 | Templates | Build one slice at a time; run that slice's test before moving on | B step 5 |
| P39 | Templates | Scheduled output is capped and ordered | H |
| P40 | Templates | Issue fields: Today with repro steps for a bug; Depends on | L |
| P41 | Templates | Interview one question at a time until the brief can be written | cs:7, 14 |
| P42 | Templates | Write the brief to a file; the user edits goal, done-when, stop-and-ask; start a fresh session | cs:7 |
| P43 | Evidence | Script the pipeline for large mechanical changes; gate every file; budget the long tail | 19.1 item 2, 19.3 |
| P44 | Evidence | External verification beats self-critique | 19.1 item 3, 19.3 |
| P45 | Evidence | Measure reliability and cost, not one good run: pass^k for unattended runs | 9.3, 19.1 item 5, 19.3 |
| P46 | Evidence | Size agent output to human review capacity | 19.1 item 6, 19.3 |
| P47 | Evidence | Search and optimization loops need a machine grader | 19.1 item 7 |
