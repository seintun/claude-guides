# Customer onboarding rebuild: decision log

Grill started 2026-10-24.

Request, verbatim: "Rebuild our customer onboarding so new clients are live in one day instead of two weeks. Must not change the contract process. Also legal wants every client to sign the new data agreement before onboarding, which currently takes about 10 days. We want it done this quarter, but there's only one engineer, part time. And maybe add a self-serve portal too."

## Looked up first

2026-10-24: searched the project root for code, README, CLAUDE.md, docs, data and git history. It is empty (no code, no records, no repository), so no fact could be found there. Every answer below comes from the user.

## Decisions

Each entry: date, question, answer, reason.

1. 2026-10-24. Question: what does the one-day count start from, given the data agreement takes about 10 days to sign and must be signed before onboarding? Answer: it starts when the client signs the data agreement and stops when they are live. The signing time stays outside this rebuild and is not part of the one-day goal. Reason: the only reading where legal's rule, the one-day goal and one part-time engineer all hold; engineering cannot control how fast legal gets a signature. Cost accepted: a client still waits the signing time plus a day, so the goal must not be reported as met from first contact.

2. 2026-10-24. Question: where does the new data agreement sit relative to the contract process, which must not change? Answer: it is a separate gate that must be complete before onboarding starts. The contract process is left exactly as it is, and no step of the rebuild may change it. Reason: it is the only option that keeps the no-change rule without waiting on anyone's answer. Cost accepted: two signings per client, and the agreement needs its own tracking that touches no contract step.

3. 2026-10-24. Question: if the date and the one-day goal cannot both be met with one part-time engineer, which gives way? Answer: the date holds. At the date, ship the slice that removes the most elapsed time and report how far the result is from one day. Reason: a date can be met by cutting scope, but a one-day goal cannot be met by trying harder, and today's baseline is unknown. Cost accepted: the one-day goal may not be met by the date.
4. 2026-10-24. Question: where does the "maybe" self-serve portal go? Answer: out of scope; a no-go for this work, revisited only after the plan is signed off. Reason: it is the largest add-on in the request, and the request itself says only "maybe". Cost accepted: no self-serve for clients in this work.

5. 2026-10-24. Question: which assumption is the riskiest, so it is tested first? Answer: that once the agreement is signed, every remaining onboarding step can be done within one day. Cheapest test: read-only, time each step from signature to live in the records of recently completed onboardings. Reason: everything else rests on the time after signing being close to one day, nobody knows today's figure, and the test costs a read, not a build. Not chosen, still open: that legal accepts the agreement as a gate outside the contract process, and that one part-time engineer has enough capacity. Cost accepted: the test needs access to records whose location is unknown, and it only yields a baseline.

## No-gos, rabbit holes and failure cases

From the request, not from a question:
- No-go: change the contract process.
- No-go: onboard a client before they have signed the new data agreement.
- Rabbit hole: the self-serve portal (decision 4).
- Rabbit hole: speeding up legal's signing of the data agreement (decision 1 keeps it outside the one-day goal).
- Failure case: a client goes live without a signed data agreement.
- Failure case: the one-day goal is reported as met when the clock started at a different event than decision 1 sets.

## Riskiest assumption and cheapest test

Riskiest assumption (decision 5): once the agreement is signed, every remaining onboarding step can be done within one day.
Cheapest test: read-only, time each step from signature to live in the records of recently completed onboardings. No build is needed.
Also open, not chosen as the riskiest: that legal accepts the agreement as a gate outside the contract process, and that one part-time engineer has enough capacity.

## Open questions

One gap per line.

UNKNOWN: the exact event that makes a client "live", which ends the one-day count (asked 2026-10-24, user did not know).
UNKNOWN: where onboarding happens today, meaning which code, tools, spreadsheets, tickets and records it touches (project folder empty, user did not know, asked 2026-10-24).

UNKNOWN: what the two-week wait costs today, in revenue, churn, support time or any other term (asked 2026-10-24, user did not know).
UNKNOWN: the last day of "this quarter" as an absolute date; the request does not say whether it is a calendar or a fiscal quarter (asked 2026-10-24, user did not know).
UNKNOWN: how many hours a week the one part-time engineer has for this (asked 2026-10-24, user did not know).

UNKNOWN: today's elapsed time from the client's signature on the data agreement to live; the request's "two weeks" has no stated start, and decision 1 moves the clock's start to the signature (logged 2026-10-24; the test in decision 5 fills it).

## ASSUMED

ASSUMED: none. Nothing was filled in by the grill itself.

Confirmed by the user on 2026-10-24 (the decisions and the UNKNOWN list; this is not a go-ahead to build, commit or publish).
