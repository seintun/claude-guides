# /orchestrate live eval: results

Run: `python3 -I tests/live/orchestrate/run.py --k 2 --record`. Each run is a fresh `claude -p` session in a throwaway project. It gets the skill's text, with one of the 12 cases in [scenarios.json](scenarios.json) as its request. Code scores every answer (see the docstring of [run.py](run.py)); no model grades another. The final round's lines are in [../../results/orchestrate-live.jsonl](../../results/orchestrate-live.jsonl). The raw lines of every round, as printed at the time, are in [rounds.txt](rounds.txt).

## Final round, round 9, 2026-11-14 (Sonnet, k = 2)

The card now opens with its working. Answers lists every question's answer, and Reasoning walks the rules in plain words ("Rule 1: skipped, E no. Rule 3: fired, B yes. Cheaper routes: ... Would change if: ..."). The checker feeds the Answers line to `route.py` and fails the card unless that gives the card's own route and runner-up (k-12). It also fails a card whose Reasoning names the wrong rule as fired, leaves out a part, or runs past 150 words (k-13).

| Measure | As first scored | After the checker fix below |
|---|---|---|
| Runs passing every check | 22 of 24 | 23 of 24 |
| Cases passing both runs (pass^2) | 10 of 12 | 11 of 12 |
| Expected route chosen (or an accepted one) | 24 of 24 | 24 of 24 |
| Route follows from the card's own Answers (k-12, route only) | 24 of 24 | 24 of 24 |
| Reasoning names the rule that fired, in shape and under 150 words (k-13) | 24 of 24 | 24 of 24 |
| Started any work | 0 of 24 | 0 of 24 |
| Cost | $2.16 in all, about $0.09 a run | same transcripts |

The one remaining failure is real. In `migrate-handlers-1` the model named route 2 as runner-up, with a good reason (a shared `AppError` change must land first), but the skill's runner-up list says 4, so k-12 fails it. The other first-scored failure was the checker reading "writes nothing to the repo" as a writer; fixed, with a regression test.

`async-refactor` chose route 1 in both runs, which the case accepts. Its 15 coupled files are one writer's job either way.

The PR #8 review then tightened the checker:
- k-12 requires `gate` and `comparison`.
- k-5 allows read-only routes 4 and 5 with no writer.
- k-9 is switched on by `F yes` in the card itself, and needs both a plan critic and an adversarial reviewer, plus the human sign-off.
- k-13 requires Reasoning to walk rules 1 to N in order.

Rescored on the same round 9 transcripts, the result is unchanged: 23 of 24, with the same single miss.

A second review pass tightened it further:
- k-9 needs a part named as a critic and one named as an adversary (by name or by agent), so a generic "Plan" or "Review" part no longer counts.
- k-13 needs "Rule k: skipped, <reason>" for each rule before the one that fired.
- k-11 runs on the card's own Answers when no `--facts` are given.
- A rescore records the model each transcript was produced with.

One round 9 card named its adversary "Diff reviewer", running the `adversarial-reviewer` agent, and was briefly failed by the narrower name rule. The rule now reads the agent too. With that fix, round 9 still scores 23 of 24.

## Round 5, the last round before Answers and Reasoning

18 of 24 as first scored, and 24 of 24 after five checker fixes, rescored on the same transcripts. All 6 first-scored failures were the checker misreading a valid card:
- 2 checks named only a command.
- 2 budgets put words between the figure and the unit.
- 1 card used a per-item scope (`handlerN.js`) and wrote "2 runs".
- 1 comparison card counted its own main thread as a helper.

Each fix has a regression test. The last two use the live cards themselves as fixtures (`tests/fixtures/orchestrate/live-*.txt`). Those two fixtures predate Answers and Reasoning, so their tests check only the rules they exposed.

## Every round

