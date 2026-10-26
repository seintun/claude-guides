# Transcript, run 3a (Dump 3)

Request: "Rebuild our customer onboarding so new clients are live in one day instead of two weeks. Must not change the contract process. Also legal wants every client to sign the new data agreement before onboarding, which currently takes about 10 days. We want it done this quarter, but there's only one engineer, part time. And maybe add a self-serve portal too."

Date: 2026-10-24.

# Part 1: /grill

## Look before asking

I searched the project root (`project/`) for code, README, CLAUDE.md, docs, data and git history. The folder is empty, so nothing could be looked up. Every fact below has to come from you.

Your request already gives me these, so I will not ask them again:
- Goal: new clients live in one day instead of two weeks.
- No-go: do not change the contract process.
- Legal wants every client to sign the new data agreement before onboarding, and that signing takes about 10 days today.
- Deadline: this quarter. Capacity: one engineer, part time.
- Maybe: a self-serve portal.

Some of these pull against each other. I settle those first, because the rest of the design depends on them.

I will log every decision in `docs/discovery/customer-onboarding-rebuild.md` (under the project root) as we go.

### Question 1 (judgment)

Your request wants new clients live in one day, and also says legal's new data agreement must be signed before onboarding and takes about 10 days today. Both cannot hold if the day is counted from the client's first contact. What should the one-day count start from?

Why I recommend A: it is the only reading where legal's rule, the one-day goal and one part-time engineer can all hold at once. Engineering cannot control how fast legal gets a signature.

- A. Starts at signature (Recommended). The clock starts when the client signs the data agreement and stops when they are live. Implies: the signing time stays outside this rebuild, and this rebuild owns only what happens after. Costs: a client still waits the signing time plus a day, so the headline cannot be reported as met from first contact.
- B. Starts at first contact. The signing time counts toward the one day. Implies: the rebuild must cut the signing to almost nothing. Costs: the signing is legal's process, not engineering's, and one part-time engineer cannot deliver it.
- C. Overlap the two. Start setup while the agreement is pending and hold go-live until it is signed. Implies: a shorter total wait. Costs: it breaks legal's rule that signing comes before onboarding, and go-live still waits for the signature.

User answer: A.

### Question 2 (judgment)

Legal's data agreement is a new document every client signs, and you said the contract process must not change. Where does the data agreement sit relative to the contract process?

Why I recommend A: it is the only option that keeps your no-change rule without waiting on anyone's answer.

- A. Separate gate (Recommended). The agreement is its own signing step that must be complete before onboarding starts, and the contract process is left exactly as it is. Implies: two signings per client, tracked apart. Costs: the plan must find a home for tracking the agreement without touching any contract step.
- B. Part of the contract package. The agreement is attached to the existing contract. Implies: one signing for the client. Costs: it changes the contract process, which your request rules out, and it would need the contract process's owner to say yes first.
- C. Ask the contract owner first. Park the question until whoever owns the contract process says whether the agreement can ride in it unchanged. Implies: no assumption made. Costs: the whole plan waits on an answer from a person your request does not name.

User answer: A.

### Question 3 (fact, open)

The one-day count now stops when a client is "live". What exact event makes a new client count as live? Name it as something a person could observe.

User answer: I don't know.

Logged as `UNKNOWN`, not as a decision.

### Question 4 (fact, open)

I found nothing in the project folder, so I cannot look this up. Where does onboarding happen today: which code, tools, spreadsheets, tickets or records does it touch?

User answer: I don't know.

Logged as `UNKNOWN`, not as a decision.

### Question 5 (fact, open)

What does the two-week wait cost today, in whatever terms you track it?

User answer: I don't know.

Logged as `UNKNOWN`.

### Question 6 (fact, open)

Your request says to finish "this quarter". "This quarter" is a relative term and I have to write an absolute date. What is the exact last day you must be done by?

User answer: I don't know.

Logged as `UNKNOWN`. I did not fill in a date myself, because I cannot tell whether your quarter is a calendar or a fiscal one.

### Question 7 (fact, open)

How many hours a week does the one part-time engineer have for this?

User answer: I don't know.

Logged as `UNKNOWN`.

### Question 8 (judgment)

You want it done this quarter with one part-time engineer, and you want new clients live in one day after signing. If both cannot be met, which gives way?

Why I recommend A: a date can be met by cutting scope, but a one-day goal cannot be met by trying harder, and nobody yet knows how long the steps after signing take today.

