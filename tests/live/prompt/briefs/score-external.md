<!-- External scorer: grades two versions of the /prompt skill against research/prompt-skill-sources.md in one run. Fill {REPO}, {SKILL_A}, {SKILL_B}, {SAMPLES_A}, {SAMPLES_B}, {OUT}. Each samples folder holds four prompts written with that version, for the same four tasks. The lead assigns A and B at random and keeps the key. Frozen 2026-10-25. -->

You are an independent reviewer. Read-only: do not edit any existing file. Judge for yourself; nobody's conclusions about either skill are given to you. Do not try to work out which version or run produced a file.

Two versions of a Claude Code skill, "Skill A" in {SKILL_A} and "Skill B" in {SKILL_B}, each tell Claude how to write a ready-to-run prompt for a coding agent. Read each folder's SKILL.md and every file it links. Each skill also has four prompts it produced, for the same four tasks: {SAMPLES_A} for Skill A and {SAMPLES_B} for Skill B. Read them all.

The guidance to score against is {REPO}/research/prompt-skill-sources.md. It lists G1 to G29 (Anthropic's own guidance) and R1 to R9 (research), each already checked against its source. Read nothing else.

For each skill:
1. Grade each G item on two layers, PASS / PARTIAL / MISS / CONFLICT / N/A:
   - Skill: does the skill's text, read as a prompt for Claude, follow the recommendation itself (especially G1 to G10, G22, G28 and G29), or require it of the prompts it writes (G11 to G27)?
   - Output: do its four sample prompts show it?
   Give a short quote for every grade other than PASS.
2. For each R item, state the design implication for a prompt-writing skill in one line. Use the same line for both skills. Then grade whether each skill acts on it (PASS / PARTIAL / MISS / N/A), with a quote.
3. Score: PASS 1, PARTIAL 0.5, MISS and CONFLICT 0; N/A is excluded. Give totals, maxima and percentages for the skill layer, the output layer and research. The overall is the mean of the three percentages, weighted equally.
4. Name the three changes that would most raise each skill's score.

Write the full grading to {OUT} with the Write tool. Create no other file. Reply with only the two skills' score lines.
