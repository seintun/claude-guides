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
| [check_card.py](check_card.py) | Checks a routing card with code: fields, route name, part lines, one writer, scopes, check count, budget, high-risk review, expected route, what the route requires, that the route follows from the card's own Answers line, and that Reasoning names the rule that fired. With `--outcome`, checks the outcome lines in a decisions file |
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
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/orchestrate" ~/.claude/skills/orchestrate
```

## How to use it

1. Ask: `/orchestrate <task>`, or just describe a big task and let Claude load the skill.
2. Read the card. `Answers` shows how it judged each question, and `Reasoning` says in plain words which rule fired, why the cheaper routes do not fit, and what would change the route.
3. Answer the closing question. Say go, or correct an answer ("C is yes") or the route. Nothing starts before a yes.
4. After a yes it writes every prompt itself (helper briefs, builder briefs, the hub prompt or the workflow script) and shows them as it sends them.
5. When the work ends it records one outcome line (budget against spent, checks, "route again: yes or no, because ...") in `docs/decisions.md`.

## With ultracode

Ultracode is a Claude Code setting that turns on automatic workflow orchestration [P]. A workflow is route 6 in this skill, but a session with ultracode on can reach the other routes too.

- **One prompt.** Putting `ultracode` in a typed prompt opts that prompt into a workflow, and so does asking for one in your own words [P]. The keyword does not trigger with `-p`, scheduled tasks or relayed comments [P]. Route 6 does not need it: the skill counts your yes to a route 6 card as the opt-in [D].
- **One session.** `/effort ultracode` (or `claude --effort ultracode`) turns it on for the session and also sets `xhigh` effort. `/effort ultracode off` turns it off. The `ultracode` setting turns it on for every session [P].
- **What changes.** With ultracode on, Claude decides when a task warrants a workflow. Each such request uses more tokens and takes longer, and on a subscription it reaches a usage limit sooner [P]. This skill aims for a quality result for the fewest tokens, so a session with ultracode on may run a workflow where the card picked route 1 to 5 [D]. Read the card and hold Claude to its route, or turn ultracode off.
- **Requirements.** Workflows are on all paid plans, and Pro turns them on in `/config` [P]. Turning workflows off also turns ultracode off [P].
- **Untested.** The live eval ran without ultracode, so how the two interact has not been measured.

Start with `/orchestrate <task>` in a session without ultracode. The skill runs on Sonnet at medium effort whatever the session's model, and the card sets a model and effort for each part [D]. Add ultracode only when the card picks route 6 and you want a larger run, and say yes to the card first.

Sources: [Workflows](https://code.claude.com/docs/en/workflows), [Model configuration](https://code.claude.com/docs/en/model-config).

## Try it

```text
/orchestrate Fix the flaky date test in utils/
/orchestrate Migrate all 40 API handlers to the new error type
/orchestrate Work the 12 open tickets in this cycle to PRs; several are blocked by others
/orchestrate Compare three charting libraries for the dashboard and recommend one
```

Expected routes: 1 (inline); 3 (parallel builders in worktrees, as two `/batch` runs because `/batch` takes 5 to 30 parts); 5 (hub plus builder sessions, because the tickets have an order); 2 (inline plus 2 to 4 read-only helpers).
