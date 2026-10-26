# Review r1: prompt-r0.md

Read only: prompt-r0.md, docs/discovery/cli-help-rename.md, prompt-SKILL.md.

## Part verdicts

- GOAL: PASS. "names that flag by its new name and never by its old name, and the CLI behaves exactly as before." One sentence, an outcome.
- DONE WHEN: FAIL. CONSTRAINTS require "in any spelling or case", but check 1 is "`<cli> <command> --help | grep -c -e <old-name>` prints 0" and check 4 is "`git grep -n -e <old-name>`", both one case-sensitive spelling (see blocker 1). The other points hold: 4 checks, commands given, zero-case guards "The list holds at least the main command", "reports at least one test run", "it must have at least one hit in a help-text file".
- CONTEXT: PASS. "Riskiest assumption: the rename is finished in the parser and the new name is final. Cheapest test: confirm the parser accepts `<new-name>` (HOW TO WORK step 2)." Terms are defined, and the decision log is cited as a path.
- CONSTRAINTS: PASS. "Change only help text, and the stored copy of the help output." No line contradicts another or the decision log (decision 2 is carried by "Leave every other place that names the old flag ... alone. List each by file and line in the report.").
- BUDGET: PASS. "One hour, from the start of the run." and "No helpers: one agent does all the work." One hour is traced to the request ("should take an hour"). The retry cap is tagged "ASSUMED: the retry cap is 2 failed attempts at the same check."
- STOP AND ASK IF: PASS. First line: "The working directory is not the CLI's repository ... Stop with BLOCKED and say where you looked." It covers the premise, an ambiguous old name, a failing baseline and the retry cap. See question 2 for the one line that holds today.
- HOW TO WORK: PASS. "One slice, one writer, no plan file. Leave the changes uncommitted." Step 3 runs a red baseline before the edit. The steps do not contradict the other sections.
- REPORT: PASS. "Each DONE WHEN item as PASS, FAIL or NOT RUN with its command and the printed counts. NOT RUN is not PASS."

## The three questions

1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
   - Check 1 cannot pass on an empty list: "The list holds at least the main command."
   - Check 3 cannot pass on zero tests: "exits 0 and reports at least one test run."
   - Check 4's pre-edit search must hit: "it must have at least one hit in a help-text file".
   - Check 2 does pass on an empty diff: "no line of `git status --short` starts with `??`, and every changed line is help text". With no changes there are no changed lines. Checks 1 and 4 and the step 3 red baseline ("Check 1 must show `<old-name>` in at least one help output (red). If it does not, stop.") carry the goal, so this is not a blocker.
   - The only fallback is "If the repository has no test command, this check is NOT RUN with that reason, and checks 1, 2 and 4 decide the goal." Check 1 is the goal check, so the fallback does not skip the GOAL.
   - A check that can pass while the goal is unmet: check 1 and check 4 on any spelling or case other than the single `<old-name>` (blocker 1).

2. Does any STOP AND ASK condition already hold?
   - Yes, for the project folder as the log describes it. The log says "the folder is empty and is not a git repository", and the first stop line reads "no command-line parser and no help text found, or it is not a git repository."
   - It is settled with the user in the log's decision 3 ("run from the repository that holds the CLI, and stop with BLOCKED if no parser and no help text are found there"), and the draft's opening line is "Start this session in the repository that holds the CLI." So I do not count it as a blocker.
   - Residual tension, not counted: decision 3's reason says "the person starting the run knows which repository holds the CLI", while the log's Open questions say "the user said 'I don't know'". If the starter cannot name the repository, the run ends at BLOCKED.
   - No other stop line holds on what is known now.

3. Is every file, record and system the steps need located, or listed as UNKNOWN?
   - The CLI's source: "UNKNOWN: where the CLI's source lives. The user did not know when asked on 2026-10-24." This is one UNKNOWN line, within the limit of 3.
   - Found at run time by steps 1 to 3, with a stated no-find path, not listed as UNKNOWN:
     - the test command, with a NOT RUN path when absent;
     - the stored copy of the help output ("if the repository has one");
     - the parser, the help-text files and the rename history.
   - The decision log is cited as "`docs/discovery/cli-help-rename.md`, if the repository has it". The log itself says "No git repository exists in the project", so it is not in the CLI repository. "This prompt carries the same decisions" covers the gap.
   - Not stated: where the report goes. "Write the report." names no sink, and check 2 forbids untracked repository files, so chat is implied.

## Not counted as blockers (could not be shown from the text; listed for the owner)

- Check 1 and check 4 use a plain `grep -e <old-name>` with no word boundary. If the old spelling is a prefix of the new one, the old-name check cannot reach 0. That would fail loudly at the retry cap, not pass silently.
- Check 1 requires "at least one match for `<new-name>`" for "the main command" unconditionally. The log says "every subcommand that takes the export flag", so the CLI has subcommands. If the main command's help does not name the export flag, a correct result would fail check 1. The log's decision 1 supports the draft's wording, so I left it.
- CONTEXT admits a gap, "The request does not say who they are or what it has cost them.", without an UNKNOWN tag. The log marks it "Not asked: the fix is the same either way."

## Blockers

1. The "any spelling or case" requirement is not enforced by any check, so DONE WHEN can pass while the GOAL is unmet.
   - Evidence: CONSTRAINTS: "every place the help output names the old flag (usage line, example lines, other flags' descriptions, each command's help), in any spelling or case." Check 1: "`<cli> <command> --help | grep -c -e <old-name>` prints 0". Check 4: "`git grep -n -e <old-name>`". CONTEXT: "`<old-name>` is the spelling before the rename, found in step 2."
   - Why it blocks: `<old-name>` is one spelling, and grep -e is case-sensitive. A help line naming the old flag in another case or form (an upper-case metavar, an underscore form, a short alias) leaves both counts at 0 and all four checks PASS. The GOAL's "never by its old name" would then be unmet. The draft asks for the coverage but no check can show it.
   - Reference: SKILL step 5, "could this pass while the goal is unmet?"; step 8, "Make each check inspect exactly its claim."

Blocker count: 1
