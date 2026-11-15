# /orchestrate live eval: results

Run: `python3 -I tests/live/orchestrate/run.py --k 2 --record`. Each run is a fresh `claude -p` session in a throwaway project. It gets the skill's text, with one of the 12 cases in [scenarios.json](scenarios.json) as its request. Code scores every answer (see the docstring of [run.py](run.py)); no model grades another. The final round's lines are in [../../results/orchestrate-live.jsonl](../../results/orchestrate-live.jsonl). The raw lines of every round, as printed at the time, are in [rounds.txt](rounds.txt).

## Final round, 2026-11-14 (Sonnet, k = 2)

| Measure | As first scored | After the checker fixes below |
|---|---|---|
| Runs passing every check | 18 of 24 | 24 of 24 |
| Cases passing both runs (pass^2) | 7 of 12 | 12 of 12 |
| Expected route chosen (or an accepted one) | 24 of 24 | 24 of 24 |
| Started any work (Agent, Write, Edit, or a writing Bash command) | 0 of 24 | 0 of 24 |
| Routed in 5 tool calls or fewer | 24 of 24 | 24 of 24 |
| Cost | $3.08 in all, about $0.13 a run | same transcripts |

All 6 first-scored failures were the checker misreading a valid card:
- 2 checks named only a command (`pytest`).
- 2 budgets put words between the figure and the unit ("12 builder sessions", "15 main-thread turns").
- 1 card used a per-item scope (`handlerN.js`) and wrote "2 runs" instead of "2 /batch runs".
- 1 comparison card counted its own main thread as a fifth helper.

Each fix has a regression test, and the last two use the live cards themselves as fixtures (`tests/fixtures/orchestrate/live-*.txt`). The rescore ran the fixed checker on the same transcripts. No session was rerun and no card was edited.

`async-refactor` chose route 1 in both runs, which the case accepts. Its 15 coupled files are one writer's job either way, and the card named route 2 as its runner-up.

## Every round

| Round | Result | What the failures were | What changed |
|---|---|---|---|
| 1, Sonnet k = 2 | 20 of 24 | Checker: a read-only comparison (no writer) counted as broken, and nested bullets read as part lines. Label: auditing 60 READMEs for a link is one grep, so the model's route 1 beat our label of route 6 | Routes 1 and 2 allow at most one writer, and sub-bullets join their part. The audit case now needs a judgment per README, and route 6 needs C (bulky reading), in both SKILL.md and `route.py` |
| 2, Sonnet k = 2 | 18 of 24; routes 24 of 24 | Checker: a shell loop's semicolons split into several checks, budgets in "hrs" or "contexts" were missed, and script steps with no model were rejected | The check splitter skips `code spans`, more budget units are accepted, and `no model` is a valid part |
| 2, Haiku k = 1 | 1 of 12 | No closing question, loose formats, and 2 wrong routes | The skill gives the exact closing line |
| 3, Sonnet k = 2 | 20 of 24; routes 24 of 24 | Checker: semicolons in parentheses or in a bulleted check counted as extra checks. Skill: named agents were written with no effort | Bullets are counted, and parentheses are skipped. The skill shows how to write a named agent and a script step |
| 3, Haiku k = 1 | 7 of 12 | 3 wrong routes, all too low: 40 handlers, 60 audits and 2 GB of logs were all routed inline | The frontmatter pins the skill to `model: sonnet` and `effort: medium` |
| 4, Sonnet k = 2 | 23 of 24 | One real miss: 6 checks on `add-mfa` | None at first. Then an independent review found false passes in the checker (below) |
| 5, Sonnet k = 2 | 18 of 24, then 24 of 24 | See the final round above | Five checker fixes |

Between rounds 4 and 5, an independent reviewer built cards by hand that a wrong card could use to pass:
- a route 1 card naming route 2's longer name;
- "critic" written only under Not used;
- nested writer scopes;
- checks that say only "yes";
- a zero budget;
- a card that skips the `/batch` run count `route.py` requires;
- closing chatter that starts with "Route:".

Each now fails, and each has a test. The checker also gained k-11, which checks that the card carries what `route.py` says its route requires.

The round 4 transcripts, rescored with that stricter checker, gave 21 of 24. Two cards had skipped the `/batch` count or the human sign-off, and SKILL.md now asks for both by name.

Across all rounds, no Sonnet failure was a wrong route. The failures were checker misreads, format gaps the skill had not explained, one label we got wrong, and real format misses (6 checks, a missing `/batch` count, a missing sign-off).

## Limits

- The labels and the facts behind them were written by the same author as `route.py`. So the unit tests prove the code and the labels agree, not that the labels are right. Two labels changed after a live run showed them wrong or arguable: `readme-audit` (round 1) and `async-refactor`, which accepts route 1. Treat new disagreements the same way: read the card first, then decide whether the skill, the checker or the label is wrong.
- The live run sends the skill's text as the prompt. It tests neither automatic invocation nor the `model` and `effort` frontmatter. The Haiku rounds ran the skill's text on Haiku, which is the situation that frontmatter is meant to prevent.
- Sessions load the runner's own user settings and hooks. `--strict-mcp-config` and `--disable-slash-commands` remove MCP servers and other skills, but not hooks. Wording may differ on another machine; what the checker requires does not.
- The card is read from the session's final message only.
- Twelve cases cover each route at least once. They are not a sample of real requests; add a case whenever a real request routes badly. The thresholds (19 against 20 items, 4 against 5 parts) are tested offline in `tests/test_orchestrate_skill.py`, not live.
