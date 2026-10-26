# Must-have check, blind23/single

## D01 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 names and assertions preserved, compared per file | PRESENT | DONE WHEN 3: "Given the baseline and final per-file lists of test titles ... no title is missing" (assertions guarded by CONSTRAINT "never edit an assertion, test title or test data") |
| M2 suite green between batches, each batch gated | PRESENT | HOW TO WORK 5: "Merge one batch at a time. For each finished batch ... rerun the full `npm test`." |
| M3 red batch reverted | PRESENT | HOW TO WORK 5: "If it is red, revert that batch, send it back once" |

## D02 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | DONE WHEN 3: "Slice 1 adds them and they pass against the unsplit src/billing.js before slice 2 starts." |
| RF2 check proves code moved verbatim | ABSENT | Only export-surface diff and line caps; no check that moved code is unchanged text. |
| RF3 deliberate break of original makes pinned test fail, break named | PRESENT | DONE WHEN 5 names the break ("change the first `+`, `-` ... operator"); HOW TO WORK 2: "Add cases until check 5's breaks fail the suite for every export" |

## D03 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields for every helper | PRESENT | HOW TO WORK 2: "Start the three helpers in parallel with the same brief"; brief: "exactly these seven fields" |
| R2 decision rule stated before evidence weighed | ABSENT | No rule for how the pick is made; only flip thresholds asked for after the fact (DONE WHEN 3). |
| R3 each load-bearing claim verified with quote and source | PRESENT | HOW TO WORK 4: "re-opens the source for every claim the recommendation rests on and confirms the quoted wording is there" |

## D04 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries current filter state, proven by a check | PRESENT | DONE WHEN 2: "A test asserts this against fixture data in which the filter hides at least one row." |
| F2 check uses more matching rows than one page shows | ABSENT | Pagination only raised in STOP AND ASK IF with a default; no check with more rows than a page. |
| F3 cells escaped against formula injection | PRESENT | CONSTRAINT: "A field that starts with `=`, `+`, `-` or `@` is prefixed with a single quote" |

## D05 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | DONE WHEN 1: "shown by a new automated test that fails on the unfixed code"; DONE WHEN 3 revert check |
| B2 test drives real token/session path, not a mock | ABSENT | Test scenario described ("complete a password reset with a valid token") but nothing requires the real issuing path or forbids mocking it. |
| B3 existing tests unedited, check lists modified/deleted test files | PRESENT | DONE WHEN 2: "list modified and deleted test files with `git diff --name-status <base>...HEAD -- <test paths>`" |

## D06 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 names and assertions preserved, compared per file | ABSENT | DONE WHEN 2 compares one global set of names (describe path plus title), not per file; assertions only by CONSTRAINT. |
| M2 suite green between batches, each batch gated | PRESENT | HOW TO WORK 5: "Lead brings each batch back one at a time: merge it ... rerun the full `npm test`" |
| M3 red batch reverted | PRESENT | HOW TO WORK 5: "If red, or any name is missing or added, revert that batch" |

## D07 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields for every helper | PRESENT | HOW TO WORK 2: "each with the brief below. They must return the same eight fields" |
| R2 decision rule stated before evidence weighed | ABSENT | Only "if the margin is thin, report a near-tie"; no rule for weighing the fields set before synthesis. |
| R3 each load-bearing claim verified with quote and source | PRESENT | DONE WHEN 3: "when you open its cited URL, then the page carries the quoted wording written beside the claim" |

## D08 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | DONE WHEN 1: "characterization tests for `src/billing.js` that were committed before any code moved" |
| RF2 check proves code moved verbatim | ABSENT | Export, untouched-files and size checks only; nothing proves moved code is unchanged. |
| RF3 deliberate break of original makes pinned test fail, break named | PRESENT | DONE WHEN 2: "before any code moves, replace the return value of the first exported function ... with `null`, run `npm test`, and see it fail" |

## D09 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries current filter state, proven by a check | PRESENT | DONE WHEN 1: "a new test that sets a filter hiding at least one row ... asserts the CSV holds ... the same rows" |
| F2 check uses more matching rows than one page shows | ABSENT | "All filtered rows, not only the current page" is an ASSUMED line; no check with more rows than a page. |
| F3 cells escaped against formula injection | PRESENT | DONE WHEN 3: "the CSV cell starts with a single quote followed by the original text" |

## D10 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 merge only when the named test job passed on head commit | ABSENT | Requires "all checks `SUCCESS` on the head commit"; no named test job, so any all-green set passes. |
| O2 patch-only from lockfile or parsed versions, not title | PRESENT | CONSTRAINT: "Decide patch-only from the diff and the version numbers, not from the title." |
| O3 zero-merge run passes only when no PR was eligible | PRESENT | DONE WHEN 1: "Given step 2 ... found at least one merge-ready PR, at least one PR was merged ... If step 2 found none, this item is NOT RUN, not PASS." |

## D11 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | DONE WHEN 2: "Given the fix's source change is reverted ... then the new test fails with the logged-out symptom." |
| B2 test drives real token/session path, not a mock | PRESENT | DONE WHEN 1: "they complete the app's password reset flow in an automated test ... the old password is rejected and the new password signs in" (borderline: no explicit no-mock rule) |
| B3 existing tests unedited, check lists modified/deleted test files | PRESENT | DONE WHEN 3: "`git diff --name-status <start-commit>`, then no test file shows as modified (M) or deleted (D)" |

## D12 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 merge only when the named test job passed on head commit | ABSENT | Uses "all required checks concluded success" on head SHA; no named test job. |
| O2 patch-only from lockfile or parsed versions, not title | PRESENT | DONE WHEN 1: "every dependency version changed in its diff (manifest and lockfile) moved only in the third number" |
| O3 zero-merge run passes only when no PR was eligible | ABSENT | Checks only that every PR is reported with a reason; a run that skips every eligible PR still passes. |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | migration | 3 | 0 |
| D02 | refactor | 2 | 1 |
| D03 | research | 2 | 1 |
| D04 | feature | 2 | 1 |
| D05 | bugfix | 2 | 1 |
| D06 | migration | 2 | 1 |
| D07 | research | 2 | 1 |
| D08 | refactor | 2 | 1 |
| D09 | feature | 2 | 1 |
| D10 | overnight | 2 | 1 |
| D11 | bugfix | 3 | 0 |
| D12 | overnight | 1 | 2 |
