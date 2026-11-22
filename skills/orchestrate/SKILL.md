---
name: orchestrate
description: Decide how to run a task before starting it, inline in one agent, with read-only helper subagents, as parallel builders in worktrees, as one session per task, as a hub over a backlog, or as a workflow script, and which model and effort each part gets. Use when work spans many files, tickets or independent parts, or the user asks how to split, delegate, parallelise, coordinate or orchestrate work. Skip single-file or one-step tasks. It recommends a route and starts nothing until the user says yes.
argument-hint: <task, ticket list or backlog>
model: sonnet
effort: medium
---

Route this work: $ARGUMENTS (if empty, the current request).

You recommend a route; you do not start agents, sessions or workflows until the user says yes. The aim is a quality result for the fewest tokens, then speed. Grades: [P] primary source, [R] research, [D] design advice.

## 1. Look before you route

Decide inline, in five tool calls or fewer. Never spawn an agent to decide whether to spawn agents.

- Read the request, the project's CLAUDE.md or AGENTS.md, and its test command.
- Size the work: how many files, tickets or items; whether they depend on each other; whether the change is high risk (schema, auth, data deletion, infrastructure, a public API, permissions).

## 2. Answer six questions

| | Question |
|---|---|
| A | Does it fit in one context with one writer? |
| B | Do the parts touch different files, have no order between them, and each need enough work to be a task of its own? A mechanical edit across a few files is one task. |
| C | Is there bulky output you only need the conclusion of (logs, wide search, docs)? A test run you can sum up in one line does not count. |
| D | Does it need a judgment from someone who did not do the work (review, critique)? |
| E | Does it span many tickets or sessions, or must it outlive this conversation? |
| F | Is it high risk? If yes, D is yes too. |

## 3. Pick the route

Check these in order; the first that matches wins. The table below says what each route costs and gives.

1. E is yes and there is more than one item: route 5 if the items have an order (blocked-by links), otherwise route 4.
2. The job is read-only, covers dozens of items (20 or more) that each need reading or judgment (C is yes), and needs no human gate mid-run: route 6. If one search or one command answers it, C is no.
3. B is yes and the parts write: route 3, as one `/batch` run per 30 parts, or as plain worktree subagents when there are fewer than 5 parts.
4. C or D is yes, or A is no: route 2.
5. Otherwise: route 1.

Runner-ups, the nearest alternative to each route: 1 to 2, 2 to 1, 3 to 4 (to 2 below 5 parts), 4 to 3, 5 to 4, 6 to 2.

| Route | Pick it when | Token cost | Speed |
|---|---|---|---|
| 1. Inline | A is yes and C is no | Lowest | Fastest to start |
| 2. Inline plus helper subagents | C or D is yes. One writer stays in the main thread; helpers read, search or review and return summaries. A comparison of options takes 2 to 4 helpers [P] | One extra context per helper | Reads run in parallel |
| 3. Parallel builders in worktrees | B is yes and each part has its own check. `/batch` splits one change into 5 to 30 worktree subagents that each open a PR [P]; more parts than that means several runs | Grows with the number of parts | Wall-clock drops |
| 4. One session per task | E is yes, there is more than one item, the items have no order between them, and each ends in its own branch or PR you may want to open and steer | A full context each | Parallel, and survives this session |
| 5. Hub plus builder sessions | E is yes and the items have an order (blocked-by links). Route 5 beats route 4 whenever an order exists | A small hub plus one session per item | Long-running |
| 6. Workflow script | A read-only fan-out over dozens of items (20 or more), with no human gate mid-run. Paid plans; up to 16 agents at once and 1,000 per run, with a warning above 25 agents or 1.5M tokens; no mid-run user input. From `claude -p` a workflow needs an approval route: an allow rule, auto mode, a PreToolUse hook that returns allow, `--permission-prompt-tool`, or an SDK `canUseTool` callback [P] | Many agents | Fast, but no way to steer mid-run |

Rules that hold on every route:

