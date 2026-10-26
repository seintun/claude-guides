# Run unattended

Use this page before Claude runs a loop, a schedule or a cloud session while you are not watching.

## Steps

1. **Check that the work suits an unattended run.** Good fits are a well-specified backlog with
   strong tests (a Ralph loop, or day shift and night shift) and one trustworthy metric (a
   hill-climbing loop). A loop burns tokens and drifts if the specs or tests are weak (D).
   [§6](../playbook/agent-harness-playbook.md#6-orchestration-patterns)
2. **Pick the surface.** `/loop` runs in your session, at a 1-minute minimum or self-paced; it
   expires after 7 days, skips missed runs and dies with the session (P). Cloud scheduled tasks
   (`/schedule`) have a 1-hour minimum for timed triggers, start from a fresh clone and push to a
   `claude/` branch (P).
   Desktop tasks need the app open and the machine awake (P).
3. **Copy a Template H prompt.** Fill in what to watch, the one small action allowed, the end
   condition and the forbidden actions. Make the action safe to run twice, and ask for one status
   line per run, with "no change" when nothing changed (D).
4. **Write the stop condition and the retry cap.** Stop when every check passes, or after N
   iterations, minutes or dollars, and stop after two failures with the same cause (D). Do not lean
   on the Stop-hook continuation cap of 8, because it is a backstop (P).
5. **Set a cost ceiling.** Use `--max-budget-usd` on headless runs and cap the fan-out in the lead's
   prompt (P, D). Read cost from OpenTelemetry or the Console, not the local `/usage` estimate (P).
6. **Give the results a home outside the chat.** Use a file, a ticket or a PR comment (D). Cloud runs
   start from a fresh clone, so keep loop state in a ticket, a PR comment or a named branch (P). For
   work that spans sessions, use an initializer session, a JSON feature list that starts at
   `passes: false` and a progress file (P), and let a verifier or the gate flip `passes` (D).
7. **Hook the events.** Add a `StopFailure` hook that writes a marker and notifies you, because API
   errors and rate limits skip the Stop gate (P, D). Hang phone pings or approval routing on
   `Notification`, `Stop` and `PermissionRequest`, and set telemetry variables on cloud environments
   too (P).
8. **Write the kill switch before the first run.** One page: disable the scheduled task or workflow,
   stop or archive the session, revoke the tokens it used and revert its branch (D).
   [§18](../playbook/agent-harness-playbook.md#18-operating-the-harness-gaps-to-close)
9. **Sandbox the run and strip secrets.** Use a dev container or Docker locally, keep the network
   level minimal and keep production keys out of cloud environments (D). For `claude -p` in CI, use
   `--bare` or a trusted checkout, and run your gate as a CI step (P, D).
10. **Judge the first run by what it leaves behind.** An overnight run should leave a clean state and
    an accurate receipt; that is the roadmap's condition for moving up from Level 4 (D). Check for
    paused runs, not only failed ones, because a cloud scheduled task can stop and wait for an answer
    (P).

## Checklist

- [ ] The prompt names an end condition: all checks pass, or N iterations, minutes or dollars.
- [ ] A retry cap stops the run after two failures with the same cause.
- [ ] A cost ceiling is set, and I know where I read the real cost.
- [ ] Results land in a file, a ticket or a PR comment, not only in the chat.
- [ ] Running the task twice cannot send, charge or create twice.
- [ ] A `StopFailure` hook records the failure and notifies me.
- [ ] The kill switch runbook exists: disable, stop, revoke, revert.
- [ ] The run is sandboxed, and no production keys are in its environment.

## Templates

- [Template H. Loop and schedule prompts](../playbook/agent-harness-playbook.md#h-loop-and-schedule-prompts): `/loop` and `/schedule` prompts with end condition, retry cap and "no change".
- [Template E. Long-running state files](../playbook/agent-harness-playbook.md#e-long-running-state-files): `features.json` and `progress.md` for work that spans sessions.
- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): its BUDGET and STOP AND ASK ME IF lines.
- [Template F. Stop hook that blocks "done" while tests fail](../playbook/agent-harness-playbook.md#f-stop-hook-that-blocks-done-while-tests-fail): counts attempts per session and logs the give-up.

## Watch out for

- **An uncapped loop.** One plugin loop set to `max_iterations: 0` ran 6,239 iterations over about
  11.7 hours (P). Always set an iteration cap.
- **Runs that die quietly.** API errors and rate limits fire `StopFailure` instead of `Stop`, so the
  Stop gate never runs (P).
- **No cloud dollar cap.** No per-session dollar cap for cloud sessions was found, and `/usage` is a
  local estimate (P).
- **Files that vanish.** A cloud run's files do not reach the next run unless merged (P).
- **A paused run that looks idle.** Cloud scheduled tasks can stop and wait for an answer (P).
- **One good run.** At 75% per-run success, three runs in a row all succeed only about 42% of the
  time, so measure pass^k (P).

## Go deeper

- [§11 Continuous and unattended operation](../playbook/agent-harness-playbook.md#11-continuous-and-unattended-operation)
- [§11.1 The long-running harness recipe](../playbook/agent-harness-playbook.md#111-the-long-running-harness-recipe)
- [§11.3 Guardrails for any loop](../playbook/agent-harness-playbook.md#113-guardrails-for-any-loop)
- [§11.4 Operating model: terminal, cloud, phone](../playbook/agent-harness-playbook.md#114-operating-model-terminal-cloud-phone)
- [§11.5 Risks of running without watching](../playbook/agent-harness-playbook.md#115-risks-of-running-without-watching)
- [§18 Operating the harness: gaps to close](../playbook/agent-harness-playbook.md#18-operating-the-harness-gaps-to-close)
- [§17 Maturity roadmap](../playbook/agent-harness-playbook.md#17-maturity-roadmap): Level 4 is the continuous stage.
- Page lessons: page Lesson 11 (Running nonstop), page Lesson 14 (Prompt library), page Lesson 4 (Goals).
- Related runbooks: [verify](verify.md), [guardrails](guardrails.md).
