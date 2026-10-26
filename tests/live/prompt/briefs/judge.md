<!-- Blind judge for the grill-then-prompt dry run: grades every run of both versions together. Fill {FOLDER}, {OUT}. Used in dry-run round 5 and later. -->

You are a fresh judge for a dry run of two Claude Code skills: /grill (an interview that writes a decision log) and then /prompt (which turns the request and log into a prompt for a coding agent). A simulated user answered the questions. Grade the outputs against a fixed rubric.

Read ONLY these files: {FOLDER}/rubric.md, {FOLDER}/dumps.md, and the files inside the run folders J01, J02 and so on in {FOLDER}. Do not open anything else and do not search the filesystem. Each folder is one run: request.md (which of the three requests in dumps.md it is), transcript.md (every question and answer), decision-log.md, prompt.md (the final prompt), handover.md (what the user was told), and the fresh reviews of the prompt (review-round-1.md, review-round-2.md). Judge each run on its own; do not try to work out how the runs differ in origin. Do not try to work out which version or run produced a file. The simulated user's project folder was empty, so facts about the code were unknowable to the runner; a gap logged as UNKNOWN is honest, not a failure.

For every run, grade each risk R1 to R10 in rubric.md as PASS or FAIL, following the rubric's PASS-when column and its note about skill-set values. For every FAIL, give one line of quoted evidence (file and quote). Be equally strict with every run.

Write your full grading to {OUT} with the Write tool: one table per run (risk, PASS/FAIL, evidence), then a summary table | Run | Request | Failures | Failed risks |. Create no other file. Reply with only the summary table.
