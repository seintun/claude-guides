# Improve

Use this page after real tasks, when you want the harness to get better, or when the model keeps
repeating a bad habit.

## Steps

1. **Hold a retro after each real task (Template I).** Ask where turns were wasted, what you had to
   correct, which check caught a real problem, which check was missing and which helper came back
   empty. Propose up to 3 changes, and apply none until you say yes (D).
2. **Turn each lesson into one change.** A change is a CLAUDE.md rule, a skill, a hook, a test or a
   tool fix (D). Keep detailed learnings in `docs/solutions/` or skills, and promote to CLAUDE.md only
   the rules that stop a repeated mistake (D). Keep a mined rule or skill only if re-running the
   evals shows it helps (D). [§13](../playbook/agent-harness-playbook.md#13-evals-and-learning)
   [Law 8](../playbook/agent-harness-playbook.md#law-8-turn-every-correction-into-a-rule)
3. **Start an eval set from real failures.** Collect 20 to 50 simple tasks drawn from real failures
   (P), one JSONL line per task (Template J). Record where each task came from, such as an incident
   (D).
4. **Pick graders and read transcripts.** Code-based graders are fast, objective and brittle,
   model-based graders need calibration, and humans are the gold standard but slow (P). Prefer code
   checks before LLM judges, and validate any judge against expert labels (P). Scores say that
   something broke; transcripts say why (P). Label failures by hand (R).
   [§13](../playbook/agent-harness-playbook.md#13-evals-and-learning)
5. **Track the scorecard.** Count first-try pass rate, rework loops, human interventions, escaped
   defects, cost per task and pass^k on the eval set (D). Read the trend after ten tasks to see where
   to invest, as page Lesson 13 (Growing) advises.
6. **Change one thing at a time.** Keep CLAUDE.md, agent definitions, skills, hooks and tool
   descriptions in git, and re-run the eval set after each change (D). On a model upgrade, re-run with
   components removed and delete what no longer earns its tokens (D).
7. **Prune on a schedule.** Cut any line whose removal would not cause a mistake (P), and drop rules
   that never fire (D).
8. **Match the symptom to its countermeasure.** Look the bad habit up in the failure-mode table and
   apply its fix. When the same check fails twice for the same reason, stop and ask for a second
   opinion (D). [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)
9. **Audit the design against the anti-patterns.** Examples are a framework built before one good
   call, the builder grading its own work, and loops with no cap (P, D).
   [§15](../playbook/agent-harness-playbook.md#15-anti-patterns)
10. **Watch the review load.** Cap PR size, route review depth by risk tier, and track approval rate
    and time-to-review (D). A near-100% approval rate with falling review time is the warning sign of
    normalization of deviance (D).

## Checklist

- [ ] A retro ran after my last real task, and each proposal was accepted or rejected.
- [ ] Each accepted lesson became a rule, skill, hook, test or tool fix.
- [ ] The eval set holds tasks from real failures, one JSONL line each.
- [ ] I read transcripts of failing runs, not only scores.
- [ ] The scorecard tracks six measures, and I looked at the trend after ten tasks.
- [ ] After a model upgrade I re-ran a frozen eval set with k trials per task.
- [ ] I pruned CLAUDE.md lines and rules that never fire.
- [ ] I looked at approval rate and time-to-review.

## Templates

- [Template I. Retro prompt](../playbook/agent-harness-playbook.md#i-retro-prompt): up to 3 changes with exact text, applied only after you say yes.
- [Template J. Eval task record (JSONL, one line per task)](../playbook/agent-harness-playbook.md#j-eval-task-record-jsonl-one-line-per-task): id, source, prompt, grader, check, expected, tags and trials.
- [Template A. CLAUDE.md skeleton](../playbook/agent-harness-playbook.md#a-claudemd-skeleton): where promoted rules land.

## Watch out for

- **Declares victory early (P).** Counter with a JSON feature list, end-to-end tests and a Stop hook.
- **Edits, disables or deletes tests to make them pass (P).** Add a test-immutability rule plus a
  hook or CODEOWNERS on test paths.
- **Loops on the same failing approach (P).** Add a retry cap and a second opinion from a fresh agent.
- **Sycophancy and no pushback (S).** Use independent reviewers who do not see the author's
  reasoning, or anonymized councils.
- **Overbuilds and adds features nobody asked for (S, P).** Set a diff-size budget, write no-gos into
  the issue, and have the reviewer flag scope creep.
- **A bloated CLAUDE.md (P).** It gets ignored, so prune it and move detail into skills or
  `docs/solutions/`.

## Go deeper

- [§13 Evals and learning](../playbook/agent-harness-playbook.md#13-evals-and-learning): graders, the scorecard and the learning loop.
- [§14 Model failure modes and countermeasures](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures): the full table, including jagged competence and context rot.
- [§15 Anti-patterns](../playbook/agent-harness-playbook.md#15-anti-patterns)
- [§18 Operating the harness: gaps to close](../playbook/agent-harness-playbook.md#18-operating-the-harness-gaps-to-close): evals across model upgrades and human review load.
- [§19.1 Findings that hold up](../playbook/agent-harness-playbook.md#191-findings-that-hold-up): finding 9, evals start from error analysis.
- [Law 1. Keep the harness thin; let the model do the work](../playbook/agent-harness-playbook.md#law-1-keep-the-harness-thin-let-the-model-do-the-work)
- Page lessons: page Lesson 13 (Growing), page Lesson 14 (Prompt library), page Lesson 15 (When it goes wrong), page Lesson 16 (Checklist).
- Related runbooks: [build-a-harness](build-a-harness.md), [verify](verify.md).
