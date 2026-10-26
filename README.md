# Claude Guides

A working guide for building, orchestrating and guiding AI coding agents with Claude. It covers what to do before a task starts, while helpers run, when nobody is watching, and after the work ships, so each run teaches the next.

> You own the goal and the bar for done. Claude runs the loop until it clears the bar, or stops and asks you.

## For AI agents given this repository's link

You don't need a clone. Every file below is plain text at `https://raw.githubusercontent.com/seintun/claude-guides/main/<path>`. For a fork, use `https://raw.githubusercontent.com/<owner>/<repo>/main/<path>`, with `<owner>/<repo>` taken from the link you were given. If the link names a branch or tag (`/tree/<branch>`), use it in place of `main`. Fetch raw text with `curl` or similar: a fetch tool that summarises pages can shorten a file. <!-- privacy: allow -->

1. Fetch [`ENTRY.md`](ENTRY.md) (72 lines). It routes a request to a few section ids, at most one runbook and one template. For the same routing as JSON, fetch [`guide-index.json`](guide-index.json).
2. Fetch that row's bundle, `routes/row-<n>.md` (or `routes/phase-<n>.md`): its sections and templates in one file, for example [`routes/row-7.md`](routes/row-7.md). For a single section, fetch `sections/<id>.md`, such as [`sections/9.5.md`](sections/9.5.md); `cs:3` is `sections/cs-3.md`. Never fetch the whole playbook (about 1,500 lines).
3. Fetch a runbook from `wiki/<name>.md` only if you need its steps and checklist.
4. To use a skill without installing it, fetch its `SKILL.md` and follow it: [`grill`](skills/grill/SKILL.md), [`prompt`](skills/prompt/SKILL.md), [`guide`](skills/guide/SKILL.md).

[`llms.txt`](llms.txt) maps every important file. An agent editing this repository starts at [`AGENTS.md`](AGENTS.md) instead.

## Install the skills

