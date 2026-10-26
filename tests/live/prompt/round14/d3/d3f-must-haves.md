# Must-have check, d3blind-full/single D01 to D12

## D01 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields | PRESENT | "Helper brief (same for all three, with OPTION filled in)"; DONE WHEN 1: "gives the same count of criterion headings in each file" |
| R2 decision rule before evidence | ABSENT | Criteria are listed, but no rule says how they are weighed or what decides the pick; only "say which volume flips it". |
| R3 claims verified with quote and source | PRESENT | "look up its cited quote with `grep -F` ... A claim with no cited file and quote, or a quote not found, fails." |

## D02 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 names and assertions preserved per file | ABSENT | Names are compared as one global set "without the file path"; only case counts are per file; assertions are never compared. |
| M2 green between batches, each batch gated | PRESENT | "Lead integrates one batch at a time. After each, rerun the full `npm test` and compare test names with the baseline." |
| M3 red batch reverted | PRESENT | "A batch that turns the suite red is reverted, retried up to the retry cap, then listed under NEEDS A HUMAN" |

## D03 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned before code moves | PRESENT | "New tests pin current behaviour (characterization tests) before the code around them moves." |
| RF2 check proves verbatim move | ABSENT | Only export names are compared; no check that moved code is unchanged text. |
| RF3 named deliberate break fails a test | PRESENT | "when its first `return` expression is replaced with `undefined` in a scratch copy of the branch, then `npm test` fails" |

## D04 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 named test job passed on head commit | ABSENT | Head commit is pinned ("checks were read as all successful"), but no test job is named; all present checks green would pass if the test job never ran. |
| O2 patch-only from lockfile or parsed versions | PRESENT | "every changed version in `package.json`, and every changed top-level dependency version in `package-lock.json` ... differs ... only in the patch number" |
| O3 zero-merge run passes only if none eligible | PRESENT | "each one appears exactly once as `merged` or `not merged: <reason>`"; zero found "names the bot filter it used, so a wrong filter shows" |

## D05 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned before code moves | PRESENT | "Slice 0: write the characterization tests, run them against the base ... Commit the tests alone." |
| RF2 check proves verbatim move | ABSENT | No check compares moved code with the original text; only exports and line counts are checked. |
| RF3 named deliberate break fails a test | PRESENT | "the first line of arithmetic that computes an amount in the new modules has its operator flipped ... then it exits non-zero" |

## D06 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | "With the fix's changes to non-test files reverted to the base commit ... the new regression test fails." |
| B2 test drives real token/session path | PRESENT | "a user who has just completed a password reset through the app's reset flow ... request an authenticated page with the credential" |
| B3 existing tests unedited, with listing check | PRESENT | "`git diff --name-status <base-sha>..HEAD` lists no existing test file with status M or D" |

## D07 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries filter state, proved | PRESENT | "the CSV has one header line plus one line per visible row ... A test in `npm test` asserts this"; break removes the filter argument. |
| F2 check uses more rows than one page | ABSENT | Paging is only a STOP AND ASK trigger; no check uses more matching rows than one page shows. |
| F3 cells escaped against formulas | PRESENT | "Given a cell starting with =, +, - or @, the exported cell begins with a single quote" |

## D08 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 named test job passed on head commit | ABSENT | "all checks on that commit were success" pins the head SHA but names no test job that must be among them. |
| O2 patch-only from lockfile or parsed versions | PRESENT | "read its dependency diff and its checks, and decide: eligible (patch-only, only the two files ...)"; DONE WHEN 1 reads the dependency diff. |
| O3 zero-merge run passes only if none eligible | PRESENT | "With zero merges the check passes only if the report lists each open dependency PR with a reason (or no dependency PR was open)." |

## D09 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 names and assertions preserved per file | PRESENT | "For each file in the list, the count of `expect(` occurrences before and after is equal."; "Assertions, test names and test data are immutable" |
| M2 green between batches, each batch gated | PRESENT | "bring batches back one at a time ... merge into the migration branch, rerun the full `npm test` and DONE WHEN checks 1 to 3" |
| M3 red batch reverted | PRESENT | "If the suite is red or a check fails, revert that batch, dispatch once more with the failure output" |

## D10 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields | PRESENT | "Give all three the same brief and the same return fields." |
| R2 decision rule before evidence | ABSENT | Fields and assumed scale are fixed, but no rule says which criterion decides or how they are weighed. |
| R3 claims verified with quote and source | PRESENT | "verify the claims the recommendation rests on by opening the cited source and finding the quoted wording" |

## D11 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | "with the fix diff reverted (revert the changed non-test source files, keep the new test), the new test fails" |
| B2 test drives real token/session path | PRESENT | "The test must call the real reset endpoint and then a protected endpoint with the resulting session." |
| B3 existing tests unedited, with listing check | PRESENT | "`git diff --name-status <base>..HEAD` ... lists no test file as `M` or `D`." |

## D12 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries filter state, proved | PRESENT | "a new test that applies a filter excluding at least one row, exports, and asserts the CSV data rows equal the visible rows" |
| F2 check uses more rows than one page | ABSENT | "large row counts" is a handling constraint; no check exports more matching rows than one page shows. |
| F3 cells escaped against formulas | PRESENT | "the `=` cell, which is expected in its changed form (single quote prefix)" |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | research | 2 (R1, R3) | 1 (R2) |
| D02 | migration | 2 (M2, M3) | 1 (M1) |
| D03 | refactor | 2 (RF1, RF3) | 1 (RF2) |
| D04 | overnight | 2 (O2, O3) | 1 (O1) |
| D05 | refactor | 2 (RF1, RF3) | 1 (RF2) |
| D06 | bugfix | 3 | 0 |
| D07 | feature | 2 (F1, F3) | 1 (F2) |
| D08 | overnight | 2 (O2, O3) | 1 (O1) |
| D09 | migration | 3 | 0 |
| D10 | research | 2 (R1, R3) | 1 (R2) |
| D11 | bugfix | 3 | 0 |
| D12 | feature | 2 (F1, F3) | 1 (F2) |
