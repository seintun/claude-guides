# The main branch: how it was formed on 2026-10-25

This repository had no `main` branch and no remote until 2026-10-25. The work lived on four branches, each cut from the tip of the one before, so the history was one straight line. `main` was created at the tip of `feat/prompt-v10`, which contains all four. This record says what `main` holds, how it was checked, which branches it replaces and what each clone must set up.

## Public release

The repository was published as one commit, the 1.0.0 release, on 2026-10-25. The private history had commits with a client name and a personal path that later commits removed, so it was squashed rather than pushed. The commit hashes in this record, in `docs/plans/` and in `tests/live/` refer to that private history, which the owner keeps on a local branch. They do not exist in the public repository. The release is tagged `v1.0.0`, with a GitHub release made from the tag.

## What main contains

128 commits, from 2026-10-24 to 2026-10-25, in four stretches, plus the commit that adds this record:

| Stretch | Branch that held it | Commits | What it added |
|---|---|---|---|
| 1 | `docs/orchestrating-claude-compendium` | 21 (from the root commit, 64fc579) | The teaching page and its baseline, the agent harness playbook (0.4, then 0.5 after the v0.3 fact-check), the decision, session and version logs, the page check harness, the orchestration index, the cheat sheet, the wiki, the offline compendium and its builder, `llms.txt` and folder READMEs, the privacy rule, and the first `/brief` skill |
| 2 | `feat/port-brief-rules` | 53 | The guide entry point (`ENTRY.md`, `tools/section.py`, `/guide`), `/grill`, the unstick and records runbooks, the offline test suite and both mutation suites, `/prompt` v1 to v4, bounded review, and the port of `/brief`'s rules into `/grill` and `/prompt` with `check_prompt.py` |
| 3 | `feat/guide-entry` | 32 | `/prompt` v5 (the consistency pass), v6 (the `/brief` port merged in), v7 (the stable baseline), the frozen evaluation, and v8 and v9, each built, failed against v7, reverted and archived |
| 4 | `feat/prompt-v10` | 22 | `/prompt` v10: v7 plus six playbook-required items, the measurement behind it, and the outside Codex judge ([docs/plans/prompt-v10.md](plans/prompt-v10.md)) |

## How /prompt reached v10

| Version | Commit | What changed | Outcome |
|---|---|---|---|
| v1 to v4 | d2d5bbc to fa8d90a | Save in the guide, the Write tool, bounded reviews | Beat a plain request 6 of 6 from v2 on |
| v5 | bcbd07f | Consistency pass (step 8) | Beat v4 4 of 6; 10 contradictions against 12 |
| /brief port | e4cf8b3 | `/brief` retired; its 7 rules moved into `/grill` and `/prompt`; `check_prompt.py`; fresh review before saving | Dry-run failures 13, 10, 9 of 30 over three rounds |
| v6 | 1f3bdf5 | The port merged into `/prompt` | Tied v5 6 of 12; contradictions 3 against 7; dry run 4 of 30 |
| v7 | 53370f1 | Where the work lives, figures marked once, three review questions | Tied v6; dry run 3 of 60; became the baseline |
| v8 | a533946, reverted in 222224b | A shorter, risk-sized skill | Lost 11 of 12 and dropped must-haves; archived |
| v9 | eac68c0, reverted in 2e19a81 | v8 plus what it dropped | Lost 7 of 12 and failed five gates; archived |
| v10 | fc7b699 to 9a4f405 | v7 plus R1 to R6 (below) | Kept |

The skill grew from 1,108 words at v1 to 2,140 at v7 and 2,375 at v10. v8 and v9 tried to shorten it and lost quality both times.

## What v10 adds

Each item is one commit and can be reverted alone (see below).

| Item | Commit | Change to the prompts `/prompt` writes | Playbook |
|---|---|---|---|
| R1 | e2106d8, guarded by e4b1660 | A `Risk: trivial`, `normal` or `high` line set by a rule; the trivial form keeps every part but CONTEXT; check c-9 fails a prompt with no risk line | Templates B and L, §5.3 |
| R2 | 67f3ce7 | Normal and high prompts end with a fresh review of the diff against DONE WHEN | §9.3 |
| R3 | fde9c62 | High-risk prompts name the gate behind each hard constraint | Law 9 |
| R4 | 63586f2 | Helper briefs say what is ruled out and decided | Template C |
| R5 | 3f39cf3 | Loops send, charge or create nothing twice, get only the permissions they need, and report in 15 lines or fewer | §11.3, Template H |
| R6 | 9a4f405 | Plan files go to `docs/plans/<task>.md` | Template B |

