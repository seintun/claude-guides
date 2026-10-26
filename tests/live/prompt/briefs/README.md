# /prompt evaluation briefs

The exact briefs the /prompt evaluations hand to fresh reviewers, as templates. Each names only the files its reviewer may read, never includes a builder's report, and tells the reviewer not to work out which version produced a file. Frozen on 2026-10-25 for the v7 against v8 comparison ([docs/plans/prompt-v8.md](../../../../docs/plans/prompt-v8.md)).

| File | Who uses it |
|---|---|
| [reviewer-round1.md](reviewer-round1.md) | The fresh reviewer that /prompt step 10 calls for, first round, with its three questions |
| [reviewer-round2.md](reviewer-round2.md) | The same reviewer's second round: which blockers closed, and whether the fixes made new ones |
| [blind-pair.md](blind-pair.md) | A blind pairwise reviewer, run once per position order |
| [audit.md](audit.md) | The one-at-a-time contradiction audit of every draft |
| [must-haves.md](must-haves.md) | The check of each draft against [../must-haves.md](../must-haves.md) |
| [judge.md](judge.md) | The blind judge of the grill-then-prompt dry runs, grading every version's runs together |
| [score-playbook.md](score-playbook.md) | Scores two skill versions against [../rubrics/playbook.md](../rubrics/playbook.md) in one run |
| [score-external.md](score-external.md) | Scores two skill versions and their sample prompts against [research/prompt-skill-sources.md](../../../../research/prompt-skill-sources.md) in one run |
