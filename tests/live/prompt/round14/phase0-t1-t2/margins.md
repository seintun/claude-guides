# Phase 0 margins (v7 trial 1 = round-11 baselines, v7 trial 2 = fresh, 2026-10-25)

| Margin | Value | Source |
|---|---|---|
| M_pair | 1.542 (T1 mean 8.000, T2 mean 6.458, 12 judgments) | p0/pair-1-reply.md, p0/pair-2-reply.md, keys/p0-battle.json; computed by margins.py into p0/margins-pairs.txt |
| M_scen | 3.00 (overnight: T1 8.75, T2 5.75); feature 1.75, refactor 2.00, migration 1.25, research 1.25, bugfix 0.00 | same |
| M_must | 3 (B2, RF2, R2: PRESENT in T1, ABSENT in T2; O1 and F2 ABSENT in both) | p0/must-haves.md (D05/D11, D03/D07, D04/D10) |
| M_audit | 1 (T1 9, T2 8) | p0/audit-reply.md |
| M_dry | 0 (judge A 3: R5, R5, R4; judge B 3: R4, R2, R4) | p0/judgeA-grades.md, p0/judgeB-grades.md, keys/p0-judgeA.json, keys/p0-judgeB.json |

Stop rule: M_pair >= 1.0 holds (1.542). M_audit >= 4 does not.

Win count: T1 won 10 of 12 judgments; position X won 7 of 12. Bugfix split by position (X both times).

Runs used in phase 0: 6 drafters, 3 step-10 reviews (overnight, refactor, migration; feature, bugfix and research judged step 10 not to apply), 2 judges, 2 pairwise, 1 audit, 1 must-haves = 15 of 18. All fix rounds continued their drafter. Refactor and migration got their rerun check back once more for a c-3 FAIL left after the fix round.
