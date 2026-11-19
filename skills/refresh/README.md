# /refresh

Keeps this repository current. It reads a fixed watchlist, writes a weekly digest of what is new, and once a month folds the verified items into a new version of the guide. It works only inside a clone of this repository, and it commits on a local branch and stops. You push, review and merge.

The routine, the digest format and the schedule are in [news/README.md](../../news/README.md). The skill's rules are in [SKILL.md](SKILL.md).

## Modes

| Command | When | What it does |
|---|---|---|
| `/refresh scan` | Weekly, Monday 09:00 | Reads sources newer than the cursor in `news/state.json`, writes `news/<YYYY>-W<ww>.md`, moves the cursor, runs the privacy check and the test suite, commits on `news/<YYYY>-W<ww>` |
| `/refresh deep` | First Monday of the month, 10:00 | Rolls the month up into `news/<YYYY>-<MM>.md`, folds the month's open and checked adopt items into the playbook and the layers below it, bumps the version, archives the old one when the minor version changes, rebuilds the generated files, runs every check and an independent review, commits on `refresh/<version>` |

## Design choices

- **Model-invocable, with no `allowed-tools` and no hooks.** A scheduled task runs only skills Claude may invoke on its own. A skill that sets `disable-model-invocation` reaches a scheduled run as plain text. Since Claude Code 2.1.325 a scheduled task also asks before it runs a skill that declares `allowed-tools` or hooks. So `/refresh` sets neither, and the task's permissions come from the task's own settings. [P: [changelog](https://code.claude.com/docs/en/changelog) and [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)]
- **The task prompt names the mode.** The scheduled task's prompt is `Run /refresh scan` or `Run /refresh deep`. [D]
- **The caps live in the skill.** The docs describe no budget control for a scheduled task, so the skill sets at most 40 sources, 8 subagents and a time box, and stops. [D]
- **Never push, merge, publish or schedule.** The routine proposes. A person decides. [D, from playbook §11.3 and §10]
- **Chrome is optional.** X and YouTube need a browser. Without one the run lists them as gaps. [D]

## Install

From a clone, link it so updates arrive with `git pull`:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/refresh" ~/.claude/skills/refresh
```

Without a clone: `npx skills add seintun/claude-guides --skill refresh`. The skill does nothing useful there, because it needs this repository's `news/` folder and `tools/`. Run it from a clone.

To run it by hand, open a session in the clone and type `/refresh scan`.

## The schedule

This repository does not create the scheduled tasks. Follow [news/README.md](../../news/README.md#the-schedule-to-be-created-by-you) to create two desktop scheduled tasks, with the folder set to your clone and the Worktree option on. Use "Run now" once on each before you rely on it.

## How it is tested

[tests/test_refresh_skill.py](../../tests/test_refresh_skill.py) runs on every commit. It checks that SKILL.md has no `disable-model-invocation`, no `allowed-tools` and no hooks; that it states the never-push and never-publish rules, the caps, the browser-only rule for X and LinkedIn, the privacy rule and the receipts rule; that `news/README.md` defines the digest fields `/guide` relies on; that `news/state.json` parses and holds the changelog cursor and only known source ids; and that every digest file name matches its pattern. Mutation cases in [tests/mutation/mutate.py](../../tests/mutation/mutate.py) check that each of these guards fails when its rule is removed.

The skill has not yet been run end to end by a scheduled task. Do that with "Run now" before trusting a schedule.
