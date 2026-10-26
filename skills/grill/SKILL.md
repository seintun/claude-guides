---
name: grill
description: Grill the user about an idea or plan, one question at a time with a recommended answer, until you share an understanding of the design. Use before writing a plan or spec for anything above a one-line fix.
argument-hint: <idea or plan to grill>
disable-model-invocation: true
---

Grill the user about: $ARGUMENTS

The goal is shared understanding before any plan or spec. Follow these rules (playbook §5.2 and Template K):

1. **Look before you ask.** Read the code, docs and data first; for a wide sweep, send read-only helpers in parallel. Never ask the user a fact you can find, or one the request or an earlier answer already gives. Tell them what you found instead. If a search finds nothing, say what you searched, then ask it as a fact question.
2. **One question per message.** Each question asks one thing, never "who, when and what it costs" at once. Settle prerequisite questions before the ones that depend on them, and keep the rest of the design tree to yourself.
3. **Shape every question the same way.**
   - A judgment question (a choice, a priority, a trade-off) gets 2 to 4 options. Your recommended option comes first, with "(Recommended)" at the end of its label.
   - Each option's description says what it implies and what it costs.
   - The question text says why the recommendation wins.
   - A question too big for 4 options gets split, not crammed.
   - A fact question (a number, date, duration, count or name) is asked open, with no options. No option and no question text carries a figure the user, the project or a lookup did not supply: one click would turn your guess into the user's fact.
   - Use the AskUserQuestion tool when it is available, with one question per call. Without it, ask in plain text with options lettered A to D, recommendation first.
4. **Cover the ground:** the problem (who struggles and when, and what it costs them), where the work lives (the code, data and records it touches), the outcome metric, the appetite (time budget), no-gos, rabbit holes, failure cases, the riskiest assumption with the cheapest test of it, and open questions.
5. **Log every decision** in `docs/discovery/<topic>.md`, or in the plan's Decisions list if one exists: the date, the question, the answer and the reason. Write it as you go, not at the end, so a compacted or new session can resume from the file. Commit it with the branch, and link it from the issue if there is one; don't copy it into the ticket.
   - "I don't know" is not a decision. Log it under open questions as `UNKNOWN: <why>`, and mark anything you filled in yourself `ASSUMED: <text>`. One gap per `UNKNOWN` line: never merge gaps, or relabel an unknown as assumed, to make the list look shorter.
   - Write relative terms ("next Friday", "this quarter", "the owner") as absolute dates and named people. Ask once if one is ambiguous.
6. **Stop** when no branch is open or at the question cap the user set. Then summarize the decisions for the user to confirm, listing every `ASSUMED` and `UNKNOWN` line.
7. **A go-ahead is not a grill question.** Approval to build, commit or publish waits for the user's explicit yes, never a picked option.

Do not write a plan, spec or code in this session.
