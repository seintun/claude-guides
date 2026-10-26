# Three requests for the /grill and /prompt dry run

Each request goes through `/grill`, then `/prompt` with the grill's decision log as input. A simulated user answers.

## Dump 1: small task
"My CLI's --help text is out of date after we renamed the export flag. Fix it so it matches. Should take an hour."

## Dump 2: report
"Need a write-up for my manager on whether we should move CI from GitHub Actions to Buildkite. Costs have gone up and builds are slow on the monorepo. She wants it next Friday, and she cares most about cost and how much migration work it is. I don't know our actual monthly CI spend."

## Dump 3: large project with contradictions
"Rebuild our customer onboarding so new clients are live in one day instead of two weeks. Must not change the contract process. Also legal wants every client to sign the new data agreement before onboarding, which currently takes about 10 days. We want it done this quarter, but there's only one engineer, part time. And maybe add a self-serve portal too."

## Simulated user

- For a question with options, pick the recommended option unless the request clearly implies another.
- For an open fact question, answer only from the request. If it doesn't say, answer "I don't know".
