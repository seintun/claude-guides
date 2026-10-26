Prompt saved at <run folder>/prompt.md. It is not ready to run: it has six UNKNOWN lines, more than the guide allows, so fill in what you can first. A fresh reviewer checked it in two rounds and the second found no open blockers.
Edit the lines that carry your judgment: GOAL, DONE WHEN and STOP AND ASK IF.
Start a fresh session with "run the prompt in <run folder>/prompt.md", and name the paths of the workflow files and the usage report in that message if you have them.
The decision log behind the prompt is `docs/discovery/ci-buildkite-writeup.md` in the project. Confirm each line below knowingly.

ASSUMED: the write-up is one Markdown file, `<scratch>/ci-move-writeup.md`, a short memo with six sections in this order: Recommendation, Cost, Migration effort, Speed, Risks, Open items.
ASSUMED: at most 12 distinct public pages are read in total, the reviewer's reads included.
ASSUMED: one helper, the fresh reviewer, run once per round, for at most two rounds.
ASSUMED: each field a reviewer returns is about 40 words at most.
UNKNOWN: the deadline date. "Next Friday", said on Saturday 2026-10-24, is 2026-10-30 or 2026-11-06, and the user could not say which.
UNKNOWN: where the monorepo and its GitHub Actions workflow files live.
UNKNOWN: which report or account shows the monthly CI cost and usage.
UNKNOWN: the actual monthly CI spend.
UNKNOWN: the typical monorepo build duration today.
UNKNOWN: whether the manager named a figure that decides yes or no (a saving she needs, a limit on migration effort, a build time she wants).
