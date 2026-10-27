# Build a harness

Use this page when you set up a harness around Claude for a repository, or need to decide which stage
to build next.

## Steps

1. **Find your level.** The roadmap runs from Level 0 (Chat) through 1 (Grounded agent), 2 (Gated),
   3 (Orchestrated) and 4 (Continuous) to 5 (Self-improving). Each level has a "move up when"
   condition, so add the next level only when that condition holds (D).
   [§17](../playbook/agent-harness-playbook.md#17-maturity-roadmap)
2. **Level 1: write CLAUDE.md from Template A.** It holds build, test and lint commands, conventions
   that differ from defaults, known gotchas, "never" rules and pointers to deeper docs. It leaves out
   what the model does anyway, long documents, secrets and stale history, and it stays short and in
   git (D). Cut generated `/init` output to what the agent can't discover (D).
   [§8](../playbook/agent-harness-playbook.md#8-context-engineering)
3. **Level 1: let the agent run its own tests.** Add Plan mode, the test command in CLAUDE.md and
   allowlisted permissions, and review plans before code (D). Write each plan as a plan file with a
   test per slice (Template D).
4. **Level 2: add the gates.** A Stop hook, a formatter hook, receipts and your first skills, until
   "done" always arrives with proof (D). The runbook is [verify](verify.md).
5. **Level 3: add helpers.** Add scout and reviewer subagents, a critic before build, worktrees for
   parallel builders and file-based handoffs, until you run three or more tasks in parallel without
   collisions (D). The runbook is [orchestrate](orchestrate.md).
6. **Level 4: put state on disk.** Add state files (Template E), loops, schedules, budgets, stop
   conditions and sandboxed unattended runs (D). The runbook is [run-unattended](run-unattended.md).
   Level 5 is [improve](improve.md).
7. **Use Linear as the planning layer.** The tracker holds intent and status. Issues go to humans and
   are delegated to agents, and the human stays the owner (P). Put repo, branch and gate rules in
   agent guidance once, and enforce the real gates in GitHub because guidance is advisory (P).
   [§12.1](../playbook/agent-harness-playbook.md#121-linear-as-the-planning-layer)
8. **Link PRs to issues and give each status one owner.** Put the issue ID in the branch name and
   "Fixes ID" in the PR body, and prefer PR-based links over commit magic words (P). The agent moves
   an issue to In Progress, your team's GitHub automation moves it to In Review, and the merge of a
   PR that says "Fixes ID" moves it to Done (D).
9. **Use GitHub as the gate.** Use rulesets with required checks, require code-owner review
   (CODEOWNERS is read from the base branch), and make CI trigger on `merge_group` if you use a merge
   queue (P). Set `GITHUB_TOKEN` read-only by default and grant write per job (P).
   [§12.2](../playbook/agent-harness-playbook.md#122-github-as-the-gate)
10. **Protect the self-certifying files, then add the PR review (Template M).** Gate config, CI
    workflows, hook scripts, `.claude/`, CODEOWNERS and rulesets decide which checks run, so put them
    behind path rules and code-owner review (D). The review workflow posts findings as a comment and
    never approves.

## Checklist

- [ ] I know my level (0 to 5) and the condition for moving up.
- [ ] CLAUDE.md is short, in git, and holds commands, conventions, never rules and pointers.
- [ ] The agent can run the test command itself.
- [ ] Linear holds intent and status, and GitHub holds the code and the gates.
- [ ] Branch names carry the issue ID, PRs say "Fixes ID", and each status move has an owner.
- [ ] Gate files (gate config, workflows, hook scripts, `.claude/`, CODEOWNERS, rulesets) sit behind path rules and code-owner review.
- [ ] Workflow `permissions:` are read-only by default, and third-party actions are pinned to full commit SHAs.
- [ ] The advisory review workflow posts comments and never approves.

## Templates

- [Template A. CLAUDE.md skeleton](../playbook/agent-harness-playbook.md#a-claudemd-skeleton): commands, conventions, never rules, when unsure, pointers.
- [Template D. Plan file](../playbook/agent-harness-playbook.md#d-plan-file): slices with a test and a rollback each.
- [Template E. Long-running state files](../playbook/agent-harness-playbook.md#e-long-running-state-files): `features.json` and `progress.md`.
- [Template M. PR review workflow with the Claude Code GitHub Action](../playbook/agent-harness-playbook.md#m-pr-review-workflow-with-the-claude-code-github-action): replace each `<full-commit-sha>` before use.

## Watch out for

- **Building a framework before trying one good call.** Try one well-built call with good context
  first ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns), P).
- **A giant CLAUDE.md.** Claude Code's best practices warn that a bloated file gets ignored (P). Keep
  detailed learnings in `docs/solutions/` or skills.
- **Must-happen checks that live only in prose.** Put them in hooks, CI, permissions or the sandbox.
- **An agent that edits its own gates.** Any change to the self-certifying files is high risk (D).
- **Commit magic words.** They can close a Linear issue as soon as a commit lands on the default
  branch, skipping review (P).
- **`pull_request_target`.** It runs base-branch code with secrets, so running PR code there is a
  "pwn request" (P). Do not switch to it to fix fork PRs in Template M.

## Go deeper

- [§17A Mapping onto an existing harness](../playbook/agent-harness-playbook.md#17a-mapping-onto-an-existing-harness): one example, and the gaps to check.
- [§3 Reference architecture](../playbook/agent-harness-playbook.md#3-reference-architecture) and [§3A Claude Code feature map](../playbook/agent-harness-playbook.md#3a-claude-code-feature-map)
- [§8 Context engineering](../playbook/agent-harness-playbook.md#8-context-engineering): what belongs in CLAUDE.md, skills and tool definitions.
- [§12 Toolchain: planning, code host and CI](../playbook/agent-harness-playbook.md#12-toolchain-planning-code-host-and-ci), with [§12.3 Reference pipeline](../playbook/agent-harness-playbook.md#123-reference-pipeline) and [§12.4 Guardrail checklist](../playbook/agent-harness-playbook.md#124-guardrail-checklist)
- [§16 Templates](../playbook/agent-harness-playbook.md#16-templates)
- [§18 Operating the harness: gaps to close](../playbook/agent-harness-playbook.md#18-operating-the-harness-gaps-to-close)
- Page lessons: page Lesson 2 (Ten rules), page Lesson 8 (Toolbox), page Lesson 12 (Linear + GitHub), page Lesson 14 (Prompt library).
- Related runbooks: [guardrails](guardrails.md), [improve](improve.md).
