# Call this guide from any project

Three ways to reach the guide from a Claude Code session in another project on this machine. All three send the session to [ENTRY.md](../../ENTRY.md). From there it loads only the sections its scenario needs, with `tools/section.py`.

| Way | When to use it | Source |
|---|---|---|
| `/guide <request>` | Any session, once the skill is installed | [SKILL.md](SKILL.md) |
| One-line CLAUDE.md pointer | A project whose sessions should know the guide exists | [snippet.md](snippet.md) |
| Paste-in prompt | A one-off session, or a machine without the skill | [prompt.md](prompt.md) |

## Where the guide lives (the one place this is documented)

The guide root is the top of your clone of this repository: whatever `git rev-parse --show-toplevel` prints inside it. Nothing stores the path.
- **The skill** finds the root itself on every run. It runs `git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel`, and git follows the symlink back into the clone.
- **The snippet and the prompt** are templates with `{{GUIDE}}` in place of the root. `install.sh` fills it in from the same `git rev-parse` and prints them.
- **If you move or re-clone the repository,** rerun `install.sh --apply` and paste the new snippet. Nothing else changes.

## Install without a clone

Run `npx skills add seintun/claude-guides --skill guide` from your project. <!-- privacy: allow -->

The [skills CLI](https://github.com/vercel-labs/skills) copies the skill folder, so `git rev-parse` finds no clone. The skill then runs in remote mode: it fetches `ENTRY.md` and one route bundle (`routes/row-<n>.md`) from `https://raw.githubusercontent.com/seintun/claude-guides/main`, and never the whole playbook. To read a fork instead, set `CLAUDE_GUIDES_REPO=<owner>/<repo>`. <!-- privacy: allow --> Install from your clone instead (below) to read local files and pick up your edits at once.

## Install from a clone

1. See the change first. This is a dry run, and it writes nothing:

   ```bash
   skills/guide/install.sh
   ```

   It prints the one change to `~/.claude` (a symlink, `~/.claude/skills/guide` pointing at `skills/guide` in your clone), then the snippet and the prompt with your root filled in.

2. Make the change:

   ```bash
   skills/guide/install.sh --apply
   ```

   Run this in your own terminal. Claude Code's sandbox blocks writes to `~/.claude/skills`, so a session can't do it for you.

3. Start a new Claude Code session in any project and type `/guide set up a Stop hook`. The skill lists itself in the `/` menu.

4. Optional: paste the printed one-line snippet into a project's `CLAUDE.md`. It is a plain pointer, not an `@` import. An import would load the whole file into every session ([memory docs](https://code.claude.com/docs/en/memory)).

To uninstall, run `rm ~/.claude/skills/guide`.

## What a route costs

An outside session reads the skill, ENTRY.md, the sections one router row names, and sometimes the row's runbook. It never reads the whole playbook. Measured with `python3 -I tools/route_cost.py`, which estimates tokens as characters divided by 4. The whole playbook is about 32,600 tokens.

| Scenario (router row) | Command | Tokens loaded | Share of the playbook |
|---|---|---|---|
| Add hooks (7), with its runbook | `route_cost.py 9.5 10.2 F G --runbook wiki/verify.md` | about 6,100 | 19% |
| Stuck agent (11) | `route_cost.py cs:3 14 4 8 11.3` | about 4,300 | 13% |
| Vague idea (1), with its runbook | `route_cost.py 5.1 5.2 K L --runbook wiki/start-a-task.md` | about 5,800 | 18% |

These are estimates. The exact count depends on the model's tokenizer, and the session's own conversation comes on top.

## Cold tests

Each way of calling the guide was tested from a fresh `claude -p` session (Sonnet) in an empty folder outside this repository, on 2026-10-24.

| Way | Request | Round 1 | Round 2, after fixes |
|---|---|---|---|
| `/guide` | "my agent keeps retrying the same failing test and never finishes" | FAIL: no answer. The skill computed its root in a shell line before it ran, and the session stalled at start-up | PASS: found the root with git, chose row 11, loaded `cs:3 14 4 8 11.3 B` and the unstick runbook |
| CLAUDE.md snippet | Three requests from a reviewer with only the snippet: Stop-hook gate, a 400-file Jest to Vitest migration, a tripled bill | PASS on routing (rows 7, 5 and 12). It reported three routing problems: row 5 loaded a research digest instead of the loop recipe, row 12 had no "find what spent it" step, and it was unclear that template letters load like sections | PASS: all three fixed in ENTRY.md, and the same rows answered with the right sections |
| Paste-in prompt | "make onboarding faster for new engineers" | PASS: row 1, loaded `5.1 5.2 K L` and the start-a-task runbook | PASS |

A second session ran its own independent cold test, read-only, on two more scenarios:

| Way | Request | Result |
|---|---|---|
| `/guide` | "onboard this new repo" | PASS: row 14, loaded `8 law-5 17 18 A` |
| Paste-in prompt | "agent-ready issue for a dark mode toggle" | PASS: row 15, loaded `5.1 law-3 L` |

No session read the whole playbook. Each loaded ENTRY.md, one `section.py` call per request, and at most one runbook. One caution came out of these runs. `--allowedTools` only pre-approves tools, so a session asked for an issue may write it into its own folder. Give the test sessions an empty scratch folder.
