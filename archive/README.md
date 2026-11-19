# archive

Read-only snapshots of earlier versions of the guide, kept so older conventions and the reasons they changed stay readable. The live guide is the source of truth; nothing here is current advice. Agents: never route to a file in this folder unless the user asks about history.

Each snapshot is made by `python3 -I tools/archive_snapshot.py` from a git tag. Its relative links are rewritten to GitHub permalinks at that tag, so they keep pointing at the text as it was. Never edit a snapshot by hand.

## Snapshots

| Version | Date | Tag | What it holds |
|---|---|---|---|
| [v0.6](v0.6/) | 2026-10-27 | `guide-v0.6` | [Playbook 0.6](v0.6/playbook/agent-harness-playbook.md), [cheat sheet](v0.6/playbook/claude-cheat-sheet.md), [wiki](v0.6/wiki/README.md), [ENTRY.md](v0.6/ENTRY.md), [orchestration index](v0.6/orchestration-index.md), the offline compendium (`v0.6/docs/orchestrating-claude-compendium.html`), and teaching page v17 (`site/history/orchestrating-claude-v17.html`) |

Older teaching pages live in [site/history/](../site/history/) (v11 is the baseline of the UX issue).

## Superseded conventions

What an earlier version advised, what replaced it, and why. Each row cites the evidence behind the change; the full record is in `research/agentic-practices-2026-11.md` (added with playbook 0.7). Grades follow the playbook: [P] primary, [S] secondary, [R] research, [D] design inference.

| Earlier convention | In | Replaced by | Why |
|---|---|---|---|
| Lead with "Explore, plan, implement, commit" as the headline workflow | Playbook 0.6 §3A, condensing the official best-practices page as it read on 2026-10-24 | A ladder of checks: give Claude a pass/fail check, then `/goal`, a Stop hook, a fresh reviewer. Planning stays for non-trivial work | The current best-practices page has no "Explore, plan, implement, commit" heading and builds its advice around checks [P: code.claude.com/docs/en/best-practices, checked 2026-11-18] |
| Turn every correction into a CLAUDE.md rule | Playbook 0.6 Law 8 | A correction ladder: fix a repeated mistake at the highest layer that works (architecture or API, then lint, types and tests, then runtime checks), with a CLAUDE.md or skill line last | Prose rules fail where checks hold: Karpathy saw errors persist "despite a few simple attempts to fix it via instructions in CLAUDE.md" [P: x.com/karpathy/status/2015883857489522876, 2026-01-26]; Lauren Tan turns each correction into "a deterministic check" [P: youtube.com/watch?v=O_zcc6Xl12g, 3:08, 2026-11-14]; OpenAI enforces architecture with custom linters [P: openai.com/index/harness-engineering, 2026-02-11] |
| Use subagents to protect the context window | Playbook 0.6 §3A model row and §8 | Keep context small through structure: state in files and git, a fresh session per unit, workflow scripts for fan-outs. Subagents stay for parallel, noisy or independent-review work | The best-practices page now lists "Use subagents to protect your context window" as old advice [P, checked 2026-11-18]. Boris Cherny's team tip of 2026-01-31 still recommends it [P: x.com/bcherny/status/2017742755737555434], so the change is dated, not a contradiction of his practice |
| Add IMPORTANT or ALL CAPS to instructions Claude keeps missing | Common community advice | A check or hook for anything that must happen | The best-practices page retires it: emphasis makes Claude over-apply the rule [P, checked 2026-11-18] |
| Sessions start in Manual (default) permission mode | Playbook 0.6 §3A | Interactive sessions start in auto mode when no mode is set (v2.1.283 for third-party providers or telemetry off; v2.1.284 for every plan and provider). `claude -p` and the Agent SDK start in Manual mode (v2.1.302) | Claude Code changelog and permission-modes page [P, checked 2026-11-18] |
| Sandboxed Bash commands run without a prompt | Claude Code before v2.1.325 | Sandboxed Bash follows the normal permission flow unless `sandbox.autoAllowBashIfSandboxed: true` | Changelog v2.1.325 [P] |
| A self-paced `/loop` schedules a fallback wakeup about 20 minutes later | Scheduled-tasks docs | A self-paced loop ends when a turn does not reschedule; `CLAUDE_CODE_LOOP_KEEPALIVE=1` restores the old behaviour | Changelog v2.1.319 [P]. The docs page still describes the fallback |
| Most sessions start in Plan mode | Boris Cherny, 2026-01-02 [P: x.com/bcherny/status/2007179845336527000] | Plan anything non-trivial, through plan mode or a spec; auto mode is now the default mode | Auto mode became the default in v2.1.283 to v2.1.284 [P]. Recaps from June 2026 say Cherny moved to auto mode [S], so the January advice is kept as dated practice |
