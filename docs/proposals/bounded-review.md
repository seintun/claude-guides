# Proposal: bounded review: every needed review, once

Status: draft, 2026-10-24. Risk: normal for this guide. Applying it to a harness touches review skills, agents and per-repo gates, so it carries that harness's own high-risk process. The playbook part is applied (§9.2, §5.4, Templates B, C and M); the harness and repository parts are proposals.

## 1. Problem

A plan or a change gets reviewed, fixed, re-reviewed and fixed again, version after version, and several reviewers stack on one diff. Audits of one personal harness and one client repository found:
- **The adversary is over-used.** It ran in 42 of 152 sessions over 21 days, in 17 of them twice or more, and in one session 7 times.
- **The review loop is visible in one branch.** It went through 23 commits in 4 days, 16 of them review fixes, one labelled the "ninth review". The repository's check script slowed from 4 to 124 seconds.
- **The same diff gets read four times.** A pre-QA reviewer, a launch audit that repeats its bugs and spec checks, a second-model review and a human all read it.

The deterministic gates (Stop hook, pre-push, CI, QA gate) converged. Every unbounded loop was an LLM reviewer.

## 2. Root causes

1. **Briefs force findings.** "Return the 3 strongest objections" and "Assume the change is wrong" always produce three objections. "Top 3" caps the width of a review, not its rounds.
2. **Caps exist for checks and interviews, never for review rounds.** "Two strikes" fires on the *same* failure repeating, so a reviewer that finds something new each round never trips it.
3. **Re-reviews start from zero.** They read the whole change again, and nobody hands them the decisions already made. Settled points come back.
4. **Severity doesn't gate a round.** A minor wording note restarts the cycle just like a bug.
5. **Reviewers of the same model family stack on one diff,** each asking the same question.

## 3. What the evidence says

The full, source-by-source record, with scope notes for every figure, is [research/bounded-review-evidence.md](../../research/bounded-review-evidence.md).

Grades: P is a vendor's or author's own words, R is research (preprints marked), and S is second-hand. "Checked" means an independent doc-checker confirmed the claim against the source on 2026-10-24.

| # | Finding | Grade | Checked |
|---|---|---|---|
| E1 | Self-correction without an outside signal lowers accuracy: GPT-4 on GSM8K fell from 95.5 to 91.5 to 89.0 over two rounds (Huang et al., ICLR 2024, arXiv 2310.01798) | R | confirmed |
| E2 | Grounded critique pays off early: "2-3 rounds of corrections yield most of the benefits" (CRITIC, ICLR 2024, arXiv 2305.11738); Self-Refine shows diminishing returns (arXiv 2303.17651) | R | confirmed (CRITIC) |
| E3 | Later review rounds manufacture findings: a second LLM review round raised recall about 0.08 but added about 62% more false positives, and later rounds fabricated findings once the real errors ran out (arXiv 2603.16244: a single-author preprint, 30 artifacts with injected errors). In real-world multi-round code review, the largest share of false positives, 32.5%, re-flag defects already resolved (MCR-bench, ISSTA 2026, arXiv 2608.27442) | R | confirmed |
| E3b | LLM-only "improvement" loops degrade code: critical vulnerabilities rose 37.6% after five iterations, and the authors recommend at most 3 consecutive LLM-only iterations (IEEE ISTAS 2025, arXiv 2506.11022) | R | confirmed |
| E4 | The evaluator-optimizer workflow fits when there are clear evaluation criteria; for agents, "stopping conditions (such as a maximum number of iterations)" are common (Anthropic, Building effective agents). Claude Code's docs: a fresh context improves code review, and after two failed corrections, start fresh with a better prompt (Claude Code best practices) | P | confirmed |
| E5 | Adding agents to a strong single agent can lower results, and independent agents amplify errors (Kim et al., arXiv 2512.08296; playbook §19.1 item 1) | R | earlier fact-check |
| E6 | External change approval boards: organizations using them were 2.6 times as likely to be low performers, with no evidence of a lower change-failure rate. DORA recommends peer review instead (DORA 2019, pp. 49-50) | P | confirmed |
| E7 | Light review works: over 80% of changes at Google need at most one iteration of comments, and fewer than 25% have more than one reviewer (Sadowski et al., ICSE-SEIP 2018) | R | confirmed |
| E8 | Re-inspect in full only after large rework: above five percent rework, Fagan's inspections reconvene for a full reinspection; below it, the moderator chooses (Fagan 1976) | R | confirmed (wording corrected) |
| E9 | Approving every action adds friction without necessarily adding safety; experienced users auto-approve more, from about 20% of sessions to over 40% (Anthropic, Measuring agent autonomy) | P | confirmed |
| E10 | Review comments about defects are few: 78 of 570 classified comments, about 14% (Bacchelli and Bird, ICSE 2013). Generic review is not a security gate | R | confirmed |
| E11 | A finding that is raised but never closed becomes normal: the Columbia accident board describes anomalies raised review after review, never resolved, then treated as acceptable | P | not re-checked |
| E12 | Rigor scales with risk class, chosen before work: OWASP ASVS levels, NIST SSDF risk-based adoption, threat modeling at design time | P | not re-checked |

One cited figure did not hold up: a "fresh review is no better than same-session review" result belongs to a different preprint (arXiv 2603.12123 v2), and was left out. No study compares stopping rules head to head for frontier coding agents, so "two rounds" is a convergent choice, not an established optimum. The agent-specific studies in E3 are unreviewed preprints.

## 4. The rule: every needed review, once

