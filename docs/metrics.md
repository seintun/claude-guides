# Guide metrics

Generated 2026-11-18 by `python3 -I tools/metrics.py`. Rerun it to refresh; the numbers below are measurements, not targets.

## Success

- **Offline suite (`tests/run.sh`):** FAIL. 325 test cases, 0 not run (a tool missing).
- **Mutation suite:** caught 71 of 71 catastrophic changes (100%), run 2026-11-18.
- **Adversarial review edits:** 75 of 75 caught firmly, still failing after the generated files are rebuilt and the baseline regenerated (100%), run 2026-10-25.
- **Live routing (`tests/live/route_scenarios.py`):** 3 of 3 runs picked the expected row (prompt 1/1, skill 1/1, snippet 1/1). Whole playbook read in 0 runs. 1 more run(s) voided by a test-harness flaw, explained in its note in tests/results/live.jsonl.

## Speed

| Step of `tests/run.sh` | Result | Seconds |
|---|---|---|
| page source: static checks, standalone copy current | PASS | 0.1 |
| links and anchors in every Markdown file | PASS | 0.1 |
| privacy: no personal paths, emails or private terms | PASS | 0.3 |
| ENTRY.md router: size, rows, section ids | PASS | 0.0 |
| runner integrity: run.sh and the commit hook still run every check | PASS | 0.1 |
| unit and guard tests | FAIL | 8.5 |
| **Total** | | **9.3** |

- **Section lookup:** 1.1 ms to load one playbook index and print 5 sections (`tools/section.py`).
- **Live session:** median 23.5 s and 5 turns from request to routed answer (3 runs).
- **Mutation suite:** 364.9 s for 71 mutations.

## Tokens and efficiency

- **Whole playbook:** 45,798 tokens. A session never loads it; it loads the skill, ENTRY.md and one row's sections.
- **Per route, all 22 router scenarios:** median 6,438 tokens (14% of the playbook), smallest 4,579, largest 11,439.
- **Savings:** a median route loads 7.1 times less than the whole playbook.
- **Live sessions, measured:** median 230,816 input and 1,707 output tokens, median $0.20 a run. Input includes the session's own system prompt and tools, not only the guide.

| Scenario | Row | Tokens loaded | Share of playbook |
|---|---|---|---|
| vague-idea | 1 | 5,642 | 12% |
| new-feature | 2 | 7,274 | 16% |
| bug-fix | 3 | 6,061 | 13% |
| refactor | 4 | 7,350 | 16% |
| migration | 5 | 4,944 | 11% |
| harness-setup | 6 | 9,419 | 21% |
| add-hooks | 7 | 6,197 | 14% |
| overnight | 8 | 6,774 | 15% |
| code-review | 9 | 6,068 | 13% |
| research-spike | 10 | 5,437 | 12% |
| stuck-agent | 11 | 6,998 | 15% |
| cost-blowup | 12 | 6,123 | 13% |
| multi-repo | 13 | 6,960 | 15% |
| onboard-repo | 14 | 7,481 | 16% |
| agent-ready-issue | 15 | 5,295 | 12% |
| retro | 16 | 6,631 | 14% |
| security-review | 17 | 6,245 | 14% |
| parallel-writers | 18 | 7,834 | 17% |
| write-a-prompt | 19 | 4,579 | 10% |
| choose-how-to-run | 20 | 11,439 | 25% |
| end-to-end-unattended | 21 | 9,566 | 21% |
| set-up-evals | 22 | 6,182 | 13% |

Tokens are characters divided by 4; the exact count depends on the tokenizer.

## Reading time

At 200 words a minute, the rate `tools/lesson_meta.py` uses for the page.

| Document | Minutes |
|---|---|
| Whole playbook | 149 |
| Teaching page (visible text) | 73 |
| ENTRY.md | 10 |
| wiki/build-a-harness.md | 5 |
| wiki/case-study.md | 10 |
| wiki/grill.md | 6 |
| wiki/guardrails.md | 5 |
| wiki/improve.md | 6 |
| wiki/orchestrate.md | 6 |
| wiki/records.md | 4 |
| wiki/run-unattended.md | 6 |
| wiki/start-a-task.md | 5 |
| wiki/unstick.md | 8 |
| wiki/verify.md | 7 |

## Growth

Each row is a commit where one of the counts changed.

| Date | Commit | Runbooks | Skills | Router rows | Scenarios | Test cases | Playbook lines |
|---|---|---|---|---|---|---|---|
| 2026-10-25 | `135f554` | 11 | 3 | 19 | 19 | 225 | 1,553 |
| 2026-10-26 | `59d376e` | 11 | 3 | 19 | 19 | 233 | 1,553 |
| 2026-10-26 | `38bedc3` | 11 | 3 | 19 | 19 | 236 | 1,553 |
| 2026-10-27 | `24a681c` | 11 | 3 | 19 | 19 | 238 | 1,582 |
| 2026-11-15 | `1b8dad2` | 11 | 4 | 20 | 20 | 287 | 1,583 |
| 2026-11-18 | `2b21a86` | 11 | 4 | 20 | 20 | 290 | 1,583 |
| 2026-11-18 | `1ce5333` | 11 | 4 | 20 | 20 | 290 | 1,729 |
| 2026-11-18 | `77882fa` | 11 | 4 | 22 | 22 | 296 | 1,729 |
| 2026-11-18 | `ee90b2e` | 11 | 4 | 22 | 22 | 298 | 1,729 |
| 2026-11-18 | `fb75c65` | 11 | 4 | 22 | 22 | 300 | 1,729 |
| 2026-11-18 | `5c91e48` | 11 | 5 | 22 | 22 | 323 | 1,729 |
| 2026-11-18 | `97a8434` | 11 | 5 | 22 | 22 | 324 | 1,729 |
| 2026-11-18 | `0915808` | 11 | 4 | 20 | 20 | 290 | 1,583 |
| 2026-11-18 | `244becc` | 11 | 4 | 20 | 20 | 290 | 1,729 |
| 2026-11-18 | `21b4a88` | 11 | 4 | 22 | 22 | 296 | 1,729 |
| 2026-11-18 | `6fe7d8e` | 11 | 4 | 22 | 22 | 300 | 1,729 |
| 2026-11-18 | `438841c` | 11 | 5 | 22 | 22 | 324 | 1,729 |
| 2026-11-18 | `dd4d55f` | 11 | 5 | 22 | 22 | 325 | 1,729 |
