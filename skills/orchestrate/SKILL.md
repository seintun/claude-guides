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
| 6. Workflow script | A read-only fan-out over dozens of items (20 or more), with no human gate mid-run. Paid plans; up to 16 agents at once and 1,000 per run; no mid-run user input [P] | Many agents | Fast, but no way to steer mid-run |

Rules that hold on every route:

- One writer per set of files. Helpers read, search and review [D].
- Do not nest coordinators. Independent agents amplified errors 17.2x, and a central orchestrator 4.4x, both against one agent [R]. Keep one coordinator; extra layers are our advice to avoid [D].
- Agent teams are experimental, give teammates no worktree isolation, and use about 7x the tokens of a standard session when teammates run in plan mode [P]. Prefer routes 3 to 5 for writing code [D].
- The orchestrator-workers pattern costs about 15x the tokens of a chat [P]. Pay that only for parallel reading, an independent judgment, or context that would overflow.
- With F yes, add a fresh critic on the plan and an adversarial review of the diff, and keep a human sign-off [D].

## 4. Pick a model and effort for each part

What the docs say [P]: Sonnet handles most coding; Opus is for complex architecture or multi-step reasoning; Haiku suits simple subagent tasks. The 5.5 models default to `medium` effort. `high` is for work where verification matters or edge cases are likely; `max` is prone to overthinking, so test it before adopting it broadly.

The ladder built on that [D]. Climb one rung at a time, and after a failure move up a rung rather than retrying on the same one.

| Rung | Model and effort | Use for |
|---|---|---|
| 1 | Haiku, low | Search, read, summarise |
| 2 | Sonnet, medium | Most coding, routing, routine review |
| 3 | Opus, medium | Work across several files, an unfamiliar area, unclear requirements, tricky logic, or a Sonnet attempt that failed |
| 4 | Opus, high | High-risk work, adversarial review, or an Opus-medium attempt that failed |
| 5 | A human | The same failure twice on rung 4 |

Set a subagent's effort with `effort` in its frontmatter, and a session's with `--effort` or `/effort` [P].

## 5. Write the routing card and stop

```text
Route: <number>. <name>. Why: <one line from the questions>
Runner-up: <number>. <name>. It would win if: <condition>
Parts:
- <part> | <model>, <effort> | reads or writes | <files or scope>
Order: <what runs in sequence, what runs in parallel, the cap>
Checks: <check 1>; <check 2>; <2 to 5 commands or observations, separated by semicolons>
Budget: <a figure: turns, minutes or dollars>. Stop when: <condition>, or after 2 failures with the same cause
Not used: <features you passed over, and why>
```

On route 3, say in Order how many `/batch` runs (or plain worktree subagents) it takes. With F yes, list the critic and the adversarial reviewer as Parts on Opus at high effort, and put the human sign-off in Order. Give a named agent its model and effort too (`doc-checker | sonnet, medium | reads | ...`), and write a step a script runs with no model as `no model`. Write one Parts line per agent or session, not per step: a single agent doing several steps is one line, so route 1 has exactly one. Put any other notes after `Not used`.

List 2 to 5 checks, never more. Give the budget as a number with a unit (turns, minutes, hours, dollars or agents).

End your reply with this exact line, and start nothing before a yes:

```text
Go, or change the route?
```

## 6. After a yes

- Brief every helper with: the objective and the decision it feeds; what is already ruled out; where to look and what not to touch; which tools to use; the output format, a length cap and a file path for long output; a budget; and when to stop and report partial results. Ask for findings with file:line or URL and a confidence (high, medium, low), under 400 words [D].
- A helper's report is a claim. Re-check any claim that drives a decision before you act on it [D].
- A reviewer gets the work and the criteria, never your conclusion [D].
- Mark every check PASS, FAIL or NOT RUN, with its command. NOT RUN is not PASS [D].
- On route 5, run the hub as a session with a bounded goal and give each builder its own session and worktree. Builders report to the hub with cross-session messages; a message never counts as consent, so it cannot answer a permission prompt [P]. Start 3 builders at most, because a person reviews every PR [D]. Use these prompts:

```text
Hub: /goal Every item in <backlog> has a PR with a PASS receipt or is marked Blocked, and your last
message prints the ledger (id, state, session, branch, PR, attempts, last receipt); or stop after
<N> turns. Start at most 3 builders at once, only for items whose blockers are done and whose
files do not overlap a running builder's.

Builder: Item <id>: <outcome>. Check that must pass: <command>. Only touch <files or area>; message
the hub if you need more. Make the check pass test-first, commit, and open a PR whose body lists each
check as PASS or FAIL with its command. Then message the hub "<id> PR <url> receipt: <PASS|FAIL>
<command>". After 2 failures with the same cause, stop and message "<id> BLOCKED: <why>". Never merge.
```
