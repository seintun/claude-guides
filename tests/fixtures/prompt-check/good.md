Risk: normal

# Prompt: fix the stale export flag in the CLI help

## GOAL
Every `--help` output names the export flag by its current name.

## DONE WHEN
1. Given the CLI, when you run `cli --help`, then the output names the new flag and exits 0.
2. Given the same command, when you search the output for the old name, then it finds nothing.

## CONTEXT
- Problem: users copy the old flag from the help and the command fails.
- Riskiest assumption: the help is hand-written. Cheapest test: search the source for the usage string.
- UNKNOWN: where the help text lives; the request names no file.
- ASSUMED: the change stays uncommitted.

## CONSTRAINTS
Edit only the help file.

## BUDGET
About an hour. ASSUMED: no helpers.

## STOP AND ASK IF
The help is generated from the parser.

## HOW TO WORK
1. Find the help file.
2. Fix it, then run checks 1 and 2.

## REPORT
Each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.
