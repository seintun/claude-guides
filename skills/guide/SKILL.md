---
name: guide
description: Route an agent-orchestration request to the claude-guides playbook and load only the sections it needs. Use for starting from a vague idea, a new feature, bug fix, refactor or migration, setting up a harness or hooks, code review by an agent, an overnight loop, a stuck or looping agent, a cost blowup, multi-repo or parallel work, onboarding a repo, writing an agent-ready issue, or a retro.
argument-hint: <what you are trying to do>
allowed-tools: Read, Bash(git -C:*), Bash(python3 -I:*), Bash(curl -fsSL https://raw.githubusercontent.com/*)
---

The guide is a separate folder of advice; call it GUIDE. The work happens in the current project, never in GUIDE.

1. Find GUIDE: run `git -C "${CLAUDE_SKILL_DIR}" rev-parse --show-toplevel`. If that prints a folder holding `ENTRY.md`, GUIDE is that clone. Otherwise (the skill was copied in by `npx skills add`, or another agent fetched this file) GUIDE is `https://raw.githubusercontent.com/<owner>/<repo>/main`, with `<owner>/<repo>` taken from the repository link the user gave, else from the `CLAUDE_GUIDES_REPO` environment variable, else `seintun/claude-guides`. That is remote mode: read files with `curl -fsSL GUIDE/<path>`, or WebFetch asking for the file's full text. <!-- privacy: allow -->
2. Read `GUIDE/ENTRY.md`. It is the only guide file you read in full.
3. Match the request to one row of its scenario router, or to a phase if no row fits. The request: $ARGUMENTS
   If the request is empty or fits no row, ask the user one question that picks a row.
4. Load that row's sections in one call: `python3 -I GUIDE/tools/section.py <ids>`. In remote mode, fetch the row's bundle `GUIDE/routes/row-<n>.md` (or `routes/phase-<n>.md`) instead; for a single id, `GUIDE/sections/<id>.md` (`cs:3` is `sections/cs-3.md`). Open the row's runbook in `GUIDE/wiki/` only if you need its steps or checklist. Never read `GUIDE/playbook/agent-harness-playbook.md` whole.
5. Answer for this project:
   - the row you chose, in one line, and the runner-up if two rows fit;
   - what to do now, as numbered steps drawn from the sections, citing them as §9.5, Template F, and so on;
   - the row's template filled in for this project, when the row names one;
   - the output the row asks for, and the checks that prove it.
   If the row is marked thin, say what the playbook lacks instead of filling the gap from memory.
6. **Log it when real work follows.** If the user goes ahead with the work (not for a quick question), append one dated line to the current project's `docs/decisions.md`: the request, the row and sections chosen, and each decision made, with its reason. Commit it with the work. Raw notes and helper output go to an ignored folder, never the log. Records belong on disk, not only in chat, because recall fades as context fills and sessions forget (Law 4, §8, §14; see `GUIDE/wiki/records.md`).
