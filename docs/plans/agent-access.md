# Plan: make the guide readable by any agent, local or remote
Goal: an agent with no clone of this repository can find and load the right playbook guidance in at most 2 fetches over plain HTTP, with the same routing ENTRY.md gives a local session. No server, no new dependency. Skills install with `npx skills add <owner>/claude-guides`.    Risk: normal    Status: built on feat/agent-access; the remote cold test waits for a push

## Where it stands (review, 2026-10-25)

What already works for a local agent with a clone:

- `ENTRY.md` (72 lines) routes 19 scenarios and 8 phases to section ids, a runbook and a template.
- `tools/section.py` prints one section by id (78 ids: sections, laws, templates, cheat sheet). A typical route (`9.5 F`) costs about 6 KB instead of the 137 KB playbook.
- `llms.txt`, a README in every folder, and `AGENTS.md` give a map. `tests/run.sh` passes (225 tests, under 9 s) and guards the router.
- `/guide`, a CLAUDE.md snippet and a paste-in prompt call the guide from other projects.

Score for agent scanning: about 8/10 locally, 3/10 remotely.

Gaps:

1. **Drift.** README and `llms.txt` say "18 scenarios"; the router and `tests/scenarios/routing.json` have 19. No test catches it.
2. **Clone required.** Every route goes through `python3 GUIDE/tools/section.py`. A remote agent (claude.ai, a cloud session, another vendor's agent) cannot run it, and the 137 KB playbook is too big to fetch whole.
3. **No structured index.** Section ids, titles, line counts, grades and the router live only in Markdown tables. A tool must parse them.
4. **No search.** An agent that does not match a router row has no way to find a section by keyword, short of reading the playbook.
5. **Noise for scanners.** `tests/live/**` (about 150 files of run records) and `issues/drafts/` sit next to the guidance. `llms.txt` steers well, but a raw tree walk or a repo-to-text packer pulls them in.

## Design

Plain files only. One generator, run like the compendium build; `tools/section.py` already knows how to split the playbook, so reuse it.

```text
playbook + ENTRY.md + wiki
        |
tools/build_index.py  (new, stdlib only)
        |
        +--> guide-index.json   router rows, phases, section ids, titles, grades, sizes, paths
        +--> sections/<id>.md   one file per id, generated, never hand-edited
```

An agent with a clone keeps using `section.py`. An agent without one fetches `guide-index.json` (or ENTRY.md), then `sections/<id>.md` by raw GitHub URL. The playbook stays the source of truth; `tests/run.sh` fails when the generated files are stale.

Not doing: an MCP server, a hosted service, embeddings or search. Each adds a process or dependency to maintain, and plain files already reach every agent that can read a file or fetch a URL. Revisit only if the slice 3 cold test fails.

## Slices

| # | Slice | Done when | Check |
|---|---|---|---|
| 1 | Fix drift; guard it | README and `llms.txt` say 19; a test fails when the router row count and any "N scenarios" claim disagree | `tests/run.sh`; mutation suite catches a changed count |
| 2 | `tools/build_index.py` writes `guide-index.json` and `sections/<id>.md` | One file per id from `section.py --list`; stale output fails the suite | `tests/run.sh`; `python3 -I tests/mutation/mutate.py` |
| 3 | Remote read path | ENTRY.md and `skills/guide/prompt.md` add a "no clone" route by raw URL; `llms.txt` lists the index and `sections/` | A cold session with fetch only and no clone routes 3 sample scenarios in at most 2 fetches |
| 4 | Trim scanner noise | `.gitattributes` marks `tests/live/**`, `issues/drafts/**` and generated files `linguist-generated` | `git check-attr` on a sample path |

| 5 | Portable skills | `/grill`, `/prompt` and `/guide` install with the skills CLI, which finds `skills/<name>/SKILL.md` and copies the folder. `/guide` falls back to remote mode (raw URLs; repo from the user's link, `CLAUDE_GUIDES_REPO`, or one question) when it finds no clone; `/prompt` saves to `~/.claude-guides/prompts/` | `tests/test_docs.py` AgentEntry; `npx skills add . --list` NOT RUN (blocked in the build session) |

The owner's GitHub handle is a private term in `.privacy-terms`, so committed files write `<owner>` and agents take the real value from the link they were given.

Maintenance after this: one more generated output, rebuilt by one command and guarded by the suite. Nothing runs between edits.

## Constraints

- Playbook section numbers, template letters and page lesson ids stay stable; `sections/` filenames use the same ids.
- Generated files are never hand-edited, like `site/index.html` and the compendium.
- Privacy check passes on every generated file.
- No fact changes: this plan moves and indexes content only.

## Open questions

- Should `sections/` be committed, or built in CI and published as a release asset? Committing keeps raw URLs working with no infrastructure.
