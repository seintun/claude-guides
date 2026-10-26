# Review r2 of prompt-r1.md

Files read: the revised draft, the decision log, the skill, the first review. Nothing else.

## Round 1 blockers

1. The checks are not rerun on the final write-up: CLOSED.
   - Step 4: "Run every DONE WHEN check except the review check yourself. Fix and rerun until they hold."
   - Step 7: "Run every DONE WHEN check again on the write-up as it now stands, the review check included, then write the report. An edit made after the last review round that no round named goes back for review while a round remains; otherwise the report lists it as unreviewed."
   - Step 7 now reruns all five checks after the step 6 edits, so the report reads the state the steps leave.

2. Check 2 demanded a migration effort range the log says not to invent, and dropped the confidence level: CLOSED.
   - Check 2: "the migration effort (a range with a stated confidence level, or `MISSING INPUT: <what>` where there is no basis for one)".
   - CONSTRAINTS: "Where there is no basis for a range (no workflow files), the effort cell is `MISSING INPUT: workflow files`, not a guess."
   - This matches the log: "Without the files, the range is marked as missing input, not invented."

3. The reviewer brief could not be followed with what the reviewer is given: CLOSED.
   - Brief, Where to look: "the write-up file, and only the pages its source labels cite, at most 12 distinct pages. In a re-review you are also given the path of your previous review file and of the fix file; read only the changed passages in the fix file and the pages their labels cite."
   - Brief, Return: "Keep every field to about 40 words at most."
   - Step 5: "A re-review also gets the path of the reviewer's own previous review file and of the fix file `<scratch>/ci-move-fix-<n>.md`". Both caps and the re-review inputs are now inside the brief or named with it.

## The three questions on the revised draft

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   - Check 3 can still print nothing for a write-up whose every cell reads `MISSING INPUT`: "`awk '/^## /{s=1} s && /[0-9]/ && !/\[(source S[0-9]+|supplied|estimate)/' <scratch>/ci-move-writeup.md` prints nothing".
   - That skeleton cannot pass the whole set. Check 4: "at least one cited URL is on github.com or a subdomain of it and at least one is on buildkite.com, so a write-up with no vendor sources fails."
   - The `UNDECIDED UNTIL` fallback does not skip the GOAL. GOAL: "or, where an input is still missing, the exact condition under which each answer wins." Check 2: "The lines after it give the cost comparison (as a formula when an input is missing)".
   - The review path cannot pass silently. Step 7: "If you cannot start a fresh reviewer, write "Review: not run" at the top of the write-up ... and report the review check as NOT RUN."

2. Does any STOP AND ASK condition already hold?
   - No. The log says "The folder is empty. Nothing to read", and the draft says "Workflow files and usage report: not located (see the UNKNOWN lines)", so no input file exists to hold a credential.
   - "A step would need an account, a trial, a vendor contact or a payment" does not hold. Step 1: "A missing input is carried into the write-up, not chased." CONSTRAINTS: "No trial or account sign-up, no vendor contact, no spending".
   - Neither the draft nor the log says the vendor pages cannot be opened. No check has failed, no two pages have disagreed, and no review round has run to leave an open blocker.

3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   - Yes. Located: "Decision log: `docs/discovery/ci-buildkite-writeup.md`".
   - Listed as UNKNOWN: "UNKNOWN: where the monorepo and its GitHub Actions workflow files live." / "UNKNOWN: which report or account shows the monthly CI cost and usage." / "UNKNOWN: the actual monthly CI spend." / "UNKNOWN: the typical monorepo build duration today."
   - The number of users and the build machine type are not their own UNKNOWN lines. Check 5 forces them into Open items: "every other input a table row needed and lacked (for example the number of users or the build machine type)". The first review also left them out of its blockers.

## Open or new blockers

none

## Considered, not counted

- Check 4 reads review-1 for a row on every listed id: "`grep -E '^\| S[0-9]+ ' <scratch>/ci-move-review-1.md` shows a MATCH or MISMATCH row for every listed id". A fix that cites a new page under a new id has no review-1 row. Step 6 does not require a new id ("correct the claim, relabel it as an estimate, or remove it"), and a false FAIL would be reported, so it does not block.
- CONTEXT and step 3 say "the last full month" of usage, a relative term. No check rests on it and the usage report is UNKNOWN, so it blocks nothing.
