Risk: low

# Prompt: make the CLI's --help name the renamed export flag

GOAL: Every `--help` screen names the export flag by its current name.

DONE WHEN:
1. Given the built CLI, when you run `cli --help` and the export subcommand's `--help`, then both name the new flag and exit 0.
2. Given the same screens, when you search them for the old flag name, then it finds nothing.

CONSTRAINTS:
- Edit only help text. Copy the wording style of the other flags' help.
- If the help is generated from the parser, stop and ask before changing the parser.
- A test that looks wrong is reported, not edited.
- When both checks pass, stop and report; add nothing else.

REPORT: each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.

ASSUMPTIONS:
- UNKNOWN: the new flag's name; the request doesn't give it, so read it from the parser first.
