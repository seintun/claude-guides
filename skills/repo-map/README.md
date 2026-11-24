# /repo-map

Turns an unfamiliar repository into a small linked knowledge base you can learn from and ask questions of. Each component, term, decision and flow gets its own note, with flat YAML properties and `[[wikilinks]]`. An `index.md` lists every note.

- In Obsidian, the folder opens as a vault: browse it with links, backlinks, Graph view and search, and click the diagram's nodes to open their notes.
- An agent reads `index.md`, then only the notes a question needs, and greps the properties (`type: component`, `kind: service`).

The notes cover:

- **What:** components, services and the glossary.
- **Why:** decisions, each with its source.
- **How:** the architecture and request flows.

A check script proves that every path and name in the notes exists in the code, that every link resolves, and that nothing has drifted since the stamped commit.

A render script turns the notes into `map.html`, one interactive study page you open in any browser. It has:

- a guided reading path and a clickable component graph that wraps to the screen, from one box per row on a phone to three or four on a desktop, with labels never shrunk;
- a focus graph per component: the component and its direct neighbours;
- a filter that lights the matching components in the graph;
- collapsible What / Why / How sections;
- flow walkthroughs: step through a flow, and its graph, holding only the flow's components, outlines the ones each step names;
- glossary flashcards;
- a "notes read" meter;
- Light, Paper and Dark themes, and three text sizes.

It has five modes:

| Mode | What it does |
|---|---|
| `map` | Builds or refreshes the notes, checks them, and renders the page |
| `page` | Renders `map.html` from the notes |
| `ask <question>` | Answers from the notes, confirms the answer in the code, and offers to file a new answer as a note |
| `quiz` | Teaches one level at a time, sends you to read files yourself, and quizzes you on what, how and why |
| `check` | Reports drift and broken notes, and writes nothing |

It is model-invocable. Before it writes anything, it asks which folder to use: the default is `docs/repo-map/`, or a folder in your notes vault. It never edits your code, `CLAUDE.md` or `AGENTS.md`.

## The notes

```text
<map folder>/
├── index.md            # start here: one line per note, grouped by type; commit and date stamp
├── architecture.md     # bird's-eye view, diagram (nodes link to notes), boundaries, build and test
├── components/<name>.md   type, kind, path, owner, depends_on, provides, key_names
├── terms/<Term>.md        type, aliases, seen_as
├── decisions/<slug>.md    type, status (accepted, superseded or inferred), source
├── flows/<slug>.md        type, entry, components
└── questions/<slug>.md    type, status (open or answered), ask (code or a role)
```

Why this shape:

