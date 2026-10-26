# Claude Guides: start here

Read this first when another project calls this guide, through `/guide`, a CLAUDE.md pointer or a pasted prompt. It routes your request to a few playbook sections, at most one runbook and one template. Never load the whole playbook: it is about 1,500 lines.

## How to use it

1. **Two folders.** GUIDE is the full path of the folder that holds this file. Your project is your current directory. The guide gives advice; your project gets the work.
2. **Find your row** in the scenario router. If none fits, use the phase table.
3. **Load only the row's sections:** `python3 -I GUIDE/tools/section.py 9.5 F` prints §9.5 and Template F, and nothing else. Ids: `9.5` or `17A` for a section, `F` for a template, `law-7` for a law, `cs:3` for the cheat sheet. `--list` lists every id. Template letters are ids too: add them to the same call when you need the artifact the row's output names.
   **No clone?** Fetch `GUIDE/sections/<id>.md` for each id instead (`cs:3` is `sections/cs-3.md`), where GUIDE is `https://raw.githubusercontent.com/<owner>/<repo>/main` from the link you were given. `GUIDE/guide-index.json` holds this router as JSON.
4. **Open the runbook** (`GUIDE/wiki/<name>.md`, about 80 lines) only if you need its steps and checklist.
5. **Produce the row's output** in your project, and follow the rules at the end.

Rows marked **thin** have no full recipe in the playbook. They route to the nearest sections and name the gap; say so to the user instead of filling it from memory. Grades in the sections: (P) primary, (S) second-hand, (R) research, (D) design advice. "Page Lesson N" in a runbook means a lesson of the teaching page, `GUIDE/site/index.html`.

## Scenario router

| # | Scenario | Read (section ids) | Runbook | Template | Output |
|---|---|---|---|---|---|
| 1 | Vague idea or pain point | `5.1 5.2` | [grill](wiki/grill.md), [start-a-task](wiki/start-a-task.md) | K, then L | A decision log from one-question-at-a-time grilling, then sliced issues. No plan or code yet |
| 2 | New feature | `5.3 5.4 6` | [start-a-task](wiki/start-a-task.md), [orchestrate](wiki/orchestrate.md) | B, D | A goal with Done-when checks, a plan file of slices (test and rollback each), then a PR with a receipt |
| 3 | Bug fix (thin) | `5.3 9.1 14 cs:3` | [verify](wiki/verify.md) | L, B (RISK trivial) | An issue whose Today line is the repro and whose Check fails before the fix, then a receipt. Gap: no reproduce-first or root-cause procedure |
| 4 | Refactor (thin) | `5.3 9.3 15 18` | [verify](wiki/verify.md) | D, B | Slices that keep behaviour, with existing or characterization tests green before and after. Gap: only the structure/behaviour split and characterization tests |
| 5 | Migration across many files (thin) | `19.3 11.1 11.3 E` | [run-unattended](wiki/run-unattended.md) | D, E | A per-file pipeline that calls the model only when a check fails, with per-item state and every file gated. The evidence behind it is in `19.1` item 2. Gap: no step-by-step recipe |
| 6 | Set up a harness | `17 17A 3A 18` | [build-a-harness](wiki/build-a-harness.md) | A, E, F, G, M | The next maturity level's pieces, with its "move up when" test |
| 7 | Add hooks (Stop gate full; guard hooks thin) | `9.5 10.2 F G` | [verify](wiki/verify.md), [guardrails](wiki/guardrails.md) | F, G | A settings entry and an executable script; a forced failing test returns exit 2. Gap: PreToolUse guard scripts are one line of prose |
| 8 | Overnight or unattended loop | `11.1 11.3 11.5 10.2 18` | [run-unattended](wiki/run-unattended.md), [guardrails](wiki/guardrails.md) | H, E, B | State files, a stop condition, retry cap and cost ceiling, one status line per pass, results in a file, ticket or PR |
| 9 | Code review by an agent | `9.2 law-7` (add `12.3` for CI) | [verify](wiki/verify.md) | C for a local review by a fresh subagent; M for a CI review | Findings most serious first: correctness bugs and missing or weakened tests. Advisory; it never approves |
| 10 | Research spike | `5.4 7` | [orchestrate](wiki/orchestrate.md) | C | `docs/research/<topic>.md`: findings with file:line or URL and confidence, plus unknowns |
| 11 | Stuck agent (looping, false "done", lost context) | `cs:3 14 4 8 11.3` | [unstick](wiki/unstick.md) | B (RULES) | A diagnosis from the symptom table, the next checkable step or a restart from files, then one rule so it doesn't repeat |
| 12 | Cost blowup (thin) | `18 11.3 11.5` | [run-unattended](wiki/run-unattended.md) | B (BUDGET), H | First find what spent it: read cost from the Console or OpenTelemetry, not `/usage`, and stop the loop or schedule with the kill switch (`18`). Then fan-out caps in the lead's prompt and budget flags on headless runs. Gap: no incident procedure |
| 13 | Work across several repos (thin) | `18 7 12.1` | [orchestrate](wiki/orchestrate.md) | D | One plan file that orders the repos and names each repo's check. Gap: a single bullet in §18 |
| 14 | Onboard a new repo | `8 law-5 17 18` | [build-a-harness](wiki/build-a-harness.md) | A | A short CLAUDE.md with a runnable test command and a map; characterization tests where tests are weak |
| 15 | Write an agent-ready issue | `5.1 law-3` | [start-a-task](wiki/start-a-task.md) | L | Outcome, Today, Where, Check, Boundary, Depends on, Open questions, Risk set by a rule |
| 16 | Retro after a task | `13 law-8 14` | [improve](wiki/improve.md) | I, J | Up to 3 changes with exact text, applied only after a yes; failures saved as eval records |
| 17 | Security review of an agent setup | `10.1 10.3 12.2 12.4` | [guardrails](wiki/guardrails.md) | F (guardrails block), M | Findings grouped as prevent, detect, recover, against §10.3 and §12.4 |
| 18 | Several writers on one codebase (thin) | `7 3A` | [orchestrate](wiki/orchestrate.md) | D, C | One writer per file set, a worktree per builder, one plan file per task. Gap: no merge or integration step |
| 19 | Write a prompt for an agent | `cs:6 cs:7 law-3 9.1` | [/prompt skill](skills/prompt/README.md) | B, C, H | A saved prompt in `GUIDE/prompts/<project>/` with a goal, 2 to 5 checks, a budget, stop-and-ask cases and a receipt. Run `/prompt`, or follow its steps |

