Phase 0b audit (folder p0/blind23/single), reply table as returned. Model: opus.

| File | Contradictions | Over-spec 0–3 | Missing essential |
|---|---|---|---|
| D01 | 2 | 2 | no |
| D02 | 3 | 2 | no |
| D03 | 2 | 2 | no |
| D04 | 1 | 1 | no |
| D05 | 1 | 1 | yes: no commit step, so check 2's base...HEAD diff can be empty |
| D06 | 2 | 2 | no |
| D07 | 1 | 2 | no |
| D08 | 0 | 2 | yes: no time or cost ceiling |
| D09 | 1 | 1 | no |
| D10 | 1 | 1 | no |
| D11 | 0 | 1 | no |
| D12 | 0 | 1 | no |

Unblinded (keys/p0-battle23.json): T2 = D01, D03, D04, D08, D10, D11 = 2+2+1+0+1+0 = 6. T3 = D02, D05, D06, D07, D09, D12 = 3+1+2+1+1+0 = 8. M_audit = 2.
Must-haves (p0/b23-must-haves.md): differences between T2 and T3 are M1 (migration, ABSENT in T3), B2 (bugfix, ABSENT in T3), O3 (overnight, ABSENT in T3). M_must = 3. Absent in both: RF2, R2, F2, O1.