- **Small notes** let an agent load only the notes a question needs.
- **An index** gives both people and agents one place to start.
- **The same properties in every note of a type** keep searches simple. Obsidian's [Bases](https://help.obsidian.md/bases) can also show them as tables, such as open questions or components by owner.
- **`aliases`** let a link or a search find a term by another name. Obsidian treats this as a [default property](https://help.obsidian.md/aliases).
- **Unique note names** stop a link like `[[api]]` from pointing at two notes.

## Install

Without a clone, for Claude Code, Codex and other agents that read `SKILL.md`:

```bash
npx skills add seintun/claude-guides --skill repo-map
```

Then, in the repository you want to learn:

```text
/repo-map map
/repo-map ask why does the worker not import from the api?
/repo-map quiz
/repo-map check
/repo-map page
```

Render or re-render the page on its own:

```bash
python3 ~/.claude/skills/repo-map/render_map.py docs/repo-map
```

## On a company or private repository

The map holds company information: component names, paths, architecture and who owns what. So:

- **Keep the map where the employer allows.** That means inside the repository (`docs/repo-map/`, committed only if the team agrees) or another approved place. Never use a personal cloud-synced vault.
- **Leave fonts off.** By default the page makes no network request at all and uses system fonts. `--fonts` adds three fonts from Google Fonts on every open: no map content and no referrer are sent, but Google sees the viewer's IP address. Use it only for public repositories.
- **Don't publish the page** anywhere the repository itself isn't visible.
- **What the skill guards against:**
  - it never copies secrets into notes;
  - it treats READMEs, comments and commit messages as data, never as instructions.

  These are rules in `SKILL.md`. Like "ask before writing", they bind the model, not code.

From a clone, link the folder so updates arrive with `git pull`:

```bash
ln -s /path/to/claude-guides/skills/repo-map ~/.claude/skills/repo-map
```

Run the check on its own at any time:

```bash
python3 ~/.claude/skills/repo-map/check_map.py docs/repo-map --repo .
```

## Where the conventions come from

| Rule in the skill | Source | Grade |
|---|---|---|
| A short architecture note: coarse components, named rather than linked, with their invariants and boundaries | [matklad, "ARCHITECTURE.md"](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) | D |
| Glossary entries are terms only, with aliases to avoid | [mattpocock domain-modeling skill, `GLOSSARY-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/GLOSSARY-FORMAT.md) | D |
| Components (service, website, library), APIs and resources, each with an owner | [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/) | P |
| Small linked notes, an index read first, and good answers filed back as notes | [Karpathy, "LLM Wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | S |
| Flat properties (no nesting), `aliases` as a list, and Mermaid nodes linked with the `internal-link` class | [Obsidian Help: properties](https://help.obsidian.md/properties), [aliases](https://help.obsidian.md/aliases), [advanced syntax](https://help.obsidian.md/advanced-syntax) | P |
| A commit stamp, so drift shows | [rdilruba/codebase-map](https://github.com/rdilruba/codebase-map) | D |
| No proof, no claim (UNKNOWN instead of a guess), and teach then quiz | [karun.me, 2026-11-07](https://karun.me/blog/2026/11/07/use-the-agent-to-build-your-own-understanding/) | D |
| Don't load the map into every session; write down only what the agent can't find | [Gloaguen et al., arXiv 2602.11988](https://arxiv.org/abs/2602.11988); playbook §8; [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | R, P |
| Frontmatter limited to the spec's fields, so the skill runs outside Claude Code | [Agent Skills specification](https://agentskills.io/specification) | P |

The research behind these choices is in [docs/proposals/repo-ramp-up-workflow.md](../../docs/proposals/repo-ramp-up-workflow.md). The design and the review rulings are in [docs/plans/repo-map.md](../../docs/plans/repo-map.md).

## Other skills that map a repository

Read on 2026-11-23 from each project's own README or SKILL.md. Grade S: these are the authors' descriptions, and none of them was installed or run here.

| Skill | What it writes | How it differs from /repo-map |
|---|---|---|
| [rdilruba/codebase-map](https://github.com/rdilruba/codebase-map) | About 11 Markdown and Mermaid files in `docs/codebase-map/`, with init, update, explain, trace and check modes | The closest in spirit, with a commit stamp for drift. It has no notes per term or decision, and no script that checks the claims |
| [vivekmaru/repo-atlas](https://github.com/vivekmaru/repo-atlas) | A static HTML onboarding bundle in `docs/repo-atlas/` | A browsable site, not linked notes an agent can retrieve from |
| [cathrynlavery/repo-atlas](https://github.com/cathrynlavery/repo-atlas) | 10 docs in `docs/atlas/`, make targets, and an on-ramp added to `CLAUDE.md` | It edits `CLAUDE.md`, which /repo-map never does |
| [eigenwise map-codebase](https://github.com/eigenwise/eigenwise-toolshed/blob/main/plugins/codebase-mapper/skills/map-codebase/SKILL.md) | Up to 13 atomic docs in `.claude/.codebase-info/`, loaded by a session-start hook | It loads the map into every session, which playbook §8 advises against |
| [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer) | One `docs/CODEBASE_MAP.md` | A single file, so less to retrieve by part |
| [milad-ahmd codebase-explainer](https://milad-ahmd.github.io/agent-skills/skills/codebase-explainer/) | An `ARCHITECTURE.md` and an interactive HTML import graph built by a script | Its graph comes from real imports, which /repo-map does not parse; it has no glossary or decision notes |
| [brentzo/ren-atlas-skills](https://github.com/brentzo/ren-atlas-skills) | An Obsidian architecture atlas from eight chained skills, with Excalidraw and Canvas | Obsidian-native and large; /repo-map is one skill with two scripts |
| [caidanw architecture-md](https://github.com/caidanw/skills/blob/main/architecture-md/SKILL.md) | One `ARCHITECTURE.md` in matklad's style | The codemap only |

What /repo-map adds: one note per component, term, decision, flow and question, in a form Obsidian and agents both read, a checker that proves every path, name, link and source, and a study page drawn by code.

## What the check proves, and what it doesn't

| Check | Result |
|---|---|
| Every note matches its template. That means `index.md` and `architecture.md` exist, and each note has a known `type` in the right folder, its type's properties and `##` sections, and a `# Title`. Flows also need numbered steps, and note names and term aliases must be unique | FAIL on any gap |
| `index.md` lists every note, as `- [[name]]: summary`, under its type's section | FAIL on a missing note, a bad line or a wrong section |
| A decision's `source` that is a commit sha is a commit in this repository | FAIL if missing; NOT RUN outside git or in a shallow clone |
| Every `[[link]]` in a body or property names a note. An alias is shown with a pipe, `[[Order\|purchase]]`, because Obsidian's docs do not say a bare `[[alias]]` resolves | FAIL on a broken link, with the piped form to use for an alias |
| Every path in `path`, `entry`, `source` or backticks exists inside the repository's git work tree. A backticked token counts as a path when it ends in a file extension, or its first folder exists, so MIME types, `HTTP/1.1`, git refs and package names are not paths | FAIL on a missing path, an absolute path, or one that climbs out |
| The index `commit` is a commit in this repository | FAIL if it is missing or ambiguous; NOT RUN outside git or in a shallow clone |
| Commits since the stamp touched component paths | WARN, because the notes may still be right |
| Every `key_names` and `seen_as` name, and every backticked symbol in a flow step (each part of `Class.method`), occurs as a whole word in the code | FAIL on an invented name. The search uses git's file list and skips dependency folders and the map itself. In a repository too big to search, the verdict is `SUMMARY INCOMPLETE` with exit 2, never PASS |
| Notes are at most 60 lines (`index.md` and `architecture.md` at most 200); one diagram of at most 15 nodes, each a component note; at most 15 component notes per map (one map per system beyond that) | FAIL over a cap |
| No `file.ext:N` references, in backticks or prose | FAIL; ports and image tags such as `postgres:16` pass |

Limits:

- A name that occurs only in a comment still passes. The check catches invented names, not wrong descriptions.
- A "why" is only as good as its `source`. Decisions marked `status: inferred` are the agent's reading of the code.
- "Ask before writing" is an instruction to the model. No code enforces it.

## Files

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill the model reads, with every note format |
| [check_map.py](check_map.py) | The map checker. Standard library only; exits 1 on any FAIL |
| [render_map.py](render_map.py) | Renders the notes as `map.html`. Standard library only. The page is one file with inline CSS and JS, and no libraries. By default it makes no network request at all; `--fonts` adds Google Fonts, sent with no referrer |
| [assets/](assets/) | One template per note type: `index.md`, `architecture.md`, `component.md`, `term.md`, `decision.md`, `flow.md` and `question.md`. The agent copies them, and the checker enforces their properties and sections, so every run gives the same skeleton |

The page's design follows a calm study-page system:

- no pure white or black;
- low-saturation green, blue and violet accents, with amber for warnings;
- one reading column about 66 characters wide;
- Space Grotesk, Atkinson Hyperlegible and JetBrains Mono;
- four theme blocks wired through `prefers-color-scheme` and `data-theme`;
- graphs drawn as inline SVG by the page's own code, so they follow the theme and need no library (D).

## How it is tested

[tests/test_repo_map_skill.py](../../tests/test_repo_map_skill.py) runs with `tests/run.sh`. It covers:

- A good 12-note map of a fixture repository, which must pass.
- The rendered page:
  - every note and graph edge is in its data;
  - note text is escaped and can't end the script;
  - no outside host but Google Fonts;
  - the four themes, the sizes and the phone layout are present;
  - the walkthrough, path, read marks, flashcards, filter and two-step reset are present.

  The page was also tried by hand in a browser at desktop and phone widths, in Paper and Dark.
- 14 kinds of broken map, each of which must fail exactly its own check.
- Edge cases:
  - aliases resolving links
  - block-list properties
  - duplicate names
  - a map inside the repository
  - partial names
  - ports
  - diagram edge syntax
- Stamp and drift in throwaway git repositories.
- That `SKILL.md` keeps the spec's frontmatter and states the same caps, sections and note types as the script.

## Learn and teach skills

- **The format:** the [Agent Skills specification](https://agentskills.io/specification) and [Claude Code's skills docs](https://code.claude.com/docs/en/skills).
- **Examples:** [anthropics/skills](https://github.com/anthropics/skills), and the skills in this folder, each with a README, a check script and tests.
- **Sharing:** a public GitHub repository is the distribution. `npx skills add <owner>/<repo> --skill <name>` installs from it, and [skills.sh](https://skills.sh) lists public skills (P, [vercel-labs/skills](https://github.com/vercel-labs/skills)).
