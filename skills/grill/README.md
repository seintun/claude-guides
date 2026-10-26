# /grill

A skill that grills you about an idea or plan before any plan or spec exists. It asks one question per message, recommendation first, until you and the agent share the design. It packages playbook §5.2 and Template K. The method, the validation checklist and a worked example are in the runbook, [wiki/grill.md](../../wiki/grill.md).

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill: look before asking, one question per message, a fixed question shape, a decision log, a stop rule |
| [test.sh](test.sh) | Cold test: a fresh `claude -p` session grills a fixture project, then the transcript is checked |
| [check_transcript.py](check_transcript.py) | The 8 checks the test runs on the transcript (grill-1 to grill-8) |

## Install

Without a clone, with the [skills CLI](https://github.com/vercel-labs/skills) (Claude Code, Codex, Cursor and other agents):

Run `npx skills add seintun/claude-guides --skill grill` from your project. <!-- privacy: allow -->

The skill is self-contained: it needs no other file from this repository. Or link it from your clone, the same way as `/guide`:

```bash
ln -s "$(git rev-parse --show-toplevel)/skills/grill" ~/.claude/skills/grill
```

Run this from your clone, in your own terminal; Claude Code's sandbox blocks writes to `~/.claude/skills`. To undo, run `rm ~/.claude/skills/grill`. Then type `/grill <idea>` in any project.

The skill sets `disable-model-invocation: true`, so it runs only when you type `/grill`. Claude never picks it on its own, and its description stays out of every session's context. A plain "grill me" goes to whatever grill skill does trigger automatically, such as Matt Pocock's `grilling`, so the two never compete.

## Test

```bash
skills/grill/test.sh
```

It needs the `claude` CLI, signed in, and costs one short session. It sends the skill's text as the prompt, so it works before you install anything. Add `--installed` to call `/grill` instead. In a sandbox where the default temp folder is not writable, set `GRILL_TEST_DIR` to a writable folder. The test works in a new subfolder there and deletes only that subfolder.
