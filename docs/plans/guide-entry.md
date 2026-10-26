# Plan: a guide any Claude session can call
Goal: any Claude Code session on this machine, in any project, can call this repository and be routed to the right sections, runbook and template for its scenario.    Risk: normal    Status: done

## Task contract (Template B)

```text
GOAL
Any local Claude Code session, in any folder, can call claude-guides (a /guide skill,
a one-line CLAUDE.md pointer, or a paste-in prompt) and reach the right playbook
sections, runbook and template for its scenario in at most 2 hops, without loading
the whole playbook.

RISK: normal (new files, docs and one symlink in ~/.claude; no schema, auth or data)

DONE WHEN
1. ENTRY.md exists, is under 150 lines, and routes any request to phase, runbook,
   template and sections in at most 2 hops.               check: wc -l; cold test
2. Its scenario router has at least 15 rows, each with Read, Template and Output.
                                                           check: row count script
3. /guide skill, CLAUDE.md snippet and paste-in prompt live in skills/guide/ with
   install steps, and each passes a cold test from a folder outside this repo.
                                                           check: claude -p runs
4. The repo root resolves from one place (git, from the skill's own folder; the
   installer fills the snippet and prompt), documented in skills/guide/README.md.
5. All runbooks have Steps, Checklist, Templates, Watch out for and Go deeper, and
   link into the playbook. check: python3 -I tools/check_links.py prints PASS.
6. No route loads the whole playbook: sections come out through tools/section.py.
   Token load for 3 sample scenarios is measured and reported.
7. README, AGENTS, llms.txt and the compendium reflect the new structure; the
   compendium is rebuilt and its checks pass.
8. Small, logical commits on feat/guide-entry, with no AI attribution.

CONSTRAINTS
- The playbook stays the source of truth: restructure, link and distill only.
- Keep playbook section numbers and page lesson ids stable.
- Don't publish the artifact. Touch ~/.claude only to add the skill symlink, after
  showing the change.

BUDGET
- One session, up to 3 helpers at a time; stop and report after 2 failed attempts
  at the same check.

STOP AND ASK ME IF
- the design needs renaming or moving the playbook
- a scenario has no playbook coverage at all
- anything is hard to undo
```

## Design

- **Entry file: `ENTRY.md` at the repository root.** It is the one file an outside session reads first. It holds the scenario router, a phase table that points into `orchestration-index.md`, and the rules that apply everywhere (receipts, one writer, fresh review, budgets). `orchestration-index.md` stays as the phase index with its review checklists. `AGENTS.md` stays for agents editing this repository.
- **Sections, not files.** `tools/section.py <id>` prints one playbook section or template (for example `9.5`, `F`, `law-7`), or a cheat-sheet section (`cs:3`). Read can't follow `#anchors`, so this is how a session loads one section without the rest of a 1,500-line file. Every router row names section ids.
- **Root resolution, one place.** The skill runs `git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel`, which follows the symlink back to the clone. `skills/guide/install.sh` computes the same root once and fills it into the printed snippet and prompt. `skills/guide/README.md` documents this, and is the only place that does.
- **Thin scenarios** (bug fix, refactor, migration, guard hooks, cost blowup, multi-repo, parallel writers) route to their nearest sections, labelled "thin", with the gap named. They need no new facts. The gaps are listed as a follow-up.
- **Stuck agent** gets a runbook, `wiki/unstick.md`. It is distilled from §4, §14, §15, §11.3 and cheat sheet §3. It is the one common scenario with no runbook today.

## Slices
| # | Change | Test that proves it | Rollback | Status |
|---|--------|---------------------|----------|--------|
| 1 | `tools/section.py`: print one section, template, law or cheat-sheet section by id | `python3 -I tools/section.py 9.5`, `F`, `law-7`, `cs:3` each print one section; an unknown id exits 1 | `git revert` | done |
| 2 | `ENTRY.md` with the scenario router (18 rows) and phase table | `wc -l ENTRY.md` < 150; every section id in it resolves via `section.py`; `check_links.py` PASS | `git revert` | done |
| 3 | `wiki/unstick.md`, and runbook fixes from the audit (the "page Lesson" references explained, the playbook's sample pointer path) | `check_links.py` PASS; the runbook has all five parts | `git revert` | done |
| 4 | `skills/guide/`: SKILL.md, snippet.md, prompt.md, install.sh (a dry run by default), README.md | `bash -n` and `shellcheck` on install.sh; the dry run prints the symlink it would create | `git revert` | done |
| 5 | Install the skill: one symlink in `~/.claude/skills/` (you run the command; the sandbox protects `~/.claude/skills`) | `ls -l ~/.claude/skills/guide` points at the clone | `rm ~/.claude/skills/guide` | done |
| 6 | Token measurement for 3 scenarios, in `skills/guide/README.md` | a script sums ENTRY.md, SKILL.md and each `section.py` output (chars / 4) | `git revert` | done |
| 7 | README, AGENTS, llms.txt, compendium builder; rebuild | `check_links`, `check_privacy`, `static.sh` and the compendium browser check PASS | `git revert` | done |
| 8 | Cold test: a fresh `claude -p` session in a folder outside the repo solves 3 scenarios, once each through /guide, the snippet and the prompt. Then fix what it finds | each run names the right row, sections and template, and reads no whole playbook | n/a | done |

## Decisions
- 2026-10-24 Reach is local sessions on this machine only, because the repository has no remote yet. (Answer to question 1.)
- 2026-10-24 Install /guide as a symlink to `skills/guide/`, so repository edits reach every session and no path is baked in. (Answer to question 2.)
- 2026-10-24 Thin scenarios route to stand-ins and are flagged, with no new content. (Answer to question 3.)
- 2026-10-24 The CLAUDE.md snippet is a plain pointer, not an `@` import, because an import loads the whole file into every session (memory docs).

- 2026-10-24 Added `wiki/grill.md` and a `/grill` skill with a cold test, at the user's request during the build. The test passed all 8 checks in 3 of 3 runs.
- 2026-10-24 The cold review changed rows 5, 7, 9 and 12 and ENTRY.md's how-to. `/guide` now finds its root by running git itself, because the pre-run shell line stalled a `claude -p` session.

## Open questions
- Should the cloud variant (GitHub raw URLs) follow once the repository is public? (owner: human)
