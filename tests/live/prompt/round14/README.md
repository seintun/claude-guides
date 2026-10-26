# Round 14 evidence: /prompt v10

The reviewer, judge, audit, must-haves and grader files behind every number in round 14 ([../results.md](../results.md)) and dry-run round 8 ([../../grill-prompt/results.md](../../grill-prompt/results.md)). Plan and dated decisions: [docs/plans/prompt-v10.md](../../../../docs/plans/prompt-v10.md). Local paths are replaced with `<scratch>`. Pair files hold the score columns each blind reviewer returned. The `*.json` keys unblind them: they map each X, Y, D or J label to a trial. T1 is the round-11 v7 drafts, T2 and T3 are fresh v7 trials, U1 and U2 are v10 trials, and D3 is the D3 variant.

| Folder | What it holds |
|---|---|
| [phase0-t1-t2/](phase0-t1-t2/) | v7 against v7, round-11 drafts (T1) against a fresh trial (T2): pairs, audit, must-haves and the margins they gave (`margins.md`) |
| [phase0-t2-t3/](phase0-t2-t3/) | Two fresh v7 trials, T2 against T3: the margins the gates use |
| [dry-margin/](dry-margin/) | Two judges on v7's frozen round-5 dry runs (the dry-run margin) |
| [bundle/](bundle/) | v10 against v7: U1 against T2 (`a-*`) and U2 against T3 (`b-*`): pairs, audits, must-haves |
| [dry-run/](dry-run/) | Dry-run judges: v10 with v7's frozen runs (judges 1 and 2), the bisect without R1, and v10 with fresh v7 runs |
| [d3/](d3/) | D3 against U1: the bugfix and refactor probe, then all six scenarios |
| [codex/](codex/) | An outside judge (Codex CLI 0.164.0, read-only) on the same blinded bundle pairs (`a-*`, `b-*`) and the fresh-v7 dry runs (`dry.md`), with `comparison.txt` unblinding them and matching each judgment to Claude's |
| [end-to-end/](end-to-end/) | The fixture builder, the hidden archive's sha256, both runs' receipts, and the grader's map and results |

## Where each number comes from

| Number | Value | File |
|---|---|---|
| T1 against T2, pair means | 8.000 / 6.458 | `phase0-t1-t2/margins-pairs.txt` |
| M_pair, M_scen (gates) | 0.250, 2.00 | `phase0-t2-t3/b23-margins-pairs.txt` |
| M_audit (gates) | 2 (T2 6, T3 8) | `phase0-t2-t3/b23-audit-reply.md` |
| M_must (gates) | 3 (M1, B2, O3) | `phase0-t2-t3/b23-must-haves.md` with `p0-battle23.json` |
| M_dry | 0 (3 and 3) | `dry-margin/judgeA-grades.md`, `dry-margin/judgeB-grades.md` |
| v10 against v7, pair means | 7.79 / 7.00; 19 of 24 wins | `bundle/*-pair-*-reply.md` with `v10-a.json`, `v10-b.json` |
| Audit gap | U1 8 against T2 3; U2 7 against T3 9 | `bundle/a-audit-reply.md`, `bundle/b-audit-reply.md` |
| Must-haves | none lost | `bundle/a-must-haves.md`, `bundle/b-must-haves.md` |
| Dry run against frozen v7 | 7 to 1, 9 to 1 | `dry-run/judge1-grades.md`, `dry-run/judge2-grades.md` |
| Bisect without R1 | 6, v10 6, v7 3 | `dry-run/judge-noR1-grades.md` |
| Dry run against fresh v7 | 7 to 7 | `dry-run/judge-fresh-v7-grades.md` |
| D3 probe | 7.75 / 7.25 | `d3/d3-probe-replies.md` |
| D3 full | 7.58 / 7.42 | `d3/d3f-pair-*-reply.md` with `d3-full.json` |
| End-to-end | no false PASS; hidden tests H1 to H6 | `end-to-end/grader.md`, `end-to-end/grader-map.md` |
| Codex, pairs | v10 6.58 / v7 6.63; 10 of 24 wins; 13 of 24 judgments agree with Claude | `codex/comparison.txt` |
| Codex, dry run | v10 16 / fresh v7 19 failures | `codex/dry.md`, `codex/comparison.txt` |
