# Prompt: make the CLI's --help match the renamed export flag

Start this session in the repository that holds the CLI.

UNKNOWN: where the CLI's source lives. The user did not know when asked on 2026-10-24.
ASSUMED: the rename is finished in the parser and the new name is final.
ASSUMED: the failure cases are every place the help output names the old flag: the usage line, example lines, other flags' descriptions and each command's help.
ASSUMED: a test or stored copy of the help output that fails after the fix is regenerated from real output; no other test is edited.
ASSUMED: the retry cap is 2 failed attempts at the same check.

## GOAL

The CLI's `--help` output, for the main command and for every command that takes the export flag, names that flag by its new name and never by its old name, and the CLI behaves exactly as before.

## DONE WHEN

1. Help check. Given the list of commands written down in HOW TO WORK step 3 (the main command, plus every command whose parser definition accepts the export flag), when you run `<cli> <command> --help` for each, then the output has at least one match for `<new-name>` and none for `<old-forms>`. Command, per listed command: `<cli> <command> --help | grep -c -e <new-name>` prints a count above zero, and `<cli> <command> --help | grep -ci <old-forms>` prints 0. The list holds at least the main command.
2. Only help text changed. Given the changes are left uncommitted, when you run `git status --short` and `git diff -U0 HEAD` from the repository root, then no line of `git status --short` starts with `??`, and every changed line is help text the CLI prints (a help string, a usage line or an example) or, in the stored copy of the help output, a line regenerated from real output. No changed line defines or handles a flag: its name, aliases, default or behaviour.
3. Tests. Given the test command found in HOW TO WORK step 1, when you run it, then it exits 0 and reports at least one test run, and `git diff --name-only --diff-filter=MD HEAD` lists no test file other than the stored copy of the help output. If the repository has no test command, this check is NOT RUN with that reason, and checks 1, 2 and 4 decide the goal.
4. Other mentions are listed. Given `git grep -n -i <old-forms>` run from the repository root before the edit (it must have at least one hit in a help-text file, which shows the search covers the right place), when you run it again after the edit, then no hit is in a help-text file, and every hit's file and line is in the report's list of other places.

## CONTEXT

- Problem: anyone who runs the CLI's `--help` sees the export flag under its old name after the rename. The request does not say who they are or what it has cost them.
- Riskiest assumption: the rename is finished in the parser and the new name is final. Cheapest test: confirm the parser accepts `<new-name>` (HOW TO WORK step 2).
- Terms:
  - `<cli>` is the CLI's executable, run as the repository documents.
  - `<new-name>` is the export flag's current spelling as the parser accepts it, with its leading dashes.
  - `<old-name>` is the spelling before the rename, found in step 2.
  - `<old-forms>` is the grep options `-e <pattern>`, one for each form the old flag takes in the help text or the parser: the dashed form, the underscore form, an upper-case placeholder, and any short alias. Each pattern is written to match only the old flag, not other flags. The checks match without regard to case.
  - A help-text file is a file that defines text the CLI prints for `--help`; it may be the same file as the parser definitions.
  - The stored copy of the help output is a snapshot or golden file of that output, if the repository has one.
- Prior decisions: `docs/discovery/cli-help-rename.md`, if the repository has it. This prompt carries the same decisions.

## CONSTRAINTS

- Change only help text, and the stored copy of the help output. If the help output is generated (from the parser or from a template), change its source and regenerate; never hand-edit a generated file.
- Change no flag behaviour: names, aliases, defaults, what a flag does. Help text may sit in the same file as the parser definitions; edit only the text.
- Leave every other place that names the old flag (README, man page, shell completions, example scripts) alone. List each by file and line in the report.
- If you notice other flags whose help has drifted, report them; do not fix them.
- Edit no test, except to regenerate the stored copy of the help output from real output with the CLI's own mechanism. Never hand-edit that copy.
- Never run a real export, and install nothing. Do not commit, push or change branch.
- Cover as requirements: every place the help output names the old flag (usage line, example lines, other flags' descriptions, each command's help), in any spelling or case.

## BUDGET

One hour, from the start of the run. Stop and report what is done and what is not when it runs out. No helpers: one agent does all the work. Stop at the retry cap.

## STOP AND ASK IF

- The working directory is not the CLI's repository: no command-line parser and no help text found, or it is not a git repository. Stop with BLOCKED and say where you looked.
- Before editing, the parser rejects `<new-name>`, or no help output matches `<old-forms>`. The premise does not hold.
- You cannot tell, with evidence from the help text or the repository's history, which spelling was the old name, or more than one flag could be it.
- The test command already fails before you edit, or the time left would not fit one run before the edit and one after.
- The fix would need a change outside CONSTRAINTS: flag behaviour, or a test other than the regenerated stored copy.
- A check fails again with the same cause at the retry cap.

## HOW TO WORK

One slice, one writer, no plan file. Leave the changes uncommitted.

1. Confirm you are in the CLI's repository: a command-line parser and help text are present, and `git rev-parse --show-toplevel` succeeds. Find the test command in the README, CI config or package scripts.
2. Find `<new-name>` in the parser. Find `<old-name>`: the help text names an export flag the parser does not accept, or the repository's history of the rename shows it. Then list every form the old flag takes in the help text and the parser, and write them as `<old-forms>`. Confirm the parser accepts `<new-name>`: read its definition, and where the CLI offers a way to run it with no side effects (a dry run, for example), run it once with the new name.
3. Write down, in your report notes: the list of commands for check 1, `<old-forms>`, the help-text files, the stored copy of the help output if any, and the test command. Before editing, run the test command, check 1 and check 4's `git grep`. Check 1 must match `<old-forms>` in at least one help output (red). If it does not, stop.
4. Edit the help text: wherever the help output names the old flag, in any of the `<old-forms>`, use `<new-name>`, and word each line to describe the flag as the parser accepts it. If the help is generated, edit the source and regenerate.
5. Re-run checks 1 to 4. If the stored copy of the help output fails, regenerate it from real output and re-run. Fix and retry up to the retry cap.
6. Write the report. Do not commit.

## REPORT

Each DONE WHEN item as PASS, FAIL or NOT RUN with its command and the printed counts. NOT RUN is not PASS. Then:

- `<new-name>`, `<old-name>`, `<old-forms>` and how you found each.
- The list of commands checked.
- The files changed, each with the class of its changes (help text, or stored copy regenerated).
- The result of step 3 before the edit: the old-form counts, the `git grep` hits and the test result.
- The other places that name the old flag, by file and line.
- Other flags whose help seems to have drifted, if you noticed any.
- What is not finished, if the budget ran out.
