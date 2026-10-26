# Orchestration index

This is an agent-readable entry point. The agent reads this file first, then pulls only the playbook sections a phase names.

Sources:
- [`playbook/agent-harness-playbook.md`](playbook/agent-harness-playbook.md) is the guiding star. The § numbers below refer to it.
- [`playbook/claude-cheat-sheet.md`](playbook/claude-cheat-sheet.md) covers commands, a prompt template and signs that a run is stuck.
- [`wiki/`](wiki/README.md) holds step-by-step runbooks for each phase.

## How an agent uses this file

1. Find the current phase in the table below.
2. Read only the sections listed for that phase. Do not load the whole playbook.
3. Run the phase's review checklist against the work, citing the section for every finding.
4. Report each item as PASS, FAIL or NOT RUN with evidence (file, line or command). Never mark PASS without evidence.

Reusable review prompt:

```
Read orchestration-index.md. We are in phase <N>. Pull only the sections it lists for
that phase, then review <file or plan or diff> against that phase's checklist.
For each item, return PASS / FAIL / NOT RUN, the evidence, and the playbook section.
Finish with up to three fixes that block, or say that none do. Do not edit anything.
```

## Phase map

| # | Phase | Question it answers | Read | Runbook | Output |
|---|---|---|---|---|---|
| 1 | Shape | What problem, and is it worth doing? | [§5.1](playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues), [§5.2](playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules), [§16K](playbook/agent-harness-playbook.md#k-grill-prompt) | [Start a task](wiki/start-a-task.md) | Problem statement, issues |
| 2 | Brief | What exactly counts as done? | [§2 Law 3](playbook/agent-harness-playbook.md#law-3-specify-outcomes-not-steps), [§5.3](playbook/agent-harness-playbook.md#53-how-much-spec-before-code), [§16B](playbook/agent-harness-playbook.md#b-task-contract-goal-prompt), [§16L](playbook/agent-harness-playbook.md#l-agent-ready-issue), cheat sheet [§6](playbook/claude-cheat-sheet.md#6-prompt-template-for-orchestrated-work) to [§7](playbook/claude-cheat-sheet.md#7-let-claude-draft-the-prompt) | [Start a task](wiki/start-a-task.md); the [`/grill`](skills/grill/SKILL.md) and [`/prompt`](skills/prompt/SKILL.md) skills | Decision log, then a ready-to-run prompt |
| 3 | Plan | How, in what slices, with what risks? | [§2 Law 6](playbook/agent-harness-playbook.md#law-6-plan-before-building), [§5.4](playbook/agent-harness-playbook.md#54-delivery-phases), [§16D](playbook/agent-harness-playbook.md#d-plan-file), [§14](playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures) | [Start a task](wiki/start-a-task.md) | `plan.md` |
| 4 | Orchestrate | Who does what, in parallel or in sequence? | [§6](playbook/agent-harness-playbook.md#6-orchestration-patterns), [§7](playbook/agent-harness-playbook.md#7-delegation-protocol), [§16C](playbook/agent-harness-playbook.md#c-subagent-brief), [§3A](playbook/agent-harness-playbook.md#3a-claude-code-feature-map) | [Orchestrate](wiki/orchestrate.md) | Agent roster, briefs |
| 5 | Build | Is the loop healthy while running? | [§4](playbook/agent-harness-playbook.md#4-the-core-loop-one-agent), [§8](playbook/agent-harness-playbook.md#8-context-engineering), cheat sheet [§3](playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) | [Orchestrate](wiki/orchestrate.md) | Commits, state file |
| 6 | Check | Is it really done? | [§9](playbook/agent-harness-playbook.md#9-verification-stack), [§16F](playbook/agent-harness-playbook.md#f-stop-hook-that-blocks-done-while-tests-fail), [Law 2](playbook/agent-harness-playbook.md#law-2-verification-multiplies-quality), [Law 7](playbook/agent-harness-playbook.md#law-7-separate-the-maker-from-the-checker) | [Verify](wiki/verify.md) | Receipts |
| 7 | Overnight | Can it run without me? | [§11](playbook/agent-harness-playbook.md#11-continuous-and-unattended-operation), [§10](playbook/agent-harness-playbook.md#10-guardrails), [§16E](playbook/agent-harness-playbook.md#e-long-running-state-files), [§16H](playbook/agent-harness-playbook.md#h-loop-and-schedule-prompts) | [Run unattended](wiki/run-unattended.md), [Guardrails](wiki/guardrails.md) | Loop or schedule, morning report |
| 8 | Learn | What should never repeat? | [§13](playbook/agent-harness-playbook.md#13-evals-and-learning), [§16I](playbook/agent-harness-playbook.md#i-retro-prompt), [Law 8](playbook/agent-harness-playbook.md#law-8-turn-every-correction-into-a-rule), [§15](playbook/agent-harness-playbook.md#15-anti-patterns) | [Improve](wiki/improve.md) | CLAUDE.md rules, evals |

## Review checklists

### 1. Shape
- The problem is stated as user pain, not as a solution.
- Grilling ran one question at a time and stopped once the answers converged (§5.2).
- Out-of-scope items are written down.

### 2. Brief
- The goal is one sentence and is an outcome, not a list of steps (Law 3).
- "Done when" is checkable by a command or an explicit acceptance list.
- Constraints name what must not change.
- "Stop and ask if" lists the risky and ambiguous cases.
- A budget is set: time, tokens or attempts.

### 3. Plan
- Slices are vertical, and each one is testable on its own.
- Each hard-to-reverse decision is recorded with the reason for it.
- Open questions are listed and not silently assumed.
- Risky plans had a fresh-context critic (Law 7).

### 4. Orchestrate
- There is one writer per set of files; helpers only read or review (§6).
- Each subagent brief has a goal, scope, what is already ruled out and the return format (§7, §16C).
- Fan-out is justified by independence, not by parallelism alone.
- Model per role: cheap scouts, a strong architect and reviewer.

### 5. Build
- Context stays lean: `/compact` at phase boundaries, files rather than chat for state (§8).
- The same failure twice triggers a stop and ranked hypotheses, not a third blind retry.
- Progress is committed in small steps.

### 6. Check
- Every acceptance criterion maps to a gate (§9.1).
- Receipts use the §9.4 format, with commands.
- The checker is not the maker (Law 7).
- Tests were not weakened or deleted to pass.
- Hooks enforce what words only request ([Law 9](playbook/agent-harness-playbook.md#law-9-enforce-with-code-request-with-words), §9.5).

### 7. Overnight
- A state file and a progress log exist so a fresh context can resume (§11.1, §16E).
- The loop has a stop condition, a budget cap and an attempt cap (§11.3).
- Permissions are pre-approved for safe actions only; nothing irreversible runs unattended (§10).
- It works on a branch or worktree, never on main.
- The morning report lists what passed, what failed and what is waiting on you.

### 8. Learn
- Each repeated correction became a rule; dead rules were pruned (Law 8).
- Failures became eval tasks (§13, §16J).
- A retro was written (§16I).

## Walkthrough: one feature, start to morning

| When | You | Agent | Artifact |
|---|---|---|---|
| Evening, 15 min | Dictate the idea | Grills you, writes the brief | `brief.md` |
| +10 min | Edit "done when" and "stop if" | Plan mode, writes the plan; a critic reviews it | `plan.md` |
| +5 min | Approve the plan | Phase 4 review of its own roster | Briefs |
| Night | Sleep | `/goal` or a loop on a branch: build, check, commit, log | Commits, `progress.md` |
| Morning, 10 min | Read the report | Phase 6 review by a fresh agent | Receipts |
| Morning, +5 min | Merge or redirect | Phase 8 retro, adds rules | CLAUDE.md, evals |
