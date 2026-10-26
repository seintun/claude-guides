# Grill before you plan

Use this page when a request is bigger than a one-line fix and you and the agent don't yet share the design. The grill runs before any plan, spec or code. The `/grill` skill in [skills/grill](../skills/grill/README.md) packages these rules. It runs only when you type `/grill`, never on its own.

## Steps

1. **Decide whether to grill.** Grill anything above trivial, and skip it for a one-line fix (D).
   [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
2. **Look before you ask.** The agent reads the code, docs and data first, and never asks you a fact it
   can find; it reports what it found instead (D). For a wide sweep it sends read-only helpers in
   parallel, so the questions start from facts.
   [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
3. **Ask one question per message,** with the agent's recommended answer and what it costs. Rounds
   are faster but get skimmed (D). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
4. **Give every question the same shape** (D):
   - 2 to 4 options, with the recommendation first, marked "(Recommended)";
   - each option says what it implies and what it costs;
   - the question text says why the recommendation wins;
   - split a question that needs more than 4 options.

   In Claude Code, ask with the AskUserQuestion tool, one question per call, so the user picks
   instead of typing. Where the tool is missing, ask in plain text with lettered options.
5. **Walk the design tree.** Settle prerequisite questions before the ones that depend on them, and
   cover who struggles and when, the outcome metric, the appetite, no-gos, rabbit holes, failure cases
   and open questions. [Template K](../playbook/agent-harness-playbook.md#k-grill-prompt)
6. **Log each decision in the repo as you go,** not only in chat: date, question, answer, reason (D). See [records](records.md). Use
   `docs/discovery/<topic>.md`, or the Decisions list of the plan file when one exists.
7. **Stop** when no branch is open or the question cap is hit, then summarize the decisions for the
   user to confirm (D). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
8. **Keep approval out of the grill.** A go-ahead to build, commit or publish waits for the user's
   explicit yes, not a picked option (D).
9. **Write the spec or plan in a fresh session** from the decision log, so the interview's clutter
   stays out of the build (D). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)

## Checklist: validate a grill

Per question:
- [ ] It could not be answered from the code, docs or data.
- [ ] It is the only question in the message.
- [ ] It has 2 to 4 options, the recommended one first and marked.
- [ ] Each option names what it implies and what it costs, and the question says why the recommendation wins.

Per session:
- [ ] Facts were looked up before the first question.
- [ ] Every answer is in the decision log with its reason.
- [ ] The grill stopped at the cap or with no branch open, and the user confirmed the summary.
- [ ] No plan, spec or code was written during the grill.

## Templates

- [Template K. Grill prompt](../playbook/agent-harness-playbook.md#k-grill-prompt): the paste-in version of these rules.
- [Template B. Task contract (goal prompt)](../playbook/agent-harness-playbook.md#b-task-contract-goal-prompt): what the grill's decisions turn into.
- [Template D. Plan file](../playbook/agent-harness-playbook.md#d-plan-file): its Decisions list can hold the grill log.

## Test the skill

`skills/grill/test.sh` runs one fresh `claude -p` session in a throwaway project outside the repository. It asks for a grill on "add full-text search to our notes service". The project's README answers two questions the grill must not ask: the database (PostgreSQL) and the test command. `check_transcript.py` then checks the session's first message against 8 rules:

| Check | Rule |
|---|---|
| grill-1 | It looked at the project before asking |
| grill-2 | It reported a fact it found (PostgreSQL) instead of asking for it |
| grill-3 | It asked no question the README answers |
| grill-4 | One question in the message |
| grill-5 | 2 to 4 options |
| grill-6 | The recommended option comes first, and only one is recommended |
| grill-7 | It wrote no plan, spec or code |
| grill-8 | The session ended without an error |

Last result, 2026-10-24: all 8 checks passed in 3 of 3 runs (Sonnet, through `claude -p`). The first run failed grill-5 and grill-6 because the checker missed the model's option format, so the checker now accepts the common ones and prints the message when a check fails.

Limits: the test checks the first message only, with one fixture and one model. Model output varies, so run it 3 times before trusting a change to the skill ([§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest) on pass^k). The `--installed` flag tests the `/grill` command itself, once you have linked it.

## Worked example

The plan for this guide's entry point began with a 3-question grill. The decisions are in [docs/plans/guide-entry.md](../docs/plans/guide-entry.md).
- **Facts first.** Before the first question, three helpers in parallel audited the entry files, mapped 18 scenarios to playbook coverage, and checked how skills and `CLAUDE.md` imports load. None of those findings became a question.
- **Three questions,** one per message, each with the recommendation first: how far "callable from anywhere" should reach, how to install the skill, and how to route scenarios the playbook covers only partly. The third was asked only after the coverage audit found 7 partial scenarios.
- **Approval stayed separate.** The plan was approved after the grill, as its own step.

## Watch out for

- **Rounds of questions.** They are faster but get skimmed (D). Keep to one per message.
- **Asking for facts.** Every question the agent could have answered itself spends your attention.
- **A picked option taken as approval.** An option chooses between designs; it doesn't authorize work.
- **Versions of Pocock's grill-me skill differ on pacing.** One asks one question at a time, while the
  current one asks in rounds (P). [§5.2](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)

## Go deeper

- [§5.2 Should you grill? Yes, with rules](../playbook/agent-harness-playbook.md#52-should-you-grill-yes-with-rules)
- [§5.1 Discovery: from pain point to issues](../playbook/agent-harness-playbook.md#51-discovery-from-pain-point-to-issues): where the grill sits among the seven stages.
- [Template K](../playbook/agent-harness-playbook.md#k-grill-prompt)
- Related runbooks: [start-a-task](start-a-task.md), [orchestrate](orchestrate.md).
