# Must-have check, blind set B (single)

## D01 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 | PRESENT | DONE WHEN 1: "Given a reports page with a filter that hides at least one row ... the CSV has one header line plus exactly the visible rows" |
| F2 | ABSENT | Paging is only a STOP AND ASK question; no check uses more matching rows than one page shows. |
| F3 | PRESENT | CONSTRAINT: "cells that begin with `=`, `+`, `-` or `@` ... prefix such a cell with a single quote. Tests expect the changed form" |

## D02 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 | PRESENT | HOW TO WORK 1: "Brief three read-only helpers in parallel, one per option, with the same brief"; brief fixes six `## ` headings |
| R2 | ABSENT | No decision rule (criteria or weighting for the pick) is stated before evidence is weighed; only conditional pick on gaps. |
| R3 | PRESENT | HOW TO WORK 3: "verify the claims the recommendation rests on against the quoted wording"; CONSTRAINT: "Every claim has a URL and the quoted wording beside it." |

## D03 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 | ABSENT | Checks compare the summed passing count with the baseline; no per-file comparison of test names and assertions. |
| M2 | PRESENT | HOW TO WORK 7: "verify its claims by running the full `npm test` after adding the batch's files ... compare the passing count with the baseline" |
| M3 | PRESENT | HOW TO WORK 7: "If anything is red or the count dropped, revert that batch, retry up to 3 times" |

## D04 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 | PRESENT | DONE WHEN 2: "Given the fix commit is reverted ... the regression test ... fails with an assertion error ...; on the fix commit it passes" |
| B2 | ABSENT | Test describes completing the reset, but nothing requires driving the real token/session issuing path or forbids mocking it. |
| B3 | PRESENT | DONE WHEN 3: "`git diff --name-status <start sha>..HEAD`, filtered to test files, lists no `M` or `D` entry" |

## D05 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 | PRESENT | DONE WHEN 3: "Slice 1 adds them and they pass against the unsplit src/billing.js before slice 2 starts." |
| RF2 | ABSENT | Only the export list and line counts are checked; no check that the code moved verbatim. |
| RF3 | PRESENT | DONE WHEN 5: "change the first `+`, `-`, `*` ... operator in that function ...; `npm test` must exit non-zero and name a failing test" |

## D06 (feature)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| F1 | PRESENT | DONE WHEN 1: "sets a filter hiding at least one row, triggers the export, and asserts the CSV holds ... the same rows ... as the filtered table" |
| F2 | ABSENT | All-pages reading is only an ASSUMED line; no check uses more matching rows than one page shows. |
| F3 | PRESENT | DONE WHEN 3: "Given a cell whose text starts with `=`, `+`, `-` or `@` ... the CSV cell starts with a single quote" |

## D07 (research)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| R1 | PRESENT | HOW TO WORK 2: "each with the brief below. They must return the same eight fields" |
| R2 | ABSENT | "Flips if" conditions and a thin-margin near-tie, but no decision rule stated before weighing evidence. |
| R3 | PRESENT | DONE WHEN 3: "when you open its cited URL, then the page carries the quoted wording ... marked VERIFIED or UNVERIFIED" |

## D08 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 | ABSENT | Gate is "all required checks concluded success" on the head SHA; no named test job is required. |
| O2 | PRESENT | DONE WHEN 1: "every dependency version changed in its diff (manifest and lockfile) moved only in the third number" |
| O3 | ABSENT | No check fails a zero-merge run when an eligible PR existed; DONE WHEN 2 only accounts for every PR. |

## D09 (bugfix)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| B1 | PRESENT | DONE WHEN 1: "shown by a new automated test that fails on the unfixed code"; DONE WHEN 3 reverts the fix and the test fails |
| B2 | ABSENT | Nothing requires the test to drive the real token/session issuing path rather than a mock. |
| B3 | PRESENT | DONE WHEN 2: "list modified and deleted test files with `git diff --name-status <base>...HEAD -- <test paths>` ... only new files appear" |

## D10 (refactor)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| RF1 | PRESENT | CONSTRAINT: "New characterization tests are written first, against the unchanged file, and must pass on it before any code moves." |
| RF2 | ABSENT | Export list, test counts and path list are checked; no check that code moved verbatim. |
| RF3 | PRESENT | DONE WHEN 4: "the lead changes one returned amount in that module by one cent and runs `npm test`, Then it fails" |

## D11 (overnight)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| O1 | ABSENT | Gate is "has all checks at success" on the head commit; no named test job is required. |
| O2 | PRESENT | DONE WHEN 1: "its diff changes only package.json and package-lock.json with patch-only bumps"; unparsable version is reported, not merged |
| O3 | PRESENT | DONE WHEN 3: "A run that merges nothing while such a PR exists fails the check." |

## D12 (migration)

| Must-have | PRESENT or ABSENT | Quote or what is missing |
|---|---|---|
| M1 | ABSENT | Test names are compared as one global set; no per-file comparison and no assertion comparison. |
| M2 | PRESENT | HOW TO WORK 5: "rerun the full `npm test`, and compare test names with the baseline" for each batch, one at a time |
| M3 | PRESENT | HOW TO WORK 5: "If red, or any name is missing or added, revert that batch and retry or skip" |

## Summary

| File | Scenario | Present | Absent |
|---|---|---|---|
| D01 | feature | 2 | 1 |
| D02 | research | 2 | 1 |
| D03 | migration | 2 | 1 |
| D04 | bugfix | 2 | 1 |
| D05 | refactor | 2 | 1 |
| D06 | feature | 2 | 1 |
| D07 | research | 2 | 1 |
| D08 | overnight | 1 | 2 |
| D09 | bugfix | 2 | 1 |
| D10 | refactor | 2 | 1 |
| D11 | overnight | 2 | 1 |
| D12 | migration | 2 | 1 |
