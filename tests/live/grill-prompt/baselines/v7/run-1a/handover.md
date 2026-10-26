# Handover (step 12)

The prompt is saved at `<run folder>/prompt.md`. Review: passed after two rounds with a fresh reviewer.
Edit these parts if they do not match your intent: GOAL (the help names the new flag and never the old one, with no behavior change), DONE WHEN (four checks) and STOP AND ASK IF.
Start a fresh session in the repository that holds the CLI, with: "run the prompt in <run folder>/prompt.md". Started anywhere else, it stops with BLOCKED.

Confirm these lines knowingly:

- UNKNOWN: where the CLI's source lives. The user did not know when asked on 2026-10-24.
- ASSUMED: the rename is finished in the parser and the new name is final.
- ASSUMED: the failure cases are every place the help output names the old flag: the usage line, example lines, other flags' descriptions and each command's help.
- ASSUMED: a test or stored copy of the help output that fails after the fix is regenerated from real output; no other test is edited.
- ASSUMED: the retry cap is 2 failed attempts at the same check.
