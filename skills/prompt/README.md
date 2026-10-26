# /prompt

`/prompt <description>` turns a description or scenario into a ready-to-run prompt for Claude agents. It interviews you only for gaps, sizes the prompt by risk, and fills the playbook's templates: B for a task, C for helper briefs, H for loops. It saves the prompt in the guide, not in your project.

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill |
| [check_prompt.py](check_prompt.py) | The deterministic check the skill runs on its draft before the fresh review. It FAILs on a missing part (a `Risk: trivial` prompt may leave out CONTEXT), no `Risk: trivial`, `Risk: normal` or `Risk: high` line before GOAL, a DONE WHEN outside 2 to 5 checks, two gaps on one UNKNOWN line, more than 3 UNKNOWN lines with no "not ready", or an unresolved relative term. It WARNs on a figure it can't trace to a `--source` file, a figure marked `ASSUMED` twice, or a check that rests on an UNKNOWN. Each check comes from a failure in the [grill-then-prompt dry runs](../../tests/live/grill-prompt/results.md) |
| [tests/live/prompt/scenarios.json](../../tests/live/prompt/scenarios.json) | Six scenarios drawn from common trouble spots: feature, bug fix, overnight loop, research with helpers, refactor, migration |
| [tests/live/prompt/run.sh](../../tests/live/prompt/run.sh) | A/B battle test: each scenario in a fresh `claude -p` session outside the repo, once with the skill and once with a plain "write me a prompt" request |
| [tests/live/prompt/score.py](../../tests/live/prompt/score.py) | A 21-check rubric drawn from the playbook (Law 3, §7, §9.1, §9.3, §9.4, Templates B, C and H) |
| [tests/live/prompt/interview.sh](../../tests/live/prompt/interview.sh) | Checks that a vague request gets one question, recommendation first, after looking things up |

## Where prompts go

`<guide>/prompts/<project>/<YYYY-MM-DD>-<short-name>.md`. The `prompts/` folder is git-ignored apart from its README, so a prompt never reaches the guide's repository or the project's. The skill finds the guide with `git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel`, the same way `/guide` does. Installed with `npx skills add` (a copy, not a clone), it saves to `~/.claude-guides/prompts/<project>/` instead, still outside every repository. See [wiki/records.md](../../wiki/records.md).

**Known conflict.** A harness hook that blocks edits in a checkout on its default branch also blocks this save once the guide sits on `main`. The skill then does not work around the hook. It keeps the prompt in its scratchpad and gives you one `cp` command to move it into place. Round 3 showed this; see the results below.

## How it was tested

1. **Rubric A/B.** Six scenarios, skill against a plain request, scored by `score.py`. The rubric comes from the same playbook as the skill, so the skill is partly graded against its own design. Treat these numbers as a check that the playbook's practices reach the prompt, not as a measure of quality. `--lenient` scoring stops a baseline from losing points for format alone.
2. **Blind pairwise review.** A fresh Opus reviewer saw each pair as X and Y, with neutral criteria: outcome clarity, whether the checks prove the claim, safety, fit and delegation. It didn't know which draft came from the skill. Its notes drove each revision.
3. **Interview check.** A vague request must get one question, the recommended option first, after looking things up, with nothing written.
4. **Save check.** The skill arm runs against a throwaway guide repository, and the test confirms the file lands in `prompts/<project>/` with nothing written in the project.
5. **Frozen comparison.** From v8 on, each version is measured with briefs, a rubric and must-haves committed before its code changes ([tests/live/prompt/briefs/](../../tests/live/prompt/briefs/README.md), [rubrics/](../../tests/live/prompt/rubrics/playbook.md), [must-haves.md](../../tests/live/prompt/must-haves.md)), against the previous version's kept drafts and runs ([baselines](../../tests/live/prompt/baselines/README.md)).

## Results (2026-10-24 and 2026-10-25)

Full tables and the reasons behind each revision are in [tests/live/prompt/results.md](../../tests/live/prompt/results.md).

