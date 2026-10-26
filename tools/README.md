# tools

Run every command from the repository root. None needs a third-party package.

| Script | What it does |
|---|---|
| `build_compendium.py` | Builds `docs/orchestrating-claude-compendium.html` from the Markdown and the page. Run: `python3 -I tools/build_compendium.py` |
| `check_links.py` | Checks that every relative link in the Markdown files points to a file that exists, and that every `#anchor` matches a heading. Run: `python3 -I tools/check_links.py` |
| `route_cost.py` | Estimates the tokens one route loads: the skill, ENTRY.md, a row's sections and optionally its runbook. Run: `python3 -I tools/route_cost.py 9.5 F --runbook wiki/verify.md` |
| `metrics.py` | Success and performance metrics: suite results and timing, mutation catch rate, live routing results, tokens per route, reading time, and growth across git history. Run: `python3 -I tools/metrics.py --write --record`, which writes docs/metrics.md |
| `section.py` | Prints one playbook section (`9.5`, `17A`), template (`F`), law (`law-7`) or cheat-sheet section (`cs:3`) by id, so a session never loads the whole playbook. `--list` shows every id. Exits 1 on an unknown id. Run: `python3 -I tools/section.py 9.5` |
| `build_index.py` | Writes `guide-index.json` (router, phases, sections, runbooks and skills as JSON) and `sections/<id>.md` (one file per id `section.py` serves), so an agent without a clone fetches only what a route names. Run it after editing the playbook, the cheat sheet, ENTRY.md, a runbook title or a skill's frontmatter; `tests/test_generated.py` fails while they are stale. Run: `python3 -I tools/build_index.py` |
| `check_entry.py` | Checks that `ENTRY.md` is under 150 lines, has at least 15 router rows, and that every section id it names resolves through `section.py`. Run it after adding or renaming a playbook section. Run: `python3 -I tools/check_entry.py` |
| `check_privacy.py` | Fails on private data in any tracked or untracked file: home paths, scratch paths, email addresses, session ids, and any term listed in the git-ignored `.privacy-terms`. Run: `python3 -I tools/check_privacy.py` |
| `build_standalone.py` | Wraps the artifact page in a full HTML document and writes `site/index.html`, so the page works when opened locally or through a dev server. `checks/static.sh` uses it for `build/preview.html`. Run: `python3 -I tools/build_standalone.py` |
| `lesson_meta.py` | Writes each lesson's level and reading time into the page, and the totals into the reading paths. Run: `python3 -I tools/lesson_meta.py site/orchestrating-claude.html` |
| `splice_figs.py` | Splices redrawn figures (SVG, caption, key, panel edits) from a draft in `issues/drafts/` into the page. Run: `python3 -I tools/splice_figs.py site/orchestrating-claude.html <draft.html>` |
| `provenance/` | The one-off scripts that applied each child issue's edits to the page, kept for the record. They ran against the page as it was at the time, so they are not a rebuild path |
