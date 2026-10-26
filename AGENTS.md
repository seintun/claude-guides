# AGENTS.md

Instructions for any agent working in this repository: Claude Code, Codex, or another tool.

## What this repository is

A guide for building, orchestrating and guiding AI coding agents. It has four layers, and each has one source of truth:

1. `playbook/agent-harness-playbook.md` is the canonical reference. Facts, laws, patterns and Templates A to M live here, each graded P (primary), S (second-hand), R (research) or D (design advice).
2. `wiki/` holds short runbooks distilled from the playbook. A wiki page links to the playbook section it summarises and adds no facts of its own.
3. `site/orchestrating-claude.html` is the teaching page, published as a claude.ai artifact. It teaches the same material in 17 lessons.
4. `site/index.html`, `docs/orchestrating-claude-compendium.html`, `guide-index.json`, `routes/` and `sections/` are generated. Never edit them by hand; rebuild them.

When the playbook and another layer disagree, the playbook wins. Fix the other layer and say so in the commit.

## Finding your way

- **A session in another project starts at [`ENTRY.md`](ENTRY.md).** Read playbook sections with `python3 -I tools/section.py <id>` (for example `9.5`, `F` or `law-7`; `--list` shows every id), never the whole playbook. Read cannot follow `#anchors`, and the playbook is about 1,500 lines.
- **[`orchestration-index.md`](orchestration-index.md) is the phase index.** Find the phase you are in, then read only the playbook sections it lists. Do not load the whole playbook when one phase's sections will do.
- **[`llms.txt`](llms.txt)** maps every important file with a one-line description.
- **Every folder has a `README.md`** that lists its files.
- **To answer a question from the playbook,** go through its Contents or Find-it-fast table, then read that section.

## Using this repository as guidance

When someone asks you to plan, run or review agent work, use this repository's own method:

- **Before a task:** follow `wiki/start-a-task.md`. Grill first for anything above trivial (`wiki/grill.md`), then write a goal with Template B and an issue with Template L.
- **Splitting work:** follow `wiki/orchestrate.md`. One writer by default; helpers read, search or review; brief them with Template C.
- **Proving work:** follow `wiki/verify.md`. Every claim of done carries a receipt: each check marked PASS, FAIL or NOT RUN, with its command. NOT RUN is not PASS.
- **Unattended runs:** follow `wiki/run-unattended.md` and `wiki/guardrails.md`. Every loop has a stop condition, a retry cap and a cost ceiling.
- **A stuck agent:** follow `wiki/unstick.md`. It covers looping, a false "done", the same mistake twice, lost context and overbuilding.

## Editing rules

**Privacy (hard rule)**
- This repository is public. Never commit client or employer names, personal paths, email addresses, session ids or personal harness details.
- Use repo-relative paths or a placeholder such as `/path/to/claude-guides`. Describe a private setup in general terms.
- To add terms of your own to the check, list them one per line in `.privacy-terms`. That file is git-ignored and stays on your machine.
- The repository's own public addresses (owner/repo, the Pages host) are listed in the committed `.privacy-public`. A private term inside one of them passes; anywhere else it still fails. Add only full addresses there, never a bare name.
- Run `python3 -I tools/check_privacy.py` before every commit. It must PASS.

**Facts**
- Add no new factual claim without a primary source. Run a fact check, such as the `doc-checker` agent, before a claim lands.
- Keep the evidence grade on every claim.
- Keep the source list in sync: on the page, every evidence-tag URL must stay (`checks/urls-v11.txt` is the floor); new URLs are allowed.

**The page (`site/orchestrating-claude.html`)**
- One writer at a time. Parallel agents write drafts to `issues/drafts/` and the lead splices them in. `tools/splice_figs.py` handles figures.
- Follow the artifact contract:
  - no doctype, html or body tags
  - colours only as tokens on `:root`, with dark values under `prefers-color-scheme` and `[data-theme]`
  - external links open in a new tab
  - scripts only from the CDN allowlist
- Keep the section ids (`#loop` … `#sources`) and the lesson numbers. The playbook map and old links depend on them.
- Follow the visual language in the page's CSS comment above the diagram classes:
  - you: an accent pill
  - Claude: a neutral box
  - automatic, or the next run: dashed
  - pass: green
  - sent back: orange, and nothing else
  - harm, or a worse result: red