| Round | Result | What the failures were | What changed |
|---|---|---|---|
| 1, Sonnet k = 2 | 20 of 24 | Checker: a read-only comparison (no writer) counted as broken, and nested bullets read as part lines. Label: auditing 60 READMEs for a link is one grep, so the model's route 1 beat our label of route 6 | Routes 1 and 2 allow at most one writer, and sub-bullets join their part. The audit case now needs a judgment per README, and route 6 needs C (bulky reading), in both SKILL.md and `route.py` |
| 2, Sonnet k = 2 | 18 of 24; routes 24 of 24 | Checker: a shell loop's semicolons split into several checks, budgets in "hrs" or "contexts" were missed, and script steps with no model were rejected | The check splitter skips `code spans`, more budget units are accepted, and `no model` is a valid part |
| 2, Haiku k = 1 | 1 of 12 | No closing question, loose formats, and 2 wrong routes | The skill gives the exact closing line |
| 3, Sonnet k = 2 | 20 of 24; routes 24 of 24 | Checker: semicolons in parentheses or in a bulleted check counted as extra checks. Skill: named agents were written with no effort | Bullets are counted, and parentheses are skipped. The skill shows how to write a named agent and a script step |
| 3, Haiku k = 1 | 7 of 12 | 3 wrong routes, all too low: 40 handlers, 60 audits and 2 GB of logs were all routed inline | The frontmatter pins the skill to `model: sonnet` and `effort: medium` |
| 4, Sonnet k = 2 | 23 of 24 | One real miss: 6 checks on `add-mfa` | None at first. Then an independent review found false passes in the checker (below) |
| 5, Sonnet k = 2 | 18 of 24, then 24 of 24 | See round 5 above | Five checker fixes |
| 6, Sonnet k = 2 | 13 of 24; k-12 24 of 24 | The first run with Answers and Reasoning. Every card's answers gave its route. But Reasoning ran past the 4-sentence cap in 8 runs, because the cards walked through every rule. 2 checks were a bare `pytest`. 1 high-risk card had no human sign-off | The cap rose to 8, and a bare command counts as a check |
| 7, Sonnet k = 2 | 16 of 24 | The cards grew to fill the new cap (9 to 10 sentences). 1 run used 7 tool calls. 1 high-risk card again had no human sign-off | A sentence cap measures length, not use. Reasoning got a fixed shape instead: one clause per rule up to the one that fired, "Cheaper routes:", "Would change if:", and at most 150 words. The card template gives the human sign-off its own slot |
| 8, Sonnet k = 2 | 23 of 24 | The audit case routed inline, correctly: its 60 placeholder files were 17 bytes each, so they fit in one context | The fixture bug was ours. Cases about bulky reading now pad their placeholder files (`stub_bytes`) |
| 9, Sonnet k = 2 | 22 of 24, then 23 of 24 | See the final round above | The checker reads "writes nothing" as reading |

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

Across all rounds, the only wrong routes were two the model got right and our test got wrong (round 1's label, round 8's fixture). The failures were checker misreads, format gaps the skill had not explained, one label we got wrong, and real format misses (6 checks, a missing `/batch` count, a missing sign-off).

## Limits

- The labels and the facts behind them were written by the same author as `route.py`. So the unit tests prove the code and the labels agree, not that the labels are right. Two labels changed after a live run showed them wrong or arguable: `readme-audit` (round 1) and `async-refactor`, which accepts route 1. Treat new disagreements the same way: read the card first, then decide whether the skill, the checker or the label is wrong.
- The live run sends the skill's text as the prompt. It tests neither automatic invocation nor the `model` and `effort` frontmatter. The Haiku rounds ran the skill's text on Haiku, which is the situation that frontmatter is meant to prevent.
- Sessions load the runner's own user settings and hooks. `--strict-mcp-config` and `--disable-slash-commands` remove MCP servers and other skills, but not hooks. Wording may differ on another machine; what the checker requires does not.
- The card is read from the session's final message only.
- The runner-up must match the skill's fixed list. A model may name a better runner-up for the task in front of it (round 9) and still fail k-12. That keeps the check deterministic, at the cost of judgment.
- The outcome line (step 7) is checked offline by `check_card.py --outcome` against sample lines. The live eval stops at the card, so no live run has written one yet.
- Twelve cases cover each route at least once. They are not a sample of real requests; add a case whenever a real request routes badly. The thresholds (19 against 20 items, 4 against 5 parts) are tested offline in `tests/test_orchestrate_skill.py`, not live.
