# Review r2 of prompt-r1.md

Read: the revised draft, the decision log, the skill, review-r1.md. Nothing else.

## First review's blockers

1. The only runnable path leaves the riskiest assumption untested, yet the checks treat it as settled: CLOSED.
   - GOAL now says what the fallback delivers: "where no records exist, the plan delivers the same with every time marked `reported` and the riskiest assumption marked `untested`, and says so."
   - Check 2 now requires the source tag and the mark, and fails without them: "This check fails while the "live" UNKNOWN is open, and while the elapsed-time UNKNOWN is open, that is, while "Gap" has no elapsed time now with a source tag or no `tested` or `untested` mark."
   - Step 2 defines both outcomes: "Mark it `tested` when the records give each completed onboarding's signature date and its times. Where there are no records, or the records show no signature date, mark it `untested` in "Gap" and tag the times `reported`."
   - The header no longer says the test is settled by the work alone: "The work itself settles some of them: where onboarding happens (HOW TO WORK step 1) and the current elapsed time from signature to live (step 2, from records, or as the figure the user reports)."
2. Check 5 and step 7 ask the reviewer for a verdict on sections that do not exist yet: CLOSED.
   - Check 5: ""Review" holds a PASS or FAIL with one line of evidence, from a fresh reviewer, for every section from "Inputs" to "Open questions"".
   - Step 7: "Ask for PASS or FAIL on each section from "Inputs" to "Open questions", with one line of evidence (it does not judge "Review" or "Sign-off", which are empty at that point)".
   - Step 5 lists the sections in the same order, so the range is the seven sections that exist when the reviewer runs.

## Three questions on the revised draft

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   - Zero cases: no. Check 1: "then it has at least one row". Check 3: "then there is at least one slice". Check 4: ""Not touched" has at least one entry".
   - Fallback path: no. The fallback is the GOAL's own second clause (quoted above), and check 2 passes on it only with a source tag and a `tested` or `untested` mark in "Gap". A run on the interview path therefore meets the GOAL as the GOAL is written.
2. Does any STOP AND ASK condition already hold?
   - No. The log records no answer on the contract process's steps, no contradiction and no build request, so ""The user cannot name any step or system of the contract process, so "Not touched" would be empty."" is open, and step 4 asks the question. ""No slice can be written that removes elapsed time from a step after the signature."" cannot be judged while the log says "today's baseline is unknown". ""A fresh reviewer cannot be started."" has no evidence either way.
3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   - Located: the plan ("`docs/plans/onboarding-rebuild.md`"), the log ("`docs/discovery/customer-onboarding-rebuild.md`"), the working notes ("`<scratch>`").
   - Listed: "UNKNOWN: where onboarding happens (the code, tools, spreadsheets, tickets and records it touches); the project folder this prompt was written from was empty."
   - The signature-date record is not located, but step 2 handles its absence with the `untested` path ("or the records show no signature date"). The contract process's steps and systems are not an UNKNOWN line, but step 4 asks for them and the STOP line covers an empty answer. Neither is counted as a blocker.

## Open or new blockers

1. DONE WHEN 5 demands sign-off content that no step collects.
   - Evidence: check 5 says ""Sign-off" quotes the user's typed yes, its date, and the user's confirmation that no step is missing from "Current steps"." Step 8 says "Show the user the plan's path and its "Gap" section, and ask for sign-off in chat. Write their typed yes and its date in "Sign-off"." Step 8 shows only "Gap", never asks the confirmation, and writes only the yes and its date. The only "no more steps" prompt is in step 1 ("until the user says there are no more steps"), which runs on the interview path only and writes to `<scratch>/interview-notes.md`, not to "Sign-off".
   - Why it blocks: a run that follows the steps leaves "Sign-off" without the confirmation on either path, so check 5 fails on a correct run, or the agent has to invent a step the prompt does not give it. The check cannot be met from the state the steps leave.

Reviewer cap note, not counted: "at most 1 read-only helper and 1 fresh reviewer" against "at most 2 review rounds" leaves the second round's reviewer unstated. Step 7 says "A re-review reads the changed passages" without saying who runs it. The first review judged this not a blocker, and nothing in the draft makes it fail.
