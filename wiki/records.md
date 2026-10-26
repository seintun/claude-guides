# Where records live

Use this page when agent work produces decisions, plans or state that must outlive one chat: a grill, a plan, a long run, delegated helpers, a ticket.

## Why not the chat

- Recall degrades as the context window fills, so treat it as a budget (P). [Law 4](../playbook/agent-harness-playbook.md#law-4-context-is-a-budget-not-a-bin)
- Models forget between sessions; the countermeasure is CLAUDE.md, memory and progress files (P). [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)
- Long runs keep progress and decision files outside the window (P). [§8](../playbook/agent-harness-playbook.md#8-context-engineering)
- Helpers write outputs to files and pass back references, never raw transcripts (P). [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol)

## Steps

1. **Sort each record by lifetime** (D), using the table below.
2. **Write decisions in the repo,** not only in chat: question or decision, answer, reason, date (D). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
3. **Keep task state in files:** JSON for status the agent must not casually rewrite, Markdown for notes, git as the audit trail (P). [§8](../playbook/agent-harness-playbook.md#8-context-engineering), [§11.1](../playbook/agent-harness-playbook.md#111-the-long-running-harness-recipe)
4. **Track the work item in the tracker** and link both ways: the issue links the plan file, and the plan names the issue id (D). PRs link the issue by id in the title, with "Fixes ID" in the body (P). [§12.1](../playbook/agent-harness-playbook.md#121-linear-as-the-planning-layer)
5. **Push decisions with the branch,** so reviewers, CI and other sessions see them and they merge with the code (D).
6. **Close out:** when the task merges, fold lasting decisions into `docs/decisions.md` or the plan, and delete progress files and scratch (D).

| Record | Where | Commit and push? |
|---|---|---|
| Grill decisions | `docs/discovery/<topic>.md` | Yes |
| Plan and its decisions | `docs/plans/<task>.md` (Template D) | Yes |
| Routing and other lasting decisions | `docs/decisions.md`, one dated line each | Yes |
| Long-run state | `features.json`, `progress.md` (Template E) | Yes while the run lasts; delete or fold in at the end |
| Work item, status, blockers | The tracker issue (Template L), short comments | Lives in the tracker |
| Final receipt | The PR description, one line in the issue | With the PR |
| Prompts that `/prompt` generates | The guide's `prompts/<project>/`, git-ignored ([prompts/README.md](../prompts/README.md)) | No: kept on your machine only |
| Helper output, transcripts, dumps | An ignored folder (for example `.agent/`) or the session scratchpad | No |

## Recommended flow

1. `/grill <idea>` logs each decision to `docs/discovery/<topic>.md`.
2. Write the issue with Template L and link the discovery file.
3. Branch `<issue-id>-<slug>`; `/guide` logs the chosen route to `docs/decisions.md`; the plan in `docs/plans/<task>.md` names the issue id.
4. Helpers write findings to scratch files and return a summary with paths.
5. Open the PR with the issue id in its title, "Fixes ID" and the receipt in its body.
6. Merge; the issue closes, and the decisions land on `main` with the code.

## Checklist

- [ ] No decision exists only in chat.
- [ ] Each decision line has a date and a reason.
- [ ] The issue links the plan, and the plan names the issue id.
- [ ] Scratch output is ignored by git.
- [ ] Progress files were deleted or folded in when the task closed.

## Templates

- [Template D. Plan file](../playbook/agent-harness-playbook.md#d-plan-file): the Decisions list.
- [Template E. Long-running state files](../playbook/agent-harness-playbook.md#e-long-running-state-files): `features.json` and `progress.md`.
- [Template L. Agent-ready issue](../playbook/agent-harness-playbook.md#l-agent-ready-issue): the tracker item.

## Watch out for

- **Two copies of one log.** A ticket and a file drift apart; link, don't copy.
- **One log file per session.** Use one file per topic or task.
- **A temporary worktree as storage.** Uncommitted files go when it is cleaned up; commit decisions on the branch.
- **A repo you don't own.** Keep logs in your own notes, and post only the decisions into the PR or ticket.
- **Linear agent threads get archived** (S), so durable state lives in files or labels. [§12.1](../playbook/agent-harness-playbook.md#121-linear-as-the-planning-layer)

## Go deeper

- [§8 Context engineering](../playbook/agent-harness-playbook.md#8-context-engineering)
- [§11.1 The long-running harness recipe](../playbook/agent-harness-playbook.md#111-the-long-running-harness-recipe)
- [§12.1 Linear as the planning layer](../playbook/agent-harness-playbook.md#121-linear-as-the-planning-layer)
- Related runbooks: [grill](grill.md), [orchestrate](orchestrate.md), [run-unattended](run-unattended.md).
