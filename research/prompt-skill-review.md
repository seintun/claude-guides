# /prompt v7: the sourced review behind v8

On 2026-10-25, `/prompt` v7 was scored against three things: the playbook, Anthropic's own guidance, and published research. This note records the scores and the findings that v8 answers. The source lists themselves are in [prompt-skill-sources.md](prompt-skill-sources.md); scorers read that file, never this one.

## Method

- Two `doc-checker` passes fetched every source, and the lists keep only what the sources support.
- Fresh reviewers then scored v7 from files only, with none of the builder's conclusions:
  - A Sonnet reviewer graded `skills/prompt/SKILL.md` against 47 recommendations it drew from the playbook sections the skill cites.
  - An Opus reviewer graded the skill's text against G1 to G28 and R1 to R9. It also graded four prompts v7 wrote against G1 to G28.
- Scoring: PASS 1, PARTIAL 0.5, MISSING and CONFLICT 0; N/A is excluded.

## v7's scores

| Measured against | Score |
|---|---|
| The playbook | 27 of 47 (57%): 18 PASS, 18 PARTIAL, 11 MISSING, 0 CONFLICT, 8 N/A |
| Anthropic guidance, the skill's own text | 21 of 28 (75%) |
| Anthropic guidance, four prompts it wrote | 23.5 of 27 (87%) |
| Research | 6.5 of 9 (72%) |

## Findings v8 acts on

| ID | Finding | Rests on |
|---|---|---|
| F1 | Step 5 asks for all eight parts, but step 3 says a single slice needs only a goal, checks and a receipt | G17, G22, R5 |
| F2 | The skill has no example and no tags around the user's input | G4, G5 |
| F3 | Step 8 is a nine-item procedure written as prose | G6, R5, playbook Law 9 |
| F4 | The ASSUMED list sits above GOAL, in the prompt's most-read position | R4 |
| F5 | There is no fresh reviewer at normal risk, only at high risk | playbook §9.3 |
| F6 | No hard constraint names the gate that enforces it | playbook Law 9 |
| F7 | Helper briefs lack "already ruled out" and "already decided" | playbook Template C |
| F8 | Unattended runs lack idempotent actions, tool and permission limits, and an output cap | playbook §11.3, Template H; G16 |
| F9 | Plan files go to `<scratch>` instead of `docs/plans/`, where Template B makes them the source of truth | playbook Template B |
| F10 | No line says to report a wrong test instead of editing it, or to stop when the work is done | G14, G25 |
| F11 | Contradictions came in through edits made to fix review blockers | the round 11 audit, [tests/live/prompt/results.md](../tests/live/prompt/results.md) |

## What happened to v8 (2026-10-25)

v8, built from these findings ([docs/plans/prompt-v8.md](../docs/plans/prompt-v8.md)), scored higher than v7 on both lists, in one blind run per scorer that graded both versions:
- **Playbook:** v8 66.3%, v7 55.4%.
- **External:** v8 90.9%, v7 74.8%.

It still failed four of its gates and was not shipped:
- **Blind comparison:** v7 won 11 of 12 pairs.
- **Must-haves:** v8 lost one that v7 had in 5 of 6 scenarios.
- **Contradictions:** 6 in v8 against 4 in v7.
- **Dry run:** 7 failures out of 60 checks against v7's 2.

Satisfying more of these recommendations made the prompts shorter and dropped checks that readers valued. Treat a score against these lists as a check on coverage, never as a stand-in for a blind comparison.

## Not adopted

pass^k for unattended runs (playbook §9.3). It measures a harness over many runs, so a single prompt can't carry it.

## Limits

- One reviewer per lane.
- Claude graded Claude's work, which R3 warns inflates scores.
- The playbook score counts some harness practices that a prompt can only point to.
- Read every figure as ±5 points.
