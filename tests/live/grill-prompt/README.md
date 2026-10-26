# live/grill-prompt

An agent-run dry run of `/grill`, then `/prompt`, on three requests. It checks the risks that a simulated user and a fresh judge can see: invented facts, figures slipped in through options, unresolved dates, hidden gaps, done-when checks a stranger can't run, contradictions, a missing problem or riskiest assumption, and no review of the output.

| File | What it is |
|---|---|
| [dumps.md](dumps.md) | The three requests (a small fix, a report, a large project with contradictions) and the simulated user's rules |
| [rubric.md](rubric.md) | The 10 risks the judge grades, R1 to R10, and the skill rule that guards each |
| [results.md](results.md) | Round 1 (before the rules moved in from the retired `/brief`), rounds 2 and 3 (after), round 4 (`/prompt` v6, the merged skill: 4 of 30), round 5 (`/prompt` v7: 3 of 60, two runs per request, graded by one judge alongside v6), rounds 6 and 7 (v8: 7 of 60, v9: 13 of 60, each graded beside v7's frozen runs; neither shipped), and round 8 (v10: 7 against 7 for fresh v7 runs made the same way) |

## How to run it

It needs agents, not a script. From a session in any folder:

1. Start six runner subagents, two per request, so the two runs of a request show the run-to-run noise. Each reads `skills/grill/SKILL.md` and `skills/prompt/SKILL.md` and nothing about earlier runs. It plays the simulated user from `dumps.md`, runs `/grill` to its confirmation, then `/prompt` with the grill's decision log as input, and stops at the hand-over. It treats a scratch folder outside this repository as the project root, saves the prompt there instead of in `prompts/`, and writes a transcript of every question and answer. Give runners the Write and Edit tools with absolute paths, and no shell or git commands in this repository: in round 3, a runner's test script fell back into the guide's worktree when its temporary folder failed, overwrote `README.md` and reset the git index.
2. Run `/prompt` steps 9 and 10 for real. A runner has no shell and cannot start its own subagent, so each runner writes its draft and pauses. The lead runs `skills/prompt/check_prompt.py` on the draft, with the decision log and the request as sources, and starts a fresh reviewer that reads only the draft, the decision log and `skills/prompt/SKILL.md`, and answers the three questions step 10 names. It sends both results back to the runner, which fixes them. Round 2 asks a new reviewer which blockers are closed and whether the fixes made new ones. After two rounds the runner saves and hands over.
3. Start one fresh judge that reads only `rubric.md`, `dumps.md` and every run's final files, including the previous version's runs, in random order and with every path that names a version or run removed. It grades R1 to R10 per run, with evidence. One judge for both versions keeps judge-to-judge variation out of the comparison.
4. Record the grades in `results.md`.

The briefs for steps 2 and 3 are in [../prompt/briefs/](../prompt/briefs/) (`reviewer-round1.md`, `reviewer-round2.md`, `judge.md`). v7's six runs are kept in [baselines/v7/](baselines/v7/), so the next version is judged alongside them instead of against a rerun.

Limits: the user is simulated, so the run tests the skills' instructions, not a real interview. The runners' project folders start empty, so facts about the code are unknowable and gaps pile up.
