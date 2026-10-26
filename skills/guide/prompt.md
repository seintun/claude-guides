Use my claude-guides guide for this task. GUIDE = {{GUIDE}}. The work happens in this project, not in GUIDE.
1. Read GUIDE/ENTRY.md and pick the one scenario-router row that matches my request below.
2. Load only that row's sections in one call: python3 -I GUIDE/tools/section.py <ids>. Never read the whole playbook. If GUIDE is a web address (no clone), fetch GUIDE/sections/<id>.md for each id instead; cs:3 is sections/cs-3.md.
3. Tell me the row you chose, then the steps for this project citing section ids, the row's template filled in, and the output with the checks that prove it. If the row is marked thin, say what the playbook lacks.
My request: <describe it>