## Phase table

Use this when the request is a stage of work, not a scenario. Each phase has a review checklist in [orchestration-index.md](orchestration-index.md).

| Phase | Read (section ids) | Runbook | Template |
|---|---|---|---|
| 1 Shape: is it worth doing? | `5.1 5.2` | [grill](wiki/grill.md), [start-a-task](wiki/start-a-task.md) | K |
| 2 Brief: what counts as done? | `law-3 5.3` | [start-a-task](wiki/start-a-task.md) | B, L |
| 3 Plan: which slices and risks? | `law-6 5.4 14` | [orchestrate](wiki/orchestrate.md) | D |
| 4 Orchestrate: who does what? | `6 7 3A` | [orchestrate](wiki/orchestrate.md) | C |
| 5 Build: is the loop healthy? | `4 8 cs:3` | [unstick](wiki/unstick.md) | B |
| 6 Check: is it really done? | `9 law-2` | [verify](wiki/verify.md) | F, G, M |
| 7 Overnight: can it run without me? | `11 10` | [run-unattended](wiki/run-unattended.md) | E, H |
| 8 Learn: what should never repeat? | `13 law-8 15` | [improve](wiki/improve.md) | I, J |

## Rules that apply everywhere

- **Goal first.** One sentence of result, 2 to 5 Done-when checks a command or a person can run, a budget and a stop-and-ask list. Load `B`.
- **One writer.** One agent edits a set of files. Helpers read, search and review, and return findings with paths. Load `7`.
- **Fresh review.** A reviewer gets the work and the criteria, never your conclusion. Load `law-7`.
- **Receipts.** Mark every check PASS, FAIL or NOT RUN, with its command. NOT RUN is not PASS. Load `9.4`.
- **Two strikes.** If the same check fails twice for the same reason, stop and ask for a second opinion. Load `B`.
- **Reviews end.** Only a blocker with evidence reopens a review, a re-review reads the fix for open and new blockers, only the reviewer or a human closes a blocker unfixed, and after two rounds a human decides. Load `9.2`.
- **Code over words.** Anything that must never happen gets a deny rule, a hook or a gate, not only a sentence. Load `law-9`.
- **Records on disk.** Decisions go to the project's `docs/` and are committed; scratch stays out of git. Open `GUIDE/wiki/records.md`.
- **Loops are bounded.** Every loop needs a stop condition, a retry cap and a cost ceiling. Load `11.3`.

## If you need more

- Pick by phase, with review checklists: [orchestration-index.md](orchestration-index.md)
- One-page cheat sheet: `cs:1` to `cs:7`
- What the evidence says about one agent or many: `19.1 19.3`
- Gaps the playbook knows it has: `18 19.4`
- Every section id: `python3 -I GUIDE/tools/section.py --list`
