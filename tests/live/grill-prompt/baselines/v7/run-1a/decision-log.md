# Discovery: CLI --help text after the export flag rename

Started 2026-10-24. Source request, in the user's words: "My CLI's --help text is out of date after we renamed the export flag. Fix it so it matches. Should take an hour."

## Found by looking

- 2026-10-24: searched the project root for source, README, CLAUDE.md, docs/ and git history. Found nothing: the folder is empty and is not a git repository.

## Decisions

(Date, question, answer, reason. One entry per answered question.)

1. 2026-10-24. Q: What should prove the help text now matches the renamed flag? A: an output check. Run the help for the main command and for every subcommand that takes the export flag. Each output names the new flag and never the old one. Reason: smallest repeatable check that fails if the old name is left behind, and it fits the one-hour appetite. Rejected: a permanent help-vs-parser test (new test code, past the hour, past the export flag) and a read-through only (nothing repeatable).

2. 2026-10-24. Q: If the old flag name also shows up outside the --help output (README, man page, shell completions, example scripts), what should the run do? A: leave those places alone and list each one by file and line in the report. Reason: the request is about the --help text, and an hour leaves no room to audit other docs. Rejected: fixing them too (more files than the request names, risk of touching generated or release docs) and stopping to ask (stalls the run).

3. 2026-10-24 (asked during /prompt). Q: The prompt needs the CLI's source and a git repository, and this folder holds neither, so a stop line "the CLI is not in the working directory" already holds today. How should the prompt treat it? A: run from the repository that holds the CLI, and stop with BLOCKED if no parser and no help text are found there. Reason: the person starting the run knows which repository holds the CLI, and a stop is cheap. Rejected: asking for the path first (the path stays unknown in the prompt and the run waits on the user).

## From the request, not asked

- Appetite: one hour (the request says "should take an hour").
- Problem: the CLI's `--help` still describes the export flag by its old name after the rename. The request does not say who reads the help or what the stale text has cost them. Not asked: the fix is the same either way.
- Scope and no-go: the `--help` text only. The request asks for the help to match the renamed flag, so no change to flag behavior (no alias, no parser edit).

## Ground covered

- Where the work lives: the CLI's source, including its help text and flag parser. Location not known (see Open questions). The new flag name is read from the parser at run time and the old name from the stale help text or git history, so neither is asked of the user.
- Outcome metric: decision 1.
- Appetite: one hour, from the request.
- No-gos: no change to flag behavior; no edits outside the help text (decision 2 and the request).
- Rabbit holes: auditing README, man pages, completions or other flags whose help has drifted. Out of scope; list what is found (decision 2).
- Failure cases and the riskiest assumption: see ASSUMED.

## Open questions

- UNKNOWN: where the CLI's source lives. Asked 2026-10-24, the user said "I don't know".

## ASSUMED

- ASSUMED: the rename is finished in the parser and the new name is final. Riskiest assumption. Cheapest test: run the CLI with the new flag name and confirm the parser accepts it. If it does not, stop: the help would then describe a flag that does not exist yet.
- ASSUMED: failure cases the fix must cover are every place the help output names the old flag: the usage line, example lines, other flags' descriptions and each subcommand's help.
- ASSUMED: if a test or stored copy of the help output fails after the fix, it is regenerated from the real output; no other test is edited.

## Not committed

No git repository exists in the project, so this log is not committed and there is no issue to link it from.
