Risk: trivial

# Prompt: point the README's install link at the current install page

GOAL: The install link in README.md opens the current install page.

DONE WHEN:
1. Given README.md, when you fetch the install link's URL exactly as the file writes it (`curl -sIL <url>`), then the last response is a success, not a 404. Read the URL from the file, not from your notes, so a link fixed only elsewhere can't pass.
2. Given the same file, when you search it for the old docs host, then it finds nothing.

CONSTRAINTS:
- Edit only that link in README.md.
- A test that looks wrong is reported, not edited.
- When both checks pass, stop and report; add nothing else.

BUDGET: ten minutes, no helpers.

STOP AND ASK IF: you can't find the current install page, or other files link to the old docs host.

HOW TO WORK: build, verify, report.

REPORT: each DONE WHEN item as PASS, FAIL or NOT RUN with its command. NOT RUN is not PASS.

ASSUMPTIONS:
- UNKNOWN: the current install page's URL; the request doesn't give it, so find it on the docs site first.
