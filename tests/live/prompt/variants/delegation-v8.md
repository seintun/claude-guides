# Delegation rules for /prompt

Read this when the prompt splits work into batches, uses helpers, or runs unattended. These rules belong to steps 4, 6 and 7 of SKILL.md.

## Batches (step 4)

For large mechanical changes, give each writer a disjoint batch and its own worktree, gate every batch, keep shared config with the lead, and say how writers stay isolated on anything they share (a database, a port, a lockfile) and how old and new tools coexist so the suite stays green. The lead merges batches one at a time, reruns the full suite after each, and reverts a batch that turns it red.

## Helper briefs (step 6, Template C)

Each brief gives the objective and the decision it feeds, what is already ruled out and already decided, where to look, a read-only scope with a cap on files or sources, and a return capped to fit its fields (about 40 words per field), with long output written to a named file and its path returned. Helpers whose results will be compared get the same brief and return the same fields, and each option is judged on the same criteria, not against the others. The lead's synthesis step reads the helpers' files, reconciles conflicts, verifies the claims the decision rests on, reports a near-tie instead of picking silently, and never forwards raw transcripts.

## Loops, schedules and unattended runs (step 7, Template H)

One small action per pass, and running twice sends, charges or creates nothing twice. "No change" when nothing changed; a stop condition; at most 2 failures with the same cause; a cap per run; only the tools and permissions the task needs. Nobody is there to answer, so "stop and ask" becomes: skip the item and list it under NEEDS A HUMAN. Results go to a named sink (a ticket, a PR comment, a file outside the repository), at most 15 lines, most important first, never a new file committed to the repository.
