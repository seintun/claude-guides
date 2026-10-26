# Review r2: prompt-r1.md

Read only: prompt-r1.md, docs/discovery/cli-help-rename.md, prompt-SKILL.md, review-r1.md.

## First-review blockers

1. "Any spelling or case" is not enforced by any check (review-r1 blocker 1): CLOSED.
   - DONE WHEN check 1 now reads: "`<cli> <command> --help | grep -ci <old-forms>` prints 0".
   - DONE WHEN check 4 now reads: "`git grep -n -i <old-forms>` run from the repository root before the edit ... when you run it again after the edit, then no hit is in a help-text file".
   - CONTEXT defines the term: "`<old-forms>` is the grep options `-e <pattern>`, one for each form the old flag takes in the help text or the parser: the dashed form, the underscore form, an upper-case placeholder, and any short alias. Each pattern is written to match only the old flag, not other flags. The checks match without regard to case."
   - HOW TO WORK step 2 builds the list ("list every form the old flag takes in the help text and the parser, and write them as `<old-forms>`"). Step 3 keeps it from being empty ("Check 1 must match `<old-forms>` in at least one help output (red). If it does not, stop.").

## New-blocker questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? No.
   - Check 1: "The list holds at least the main command."
   - Check 3: "it exits 0 and reports at least one test run".
   - Check 4 pre-edit: "it must have at least one hit in a help-text file, which shows the search covers the right place".
   - Check 2 passes on an empty diff, as in round 1, but checks 1 and 4 and the red baseline carry the goal.
   - The one fallback keeps the goal check: "If the repository has no test command, this check is NOT RUN with that reason, and checks 1, 2 and 4 decide the goal."
   - A list of commands that is too short would pass check 1. Check 4 covers it: after the edit, "no hit is in a help-text file".

2. Does any STOP AND ASK condition already hold? Only the one the log settled.
   - The log says "the folder is empty and is not a git repository", and the first stop line is "The working directory is not the CLI's repository: no command-line parser and no help text found, or it is not a git repository."
   - It is settled with the user as decision 3: "run from the repository that holds the CLI, and stop with BLOCKED if no parser and no help text are found there." The draft opens with "Start this session in the repository that holds the CLI." and carries "UNKNOWN: where the CLI's source lives."
   - No other stop line holds. The parser, old-name, test-baseline and time-fit lines all depend on a repository the draft does not yet have.

3. Is every file, record and system the steps need located, or listed as UNKNOWN? Yes.
   - The CLI's source is the one gap, listed as "UNKNOWN: where the CLI's source lives. The user did not know when asked on 2026-10-24." That is 1 UNKNOWN line, under the limit of 3.
   - The parser, help-text files, stored copy, test command and rename history are found by steps 1 to 3 or have a stated path when absent: "if the repository has one", "this check is NOT RUN with that reason".
   - The decision log is cited as "`docs/discovery/cli-help-rename.md`, if the repository has it. This prompt carries the same decisions."

## Open or new blockers

none

## Not counted (no evidence that they block)

- Check 1 asks for a `<new-name>` match in the main command's help ("then the output has at least one match for `<new-name>`"). The log's decision 1 asks the same ("Each output names the new flag and never the old one"). If the main command's help does not name the flag, the check fails loudly, and the retry-cap stop line applies.
- Check 2 requires no `??` lines. The tests or CLI could leave untracked files in a repository that does not ignore them. Nothing in the draft or the log shows this; it would fail loudly.

Blocker count: 0