- One writer per set of files. Helpers read, search and review [D]. Writers in parallel (routes 3 to 5) fit only when each has an isolated checkout, the work splits into independent failing checks, a strong verifier grades the result, and a claim mechanism stops two writers taking the same task [D, built on P and R sources: playbook §6].
- Do not nest coordinators. Independent agents amplified errors 17.2x, and a central orchestrator 4.4x, both against one agent [R]. Keep one coordinator; extra layers are our advice to avoid [D].
- Agent teams are experimental, give teammates no worktree isolation, and use about 7x the tokens of a standard session when teammates run in plan mode [P]. Prefer routes 3 to 5 for writing code [D].
- The orchestrator-workers pattern costs about 15x the tokens of a chat [P]. Pay that only for parallel reading, an independent judgment, or context that would overflow.
- With F yes, add a fresh critic on the plan and an adversarial review of the diff, and keep a human sign-off [D].
- A `/goal` condition cites output the session prints, because its evaluator runs no commands, and always carries a turn bound [P]. A headless run's cost ceiling is `--max-budget-usd` on an API key, a soft cap on estimated spend, or on a subscription the plan's usage limits and the usage-credits spend limit [P]; `--max-turns` bounds turns, not cost [D].

## 4. Pick a model and effort for each part

What the docs say [P]: Sonnet handles most coding; Opus is for complex architecture or multi-step reasoning; Haiku suits simple subagent tasks. The 5.5 models default to `medium` effort. `high` is for work where verification matters or edge cases are likely; `max` is prone to overthinking, so test it before adopting it broadly.

The ladder built on that [D]. Climb one rung at a time, and after a failure move up a rung rather than retrying on the same one. Count turns, not token price: the cheapest models often take 2 to 3 times the turns on multi-step work and end up costing more, so Haiku stays on reading and exact transcription, and Sonnet is the floor for every reviewer and every builder that writes code [D].

| Rung | Model and effort | Use for |
|---|---|---|
| 1 | Haiku, low | Search, read, summarise |
| 2 | Sonnet, medium | Most coding, routing, routine review |
| 3 | Opus, medium | Work across several files, an unfamiliar area, unclear requirements, tricky logic, or a Sonnet attempt that failed |
| 4 | Opus, high | High-risk work, adversarial review, or an Opus-medium attempt that failed |
| 5 | A human | The same failure twice on rung 4 |

Set a subagent's effort with `effort` in its frontmatter or per call with the Agent tool's `effort` parameter (v2.1.292), and a session's with `--effort` or `/effort` [P].

## 5. Write the routing card and stop

```text
Route: <number>. <name>. Why: <one line from the questions>
Answers: A <yes|no>; B <yes|no>; C <yes|no>; D <yes|no>; E <yes|no>; F <yes|no>; order <yes|no>; read-only <yes|no>; gate <yes|no>; comparison <yes|no>; items <number>
Reasoning: Rule 1: skipped, <why>. <one clause per rule, in order, until> Rule <n>: fired, <why>. Cheaper routes: <why each cheaper route does not fit, or "none">. Would change if: <condition>.
Runner-up: <number>. <name>. It would win if: <condition>
Parts:
- <part> | <model>, <effort> | reads or writes | <files or scope>
Order: <what runs in sequence, what runs in parallel, the cap; with F yes, end with "human sign-off">
Checks: <check 1>; <check 2>; <2 to 5 commands or observations, separated by semicolons>
Budget: <a figure: turns, minutes or dollars>. Stop when: <condition>, or after 2 failures with the same cause
Not used: <features you passed over, and why>
```

Answers holds your answer to each question in step 2, plus four facts: order (the items have blocked-by links), read-only (nothing is written), gate (a person must approve something mid-run), comparison (the job compares options), and the number of items. The route and runner-up must follow from those answers by the rules in step 3, so anyone can check the card line by line. Reasoning walks the same rules in plain words for the user, who decides from it: one short clause per rule up to the one that fired, then why the cheaper routes do not fit and what would change the route. Keep it under 150 words.

On route 3, say in Order how many `/batch` runs (or plain worktree subagents) it takes. With F yes, list the critic and the adversarial reviewer as Parts on Opus at high effort, and put the human sign-off in Order. Give a named agent its model and effort too (`doc-checker | sonnet, medium | reads | ...`), and write a step a script runs with no model as `no model`. Write one Parts line per agent or session, not per step: a single agent doing several steps is one line, so route 1 has exactly one. Put any other notes after `Not used`.

List 2 to 5 checks, never more. Give the budget as a number with a unit (turns, minutes, hours, dollars or agents).

End your reply with this exact line, and start nothing before a yes:

```text
Go, or change the route?
```