The skills follow the open `SKILL.md` format, so the [skills CLI](https://github.com/vercel-labs/skills) installs them into Claude Code, Codex, Cursor and other agents. No clone needed. From your project, run `npx skills add seintun/claude-guides`. <!-- privacy: allow -->

Add `--skill grill` (or `prompt`, `guide`) for one skill, and `-g` to install for every project. To try one without installing it, run `npx skills use seintun/claude-guides@grill`. For a fork, use its `<owner>/<repo>` instead. <!-- privacy: allow --> `/guide` reads this repository over the network when it has no clone, and uses your clone when you link it with [`skills/guide/install.sh`](skills/guide/README.md).

## Start here

| I want to… | Go to |
|---|---|
| Call this guide from another project | [`ENTRY.md`](ENTRY.md), then [`skills/guide/README.md`](skills/guide/README.md): the `/guide` skill, a one-line snippet for the project's `CLAUDE.md`, and a paste-in prompt for one-off sessions |
| Understand the ideas, with pictures | The teaching page: [Orchestrating Claude](https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq), or open [`site/index.html`](site/index.html) locally. It is also embedded in the [compendium](docs/orchestrating-claude-compendium.html), which reads offline |
| Turn an idea or pain point into work Claude can finish | [Start a task](wiki/start-a-task.md) |
| Settle a design before planning, one question at a time | [Grill](wiki/grill.md) and the [`/grill` skill](skills/grill/README.md) |
| Split work between a lead and helper agents | [Orchestrate](wiki/orchestrate.md) |
| Make Claude prove its work | [Verify](wiki/verify.md) |
| Keep Claude working when I step away | [Run unattended](wiki/run-unattended.md) and [Guardrails](wiki/guardrails.md) |
| Set up my own harness | [Build a harness](wiki/build-a-harness.md) |
| Unstick an agent that loops, claims done too early, repeats a mistake, loses context or overbuilds | [Unstick](wiki/unstick.md) |
| Get better with every run | [Improve](wiki/improve.md) |
| See all of it applied to a real project | [Case study: this repository](wiki/case-study.md) |
| Review work phase by phase, or point an agent at the right sections | The [orchestration index](orchestration-index.md): 8 phases, each with the sections to read and a review checklist |
| Turn a brain-dump into a shared design, then a ready-to-run prompt | [`/grill`, then `/prompt`](skills/README.md) |
| Look up the detail behind any of the above | The [Agent Harness Playbook](playbook/agent-harness-playbook.md) (see its Contents and Find-it-fast table), and the one-page [cheat sheet](playbook/claude-cheat-sheet.md) |
| Search everything at once, offline | [`docs/orchestrating-claude-compendium.html`](docs/orchestrating-claude-compendium.html). Open it in a browser and press `/` |

An agent in another project starts at [`ENTRY.md`](ENTRY.md). An agent editing this repository starts at [`AGENTS.md`](AGENTS.md), then the [orchestration index](orchestration-index.md). [`llms.txt`](llms.txt) is a machine-readable map of the whole repository.

## Templates to copy

Every template lives in [playbook §16](playbook/agent-harness-playbook.md#16-templates).

| Template | Use it when |
|---|---|
| [A. CLAUDE.md skeleton](playbook/agent-harness-playbook.md#a-claudemd-skeleton) | Starting a repository's standing rules |
| [B. Task contract (goal prompt)](playbook/agent-harness-playbook.md#b-task-contract-goal-prompt) | Handing Claude a task with a checkable goal |
| [C. Subagent brief](playbook/agent-harness-playbook.md#c-subagent-brief) | Sending a helper agent off to work |
| [D. Plan file](playbook/agent-harness-playbook.md#d-plan-file) | Writing slices, each with the test that proves it |
| [E. Long-running state files](playbook/agent-harness-playbook.md#e-long-running-state-files) | Work that spans many sessions |
| [F. Stop hook](playbook/agent-harness-playbook.md#f-stop-hook-that-blocks-done-while-tests-fail) | Blocking "done" while tests fail |
| [G. PostToolUse formatter](playbook/agent-harness-playbook.md#g-posttooluse-formatter) | Formatting every file Claude edits |
| [H. Loop and schedule prompts](playbook/agent-harness-playbook.md#h-loop-and-schedule-prompts) | Running `/loop` or `/schedule` |
| [I. Retro prompt](playbook/agent-harness-playbook.md#i-retro-prompt) | Learning from a finished task |
| [J. Eval task record](playbook/agent-harness-playbook.md#j-eval-task-record-jsonl-one-line-per-task) | Tracking runs over time |
| [K. Grill prompt](playbook/agent-harness-playbook.md#k-grill-prompt) | Settling a design before any plan |
| [L. Agent-ready issue](playbook/agent-harness-playbook.md#l-agent-ready-issue) | Writing a ticket an agent can finish alone |
| [M. PR review workflow](playbook/agent-harness-playbook.md#m-pr-review-workflow-with-the-claude-code-github-action) | Reviewing pull requests with the Claude Code GitHub Action |

## What is in this repository

Every folder has a README that lists its files.

| Path | What it is |
|---|---|
| [`ENTRY.md`](ENTRY.md) | The entry point for a session in another project: a router from 19 scenarios to sections, runbook, template and output, plus the rules that apply everywhere |
| [`orchestration-index.md`](orchestration-index.md) | The phase index: eight phases, the sections to read for each, review checklists, and a one-night walkthrough |
| [`guide-index.json`](guide-index.json), [`routes/`](routes/README.md), [`sections/`](sections/README.md) | Generated by `tools/build_index.py`: the router, phases, runbooks and skills as JSON, one bundle per route, and one file per playbook section, so an agent without a clone fetches only what a route names |
| [`wiki/`](wiki/README.md) | Short runbooks distilled from the playbook. People start here |
| [`playbook/`](playbook/README.md) | The full reference (version 0.5) and the cheat sheet. The wiki and the index point into it |
| [`skills/`](skills/README.md) | Claude Code skills: `/guide` (`skills/guide/`), which lets any project call this guide, `/grill`, which reaches a shared design one question at a time, and `/prompt`, which turns it into a ready-to-run agent prompt |
| [`site/`](site/README.md) | The teaching page. Open `index.html` locally; `orchestrating-claude.html` is the artifact source, with no doctype because the claude.ai viewer wraps it. `site/history/` holds the v11 baseline |
| [`research/`](research/README.md) | Primary-source fact-checks |
| [`issues/`](issues/README.md) | The UX issue (13 children), every review report, and the drafts subagents wrote |
| [`docs/`](docs/README.md) | The decision log, session log, version history, a proposal, and the generated compendium |
| [`checks/`](checks/README.md) | Static and browser checks that gate every change to the page and the compendium |
| [`tools/`](tools/README.md) | Build, link-check and maintenance scripts. `tools/provenance/` keeps the one-off edit scripts for the record |
| [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), [`llms.txt`](llms.txt) | Instructions and a machine-readable map for agents |

## Keep it current

```bash
tests/run.sh
```

Runs every offline check and test in under 10 seconds. [tests/README.md](tests/README.md) says what each test guards, and [docs/metrics.md](docs/metrics.md) has the latest success, speed, token and growth numbers (`python3 -I tools/metrics.py --write`).

```bash
python3 -I tools/check_links.py
```

Checks that every relative link and `#anchor` in the Markdown resolves. Run it after editing headings.

```bash
python3 -I tools/check_entry.py
```

Checks that `ENTRY.md` stays under 150 lines, keeps at least 15 router rows, and names only section ids that resolve. Run it after adding or renaming a playbook section.

```bash
python3 -I tools/section.py --list
```

Lists every id that `tools/section.py` can print: sections, templates, laws and cheat-sheet sections. For example, `python3 -I tools/section.py 9.5` prints one playbook section.

```bash
python3 -I tools/build_compendium.py
```

Rebuild the compendium after changing any Markdown or the page.

```bash
checks/static.sh
```

Static checks on the page. This also writes `build/preview.html` for the browser checks (`checks/run-dom.js`; see `checks/README.md`).

```bash
python3 -I tools/lesson_meta.py site/orchestrating-claude.html
```

Refresh the page's reading times after editing its text.

```bash
python3 -I tools/build_standalone.py
```

Refresh `site/index.html`, the standalone copy of the page, after editing the page.

```bash
python3 -I tools/check_privacy.py
```

Checks that no file holds private data: personal paths, email addresses, session ids or terms listed in the git-ignored `.privacy-terms`. Run it before every commit.

## Status

- **Page:** version 16. All 21 browser checks pass in 8 views.
- **Playbook:** version 0.5. Every open item from the [v0.3 fact-check review](issues/reviews/playbook-factcheck-v0.3.md) is fixed or rejected with a reason.
- **Not yet done:** a blind three-reader test of the page's quiz, vertical phone layouts for the figures, and the remaining PARTLY items in [`issues/reviews/final-review-v15.md`](issues/reviews/final-review-v15.md).
