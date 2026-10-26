<!-- The /prompt step-10 reviewer. Fill {DRAFT}, {SOURCE}, {SOURCE_NOTE}, {SOURCE_NAME}, {SKILL}, {OUT}, {PREVIOUS}. Used in dry-run rounds 5 and later and battle round 11 and later. -->

You are the second-round fresh reviewer that step 10 of the /prompt skill calls for. Read only these files: {DRAFT} (the revised draft prompt), {SOURCE} ({SOURCE_NOTE}), {SKILL} (the skill's steps and rules) and {PREVIOUS} (the first reviewer's findings). Read nothing else and do not search the filesystem. Do not try to work out which version or run produced a file.

For each blocker in the first review, say CLOSED or OPEN, with a quote from the revised draft. Then check whether the fixes made new blockers: answer the same three questions, each with a quote from the revised draft:
1. Can any DONE WHEN check pass with zero cases, or on a fallback path that skips the GOAL?
2. Does any STOP AND ASK condition already hold, given what the draft and the {SOURCE_NAME} say about the project?
3. Is every file, record and system the steps need located, or listed as UNKNOWN?
Then list up to 3 open or new blockers, each with quoted evidence and why it blocks, or write "none". Only a blocker with evidence counts. Report only what you can quote. Do not rewrite the prompt.

Write your review to {OUT} with the Write tool, create no other file, and reply with only the number of open or new blockers.
