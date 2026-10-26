GOAL
Each night, triage new issues labelled bug and post a reproduction note on each.

DONE WHEN
1. Every new issue labelled `bug` since the last run has a comment from the agent by 07:00.
2. The run log in ticket `OPS-12` has one status line per issue, or "no change" when there were none.
3. Given an issue with no reproduction steps, when the run reaches it, then it is listed under NEEDS A HUMAN.

CONSTRAINTS
- Read-only on the code: never push, merge or close an issue.

BUDGET
- At most 20 issues and 30 minutes per run.

STOP AND ASK IF
- nobody is there to answer, so skip the item and list it under NEEDS A HUMAN

HOW TO WORK
1. One issue per pass; write "no change" when nothing changed.
2. Stop when every new issue is handled or the budget runs out.
3. After two failures with the same cause, skip the item and list it under NEEDS A HUMAN.

REPORT
PASS, FAIL or NOT RUN for each DONE WHEN item, with the command or link. NOT RUN is not PASS.
