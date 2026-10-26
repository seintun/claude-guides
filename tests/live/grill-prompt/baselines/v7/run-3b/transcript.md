# Run 3b transcript: /grill then /prompt on Dump 3

Date: 2026-10-24. Project root: `project/` (empty, no repository).

## /grill

Request (Dump 3):

> Rebuild our customer onboarding so new clients are live in one day instead of two weeks. Must not change the contract process. Also legal wants every client to sign the new data agreement before onboarding, which currently takes about 10 days. We want it done this quarter, but there's only one engineer, part time. And maybe add a self-serve portal too.

GRILL (look first): I searched the project root for a README, CLAUDE.md, docs/, code, config and any earlier discovery notes. The folder is empty, so nothing in it answers a question about your onboarding. From your request I already have these, so I won't ask for them:
- Goal: new clients live in one day instead of two weeks.
- No-go: the contract process does not change.
- Legal's rule: every client signs the new data agreement before onboarding; that signing takes about 10 days today.
- Failure case: a client going live without a signed data agreement.
- Deadline: "this quarter". Staffing: one engineer, part time. Portal: a "maybe".
I will log each decision in `docs/discovery/customer-onboarding-rebuild.md` as we go.

### Question 1 (judgment)

GRILL: When does the one-day clock start?

Your request says new clients should be live in one day, and that every client signs the new data agreement before onboarding, which takes about 10 days. Those two only fit together if the clock starts after the signing. I recommend A: the signing is legal's and the client's step, and one part-time engineer can't remove it, so a goal that counted it couldn't be met by this project.

- A. The clock starts when the signed data agreement arrives (Recommended). Implies: "live in one day" covers everything after signing. Costs: the 10 days of signing stay outside this goal, so a client's total wait from first contact will still be longer than one day.
- B. The clock starts at first contact with the client. Implies: the 10 days of signing count toward the one day. Costs: the goal can't be met unless the signing itself gets far faster, which this project can't deliver.
- C. Clients go live first and sign the data agreement afterwards. Implies: one day is reachable from first contact. Costs: breaks legal's rule that every client signs before onboarding.

USER: A. (The request says legal wants the signing done before onboarding, so the one day can only run after it.)

### Question 2 (fact, asked open)

GRILL: Today's onboarding takes two weeks. Does that two weeks already include the roughly 10 days that signing takes, or does signing come on top of it?

(No options: this is a fact only you can give, and I won't guess it for you. Nothing in the project can answer it.)

USER: I don't know.

GRILL: Logged as UNKNOWN. A timing walk through a real onboarding can answer it later.

### Question 3 (fact, asked open)

GRILL: What event marks a client as "live", the last step of onboarding?

(No options: the answer is a name for your own process, and any option I wrote would be my guess.)

USER: I don't know.

GRILL: Logged as UNKNOWN. The one-day goal has no finish line until this is filled in.

### Question 4 (judgment)

GRILL: How does the new data agreement sit next to the contract process, which must not change?

Your request says the contract process must not change, and also that legal wants every client to sign the new data agreement. I recommend A because it is the only reading that keeps both statements true without asking anyone to change the contract process.

- A. The data agreement is its own step before onboarding, outside the contract process (Recommended). Implies: the contract process is untouched, and the agreement has its own signature and its own record that onboarding checks before a client goes live. Costs: clients sign two documents, and the two records must be linked.
- B. The data agreement becomes part of the contract process. Implies: one signing flow for the client. Costs: it changes the contract process, which you ruled out, and needs the owner of that process to agree.

USER: A. (The request says the contract process must not change.)

### Question 5 (fact, asked open)

GRILL: How many hours a week does the engineer have for this work?

(No options: it is a number, and I won't offer one you didn't give me.)

USER: I don't know.

GRILL: Logged as UNKNOWN.

### Question 6 (fact, asked open)

GRILL: Today is 2026-10-24, and "this quarter" could mean a calendar quarter or one of your fiscal quarters. What date does it end for you?

(No options: it is a date, and I won't offer one you didn't give me.)

USER: I don't know.

GRILL: Logged as UNKNOWN. I will not write a date in for you.

### Question 7 (judgment)

GRILL: With one part-time engineer and a deadline at the end of this quarter, how should the rebuild be scoped?

The hours and the end date are unknown, but "one engineer, part time" is a hard limit in your request. I recommend A because slices leave you something usable if time runs out, while a full rebuild can't be shown to fit.

- A. Ship in slices, the slowest removable steps first, and stop when the time runs out (Recommended). Implies: "rebuild" becomes "remove the biggest delays first", and the one-day goal is the target the slices are measured against. Costs: some steps may stay manual, and the one-day goal may not be fully met by the deadline.
- B. Rebuild everything, with one day as a hard requirement. Implies: the whole onboarding is redone. Costs: unlikely to fit one part-time engineer in this quarter, and an unfinished rebuild leaves nothing usable.
- C. Keep the full scope and move the deadline. Implies: the whole onboarding is redone with more time. Costs: you said you want it done this quarter, and moving the deadline needs whoever owns it to agree.

USER: A. (The request wants it done this quarter with one part-time engineer, so B and C do not fit, and nothing in it clearly asks for the full rebuild.)

### Question 8 (judgment)

GRILL: Is the self-serve portal part of this work?

You wrote "maybe", and the last answer cut the scope to fit one part-time engineer. I recommend A because a portal is a second project, and starting it would take time from the steps that decide whether one day is reachable.

- A. Out of scope this quarter; list it as a follow-up (Recommended). Implies: no portal work, and the prompt names it as a no-go. Costs: clients still depend on staff to onboard them until a later project.
- B. A stretch goal, started only after every slice in the plan is done and time remains. Implies: portal work can begin late in the quarter. Costs: a half-built portal may be left behind, and it still draws attention from the slices.
- C. In scope as part of the rebuild. Implies: the portal is planned and built with the slices. Costs: it adds a large piece of work for one part-time engineer and conflicts with the scoping you just chose.

USER: A. (The request says only "maybe", and one part-time engineer is a hard limit.)

### Question 9 (fact, asked open)

GRILL: Where does today's onboarding live: which repository, tools, data stores and records does this work read or change? (I looked in the project folder first; it is empty, so I can't find it myself.)

