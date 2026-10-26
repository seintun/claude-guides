# Unstick an agent

Use this page when a Claude agent loops, will not finish, says "done" over broken work, repeats a
mistake, loses context in a long session or builds more than you asked for.

## Symptoms

| Symptom | Likely cause | First move | Playbook |
|---|---|---|---|
| Same error twice, or the same fix tried again | Loops on the same failing approach (P) | Stop it. Ask for 3 ranked hypotheses and one test that separates them, or bring in a fresh reviewer agent | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures), [cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |
| Busy, no progress | No checkable next step | Ask "What is the next checkable step, and what proves it is done?" | [§4](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent), [cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |
| "Done" with no proof | Declares victory early (P) | Ask "Receipt please: PASS, FAIL or NOT RUN, with the command for each" | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures), [cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |
| Tests pass, but the tests changed | Edits, disables or deletes tests to make them pass (P) | Read the test diff. Add a test-immutability rule plus a hook or CODEOWNERS on test paths | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures) |
| Forgets earlier decisions in a long session | Context rot (P) | `/compact <focus>`, or start a new session from the plan file | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures), [cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |
| Repeats an old mistake in a new session | Forgets between sessions (P) | Put the lesson in CLAUDE.md, memory or a progress file | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures), [§8](../playbook/agent-harness-playbook.md#8-context-engineering) |
| Builds extras, bloats, leaves dead code | Overbuilds (S); adds features nobody asked for (P) | Set a diff-size budget, write no-gos into the issue, ask for a simplifier pass | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures) |
| Waiting on permission | A permission prompt is blocking it | Check the sidebar for "waiting". Pre-allow safe commands in settings | [Cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |
| Silent background agent | The helper went quiet | Ask for status. If nothing comes back, stop it and re-brief it with narrower scope | [Cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes) |

## Steps

1. **Break a loop.** When the same check fails twice for the same reason, stop and get a second
   opinion: 3 ranked hypotheses and one test that separates them, or a fresh agent (P). The loop
   escalates to a second opinion or a human, never a sixth retry (D).
   [§4](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent)
2. **Restore a checkable step.** If it is busy with no progress, ask what the next checkable step is
   and what proves it done. The loop takes one small step toward a "done when" item and verifies it
   before the next (D). [§4](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent)
3. **Replace "done" with a receipt.** Ask for PASS, FAIL or NOT RUN with the command for each item.
   NOT RUN is not PASS. A JSON feature list, end-to-end tests and a Stop hook counter early victory
   (P). Models also edit, disable or delete tests to make them pass (P), so read the test diff and
   guard test paths with a hook or CODEOWNERS.
   [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)
4. **Rescue a long session.** Run `/compact <focus>`, or start a new session from the plan file, which
   is the source of truth, so keep it current. Counter context rot with subagents, compaction and
   notes on disk (P). Keep progress and decisions in files: JSON for state such as feature lists,
   Markdown for narrative notes (P). [§8](../playbook/agent-harness-playbook.md#8-context-engineering)
5. **Cut overbuilding.** Set a diff-size budget, ask for a simplifier pass and have the reviewer flag
   scope creep (S). Write no-gos into the issue for features nobody asked for (P).
   [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)
6. **Unblock a helper or a prompt.** Check the sidebar for "waiting" and pre-allow safe commands in
   settings. If a background agent is silent, ask for status, then stop it and re-brief it with
   narrower scope. [Cheat sheet §3](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes)
7. **Cap the next run.** Give it a stop condition (every check passes, or N iterations, minutes or
   dollars), a retry cap (after two failures with the same cause, stop and report) and a results sink
   outside the chat (D). When the budget runs out, stop and report. The Stop-hook continuation cap of
   8 is a backstop, not your stop condition (P).
   [§11.3](../playbook/agent-harness-playbook.md#113-guardrails-for-any-loop)
8. **Hand the lesson to a retro.** Run Template I and propose up to 3 changes: a CLAUDE.md rule, a
   skill, a hook, a test or a tool fix. Apply none until you say yes (D). Promote to CLAUDE.md only
   the rules that stop a repeated mistake (D).
   [Law 8](../playbook/agent-harness-playbook.md#law-8-turn-every-correction-into-a-rule)

## Checklist

- [ ] After two failures with the same cause, a fresh agent or I gave a second opinion.
- [ ] Every "done" has a receipt with PASS, FAIL or NOT RUN and the command, and NOT RUN is not PASS.
- [ ] I read the test diff, and test paths are guarded by a hook or CODEOWNERS.
- [ ] Decisions and progress live in files, so a new session can start from the plan file.
- [ ] The goal names no-gos and a diff-size budget.
- [ ] The next run has a stop condition, a retry cap and a results sink outside the chat.
- [ ] I ran a retro, and each proposed change was accepted or rejected.

## Templates

- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): the Done-when lines, the budget, the stop-and-ask list and the RULES block.
- [Template D. Plan file](../playbook/agent-harness-playbook.md#d-plan-file): the file a fresh session starts from.
- [Template C. Subagent brief](../playbook/agent-harness-playbook.md#c-subagent-brief): re-brief a silent helper with a narrower scope.
- [Template F. Stop hook that blocks "done" while tests fail](../playbook/agent-harness-playbook.md#f-stop-hook-that-blocks-done-while-tests-fail): enforces "done" with code, because must-happen checks that live only in prose are an anti-pattern.
- [Template I. Retro prompt](../playbook/agent-harness-playbook.md#i-retro-prompt): up to 3 changes, applied only after you say yes.

## Watch out for

- **Loops with no cap.** They keep going ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns)).
  Set the iteration, time or cost cap before you restart.
- **A second opinion that read the first answer.** Give the fresh agent the failing check and the
  criteria, not the first agent's reasoning (S).
- **Trusting skill across areas.** Competence is jagged, so verify everything (P). On genuinely novel
  code, use more human design, smaller steps and closer collaboration (P, S).

## Go deeper

- [§14 Model failure modes and countermeasures](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures): the full table, including hidden trade-offs and sycophancy.
- [§4 The core loop (one agent)](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent): where escalation sits, and the order to verify in.
- [§8 Context engineering](../playbook/agent-harness-playbook.md#8-context-engineering): compaction, notes, subagents and state formats.
- [§11.3 Guardrails for any loop](../playbook/agent-harness-playbook.md#113-guardrails-for-any-loop): stop condition, retry cap and results sink.
- [§15 Anti-patterns](../playbook/agent-harness-playbook.md#15-anti-patterns)
- [Cheat sheet §3. Stuck signs and fixes](../playbook/claude-cheat-sheet.md#3-stuck-signs-and-fixes): six signs and one-line fixes.
- Page lessons: page Lesson 1 (Everything is one loop), page Lesson 15 (When it goes wrong).
- Related runbooks: [verify](verify.md), [improve](improve.md), [run-unattended](run-unattended.md).
