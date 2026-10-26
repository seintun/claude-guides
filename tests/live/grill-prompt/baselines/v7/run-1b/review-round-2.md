# Review r2: prompt-r1.md against review-r1.md, the decision log and the /prompt skill

Sources read: prompt-r1.md (revised draft), project/docs/discovery/export-flag-help-text.md (log), skills/prompt-SKILL.md (skill), review-r1.md (first findings). Nothing else.

## Status of the three blockers from review-r1

### Blocker 1: a STOP AND ASK condition already held, and the draft claimed a location the log did not support. CLOSED.

- The log now records the claim. Log, decision of 2026-10-24 (P1): "Inside the CLI's own git repository (option A of three). Not a copy or export of the source without history, and not a first step that clones the repository." It adds: "This settles the starting folder only: where the source lives stays UNKNOWN (first open question), and the prompt stops if the working directory is not a git repository or holds no CLI source."
- The draft matches the log and keeps the source as UNKNOWN: "UNKNOWN: where the CLI's source lives. The request doesn't say and the decision log records no answer. The decision log does record that the session that runs this prompt starts inside the CLI's own git repository, so step 1 finds the source from the working directory."
- The stop line "The working directory is not a git repository, or holds no source for the CLI." does not already hold. The log's "the project root is empty" describes the folder where the prompt was written. The user decided the run starts elsewhere.
- The missing-file risk is covered: "This prompt restates everything the work needs from it, so a missing file is not a reason to stop."

### Blocker 2: checks rested on UNKNOWN values, and the walk's completeness was unchecked. CLOSED.

- Walk completeness is now checked against the source: "every command the parser registers (read from the source, not from the help) has a capture". Step 1 adds "List the commands the parser registers", and REPORT asks for "the commands the parser registers beside the screens captured".
- The checks fail while the values are open, as skill step 9 (c-8) allows: "OLD and NEW are the values recorded by the baseline check; this check fails while either is missing." and "This check fails while NEW or OLD is still unknown."

### Blocker 3: CONSTRAINTS conflicted with running the build and tests, and untracked output could break Rename only. CLOSED.

- The constraint now allows the runs and fences the output: "write nothing outside `<scratch>` except the output of the project's own build and test commands, which you may run (steps 1, 2 and 5); that output must land in paths the repository ignores."
- Output that does not land in ignored paths is a stop, not a silent failure: "A build or test run leaves a file that git shows as untracked or modified, other than the help strings you edited. Don't delete or revert it; report which file."
- Step 5 lists changed files, and Rename only reads `git status --short`, so a stray file shows up.

## The three questions, on the revised draft

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? No for every check that carries the GOAL.
   - Help matches needs a root capture and the export screen: "every capture is non-empty ... the captures include the root screen and the screen that documents the export flag ... the export flag's screen contains NEW". It fails while OLD or NEW is missing.
   - Baseline found needs a hit: "the captures contain OLD at least once, and the report quotes each hit with its screen and line". Together, Baseline found and Help matches cannot both pass with zero edits.
   - Tests unchanged cannot pass on zero tests: "it runs at least one test ... If the project has no test command, or the command runs no tests, this check is NOT RUN." Zero tests is NOT RUN, not PASS, and this is a guard, not the GOAL's check.
   - Non-blocking: Rename only passes with zero hunks ("every line starts with \" M\"" and "in every changed hunk"), but Help matches and Baseline found cannot pass without an edit, so the GOAL is not skipped.
2. Does any STOP AND ASK condition already hold, given the draft and the log? No.
   - "The working directory is not a git repository, or holds no source for the CLI." The log records the run starts "Inside the CLI's own git repository".
   - "NEW or OLD can't be settled ..." and "The baseline captures don't contain OLD. The premise is wrong." depend on code nobody has read yet. Nothing in the draft or log says they hold.
   - The remaining stop lines (a changed test, an untracked build file, a repeated failure, OLD in a shared constant) depend on the run.
3. Is every file, record and system the steps need located, or listed as UNKNOWN? Yes, with one soft spot.
   - The source, NEW and OLD are three separate UNKNOWN lines, the maximum the skill allows: "UNKNOWN: where the CLI's source lives.", "UNKNOWN: the export flag's current name, called NEW below.", "UNKNOWN: the export flag's previous name, called OLD below."
   - The decision log is located: "`docs/discovery/export-flag-help-text.md`", and the draft says a missing file is not a stop.
   - `<scratch>` is defined: "`<scratch>` is a temporary folder outside the repository."
   - The build and test commands are found by the steps, with a defined fallback: "build the CLI with the project's own build command if it needs one" and "Find the project's test command (README, build file or script definitions) ... If there is no test command, note that." The test command falling back to NOT RUN means a missing one does not skip the GOAL. A CLI that cannot be built or run is caught by "The same check fails twice with the same cause."

## Non-blocking observations (no instance in the sources, so not counted)

- Rename only passes on one wrong result. If OLD is a prefix of another flag, a blind substring replacement turns that flag into NEW plus its tail. Replacing NEW by OLD in the added lines then restores the removed line, and Help matches ignores longer names ("a longer flag name that merely starts with OLD doesn't count"). The draft says "Replace OLD with NEW", not "whole flag tokens only". Nothing in the log or draft says such a flag exists.
- Wrapping: "without line wrapping where the CLI lets you set that" leaves a split OLD possible on a CLI that cannot turn wrapping off. Step 5 searches the source for remaining OLD, which partly covers it.

## Open or new blockers

none

Count: 0
