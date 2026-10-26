# Sources for judging /prompt

What Anthropic's own guidance and published research say about writing prompts and briefing agents. The `/prompt` scorers grade against this list (`tests/live/prompt/briefs/score-external.md`). It holds no scores and no findings about any version of the skill; those are in [prompt-skill-review.md](prompt-skill-review.md).

Two `doc-checker` passes fetched every source on 2026-10-25. Each item paraphrases its source. **VERIFIED** means the source says this; **PARTLY** means it says something narrower, and the item is worded to match the source.

## Anthropic guidance

Sources:
- **BP:** [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- **S55:** [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- **CC:** [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- **HL:** [Claude Code headless mode](https://code.claude.com/docs/en/headless)
- **CW:** [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows)
- **BEA:** [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- **MAR:** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **CTX:** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

| ID | Recommendation | Source | Check |
|---|---|---|---|
| G1 | Write for a capable newcomer who lacks your context; be clear and direct | BP | VERIFIED |
| G2 | Give the reason behind an instruction, not only the instruction | BP | VERIFIED |
| G3 | Say what to do rather than what not to do (given as a formatting tip) | BP | VERIFIED |
| G4 | Examples steer format reliably; make them relevant, varied and clearly marked (3 to 5 suggested) | BP | PARTLY |
| G5 | Use XML tags when a prompt mixes instructions, context, examples and inputs | BP | VERIFIED |
| G6 | Prefer general instructions to prescriptive step lists; thinking is configured, not prompted, and a request to write out reasoning may be declined | BP, S55 | PARTLY |
| G7 | Chain prompts only to inspect intermediate outputs or enforce a pipeline | BP | PARTLY |
| G8 | Put long material near the top, with the query and instructions after it | BP | VERIFIED |
| G9 | Soften aggressive emphasis written to fight under-triggering; emphasise at most one line | BP, CC | PARTLY |
| G10 | Be specific about output format and constraints; match the prompt's style to the output wanted | BP | VERIFIED |
| G11 | Give the agent a check it can run: tests, a build, a screenshot | CC | PARTLY |
| G12 | Separate research and planning from implementation | CC | VERIFIED |
| G13 | Reference specific files, name constraints, point to example patterns | CC | VERIFIED |
| G14 | Tests are not removed or edited to make them pass; a wrong test is reported instead | BP | VERIFIED |
| G15 | Correct early, clear context between tasks, and use subagents to investigate | CC | VERIFIED |
| G16 | For unattended runs, restrict tools and permissions; test autonomous agents in sandboxes | HL, BEA | PARTLY |
| G17 | Start with the simplest solution; add complexity only when needed | BEA | VERIFIED |
| G18 | Include stopping conditions such as a maximum number of iterations | BEA | VERIFIED |
| G19 | Brief each subagent with an objective, an output format, tool and source guidance, and task boundaries | MAR | VERIFIED |
| G20 | Put effort-scaling rules in the prompt; agents misjudge effort on their own | MAR | VERIFIED |
| G21 | An evaluator loop pays off when the evaluation criteria are clear | BEA | VERIFIED |
| G22 | Use the smallest set of high-signal tokens; write at the right altitude, neither brittle logic nor vague guidance | CTX | VERIFIED |
| G23 | Subagents return condensed summaries, or store work externally and pass back references | CTX, MAR | VERIFIED |
| G24 | Self-contained specs name files and interfaces, state what is out of scope, and end with an end-to-end check | CC | VERIFIED |
| G25 | When the asked-for work is done and checked, stop; add nothing unasked | S55 | VERIFIED |
| G26 | For unattended runs, say what success looks like and what to do with the results | CW | VERIFIED |
| G27 | Brief a reviewer narrowly: the work, what to check it against, and what counts as a finding | CC | VERIFIED |
| G28 | Write instructions as imperatives, not questions | BP | VERIFIED |
| G29 | Keep a skill's SKILL.md short (under 500 lines) as an overview, and move detail into files one level deep that it links and Claude loads when needed | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices); [Claude Code skills](https://code.claude.com/docs/en/skills) | VERIFIED |

Not found on any current Anthropic page: an instruction to tell Claude it is doing test-driven development. G14 is the nearest verified guidance.

## Research

| ID | Finding | Source | Venue |
|---|---|---|---|
| R1 | Without external feedback, models struggle to self-correct, and performance can drop after a self-correction step | [Huang et al.](https://arxiv.org/abs/2310.01798) | ICLR 2024 |
| R2 | LLM judges show position, verbosity and self-enhancement bias; judging twice with the order swapped, and counting only consistent wins, mitigates position bias | [Zheng et al.](https://arxiv.org/abs/2306.05685) | NeurIPS 2023 Datasets and Benchmarks |
| R3 | LLM evaluators score their own outputs higher, and can recognise them | [Panickssery et al.](https://arxiv.org/abs/2404.13076) | NeurIPS 2024 |
| R4 | Models use information at the start and end of a long context best, and the middle worst | [Liu et al.](https://arxiv.org/abs/2307.03172) | TACL 2024 |
| R5 | Instruction-following falls as the number of instructions grows; the best model reached 68% at 500 instructions, and models degrade in three different patterns | [Jaroslawicz et al.](https://arxiv.org/abs/2507.11538) | NeurIPS 2025 workshop |
| R6 | Frontier models reward-hack coding tasks by editing tests or scoring code, or deleting failing tests | [METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/); [ImpossibleBench](https://arxiv.org/abs/2510.20270) | Blog post; preprint |
| R7 | With reliable tool feedback, two to three correction rounds give most of the benefit; feedback from the model alone gives weaker returns (QA, maths and toxicity tasks, not unit tests) | [Gou et al.](https://arxiv.org/abs/2305.11738) | ICLR 2024 |
| R8 | When challenged, assistants sometimes drop correct answers: they change the answer in 32% (GPT-4) to 86% (Claude 1.3) of cases | [Sharma et al.](https://arxiv.org/abs/2310.13548) | ICLR 2024 |
| R9 | Equivalent formatting changes (separators, casing, spacing) swing few-shot accuracy by up to 76 points on one open model; rewording was not studied | [Sclar et al.](https://arxiv.org/abs/2310.11324) | ICLR 2024 |