- **Blind reviews:**
  - v1 tied the baseline 3–3 (7.3 vs 7.0);
  - v2 won 6–0 (8.0 vs 5.8);
  - v3 won 6–0 (7.8 vs 6.0);
  - v4 won 6–0 (8.2 vs 6.7), though the reviewer found contradicting constraints in 5 of its 6 drafts;
  - v5, which adds a consistency pass, won 6–0 against the baseline (8.2 vs 6.2) and 4–2 against v4 (8.2 vs 7.3). A blind audit found 10 contradictions in its drafts against 12 for v4: fewer, not none.
  - The checker trial (round 9), a v5 variant with a separate checker and a 100-line aim, cut contradictions to 2 but lost 11 of 12 pairs to v5 because its shorter drafts dropped checks. It was not shipped; see `tests/live/prompt/variants/`.
  - v6, v5 merged with the retired `/brief`'s rules, `check_prompt.py` and a fresh review before saving, tied v5 6–6 across both position orders (7.5 vs 7.6). A blind audit found 3 contradictions in its drafts against 7 for v5, but rated them more over-specified (14 vs 11 of 18), and they were no shorter.
  - v7 lists each chosen figure once, asks where the work lives, and gives the fresh review three pointed questions. It tied v6 7–5 across both orders (7.5 vs 7.5), with drafts 6.5% shorter and 37% fewer `ASSUMED` tags. Pairwise reviewers counted fewer conflicts in its drafts (4 vs 6), but a blind audit counted more (11 vs 4).
  - v8 was built from a sourced review of v7 ([research/prompt-skill-review.md](../../research/prompt-skill-review.md)). It scored higher against the playbook and the sources, but lost 1 to 11 in blind review, dropped must-haves in 5 of 6 scenarios and failed 7 of 60 dry-run checks against 2. It was not shipped.
  - v9 kept v8's playbook-backed rules and restored what v8 dropped: Templates B and L's sizes, Template B's trivial form, and a rule that each check fails on its likeliest fake. It also scored higher on both lists, but lost 5 to 7 in blind review, lost one must-have, had more contradictions (12 vs 8) and failed 13 of 60 dry-run checks against 6. It was not shipped; v7 is the current version.
  - v10 is v7 plus six playbook-required items, each its own commit: Template L's risk sizes and Template B's trivial form, a fresh diff review at normal and high risk, a named gate per hard constraint at high risk, briefs that say what is settled, safe loops, and plan files in `docs/plans/`. Judged against two fresh v7 trials, it won 19 of 24 pairs (7.8 vs 7.0) and lost no must-have. An outside judge (Codex) on the same blind pairs scored it a tie (6.6 vs 6.6, 10 of 24), so read v10 as no worse than v7, not clearly better. Two of its prompts ran to completion with no false PASS under hidden tests. Evidence: [tests/live/prompt/round14/](../../tests/live/prompt/round14/README.md).
- **Rubric:**
  - v4 scored 67 of 67;
  - v6 scored 62 against v5's 59, and v7 60 against v6's 62, on drafts written by subagents;
  - the baseline scored 23–24, or 27–28 in lenient mode.
- **Interview check:** passed 8 of 8.
- **Grill-then-prompt dry run:** v6 failed 4 of 30 risk checks, against 13, 10 and 9 in the three earlier rounds, and no final prompt had a FAIL from `check_prompt.py`. v7, run twice per request and graded by one blind judge alongside v6, failed 3 of 60 against v6's 4 of 30. The two v7 sets differed by 3, so the totals are within noise, but the risks v7 targets (a stop condition that already holds, a fallback that skips the GOAL, where the work lives) failed in 2 v6 runs and no v7 run. See [tests/live/grill-prompt/results.md](../../tests/live/grill-prompt/results.md).
- **Save check:** v2 to v4 saved in the guide's `prompts/<project>/` in 6 of 6 runs each, and wrote nothing in the project.
- **Run to completion:** two v10 prompts (a CSV export and a session bug) ran on a small Node app; hidden tests passed and no receipt claimed a false PASS.

## Install

Without a clone, with the [skills CLI](https://github.com/vercel-labs/skills); it copies `check_prompt.py` along with the skill:

Run `npx skills add seintun/claude-guides --skill prompt` from your project. <!-- privacy: allow -->

Or link it from your clone. Run this in your own terminal; Claude Code's sandbox blocks writes to `~/.claude/skills`:

```bash
ln -s "$(git rev-parse --show-toplevel)/skills/prompt" ~/.claude/skills/prompt
```

To undo, run `rm ~/.claude/skills/prompt`. ENTRY.md routes "write a prompt for an agent" here (row 19).
