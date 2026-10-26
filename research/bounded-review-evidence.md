# Evidence: how agent reviews should end (bounded review)

The research behind the bounded-review rule in playbook [§9.2](../playbook/agent-harness-playbook.md#92-trust-ladder). Four independent doc-checker passes read each primary source on 2026-10-24. Every finding below is CONFIRMED against its source unless marked. Scope notes say where a number holds; cite a finding only within its scope.

Grades follow playbook §0: **[P]** a vendor's, standard body's or author's own words; **[R]** research. "Preprint" means no venue was found.

## A. Repeated LLM critique: early rounds help, later rounds hurt

| # | Finding | Source | Grade, venue | Scope |
|---|---|---|---|---|
| A1 | Self-correction without an outside signal lowers accuracy: GPT-4 on GSM8K fell from 95.5 to 91.5 to 89.0 over two rounds | Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", https://arxiv.org/abs/2310.01798 (Table 3) | [R] ICLR 2024 | Reasoning benchmarks, intrinsic self-correction (no tools, no tests) |
| A2 | With grounded feedback, "2-3 rounds of corrections yield most of the benefits"; self-feedback alone gives weaker returns | Gou et al., CRITIC, https://arxiv.org/abs/2305.11738 (Section 4.4) | [R] ICLR 2024 | Tool-verified critique on QA, math and toxicity tasks |
| A3 | Self-repair "is not a silver bullet": at the same sample budget, plain resampling scores as high or higher, especially at small budgets; feedback from a stronger model helps more | Olausson et al., https://arxiv.org/abs/2306.09896 | [R] ICLR 2024 | HumanEval and APPS; Code Llama, GPT-3.5, GPT-4 |
| A4 | A second LLM review round raised recall about 0.08 but produced 62% more false positives; later rounds "fabricate findings" once the real errors are exhausted | https://arxiv.org/abs/2603.16244 | [R] preprint, single author | 30 artifacts with 150 injected errors |
| A5 | LLM-only "improvement" loops made code less secure: critical vulnerabilities rose 37.6% after five iterations; the authors advise at most 3 consecutive LLM-only iterations, with human review between chains | https://arxiv.org/abs/2506.11022 | [R] IEEE ISTAS 2025 | Iterative code refinement by an LLM |
| A6 | More debate rounds stop helping: "additional debate rounds above four led to a similar final performance" | Du et al., https://arxiv.org/abs/2305.14325 (Section 3.3) | [R] preprint | Arithmetic task, 3 agents, one ChatGPT-based model |
| A7 | Critics trade precision for recall: "the probability of catching a bug increases with the number of claims", and longer critiques carry more nitpicks and hallucinations | McAleese et al., CriticGPT, https://arxiv.org/abs/2407.00215 | [R] preprint | Contractor ratings on inserted and found code bugs |

## B. What multi-round code review misses

| # | Finding | Source | Grade, venue | Scope |
|---|---|---|---|---|
| B1 | The largest share of false positives in multi-round review, 32.5%, re-flag defects that were already resolved ("state–temporal misalignment") | MCR-bench, https://arxiv.org/abs/2608.27442 (Table 11) | [R] ISSTA 2026 | 2,269 real-world multi-round review tasks, human-coded error causes |
| B2 | The leading false-negative causes are cross-round defect forgetting (25.1%), long-range dependency misses (23.4%) and over-optimistic fix assumptions (15.2%); sycophancy toward the developer accounts for 6.5% | Same, Table 11 | [R] ISSTA 2026 | Same |
| B3 | A verifier is "not a silver bullet", but a high-level objective check raised task success on ProgramDev by 15.6 percentage points | MAST, https://arxiv.org/abs/2503.13657 | [R] NeurIPS 2025 workshop | 32-task ProgramDev set, ChatDev |

## C. Reviewer bias: why evidence must gate a blocker

| # | Finding | Source | Grade, venue | Scope |
|---|---|---|---|---|
| C1 | LLM judges show position, verbosity and self-enhancement bias; GPT-4 was position-consistent on 65.0% of pairs; a reference answer cut its math-grading failures from 70% to 15% | Zheng et al., MT-Bench and Chatbot Arena, https://arxiv.org/abs/2306.05685 | [R] NeurIPS 2023 Datasets and Benchmarks | 80 near-duplicate answer pairs; 10 math questions, 20 judgments |
| C2 | Challenged with "Are you sure?", models wrongly admit mistakes on correct answers, from 42% (GPT-4) to 98% (Claude 1.3) of questions | Sharma et al., "Towards Understanding Sycophancy in Language Models", https://arxiv.org/abs/2310.13548 | [R] ICLR 2024 | Subsets of MMLU, MATH, AQuA, TruthfulQA and TriviaQA |

## D. Human review, approval and gates

| # | Finding | Source | Grade, venue | Scope |
|---|---|---|---|---|
| D1 | Organizations with formal external change approval were 2.6 times as likely to be low performers, with "no evidence" it lowers the change failure rate; DORA recommends peer review instead | DORA, 2019 State of DevOps Report, https://services.google.com/fh/files/misc/state-of-devops-2019.pdf (pp. 49-50) | [P] | Survey correlation; external boards, not peer review |
| D2 | At Google, over 80% of changes need at most one iteration of resolving comments, fewer than 25% have more than one reviewer, and the median change is 24 lines | Sadowski et al., "Modern Code Review: A Case Study at Google", https://sback.it/publications/icse2018seip.pdf | [R] ICSE-SEIP 2018 | One company's review data |
| D3 | Google's reviewer standard: approve once a change "definitely improves the overall code health", even if it isn't perfect | Google engineering practices, https://google.github.io/eng-practices/review/reviewer/standard.html | [P] | Google's published guideline |
| D4 | Review comments about defects are few: 78 of 570 classified comments (about 14%); understanding the change is the key challenge | Bacchelli and Bird, https://sback.it/publications/icse2013.pdf | [R] ICSE 2013 | Microsoft, hand-classified sample |
| D5 | Above five percent rework, an inspection reconvenes for a full reinspection; below it, the moderator may check the rework or reconvene | Fagan, "Design and code inspections", https://www.ida.liu.se/~TDDC90/labs/lab-papers/fagan76.pdf | [R] IBM Systems Journal 1976 | Formal inspections |
| D6 | Anomalies were repeatedly "addressed" in flight readiness reviews but never fully resolved, until flying with them became routine: the normalization of deviance. The board recommends an independent technical engineering authority (R7.5-1) | Columbia Accident Investigation Board, Vol. 1, ch. 8 (https://govinfo.library.unt.edu/caib/news/report/pdf/vol1/chapters/chapter8.pdf) and ch. 7 | [P] | Safety-critical engineering |
| D7 | Automation bias affects novices and experts alike and "cannot be prevented by training or instructions" | Parasuraman and Manzey, Human Factors 2010, https://doi.org/10.1177/0018720810376055 | [R] (abstract checked) | Review of human-automation studies |
| D8 | Approving every agent action creates friction "without necessarily producing safety benefits"; experienced users move from about 20% to over 40% full auto-approve | Anthropic, "Measuring agent autonomy", https://www.anthropic.com/research/measuring-agent-autonomy | [P] | Claude Code usage; partly a recommendation |

## E. Risk-based security assurance

| # | Finding | Source | Grade | Scope |
|---|---|---|---|---|
| E1 | ASVS "defines three security verification levels", and an organization picks the level from its risk analysis | OWASP ASVS 5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x03-What-is-the-ASVS.md | [P] | Application security requirements |
| E2 | SSDF practices are adopted on a risk basis, and include reviewing the design (PW.2) and the code (PW.7) for security | NIST SP 800-218 v1.1, https://doi.org/10.6028/NIST.SP.800-218 | [P] | Not a checklist; the organization decides the depth |
| E3 | Two-party review is the top source level (Level 4) and "applies to the final revision submitted" | SLSA v1.2 source requirements, https://slsa.dev/spec/v1.2/source-requirements | [P] | Supply-chain source integrity |
| E4 | Telling reviewers to focus on security made detection about eight times as likely; a checklist added nothing significant on top | https://arxiv.org/abs/2202.04586 | [R] | Developer experiment, relative increase |

## F. Vendor guidance on loops and fresh review

| # | Finding | Source | Grade |
|---|---|---|---|
| F1 | The evaluator-optimizer workflow fits when there are clear evaluation criteria; for agents, "stopping conditions (such as a maximum number of iterations)" are common | Anthropic, "Building effective agents", https://www.anthropic.com/engineering/building-effective-agents | [P] |
| F2 | A fresh context improves code review; after two failed corrections, `/clear` and write a better prompt | Claude Code best practices, https://code.claude.com/docs/en/best-practices | [P] |
| F3 | Claude Code overrides a Stop hook after it blocks eight times in a row with no tool call in between | Claude Code hooks guide, https://code.claude.com/docs/en/hooks-guide | [P] |

## How the rule maps to the evidence

| Part of the bounded-review rule (§9.2) | Supported by | Strength |
|---|---|---|
| A finding blocks only with evidence; tests outrank reviewer opinion | A1, A2, C1 (reference answers), C2, F1 | Strong, consistent across studies |
| "No blockers" is a valid result; don't loop until a review is empty | A4, A7, B1 | Moderate: A4 is one preprint, B1 is peer-reviewed |
| Two rounds, then a human decides | A2, A5, A6, D2, F2 | Convergent, not tested head to head |
| Later reviewers get the decision log; settled points stay settled | B1 (re-flagging), B2 (cross-round forgetting) | Strong for real-world review (ISSTA) |
| Only the reviewer or a human closes a blocker the builder didn't fix | D6, C2, B2 (sycophancy) | Moderate: safety-engineering and model-behaviour evidence |
| Round 2 checks the fix for new defects; a large fix gets a full re-review | B2 (long-range misses, over-optimistic fixes), D5, A5 | Moderate |
| Deterministic gates rerun freely; LLM reviews run once per version | A1, A5, B3, F3 | Moderate |
| No external approval board; light peer review | D1, D2, D3 | Strong for human teams (survey and field data) |
| Humans decide high-risk and irreversible steps, not every step | D7, D8, E3 | Moderate |
| Pick the risk tier, and the review depth, before work starts | E1, E2 | Strong as practice (standards) |
| At high risk, one security pass reads the code, scoped explicitly to security | E2, E4, D4 | Moderate |

## Not used, and why

- **"A fresh review is no better than a same-session review" (27.1% vs 28.6%, p = 0.26).** It was attributed to arXiv 2603.16244, but the figures belong to a revision of a different preprint (2603.12123 v2). 2603.16244's own body reports the opposite, from numbers its author later revised. Contested either way; left out.
- **"Restrict to 3 iterations" as a general law.** A5 recommends it for LLM-only code refinement. The rule uses two review rounds, which is consistent but not the same claim.

## Limits

- No study compares stopping rules head to head for frontier coding agents with a writer and a reviewer. The two-round cap is a convergent design choice [D], not an established optimum.
- Several LLM findings are preprints (A4, A6, A7) or come from small controlled tests (C1). Their scope notes matter.
- The human-review evidence comes from human teams. Its transfer to agent reviewers is an inference.
