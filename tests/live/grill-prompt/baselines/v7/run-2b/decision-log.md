# Discovery log: write-up on moving CI from GitHub Actions to Buildkite

Started 2026-10-24 (a Saturday). Status: summary confirmed by the user 2026-10-24; no plan, spec or code written.

## Request

> Need a write-up for my manager on whether we should move CI from GitHub Actions to Buildkite. Costs have gone up and builds are slow on the monorepo. She wants it next Friday, and she cares most about cost and how much migration work it is. I don't know our actual monthly CI spend.

## Found before asking

- Searched the project folder for a README, CLAUDE.md, docs, CI configuration, billing exports and build logs: the folder is empty, with no git repository. Nothing about the CI is in the project.
- Given by the request: the question is move or not; costs have gone up; builds on the monorepo are slow; the manager's priorities are cost first, then migration work; the deadline is "next Friday"; the monthly CI spend is not known to the user.

## Decisions

1. 2026-10-24. Q: What should the write-up be? A: A short decision memo that opens with a move, stay or wait call, then the cost case and the migration work, then detail. Reason: the request asks "whether we should move", which needs a call; a neutral table leaves her question open and a migration plan presumes yes.
2. 2026-10-24. Q: What is Buildkite compared against? A: Staying on GitHub Actions as it runs today. Any in-place fix is out of scope, and the memo says so. Reason: it is the question asked ("whether we should move") and fits the deadline; an in-place fix would be a second research branch.
3. 2026-10-24. Q: Which costs does the write-up count? A: Everything that changes with the move, as separate lines: vendor charges, the compute the builds run on, and the migration effort in engineer-weeks. Reason: she cares about migration work as well as the bill, and bills alone would hide it.
4. 2026-10-24. Q: How is the migration work expressed? A: A counted inventory (workflow files, third-party actions, secrets, runner types) from the monorepo's CI configuration, then a low-to-high range in engineer-weeks with its main drivers. Without the configuration the memo lists what to count and gives no range. Reason: she ranks migration work second; counted items can be checked and a size label cannot.
5. 2026-10-24. Q: How much weight does build speed get? A: A secondary criterion. The memo reports current build times and what a move could change, and promises no gain. Reason: the request puts cost and migration work first, and a speed gain is the claim least likely to be proven in a desk write-up.
6. 2026-10-24. Q: What decision rule does the memo give? A: The net monthly saving and the migration effort in engineer-weeks side by side, and a formula for months to repay the work, with the cost of an engineer-week left as the manager's input. No single payback number. Reason: an engineer-week rate is a company figure the user does not have; converting would add a guess or another unknown.
7. 2026-10-24. Q: What is out of bounds while the write-up is prepared? A: Desk research only: public pricing and documentation, plus data the user supplies. No vendor sign-ups, trials or sales contact, no change to any CI configuration, no pilot pipeline, and no message sent to the manager or anyone else. Reason: the memo is advice; a trial or a contact would commit the company before she has seen the numbers.
8. 2026-10-24. Q: Which assumption is riskiest, and what is its cheapest test? A: That the saving is real once the build compute and migration effort are counted. Cheapest test: price the last full billing period of GitHub Actions usage against Buildkite's published pricing, first. Not tested in this write-up: whether the slow builds come from the CI service or from the monorepo's own build design; the memo says so. Reason: cost is what she cares about most, and the test needs only public prices and the user's usage.
<!-- decisions-end -->

## Open questions

- UNKNOWN: location of the monorepo and its CI configuration. Asked 2026-10-24; the user did not know, and the project folder is empty. The migration inventory (decision 4) cannot be built until it is located.
- UNKNOWN: where the GitHub Actions bill and usage figures can be read (a billing page, an export or a person). Asked 2026-10-24; the user did not know. The cost case (decisions 3 and 6) needs them.
- UNKNOWN: the deadline's calendar date. Said on Saturday 2026-10-24, "next Friday" is 2026-10-30 or 2026-11-06; asked once, the user did not say which.
- UNKNOWN: the monthly CI spend. The user stated they do not know it, so it was not asked again.
- ASSUMED: "build time" means wall-clock time from a push to the last check finishing on the monorepo's main pipeline. No check depends on it.
<!-- open-end -->
