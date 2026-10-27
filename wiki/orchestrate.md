# Orchestrate

Use this page when a task is big enough that you must decide whether the lead agent should hand part
of it to helper agents.

## Steps

1. **Default to one writer.** One agent writes each set of files, and each builder works in its own
   git worktree (D). The evidence backs this: pick the topology by task shape and default to one
   writer (R). [§19.1](../playbook/agent-harness-playbook.md#191-findings-that-hold-up)
2. **Ask whether you need a helper at all.** Start with the simplest solution, because many tasks
   need one well-built call, not an agent (P). If one call with good context is enough, stop here.
3. **Send a helper when the job fits.** Send wide reading where you only need the conclusion, jobs
   that do not depend on each other, judgments from someone who did not do the work, and cheap
   search or summary jobs. Keep a job in the lead when it is a handful of steps, needs every detail,
   takes longer to brief than to do, or would have two helpers editing the same files. Both lists
   come from page Lesson 6 (Orchestration).
4. **Match the task shape to a pattern.** Known steps and independent parts: parallel sectioning.
   Known steps that depend on each other: a prompt chain with checks. Unknown steps and read-heavy
   work: orchestrator-workers. Work that spans many sessions: an initializer plus incremental
   workers, or a Ralph loop. Anything else: one agent running plan → critique → build. For one
   trustworthy metric use a hill-climbing loop; for a judgment call with no test use a council or an
   adversarial review. [§6](../playbook/agent-harness-playbook.md#6-orchestration-patterns)
5. **Write the brief.** Give each helper an objective, context (what is already ruled out), scope,
   tools, output, budget and a stop rule (D). Vague briefs cause duplicated work and gaps (P). Use
   Template C for read-only work.
6. **Say what comes back.** Ask for a short summary, findings with file:line or URL and a confidence,
   unknowns and artifact paths (D). Have helpers write long output to files and pass paths back, to
   avoid a "game of telephone" (P). For unfamiliar work, search the repo first, then the official
   docs, then other projects for ideas, not code (D). [§5.4](../playbook/agent-harness-playbook.md#54-delivery-phases)
7. **Scale effort to the task.** Use 1 agent and 3 to 10 tool calls for simple fact-finding, 2 to 4
   subagents with 10 to 15 calls each for a direct comparison, and more than 10 only for complex
   research (P). Cap agents per task and calls per agent in the lead's prompt (D).
8. **Launch in parallel and keep the plan on disk.** Anthropic reports that spawning subagents in
   parallel cut research time by up to 90% (P). The lead saves its plan, because context beyond
   200,000 tokens gets truncated (P); Template D is a plan file.
9. **Treat each report as a claim.** The lead re-checks any claim that drives a decision, and passes
   summaries and file paths between agents, never raw transcripts (D).
10. **Stop on a repeat failure.** If the same check fails twice for the same reason, stop and get a
    second opinion from a fresh agent instead of retrying (D).
    [§4](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent)

## Checklist

- [ ] One agent writes each set of files, and each builder has its own worktree.
- [ ] I can say why this task needs helpers, or I kept it in the lead.
- [ ] I named the task shape and the pattern that fits it.
- [ ] Every helper has a written brief with objective, scope, output, budget and stop rule.
- [ ] Helpers return summaries and file paths, not transcripts.
- [ ] The fan-out has a cap on agents per task and calls per agent.
- [ ] The lead re-checked every claim that drives a decision.
- [ ] The plan file is current.

## Templates

- [Template C. Subagent brief](../playbook/agent-harness-playbook.md#c-subagent-brief): read-only work for a helper. For a builder, use the brief schema in [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol) and set the scope to what it may touch.
- [Template D. Plan file](../playbook/agent-harness-playbook.md#d-plan-file): slices, each with its test and rollback.
- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): sets the helper budget and the second-opinion rule.

## Watch out for

- **Fanning out tightly coupled edits.** In Google Research's study, multi-agent setups lost 39 to
  70% on sequential planning (R). Coupled edits belong in one agent
  ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns)).
- **Agents with no central lead.** Independent agents amplified errors 17.2× versus 4.4× with a
  central orchestrator, both relative to a single agent (R).
- **Adding agents to a task one agent already handles.** Gains shrank, and often turned negative,
  once a single agent scored above about 45%; that is a fitted estimate, not a hard cutoff (R).
- **Ignoring the token bill.** Orchestrator-workers costs about 15 times the tokens of a chat, where
  a single agent uses about 4 times (P).
- **Agent teams.** They are experimental, off by default and have no worktree isolation, so partition
  the files yourself (P).
- **Passing transcripts between agents.** Pass files and summaries instead
  ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns)).

## Go deeper

- [§3 Reference architecture](../playbook/agent-harness-playbook.md#3-reference-architecture): the lead, the workers and the gates on one page.
- [§3A Claude Code feature map](../playbook/agent-harness-playbook.md#3a-claude-code-feature-map): subagents, workflows, worktrees and agent teams, with limits.
- [§6 Orchestration patterns](../playbook/agent-harness-playbook.md#6-orchestration-patterns): sixteen patterns and the decision chart.
- [§7 Delegation protocol](../playbook/agent-harness-playbook.md#7-delegation-protocol): brief schema, return schema and house rules.
- [Law 10. Spend compute where it buys accuracy](../playbook/agent-harness-playbook.md#law-10-spend-compute-where-it-buys-accuracy)
- [§19 Proven orchestration: what the evidence says](../playbook/agent-harness-playbook.md#19-proven-orchestration-what-the-evidence-says)
- Page lessons: page Lesson 6 (Orchestration), page Lesson 7 (Patterns), page Lesson 8 (Toolbox), page Lesson 17 (Evidence).
- Related runbooks: [start-a-task](start-a-task.md), [verify](verify.md).