(No options: it is a location only you can name.)

USER: I don't know.

GRILL: Logged as UNKNOWN.

### Question 10 (judgment)

GRILL: Which assumption should we test first, because it would sink the most if wrong?

I recommend A. If most of today's wait after signing is people waiting on people, nothing the engineer builds can reach one day, and the test costs only a read of a past onboarding's records. B can't be tested until the engineer's hours are known.

- A. "Most of the wait after signing is manual or waiting work that software can remove." (Recommended) Cheapest test: record every step of a recent completed onboarding with its start, end and what it waited on, and see where the days go. Costs: needs access to a past onboarding's records, whose location is unknown, and the test also answers the open question from Question 2 (whether signing is inside today's two weeks).
- B. "One part-time engineer can build enough of it in the time there is." Cheapest test: size the first slice and compare it with the hours available. Costs: the hours and the end date are unknown, so the test can't run yet.

USER: A. (Recommended option; the request doesn't clearly imply the other.)

### Question 11 (fact, asked open)

GRILL: What does the two-week wait cost you or your clients today?

(No options: any cost I wrote would be a figure you didn't give me.)

USER: I don't know.

GRILL: Logged as UNKNOWN. No question is left that the request or an earlier answer leaves open, and you set no question cap, so I stop here.

### Confirmation summary

GRILL: Here is what the log in `docs/discovery/customer-onboarding-rebuild.md` now holds. Please confirm it.

Decisions:
1. The one-day clock starts when the signed data agreement arrives; the roughly 10 days of signing stay outside the goal.
2. The data agreement is its own step before onboarding, outside the contract process, which stays untouched. No client goes live without a recorded signed agreement.
3. The rebuild ships in slices, the slowest removable steps first, and stops when the time runs out.
4. The self-serve portal is out of scope this quarter and listed as a follow-up.
5. The riskiest assumption is that most of the wait after signing is work software can remove; the cheapest test is a timing walk through a recent completed onboarding.

ASSUMED: none.

UNKNOWN (six, one gap each):
1. Whether today's two weeks already includes the roughly 10 days of signing.
2. Which event marks a client as "live".
3. How many hours a week the engineer has.
4. The end date of "this quarter", and whether it is calendar or fiscal.
5. Where today's onboarding lives (repository, tools, data stores, records).
6. What the two-week wait costs today.

Six UNKNOWN lines is more than a prompt can carry and still be ready to run, so the next step will say so.

(No go-ahead to build, commit or publish is being asked for here. This only confirms what was logged.)

USER: Confirmed.

/grill ends here.

## /prompt

Input: the request (Dump 3) and the decision log `project/docs/discovery/customer-onboarding-rebuild.md`.

PROMPT (step 1, look first): The project folder is empty, so there is no README, CLAUDE.md, test command or existing plan to read. The decision log is the only source. Where the work lives is the UNKNOWN the grill already logged; I will carry it, not re-ask it.

PROMPT (step 2, interview): No questions asked. The gaps in the outcome (what "live" means), the checks and the risk are all already in the log as UNKNOWN lines that the user was asked and could not answer; asking them again would only repeat "I don't know". The risk is clear from the log: legal's go-live gate, client data, and one part-time engineer.

PROMPT (step 3, size): High risk and several slices, so: a research step (the timing walk, the test of the riskiest assumption), a plan file of slices with a test and a rollback each, a fresh critic on the plan, and human sign-off before any build.

PROMPT (step 4, who does what): one writer (the lead); helpers only read, one for the timing walk and one fresh critic for the plan; tests first and immutable to the builder. It is not a large mechanical change, so no batch pipeline.

PROMPT (steps 5 to 8): draft and consistency pass done; the draft is at `prompt-r0.md`. Six UNKNOWN lines is more than 3, so the draft says at its top that it is not ready to run. Step 10 calls for a review (several slices, high risk, a decision log behind it), which the lead runs.

### Round 1 fixes: two new /prompt questions

The round-1 reviewer found that the signed-agreement record and the contract-process files are neither located nor listed as UNKNOWN, and that the gate and the one-day clock depend on both. The project folder holds nothing to read, so /prompt step 1 says to ask or log an UNKNOWN. I ask, one thing per message, open because each is a fact.

PROMPT (question 1, fact, asked open): Where is the signed data agreement recorded, if it is recorded at all?

(No options: it is a location only you can name. The go-live gate and the one-day clock both depend on it.)

USER: I don't know.

PROMPT: Logged as UNKNOWN.

PROMPT (question 2, fact, asked open): Which files, data and records make up the contract process?

(No options: it is a list only you can give. The run must be able to prove it did not change them.)

USER: I don't know.

PROMPT: Logged as UNKNOWN. No more questions: the request and the log answer the rest, and the cap is 5.

Other round-1 changes, no user input needed: the retry cap is now per slice and a failure repeating across slices is the stop (blocker 1); the go-live gate is a required first slice that is never cut or skipped (blocker 2); check 2 starts the clock at arrival of the signed agreement, not its recording, and the timing walk records both (blocker 3). Not changed, because the reviewer did not name them as blockers and the coordinator said to change nothing else: the zero-case guards on checks 4 and 5 (the REPORT's "zero is a FAIL" stays the guard) and the break file in check 3 being named by the plan.


