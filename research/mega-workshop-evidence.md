# Evidence: what holds up from a workshop on running coding agents

The research behind the October 2026 additions to playbook [§5.4](../playbook/agent-harness-playbook.md#54-delivery-phases), [§8](../playbook/agent-harness-playbook.md#8-context-engineering), [§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest), [§13](../playbook/agent-harness-playbook.md#13-evals-and-learning), [§18](../playbook/agent-harness-playbook.md#18-operating-the-harness-gaps-to-close) and [§19](../playbook/agent-harness-playbook.md#19-proven-orchestration-what-the-evidence-says). It asks which advice from a workshop on running coding agents (the MEGA.dev kickoff, October 2026), plus a "search GitHub before you build" rule from a social post, holds up against research and first-party reports.

How it was checked:
- **Sweep.** Research agents, one per topic (autonomy, test quality, evals and learning, context files, delivery safety, human factors, prior art), read about 170 sources.
- **Admission bar.** Only [R] (a peer-reviewed venue, or a preprint from a major lab or with a large dataset, marked "preprint") and [P] (a first-party report or official doc with concrete content). Vendor marketing, recaps, opinion and social posts were rejected.
- **Two checkers per claim.** 81 shortlisted claims went to two independent `doc-checker` agents each: one tried to confirm the numbers, scope and venue; the other tried to refute them. A claim survived only with no refutation and at least one confirmation. 76 survived, many with corrected wording.
- **Re-check of the shortened wording.** On 2026-10-26 and 2026-10-27, six more `doc-checker` passes read the primary source behind every claim the playbook now cites, and every number in the verdict table, in the shortened wording. Each pass opened the paper or page itself and quoted it. Their verdicts, and what each changed, are in [Re-check of the playbook wording](#re-check-of-the-playbook-wording).
- **Links.** Every URL in [Sources](#sources) was fetched on 2026-10-27. All resolved except two that refuse scripted clients (HTTP 403): the ACM page behind the Luo et al. DOI, which was read in a browser-rendered fetch, and the SEC order on Knight Capital, which a `doc-checker` read in full.
- **Independent review:** pending.

"Survives" means the source says what we quote, within the stated scope. It does not mean the finding generalises. Grades follow playbook §0: **[P]** a vendor's or author's own words; **[R]** research. "Preprint" means no venue was found.

## Verdict on what the workshop said

| Workshop claim | Verdict | Why | Sources |
|---|---|---|---|
| Start protective: let agents merge only low-risk PRs, and raise autonomy on purpose | **Supported as practice, untested as policy** | Intercom auto-approves a share of PRs, excludes large or broad ones and logs every approval [P, self-reported]. Mean acceptance of agent PRs, across weekly agent-and-task observations, differs sharply by task type: chore 84% and docs 82% against performance 55% (7,156 filtered PRs) [R]. No study tests a staged autonomy ladder against alternatives | Intercom, "AI is approving our pull requests" (2026); Pinna et al. (MSR 2026 Mining Challenge) |
| Users raise autonomy as trust grows | **Observed, not shown warranted** | Among users who signed up after 19 September 2025, full auto-approve rises from about 20% of sessions for new users to over 40% by 750 sessions, partly perhaps because users change their default settings [P]. Users accept 93% of manual permission prompts, and Anthropic warns that over time such prompts lead to approval fatigue [P] | Anthropic, "Measuring AI agent autonomy"; Anthropic, "Claude Code auto mode" |
| Merge rate shows agent PRs are good | **Weak evidence** | Submitter attributes carry about 76% of an agent-PR merge model's explanatory power (a correlational model); 77.5% of merged agent PRs were merged by their submitter, against 57.6% of human PRs [R] | Yoshioka et al. (MSR 2026) |
| Agents game tests, so protect the checker | **Strongly supported in benchmark and eval settings** | ImpossibleBench and METR measure the propensity on benchmark task suites, METR with an earlier version of o3 [R, P]; UTBoost shows weak benchmark tests let wrong patches pass [R]. Not measured in real repositories | ImpossibleBench (preprint, 2025); METR (2025); UTBoost (ACL 2025) |
| Delete over half of agent-written tests, and schedule test pruning | **No evidence** | No study varies suite size or flakiness against agent success. Flaky-test research says don't simply remove or disable flaky tests: in one study 24% of flaky-test fixes changed the code under test, and 94% of those fixed a bug there [R]. Google notes that automatic quarantine "could easily mask a real race condition" [P]. No study compares quarantine, rerun and deletion | Luo et al. (FSE 2014); Google Testing Blog (2016) |
| Mine your sessions into specialised agents, and test them with about 50 generated scenarios | **Partly supported, with sharp caveats** | In an online setting without ground-truth feedback, self-evolving context fell below the base model [R]. Skills a model writes for itself before a task did worse than none [R]. An unguided LLM judge was near chance at picking the better skill (46.4% on 151 pairs; 73.8% with a rubric derived from the same pairs) [R]. Simulated users inflate scores [R] | ACE (ICLR 2026); SkillsBench (preprint, v4 2026); "From raw experience to skill consumption" (preprint, 2026); "Mind the Sim2Real gap" (COLM 2026) |
| Keep one small AGENTS.md as a map | **Supported for "small", not for "map"** | LLM-written context files raised cost by over 20% without a significant gain; developer-written ones showed a small, non-significant gain on the authors' benchmark (+2.4%, p=0.21, in v2 and v3; v1 reported +4%); codebase overviews did not help [R] | Gloaguen et al. (preprint, v3 2026) |
| Write down the "no": ADRs with a "Revisit if" line | **No direct evidence** | None of the ADR templates checked (Nygard, MADR, Y-statements) has a dedicated revisit field, though MADR's optional "More Information" section prompts for when a decision should be revisited [P]. No study tests one | Nygard (2011); MADR; Zimmermann on Y-statements |
| Share a grammar or glossary with agents | **No evidence found** | Nothing tests a project glossary as agent input | |
| Ship risky changes dark, and test recovery | **Supported by incidents and practice, not by effect studies** | Postmortems and incident reports from Google, Facebook, Knight Capital, Google Cloud (2025) and GitLab (2017) [P, R]. No study measures the effect of flags on failure rate, and none covers agent-authored deploys | Google SRE Workbook, Appendix C; Tang et al. (SOSP 2015); SEC order on Knight Capital (2013); Google Cloud incident report (Jun 2025); GitLab postmortem (2017) |
| Have agents file friction notes after every PR | **No evidence** | Stripe describes friction logging as a practice in which its teams use the product end to end as a user would [P]; nothing covers agent-filed friction | Stripe Sessions 2024, "Craft and beauty" |
| Burnout is the main risk, and people now work far longer hours | **Not established** | DORA 2024's burnout estimate (-0.6% for a 25% rise in AI adoption) has an 89% uncertainty interval that spans zero [P]. In Danish administrative data for 11 exposed occupations, confidence intervals rule out effects above 2% on earnings and recorded hours from AI chatbots two years after ChatGPT's launch (the October 2025 and March 2026 revisions; the May 2025 version said 1%); unrecorded hours are not visible [R] | DORA 2024 (the playbook cites DORA 2025 instead); Humlum and Vestergaard (NBER working paper) |
| Outcomes over output | **Indirectly supported** | After Cursor adoption, velocity gains faded within about two months while static-analysis warnings and complexity stayed up [R]. DORA 2025 links AI adoption to higher instability [P] | He et al. (MSR 2026); DORA 2025 |
| For an unfamiliar feature, search GitHub first and compare approaches (social post) | **Not as worded; a guarded version is defensible as practice** | Retrieval helps when the model lacks the knowledge and can hurt when it doesn't, and pulling in code carries supply-chain risk: off-the-shelf models invented 5.2% (commercial) to 21.7% (open-source) of the packages they recommended [R]. The guarded version (repo first, then official docs, then other projects for ideas; vet every new dependency; copy only under a permissive licence) is in playbook §5.4 as practice [D] | Spracklen et al. (USENIX Security 2025) |

Titles, venues, grades and URLs for every source above are in [Sources](#sources).

## What went into the playbook

About 700 words and 19 sources. Three independent reviewers read the full drafts against the playbook and cut them to the rule under each finding, keeping only the numbers that carry it, because most of the drafted weight was model-specific numbers that will date.

| Where | What it adds |
|---|---|
| §5.4, after the Delivery phases table | Repo first, then official docs, then other projects for ideas; vet new dependencies; copy only under a permissive licence |
| §8 | Generated context files don't pay; cut a generated CLAUDE.md to what the agent can't discover |
| §9.3 | Read-only tests aren't enough: keep one acceptance check outside the builder's workspace, and a sanctioned "can't be done" exit. Inspect test diffs for mocks that replace the behaviour under test. A judge favours its own outputs, and open-weight judges disagreed with themselves across runs |
| §13 | Mined lessons need an outcome signal; reviewed skills beat self-written ones; label failures by hand |
| §18 | Approval fatigue, and merge rate is not a quality signal; quarantine flaky tests, don't delete them; ship risky changes dark and test restores |
| §19.1 items 5 and 6 | Weak benchmark tests (UTBoost); fading velocity gains after Cursor adoption, and lower comprehension in one skill-formation trial |
| §19.2 | Intercom's scoped auto-approval |
| Follow-on qualifiers | Laws 2, 5 and 8, §14, §19.1 item 8, §19.3 and §19.4, so no part of the playbook contradicts the additions; one clause each in the verify, build-a-harness, improve and orchestrate runbooks; router rows 9, 10, 14 and 16 in ENTRY.md |

Left out on purpose: a line under Law 8 (it restated §8 and §13), instruction-count and input-length studies (Law 4 and §8 already treat context as a budget), a study of context files growing by accretion (descriptive, not evidence of harm), and simulated-user results (the playbook never recommends simulated users).

## Re-check of the playbook wording

Each claim as it now reads in the playbook, the verdict on the shortened draft, and what the check changed. CONFIRMED: the source says it, within scope. PARTIAL: true in part, or the scope or a qualifier was off. WRONG: the source says otherwise.

| # | Claim (where) | Source read | Verdict on the draft | What changed |
|---|---|---|---|---|
| 1 | LLM-written context files changed resolve rate by -0.5 and -2 points, neither significant, and raised cost over 20%; developer-written files gained 2.4%, not significant (§8) | Gloaguen et al., arXiv v3, §4.2 and Table 3 | PARTIAL: the draft said "under 2 points" and "about 20%"; the paper gives 0.5% and 2%, and 20% and 23%. Developer-written files were tested only on the authors' own benchmark | Exact figures; "on the authors' own benchmark" |
| 2 | With tests that contradict the spec, models passed by editing tests or special-casing; read-only tests stopped only the edits; a stop-and-report exit helped some models far more than others (§9.3) | ImpossibleBench, arXiv v1, §5.2 and §5.3 | CONFIRMED | None |
| 3 | A Read deny rule doesn't cover a script that opens the file itself, or a command that reads without naming it (§9.3) | Claude Code permissions docs, "What Read and Edit rules cover" | PARTIAL: the draft said a Read deny "doesn't hide a file from Bash", but Read deny rules do cover `cat`, `head`, `tail`, `sed`, `tee` and redirects in Bash | Names the two real gaps |
| 4 | A judge favours its own outputs (§9.3) | Panickssery et al., arXiv v1; NeurIPS 2024 | PARTIAL: the draft said "its own model family's"; the paper tested a model judging its own generations, not a family | "its own outputs" |
| 5 | Open-weight judges disagreed with themselves across runs (§9.3) | Haldar and Hockenmaier, arXiv v1; Findings of EMNLP 2025 | CONFIRMED: the judges were Llama 3.1 70B, a DeepSeek-R1 distillation and Qwen3 32B, and a majority vote over runs agreed better with humans | None |
| 6 | In an online finance setting without reliable feedback, self-evolving context could fall below the base model (§13) | ACE, arXiv v3, Table 2 | PARTIAL: only one ACE cell fell below the base model (67.3 against 70.7), and ACE's own average there stayed above it; another adaptive method fell below on both datasets | "could fall", and the setting named |
| 7 | An unguided LLM judge was near chance at picking the better of two skills (§13) | "From raw experience to skill consumption", arXiv v1, §5.2 | CONFIRMED: 46.4% on 151 pairs with no rubric. The 73.8% with a rubric is in-sample | None |
| 8 | Curated skills reviewed by maintainers raised pass rates; skills a model wrote for itself did worse than none; focused sets of at most three skills beat larger or exhaustive bundles (§13) | SkillsBench, arXiv v4 and v1 | CONFIRMED: v4 reports -8.1 to -11.5 points for self-written skills, and v1 to v3 a smaller -1.3 points | Uses the paper's "curated" and its at-most-three wording |
| 9 | Automated attribution rarely found the decisive failing step (§13) | Who&When, arXiv v3; ICML 2025 | CONFIRMED: 53.5% at naming the agent, 14.2% at the step | None |
| 10 | Users accept 93% of manual Claude Code permission prompts; Anthropic warns that over time such prompts lead to approval fatigue (§18) | Anthropic, "Claude Code auto mode" (Mar 2026) | PARTIAL: the draft said Anthropic attributes the 93% to fatigue. The post states the 93% with no population or method, and names fatigue as the risk without tying the figure to it | Reworded to what the post says |
| 11 | Across 33,596 agent PRs, submitter attributes carried about 76% of a merge model's explanatory power (§18) | Yoshioka et al., arXiv v1; MSR 2026 | CONFIRMED: 76.15% of the likelihood-ratio chi-square, pooled agent model, correlational. "Merge rate is not a quality signal" is our inference | That inference is now graded [D] |
| 12 | In 161 classified flaky-test fixes, 24% changed the code under test, and 94% of those fixed a bug there (§18) | Luo et al., FSE 2014, opened at its ACM page through the DOI | CONFIRMED: 161 of 201 commits could be classified; the authors advise against simply removing or disabling flaky tests | "classified"; "a bug" for "a real bug" |
| 13 | In an injection experiment, two models copied a flaky assertion from the example tests into 42% to 78% of the new C++ tests they wrote (§18) | Berndt et al., arXiv; ICSE-SEIP 2026, Table 5 | PARTIAL: the assertion was injected into every example test, C++ tests only, two models on two systems | "injection experiment", "C++" |
| 14 | Put risky changes behind a flag that starts off and canary configuration changes; give each flag an owner and an expiry (§18) | Tang et al., SOSP 2015; Meinicke et al., ICSE-SEIP 2020 | PARTIAL: one tag on the whole sentence overstated it. Tang supports the first two clauses; owner and expiry come from Meinicke's nine interviews | Tag split by clause |
| 15 | GitLab's daily backup had silently produced nothing (§18) | GitLab postmortem, Feb 2017 | CONFIRMED | None |
| 16 | Intercom auto-approves a share of PRs with no human reviewer; its agent won't approve large or broad PRs, every approval is logged, any engineer can ask for a human review (§19.2) | Intercom, Apr 2026 | CONFIRMED: "over 19%" (19.2% in a chart caption) | "won't approve" for "excluded"; graded [P, vendor]; revert rates left out |
| 17 | Across 2.23 million package recommendations pooled over 16 off-the-shelf models, about 20% named packages that don't exist; commercial models averaged at least 5% (§5.4) | Spracklen et al., arXiv v3; USENIX Security 2025 | PARTIAL: about 20% is pooled and weighted toward 13 open-source models; "with no tools" is not the paper's term | Pooled and commercial figures; "off-the-shelf" |
| 18 | UTBoost's added tests and a fixed log parser exposed 345 SWE-bench patches wrongly marked as passing, changing 18 of 44 Lite and 11 of 45 Verified rankings (§19.1 item 5) | UTBoost, ACL 2025, §4.4 | PARTIAL: the draft blamed weak tests alone; the 345 also come from a parser fix | Both causes, and the counts |
| 19 | After Cursor adoption in 806 repos, velocity gains faded within about two months while warnings and complexity stayed up (§19.1 item 6) | He et al., arXiv v3; MSR 2026 | CONFIRMED: difference-in-differences against 1,380 matched repos; persistence is shown up to six months | None |
| 20 | In one pre-registered trial with 52 participants on a 35-minute task, the AI-assisted group scored 17% lower on a quiz about the library (§19.1 item 6) | Shen and Tamkin, arXiv v2 | WRONG on "(exploratory)": the quiz gap is the pre-registered main comparison; only the breakdowns by question type are exploratory. The 17% is the authors' own figure | "pre-registered", sample and task length, "(the authors' figure)" |

The advice that follows several of these claims (cut a generated CLAUDE.md, keep a hidden check, judge with another model family, quarantine with an owner, ask the agent to explain code you will own) is graded [D]. Its direction matches the sources; none of them tested it as an intervention.

## Gaps no source covers

- Whether the prior-art rule, or any written CLAUDE.md rule, beats Claude Code's default behaviour end to end.
- Defect or revert rates for agent PRs merged without human review, measured independently.
- Agents deleting or weakening tests in real repositories; only benchmark measurements exist.
- Progressive delivery of agent-authored changes: all the flag, canary and rollback evidence concerns human-authored changes.
- Whether evals built from your own traces predict production failures better than synthetic ones.
- Long-run skill effects of delegating to agents, beyond a single short task.

## Sources

Every source behind every verdict above. "Playbook" marks the 19 that playbook §20 also lists; the rest stand behind a verdict here and are not cited in the playbook. Grades follow playbook §0.

**Tests, evals, context, autonomy and delivery**
- Zhong, Raghunathan, Carlini, ImpossibleBench (preprint, 2025) [R], playbook: https://arxiv.org/abs/2510.20270
- METR, Recent frontier models are reward hacking (blog, Jun 2025) [P]: https://metr.org/blog/2025-06-05-recent-reward-hacking/
- UTBoost (ACL 2025) [R], playbook: https://aclanthology.org/2025.acl-long.189
- Hora and Robbes, Are coding agents generating over-mocked tests? (MSR 2026) [R]: https://arxiv.org/abs/2602.00409
- Micco, Flaky tests at Google and how we mitigate them (Google Testing Blog, May 2016) [P]: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- Luo, Hariri, Eloussi, Marinov, An empirical analysis of flaky tests (FSE 2014) [R], playbook: https://doi.org/10.1145/2635868.2635920
- Memon et al., Taming Google-scale continuous testing (ICSE-SEIP 2017) [R]: https://research.google/pubs/taming-google-scale-continuous-testing/
- Inozemtseva and Holmes, Coverage is not strongly correlated with test suite effectiveness (ICSE 2014) [R]: https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf
- Berndt et al., Flakiness of LLM-generated tests for database systems (ICSE-SEIP 2026) [R], playbook: https://arxiv.org/abs/2601.08998
- SkillsBench (preprint, v4 2026) [R], playbook: https://arxiv.org/abs/2602.12670
- Agentic Context Engineering (ICLR 2026) [R], playbook: https://arxiv.org/abs/2510.04618
- From raw experience to skill consumption (preprint, 2026) [R], playbook: https://arxiv.org/abs/2605.23899
- Mind the Sim2Real gap in user simulation (COLM 2026) [R]: https://arxiv.org/abs/2603.11245
- Panickssery, Bowman, Feng, LLM evaluators recognize and favor their own generations (NeurIPS 2024) [R], playbook: https://arxiv.org/abs/2404.13076
- Haldar and Hockenmaier, Rating Roulette (Findings of EMNLP 2025) [R], playbook: https://arxiv.org/abs/2510.27106
- Zhang et al., Which agent causes task failures and when? (ICML 2025) [R], playbook: https://arxiv.org/abs/2505.00212
- Gloaguen et al., Evaluating AGENTS.md (preprint, v3 2026) [R], playbook: https://arxiv.org/abs/2602.11988
- IFScale, How many instructions can LLMs follow at once? (preprint, Distyl AI, 2025) [R]: https://arxiv.org/abs/2507.11538
- Du et al., Context length alone hurts LLM performance (Findings of EMNLP 2025) [R]: https://arxiv.org/abs/2510.05381
- Agent READMEs: context files for agentic coding (preprint, 2026) [R]: https://arxiv.org/abs/2511.12884
- Anthropic, Measuring AI agent autonomy in practice (Feb 2026) [P], playbook (already cited): https://www.anthropic.com/research/measuring-agent-autonomy
- Anthropic, Claude Code auto mode (Mar 2026) [P], playbook (already cited): https://www.anthropic.com/engineering/claude-code-auto-mode
- Claude Code docs, permissions (Read and Edit rules) [P], playbook (already cited): https://code.claude.com/docs/en/permissions
- Pinna et al., Task-stratified analysis of agent PR acceptance (MSR 2026 Mining Challenge) [R]: https://arxiv.org/abs/2602.08915
- Yoshioka et al., Developer and agentic pull requests (MSR 2026) [R], playbook: https://arxiv.org/abs/2601.18749
- Intercom, AI is approving our pull requests (Apr 2026) [P, vendor], playbook: https://intercom.com/blog/ai-is-approving-our-pull-requests-heres-how-we-made-it-safe
- Google SRE Workbook, Appendix C, results of postmortem analysis [P]: https://sre.google/workbook/postmortem-analysis/
- Google SRE book, ch. 26, Data integrity [P]: https://sre.google/sre-book/data-integrity/
- Tang et al., Holistic configuration management at Facebook (SOSP 2015) [R], playbook: https://sigops.org/s/conferences/sosp/2015/current/2015-Monterey/printable/008-tang.pdf
- Meinicke et al., Feature flags and configuration options (ICSE-SEIP 2020) [R], playbook: https://par.nsf.gov/servlets/purl/10157116
- SEC order, Knight Capital, Release 34-70694 (Oct 2013) [P]: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
- Google Cloud incident report, 12 Jun 2025 [P]: https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW
- GitLab, Postmortem of database outage of January 31 (Feb 2017) [P], playbook: https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
- DORA, Accelerate State of DevOps 2024 [P]: https://dora.dev/research/2024/dora-report/2024-dora-accelerate-state-of-devops-report.pdf
- DORA 2025 report [P], playbook (already cited): https://dora.dev/research/2025/dora-report/
- He et al., Cursor adoption, development velocity and code quality (MSR 2026) [R], playbook: https://arxiv.org/abs/2511.04427
- Humlum and Vestergaard, NBER working paper 33777 (May 2025, revised March 2026) [R]: https://www.nber.org/papers/w33777
- Paradis et al., Enterprise RCT at Google (ICSE-SEIP 2025) [R]: https://arxiv.org/abs/2410.12944
- Shen and Tamkin, How AI impacts skill formation (preprint, Anthropic, 2026) [R], playbook: https://arxiv.org/abs/2601.20245
- Nygard, Documenting architecture decisions (2011) [P]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR, Markdown Architectural Decision Records [P]: https://adr.github.io/madr/
- Zimmermann, Architectural decisions, the making of (Y-statements) [P]: https://www.ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html
- Stripe Sessions 2024, Craft and beauty: the business value of form in function (friction logging) [P]: https://stripe.com/sessions/2024/craft-and-beauty-the-business-value-of-form-in-function

**Prior art and reuse (the guarded rule in §5.4)**
- CodeRAG-Bench (Findings of NAACL 2025) [R]: https://arxiv.org/abs/2406.14497
- EvoR, Evolving retrieval for code generation (Findings of EMNLP 2024) [R]: https://arxiv.org/abs/2402.12317
- On mitigating code LLM hallucinations with API documentation (ICSE-SEIP 2025) [R]: https://arxiv.org/abs/2407.09726
- Repoformer, Selective retrieval (ICML 2024) [R]: https://arxiv.org/abs/2403.10059
- BeyondSWE (preprint, 2026) [R]: https://arxiv.org/abs/2603.03194
- PlanSearch (ICLR 2025) [R]: https://arxiv.org/abs/2409.03733
- CodeTree (NAACL 2025) [R]: https://arxiv.org/abs/2411.04329
- Anthropic, Prompting best practices (current docs) [P]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- More code, less reuse: agent PRs (MSR 2026) [R]: https://arxiv.org/abs/2601.21276
- Shortcutting the fix: agentic exploits in SWE benchmarks (preprint, 2026) [R]: https://arxiv.org/abs/2609.06780
- Spracklen et al., Package hallucinations by code-generating LLMs (USENIX Security 2025) [R], playbook: https://arxiv.org/abs/2406.10279
- He et al., Six million suspected fake stars in GitHub (ICSE 2026) [R]: https://arxiv.org/abs/2412.13459
- Ohm et al., Backstabber's knife collection (pre-print of a DIMVA 2020 paper) [R]: https://arxiv.org/abs/2005.09535
- Ladisa et al., Taxonomy of attacks on open-source supply chains (IEEE S&P 2023) [R]: https://arxiv.org/abs/2204.04008
- GitHub Docs, Licensing a repository [P]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- Wolter et al., Open source license inconsistencies on GitHub (ACM TOSEM 2023, per the authors' publication list; 2022 manuscript) [R]: https://oss.cs.fau.de/wp-content/uploads/2022/10/wolter-2022-open.pdf
- Baltes and Diehl, Usage and attribution of Stack Overflow code snippets (Empirical Software Engineering, 2019) [R]: https://arxiv.org/abs/1802.02938
- Software Engineering at Google, ch. 21, Dependency management [P]: https://abseil.io/resources/swe-book/html/ch21.html
- Zahan et al., Do software security practices yield fewer vulnerabilities? (ICSE-SEIP 2023) [R]: https://arxiv.org/abs/2210.14884

## Held back

Read in the sweep but not admitted, so nothing above rests on them.

| Source | Why it was held back |
|---|---|
| Cui et al., three Copilot field experiments (Management Science, 2026) | Neither checker could open the primary page; only an author copy was read. Re-check before admitting |
| A Claude Code team post on code review (claude.dev, Oct 2026) | The content matched, but authorship and domain ownership were not confirmed: the canonical claude.com address returned 404. It is the only source found that describes a risk-tiered approval ladder |
| Vercel, "58% of PRs merge without human review" | The primary page returned 404; it was read only through a mirror |
| Baker et al. on chain-of-thought monitoring (OpenAI, 2025) and METR's MALT dataset | Both survived the check, but they disagree on whether reading the chain of thought helps, and they concern training and eval monitors more than harness practice |
| Gunawi et al., cloud outage study (SoCC 2016) | The checkers could not open the paper |
| Falessi et al. (2006) on documenting design alternatives | One check only; a 50-student experiment on one case |
| Lam et al., flaky tests at Microsoft (ISSTA 2019) | One check only |
| Vendor telemetry and magazine surveys on AI and burnout | No primary study behind them |
