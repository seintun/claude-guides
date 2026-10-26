# Review r1: prompt-r0.md against the /prompt skill and the decision log

Sources read: prompt-r0.md (the draft), project/docs/discovery/export-flag-help-text.md (the log), skills/prompt-SKILL.md (the skill). Nothing else.

## Part verdicts

- GOAL: PASS. "Every --help screen of the CLI shows the export flag under its current name (NEW) and none still shows its previous name (OLD)." It is one outcome sentence. A screen that never mentions the export flag cannot "show the export flag", and the log words it as "the new name appears on the export flag's screen". That is a small mismatch, not a blocker.
- DONE WHEN: FAIL. There are 4 checks, which is within the limit, but see blockers 2 and 3 and the answer to question 1. Evidence: "the captures include the root screen and the screen that documents the export flag" with no independent count of screens.
- CONTEXT: PASS. "Riskiest assumption: the parser already defines the export flag under NEW and only the help lags. Cheapest test: read the parser's definition and compare it with the help as it is now (step 1)." The problem line, the riskiest assumption with its cheapest test, and the log path are all present.
- CONSTRAINTS: FAIL. "Don't run the export itself, or anything else that writes outside `<scratch>`, apart from the edits." conflicts with HOW TO WORK step 2, "Run it and record which tests fail". See blocker 3.
- BUDGET: PASS. "Time: one hour from the start." This matches the user's words in the log ("Should take an hour."). "Helpers: none." matches "ASSUMED: no helpers or sub-agents are used." The draft does not show that the walk plus two test runs fit the hour, but the item count and test duration are unknown, so I do not count that against it.
- STOP AND ASK IF: FAIL. The first line already holds. See blocker 1.
- HOW TO WORK: PASS on structure. "6. Write the report." follows five steps, and the steps agree with the other sections except for the conflict in blocker 3. Step 1 ("Find the CLI's source from the working directory.") cannot run if blocker 1 stands.
- REPORT: PASS. "Each DONE WHEN item (help matches, baseline found, rename only, tests unchanged) as PASS, FAIL or NOT RUN, with the command that produced it. NOT RUN is not PASS."

## The three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL? Yes, in three ways.
   - Walk completeness. Help matches reads "capture `--help` for the root command and for every subcommand (found by walking the command tree)", and the only coverage test is "the captures include the root screen and the screen that documents the export flag". A subcommand screen that the walk misses and that still names OLD leaves the check passing while the GOAL's "Every --help screen" is unmet.
   - Tests unchanged. "the same tests fail both times (none, if all pass)" passes when the test command runs zero tests. The draft does not require at least one test to run. Its fallback line, "If the project has no test command, this check is NOT RUN.", does not skip the GOAL, because this check is only a guard.
   - Wrapping. "Capture help ... without line wrapping where the CLI lets you set that". If the CLI does not allow it, the search runs on wrapped text and a split OLD passes, even though the stated purpose is "so a name split across two lines isn't missed".
2. Does any STOP AND ASK condition already hold? Yes. The draft's line "The working directory is not a git repository, or holds no source for the CLI." holds, because the log says "the project root is empty: no source, README, CLAUDE.md, build files or git repository." The second line, "NEW or OLD can't be settled", and the third, "The baseline captures don't contain OLD", follow from the same empty root, since there is no parser to read and no CLI to capture.
3. Is every file, record and system the steps need located, or listed as UNKNOWN? Partly.
   - The source, NEW and OLD are each listed: "UNKNOWN: where the CLI's source lives.", "UNKNOWN: the export flag's current name, called NEW below.", "UNKNOWN: the export flag's previous name, called OLD below."
   - The decision log is located: `docs/discovery/export-flag-help-text.md`.
   - The test command is left to discovery ("Find the project's test command (README, build file or script definitions)"). The log says the project has no README or build files, and the test command is not listed as UNKNOWN.
   - How to build or invoke the CLI to capture `--help` is neither located nor listed as UNKNOWN. Step 1 only says "capture `--help` for the root command and every subcommand".
   - The draft's own line "The session that runs this prompt starts inside the CLI's own git repository" gives a location that the log does not support (blocker 1).

## Blockers

1. A STOP AND ASK condition already holds, and the draft covers it with a claim the log contradicts.
   - Draft: "UNKNOWN: where the CLI's source lives. ... The session that runs this prompt starts inside the CLI's own git repository, so step 1 finds the source from the working directory." Stop line: "The working directory is not a git repository, or holds no source for the CLI."
   - Log: "UNKNOWN: where the CLI's source code lives. The user does not know (asked 2026-10-24), and the project root is empty: no source, README, CLAUDE.md, build files or git repository." Also: "this log is not committed ... because the project root has no git repository".
   - Why it blocks: nothing in the log says where the session starts. The draft states a location as fact, and the log says no source or repository exists where the prompt was made. The skill's step 8 says a stop line that already holds "is settled with the user before saving". The CONTEXT path `docs/discovery/export-flag-help-text.md` also lives in that empty project root, so it may not exist in a repository the run starts in.

2. The checks rest on UNKNOWN values, and the walk's completeness is unchecked.
   - Draft: "no capture contains OLD as a whole flag token ... and the export flag's screen contains NEW", where OLD, NEW and the source are all `UNKNOWN`.
   - Draft: "walking the command tree" with no check of the walk against the parser's registered commands or a count.
   - Why it blocks: the skill says "No check rests on an UNKNOWN". With no source, no check can run. If the source turns up, Help matches can still pass on a partial walk while a screen the walk missed still shows OLD. The GOAL says "Every --help screen".

3. Two lines cannot both be followed unless the project's build and tests write nothing outside `<scratch>`, and the draft does not establish that.
   - Draft CONSTRAINTS: "Don't run the export itself, or anything else that writes outside `<scratch>`, apart from the edits." and "Write working files only to `<scratch>`."
   - Draft HOW TO WORK step 2: "Run it and record which tests fail, if any." Step 5 runs it again. Step 1 runs the CLI to capture help, which may need a build.
   - Draft DONE WHEN Rename only: "every line starts with \" M\" (modified; nothing added, deleted, renamed or untracked)".
   - Why it blocks: a test run or build commonly writes caches or build output into the tree. That breaks the CONSTRAINT, and any untracked output fails the Rename only check even when the help is correct. The draft does not say how to run the tests or build without writing outside `<scratch>`.
