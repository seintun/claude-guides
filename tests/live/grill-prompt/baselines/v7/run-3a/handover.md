The prompt is saved at <run folder>/prompt.md. It is NOT READY TO RUN: it has 6 UNKNOWN lines, and more than 3 means it is not ready. Settle the four that only you can answer before you start: what "live" means, what the two-week wait costs, the last day of the quarter and the engineer's weekly hours.
Edit the lines that carry your judgment: GOAL, DONE WHEN and STOP AND ASK IF.
Once the gaps are settled, start a fresh session in the project that holds `docs/discovery/customer-onboarding-rebuild.md` and say "run the prompt in <run folder>/prompt.md". This prompt only plans; the build is a separate prompt written after you sign off the plan.
Review: two fresh-review rounds ran. The second round named one blocker (DONE WHEN 5 asked for a sign-off confirmation that no step collected). The fix, a changed step 8 that asks for the confirmation, was not re-reviewed. You decide whether to accept it or have it reviewed in a fresh session.
Two other notes from the reviews, not blockers: the round cap of 2 against a reviewer cap of 1 does not say who runs the second round, and the steps and systems of the contract process are asked at run time, not logged as an UNKNOWN.

ASSUMED (6):
- the plan is written to `docs/plans/onboarding-rebuild.md`
- at most 1 read-only helper and 1 fresh reviewer
- the helper reads at most 30 files
- the helper's return is at most 40 words per field
- at most 2 review rounds before the user decides
- the time ceiling is one working session, because the request gives no number of hours

UNKNOWN (6):
- the exact event that makes a client "live", which ends the one-day count
- where onboarding happens (the code, tools, spreadsheets, tickets and records it touches); the project folder this prompt was written from was empty
- what the two-week wait costs, in revenue, churn, support time or any other term
- the last day of the quarter the request calls "this quarter", as an absolute date; calendar or fiscal is not stated
- how many hours a week the one part-time engineer has for this
- the current elapsed time from the client's signature on the data agreement to live
