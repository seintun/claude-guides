# Claude Code cheat sheet

Companion to `agent-harness-playbook.md`. Command names change between releases; type `/` or `/help` to see what your version supports.

## 1. Which surface

| Surface | Use it for | Gives up |
|---|---|---|
| Terminal (`claude`) | Newest features first, scripting (`claude -p`), worktrees (`claude -w`), `--cloud`, teleport, Remote Control | Diff pane, browser, visuals |
| Desktop, Code tab | Control room: many sessions side by side, built-in browser, artifacts, task lists, splitting work into new sessions, phone follow-along | Some CLI-only commands (`/permissions`, `/config`) |
| VS Code extension | Reading and reviewing diffs inline, shared file and selection context, small edits while you code | Running many sessions in parallel |
| claude.ai/code and phone | Unattended cloud runs, steering from anywhere | Local files, unless you use Remote Control |

Default: Desktop as the control room, Terminal for scripts and CLI-only features, VS Code when reading code line by line. All of them share `~/.claude` (CLAUDE.md, skills, hooks, agents), so switching costs nothing.

## 2. Commands

| Need | Command |
|---|---|
| Side question without derailing | `/btw <question>` |
| What fills the context | `/context` |
| Shrink context, keep a focus | `/compact <focus>` |
| Start clean | `/clear` |
| Cost | `/usage` |
| Plan before building | Shift+Tab to plan mode |
| Interrupt | Esc |
| Go back to an earlier turn | Esc Esc, or `/rewind` |
| Continue or pick a session | `claude -c`, `/resume` |
| See running sessions | `claude agents`, Desktop sidebar, or ask "list current sessions and their status" |
| Manage subagents | `/agents` |
| Repeat a prompt in this session | `/loop` |
| Cloud runs on a timetable | `/schedule` |
| Keep going until a condition holds | `/goal <condition>` |
| Split mechanical changes into many PRs | `/batch` |

## 3. Stuck signs and fixes

| Sign | Fix |
|---|---|
| Same error twice | Stop it. Ask for 3 ranked hypotheses and one test that separates them, or bring in a fresh reviewer agent |
| Busy, no progress | "What is the next checkable step, and what proves it is done?" |
| Forgets earlier decisions | `/compact <focus>`, or a new session started from the plan file |
| Waiting on permission | Check the sidebar for "waiting"; pre-allow safe commands in settings |
| Silent background agent | Ask for status; if nothing comes back, stop it and re-brief it with narrower scope |
| "Done" with no proof | "Receipt please: PASS, FAIL or NOT RUN, with the command for each" |

## 4. Mindset

- Give outcomes and how you will check them, not step-by-step instructions.
- Plan first; get a fresh critic for anything risky.
- One agent writes; helpers only read and review.
- Turn each repeated correction into a rule ("update CLAUDE.md so this does not repeat"); prune rules that never fire.
- Put "stop and ask me if..." lines and a budget in every long task.
- Be specific: file paths, examples, constraints.

## 5. Voice input (Wispr Flow)

- Dictation suits agents: longer, richer prompts beat terse ones.
- Read file names, commands and flags back before sending; dictation mangles them.
- Do not let cleanup soften constraints. "Do not touch X" must survive word for word.

## 6. Prompt template for orchestrated work

```
Goal: <outcome, one sentence>
Context: <files, links, prior decisions>
Done when: <checkable test, command, or acceptance list>
Constraints: <must not touch, budget, style>
Stop and ask if: <risky or ambiguous cases>
Plan: interview me first, then write a plan file before building.
Orchestration: one writer; read-only subagents for search and review.
Report: receipt per change (PASS/FAIL/NOT RUN with the command).
```

## 7. Let Claude draft the prompt

1. Brain-dump the idea (voice works well).
2. "Interview me one question at a time until you can write the brief."
3. "Write the brief using the template above, into a file."
4. Edit the goal, done-when and stop-and-ask lines yourself. Those carry your judgment.
5. Start a fresh session from the file.
