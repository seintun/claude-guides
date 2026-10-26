# Session log

The work happened on 2026-10-24, in one Claude Code session in the Claude desktop app. Each step lists the owner's request and the outcome.

| # | Request | Outcome |
|---|---|---|
| 1 | Teach goals, orchestration, the workflow and its phases, self-checks, running continuously, growth and planning, in simple terms with diagrams | The "Orchestrating Claude" page, published as a claude.ai artifact |
| 2 | As an expert drawing on Boris Cherny and Andrej Karpathy, write the findings up as knowledge for building an orchestration harness | `playbook/agent-harness-playbook.md` |
| 3 | Use 5–10 subagents with Firecrawl or Exa to research best practices: Linear, GitHub Actions, checks, gates, guardrails, terminal to cloud to unattended work, pain point to action items. Should I grill like Matt Pocock? | Research folded into the page and the playbook. The answer: yes, with rules (Lesson 3, playbook §5.2) |
| 4 | Include the research in the artifacts | New lessons and playbook sections, with sources |
| 5 | Verify the artifacts in Brave | Brave (Claude in Chrome) never connected, so the owner approved the built-in browser and signed in there |
| 6 | Have an independent subagent fact-check the artifacts | Corrections made. Examples: routines renamed to scheduled tasks; `--cloud` does not open a PR; council call count; BMAD agents; Ralph attribution; Karpathy dates; autoresearch's read-only rule is an instruction, not a lock |
| 7 | Have one fresh reviewer confirm the corrections | Confirmed, and new issues fixed |
| 8 | Add cited links with tooltips on the P, S, R and D tags | 130 linked tags and 11 tooltip-only tags |
| 9 | Find proven, research-backed orchestration from reputable builders and companies, with no YouTubers or marketing | Lesson 17 and playbook §19 |
| 10 | Make the tooltip theme match light and dark | Done |
| 11 | D tags should not jump to Sources | D and legend tags became tooltip-only |
| 12 | Clicking a tag should open the source in a new tab | Done |
| 13 | Run independent UI/UX, learning-psychology and charting reviews, and write an issue for a builder | Three reviews (`issues/reviews/ux.md`, `lx.md`, `vz.md`), and `issues/orchestrating-claude-ux.md` with 13 children in playbook templates L, B and D |
| 14 | Build it with the default answers, starting with the check script | Child 0: `checks/` with the v11 baseline (12 PASS, 57 FAIL) |
| 15 | Parallelize independent work with subagents | Playbook navigation, the fact-check and three content drafts ran in parallel; the lead stayed the only writer on the page |
| 16 | Ship for a production launch within 30 minutes | Version 12 at the same URL: 20 of 20 checks pass in 6 views |
| 17 | Put the phase buttons under the diagram, with no flashing or moving | Version 13 |
| 18 | Center the phase nav and use short labels | Version 14: "← Prev" and "Next →" |
| 19 | Fix the review bugs and blocking chart items, then finish children 8, 11 and 12 | Version 15. Two agents redrew four diagrams in parallel |
| 20 | Show glossary definitions as tooltips instead of jumping | Version 15 |
| 21 | Mark quiz answers green and red | Version 15 |
| 22 | The final independent review found a blocking quiz keyboard bug and mid-width text problems | Version 16: 21 of 21 checks pass in 8 views |
| 23 | Compile everything into one searchable HTML file, in a Git repo with an agents file | This repository |

## Tools and agents used

- **Browsers:** the built-in browser pane, for checking the published page while signed in; Playwright (Chromium), for the automated checks on a local wrapped copy.
- **Research:** Firecrawl, Exa and web search through research subagents. `doc-checker` handled primary-source fact checks.
- **Reviewers:** fresh Sonnet subagents, given files and briefs and never the builder's conclusions.
- **Builders in parallel:** a Sonnet subagent for the playbook (child 5); drafting agents for the glossary, takeaways and running example; two figure agents that wrote SVG drafts for the lead to splice in.
- **Palette check:** the dataviz skill's `validate_palette.js`, which ruled out green against red on the evidence chart.
