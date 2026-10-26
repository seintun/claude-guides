# Discovery: customer onboarding rebuild

Started 2026-10-24. Written as the grill runs, so a new session can resume from this file.

## Request (verbatim)

> Rebuild our customer onboarding so new clients are live in one day instead of two weeks. Must not change the contract process. Also legal wants every client to sign the new data agreement before onboarding, which currently takes about 10 days. We want it done this quarter, but there's only one engineer, part time. And maybe add a self-serve portal too.

## Searched

2026-10-24: the project root holds no files (no README, CLAUDE.md, docs/, code, config or earlier notes), so nothing here answers a fact question about the current onboarding.

## Given by the request (not asked)

- Goal: new clients live in one day instead of two weeks.
- No-go: the contract process does not change.
- Legal's rule: every client signs the new data agreement before onboarding; signing takes about 10 days today.
- Failure case: a client goes live without a signed data agreement.
- Deadline: "this quarter" (end date not given, see open questions). Staffing: one engineer, part time. Portal: "maybe".

## Decisions

1. 2026-10-24. Q: When does the one-day clock start? A: when the client's signed data agreement arrives. Why: legal requires signing before onboarding, and the signing takes about 10 days, so the one day can only cover what happens after it. Consequence: the signing time stays outside this goal; a client's wait from first contact will still be longer than one day. Rejected: counting from first contact (unreachable without faster signing, which this project can't deliver); going live before signing (breaks legal's rule).

2. 2026-10-24. Q: How does the new data agreement sit next to the contract process, which must not change? A: the data agreement is its own step before onboarding, outside the contract process, with its own record that onboarding checks before a client goes live. Why: it is the only reading that keeps "must not change the contract process" and "every client signs the new data agreement" both true. Consequence: clients sign two documents; the two records must be linked; no client goes live without the data-agreement record (the failure case from the request). Rejected: folding it into the contract process (changes what was ruled out).

3. 2026-10-24. Q: How should the rebuild be scoped, given one part-time engineer and a deadline at the end of this quarter? A: ship in slices, the slowest removable steps first, and stop when the time runs out. Why: slices leave something usable if time runs out; a full rebuild can't be shown to fit. Consequence: some steps may stay manual, and the one-day goal may not be fully met by the deadline; the one-day goal is the target the slices are measured against. Rejected: a full rebuild with one day as a hard requirement; keeping the full scope and moving the deadline.

4. 2026-10-24. Q: Is the self-serve portal part of this work? A: out of scope this quarter; list it as a follow-up. Why: a portal is a second project and would take time from the steps that decide whether one day is reachable. Consequence: clients still depend on staff to onboard them until a later project. Rejected: a stretch goal after all slices (a half-built portal may be left behind); in scope (conflicts with the slice scoping in decision 3).

5. 2026-10-24. Q: Which assumption should be tested first? A: the riskiest assumption is that most of the wait after signing is manual or waiting work that software can remove. Cheapest test: record every step of a recent completed onboarding with its start, end and what it waited on, and see where the days go. Why: if most of the wait is people waiting on people, nothing the engineer builds can reach one day, and the test only reads a past onboarding's records. Consequence: the test needs access to those records (location UNKNOWN) and also answers the UNKNOWN about whether signing is inside today's two weeks. Second risk, not tested yet: that one part-time engineer can build enough in the time there is (hours and end date UNKNOWN).

## No-gos and rabbit holes

- No-go (request): the contract process does not change (decision 2).
- No-go (request, decision 4): the self-serve portal is a follow-up, not part of this work.
- Rabbit hole: shortening the roughly 10 days of signing. It is legal's and the client's step and sits outside the one-day goal (decision 1).
- Rabbit hole: a full rebuild of the onboarding before the slowest steps are removed (decision 3).
- Failure case (request, decision 2): a client goes live without a recorded signed data agreement.

## Open questions

- UNKNOWN: whether today's two weeks already includes the about 10 days of signing or comes on top of it (asked 2026-10-24; the user doesn't know, and the project holds no records). The time after signing today is therefore not known.

- UNKNOWN: which event marks a client as "live", the last step of onboarding (asked 2026-10-24; the user doesn't know). The one-day goal has no finish line until this is filled in.

- UNKNOWN: how many hours a week the one part-time engineer has for this work (asked 2026-10-24; the user doesn't know; the request says only "part time").

- UNKNOWN: the end date of "this quarter" (asked 2026-10-24; the user doesn't know whether it is a calendar or a fiscal quarter). The deadline has no absolute date.

- UNKNOWN: where today's onboarding lives, meaning the repository, tools, data stores and records the work reads or changes (asked 2026-10-24; the user doesn't know, and the project folder is empty).

- UNKNOWN: what the two-week wait costs the clients or the business today (asked 2026-10-24; the user doesn't know).
- UNKNOWN: where the signed data agreement is recorded, if it is recorded at all (asked 2026-10-24 during /prompt; the user doesn't know, and the project folder is empty). The go-live gate (decision 2) and the one-day clock (decision 1) both depend on it.
- UNKNOWN: which files, data and records make up the contract process (asked 2026-10-24 during /prompt; the user doesn't know). The no-change constraint can't be proven without them.

## Assumed

None. The grill filled nothing in itself; every gap above is an UNKNOWN because the user said they don't know.
