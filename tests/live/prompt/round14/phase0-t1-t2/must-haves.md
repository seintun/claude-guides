# Must-have check, blind single drafts

## D01 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 per-file names and assertions | PRESENT | DONE WHEN 2(b): "Per file, the count of `expect(` and the sorted list of matcher names ... are the same at BASE and HEAD". Gap: test titles are compared per file only as counts (step 8), not by name. |
| M2 green between gated batches | PRESENT | Step 8: "run the full `npm test`. If it exits 0 and the counts match, commit and log" |
| M3 red batch reverted | PRESENT | Step 8: "Otherwise discard the changes, log the failure, and send the batch to a fresh writer once" |

## D02 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 named test job on head commit | ABSENT | Requires every check on the head to be `SUCCESS`; names no test job that must have passed. |
| O2 patch-only from versions, not title | PRESENT | CONSTRAINTS: "Decide patch-only from the diff and the version numbers, not from the title." |
| O3 zero merges passes only if none eligible | PRESENT | DONE WHEN 1: "Given step 2 ... found at least one merge-ready PR, at least one PR was merged" |

## D03 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 tests pin behaviour before moves | PRESENT | Step 3: "Commit only new test files, as T. Run the Pins check before step 4." |
| RF2 check proves verbatim move | PRESENT | DONE WHEN 5: sorted BASE and HEAD line lists, "`diff` of the sorted BASE list and the sorted HEAD list exits 0" |
| RF3 named deliberate break fails a test | PRESENT | DONE WHEN 3: "function body ... replaced by `{ throw new Error('broken'); }` ... exits non-zero" |

## D04 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields | PRESENT | Step 2: "Start the three helpers in parallel with the same brief and their option name." |
| R2 decision rule before evidence | ABSENT | No rule for choosing between options is stated; DONE WHEN 3 only asks for a pick or near-tie. |
| R3 claims verified with quote and source | PRESENT | Step 4: "re-opens the source for every claim the recommendation rests on and confirms the quoted wording" |

## D05 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with | PRESENT | DONE WHEN 2: "the fix's source change is reverted ... then the new test fails with the logged-out symptom" |
| B2 test drives real token/session path | ABSENT | Asks for the reset flow "in an automated test" but never forbids mocking the token or session code. |
| B3 existing tests unedited, with listing check | PRESENT | DONE WHEN 3: "`git diff --name-status <start-commit>`, then no test file shows as modified (M) or deleted (D)" |

## D06 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 named test job on head commit | ABSENT | Requires all check runs on the head SHA to succeed (skipped/neutral allowed); names no required test job. |
| O2 patch-only from versions, not title | PRESENT | CONSTRAINTS: "Decide from GitHub's data and the PR diff only"; patch-only defined on `x.y.z` versions. |
| O3 zero merges passes only if none eligible | PRESENT | DONE WHEN 3: every unmerged reason must match evidence; "'merge cap reached' holds only if MERGED has exactly as many entries as the merge cap" |

## D07 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 tests pin behaviour before moves | PRESENT | DONE WHEN 1: "characterization tests for `src/billing.js` that were committed before any code moved" |
| RF2 check proves verbatim move | ABSENT | No check compares moved code with the original; only exports, untouched files and sizes are checked. |
| RF3 named deliberate break fails a test | PRESENT | DONE WHEN 2: "replace the return value of the first exported function ... with `null`, run `npm test`, and see it fail" |

## D08 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries filter state, proven | PRESENT | DONE WHEN 2: "the request it makes carries exactly the filters the page used to load its rows" |
| F2 more rows than one page | ABSENT | All-pages scope is only ASSUMED; no check uses more matching rows than one page shows. |
| F3 formula-safe cells | PRESENT | DONE WHEN 3: cells are byte for byte "`'=1+1`" for the `=1+1` input |

## D09 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 export carries filter state, proven | PRESENT | DONE WHEN 2: "Given a reports page with a filter that leaves several rows ... the CSV has the header line plus one line per visible row" |
| F2 more rows than one page | ABSENT | Pagination is only a STOP AND ASK question with a default; no check uses more rows than one page. |
| F3 formula-safe cells | PRESENT | CONSTRAINTS: "A field that starts with `=`, `+`, `-` or `@` is prefixed with a single quote" |

## D10 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 same brief, same fields | PRESENT | Step 2: "with the brief below. Only the option name and file name differ." |
| R2 decision rule before evidence | PRESENT | Rule fixed in ASSUMED ("prefer the option that adds the fewest new services"); step 4: "Then apply the decision rule." |
| R3 claims verified with quote and source | PRESENT | DONE WHEN 3: "every row number on the `Rests on:` line has the status VERIFIED or CORRECTED" |

## D11 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with | PRESENT | DONE WHEN 1: "put every non-test file back to its state at BASE ... reports at least one of those cases as failed" |
| B2 test drives real token/session path | PRESENT | CONSTRAINTS: "with the app's real session, token and storage code; mock none of the session, token, clock or reset code" |
| B3 existing tests unedited, with listing check | PRESENT | DONE WHEN 4: "`git diff --name-status --diff-filter=MDR BASE FIX` lists no path in a test location" |

## D12 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 per-file names and assertions | PRESENT | DONE WHEN 3: "baseline and final per-file lists of test titles ... no title is missing". Gap: assertions kept only by CONSTRAINT ("never edit an assertion"), not compared per file. |
| M2 green between gated batches | PRESENT | Step 5: "add its files to `vitest-migrated.txt` ... and rerun the full `npm test`" |
| M3 red batch reverted | PRESENT | Step 5: "If it is red, revert that batch, send it back once" |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | migration | 3 | 0 |
| D02 | overnight | 2 | 1 (O1) |
| D03 | refactor | 3 | 0 |
| D04 | research | 2 | 1 (R2) |
| D05 | bugfix | 2 | 1 (B2) |
| D06 | overnight | 2 | 1 (O1) |
| D07 | refactor | 2 | 1 (RF2) |
| D08 | feature | 2 | 1 (F2) |
| D09 | feature | 2 | 1 (F2) |
| D10 | research | 3 | 0 |
| D11 | bugfix | 3 | 0 |
| D12 | migration | 3 | 0 |
