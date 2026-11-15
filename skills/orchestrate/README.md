# /orchestrate

Decides how to run a task before any work starts: inline in one agent, with helper subagents, as parallel builders in worktrees, as one session per task, as a hub over a backlog, or as a workflow script. It also picks a model and effort for each part. It writes a routing card and starts nothing until you say yes.

It runs on Sonnet at medium effort whatever the session's model (frontmatter `model: sonnet` and `effort: medium`; the override lasts for the rest of the turn, and an organization's model allowlist or auto mode can keep the session's model instead [P]). The live eval is why: given the skill's text, Sonnet's route matched the expected one in 119 of 120 runs across five rounds (the one miss was a wrong label, since fixed), while Haiku misrouted 3 of 12 cases. The live eval does not exercise the frontmatter itself.

It is model-invocable: Claude can load it on its own when a task looks multi-step, parallel or backlog-sized, as well as when you type `/orchestrate <task>`. That is safe because the skill only recommends.

## Where the rules come from

| Rule in the skill | Playbook source |
|---|---|
| Six questions and six routes | §6 orchestration patterns and decision tree; §7 delegation protocol and effort scaling |
| `/batch` and workflow limits | §3A feature map |
| One writer; one coordinator | §7 house rules [D]; §19.1 item 1 [R] |
| Agent-team and orchestrator-workers token costs | §3A [P]; §6 [P] |
| What the docs say about models and effort | §3A, "Model and effort" row [P] |
| The rung-by-rung ladder | Design advice built on §3A [D] |
| Helper brief, re-check, fresh reviewer, receipts | Template C; §7; Law 7; §9.4 |
| Hub goal and builder brief | §3A (`/goal`, cross-session messaging); §11.3 loop guardrails |

SKILL.md is self-contained, so an installed copy works without this repository. The section numbers live here only.

## Files

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill the model reads |
| [route.py](route.py) | The routing rules as code. `python3 -I route.py --explain '<facts>'` prints the route, runner-up and requirements |
| [check_card.py](check_card.py) | Checks a routing card with code: fields, route name, part lines, one writer, scopes, check count, budget, high-risk review, expected route |
| [EXAMPLE.md](EXAMPLE.md) | A worked example: four requests on one codebase and the route each gets |

## How it is tested

- Offline, every commit: [tests/test_orchestrate_skill.py](../../tests/test_orchestrate_skill.py) runs `route.py` on 12 labelled cases, checks that SKILL.md states the same rule order, thresholds and route names as the code, and runs `check_card.py` on fixtures where each broken card must fail exactly one check.
- Live, opt-in: [tests/live/orchestrate/run.py](../../tests/live/orchestrate/run.py) gives the skill to fresh `claude -p` sessions on the same 12 cases and scores each answer with code: it started nothing, routed in 5 tool calls or fewer, asked to go, and wrote a card that passes `check_card.py` with the expected route. Results: [tests/live/orchestrate/results.md](../../tests/live/orchestrate/results.md).

## Install

Without a clone:

```bash
npx skills add seintun/claude-guides --skill orchestrate
```

From a clone, link it so updates arrive with `git pull`:

```bash
ln -s "$(pwd)/skills/orchestrate" ~/.claude/skills/orchestrate
```

## Try it

```text
/orchestrate Fix the flaky date test in utils/
/orchestrate Migrate all 40 API handlers to the new error type
/orchestrate Work the 12 open tickets in this cycle to PRs; several are blocked by others
/orchestrate Compare three charting libraries for the dashboard and recommend one
```

Expected routes: 1 (inline); 3 (parallel builders in worktrees, as two `/batch` runs because `/batch` takes 5 to 30 parts); 5 (hub plus builder sessions, because the tickets have an order); 2 (inline plus 2 to 4 read-only helpers).