- A. Hold the date (Recommended). At the date, ship the slice that removes the most elapsed time and report how far the result is from one day. Implies: a partial result on time. Costs: the one-day goal may not be met by the date.
- B. Hold the one-day goal. Keep working until it is reached and let the date move. Implies: the goal is met in the end. Costs: the slip cannot be sized while the engineer's hours and today's baseline are unknown.
- C. Hold both by adding capacity. Ask for more engineer time. Implies: both targets stay. Costs: it overrides your "only one engineer, part time" and needs someone to grant the time.

User answer: A.

### Question 9 (judgment)

Your request says "maybe add a self-serve portal too". Where does the portal go?

Why I recommend A: it is the largest add-on in the request, and the request itself only says "maybe".

- A. Out of scope (Recommended). The portal is a no-go for this work and is revisited only after the plan is signed off. Implies: the engineer's time stays on the one-day goal. Costs: no self-serve for clients in this work.
- B. Stretch goal. Build it only if the one-day slice finishes early. Implies: a chance of the portal. Costs: it invites scope creep on a capacity that is still unknown.
- C. In scope. The portal is part of the rebuild. Implies: one deliverable instead of two. Costs: a second large build for one part-time engineer, which puts the date at risk.

User answer: A.

### Question 10 (judgment)

Every plan rests on one assumption that sinks it if it is wrong. Which of these is the riskiest here, so we test it first?

Why I recommend A: everything else rests on the time after signing being close to one day, nobody knows today's figure, and the test costs a read, not a build.

- A. Steps fit in a day (Recommended). The assumption: once the agreement is signed, every remaining onboarding step can be done within one day. Cheapest test: read-only, time each step from signature to live in the records of recently completed onboardings. Costs: it needs access to those records, whose location is unknown, and it only yields a baseline.
- B. Legal accepts a separate gate. The assumption: legal accepts the agreement as a gate outside the contract process. Cheapest test: ask legal one yes or no question. Costs: it depends on an answer from legal, and nobody knows how long that takes.
- C. Capacity is enough. The assumption: one part-time engineer can finish this work. Cheapest test: get the engineer's weekly hours and compare them with the plan's slices. Costs: the hours are unknown and the comparison needs the plan first.

User answer: A.

Decision 1 moved the clock's start, so the baseline from signature to live is now a gap of its own. It is logged as `UNKNOWN`; the test in option A is what fills it.

## Branches closed without a question

- No-gos, rabbit holes and failure cases come from your request and decisions 1, 2 and 4.
- Appetite: the date and the engineer's hours are `UNKNOWN`; decision 3 says what gives way.
- The outcome metric is time from signing to live, target one day (decision 1); its end event is `UNKNOWN`.

No branch is open. I stop here and summarize.

## Summary to confirm

Decisions:
1. The one-day count starts when the client signs the data agreement and stops when they are live. The signing time (about 10 days today) is outside this rebuild.
2. The data agreement is a separate gate that must be complete before onboarding starts. The contract process is not changed.
3. If the date and the one-day goal conflict, the date holds: ship the slice that removes the most elapsed time and report the gap to one day.
4. The self-serve portal is out of scope; it is revisited after the plan is signed off.
5. Riskiest assumption: the steps after signing fit in one day. Cheapest test: read-only timing of each step from signature to live in recently completed onboardings.

From your request: do not change the contract process; do not onboard a client before the agreement is signed.

ASSUMED lines: none. I filled in nothing myself.

UNKNOWN lines (6):
- the exact event that makes a client "live"
- where onboarding happens today (code, tools, spreadsheets, tickets, records)
- what the two-week wait costs today
- the last day of "this quarter" as an absolute date
- how many hours a week the engineer has
- today's elapsed time from signature to live

The log is at `docs/discovery/customer-onboarding-rebuild.md`. Do you confirm these decisions and the UNKNOWN list? Type yes to confirm; a yes here only confirms the log, it is not a go-ahead to build, commit or publish anything.

User answer: Yes, confirmed.

/grill ends here.

---

# Part 2: /prompt

Input: the request above and the decision log `docs/discovery/customer-onboarding-rebuild.md`.

## Step 1: look before asking

I read what the project says: the project root is empty. There is no README, CLAUDE.md, test command or plan in `docs/` beyond the decision log. The log is my only source. Where the work lives is already logged there as an `UNKNOWN`, so I do not ask it again.

## Step 2: interview for gaps

The outcome, the done-when checks and the risk are unclear because the log holds 6 UNKNOWN lines. Two questions follow.

### Prompt question 1 (judgment)

The log leaves 6 UNKNOWN lines, among them what "live" means, where onboarding lives, the last day of the quarter and the engineer's hours. A prompt to build the rebuild would need checks that rest on those. What should this prompt ask the agent to deliver?

Why I recommend A: every check in a build prompt would rest on a gap that is still open, while a plan can be checked against what is known.

