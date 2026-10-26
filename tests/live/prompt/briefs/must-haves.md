<!-- Must-haves check of every battle draft, blinded as D01 to D12. Fill {FOLDER}, {MUST_HAVES}, {OUT}. Added for the v7 against v8 comparison (battle round 12). -->

You are checking prompts written for Claude coding agents against a fixed list of must-haves. Read ONLY {MUST_HAVES} and the twelve files D01.md to D12.md in {FOLDER}. Do not open any other file or folder, do not search the filesystem, and do not compare drafts to guess where they came from; judge each on its own. Do not try to work out which version or run produced a file.

Each file holds a task (its scenario is named at the top) and one prompt. For every draft, take the must-haves listed under its scenario and mark each PRESENT or ABSENT:
- PRESENT means a DONE WHEN check, a CONSTRAINT or a HOW TO WORK step requires it. Quote the line, under 25 words.
- A mention in CONTEXT or a hope ("ideally", "if possible") is ABSENT. Say in one line what is missing.
Judge only what the text requires, not what a capable agent might do anyway.

Write to {OUT} with the Write tool: one table per draft, | Must-have | PRESENT or ABSENT | Quote or what is missing |, then a summary table | File | Scenario | Present | Absent |. Create no other file. Reply with only the summary table.