- Draw figures at most 880 units wide, never scaled below 1:1, with text of 12px or more.
- Glossary terms (`a.term`, `#glossary [data-term]`) must be defined in the block where they first appear. Check dom-9 enforces this.
- After editing text, run `python3 -I tools/lesson_meta.py site/orchestrating-claude.html` to refresh reading times.
- After any edit, run `python3 -I tools/build_standalone.py` to refresh `site/index.html`, the copy people open locally. `checks/static.sh` fails while it is stale. Never edit `site/index.html` by hand.

**Wiki, playbook and index**
- Link playbook sections by their GitHub anchor. After editing any heading or link, run `python3 -I tools/check_links.py`; every line should read PASS.
- After editing the playbook, the cheat sheet, `ENTRY.md`, a runbook title or a skill's frontmatter, run `python3 -I tools/build_index.py`. It regenerates `guide-index.json`, `routes/` and `sections/`, which agents without a clone fetch. Never edit them by hand.
- When you add or rename a playbook section, run `python3 -I tools/check_entry.py`. `ENTRY.md` routes by section id, so a renamed or removed section breaks its router.
- When you add a file, add it to its folder's README and, if it matters to agents, to `llms.txt`.
- Write short, active, plain sentences: no marketing tone, no em-dash asides.

## Checks: what "done" means here

The whole offline suite is one command. Run it before every commit; it must end with SUMMARY all PASS:

```bash
tests/run.sh
```

It runs every check below and every test in `tests/`, in under 10 seconds. [tests/README.md](tests/README.md) explains what each test guards and how to run the mutation, live and browser layers. When you change a test, a check or a guarded file, also run `python3 -I tests/mutation/mutate.py`; every mutation must be CAUGHT. A guard that fails on purpose (a section renamed by design, say) is updated in the same commit, as tests/README.md describes. Never weaken or delete a test to make it pass.

The individual checks, for when one fails. Run the privacy check before every commit:

```bash
python3 -I tools/check_privacy.py
```

Every line should read PASS. It fails on personal paths, email addresses, session ids and any term in `.privacy-terms`.

```bash
checks/static.sh
```

Every line should read PASS. The script also writes `build/preview.html`.

Then run `checks/run-dom.js` with Playwright (`browser_run_code_unsafe`, `filename` set to that file; set `ROOT` in it to your clone). All checks should read PASS in all 8 views: 320, 375, 414, 768, 1024 and 1280px, in light and dark.

Then check the links and the entry point, and rebuild the compendium:

```bash
python3 -I tools/check_links.py
```

```bash
python3 -I tools/check_entry.py
```

`check_entry.py` confirms `ENTRY.md` is under 150 lines, has at least 15 router rows, and names only section ids that `tools/section.py` resolves.

```bash
python3 -I tools/build_compendium.py
```

The compendium check (`checks/compendium-check.js`) confirms the result has no network requests, no dangling links and no sideways scroll.

Report results as receipts: `<path:line-range> — <change> | verified: PASS <command>`, or FAIL, or NOT RUN with the reason.

Get an independent review for any change to facts, figures or interaction. Give the reviewer the files and the brief, never your conclusions.

## Publishing the page

The live page is https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq. Publish updates to that same URL with the Artifact tool, passing `url`. Publishing is outward-facing, so do it only when the owner asks.

Every push to `main` also publishes `site/index.html` (as the site's home page), the compendium (as `compendium.html`), and `llms.txt`, `guide-index.json` and every tracked Markdown file outside `tests/live/` at its repository path, to GitHub Pages, through `.github/workflows/pages.yml`. Merging to `main` therefore publishes; rebuild both files before you merge.

## Git

- Work on a branch, not on `main`.
- Each clone runs `git config merge.ours.driver true` once: `.gitattributes` marks the generated compendium `merge=ours`, so a merge or revert keeps it, and you rebuild it after. How `main` was formed: [docs/main-branch.md](docs/main-branch.md).
- Make small, logical commits with plain messages.
- Add no AI attribution: no Co-Authored-By trailer and no "Generated with" line.
- Never commit secrets, `.env` files or `build/`.
