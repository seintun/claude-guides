# REPORT: CSV export on the reports page

Baseline: `npm test` passed (4 tests) before any change. Base commit e24667d.

1. PASS `npm test` exits 0 (8 pass, 0 fail); output lists "export CSV keeps header plus the filtered rows, matching the page", "export CSV round-trips commas, quotes and newlines", "export CSV prefixes formula-like values with a single quote", "export CSV with a filter that keeps no rows is the header only".
2. PASS `npm test`: 5-row dataset, filter { minAmount: 60 } keeps 2; CSV has 3 lines, data rows equal the cells parsed from `renderReportsPage` output, same order, no filtered-out row.
3. PASS `npm test`: value `a, "b"\nc` round-trips through the test's RFC 4180 parser; formula-prefixed values (=, +, -, @) read back with a leading single quote.
4. PASS `npm test`: filter keeping zero rows gives the header line only.
5. PASS `git diff --name-status e24667d -- test` prints nothing (new test file is untracked, no M or D on existing tests). Break check: with `exportCsv` using `visibleRows(rows, {})`, `npm test` failed the check 2 test (and the zero-row test); reverted, `npm test` 8 pass, 0 fail.

NOT RUN: the fresh reviewer step (HOW TO WORK 5), because no subagent can be started here. Not independently reviewed.

Notes: header keys come from the first input row (unfiltered), falling back to COLUMNS when there are no rows. The page already had an "Export CSV" link to /reports/export.csv; I added `download="reports.csv"`. No server route exists in the repo, so nothing serves that URL yet; wiring it is outside the allowed files.

Changed files:
- src/reports.js — exportCsv implemented via visibleRows; csvCell escaping; download attribute on link | verified: PASS npm test
- test/reports-export.test.js — new; 4 export tests | verified: PASS npm test
