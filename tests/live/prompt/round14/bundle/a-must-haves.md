# Must-have check, blind set A (single)

## D01 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 filter state carried, proven by a check | PRESENT | DONE WHEN 1: "with a filter applied that hides at least one row ... the CSV has one header line plus one line per visible row" |
| F2 check uses more matching rows than one page shows | ABSENT | Paging only appears as a STOP AND ASK trigger; no check uses more matching rows than one page holds. |
| F3 cells quoted or escaped against formula injection | PRESENT | DONE WHEN 3: "Given a cell starting with =, +, - or @, the exported cell begins with a single quote" |

## D02 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields for every helper | PRESENT | HOW TO WORK 2: "Start the three helpers in parallel with the same brief and their option name." |
| R2 decision rule stated before evidence is weighed | ABSENT | Fields to compare are fixed, but no rule says how the pick will be made from them before the findings are read. |
| R3 each load-bearing claim verified with quote and source | PRESENT | HOW TO WORK 4: "re-opens the source for every claim the recommendation rests on and confirms the quoted wording is there" |

## D03 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 merge only when the named test job passed on the head commit | ABSENT | Requires "all checks on that commit were success" on the head SHA, but names no test job; any set of green checks would satisfy it. |
| O2 patch-only from lockfile or parsed versions, not title | PRESENT | DONE WHEN 1: "when each is read with `gh pr view ...` and its dependency diff, then ... every changed dependency moved by a patch version only" |
| O3 zero-merge run passes only when no PR was eligible | PRESENT | DONE WHEN 1: "With zero merges the check passes only if the report lists each open dependency PR with a reason" (reasons are ineligibility reasons; weaker than D05's explicit rule) |

## D04 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | DONE WHEN 1: "characterization tests for `src/billing.js` that were committed before any code moved" |
| RF2 check proves code moved verbatim | ABSENT | Export-key and untouched-file checks only; nothing compares moved function bodies with the original. |
| RF3 named deliberate break of original code fails a pinned test | PRESENT | DONE WHEN 2: "replace the return value of the first exported function in `src/billing.js` with `null`, run `npm test`, and see it fail" |

## D05 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 merge only when the named test job passed on the head commit | ABSENT | Requires "all checks `SUCCESS` on the head commit that was merged"; no specific test job is named. |
| O2 patch-only from lockfile or parsed versions, not title | PRESENT | CONSTRAINTS: "Decide patch-only from the diff and the version numbers, not from the title." |
| O3 zero-merge run passes only when no PR was eligible | PRESENT | DONE WHEN 1: "Given step 2 ... found at least one merge-ready PR, at least one PR was merged ... If step 2 found none, this item is NOT RUN" |

## D06 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields for every helper | PRESENT | HOW TO WORK 1: "Give all three the same brief and the same return fields." |
| R2 decision rule stated before evidence is weighed | ABSENT | Scale and fields are fixed up front, but no rule for choosing among options is stated before the findings are read. |
| R3 each load-bearing claim verified with quote and source | PRESENT | DONE WHEN 2: "Each claim it rests on is repeated with its source URL and quoted wording." |

## D07 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without the fix, passes with it | PRESENT | DONE WHEN 2: "Given the fix's source change is reverted ... then the new test fails with the logged-out symptom." |
| B2 test drives the real token or session path, not a mock | PRESENT | DONE WHEN 1: "when they complete the app's password reset flow in an automated test and then make an authenticated request in the same session" (no explicit ban on mocks) |
| B3 existing tests unedited, checked by a file listing | PRESENT | DONE WHEN 3: "`git diff --name-status <start-commit>`, then no test file shows as modified (M) or deleted (D)" |

## D08 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | CONSTRAINTS: "New tests pin current behaviour (characterization tests) before the code around them moves." |
| RF2 check proves code moved verbatim | ABSENT | Only export keys and line counts are compared; no verbatim-move check. |
| RF3 named deliberate break of original code fails a pinned test | PRESENT | DONE WHEN 4: "its first `return` expression is replaced with `undefined` ... then `npm test` fails" (break is on the moved code at branch head, not the pre-move original) |

## D09 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without the fix, passes with it | PRESENT | DONE WHEN 2: "With the fix's changes to non-test files reverted to the base commit ... the new regression test fails." |
| B2 test drives the real token or session path, not a mock | PRESENT | DONE WHEN 1: "a user who has just completed a password reset through the app's reset flow ... request an authenticated page" (no explicit ban on mocks) |
| B3 existing tests unedited, checked by a file listing | PRESENT | DONE WHEN 3: "`git diff --name-status <base-sha>..HEAD` lists no existing test file with status M or D" |

## D10 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 filter state carried, proven by a check | PRESENT | DONE WHEN 2: "A test asserts this against fixture data in which the filter hides at least one row." |
| F2 check uses more matching rows than one page shows | ABSENT | Paging is a STOP AND ASK item with a default; no check uses more rows than one page shows. |
| F3 cells quoted or escaped against formula injection | PRESENT | CONSTRAINTS: "A field that starts with `=`, `+`, `-` or `@` is prefixed with a single quote so a spreadsheet does not run it" |

## D11 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 test names and assertions preserved, compared per file | PRESENT | DONE WHEN 3: "Given the baseline and final per-file lists of test titles ... no title is missing"; CONSTRAINTS: "never edit an assertion, test title or test data" |
| M2 suite green between batches, each batch gated | PRESENT | HOW TO WORK 5: "Merge one batch at a time ... and rerun the full `npm test`." |
| M3 a batch that turns the suite red is reverted | PRESENT | HOW TO WORK 5: "If it is red, revert that batch, send it back once" |

## D12 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 test names and assertions preserved, compared per file | ABSENT | Names are compared as one set "without the file path"; per file only case counts match. No per-file name or assertion comparison. |
| M2 suite green between batches, each batch gated | PRESENT | HOW TO WORK 7: "Lead integrates one batch at a time. After each, rerun the full `npm test`" |
| M3 a batch that turns the suite red is reverted | PRESENT | HOW TO WORK 7: "A batch that turns the suite red is reverted, retried up to the retry cap" |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | feature | 2 | 1 (F2) |
| D02 | research | 2 | 1 (R2) |
| D03 | overnight | 2 | 1 (O1) |
| D04 | refactor | 2 | 1 (RF2) |
| D05 | overnight | 2 | 1 (O1) |
| D06 | research | 2 | 1 (R2) |
| D07 | bugfix | 3 | 0 |
| D08 | refactor | 2 | 1 (RF2) |
| D09 | bugfix | 3 | 0 |
| D10 | feature | 2 | 1 (F2) |
| D11 | migration | 3 | 0 |
| D12 | migration | 2 | 1 (M1) |