A variant called D3 was tested and not shipped: its gain was inside the noise margin. It is archived in [tests/live/prompt/variants/](../tests/live/prompt/variants/README.md).

## How v10 was measured

Evidence for every number: [tests/live/prompt/round14/](../tests/live/prompt/round14/README.md).

| Measure | v10 | v7 | Better is |
|---|---|---|---|
| Blind pairs, Claude judges (24 judgments) | 7.79, 19 wins | 7.00 | higher |
| Blind pairs, Codex judge (same files) | 6.58, 10 wins | 6.63 | higher |
| Must-haves lost | 0 | — | lower |
| Contradictions (two audits) | 15 | 12 | lower |
| Dry-run failures, same method, Claude judge | 7 | 7 | lower |
| Dry-run failures, same method, Codex judge | 16 | 19 | lower |
| False PASS in two prompts run to completion | 0 | — | lower |

Read: v10 is no worse than v7 under both judges. That it is better holds only under Claude. Contradictions rose 25%, inside the noise margin; that is the first thing to watch in v11. The baselines for the battle and dry-run gates were moved to fresh v7 runs during the work, with the user's approval each time, because the older v7 material had been made by a different method (the plan's Decisions section records each step).

## Checks at the merge

Run on the commit that became `main`:

| Check | Command | Result |
|---|---|---|
| Offline suite | `tests/run.sh` | SUMMARY all PASS, 225 tests |
| Privacy | `python3 -I tools/check_privacy.py` | PASS |
| Links | `python3 -I tools/check_links.py` | every line PASS |
| Entry router | `python3 -I tools/check_entry.py` | PASS |
| File mutations | `python3 -I tests/mutation/mutate.py` | 23 of 23 caught |
| Review edits | `python3 -I tests/mutation/review_edits.py` | 75 of 75 caught |
| Per-item revert | `git revert` of each of R2 to R6, and of R1 with its guard commit, in a scratch clone | no conflicts; after a compendium rebuild and a lower test floor, the suite passes |

## Branches

| Branch | State against main | What happens to it |
|---|---|---|
| `docs/orchestrating-claude-compendium` | fully contained | can be deleted |
| `feat/port-brief-rules` | fully contained; checked out in `.claude/worktrees/port-brief-rules` with no uncommitted work | remove the worktree, then the branch |
| `feat/guide-entry` | fully contained | can be deleted |
| `feat/prompt-v10` | same commit as `main` at the merge | can be deleted |
| `feat/prompt-v10-pre-rewrite` | v10's history before it was rewritten for clean reverts: same content, older layout, no Codex commits | backup; delete once v10 has been in use for a while |
| `feat/prompt-v10-rebuilt`, `feat/prompt-v10-rebuilt2` | two superseded rebuild attempts | delete |
| `stash@{0}` (on `feat/guide-entry`) | a half-finished v8 draft; the finished v8 is archived | drop |

Deleting branches and worktrees is left to the owner. On 2026-10-25 the owner removed the worktree, deleted every branch above except `feat/prompt-v10` and `feat/prompt-v10-pre-rewrite`, and dropped the stash. After the public release the owner also deleted `feat/prompt-v10` and `feat/prompt-v10-pre-rewrite`. The private history lives only on the local branch `archive/private-history`, whose push remote is set to one that does not exist, so a plain `git push` from it fails.

## Setup each clone needs

```bash
git config merge.ours.driver true
```

`.gitattributes` marks the generated compendium `merge=ours`, so a merge or revert keeps the current copy instead of conflicting on it. Without this setting git treats it as an unknown driver and stops on a conflict. After any merge or revert, rebuild the generated files:

```bash
python3 -I tools/build_compendium.py
```

## Reverting one v10 item

```bash
git revert <commit>
```

Use the commit from the table above. For R1, revert its guard commit e4b1660 first, then e2106d8. Then rebuild the compendium, lower `min_test_cases` in `tests/baselines/suite.json` to the new test count in the same commit (the file's note asks for that), and run `tests/run.sh`.

## Next

1. Use `/prompt` on real tasks for a few days and note each prompt's risk size, contradictions and failures.
2. v11, from the backlog in [docs/plans/prompt-v10.md](plans/prompt-v10.md): fix the measurement method before collecting evidence (frozen runner brief, fresh trials, Codex as a standing second judge), move rules from prose into `check_prompt.py`, lower contradictions, and test an on-demand split of the skill as a single change.
3. Work on a branch cut from `main` and merge it through a pull request; `main` holds only the 1.0.0 release commit and what follows it.
