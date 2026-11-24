# Plan: the /repo-map skill

Date: 2026-11-23. Tier: T1 (new skill, about 300 to 400 lines over 8 files, no T2 trigger). Branch: `repo-map-skill`.

## Goal

A skill anyone can install from GitHub (`npx skills add seintun/claude-guides --skill repo-map`) and run in an unfamiliar repository to get a short, checkable map: what the components and services are, where things live, what the project's words mean, and what is still unknown. Done when the skill, its check script and its tests are in the repository, `tests/run.sh` ends SUMMARY all PASS, and a run on a real repository produces a map that passes the check script.

## Why build one

Existing skills (rdilruba/codebase-map, two "repo-atlas" skills, cartographer, codebase-explainer, codebase-onboarding, eigenwise map-codebase) write 10 or more files, and few check their own claims. One (eigenwise) loads its map into every session, which playbook §8 advises against. The research is in `docs/proposals/repo-ramp-up-workflow.md`.

## Conventions it adopts

| Convention | Source | Grade |
|---|---|---|
| A short codemap of coarse modules; name files and types, don't link them; call out invariants and boundaries; revisit rarely | matklad, "ARCHITECTURE.md" (2021) | D |
| A glossary of domain terms only, no implementation, with aliases to avoid; one glossary per context, a map file when there are several | mattpocock domain-modeling skill, GLOSSARY-FORMAT.md | D |
| Services described as Component (service, website, library), API, Resource and System, each with an owner | Backstage system model docs | P (for the model) |
| A commit stamp so drift is visible | rdilruba/codebase-map, eigenwise map-codebase | D |
| Unproven facts are UNKNOWN, never guessed | karun.me, 2026-11-07 | D |
| Don't load generated maps into every session; write down only what the agent can't find | Playbook §8; Claude Code best practices | R, P |
| Skill frontmatter limited to the Agent Skills spec fields, so it runs outside Claude Code | agentskills.io specification | P |

## Design

> **Superseded.** The design, check script, tests and files below describe the first version: three files, `MAP.md`, `GLOSSARY.md` and `QUESTIONS.md`. Revision 2 replaced them with linked notes and templates in `assets/`, revision 3 added the HTML page, and revision 4 the adaptive graph. The current state is in the skill's README.

Three modes, from the argument: `map` (default: build or refresh), `check` (report drift, write nothing), `quiz` (teach from the map one level at a time and quiz the user).

At most three output files, in a folder the user picks (default `docs/repo-map/` in the target repository, asked once before writing):

1. `MAP.md`, at most 200 lines: a stamp line `Built from <short sha> on <YYYY-MM-DD>`; a bird's-eye view; a services table (name, kind, provides, depends on, owner, entry point); a codemap with one `### \`path/\`` heading per coarse module, 1 to 3 sentences, `Key names:` in backticks, and optional `Boundary:` and `Invariant:` lines; one Mermaid diagram of at most 15 nodes; build and test commands as found; and "What this map can't see".
2. `GLOSSARY.md`: `**Term**: definition.` lines, with optional `_Avoid_:` aliases and `_Seen as_:` symbol names. No implementation detail.
3. `QUESTIONS.md`: open questions, each with `ask: code` or `ask: <role>`, and the UNKNOWN facts.

Claims name paths and symbols, never line numbers: line numbers go stale (matklad), while a name can be checked by a script. Line-level proof goes in chat when the user asks.

The skill never edits `CLAUDE.md` or `AGENTS.md`. It may offer one pointer line, written only on a yes.

## The check script

`skills/repo-map/check_map.py <map-dir> [--repo <root>]`, standard library only, prints one PASS or FAIL line per check and exits 1 on any FAIL:

1. Required files and sections exist.
2. The stamp line parses, and in a git repository the commit exists; it reports (as a warning, not a FAIL) how many commits since then touched mapped paths.
3. Every backticked path in `MAP.md` exists in the repository.
4. Every name in a `Key names:` line or a glossary `_Seen as_:` field occurs in a source file.
5. `MAP.md` is at most 200 lines, and the Mermaid block has at most 15 nodes.
6. `MAP.md` has no `path:line` references.

