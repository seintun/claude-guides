# Watchlist

The sources `/refresh scan` reads. Each row has an id, which `state.json` uses for its cursor. Keep this list at 40 rows or fewer: that is the cap on sources per run.

Seeded 2026-11-18 from the roster in [research/agentic-practices-2026-11.md](../research/agentic-practices-2026-11.md). Index-page URLs for blogs were not all fetched when this list was written. If a URL fails, the run lists the source under "Gaps not read" and the fix goes here.

How to read each source (the "Read with" column):

- **fetch**: a fetch tool or `curl` on an allowed host: `WebFetch`, a search tool, or `curl -fsSL`. Prefer the raw page. For `code.claude.com/docs`, append `.md` to a page URL to get its raw Markdown.
- **browser**: a signed-in browser only (the Claude in Chrome extension or the built-in browser pane). Never a fetch tool.
- **transcript**: in a browser, open the video and read its transcript panel. Never a fetch tool.

**Never run any fetch tool, `curl` or search on `x.com`, `twitter.com` or `linkedin.com`.** If no browser is connected, list those sources under "Gaps not read".

## Claude Code

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| cc-changelog | Claude Code changelog | https://code.claude.com/docs/en/changelog | fetch | Entries newer than `claude_code_changelog.last_seen_version` in `state.json`: defaults, removals, limits, new hooks, permission changes |
| cc-best-practices | Best practices | https://code.claude.com/docs/en/best-practices | fetch | Changed advice, new "old advice" rows |
| cc-permission-modes | Permission modes | https://code.claude.com/docs/en/permission-modes | fetch | Defaults, auto mode limits |
| cc-workflows | Workflows | https://code.claude.com/docs/en/workflows | fetch | Limits, approval routes |
| cc-sub-agents | Sub-agents | https://code.claude.com/docs/en/sub-agents | fetch | Nesting, concurrency, frontmatter fields |
| cc-hooks | Hooks | https://code.claude.com/docs/en/hooks | fetch | Event count, new fields, caps |
| cc-scheduled-tasks | Scheduled tasks | https://code.claude.com/docs/en/scheduled-tasks | fetch | Loop limits, cloud tasks |
| cc-desktop-scheduled | Desktop scheduled tasks | https://code.claude.com/docs/en/desktop-scheduled-tasks | fetch | Catch-up rules, permissions, worktree option |
| cc-goal | Goal | https://code.claude.com/docs/en/goal | fetch | What pauses or clears a goal |
| cc-context-memory | Context window, model config, memory | https://code.claude.com/docs/en/context-window | fetch | Compaction, memory limits; also read `/model-config` and `/memory` when the changelog hints at a change |

Read the docs pages only when the changelog suggests an edit. Record in `state.json` the date each was last read.

## Anthropic and OpenAI

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| anthropic-engineering | Anthropic engineering index | https://www.anthropic.com/engineering | fetch | New posts on harnesses, agents, evals, memory |
| anthropic-research | Anthropic research index | https://www.anthropic.com/research | fetch | Containment, safety, source-control posts |
| claude-blog | Claude blog | https://claude.com/blog | fetch | Product and feature posts |
| openai-index | OpenAI index pages for Codex, evals and engineering | https://openai.com/news/engineering/ | browser | Harness, Codex and eval posts. Returns 403 to fetch tools (checked 2026-11-18); read it in a browser |

## Tool vendors

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| cursor-blog | Cursor blog | https://cursor.com/blog | fetch | Multi-agent and scaling posts with numbers |
| cognition-blog | Cognition blog | https://cognition.com/blog | fetch | Multi-agent and context posts |
| amp-news | Amp news | https://ampcode.com/news | fetch | Agent design notes |
| github-ai-blog | GitHub blog, AI and ML | https://github.blog/ai-and-ml/ | fetch | Copilot agent practice |
| factory-blog | Factory blog | https://factory.com/news | fetch | Droid and agent-run posts |

## Labs and papers

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| metr-blog | METR blog | https://metr.org/blog | fetch | Time horizon, productivity, reward hacking |
| arxiv-coding-agents | arXiv query: coding agents | https://arxiv.org/search/?searchtype=all&order=-announced_date_first&query=%22coding+agents%22 | fetch | New preprints on agents that write code. Newest first; verify any claim on the paper itself |
| arxiv-multi-agent | arXiv query: multi-agent | https://arxiv.org/search/?searchtype=all&order=-announced_date_first&query=%22multi-agent%22+LLM | fetch | Scaling, failure taxonomies |
| arxiv-evals | arXiv query: evals and benchmarks | https://arxiv.org/search/?searchtype=all&order=-announced_date_first&query=agent+benchmark+audit | fetch | Benchmark audits, grader studies |
| arxiv-context | arXiv query: long context | https://arxiv.org/search/?searchtype=all&order=-announced_date_first&query=long+context+agents | fetch | Context-use and memory studies |

A preprint is graded R and noted as a preprint. A peer-reviewed venue is named only when the venue's own page says so.

## Independent practitioners

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| willison-blog | Simon Willison | https://simonwillison.net/ | fetch | Prompt injection, the trifecta, tool notes |
| husain-blog | Hamel Husain | https://hamel.dev/blog/ | fetch | Evals method |
| hashimoto-writing | Mitchell Hashimoto | https://mitchellh.com/writing | fetch | Adoption and workflow notes |
| huntley-blog | Geoffrey Huntley | https://ghuntley.com/ | fetch | Loops and unattended runs |

## X accounts (browser only)

Open each profile in a signed-in browser and read the posts since the cursor. Read a post on its own page before grading a claim [P]; a claim known only from a recap is [S]. Only the accounts the research roster names are listed. Add a handle here after you have checked it on the profile.

| Id | Account | URL | Read with | Look for |
|---|---|---|---|---|
| x-bcherny | Boris Cherny (Anthropic, Claude Code) | https://x.com/bcherny | browser | Setup threads, team tips, feature notes |
| x-karpathy | Andrej Karpathy | https://x.com/karpathy | browser | Notes on agent coding, verification, context |
| x-poteto | Lauren Tan | https://x.com/poteto | browser | Agent and tooling practice |
| x-simonw | Simon Willison | https://x.com/simonw | browser | Short notes that precede blog posts |

## YouTube (transcript panel in a browser)

| Id | Source | URL | Read with | Look for |
|---|---|---|---|---|
| yt-ai-engineer | AI Engineer | https://www.youtube.com/@aiDotEngineer | transcript | New talks on agents and harnesses |
| yt-anthropic | Anthropic | https://www.youtube.com/@anthropic-ai | transcript | Talks and product walkthroughs |
| yt-yc | Y Combinator | https://www.youtube.com/@ycombinator | transcript | Talks by agent builders |

Read only the talks whose titles fit the guide's scope. A transcript is a primary source for what the speaker said. Figures a speaker reports about their own team are noted as self-reported.

## Adding or removing a source

Edit this file and `state.json` in the same change. Keep ids unique, URLs complete and the total at 40 rows or fewer. A source that returns nothing useful for 8 scans in a row is a candidate to drop; say why in the commit.
