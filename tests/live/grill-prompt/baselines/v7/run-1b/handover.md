# Hand-over (step 12)

The prompt is saved at <run folder>/prompt.md.
Edit these parts if they don't match your intent: GOAL, DONE WHEN and STOP AND ASK IF. They carry your judgment (scope, proof and when to stop).
Start a fresh session inside the CLI's own git repository and say: "run the prompt in <run folder>/prompt.md".
It passed a fresh review (two rounds, no open blockers). It has exactly 3 UNKNOWN lines, so it is ready to run, but it can only finish once the session finds the source, NEW and OLD.
Step 9's check left one WARN (c-6, "steps 1, 2 and 5" in CONSTRAINTS). It is a reference to steps, not a figure, and I left it because the review was closed.

Confirm these knowingly:

- ASSUMED: readers copy the flag name from --help, so a stale name sends them to the wrong flag. The request doesn't say who they are or what the stale text has cost them.
- ASSUMED: the parser already defines the export flag under its new name, and only the help text lags. The request says the flag was renamed.
- ASSUMED: the changes stay uncommitted for review, because the request doesn't ask for a commit.
- ASSUMED: no helpers or sub-agents are used.
- ASSUMED: stop after two failed attempts at the same check with the same cause.
- UNKNOWN: where the CLI's source lives. The request doesn't say and the decision log records no answer. The decision log does record that the session that runs this prompt starts inside the CLI's own git repository, so step 1 finds the source from the working directory.
- UNKNOWN: the export flag's current name, called NEW below. The request and the decision log don't give it. Step 1 reads it from the parser.
- UNKNOWN: the export flag's previous name, called OLD below. The request and the decision log don't give it. Step 1 reads it from the help text as it is now.
