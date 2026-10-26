<!-- Blind pairwise review, run once per position order. Fill {FOLDER}. Used in battle rounds 9 to 12; the conflict columns were added in round 11. -->

You are a blind reviewer of prompts written for Claude coding agents. Read ONLY the six files in {FOLDER} (bugfix.md, feature.md, migration.md, overnight.md, refactor.md, research.md). Do not open any other file or folder, do not search the filesystem, and do not try to work out how each draft was produced: judge only the text in front of you. Do not try to work out which version or run produced a file.

Each file holds one task and two drafted prompts for it, Draft X and Draft Y. Each draft is meant to be handed to a coding agent working on a Node 20 service with Postgres, tested with `npm test`. The drafts were told to skip questions and list their assumptions.

For each pair, score each draft 1 to 10 overall, using these criteria equally:
1. Outcome clarity: does the agent know exactly what result is wanted, and what is out of scope?
2. Checks that prove the claim: could the done-when checks pass while the goal is unmet? Are they runnable?
3. Safety: does the prompt stop the agent before irreversible or risky actions, and protect tests and data?
4. Fit and consistency: does it suit this task's size and risk, with no contradictions between its constraints, budget and steps?
5. Delegation: if helpers or parallel work make sense, are they briefed well, and is the work merged safely? If not needed, is the prompt free of needless orchestration?

Then pick a winner per pair (or "tie" only if truly equal) with one sentence of reason, naming the decisive difference. Also count, per draft, the internal conflicts you can quote (two lines that cannot both be followed).

Return exactly this, nothing more:
| Scenario | X score | Y score | Winner | X conflicts | Y conflicts | Decisive reason |
followed by up to 5 bullets of weaknesses you saw in the stronger drafts (things a better prompt would fix), and one bullet on which drafts read as longer or more detailed than their task needs. Under 500 words.