The playbook now carries this as **Bounded review** under §9.2.
1. **Pick the tier before work starts,** from the paths the change touches, not from how it feels (§5.4, E12). Trivial work gets a receipt; normal work gets hooks plus one fresh reviewer; high-risk work adds one adversary on the plan and a human sign-off.
2. **Deterministic gates rerun freely.** Hooks and CI check every change (rung 3). They cost little and never invent findings.
3. **Each LLM review runs once per version of the work.** At high risk, the adversary reviews the plan before code, when design holes cost least; the security pass in item 7 then reads the code once per version.
4. **A finding blocks only with evidence:** a failing command, a concrete input, or a cited line that breaks a stated criterion. Everything else is advisory and goes on a follow-up list. "No blockers" is a valid result (E1, E3).
5. **Every blocker closes, but not by the builder's word.** The builder closes a blocker by fixing it; only the reviewer that raised it, or a human, closes it any other way. The builder may reject advisory findings with a reason. Later reviewers receive the decision log with the criteria, never the builder's reasoning, so points the reviewer or a human closed stay closed (E11: a finding the builder waves off is how deviance becomes normal; Law 7).
6. **Round 2 reads the fix diff for open blockers and for anything new the fix adds.** Every reviewer whose question the fix touches runs again on it, such as security for access, input or data handling. A large fix gets a full re-review (E8). There is no round 3: after two rounds a human decides to ship, fix, hold or stop (E2, E3b, E4, E7).
7. **At high risk, one security pass reads the code, not only the plan,** against an application checklist: authorization on every new entry point, input handling, data deletion and migrations, secrets, and the project's own list. It runs once per version, inside the adversary's review or as the project's own security reviewer, never both. Deterministic guards (deny rules, secret scanning) back it (E10, E12).
8. **Humans decide what only humans should decide:** high-risk plans, irreversible actions, merges, and anything still open after round 2. They are not a checkpoint on every step (E6, E9).

## 5. Universal and light globally, strict locally

| Layer | Holds | Applies to |
|---|---|---|
| **Global** (personal harness) | The security floor (sandbox, deny and ask rules, destructive-command guard); the gate runner; receipts; the generic tiers; this review rule; three agents: a fresh reviewer, an adversary and a doc checker | Every project, and kept light |
| **Local** (each repository) | Its checks (gates file, check script, CI), its high-risk path list (with CODEOWNERS as the source of truth), any extra reviewers (a second-model plan review, a one-pass CI review), its tracker policy | Only the repository that needs it |

A strict client process belongs in the client's repository, where its team can see and change it. Today, high-risk path lists and client steps sit in global rules and agent descriptions, which load into every session in every project.

## 6. Where it lands: a patch, not an overhaul

**This guide (applied):**
- **§9.2:** the Bounded review rule.
- **§5.4:** the Critique and Review exits now close.
- **Template B:** steps 4 and 7 bounded, plus a two-round rule.
- **Template C:** an "Already decided" field.
- **Template M:** later pushes review only the new commits.
- **The routes:** `ENTRY.md` gains "Reviews end", and the orchestration index's review prompt changed.
- **The runbook and skill:** `wiki/verify.md` step 9 and `/prompt`, so generated prompts carry the bound.
- **The teaching page:** its four echoes.

`tests/test_critical.py` pins the new wording.

**A personal harness (proposed, owner applies):**
- **Launch audit:** after a blocker fix, re-run only the reviewer that raised it, on the fix diff, with the earlier findings and rulings, once per ticket.
- **Launch audit stacking:** drop its bugs and spec review where a pre-QA review already covered the same head.
- **Pre-QA round count:** count rounds per ticket, so a later fix commit can't reopen a third round.
- **Adversary brief:** change "exactly three objections" to "up to three; none is valid".
- **Second-model plan review:** re-run it once, and only after a block verdict.
- **Client lists:** move them out of global rules and agent descriptions into the client repository.

**A client repository (proposed, owner applies):**
- A local review policy holding its high-risk path list, with CODEOWNERS as the source and a check that keeps the two in sync.
- Its extra reviewers, each run once.
- Approve the gates file from the main development branch after merge, not from a feature worktree, so the local Stop gate works in every worktree.

## 7. Patch or clean slate

Patch the review loops now. They come from a few sentences, and the deterministic gates already work.

The workflow-layer bloat (skills, agents, rules, plugins) is a separate problem. A clean-slate reset is already drafted in [harness-reset-proposal.md](harness-reset-proposal.md). It keeps the security floor and cuts the workflow layer. This audit refines its agent list: keep a fresh reviewer, an adversary and a doc checker; drop the release verifier; fold the config auditor into the harness's own check script. Do the reset after the review patch has run for a week, so the two changes can be told apart.

## 8. Review of this proposal

One adversarial round found three blockers, all fixed before commit, as the rule says:
1. **Round 2 checked only the old blocker,** so a fix that adds a defect (an N+1 fix that drops an owner check) shipped unreviewed. Now round 2 looks for new blockers in the fix, every reviewer whose question the fix touches runs again, and a large fix gets a full re-review.
2. **The builder could close an evidenced blocker with a one-line rejection.** Now only the reviewer or a human closes a blocker without a fix.
3. **At high risk nothing read the code for security,** because the cited checklists cover the harness, not the application. Now one security pass reads the code against an application checklist.

## 9. How we'll know it works

Measure over the next two weeks, against the 21 days before:
- review rounds per ticket (target: never above 2);
- adversary runs per session;
- review-fix commits per branch;
- time from first review to merge;
- defects found after merge;
- the share of reviews that report "no blockers", where near 100% signals rubber-stamping (E9).

**Verification status (2026-10-24):** two independent doc-checks read each primary source. E1 to E4 and E6 to E10 are confirmed, with E4's attribution and E8's wording corrected. E11 and E12 rest on the research helper's reading and were not re-checked.
