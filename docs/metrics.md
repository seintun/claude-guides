# Guide metrics

Generated 2026-10-24 by `python3 -I tools/metrics.py`. Rerun it to refresh; the numbers below are measurements, not targets.

## Success

- **Offline suite (`tests/run.sh`):** all PASS. 160 test cases, 0 not run (a tool missing).
- **Mutation suite:** caught 23 of 23 catastrophic changes (100%), run 2026-10-24.
- **Adversarial review edits:** 56 of 56 caught firmly, still failing after the generated files are rebuilt and the baseline regenerated (100%), run 2026-10-24.
- **Live routing (`tests/live/route_scenarios.py`):** 3 of 3 runs picked the expected row (prompt 1/1, skill 1/1, snippet 1/1). Whole playbook read in 0 runs. 1 more run(s) voided by a test-harness flaw, explained in its note in tests/results/live.jsonl.

## Speed

| Step of `tests/run.sh` | Result | Seconds |
|---|---|---|
| page source: static checks, standalone copy current | PASS | 0.1 |
| links and anchors in every Markdown file | PASS | 0.0 |
| privacy: no personal paths, emails or private terms | PASS | 0.2 |
| ENTRY.md router: size, rows, section ids | PASS | 0.0 |
| runner integrity: run.sh and the commit hook still run every check | PASS | 0.1 |
| unit and guard tests | PASS | 5.8 |
| **Total** | | **6.5** |

- **Section lookup:** 1.1 ms to load one playbook index and print 5 sections (`tools/section.py`).
- **Live session:** median 23.5 s and 5 turns from request to routed answer (3 runs).
- **Mutation suite:** 78.7 s for 23 mutations.

## Tokens and efficiency

- **Whole playbook:** 32,586 tokens. A session never loads it; it loads the skill, ENTRY.md and one row's sections.
- **Per route, all 18 router scenarios:** median 4,508 tokens (14% of the playbook), smallest 3,236, largest 6,153.
- **Savings:** a median route loads 7.2 times less than the whole playbook.
- **Live sessions, measured:** median 230,816 input and 1,707 output tokens, median $0.20 a run. Input includes the session's own system prompt and tools, not only the guide.

| Scenario | Row | Tokens loaded | Share of playbook |
|---|---|---|---|
| vague-idea | 1 | 4,133 | 13% |
| new-feature | 2 | 5,050 | 15% |
| bug-fix | 3 | 4,139 | 13% |
| refactor | 4 | 4,879 | 15% |
| migration | 5 | 3,419 | 10% |
| harness-setup | 6 | 6,153 | 19% |
| add-hooks | 7 | 4,688 | 14% |
| overnight | 8 | 4,688 | 14% |
| code-review | 9 | 3,236 | 10% |
| research-spike | 10 | 3,564 | 11% |
| stuck-agent | 11 | 4,410 | 14% |
| cost-blowup | 12 | 4,038 | 12% |
| multi-repo | 13 | 4,875 | 15% |
| onboard-repo | 14 | 4,870 | 15% |
| agent-ready-issue | 15 | 3,788 | 12% |
| retro | 16 | 3,707 | 11% |
| security-review | 17 | 4,607 | 14% |
| parallel-writers | 18 | 4,822 | 15% |

Tokens are characters divided by 4; the exact count depends on the tokenizer.

## Reading time

At 200 words a minute, the rate `tools/lesson_meta.py` uses for the page.

| Document | Minutes |
|---|---|
| Whole playbook | 103 |
| Teaching page (visible text) | 62 |
| ENTRY.md | 7 |
| wiki/build-a-harness.md | 5 |
| wiki/case-study.md | 10 |
| wiki/grill.md | 6 |
| wiki/guardrails.md | 5 |
| wiki/improve.md | 5 |
| wiki/orchestrate.md | 5 |
| wiki/records.md | 4 |
| wiki/run-unattended.md | 5 |
| wiki/start-a-task.md | 5 |
| wiki/unstick.md | 7 |
| wiki/verify.md | 5 |

## Growth

Each row is a commit where one of the counts changed.

| Date | Commit | Runbooks | Skills | Router rows | Scenarios | Test cases | Playbook lines |
|---|---|---|---|---|---|---|---|
| 2026-10-24 | `64fc579` | 0 | 0 | 0 | 0 | 0 | 0 |
| 2026-10-24 | `e367f9d` | 0 | 0 | 0 | 0 | 0 | 1,481 |
| 2026-10-24 | `5a0e8f3` | 0 | 1 | 0 | 0 | 0 | 1,481 |
| 2026-10-24 | `31b8e00` | 8 | 1 | 0 | 0 | 0 | 1,481 |
| 2026-10-24 | `6eb9f54` | 8 | 1 | 0 | 0 | 0 | 1,512 |
| 2026-10-24 | `53c9f6c` | 8 | 1 | 18 | 0 | 0 | 1,512 |
| 2026-10-24 | `8745e2e` | 8 | 2 | 18 | 0 | 0 | 1,512 |
| 2026-10-24 | `144bf58` | 9 | 2 | 18 | 0 | 0 | 1,512 |
| 2026-10-24 | `5d37683` | 10 | 3 | 18 | 0 | 0 | 1,512 |
| 2026-10-24 | `6a3128a` | 10 | 3 | 18 | 18 | 13 | 1,512 |
| 2026-10-24 | `c71b095` | 10 | 3 | 18 | 18 | 44 | 1,512 |
| 2026-10-24 | `8227c85` | 10 | 3 | 18 | 18 | 97 | 1,512 |
| 2026-10-24 | `6dda5b3` | 11 | 3 | 18 | 18 | 97 | 1,512 |
| 2026-10-24 | `e228914` | 11 | 3 | 18 | 18 | 99 | 1,512 |
| 2026-10-24 | `5a62f37` | 11 | 3 | 18 | 18 | 118 | 1,512 |
| 2026-10-24 | `dc5f7ee` | 11 | 3 | 18 | 18 | 147 | 1,512 |
| 2026-10-24 | `2c6bc7c` | 11 | 3 | 18 | 18 | 160 | 1,512 |
