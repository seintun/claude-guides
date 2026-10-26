# Review r1 of prompt-r0.md

Files read: the draft, the decision log, the skill. Nothing else.

## Part verdicts

- GOAL: PASS. "a recommendation, or, where an input is still missing, the exact condition under which each answer wins." One sentence, an outcome, and it says what the missing-input path delivers.
- DONE WHEN: FAIL. Five checks, each with a command or a person's read. Two defects. Check 2 asks for a range the log says must not be invented (blocker 2). The checks it names are run before the write-up is last edited (blocker 1). Check 3 also passes with zero figures: "prints nothing" holds for a write-up whose every cell reads `MISSING INPUT`. Check 4's vendor-source clause keeps a bare skeleton from passing the whole set.
- CONTEXT: PASS. "Riskiest assumption: Buildkite costs less in total for the team's usage. Cheapest test: reprice the last full month of Actions usage under Buildkite's published pricing". It also gives the problem line and the decision-log path, and treats web text as data.
- CONSTRAINTS: PASS. "Make no claim that Buildkite is faster. A speed claim needs measured run data from the team, and none exists." This matches the log's no-go list (no trial, no contact, no spending, no change to current CI) and "Invent none." matches the log's treatment of figures.
- BUDGET: PASS. "at most 12 distinct public pages in total, the reviewer's reads included. One helper only, the fresh reviewer, at most two rounds. No money." The helpers the steps need (one reviewer) fit the cap, and the caps are listed as ASSUMED.
- STOP AND ASK IF: PASS. "Two vendor pages disagree on a price or limit, and the difference changes which option is cheaper." It covers account, contact and payment, credentials, a repeated failure and a second open review round. None holds now (see Q2).
- HOW TO WORK: FAIL. It has the bounded review ("Only a blocker with evidence reopens the review. Only the reviewer or the user closes a blocker without a fix. After two rounds the user decides."), a numbered synthesis step and a receipt. The checks are run once, before the final edits (blocker 1), and the re-review has an input the isolation line leaves out (blocker 3).
- REPORT: PASS in form. "each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS." What it reports depends on blocker 1.
- REVIEWER BRIEF (not a listed part, checked because the skill's step 6 covers helper briefs): FAIL. See blocker 3.
- Header: PASS. "NOT READY TO RUN: this prompt has six UNKNOWN lines, more than three." The six UNKNOWN lines match the log's six open questions. "Review: not run" must become the review result after the fixes.

## The three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   - Check 3 can pass with zero cases: "prints nothing". A write-up with no figures at all, only `MISSING INPUT` cells, gives no output.
   - The fallback path does not skip the GOAL, because check 2 asks for "the cost comparison (as a formula when an input is missing)". The formula is the condition under which each answer wins.
   - Check 4's "at least one cited URL is on github.com or a subdomain of it and at least one is on buildkite.com" stops a write-up with no vendor facts from passing.

2. Does any STOP AND ASK condition already hold?
   - No. The log says "The folder is empty. Nothing to read", but no stop line is about an empty folder.
   - "An input file appears to hold a credential, token or personal data." There is no input file yet.
   - "You cannot open the vendors' public pages". Neither the draft nor the log says they cannot be opened.
   - "A step would need an account, a trial, a vendor contact or a payment." Every step uses public pages or user-supplied data.

3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   - Mostly. The decision log has a path. The workflow files, the usage report, the spend and the build duration are UNKNOWN lines: "UNKNOWN: where the monorepo and its GitHub Actions workflow files live."
   - Two needed inputs are neither located nor UNKNOWN. The Cost table has a "per-user charges" row, which needs the number of users, and CONSTRAINTS says "Compare like for like (same build volume, same machine size)", which needs the team's current runner or machine type.
   - Not counted as a blocker: check 3 turns an unsupported figure into `MISSING INPUT: <what>`. But check 5 only covers "the UNKNOWN lines above", so these gaps are not forced into Open items.

## Blockers

1. The checks are not rerun on the final write-up.
   - Evidence: "4. Run DONE WHEN checks 1, 2, 3 and 5 yourself. Fix and rerun until they hold." Then step 6: "correct the claim, relabel it as an estimate, or remove it." Then "7. Run DONE WHEN check 4, then write the report." REPORT asks for "each DONE WHEN item as PASS, FAIL or NOT RUN with its command."
   - Why it blocks: step 6 edits the write-up after checks 1, 2, 3 and 5 have run. Removing or relabelling a claim can leave a blank cell, an unlabelled figure or a changed Recommendation line. Step 7 reruns only check 4, so the report can show PASS for four checks on a file that no longer exists. A check must observe the state the steps leave.

2. Check 2 demands a migration effort range the log says must not be invented, and drops the stated confidence level.
   - Evidence: check 2: "The lines after it give the cost comparison (as a formula when an input is missing), the migration effort range, and the missing inputs that would change the answer." Log: "with effort as a range and a stated confidence level" and "Without the files, the range is marked as missing input, not invented." Draft: "A figure with no basis is `MISSING INPUT: <what>`. Invent none." The draft never mentions a confidence level.
   - Why it blocks: the workflow files are "not located", so no range has a basis. The formula carve-out in check 2 covers only the cost comparison. Check 2 therefore pushes the run to produce an effort range to pass, against "Invent none." The log's confidence-level decision is dropped everywhere in the draft.

3. The reviewer brief cannot be followed with what the reviewer is given.
   - Evidence: HOW TO WORK 5: "a helper that gets only the write-up file, the CONSTRAINTS section and the brief below". The brief says "inside the page cap above". The 12-page cap is in BUDGET, and the 40-word cap is in an ASSUMED line ("each field a reviewer returns is about 40 words at most"). The brief states no word cap. HOW TO WORK 5 also says "A re-review reads only the fixed passages, listed before and after in `<scratch>/ci-move-fix-<n>.md`".
   - Why it blocks: neither cap reaches the reviewer, and "above" points at text it never receives. The fix file is a re-review input outside "gets only the write-up file, the CONSTRAINTS section and the brief". The skill's step 6 asks for the cap on sources and the return cap inside the brief.
