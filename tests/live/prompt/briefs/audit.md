<!-- One-at-a-time contradiction audit of every battle draft, blinded as D01 to D12. Fill {FOLDER}. Used in battle rounds 8 to 12. -->

You are auditing prompts written for Claude coding agents, one at a time. Read ONLY the twelve files D01.md to D12.md in {FOLDER}. Do not open any other file or folder, do not search the filesystem, and do not compare drafts to guess where they came from; judge each on its own. Do not try to work out which version or run produced a file.

Each file holds a task and one prompt meant for a coding agent on a Node 20 service with Postgres, tested with `npm test`. For each prompt, find every internal contradiction: two lines of the same prompt that cannot both be followed. Look specifically for:
- a file a step creates or changes that a constraint or a check forbids;
- helpers, writers or reviewers the steps require beyond what the budget allows;
- time or item arithmetic that overruns a stated cap;
- a check that reads data a step transforms, without saying whether it expects the original or changed form;
- a final step that requires every item while the prompt lets items be skipped;
- a check on CI, a deploy or a PR that does not name which run, commit or PR it reads;
- a deliberate-break check that lets the agent choose the break;
- a word or source cap too small for the fields the prompt asks for;
- any other pair of lines that demand opposite things.
Only count real conflicts you can quote. Also rate over-specification 0 to 3 (0 = as simple as the task allows, 3 = much harder to follow than the task needs), and say whether anything essential for the task is missing (yes/no, and what).

Return exactly: a table | File | Contradictions | Over-spec 0–3 | Missing essential |, then one line per contradiction as "<file>: <quote A> vs <quote B>". Under 650 words.