## 6. After a yes: you write every prompt

The user approves the card; you write every brief and prompt the route needs. Show the briefs in one block as you send them, so the user can stop you there.

Write each brief for a stranger: the agent sees nothing else. An Opus brief can stop at the goal, the constraints and what done looks like; a Sonnet or Haiku brief also names the exact files and the checks it can run, wherever you know them. Pass long inputs as a file and send the path, never pasted history [D].

| Route | How to start it |
|---|---|
| 1 | Do the work yourself in this session |
| 2 | Spawn each helper with the Agent tool, on the model and effort its Parts line names, with a helper brief |
| 3 | With 5 parts or more, run `/batch` with one instruction: the change, each part's check, the scope, "open draft PRs", and "do not edit the checks or their tests". With fewer, spawn one worktree subagent (`isolation: worktree`) per part, each with a builder brief |
| 4 | Start one session per task, each with a builder brief |
| 5 | Start the hub with the hub prompt, and paste the builder template into it; the hub starts builders with builder briefs |
| 6 | Write the workflow script. The user's yes to this card is the opt-in it needs |

```text
Helper: Objective: <what to return, and the decision it feeds>. Already ruled out: <...>. Look at:
<files, folders, URLs>; do not touch <...>. Tools: <which to use>. Return under 400 words: a summary,
findings with file:line or URL and a confidence (high, medium, low), and what you could not find.
Write long output to <path> and return the path. Budget: <N tool calls>. Stop and report partial
results when <condition>.

Builder: Item <id>: <outcome>. Check that must pass: <command>. Only touch <files or area>; message
the hub (or report back) if you need more. Do not edit the check or its tests unless this brief says
so. Make the check pass test-first, commit, and open a draft PR whose body lists each check as PASS or
FAIL with its command. Do not mark it ready. Then report "<id> PR <url> receipt: <PASS|FAIL> <command>".
After 2 failures with the same cause, stop and report "<id> BLOCKED: <why>" with the failing command
and the last lines of its output. Never merge.

Hub: /goal Every item in <backlog> has a PR with a PASS receipt and an end-panel receipt or is
marked Blocked, and your last message prints the ledger; or stop after <N> turns. Keep the ledger
in <ledger file>: one row per item (id, state, session, branch, PR, attempts, last receipt, panel),
written when a builder starts and updated on every report. After context compaction, read the ledger
first; an item marked running stays running until its session reports or is checked, never started
again. Start at most 3 builders at once, only for items whose blockers are done and whose files do
not overlap a running builder's.
```

While it runs:

- A helper's report is a claim. Re-check any claim that drives a decision before you act on it [D].
- A reviewer gets the work and the criteria, never your conclusion [D].
- Mark every check PASS, FAIL or NOT RUN, with its command. NOT RUN is not PASS [D].
- When a BLOCKED item moves up a rung, the new builder's brief carries the failing command and the output the old builder reported, as written, not your summary of it [D].
- On route 3 with plain worktree subagents and more than 3 parts, keep the same ledger as the hub prompt, in a file you name on the card's Order line, so a compacted context does not start finished or running parts again [D].
- Review twice per item, never per commit: a plan check by one fresh reviewer before builders start (medium and large items), and an end panel on each draft PR once its builder reports, before it is marked ready. The end panel is a spec reviewer (does the diff do what the item asks, and were tests weakened) plus, for high-risk or large items, an adversarial reviewer; each gets the diff file, the item and the checks, never your view. Use the project's own review rules where it has them. On routes 3 to 5 the driver or hub runs the panel, since builders cannot start subagents [D].
- On route 5, builders report to the hub with cross-session messages; a message never counts as consent, so it cannot answer a permission prompt [P]. Start 3 builders at most, because a person reviews every PR [D].

## 7. After the work: record the outcome

When the route finishes or stops, write one outcome line and show it to the user:

```text
- <YYYY-MM-DD> /orchestrate outcome: <task in a few words> | route <number> (<name>) | budget <figure> | spent <figure> | checks PASS <n>, FAIL <n>, NOT RUN <n> | route again: <yes|no>, because <reason>
```

Append it to the project's `docs/decisions.md` if the project keeps one; otherwise show it and ask where to save it. A "route again: no" is the most useful line there is: it names a task the rules routed badly, so suggest turning it into a new labelled case.
