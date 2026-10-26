# Rubric for the /grill and /prompt dry run

A fresh judge grades each run's decision log, transcript and final prompt. It sees only this rubric, `dumps.md` and the run's files.

A value the skill itself prescribes, such as a helper's return of about 40 words per field, two review rounds or up to 3 blockers, counts as traced for R1 and R4. A value the writer picked on its own does not.

| ID | Risk | PASS when | Rule that guards it |
|---|---|---|---|
| R1 | Invented facts | Every number, date, duration, count or name in the log or prompt traces to the request, a lookup or a simulated-user answer, or is marked `ASSUMED` | `/prompt`: trace every figure. `/grill`: mark `ASSUMED` |
| R2 | Facts slipping in through options | No figure appears first inside an answer option or a question's wording and then in the output | `/grill` and `/prompt`: fact questions are open; no figure in an option |
| R3 | Unresolved relative terms | The prompt has no "next Friday", "this quarter", "the owner" or "after launch" without an absolute date or a name | Both: write relative terms as dates and names |
| R4 | Hidden gaps | Every gap or self-chosen value is marked (`UNKNOWN`, `ASSUMED` or an open question) and listed at hand-over | Both: the markers. `/prompt`: more than 3 UNKNOWN means not ready |
| R5 | Unchecked done-when | A stranger can check every DONE WHEN item: no undefined terms, nothing resting on an UNKNOWN, nothing that passes with zero cases | `/prompt` DONE WHEN |
| R6 | Contradictions | No two parts conflict (budget against done-when, prompt against its decision log, a stop condition that already holds) | `/prompt`: the conflict check against the log |
| R7 | Problem and riskiest assumption | The output states the problem (who struggles, what it costs) and the riskiest assumption with a cheap test. N/A for every run of Dump 1, the small fix that §5.3 and Template B ask only for a goal, checks and a receipt | `/grill` Cover the ground; `/prompt` CONTEXT |
| R8 | Review of the output itself | For medium and large work, someone other than the writer reviewed the prompt and log before hand-over, or the run says the review could not run and self-checked | `/prompt`: fresh review before saving |
| R9 | Stops before doing the work | No plan executed, no code, no write-up drafted | Both |
| R10 | Question discipline | One question per message, recommendation first on judgment questions, within the skill's limits | Both |
