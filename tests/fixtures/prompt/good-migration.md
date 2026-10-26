GOAL
Move the 400 Jest test files to Vitest with no loss of coverage.

DONE WHEN
1. `npx vitest run` exits 0 and reports 400 test files.
2. `git diff --name-status main -- '*.test.js'` lists no deleted test file.
3. Given a deliberately broken assertion in one migrated file, when `npx vitest run` runs, then it exits 1.

CONSTRAINTS
- Do not edit or delete existing tests to make them pass; change only the runner syntax.
- Keep shared config (vitest.config.ts, package.json) with the lead.

BUDGET
- At most 4 writers and 6 hours; stop and report when it runs out.

STOP AND ASK IF
- a file needs a behaviour change, not a syntax change
- the same failure repeats across 2 batches

HOW TO WORK
1. Split the files into disjoint batches of 50; each writer gets its own batch and its own worktree.
2. Each batch must pass its gate: `npx vitest run <batch>` exits 0.
3. The lead merges one batch at a time and reruns the full suite; a batch that turns the full run red is reverted.
4. The full suite stays green between batches.

REPORT
Each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.
