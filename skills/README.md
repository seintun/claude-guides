# skills

Claude Code skills built while working on this repository, with the brief, plan and tests that shaped them.

| Skill | What it does | Files |
|---|---|---|
| `/guide` | Lets a session in any project call this guide. It resolves this repository's root, reads [ENTRY.md](../ENTRY.md), finds the scenario, and reads only the sections that scenario names. `install.sh` links it into `~/.claude/skills/` and prints a one-line `CLAUDE.md` snippet and a paste-in prompt | [README.md](guide/README.md) (install steps and how the root is resolved), [SKILL.md](guide/SKILL.md), [snippet.md](guide/snippet.md), [prompt.md](guide/prompt.md), [install.sh](guide/install.sh) |
| `/grill` | Grills an idea or plan one question at a time, recommendation first, until the design is shared, before any plan or spec (playbook §5.2, Template K). The method and its validation checklist are in [wiki/grill.md](../wiki/grill.md) | [README.md](grill/README.md) (install and test), [SKILL.md](grill/SKILL.md), [test.sh](grill/test.sh), [check_transcript.py](grill/check_transcript.py) |
| `/prompt` | Turns a description into a ready-to-run agent prompt from Templates B, C and H. It interviews only for gaps, sizes the prompt by risk, and saves it in the guide's git-ignored `prompts/<project>/`, never in your project. Slash-only | [README.md](prompt/README.md) (install, tests, results), [SKILL.md](prompt/SKILL.md), [check_prompt.py](prompt/check_prompt.py) (the check it runs on each draft), battle tests in [tests/live/prompt/](../tests/live/prompt/) |
A `/brief` skill was built here and retired on 2026-10-24. It duplicated `/grill` and `/prompt`. A dry run of those two on three requests showed they lacked 7 of its rules, so the rules moved into them. The dry run and its results are in [tests/live/grill-prompt/](../tests/live/grill-prompt/).

Install any of them without a clone: `npx skills add seintun/claude-guides` (add `--skill <name>` for one). `/grill` needs nothing else; `/prompt` brings its check script; `/guide` reads this repository over the network. From a clone, install `/guide` with `guide/install.sh`, which links the folder rather than copying it; see [guide/README.md](guide/README.md). Each other skill's README gives its one-line install.