- A. A signed-off plan first (Recommended). The agent researches, writes a plan of slices that each carry a test and a rollback, gets a fresh review and then your sign-off. The build is a separate prompt written afterwards. Implies: this prompt changes nothing in onboarding. Costs: one more round before any build starts.
- B. The whole rebuild. Discovery, plan and build in one prompt. Implies: a single prompt. Costs: its checks would rest on the open gaps, and it would stop at its first step.

User answer: A.

### Prompt question 2 (judgment)

The project folder is empty, so a STOP AND ASK line such as "no onboarding code found" would already hold when the prompt starts. If the session that runs the prompt finds no onboarding code or records in its project, what should it do?

Why I recommend A: the folder was empty when the prompt was written, and you can answer what you know, so stopping would deliver nothing.

- A. Interview you (Recommended). It asks you, one question per message, to name each onboarding step, its system and how long it takes, and tags every such fact `reported`, not verified. Implies: the plan can still be written. Costs: the plan rests on your memory instead of records, and some steps may be missed.
- B. Stop and wait. It stops and asks you to point it at the code or records. Implies: every figure in the plan comes from a record. Costs: with an empty project this stops at the first step and delivers nothing.

User answer: A.

## Steps 3 to 8

Step 3, size: high risk (client data, a legal agreement and a process that must not change). The prompt gets a research step, a plan of slices each with a test and a rollback, a fresh critic on the plan and human sign-off.

Step 4, who does what: one writer, the lead, writes the plan file. One read-only helper may sweep the project for steps and recorded times; a fresh reviewer checks the plan. Tests come first for every slice. Writers are not needed, because the prompt writes no code, so no batches or merge order apply.

Step 5, draft: written to `prompt-r0.md`. The decision log is passed by path.

Step 6, helper brief: one helper, so no comparison and no second brief. The lead's synthesis is its own numbered step.

Step 7: not a loop or a schedule, so Template H does not apply.

Step 8, consistency pass:
- Files: the prompt creates `docs/plans/onboarding-rebuild.md` and `<scratch>/helper-steps.md`. CONSTRAINTS allows both and DONE WHEN reads the plan. The reviewer's findings go into the plan's Review section, not a third file.
- Helpers: one helper and one fresh reviewer; BUDGET allows both.
- Time and cost: no per-item runs, so nothing multiplies. The ceiling is one session.
- Transformations: client names and data are left out of every file; DONE WHEN check 1 says so.
- Skips: a fallback path with no records tags figures `reported`; DONE WHEN does not require every row to be `records`.
- Targets: no CI, deploy or PR. No test or tooling is changed, so no deliberate-break check applies.
- Evidence: each `records` row quotes its wording beside the figure.
- Caps: the helper's return has four fields and the cap leaves room for all of them.
- Contradictions: the plan file is the only repository write; the "STOP AND ASK" lines are tested below against an empty project.
- STOP AND ASK tested against what is known now: "no onboarding code found" is not a stop line, because prompt question 2 turned it into the interview path. The other lines depend on facts the session discovers, so none holds now.

Draft written to `prompt-r0.md`. Step 10 calls for a fresh review (a decision log is behind it and the risk is high), which the lead runs.

## Round 1 fixes (check output and review-r1.md)

No new question to the user was needed, and the decision log is unchanged: both blockers are fixed inside the draft by decisions the user already made (prompt question 2 chose the interview path).

- Blocker 1 (the interview path leaves the riskiest assumption untested, yet check 2 could pass with an untraced figure, and the GOAL did not say what that path delivers): the GOAL now says that where no records exist, the plan delivers the same with every time marked `reported` and the riskiest assumption marked `untested`. Check 2 now needs a source tag on the elapsed time now and a `tested` or `untested` mark, and fails while the elapsed-time UNKNOWN is open. Check 3 also fails while that UNKNOWN is open. Step 2 defines `tested` (the records give each completed onboarding's signature date and its times) and `untested` (no records, or no signature date).
- Blocker 2 (check 5 and step 7 asked the reviewer to judge sections that do not exist when it runs): the reviewer now judges the sections from "Inputs" to "Open questions". Check 5 asks for a verdict on those sections only.
- c-6 WARNs: the number words in the header, in CONSTRAINTS and in HOW TO WORK step 3 are reworded, so the prompt carries no unsourced figure.
- c-8 WARN: checks 2 and 3 overlapped the elapsed-time UNKNOWN without failing while it is open. Both now do.
- Not changed: the reviewer's non-blocker notes (the round cap against the reviewer cap, and the contract-process steps being asked at run time).

Written to `prompt-r1.md`.

