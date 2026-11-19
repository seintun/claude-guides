# Evidence: agentic practices, November 2026

The research record behind playbook 0.7 (2026-11-18). It holds who said what, what was checked against a primary page, where the sources disagree, and which playbook section each finding changed. Every new attributed claim in [playbook 0.7](../playbook/agent-harness-playbook.md) cites this file or a URL listed here.

Checked 2026-11-18. Method:
- **Research reports.** Two research reports of 2026-11-18: one on the Claude Code changelog and docs and on three named practitioners, one on about 30 other voices (labs, vendors, independents, academic groups). Each proposed playbook changes. Where a report and the ledger below disagree, the ledger wins.
- **`doc-checker` passes.** Three passes read the primary pages for the Claude Code docs and changelog, for the research papers and METR pages, and for the vendor engineering posts.
- **Raw docs fetches.** The Claude Code docs and changelog were fetched as raw Markdown (`.md` pages), not as model-written summaries.
- **Browser reads.** The X threads, the YouTube transcripts and OpenAI's harness post were read in a browser, in full, because no fetch tool reaches X. The Karpathy post of 2026-10-02 was read the same way.
- **Re-check rule.** A claim that a researcher read only through a model-written summary stays at [S] or is dropped, unless a later pass read the page itself.

Grades follow playbook [§0](../playbook/agent-harness-playbook.md#0-how-to-use-this-file): **[P]** primary, **[S]** secondary, **[R]** research, **[D]** design inference. Evidence type: **measured** (numbers from a run), **opinion** (experience or argument), **vendor** (a company reporting on its own product). Venue: **peer-reviewed** (a named venue) or **preprint**.

Quotes are short and verbatim from the page named. Everything else is paraphrase.

## Expert roster

Credibility here rests on first-party, dated, concrete work, not follower counts. "Checked" says whether a pass on 2026-11-18 read the primary page: **yes** means the claims the playbook uses were confirmed; **read only** means a researcher read it and no later pass re-checked it, so the playbook does not rest on it.

| Name | Role | Primary works (date) | Type | Venue | Checked |
|---|---|---|---|---|---|
| Boris Cherny | Anthropic, Claude Code | [2 Jan 2026 setup thread](https://x.com/bcherny/status/2007179832300581177); [31 Jan 2026 team-tips thread](https://x.com/bcherny/status/2017742741636321619); [Latent Space](https://latent.space/p/claude-code) (May 2025) | opinion | none | yes (X in a browser; 31 Jan from search cards, quoted parts only) |
| Andrej Karpathy | Independent | [Notes of 26 Jan 2026](https://x.com/karpathy/status/2015883857489522876); [context engineering](https://x.com/karpathy/status/1937902205765607626) (2025-06-25); [Software Is Changing (Again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ) (2025-06-18); [understanding LLM outputs](https://x.com/karpathy/status/2105819303471976479) (2026-10-02 UTC) | opinion | none | yes |
| Lauren Tan | Grok Bot, SpaceXSI; tooling Cursor | [All Code Is Slop (Except Mine)](https://www.youtube.com/watch?v=O_zcc6Xl12g), AI Engineer, published 2026-11-14 | opinion, self-reported figures | none | yes (transcript read in full) |
| Prithvi Rajasekaran | Anthropic Labs | [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) | vendor, measured (one task) | none | yes, with two figures unverified |
| Justin Young | Anthropic | [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (2025-11-26) | vendor, opinion | none | yes |
| Jeremy Hadfield, Barry Zhang and others | Anthropic | [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025-06-13) | vendor, measured | none | yes (model names unverified) |
| Erik Schluntz, Barry Zhang | Anthropic | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024-12-19) | vendor, opinion | none | yes |
| Mikaela Grace and others | Anthropic | [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (2026-01-09) | vendor, measured in part | none | yes |
| Nicholas Carlini | Anthropic Safeguards | [C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) (2026-02-05) | vendor, measured (one run) | none | yes |
| Lance Martin | Anthropic | [Components of agent memory](https://www.anthropic.com/engineering/components-of-agent-memory) (2026-11-06) | vendor, opinion | none | yes |
| Anthropic | Vendor | [How we contain Claude](https://www.anthropic.com/research/how-we-contain-claude) (2026-05-25); [Redesigning source control](https://www.anthropic.com/research/redesigning-source-control) (2026-10-13); [Claude Code docs](https://code.claude.com/docs/en/best-practices) | vendor, P | none | yes (source-control post: cite its narrow wording only) |
| Ryan Lopopolo | OpenAI | [Harness engineering](https://openai.com/index/harness-engineering/) (2026-02-11) | vendor, opinion, one repo | none | yes (browser read) |
| OpenAI evals group | OpenAI | [Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) (2026-02-23) | vendor, measured audit | none | yes (via Wayback) |
| Wilson Lin | Cursor | [Scaling agents](https://cursor.com/blog/scaling-agents) (Jan 2026); [Self-driving codebases](https://cursor.com/blog/self-driving-codebases) (Feb 2026); [Swarm economics](https://cursor.com/blog/agent-swarm-model-economics) (Jul 2026) | vendor, measured (one task) | none | yes |
| Walden Yan | Cognition | [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents) (2025-06-12); [Multi-agents: what's actually working](https://cognition.com/blog/multi-agents-working) (2026-04-22) | vendor, opinion | none | yes |
| Tyler McGoffin | GitHub Copilot Applied Science | [Agent-driven development](https://github.blog/2026-03-31-agent-driven-development-in-copilot-applied-science/) (2026-03-31) | vendor, opinion | none | yes |
| Simon Willison | Independent | [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) (2025-06-16) | opinion, incident-based | none | yes |
| Geoffrey Huntley | Independent | [Ralph](https://ghuntley.com/ralph/) (2025-07-14) | opinion | none | yes |
| Dex Horthy | HumanLayer | [Getting AI to Work in Complex Codebases](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md) (no author or date on the page) | vendor, opinion | none | yes (40 to 60% is his unmeasured hint) |
| Mitchell Hashimoto | Independent | [My AI adoption journey](https://mitchellh.com/writing/my-ai-adoption-journey) (2026-02-05) | opinion | none | yes |
| Hamel Husain, Shreya Shankar | Independent | [Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) (2026-09-18) | opinion, procedural | none | yes |
| METR | Independent lab | [Time horizon 1.1](https://metr.org/blog/2026-01-29-time-horizon-1-1/) (2026-01-29); [productivity trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (2025-07-10) and [update](https://metr.org/blog/2026-02-24-uplift-update/) (2026-02-24); [reward hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/) (2025-06-05) | measured [R: METR report] | METR reports; the trial also has an arXiv preprint | yes |
| Kim, Liu and others | Google Research, DeepMind, MIT | [Towards a science of scaling agent systems](https://arxiv.org/abs/2512.08296), v3 of 8 Apr 2026 | measured | preprint | yes (full text) |
| Cemri, Pan, Zaharia, Gonzalez, Stoica and others | UC Berkeley | [MAST](https://arxiv.org/abs/2503.13657) | measured | peer-reviewed (NeurIPS 2025 poster) | yes |
| Aleithan and others | Academic | [SWE-Bench+](https://arxiv.org/abs/2410.06992) | measured | preprint | yes |
| Chroma | Vendor | [Context Rot](https://www.trychroma.com/research/context-rot) | vendor, measured | report | yes |
| Liu, Liang and others | Stanford | [Lost in the Middle](https://arxiv.org/abs/2307.03172) | measured | peer-reviewed (TACL 2024) | yes |
| Huang and others | Academic | [LLMs cannot self-correct reasoning yet](https://arxiv.org/abs/2310.01798) | measured | peer-reviewed (ICLR 2024) | yes |
| Shinn and others | Academic | [Reflexion](https://arxiv.org/abs/2303.11366) | measured | peer-reviewed (NeurIPS 2023, per search) | yes |
| SlopCodeBench authors | Academic | [arXiv 2603.24755](https://arxiv.org/abs/2603.24755), v2 | measured | preprint | yes |
| Yao and others | Academic | [tau-bench](https://arxiv.org/abs/2406.12045) | measured | peer-reviewed (ICLR 2025, as cited in playbook §19.1) | yes (applies to gpt-4o) |
| Yang and others | Princeton | [SWE-agent](https://arxiv.org/abs/2405.15793) | measured | peer-reviewed (NeurIPS 2024) | yes (12.5%) |
| Xia and others | Academic | [Agentless](https://arxiv.org/abs/2407.01489) | measured | peer-reviewed (FSE 2025) | yes (32.00% at $0.70) |
| Thariq Shihipar, Ken Aizawa, Cat Wu, Michael Bolin, Alexander Embiricos, Thorsten Ball, Quinn Slack, Eno Reyes, Addy Osmani, Armin Ronacher, Kent Beck, Kieran Klaassen, Dan Shipper, Harper Reed, Steve Yegge, Gergely Orosz | Various | Listed in the research reports with URLs | opinion or vendor | none | read only |

Karpathy's blog posts of 2025 and 2026 (the Sequoia Ascent write-up, "Verifiability", "HackerTube"), his autoresearch and llm-council repos and the LLM Wiki gist were read by researchers and are not re-checked here. The playbook already cites autoresearch and llm-council at [P] from earlier versions. 0.7 adds nothing new from the others.

## Verification ledger

Each row: the claim as the playbook now states it, the verdict, the primary URL, and a short quote or figure from the page. TRUE means the page says it, within scope.

### Claude Code docs and changelog

Raw Markdown pages, read 2026-11-18. Base URLs: [changelog](https://code.claude.com/docs/en/changelog), [best practices](https://code.claude.com/docs/en/best-practices), [permission modes](https://code.claude.com/docs/en/permission-modes), [workflows](https://code.claude.com/docs/en/workflows), [sub-agents](https://code.claude.com/docs/en/sub-agents), [hooks](https://code.claude.com/docs/en/hooks), [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks), [goal](https://code.claude.com/docs/en/goal), [context window](https://code.claude.com/docs/en/context-window), [model config](https://code.claude.com/docs/en/model-config), [memory](https://code.claude.com/docs/en/memory).

| Claim | Verdict | Where | Note |
|---|---|---|---|
| Auto mode is the default for interactive sessions: v2.1.283 for third-party providers or telemetry off, then v2.1.284 for every plan and provider; HIPAA sessions use auto from v2.1.326 | TRUE | changelog | The permission-modes and best-practices pages cite v2.1.283 for the general default; the changelog entries are the precise source |
| Auto mode pauses after 3 consecutive or 20 total blocks; in `-p` the action is denied and Claude keeps going | TRUE | permission modes | |
| `-p` with no mode set starts in Manual: the permission-modes page states it without conditions; changelog v2.1.302 limits it to third-party providers, telemetry off or a fresh install | TRUE, both cited | permission modes; changelog | The logged-in, telemetry-on case is not stated anywhere |
| 33 hook events | TRUE | hooks | None added in the window |
| Subagent nesting 3, concurrency 20 | TRUE | sub-agents | |
| `autoCompactWindow` (v2.1.296) and the Agent-tool `effort` parameter (v2.1.292) | TRUE | sub-agents; changelog | |
| Workflows: 16 concurrent agents, 1,000 per run, 4,096 items per call; a large-workflow warning above 25 agents or 1.5M projected tokens; `ultracode` does not trigger from `-p` or scheduled prompts | TRUE | workflows | |
| Workflows from `-p` have five approval routes: an allow rule, auto mode, a PreToolUse hook that returns allow, `--permission-prompt-tool`, an SDK `canUseTool` callback | TRUE | workflows | The earlier reports named one |
| `/loop`: 1-minute minimum, 7-day expiry, 50 tasks per session; cloud tasks 1-hour minimum | TRUE | scheduled tasks | |
| Self-paced `/loop` ends when a turn finishes without rescheduling (v2.1.319); the docs page is stale | TRUE | changelog | `CLAUDE_CODE_LOOP_KEEPALIVE` appears only in the changelog |
| v2.1.325: sandboxed Bash follows the normal permission flow, so `sandbox.autoAllowBashIfSandboxed` is opt-in; scheduled tasks ask before running a skill that declares `allowed-tools` or hooks, unless `Skill(name)` is allowed | TRUE | changelog | The `Skill(name)` rule appears only in the changelog |
| `sandbox.failIfUnavailable` was added in v2.1.83, not v2.1.328 | CORRECTION | changelog | The first research report was wrong |
| Stop hook is overridden after 8 consecutive blocks (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) | TRUE | hooks | |
| `onFailure` on command and HTTP hooks (v2.1.295), `mcp_tool` hooks (v2.1.328), SDK callbacks (v2.1.317) | TRUE | changelog | |
| Up to 12 prompt or agent hooks run at once | TRUE | hooks | The "24-hook cap" in the first report was NOT FOUND; drop it |
| What pauses and clears `/goal`; the evaluator "doesn't run commands or read files" | TRUE | goal | |
| Removed: `subagentStatusLine` (v2.1.323), `pluginDigests` (v2.1.325), the plugin `agent` setting (v2.1.323), `claude project purge` renamed `claude purge` (v2.1.288); Opus 4.8 fast mode removed 2026-11-30; Code Mode experimental (v2.1.323) | TRUE | changelog | |
| Mods arrived in v2.1.287 | TRUE | changelog | No "experimental" label found; write "no status label" |
| Best-practices "old advice" table: IMPORTANT and ALL CAPS emphasis, "Use subagents to protect your context window" and others; "at forty of them"; a reviewer "will always find *something*"; `--max-turns` and `--max-budget-usd`; no "Explore, plan, implement, commit" heading | TRUE | best practices | |
| What survives compaction; auto-compaction at about 967K tokens with a 100K minimum | TRUE | context window; model config | Path-scoped rules are dropped, then reloaded on demand. The table and its prose conflict; the playbook says "reloaded on demand" |
| Auto memory loads 200 lines or 25 KB | TRUE | memory | |
| Compaction re-reads "up to five" recent files, most recently modified first; skills are "capped at 5,000 tokens per skill and 25,000 tokens total" | TRUE | context window | Confirmed on the raw page |
| Best practices, "Let Claude run without you": "it's worth going through these five questions"; item 4 asks what stops the run (`--max-turns`, `--max-budget-usd`, a spend limit); item 5 asks where the result goes and who signs off | TRUE | best practices | `--max-turns` semantics are not documented on the headless page |
| Best practices, "Deterministic and non-deterministic instructions": hooks for rules with "zero exceptions" | TRUE | best practices | The page does not state a ladder; the ladder in Law 8 is design advice [D] |
| Changelog v2.1.328 is dated 19 November 2026 on the changelog page | TRUE | changelog | One day after the research date. Six version numbers were not found (2.1.297, 298, 313, 315, 320, 324), so the playbook does not call the list complete |

### Research papers and METR

| Claim | Verdict | URL | Short quote or figure |
|---|---|---|---|
| Google/MIT (arXiv 2512.08296): 180 configurations in v1 and v2, 260 across 6 benchmarks in v3 (8 Apr 2026, abstract checked 2026-11-18); negative returns above a 45% single-agent baseline; errors amplified 17.2x against 4.4x (CI 14.3 to 20.1) | TRUE | https://arxiv.org/abs/2512.08296 | v3 says planning "-39% to -70%"; "39-70%" is v1 and v2 wording. +80.9% is v1; the current figure is +80.8%, Finance Agent only. Preprint |
| MAST: 1,600+ traces, failure taxonomy | TRUE | https://arxiv.org/abs/2503.13657 | NeurIPS 2025 poster |
| METR time horizon: doubling about every 7 months over 2019 to 2025; 89 days is the since-2024 fit only; TH1.1 overall 196.5 days; Opus 4.5 about 320 minutes (CI 170 to 729) | TRUE | https://metr.org/blog/2026-01-29-time-horizon-1-1/ | |
| METR trial 2025: 16 developers, 246 tasks, 19% slower, expected 24% faster | TRUE | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | |
| METR update, Feb 2026: original developers -18% (CI -38 to +9); new developers -4% (CI -15 to +9) | TRUE | https://metr.org/blog/2026-02-24-uplift-update/ | METR calls it "only very weak evidence" |
| METR reward hacking: RE-Bench 30.4% (39 of 128) of runs; HCAST 0.7%; telling the model not to cheat had a "nearly negligible effect" | TRUE | https://metr.org/blog/2025-06-05-recent-reward-hacking/ | "o3 1 to 2%" NOT FOUND; dropped |
| OpenAI audit, 23 Feb 2026: 59.4% of 138 audited problems flawed; reporting of SWE-bench Verified stopped | TRUE | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | |
| SWE-Bench+ figures | TRUE | https://arxiv.org/abs/2410.06992 | Preprint |
| Chroma Context Rot: evaluates 18 LLMs; focused prompts of about 300 tokens against the full LongMemEval input of about 113k; "significantly higher performance on focused prompts" | TRUE | https://www.trychroma.com/research/context-rot | Vendor report. The interview-reported "degradation from about 10k tokens" is dropped |
| Lost in the Middle | TRUE | https://arxiv.org/abs/2307.03172 | TACL 2024 |
| Huang et al. | TRUE | https://arxiv.org/abs/2310.01798 | ICLR 2024 |
| Reflexion: 91 against 80 pass@1 on HumanEval | TRUE | https://arxiv.org/abs/2303.11366 | NeurIPS 2023, per search |
| SlopCodeBench v2: no end-to-end solve; erosion in 77% of trajectories | TRUE | https://arxiv.org/abs/2603.24755 | v1 said 80%. Preprint |
| tau-bench result applies to gpt-4o; SWE-agent 12.5%; Agentless 32.00% at $0.70 | TRUE | arXiv 2406.12045, 2405.15793, 2407.01489 | |

### Vendor engineering posts

| Claim | Verdict | URL | Short quote or figure |
|---|---|---|---|
| Multi-agent research system: 90.2%; about 15x chat tokens; token use explains 80% of variance; a coding caveat; subagents return lightweight references; context past 200K truncated | TRUE | https://www.anthropic.com/engineering/multi-agent-research-system | Model names not verified |
| Harness design: "over 20x more expensive"; the solo core feature was broken; resets needed on Sonnet 4.5, not on Opus 4.5; "every component ... encodes an assumption" | TRUE | https://www.anthropic.com/engineering/harness-design-long-running-apps | The $9 against $200 and 20 minutes against 6 hours figures are UNVERIFIED; the playbook uses "over 20x" |
| Effective harnesses: features marked done early; "unacceptable to remove or edit tests" | TRUE | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | |
| C compiler: 16 agents, about 2,000 sessions, under $20,000, 99%, lock files | TRUE | https://www.anthropic.com/engineering/building-c-compiler | |
| Demystifying evals: 42% to 95% after grader fixes; 20 to 50 tasks; pass^k; a git-history exploit | TRUE | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | |
| Memory components (2026-11-06) | TRUE | https://www.anthropic.com/engineering/components-of-agent-memory | |
| Containment (2026-05-25): about 93% of permission prompts approved | TRUE | https://www.anthropic.com/research/how-we-contain-claude | |
| Building effective agents never says "start simple" | TRUE (negative) | https://www.anthropic.com/engineering/building-effective-agents | Quote only "finding the simplest solution possible" |
| Cursor, January: flat lock coordination collapsed | TRUE | https://cursor.com/blog/scaling-agents | |
| Cursor, February: handoff fields, scratchpad rewritten, judge and integrator removed | TRUE | https://cursor.com/blog/self-driving-codebases | |
| Cursor, July: $1,339 for the Opus 4.8 hybrid against $10,565 for GPT-5.5 alone; 70,000+ merge conflicts against fewer than 1,000 | TRUE | https://cursor.com/blog/agent-swarm-model-economics | Vendor, one task |
| Cognition: both posts | TRUE | https://cognition.com/blog/dont-build-multi-agents ; https://cognition.com/blog/multi-agents-working | |
| Willison, the lethal trifecta, 2025-06-16 | TRUE | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | Use the full title |
| Huntley, Ralph, 2025-07-14 | TRUE | https://ghuntley.com/ralph/ | |
| Horthy: "Getting AI to Work in Complex Codebases"; 40 to 60% context | TRUE | https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md | No author or date on the page; the 40 to 60% is a hint, not measured |
| Hashimoto, 2026-02-05 | TRUE | https://mitchellh.com/writing/my-ai-adoption-journey | |
| Husain and Shankar: at least 100 traces until saturation; 30 to 50 for open coding | TRUE | https://hamel.dev/blog/posts/evals-faq/ (2026-09-18) | |
| McGoffin, 2026-03-31: guardrails "akin to contract testing that can only be updated by humans" | TRUE | https://github.blog/2026-03-31-agent-driven-development-in-copilot-applied-science/ | |

### Browser pulls

Read in full in a browser on 2026-11-18. Wording is checked for the parts quoted.

- **Lauren Tan, talk** [P]: the words are hers; all figures are self-reported. Her tool is Cursor, not Claude Code. Her employer is SpaceXSI (Grok Bot).
- **Boris Cherny threads** [P]: the 2 Jan thread and the 31 Jan thread (31 Jan read from search-result cards, not each post page).
- **Karpathy posts and talk** [P].
- **OpenAI, Harness engineering** [P, vendor]: 0 manual lines; about 1/10th the time; about 1M lines; about 1,500 PRs from 3 engineers, a team of 7 later; one big AGENTS.md "failed in predictable ways"; a roughly 100-line AGENTS.md as a map; custom linters and "taste invariants"; Chrome DevTools Protocol in the runtime; runs of "upwards of six hours"; "minimal blocking merge gates"; agent-to-agent review; the setup "should not be assumed to generalize".
- **Karpathy on explaining outputs** (2026-10-02 UTC) [P, opinion]: ask the model for an explanation in a controlled language such as ASD-STE100, then diagrams, then HTML pages, then explainer videos.

ASD-STE100 checks (`doc-checker`, 2026-11-18):
- The history is TRUE. It began as AECMA Simplified English in the 1980s for aircraft maintenance and is maintained by ASD STEMG. Issue 9 (January 2025) made it an international standard, so write "standard", not "specification". [P] https://asd-europe.org/news-media/news-events/news/simplified-technical-english-asd-ste100-issue-9
- The specific rules (word limits, one meaning per word) are unverified from the official site, which returns 403. The playbook states no word limit.
- Comprehension evidence is partial and old. Holmback, Shubert and Spyridakis (CLAW 1996, summarising a 1995 study, 130 students) found better comprehension on the complex procedure only, and the most benefit for non-native speakers. Chervak, Drury and Ouellette (1996, maintenance technicians) found a similar pattern. [R, 1990s] https://aclanthology.org/www.mt-archive.info/90/CLAW-1996-Holmback.pdf
- None of these tests LLM output or agent reviewers. A 2025 randomized preprint on plain-language LLM text (n=4563) found a 3.9% comprehension gain in general readers. [R, preprint] https://arxiv.org/abs/2505.01980
- A diagram tool (CodeMap, 15 developers) improved perceived usefulness only, not error detection. [R, ICPC 2026] https://arxiv.org/abs/2504.04553
- No study tests Karpathy's ordering. It is his design advice [P, opinion]; adopting it in a receipt is [D].

## Per-post URL index

### Boris Cherny, 2 Jan 2026 thread [P]

Root: https://x.com/bcherny/status/2007179832300581177

| Post | URL | Content |
|---|---|---|
| 1/ | https://x.com/bcherny/status/2007179833990885678 | 5 parallel sessions in the terminal |
| 2/ | https://x.com/bcherny/status/2007179836704600237 | 5 to 10 on the web, plus the phone |
| 3/ | https://x.com/bcherny/status/2007179838864666847 | Opus 4.5 with thinking for everything |
| 4/ | https://x.com/bcherny/status/2007179840848597422 | A shared CLAUDE.md. "Anytime we see Claude do something incorrectly we add it to the CLAUDE.md" |
| 5/ | https://x.com/bcherny/status/2007179842928947333 | `@.claude` on PRs; compounding engineering |
| 6/ | https://x.com/bcherny/status/2007179845336527000 | "Most sessions start in Plan mode"; Claude "can usually 1-shot it" |
| 7/ | https://x.com/bcherny/status/2007179847949500714 | Slash commands in git; `/commit-push-pr` |
| 8/ | https://x.com/bcherny/status/2007179850139000872 | `code-simplifier` and `verify-app` subagents |
| 9/ | https://x.com/bcherny/status/2007179852047335529 | A PostToolUse formatter for "the last 10%" |
| 10/ | https://x.com/bcherny/status/2007179854077407667 | No skip-permissions; a shared pre-allow list |
| 11/ | https://x.com/bcherny/status/2007179856266789204 | MCP and CLIs |
| 12/ | https://x.com/bcherny/status/2007179858435281082 | A background verify agent; a Stop hook "more deterministically"; ralph-wiggum; `dontAsk` or skip-permissions only "in a sandbox" |
| 13/ | https://x.com/bcherny/status/2007179861115511237 | "give Claude a way to verify its work", with an estimate of "2-3x the quality" |

### Boris Cherny, 31 Jan 2026 team-tips thread [P]

Read from search-result cards, not each post page. Only the parts quoted here are checked.

Root: https://x.com/bcherny/status/2017742741636321619

| Tip | URL | Content |
|---|---|---|
| 1 | https://x.com/bcherny/status/2017742743125299476 | Spin up 3 to 5 git worktrees at once; "the single biggest productivity unlock" |
| 2 | https://x.com/bcherny/status/2017742745365057733 | "Start every complex task in plan mode"; a second Claude reviews the plan as a staff engineer |
| 3 | https://x.com/bcherny/status/2017742747067945390 | After a correction, ask Claude to update CLAUDE.md so it doesn't repeat the mistake |
| 4 | https://x.com/bcherny/status/2017742748984742078 | Skills committed to git |
| 5 | https://x.com/bcherny/status/2017742750473720121 | "Go fix the failing CI tests. Don't micromanage how." |
| 6 | https://x.com/bcherny/status/2017742752566632544 | "Grill me on these changes"; "Prove to me this works" |
| 7 | https://x.com/bcherny/status/2017742753971769626 | Ghostty; `/statusline` for context usage |
| 8 | https://x.com/bcherny/status/2017742755737555434 | "use subagents" for more compute; offload tasks "to keep your main agent's context window clean"; route permission requests to Opus through a hook |
| 9 | https://x.com/bcherny/status/2017742757666902374 | `bq` for analytics |
| 10 | https://x.com/bcherny/status/2017742759218794768 | Learning output styles |

### Karpathy [P]

- Notes of 26 Jan 2026: https://x.com/karpathy/status/2015883857489522876. About 80% agent coding since December; agent swarms "too much for right now"; "watch them like a hawk"; models make "wrong assumptions on your behalf" and run along with them; no pushback; "a little too sycophantic"; "Things get better in plan mode"; bloat and orthogonal edits that persist "despite a few simple attempts to fix it via instructions in CLAUDE.md"; "give it success criteria and watch it go"; tests first, a browser MCP, naive-correct first and then optimize, declarative over imperative; the speedup is "possibly a lot more an expansion"; skill atrophy.
- Context engineering, 2025-06-25: https://x.com/karpathy/status/1937902205765607626
- Understanding the outputs of language models, 2026-10-02 UTC (1 Oct local): https://x.com/karpathy/status/2105819303471976479. Tips in increasing order: a controlled-language explanation, diagrams, HTML pages, explainer videos. Summary: work will "rise up the abstractions into oversight and understanding". Grady Booch replies that UML covers diagrams.
- "Software Is Changing (Again)", YC talk, 2025-06-18 [P, auto-captions]: https://www.youtube.com/watch?v=LCEmiRjPEtQ

| Time | Content |
|---|---|
| 20:23 | The autonomy slider |
| 22:16 | "we as humans are doing the verification" |
| 22:56 | "AI on the leash" |
| 23:55 | Small incremental chunks |
| 24:32 | Concrete prompts |
| 34:18 | A Markdown file for agents. The captions spell it "lm.txt"; the playbook says "an llms.txt-style Markdown file" |
| 35:01 | Markdown docs |

### Lauren Tan, "All Code Is Slop (Except Mine)" [P: talk transcript]

URL: https://www.youtube.com/watch?v=O_zcc6Xl12g (published 2026-11-14). Auto-captions. All figures are her own.

| Time | Content |
|---|---|
| 0:42 | 3,000 PRs in a month |
| 2:03 | The trust pyramid: deterministic layers first, prose last |
| 3:08 | A correction becomes a deterministic check |
| 3:34 | Review volume from about 3 PRs a day to about 300 |
| 5:26 | `useEffect` banned in product code |
| 6:10 | Boundaries enforced by directory structure |
| 6:56 and 8:20 | Markdown justifications; about 99% of comments banned |
| 9:10 | "nothing left to review" |
| 9:48 to 10:45 | Review the verification artifacts; a feature map; CLIs inside skills |
| 10:02 | Runtime verification is "giving your agent a way to run the code for itself" and use debugging tools such as the Chrome DevTools protocol |
| 16:44 | "most product code that we land no longer really requires deep human review" |
| 10:50 | TLA+ and Lean: "not a silver bullet" |
| 12:05 | Most tokens go to verification |
| 13:32 | 11,000 PRs a month, 0.5% reverts |
| 15:32 | Automating a loop that produces slop "just produces more slop" |
| 16:21 | Release fuzzing, then auto-merge |

## Discrepancies and how each was resolved

| Item | Version A | Version B | Resolution in 0.7 |
|---|---|---|---|
| Boris on plan mode | Report 1: "Most sessions start in Plan mode" has no primary source | His own post 6/ of 2 Jan 2026 says it | Report 1 was wrong. [P, Jan 2026]. Docs now default to auto mode, so the playbook keeps plan mode for anything non-trivial and dates his June 2026 move to auto mode at [S] |
| Auto mode default | Docs pages cite v2.1.283 | Changelog: v2.1.283 (third-party or telemetry off), v2.1.284 (all) | Write "v2.1.283 to v2.1.284", cite the changelog |
| `-p` default | permission-modes: Manual, no conditions | Changelog v2.1.302: only third-party, telemetry off or fresh install | Scope the sentence; cite both |
| 24-hook cap | Report 1 | Docs: 12 concurrent prompt or agent hooks | 12; the 24 was not found |
| `sandbox.failIfUnavailable` | Report 1: v2.1.328 | Changelog: v2.1.83 | v2.1.83 |
| Workflows from `-p` | One approval route | Five routes | Five |
| Self-paced `/loop` fallback | Docs: about 20-minute fallback | v2.1.319: ends without rescheduling | Follow the changelog; docs lag |
| Mods status | Report 1: "preview" | No label found | "no status label" |
| Karpathy file name | Transcript: "lm.txt" | Playbook: "llms.txt" | "an llms.txt-style Markdown file" |
| Google/MIT figures | v1 and v2: "39-70%", +80.9% | v3: planning "-39% to -70%", +80.8% | Name the version; cite v3 as the current text |
| METR horizon | 89 days | About 7 months over 2019 to 2025 | 7 months is the long fit; 89 days is the since-2024 fit only |
| METR reward hacking | Report 2: "o3 1 to 2%" | Page: RE-Bench 30.4%, HCAST 0.7% | Drop the o3 figure |
| Harness-design cost | Report 2: $9 against $200 | Page: "over 20x more expensive" | Use "over 20x"; the two figures are unverified |
| Husain and Shankar traces | Report 2: at least 30 | Page: at least 100 until saturation; 30 to 50 for open coding | 100 until saturation; 30 to 50 to start |
| Horthy title | Several names | Document: "Getting AI to Work in Complex Codebases" | Use the title |
| Tan PR counts | Earlier recaps: about 2,500 | Transcript: 3,000 personal, 11,000 team | Transcript, labelled self-reported |
| Tan's tool | A third-party "Poteto Mode" Claude Code skill | Transcript: Cursor | Say Cursor |
| Anthropic post paths | /engineering/ | /research/ | Both resolve; the playbook uses the path each post is fetched from |
| Judge value | Anthropic harness post: evaluator worth it beyond solo reliability | Cursor dropped judge and integrator in February | Task-dependent |
| Building effective agents | "start simple" as a quote | Page says "finding the simplest solution possible" | Quote only the page |

## Kept at [S] or dropped

| Claim | Action | Reason |
|---|---|---|
| Boris's June 2026 move to auto mode; loops, routines, phone work, fleet-scale claims | Kept [S] | Recaps only |
| "2-3x" from verification | Moved to [P] as his own estimate | Post 13/ of the 2 Jan thread |
| Tan's earlier-talk figures | Kept [S] | Recaps |
| Cat Wu, the Embiricos podcasts, Yegge, Beck, Orosz | Kept [S], not used for new claims | Recaps, mirrors, a 403 |
| Lopopolo throughput | [P, vendor], never an outcome | One repo, no baseline |
| Cursor outcomes and costs | [P, vendor], dated to the post | No replication |
| Tan's revert rate, comment ban, "nothing left to review", auto-merge | Recorded as single-team self-reports, not defaults | No independent audit |
| Tan's "70% of tokens go to verification" | Dropped | A peer's figure; she says only "most" |
| Boris and Karpathy atrophy exchange | Dropped | One snippet |
| Boris: 10 to 20% of sessions thrown away; CLAUDE.md of 2 or 100 lines | Dropped | Conflicting snippets |
| METR 12-hour and 1.5-hour horizons; METR "o3 1 to 2%" | Dropped | Recap only, or not on the page |
| Chroma "10k tokens" | Dropped | Interview-reported |
| Later Lopopolo figures (GPT-5.5, "Symphony", token counts) | Dropped | Podcast or aggregator only |
| Cognition Devin Review rates; Amp release counts; GitHub token savings; Factory readiness score | Dropped | Vendor, no baseline, or a secondary summary |
| Mods preview status; `--max-turns` semantics; teams concurrency | Marked unverified | Not found in fetched pages |

## From finding to playbook section

| Finding | Playbook section |
|---|---|
| Correction ladder: fix at the highest layer that works; prose last | [Law 8](../playbook/agent-harness-playbook.md#law-8-turn-every-correction-into-a-rule), §15 |
| Boris's "2-3x" is his own estimate [P] | [Law 2](../playbook/agent-harness-playbook.md#law-2-verification-multiplies-quality), §19 |
| Claude Code limits, defaults and removals as of v2.1.328 | [§3A](../playbook/agent-harness-playbook.md#3a-claude-code-feature-map) |
| Plan mode: Boris and Karpathy [P]; auto mode is the current default | [Law 6](../playbook/agent-harness-playbook.md#law-6-plan-before-building), §3A |
| Single writer by default; conditions for parallel writers; planner and worker; routing by cost | [§6](../playbook/agent-harness-playbook.md#6-orchestration-patterns) |
| Brief contents, reviewer rule | [§7](../playbook/agent-harness-playbook.md#7-delegation-protocol) |
| Context kept small by structure; isolation ranking; context rot | [§8](../playbook/agent-harness-playbook.md#8-context-engineering), [Law 4](../playbook/agent-harness-playbook.md#law-4-context-is-a-budget-not-a-bin) |
| Layered check order; runtime verification; plain-English receipts | [§9](../playbook/agent-harness-playbook.md#9-verification-stack), [§9.3](../playbook/agent-harness-playbook.md#93-rules-that-keep-verification-honest), [§9.4](../playbook/agent-harness-playbook.md#94-receipt-format) |
| Trifecta check; 93% approvals | [§10](../playbook/agent-harness-playbook.md#10-guardrails) |
| End-to-end run with minimal supervision | [§11.6](../playbook/agent-harness-playbook.md#116-end-to-end-with-minimal-supervision), [§11.5](../playbook/agent-harness-playbook.md#115-risks-of-running-without-watching) |
| Eval sets from real failures; leaderboards decay | [§13](../playbook/agent-harness-playbook.md#13-evals-and-learning) |
| New failure modes and anti-patterns | [§14](../playbook/agent-harness-playbook.md#14-model-failure-modes-and-countermeasures), [§15](../playbook/agent-harness-playbook.md#15-anti-patterns) |
| Dated evidence rows and superseded claims | [§19](../playbook/agent-harness-playbook.md#19-proven-orchestration-what-the-evidence-says) |
| Every URL above | [§20](../playbook/agent-harness-playbook.md#20-sources) |