## Tests

`tests/test_repo_map_skill.py`, run by `tests/run.sh`: a small fixture repository under `tests/fixtures/repo-map/`, one good map that passes, and broken maps that each fail exactly one check. Text tests that SKILL.md keeps its frontmatter within the spec's six fields, says it writes nothing before the user picks a folder, and states the same caps as the script.

## Files

- `skills/repo-map/SKILL.md`, `README.md`, `check_map.py`, `TEMPLATES.md`
- `tests/test_repo_map_skill.py`, `tests/fixtures/repo-map/**`
- `skills/README.md`, `llms.txt`: one row each

## Plan check (adversarial-reviewer, Opus, 2026-11-23): 3 objections, 4 minor

| Finding | Ruling |
|---|---|
| 1. The name check passes invented names when the map sits inside the repository (it finds them in MAP.md); substring matches and dependency folders also pass | Fixed. The search skips the map folder, uses `git ls-files` when there is a work tree (falling back to a walk), skips dependency and build folders, and matches whole words. Tests: map inside the repo, partial name, name only in `node_modules` |
| 2. The stamp check fails the good fixture (it sits inside this repository's git tree), skips monorepo sub-folders if "git root" is required, and false-fails on shallow clones and ambiguous short shas | Fixed. Any folder inside a work tree is checked; a shallow clone gives NOT RUN; the stamp uses a 12-character sha; `rev-parse --verify` rejects ambiguous ones. The fixture is stamped `no git` (WARN inside a work tree). Throwaway git repos test PASS, drift WARN and unknown-commit FAIL |
| 3. Text checks false-fail on what the template asks for: names and commands as paths, `postgres:16` as a line reference, diagram edge syntax | Fixed. A path needs a `/` or a known file extension; a line reference needs a known extension before `:<digits>`; the node count strips labels, shapes and `&`. Tests for each |
| Monorepo sub-maps break the three-file cap and go unchecked | Accepted: one folder per system, each checked on its own; README says so |
| The write guard is only a text test | Accepted and stated as a limit in the README: it is an instruction, not code |
| Fixture `.md` files publish to GitHub Pages | Accepted: only the good fixture is tracked, and it is a harmless sample; broken maps are built in temp folders |
| Non-UTF-8 sources | Already handled: files are decoded with `errors="replace"`, binaries skipped |

## Revision 2 (2026-11-23): linked notes for Obsidian and agents

The owner asked that the map be easy for Obsidian and an agent to parse and retrieve from, so they can ask questions while learning the what, the why and the architecture. Three files became a folder of small notes:

- `index.md`, holding the stamp
- `architecture.md`
- one note per component, term, decision, flow and question

Each note has flat YAML properties and `[[wikilinks]]`. Two modes changed:

- a new `ask` mode answers from the notes, confirms in the code, and files new answers back (Karpathy's "query" step);
- `quiz` now covers what, how and why.

The checker gained checks for:

- note types and their properties
- unique note names
- the index listing every note
- links resolving, through aliases too
- every diagram node being a component note

A real run on this repository caught a duplicate name (a `Playbook` term next to a `playbook` component), which led to the unique-name check.

## Revision 3 (2026-11-23): the HTML study page

The owner asked for HTML output they can open, read and follow visually and interactively.

**What changed:**

- A new `page` mode and `render_map.py` turn the notes into one self-contained `map.html`. It has a guided path, a clickable component graph, collapsible What / Why / How sections, flow walkthroughs (the graph lights each step's components), glossary flashcards, a notes-read meter and four themes.
- The design is a calm study-page system: low-contrast tokens, four themes, three text sizes, and collapsible What / Why / How sections.

**Bugs a browser check found and fixed:**

- links not navigating when the page is served as a `data:` URL;
- every nav item highlighted;
- a property-list parser bug that skipped the second link in `["[[a]]", "[[b]]"]`. That was a false PASS in the checker, and a test now covers it.

## Revision 4 plan (2026-11-23): a page that adapts to repo size

Asked for by the owner. The goal: `map.html` adapts to the repository's size and content, while the design system stays fixed and the model never writes raw HTML.

**1. Graph tiers, chosen from the component count.** The ranges, and what each draws:

| Components | Graph |
|---|---|
| 8 or fewer | One graph, as now |
| 9 to 40 | Clustered by a component's `system` property, falling back to the top folder of its `path`. Each cluster is a labelled, collapsible box |
| Over 40, or more than one `system` with over 8 components | The overview shows systems only; clicking a system drills into its graph |

In every tier:

- **Focus mode** shows one component and its direct neighbours, which also caps the nodes in view.
- **Zoom and pan**, with buttons and wheel or drag.
- **Search highlights** matching nodes.
- **The graph draws at its natural size** and scrolls inside its frame; it never shrinks to fit.
- **The layout is computed in Python:** clusters get columns by dependency depth inside the cluster, and the clusters are packed into rows. The JS only draws.

**2. Generic rendering:**

- Every `## heading` in a note body renders as a section, so notes are not limited to the template's headings.
- A note of an unknown type gets its own group instead of being dropped. The checker accepts an extra type only when a page plan declares it in `extra_types`.
- Empty sections and guided-path steps with no notes are hidden.

**3. An optional page plan, `page.md`** (`type: page`, at the map root), with flat properties:

| Property | What it sets |
|---|---|
| `order` | The order of the sections |
| `path` | Wikilinks that replace the guided path |
| `panels` | Panels picked from a fixed library: graph, flows, cards, table, timeline (from decision `date` properties), endpoints (from a component's `endpoints` property), flashcards, questions |
| `group_by` | A property that groups the component cards |
| `extra_types` | Note types beyond the seven |

`check_map.py` validates the panel names, the link targets and that `group_by` is a known property.

**4. Tests:**

- Generated fixtures with 3, 15 and 150 components. For each, assert:
  - the tier chosen;
  - at most 15 nodes in any view, except a cluster view, which has its own cap of 40;
  - every SVG text at 12px or more.
- The escaping and outside-host tests run on every panel.
- The browser check at 375px and 1280px for each fixture uses the built-in pane by hand, and the receipt says so. It is not in `tests/run.sh`, which has no browser.

**Size:** about 300 lines in `render_map.py`, 40 in `check_map.py` and 120 in tests. The fixtures are generated in the tests, not committed.

**Risks:**

- **Layout quality at 150 nodes.** Mitigation: never show more than one cluster's graph at a time.
- **Feature creep in panels.** Mitigation: a fixed library, each panel tested.

## Revision 4 as built (2026-11-23): the lean version

The plan check objected that the skill already caps a map at 15 components and splits monorepos, so the 9 to 40 and over-40 tiers and `page.md` would serve maps the skill forbids. The owner chose the lean version:

- **One layout for every view.** A JS `layout()` places components in reading order (dependants first), wrapped to the column width: one box per row on a phone, three on a desktop. Boxes and their 14px and 12px labels are never shrunk, and the page redraws when the width changes.
- **Focus view.** Each component's section has a focus graph of the component and its direct neighbours.
- **Flow graphs** draw only the flow's components.
- **The filter** lights matching components in the overview graph.
- **An optional `system` property** shows under each box's kind and orders boxes within a level.
- **Empty `##` sections are hidden.**
- **The checker now enforces at most 15 component notes per map**, the premise the layout relies on.

**Tests:**

- a generated 15-component chain must pass the checker;
- the page's own `layout()` is run in node at 343px and 848px: 1 and 3 boxes per row, reading order, no overlaps;
- the label sizes are checked;
- a 16-component map fails.

The browser check at 375px and 1280px was done by hand in the built-in pane. No `page.md`, drill-down or extra note types were built.

## Risks

- The name check can pass on a name that appears only in a comment. Accepted: it catches invented names, which is the main failure.
- A monorepo can exceed 15 nodes. The skill splits into one map per system, with an index line in the top `MAP.md`.
- Model-invocable, and it writes files. Mitigation: it asks for the folder before any write, and `check` writes nothing.
