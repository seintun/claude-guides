# Wiki

Short runbooks distilled from the [playbook](../playbook/agent-harness-playbook.md). Each one gives the steps, a checklist, the templates to copy, the pitfalls, and links into the playbook for the detail. A wiki page adds no facts of its own; when it and the playbook disagree, the playbook wins.

| Runbook | Use it when | Phase in the [orchestration index](../orchestration-index.md) |
|---|---|---|
| [Start a task](start-a-task.md) | An idea or pain point needs to become work Claude can finish and check | 1 Shape, 2 Brief, 3 Plan |
| [Grill](grill.md) | Settling the design with one question at a time before any plan or spec; includes how to validate and test a grill | 1 Shape |
| [Orchestrate](orchestrate.md) | Deciding what the lead does and what goes to helper agents | 4 Orchestrate, 5 Build |
| [Verify](verify.md) | Turning "done when" into gates, receipts and independent review | 6 Check |
| [Run unattended](run-unattended.md) | Claude keeps working while you are away | 7 Overnight |
| [Guardrails](guardrails.md) | Setting permissions, the sandbox and safe defaults | 7 Overnight |
| [Build a harness](build-a-harness.md) | Setting up CLAUDE.md, hooks, state files, CI and the roadmap | All |
| [Unstick](unstick.md) | A run goes wrong: the agent loops, claims done too early, repeats a mistake, loses context or overbuilds | Any |
| [Records](records.md) | Deciding where decisions, plans, state and scratch live, and the flow from grill to merged PR | Any |
| [Improve](improve.md) | After real work: retros, evals, the scorecard, pruning | 8 Learn |
| [Case study](case-study.md) | Seeing every step applied to this repository's own build | All |

For a phase-by-phase review checklist, use the [orchestration index](../orchestration-index.md). For commands and a prompt template, use the [cheat sheet](../playbook/claude-cheat-sheet.md).
