# Hand-over (step 12)

The prompt is saved at `prompt.md` in this run folder (it stands in for the guide's `prompts/<project>/` folder).

Edit these parts, because they carry your judgment: GOAL (the Move, Stay or Wait rule), DONE WHEN (checks 2 and 3 especially) and STOP AND ASK IF.

It is NOT READY TO RUN: it has 5 UNKNOWN lines, more than 3. When you start a fresh session with "run the prompt in prompt.md", its first step asks you for the missing inputs, so have the CI configuration, the bill and usage, the GitHub plan and the deadline date to hand.

Review status: two review rounds ran and the second found one blocker (step 5 did not give the reviewer the helper files, your reply to step 1 or the CI configuration). That fix, in step 1 and step 5, was made after the last review and was not re-reviewed. Per the skill, you decide whether it stands or needs another review.

ASSUMED:
- ASSUMED: at most 3 helpers.
- ASSUMED: at most 8 pages read per vendor.
- ASSUMED: a helper's return is capped at 40 words per field.
- ASSUMED: "build time" means wall-clock time from a push to the last check finishing on the monorepo's main pipeline.

UNKNOWN:
- UNKNOWN: location of the monorepo, its CI configuration and its run history (the project folder is empty).
- UNKNOWN: where the GitHub Actions bill and the usage behind it (for example minutes used, the number of people who use CI and the most builds that ran at once) can be read.
- UNKNOWN: the monthly CI spend; you do not know it.
- UNKNOWN: which GitHub plan the team is on, which sets the Actions prices and allowances that apply.
- UNKNOWN: the deadline's calendar date, 2026-10-30 or 2026-11-06; the request gave only a relative weekday.
