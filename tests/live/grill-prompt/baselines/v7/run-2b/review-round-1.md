# Review r1 of prompt-r0.md (CI move memo)

Read: the draft, the decision log, the skill. Nothing else.

## Part verdicts

- GOAL: PASS. One sentence of outcome, and it says what the fallback delivers: "otherwise it is Wait, naming each figure that would settle it."
- DONE WHEN: FAIL. See blockers 2 and 3. Evidence: "there is one GAP line for each of these the user did not supply" and "the memo cites at least one price for each of the two vendors".
- CONTEXT: PASS. Problem, riskiest assumption and cheapest test are present, and the log is a path: "`docs/discovery/ci-buildkite-writeup.md`, decisions 1 to 8; read it first." The log has exactly 8 decisions. Note, not a blocker: the cheapest test is "price the last full billing period ... before any other analysis", but HOW TO WORK step 2 sends the inventory helper "in parallel" with the pricing helpers, and the pricing of usage happens in step 3.
- CONSTRAINTS: FAIL. The line "Show no dollar or usage figure for the team's own CI unless the user supplied it. Do not estimate a missing input." cannot be reconciled with a Move or Stay call that needs a net saving (blocker 1).
- BUDGET: PASS. "Helpers: at most the helper cap. Reviewer runs: at most two, one review and one re-review of the changed passages." The steps need 2 pricing helpers and 1 inventory helper against "ASSUMED: at most 3 helpers", and at most 2 reviewer runs.
- STOP AND ASK IF: PASS. None of its three conditions holds now (see question 2).
- HOW TO WORK: FAIL. Step 4 says "What could not be verified (every GAP with the figure that would settle it)", which collides with the GAP-count check (blocker 2). The synthesis is its own step 3, the briefs are same-brief and same-fields, and the review is bounded ("after two rounds the user decides"). Those parts pass.
- REPORT: PASS. "Each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS."

## The three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   Yes, on the Wait path. The GOAL says the memo gives "the cost lines and the migration effort laid out". The only check on cost content is "the memo cites at least one price for each of the two vendors". A memo with a first-line Wait, one cited price per vendor, the four GAP lines and a Migration work section holding a GAP line passes all five checks. It has no cost lines, no tiers, no metered items and no compute line. Check 5's second branch ("the section holds a GAP line and the list of those four things to count, and gives no range") is a legitimate fallback, but nothing checks that the Cost lines section exists. Checks 4 and 5 start with "Given the user's reply at step 1" and "Given the CI configuration was supplied". If step 1 is skipped there is no reply to be given, so the conditions are vacuous.

2. Does any STOP AND ASK condition already hold?
   No. "Two supplied figures contradict each other, or a supplied figure cannot be matched to the unit a vendor prices in": nothing is supplied yet, and the log says "the user did not know" for the bill and the configuration. "Two helpers fail for the same cause": no helper has run. "The user asks, during the run, for something CONSTRAINTS forbids": no such request has been made.

3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   Mostly. The monorepo, CI configuration and run history are covered by "UNKNOWN: location of the monorepo, its CI configuration and its run history (the project folder is empty)". The bill is covered by "UNKNOWN: where the GitHub Actions bill and usage figures can be read". The plan by "UNKNOWN: which GitHub plan the team is on". The memo path is `docs/ci-migration-memo.md` and `<scratch>` is a placeholder. One input is missing. CONSTRAINTS requires "every metered item the pages list for the plan in question, such as per-user, per-minute or per-agent charges". Step 1 asks only for "the monorepo's CI configuration ... and recent build times", "the last full billing period's GitHub Actions bill and usage", "the GitHub plan", and "the deadline's calendar date". The seat count and agent or concurrency count that Buildkite's per-user and per-agent items need are neither asked for nor listed as UNKNOWN. Also unnamed: "the manager who asked for it" (the log does not name her either).

## Blockers

1. The Move or Stay path has no permitted figure and no complete input to rest on.
   - Evidence: GOAL, "the call is Move or Stay only when the cost lines and the effort range both rest on data the user supplied". CONSTRAINTS and check 4, "no dollar or usage figure about the team's own CI appears in the memo except one the user supplied, quoted beside where it came from". Decision 6 of the log needs "the net monthly saving".
   - Why it blocks: a Buildkite charge for the team's usage, and the net saving, are computed dollar figures the user did not supply. Check 4 as written fails the very Move or Stay memo that DONE WHEN 2 allows ("a Move or Stay rests on the supplied bill and the supplied CI configuration"). Separately, step 1 does not ask for the seat and agent counts that the per-user and per-agent items in CONSTRAINTS need, so even a user who supplies the bill and configuration cannot make a Buildkite cost line complete.

2. The GAP-count check can fail a correct memo.
   - Evidence: check 4, "there is one GAP line for each of these the user did not supply" run as `grep -n 'GAP:'`. Check 5, "the section holds a GAP line" (in Migration work). Step 4, "What could not be verified (every GAP with the figure that would settle it)". CONSTRAINTS, "mark which one applies as a GAP" (Cost lines). Step 1, "Each missing item becomes a line starting `GAP:` in the memo."
   - Why it blocks: the same missing item is required to appear as a GAP line in its own section and again in the closing section, so the grep returns two or more lines per item. The prompt never says whether the closing section repeats the `GAP:` prefix. A reader who follows step 4 literally fails check 4, and one who follows check 4 literally drops the closing list. Check 4 also lists "the CI configuration and run history" and "the build times" as separate items although run history carries the build times, so a user who supplies the configuration but not the run history leaves the count undefined.

3. No check covers the cost lines, so the memo can meet every check without meeting the GOAL.
   - Evidence: GOAL, "with the cost lines and the migration effort laid out". CONSTRAINTS, "Keep the vendor charges, the build compute and the migration effort in engineer-weeks as separate lines" and "include every metered item the pages list". Check 3, "the memo cites at least one price for each of the two vendors".
   - Why it blocks: one cited price per vendor satisfies check 3, and checks 1, 2, 4 and 5 are satisfied by a Wait memo with GAP lines. Nothing observes that the Cost lines section holds the separate lines, the published tiers or every metered item. The skill asks "could this pass while the goal is unmet?", and here it can.

## Notes (not blockers)

- "at most 40 words per field" (both briefs) and "Two helpers fail for the same cause" are chosen values that are not in the `ASSUMED` list at the top; the skill says a word limit and a retry count belong there.
- "Sources: at most the source cap of pages read per vendor" does not say whether the lead's re-opening of quoted pages in step 3 counts against the cap.
- Step 5 and the cheapest test in CONTEXT are consistent with the two-round review cap.
