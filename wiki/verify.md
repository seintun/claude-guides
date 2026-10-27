# Verify

Use this page when you need to make "done" provable: what to check, who checks it, and what proof the
agent hands back.

## Steps

1. **Write each criterion as a scenario.** "Export matches the screen" becomes "Given 3 rows filtered
   to 2, the CSV has 2 rows." Write Given/When/Then declaratively, in 3 to 5 steps (P).
   [§9.1](../playbook/agent-harness-playbook.md#91-from-criterion-to-gate)
2. **Turn the scenario into an automated check, then a gate.** The path is criterion → scenario →
   automated check → gate → receipt. For example, a test in `npm test`, enforced by a Stop hook and a
   CI required check (D).
3. **Require a receipt.** For each criterion, record PASS, FAIL or NOT RUN with the command and its
   output, then list what is not done and the next step. NOT RUN is not PASS (D).
   [§9.4](../playbook/agent-harness-playbook.md#94-receipt-format)
4. **Pick a rung on the trust ladder by risk.** Rung 1, "the agent says it's done", is never enough.
   Rung 2 shows the command and output, rung 3 has a hook rerun the checks, rung 4 adds a fresh
   reviewer, rung 5 an adversary, and rung 6 a human (D).
   [§9.2](../playbook/agent-harness-playbook.md#92-trust-ladder)
5. **Install the Stop hook (Template F).** Exit code 2 blocks the stop and feeds stderr back to
   Claude, and `stop_hook_active` tells the hook Claude is already continuing (P). Make the script
   executable, force one failing test and confirm the hook returns exit 2 (D).
6. **Add the formatter hook (Template G).** It runs after Edit or Write, uses the project's own
   Prettier and leaves gate and config files alone (D). A PostToolUse exit code 2 shows stderr, but the
   tool has already run (P).
7. **Make tests immutable to the builder.** Back the rule with a hook or CODEOWNERS on test paths, and
   have the reviewer inspect every test diff, including mocks that replace the behaviour under test
   (D). Anthropic's long-running harness called removing or editing tests unacceptable (P). Keep one
   acceptance check outside the builder's workspace, run by CI or the Stop gate (D).
   [§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest)
8. **Check in order, cheapest first.** Use rules-based feedback (lint, types, tests), then visual
   feedback through a browser for UI, then an LLM judge (P). Give any judge a rubric (P), use one from
   a different model family than the work and repeat it (D), and never make it the only gate (D).
   [§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest)
9. **Get an independent review.** The maker is not the checker. A fresh reviewer gets the artifact
   and the criteria, never the author's reasoning or conclusion, and sources are anonymized when it
   compares candidates (D). Keep the fresh-eyes review even when tests are green (S). Bound it: only
   a blocker with evidence reopens a review, a re-review reads the fix diff for open and new blockers,
   only the reviewer or a human closes a blocker without a fix, and after two rounds a human decides (D). [§9.2](../playbook/agent-harness-playbook.md#92-trust-ladder);
   evidence in [research/bounded-review-evidence.md](../research/bounded-review-evidence.md).
10. **Measure repeated runs for unattended work.** Track pass^k (all k runs succeed), not only pass@k.
    At 75% per-run success, three runs in a row all succeed only about 42% of the time (P). Decide on
    purpose which tiers get line-by-line human review (D).

## Checklist

- [ ] Every criterion has a scenario and a command that checks it.
- [ ] The Stop hook is executable, and I forced a failing test to confirm exit 2.
- [ ] The receipt lists PASS, FAIL or NOT RUN per criterion, with the command.
- [ ] NOT RUN is not counted as PASS.
- [ ] Test paths are protected from the builder by a hook or CODEOWNERS.
- [ ] A reviewer with a fresh context got the diff and the criteria only.
- [ ] No LLM judge is the only gate.
- [ ] I chose which risk tiers get line-by-line human review.

## Templates

- [Template F. Stop hook that blocks "done" while tests fail](../playbook/agent-harness-playbook.md#f-stop-hook-that-blocks-done-while-tests-fail): retries up to a cap, then logs the give-up.
- [Template G. PostToolUse formatter](../playbook/agent-harness-playbook.md#g-posttooluse-formatter): formats each edited file with the project's own Prettier.
- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): the Done-when lines and "NOT RUN is not PASS".
- [Template A. CLAUDE.md skeleton](../playbook/agent-harness-playbook.md#a-claudemd-skeleton): its Never list holds the receipt rule and the test rule.

## Watch out for

- **The builder grading its own work.** Also a reviewer that read the author's conclusion first
  ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns)). Hand over code and criteria only.
- **Edited tests and early victory.** Models edit, disable or delete tests to make them pass, and
  declare victory early (P). Counter with a test-immutability rule, a JSON feature list, end-to-end
  tests and a Stop hook
  ([§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)).
- **A gate that silently turns off.** A non-executable hook script exits 126, which Claude Code
  treats as a non-blocking error (D). Stop does not run on a user interrupt, and API errors fire
  `StopFailure` instead (P). `--bare` skips your hooks, so run the gate as a CI step (D).
- **Green tests, broken spec.** One practitioner's Ralph run passed 28 tests and then failed a fresh
  review on a real spec breach (S).
- **An LLM judge as the only gate.** The Agent SDK guidance calls it not very robust on its own (P).
- **Normalization of deviance.** Simon Willison wrote that he no longer reviews every line of agent
  output and named this risk himself (P). A near-100% approval rate with falling review time is the
  warning sign (D).

## Go deeper

- [§9 Verification stack](../playbook/agent-harness-playbook.md#9-verification-stack)
- [§9.3 Rules that keep verification honest](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest)
- [§9.5 Hooks that enforce it (Claude Code)](../playbook/agent-harness-playbook.md#95-hooks-that-enforce-it-claude-code)
- [§4 The core loop (one agent)](../playbook/agent-harness-playbook.md#4-the-core-loop-one-agent): where verify sits in the loop.
- [Law 2. Verification multiplies quality](../playbook/agent-harness-playbook.md#law-2-verification-multiplies-quality)
- [Law 7. Separate the maker from the checker](../playbook/agent-harness-playbook.md#law-7-separate-the-maker-from-the-checker)
- [Law 9. Enforce with code; request with words](../playbook/agent-harness-playbook.md#law-9-enforce-with-code-request-with-words)
- Page lessons: page Lesson 9 (Self-checks), page Lesson 15 (When it goes wrong), page Lesson 16 (Checklist).
- Related runbooks: [orchestrate](orchestrate.md), [run-unattended](run-unattended.md).
