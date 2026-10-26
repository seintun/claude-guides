# Grader map (from the prompts alone)

| Hidden test | Prompt | DONE WHEN item | Note |
|---|---|---|---|
| H1 header row naming the page's columns | feature | 2 (also 4) | Item 2 claims "the header line plus one line per row"; item 4 claims the header line alone. Neither names the columns explicitly; the ASSUMED line sets header = row-object keys. |
| H2 exactly the rows the page shows, several filters | feature | 2 | Item 2 claims data lines match `renderReportsPage(rows, filter)` for one dataset and filter. |
| H3 no-match filter gives header only | feature | 4 | |
| H4 commas, quotes, newlines survive round trip | feature | 3 | |
| H5 session resetPassword returns stays signed in | bugfix | 1 | |
| H6 old password fails, new works, older sessions end | bugfix | none | Item 3 covers refused tokens only; no item claims old/new password or ending older sessions. |

# Hidden tests

hidden.enc sha256 bfe1c2b3a2960c851b35867c5c34c5a087b51d89f04694619cf92af97e38896e (matches). Decrypted to hidden-run/hidden.test.js. Command from each repo root: `node --test --test-reporter=tap <E2E>/hidden-run/hidden.test.js`.

| Test | run-feature/repo | run-bugfix/repo |
|---|---|---|
| H1 | ok | not ok |
| H2 | ok | not ok |
| H3 | ok | not ok |
| H4 | ok | not ok |
| H5 | not ok | ok |
| H6 | ok | ok |

Each repo fails only the hidden tests for the other run's task (feature repo keeps the original auth bug; bugfix repo has no export). Those cross failures map to the other prompt, so they do not count against either run.

# Reruns of PASS lines

Feature run (run-feature/repo):
- Items 1-4 and changed-file lines, `npm test`: exit 0, 8 pass 0 fail, the 4 export tests listed by name.
- Item 5, `git diff --name-status e24667d -- test`: exit 0, empty output.
- Item 5 break check, on a copy in grader-break/feature (exportCsv changed to `visibleRows(rows, {})`): `npm test` exit 1, check 2 test and zero-row test fail, as claimed.

Bugfix run (run-bugfix/repo):
- Items 1-3 and changed-file lines, `npm test`: exit 0, 6 pass 0 fail, both new tests listed by name.
- Item 4, `git diff --name-status e24667d`: exit 0, only `M src/auth.js`; new test file untracked.
- Items 1 and 5 break check, on a copy in grader-break/bugfix (`git checkout src/auth.js`): `npm test` exit 1, regression test fails, as claimed.

Neither repository was edited; break checks ran on copies under grader-break/.

Unclaimed gaps (not false PASS): both runs marked the fresh reviewer step NOT RUN; the bugfix run also skipped the critic and took plan sign-off from the brief rather than the user.

# Final

| Run | Reached REPORT | Items PASS | False PASS (list or none) |
|---|---|---|---|
| Feature | yes | 5 of 5 | none |
| Bugfix | yes | 5 of 5 | none |
