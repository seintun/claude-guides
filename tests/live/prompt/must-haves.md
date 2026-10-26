# Must-haves per battle scenario

The acceptance checks each scenario's prompt needs, taken from the reasons blind reviewers gave for picking a winner in past rounds ([results.md](results.md)). A v8 prompt may not lose one that the v7 prompt for the same scenario has. Frozen on 2026-10-25, before any v8 code changed.

A reviewer marks each item PRESENT or ABSENT in a draft, with a quote. PRESENT means a DONE WHEN check, a CONSTRAINT or a HOW TO WORK step requires it, not just a mention.

## bugfix

- B1. A new test that fails without the fix and passes with it (rounds 4 and 11).
- B2. The test drives the real path that issues the token or session, not a mock of it (round 11).
- B3. Existing tests are left unedited, with a check that lists modified or deleted test files (round 4).

## feature

- F1. The export carries the page's current filter state, and a check proves it (round 9).
- F2. A check uses more matching rows than one page shows, so a one-page export fails (round 11).
- F3. Cell values are quoted or escaped so a value can't run as a spreadsheet formula (round 4).

## overnight

- O1. A PR merges only when the named test job passed on the PR's head commit, not when any check is green (rounds 10 and 11).
- O2. Patch-only is decided from the lockfile or parsed versions, not from the PR title (round 4).
- O3. A run that merges nothing passes only when no PR was eligible (round 10).

## research

- R1. Every helper gets the same brief and returns the same fields (round 4).
- R2. A decision rule is stated before the evidence is weighed (round 11).
- R3. Each claim the recommendation rests on is verified with a quote and its source (round 11).

## refactor

- RF1. Behaviour is pinned by tests before any code moves (round 10).
- RF2. A check proves the code moved verbatim (rounds 10 and 11).
- RF3. A deliberate break of the original code makes a pinned test fail, with the break named (round 11).

## migration

- M1. Each file's test names and assertions are preserved, compared per file, not as summed counts (round 9).
- M2. The suite stays green between batches, with each batch gated (round 4).
- M3. A batch that turns the suite red is reverted (round 4).
