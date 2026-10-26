# Review r2 of prompt-r1.md (CI move memo)

Read: the revised draft, the decision log, the skill, review-r1.md. Nothing else.

## First-review blockers

1. Move or Stay path had no permitted figure and no complete input: CLOSED.
   - CONSTRAINTS now allows computed figures: "Show no dollar or usage figure for the team's own CI unless the user supplied it, or you computed it from supplied figures and cited prices and show its inputs and arithmetic beside it (for example a vendor's charge for the supplied usage, or the net monthly saving)."
   - DONE WHEN 4 carries the same exception: "or one computed from supplied figures and cited prices with its inputs and arithmetic shown beside it."
   - Step 1 now asks for the seat and agent inputs: "the usage behind it (for example minutes used, the number of people who use CI and the most builds that ran at once)". A matching line was added: "UNKNOWN: where the GitHub Actions bill and the usage behind it (for example minutes used, the number of people who use CI and the most builds that ran at once) can be read."

2. GAP-count check could fail a correct memo: CLOSED.
   - CONSTRAINTS now fixes where the prefix lives: "Every gap is one line starting `GAP:`, in the What could not be verified section and nowhere else. Other sections say a figure is missing and point to that list, without the prefix."
   - DONE WHEN 4 matches it: "every line is in the What could not be verified section; exactly one line names each of the CI configuration, the build times, the bill and usage, and the GitHub plan that the user did not supply".
   - "Run history" no longer sits in the count, and "no reply counts as nothing supplied" settles the no-reply case.

3. No check covered the cost lines: CLOSED.
   - DONE WHEN 3 now reads: "it has separate lines for the vendor charges, the build compute and the migration effort in engineer-weeks, with no total", and "every metered item a helper's file lists for GitHub Actions on the user's plan (each published tier read, where no plan was named) and for each published Buildkite tier read appears in that vendor's lines; at least one price is named for each of GitHub Actions and Buildkite; and when the person opens the URL cited beside each price, it is on the vendor's own site and the quoted wording on that page states that price."

Part notes from r1 also closed: "ASSUMED: a helper's return is capped at 40 words per field." and "The same failure repeats across helpers." are now in the draft. Step 3 now prices first: "price the supplied usage at each vendor's cited prices first, showing inputs and arithmetic".

## The three questions, on the revised draft

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? No.
   - The Wait path is what the GOAL says it delivers: "otherwise it is Wait, naming each figure that would settle it". DONE WHEN 2 requires the same: "a Wait names each missing figure that would settle it".
   - A Wait memo still has to show the cost structure: "at least one price is named for each of GitHub Actions and Buildkite", plus every metered item a helper file lists.
   - The vacuous "Given" conditions are closed: "no reply counts as nothing supplied" (check 4) and "no reply counts as not supplied" (check 5). Check 5's no-configuration branch "gives no range" and must list "what to count (workflow files, third-party actions, secrets by name and runner types)".

2. Does any STOP AND ASK condition already hold? No.
   - "Supplied figures contradict each other, or a supplied figure cannot be matched to the unit a vendor prices in (for example dollars with no usage)": the log shows nothing supplied. The project folder holds "only the decision log", and the user "does not know" the spend.
   - "The same failure repeats across helpers": no helper has run.
   - "The user asks, during the run, for something CONSTRAINTS forbids": no such request exists.

3. Is every file, record and system the steps need located, or listed as UNKNOWN? Not quite, for one record (see blocker 1 below).
   - Covered by UNKNOWN: "location of the monorepo, its CI configuration and its run history (the project folder is empty)", the bill and usage, the GitHub plan, the deadline date and the monthly spend.
   - Covered by path: "`docs/ci-migration-memo.md`", "`docs/discovery/ci-buildkite-writeup.md`", and `<scratch>` for helper files.
   - Not covered: the inputs the step 5 reviewer needs to judge DONE WHEN 3, 4 and 5.

## Open or new blockers

1. Step 5's reviewer is not given what DONE WHEN 3, 4 and 5 need, so it cannot give the PASS or FAIL that step 5 asks for. New: DONE WHEN 3 now depends on helper files.
   - Evidence, step 5: "give one fresh reviewer only the memo, the decision log and this prompt's DONE WHEN and CONSTRAINTS, nothing from this session. Ask for PASS or FAIL on each DONE WHEN item with one line of evidence".
   - Evidence, the checks: DONE WHEN 3, "Given the memo and the pricing helpers' files in `<scratch>`"; DONE WHEN 4, "Given the user's reply to the step 1 ask ... none names one the user did supply"; DONE WHEN 5, "when a person re-counts each number in the Migration work section from that configuration".
   - Why it blocks: the reviewer has no helper files, no record of what the user supplied and no CI configuration. It cannot check that every metered item a helper listed is in the memo, that no GAP line names an input the user did supply, or that the counts match. The only independent read is therefore blind on three of five checks. Step 6 is the lead's own run of the same checks, and the skill says a self-check "misses the conflicts a fresh reader finds". Step 5 has to name the helper files, the user's reply and the supplied configuration as inputs, or drop the PASS or FAIL request for those checks.

Count: 1
