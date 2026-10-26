# Guardrails

Use this page when you set permissions, a sandbox or an allowlist, or let an agent read untrusted
input.

## Steps

1. **Start from the premise.** Prompt-level guardrails are not reliable, so put controls at the tool,
   OS and identity boundary (D, built on P and R sources). Enforce with code and request with words.
   [§10](../playbook/agent-harness-playbook.md#10-guardrails)
2. **Prevent: write deny rules for secrets and state files.** Rules evaluate deny, then ask, then
   allow; the first match wins, and an allow cannot carve an exception out of a deny (P). Deny rules
   hold in every permission mode (P).
3. **Prevent: turn the sandbox on and learn its limits.** It covers Bash and its child processes
   only, so Read, Edit, WebFetch, MCP servers and hooks run outside it (P). Set `denyRead` on `~/.ssh`
   and `~/.aws`, add Read deny rules for the same paths, and set `allowUnsandboxedCommands: false`,
   because Claude can retry a failed command outside the sandbox and a matching allow rule approves
   that retry silently (P).
4. **Prevent: put the rules in managed settings.** Managed settings sit above user, project and local
   settings, and `allowManagedPermissionRulesOnly` ignores allow, ask and deny rules from those
   levels, so your deny rules must live in the managed file too (P). Without a managed policy, run
   agents only in checkouts you trust (P).
5. **Prevent: do not treat auto mode as a boundary.** An independent stress test measured 81%
   end-to-end false negatives across 253 actions in deliberately ambiguous scenarios, against the 17%
   Anthropic reports on production traffic (R). Entering auto mode drops blanket allows such as
   `Bash(*)` (P), so remove them on purpose before you rely on it (D).
6. **Prevent: cut one trifecta leg per session.** An agent with private data, exposure to untrusted
   content and a channel to send data out can be steered into exfiltration by injected text (P). For
   example, run with no outbound network while it reads untrusted issues, web pages or new skills (D).
7. **Prevent: lock down headless runs and the code host.** `claude -p` without `--bare` runs the
   repo's hooks and `.mcp.json` servers with no workspace trust prompt (P). Use `--bare` or a trusted
   checkout in CI, run the gate as a CI step (D), and treat issue bodies, PR comments and commit
   messages as untrusted input (P).
8. **Prevent: vet skills, plugins and MCP servers.** A scan of 98,380 community skills confirmed 157
   malicious ones, and poisoned MCP tool descriptions reached up to 72.8% attack success across 45
   live servers (R). Pin versions, read the code, and treat tool descriptions as untrusted input until
   reviewed (D).
9. **Detect: log and alert.** Append every tool call to a log with a PreToolUse hook, and alert on
   denials, repeated blocks and in-project writes to settings, CLAUDE.md, hooks, skills and agent
   definitions (D). Write logs where the agent cannot edit them, and redact secrets (D).
10. **Recover: make every run revertible.** Commit or use a worktree before long runs, and snapshot
    memory and rule files (D). Require human approval, bound to the exact action and shown as a
    dry-run diff, for delete, send, publish, deploy and pay (D).
    [§10.2](../playbook/agent-harness-playbook.md#102-layered-model)

## Checklist

- [ ] Deny rules cover secrets and state files and live in the managed file.
- [ ] The sandbox is on, `denyRead` covers `~/.ssh` and `~/.aws`, and `allowUnsandboxedCommands` is false.
- [ ] Read deny rules cover the same paths, since the sandbox does not cover the Read tool.
- [ ] No blanket allows such as `Bash(*)` remain before I use auto mode.
- [ ] Each session drops at least one leg of the lethal trifecta.
- [ ] Skills, plugins and MCP servers are pinned and read before install.
- [ ] CI runs `claude -p` with `--bare` or in a trusted checkout, with the gate as its own step.
- [ ] Logs, snapshots and approval gates exist for the detect and recover layers.

## Templates

- [Template A. CLAUDE.md skeleton](../playbook/agent-harness-playbook.md#a-claudemd-skeleton): its Never list is advisory, so back each line with a rule or hook.
- [Template G. PostToolUse formatter](../playbook/agent-harness-playbook.md#g-posttooluse-formatter): a hook that runs outside the sandbox, so it uses the project's own Prettier, never `npx`.
- [Template M. PR review workflow with the Claude Code GitHub Action](../playbook/agent-harness-playbook.md#m-pr-review-workflow-with-the-claude-code-github-action): scrubbed environment, minimal `--allowedTools`, no approval.

## Watch out for

These are the playbook's top mistakes
([§10.3](../playbook/agent-harness-playbook.md#103-top-mistakes)).

- **Auto mode as a security boundary.** Also a "95% detection" filter. Treat auto mode as
  convenience.
- **Bypassing permission checks with credentials mounted in the container.** Dev containers do not
  stop credential theft in that case (P).
- **Blanket shell or interpreter allows.** Remove them before you use auto mode.
- **Assuming the sandbox covers Read, hooks or MCP servers.** It does not (P).
- **A cloned repo's settings with no managed policy.** The repo can grant itself permissions.
- **Unreviewed skills and MCP servers.** They run with your full user privileges.

## Go deeper

- [§10.1 Facts to design around](../playbook/agent-harness-playbook.md#101-facts-to-design-around): the lethal trifecta, the sandbox, managed settings, headless runs and supply chain.
- [§10.2 Layered model](../playbook/agent-harness-playbook.md#102-layered-model): prevent, detect and recover.
- [§12.2 GitHub as the gate](../playbook/agent-harness-playbook.md#122-github-as-the-gate): workflow security.
- [§12.4 Guardrail checklist](../playbook/agent-harness-playbook.md#124-guardrail-checklist)
- [§11.5 Risks of running without watching](../playbook/agent-harness-playbook.md#115-risks-of-running-without-watching)
- [Law 9. Enforce with code; request with words](../playbook/agent-harness-playbook.md#law-9-enforce-with-code-request-with-words)
- Page lessons: page Lesson 10 (Guardrails), page Lesson 11 (Running nonstop), page Lesson 12 (Linear + GitHub).
- Related runbooks: [run-unattended](run-unattended.md), [build-a-harness](build-a-harness.md).
