# Start a task

Use this page when you have a pain point or an idea and need a goal Claude can check and an issue an
agent can finish.

## Steps

1. **Frame the outcome.** Name who struggles, what progress they want and the metric to move. Do not
   go on until the outcome has a number. [§5.1](../playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues) (D)
2. **Map the assumptions.** Rank the desirability, viability and feasibility assumptions by
   importance and evidence, and test the important, unproven ones first (P). Let the agent draft the
   feasibility items from the code (D).
3. **Grill anything above trivial.** Skip it for a one-line fix (D). Run Template K: one question
   per message with a recommended answer and its cost, no question the agent can answer from the
   code, a decision log in the repo, and a stop when no branch is open or the question cap is hit
   (D). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
4. **Shape a pitch and fix the appetite.** A pitch has a problem, an appetite, a solution, rabbit
   holes and no-gos. Appetite is a time budget, not an estimate, and the no-gos become the agent's
   scope fence (P). Park pitches you do not bet on instead of keeping a backlog (P).
5. **Pick the spec weight by risk and novelty.** A small fix needs an issue with a check. A normal
   feature needs a grill log, a one-page spec with Given/When/Then scenarios and open questions, and
   sliced issues. A large or risky change adds a research doc, an architecture decision record, the
   critic and human sign-off (D). [§5.3](../playbook/agent-harness-playbook.md#53-how-much-spec-before-code)
6. **Write the spec in a fresh session from the decision log.** Make every criterion observable and
   write the failure cases into the spec, since requirements usually go missing there (P). List
   undecided policy under Open Questions, because LLM-drafted PRDs state unagreed policy as fact (S).
7. **Slice into agent-ready issues with Template L.** Each issue states an outcome, a check, a
   boundary, dependencies, open questions and a risk. Build a thin end-to-end slice first, split
   vertically through the layers, and keep throwaway spikes out of production issues (P).
8. **Size and risk-rate each issue.** Treat a few person-days of human work as the ceiling for one
   issue and prefer smaller (D). Set Risk by a rule (paths touched, new dependencies, schema or auth
   changes), and when the rule and a person disagree, take the higher (D).
9. **Turn each issue into a goal with Template B.** Write the result in one sentence, then list two
   to five Done-when checks that a command or a person can run, the constraints, a budget and a
   stop-and-ask list, as page Lesson 4 (Goals) shows. Ask for a receipt: each line marked PASS, FAIL
   or NOT RUN, with its command.
10. **Run a QA loop.** An upfront spec never catches everything, so turn each QA finding into a new
    issue and send it back to slicing (P).

## Checklist

- [ ] The outcome has a number and names the person who struggles.
- [ ] Every important, unproven assumption has a test or a spike.
- [ ] The grill log lives in the repo, and I confirmed its summary.
- [ ] The appetite and the no-gos are written down.
- [ ] The spec weight matches the risk and novelty of the change.
- [ ] Every issue has a runnable check, a named boundary and a Risk set by a rule.
- [ ] Open questions are listed, not guessed.
- [ ] The goal has Done-when lines that a command or a person can check, and a stop-and-ask list.

## Templates

- [Template K. Grill prompt](../playbook/agent-harness-playbook.md#k-grill-prompt): shared understanding before any plan or spec.
- [Template L. Agent-ready issue](../playbook/agent-harness-playbook.md#l-agent-ready-issue): the issue an agent can finish.
- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): the goal, with done-when, budget and stop rules.

## Watch out for

- **Goals with no "done when".** Claude guesses and polishes what you did not ask for, as
  page Lesson 4 (Goals) shows ([§15](../playbook/agent-harness-playbook.md#15-anti-patterns)).
- **Acting on wrong assumptions.** The model proceeds without checking (S). Counter it with a
  discovery interview up front, "state your assumptions" in the plan, and plan approval
  ([§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures)).
- **Not asking when confused.** The model often keeps going (S). Add an explicit stop-and-ask list and
  a confidence field in receipts.
- **Upfront specs that miss edge cases.** Matt Pocock says QA keeps surfacing them (P). Keep a QA
  loop whose findings become new issues.
- **One-line tickets.** They drop edge cases, and a PRD that says what and why still lacks the exact
  change, boundary and check an agent needs (S).
- **Rounds of questions.** Rounds are faster but get skimmed (D), so ask one question at a time.

## Go deeper

- [§5.1 Discovery: from pain point to issues](../playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues): the seven stages and their exit gates.
- [§5.2 Should you grill? Yes, with rules](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
- [§5.3 How much spec before code?](../playbook/agent-harness-playbook.md#53-how-much-spec-before-code)
- [§5.4 Delivery phases](../playbook/agent-harness-playbook.md#54-delivery-phases): what happens after the issue is ready.
- [§0 How to use this file](../playbook/agent-harness-playbook.md#0-how-to-use-this-file): what the grades (P), (S), (R) and (D) mean.
- Page lessons: page Lesson 3 (Idea to issues), page Lesson 4 (Goals), page Lesson 5 (Phases), page Lesson 14 (Prompt library).
- Related runbooks: [orchestrate](orchestrate.md), [verify](verify.md).
