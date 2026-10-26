# Discovery: moving CI from GitHub Actions to Buildkite (write-up for the requester's manager)

Started 2026-10-24 (Saturday). Status: summary confirmed by the user on 2026-10-24. Not committed: the project has no git repository.

## Request

"Need a write-up for my manager on whether we should move CI from GitHub Actions to Buildkite. Costs have gone up and builds are slow on the monorepo. She wants it next Friday, and she cares most about cost and how much migration work it is. I don't know our actual monthly CI spend."

## Found before asking

- 2026-10-24: searched the project root for a README, CLAUDE.md, CI config (`.github/workflows`), docs and any billing or usage export. The folder is empty. Nothing to read, so no fact was found there.

## Decisions

- 2026-10-24 | Question: what is the deliverable? | Answer: a write-up that says whether to move CI from GitHub Actions to Buildkite. | Reason: stated in the request ("whether we should move"); not asked. A recommendation is wanted, not a neutral survey.
- 2026-10-24 | Question: who reads it and what do they weigh? | Answer: the requester's manager; she cares most about cost and how much migration work it is. | Reason: stated in the request; not asked. Her name is not given and does not change the write-up, so it is not asked.
- 2026-10-24 | Question: what is the problem? | Answer: CI costs have gone up and builds are slow on the monorepo. | Reason: stated in the request; not asked. How much and how slow are asked below.

- 2026-10-24 | Question: what is the move compared against? | Answer: A, move vs stay as-is (the current GitHub Actions setup at today's cost). | Reason: it is the question the manager asked; a stay-and-tune comparison needs workflow files the user cannot locate. A cheaper fix for Actions appears only as a follow-up line, not an analysis. Surveying other CI vendors is a no-go (rabbit hole).

- 2026-10-24 | Question: which assumption does the write-up test first? | Answer: A, that Buildkite costs less in total for the team's usage. | Reason: the manager ranks cost first. Cheapest test: reprice the last full month of Actions usage under Buildkite's published pricing plus the cost of running the build machines. That test needs the usage report (location UNKNOWN); until it is supplied the write-up gives a formula with named blanks. The speed assumption (B) and the migration-size assumption (C) are not tested first; both stay open questions in the write-up.

- 2026-10-24 | Question: how is migration effort expressed? | Answer: A, an inventory of what must be ported (workflows, secrets, build machines, caches, third-party actions) with effort as a range and a stated confidence level. | Reason: the workflow files are out of reach, so a range with a stated confidence is the honest form and still lets the manager plan. Without the files, the range is marked as missing input, not invented.

- 2026-10-24 | Question: what evidence may be used and what is off limits? | Answer: A, public vendor docs and pricing pages plus the team's own usage data. No-gos: no trial or account sign-up, no vendor contact, no spending, no change to the current CI. | Reason: free, quick, touches no account or production CI. Cost: speed claims stay unmeasured and prices are list prices, not quotes. A pilot (B) and a vendor quote (C) are rabbit holes for this deadline.

- 2026-10-24 | Question: how are unverifiable figures treated? | Answer: A, every figure is labelled as sourced (link, date read, quoted wording), supplied by the user, or an estimate with a range and its basis; none is invented, and a figure with no basis is a named missing input. | Reason: a wrong cost number in front of the manager is the worst failure; a visible gap beats a believable guess. Cost: some cells stay empty until the user supplies data.

<!-- decisions-end -->

## Open questions

- UNKNOWN: the deadline date. "Next Friday", said on Saturday 2026-10-24, is 2026-10-30 or 2026-11-06, and the user could not say which.
- UNKNOWN: where the monorepo and its GitHub Actions workflow files live. The project root is empty and the user could not say.
- UNKNOWN: which report or account shows the monthly CI cost and usage. The user could not say where the bill lives.
- UNKNOWN: the actual monthly CI spend. The user said so in the request.
- UNKNOWN: the typical monorepo build duration today. The user only knows builds are "slow".
- UNKNOWN: whether the manager named a figure that decides yes or no (a saving she needs, a limit on migration effort, a build time she wants). The user could not say.
- ASSUMED: the write-up is a short Markdown memo: recommendation first, then cost, migration effort, speed, risks and open items. The user did not choose the format.
<!-- open-end -->
