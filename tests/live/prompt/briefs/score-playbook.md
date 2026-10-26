<!-- Playbook scorer: grades two versions of the /prompt skill against the frozen rubric in one run. Fill {REPO}, {SKILL_A}, {SKILL_B}, {OUT}. The lead copies each version's skill folder (SKILL.md plus every file it links) to A or B at random and keeps the key. Frozen 2026-10-25. -->

You are an independent reviewer. Read-only: do not edit any repository file. Judge for yourself; nobody's conclusions are given to you. Do not try to work out which version or run produced a file.

Two versions of a Claude Code skill, "Skill A" in {SKILL_A} and "Skill B" in {SKILL_B}, each tell Claude how to write a ready-to-run prompt for a coding agent. Read each folder's SKILL.md and every file it links. Grade both against the rubric in {REPO}/tests/live/prompt/rubrics/playbook.md, items P1 to P47. For each item, read the playbook section named in the last column with `python3 -I tools/section.py <id>`, run from {REPO}. Never read playbook/agent-harness-playbook.md whole.

For each item and each skill, give one grade:
- PASS: the skill requires the recommendation.
- PARTIAL: it requires part of it, or only in some cases.
- MISSING: it says nothing.
- CONFLICT: it requires the opposite.
- N/A: the item does not apply to writing a prompt. Use the same N/A decision for both skills.
Quote the skill (step number, under 25 words) for every grade other than MISSING and N/A.

Scoring: PASS 1, PARTIAL 0.5, MISSING and CONFLICT 0; N/A is excluded. Give each skill's total, maximum and percentage, and a sub-score per group (Laws, Lifecycle and delegation, Verification, Guardrails and loops, Templates, Evidence). Also list anything either skill requires that the playbook does not support.

Write the full table (item, Skill A grade, Skill A quote, Skill B grade, Skill B quote) and the scores to {OUT} with the Write tool. Create no other file. Reply with only the two skills' score lines.
