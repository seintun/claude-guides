# Must-have check, d3 single drafts

## D01 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | DONE WHEN 1: "This is a new automated test... with the fix diff reverted... the new test fails" |
| B2 test drives the real path, not a mock | PRESENT | DONE WHEN 1: "The test must call the real reset endpoint and then a protected endpoint with the resulting session." |
| B3 existing tests unedited, checked by listing | PRESENT | DONE WHEN 2: "`git diff --name-status <base>..HEAD` ... lists no test file as `M` or `D`." |

## D02 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 new test fails without fix, passes with it | PRESENT | DONE WHEN 2: "With the fix's changes to non-test files reverted... the new regression test fails." |
| B2 test drives the real path, not a mock | PRESENT | DONE WHEN 1: "a user who has just completed a password reset through the app's reset flow" (no explicit no-mock wording, but real flow required) |
| B3 existing tests unedited, checked by listing | PRESENT | DONE WHEN 3: "`git diff --name-status <base-sha>..HEAD` lists no existing test file with status M or D" |

## D03 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | HOW TO WORK 6: "Slice 0: write the characterization tests, run them against the base... Commit the tests alone." (plus DONE WHEN 1 base run) |
| RF2 check proves code moved verbatim | ABSENT | Only export lists and line counts are compared; no check that moved code is unchanged text. |
| RF3 deliberate break of original code fails a pinned test, break named | PRESENT | HOW TO WORK 6: "run the hand-made money-line change from CONTEXT" (on the old file; break named only loosely as "a money line") |

## D04 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 behaviour pinned by tests before code moves | PRESENT | CONSTRAINT: "New tests pin current behaviour (characterization tests) before the code around them moves." |
| RF2 check proves code moved verbatim | ABSENT | No diff or text comparison of moved code; checks cover exports, line counts and mutants only. |
| RF3 deliberate break of original code fails a pinned test, break named | ABSENT | Breaks in DONE WHEN 2 and 4 target the branch head's new modules, never the original code at S. |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | bugfix | 3 (B1, B2, B3) | 0 |
| D02 | bugfix | 3 (B1, B2, B3) | 0 |
| D03 | refactor | 2 (RF1, RF3) | 1 (RF2) |
| D04 | refactor | 1 (RF1) | 2 (RF2, RF3) |
