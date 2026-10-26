# Draft: density (child 11)

Draft text for child 11, "Density: takeaways, starter sets and grouping". Nothing here edits the page.

**Base.** Checked against `site/orchestrating-claude.html` as of 13:58 on 2026-10-24 (md5 `6bb595b5498719d436e93894af0fd9da`). Children 1 and 2 (navigation, reading paths, levels, the collapsed Lesson 8 example) and part of child 7 (the Lesson 17 chart and finding cards) are already in. Every quoted page text, URL and data-src below was re-checked against that version by script. Insertion points use section ids and heading text, not line numbers, because the page is still being edited.

**Conventions.**
- Lesson id = the section id (`#loop` ... `#evidence`).
- "Reference" = a `<details class="reference">`, closed by default. Its summary says what is inside and how many items. "Show all N" = a `<details>` holding the remaining rows. Both copy the page's existing `details.table-view`; no new JS.
- Evidence tags move as whole elements. Do not retype a URL. The href and data-src values below are for checking.
- No new facts. Every line below is page text, rearranged or shortened. The few places that are advice rather than page text are marked and listed under Flags.

---

## 1. Takeaways (17)

New first paragraph under each h2, above `p.intro`:

```html
<h2>…</h2>
<p class="takeaway">…</p>
<p class="intro">…</p>
```

Every takeaway is 24 words or fewer, so a one-word label ("Takeaway") in the same paragraph still stays within 25. It adds no new jargon: each term it uses is one the lesson explains.

| # | id | Takeaway | Words |
|---|---|---|---|
| 1 | `#loop` | You set the goal and the check; Claude runs the loop. Without a real check, it stops when it feels finished. | 21 |
| 2 | `#rules` | Give outcomes and a way to prove them, load only what the next step needs, and enforce must-happen rules in code. | 21 |
| 3 | `#discovery` | By the end, every issue has an outcome, a runnable check and a boundary, and open questions are written down, not guessed. | 22 |
| 4 | `#goals` | State the result you want and two to five checks that prove it, plus when Claude must stop and ask. | 20 |
| 5 | `#phases` | Ten phases take big tasks from goal to ship. Critique and Learn get skipped, but matter most when Claude works alone. | 21 |
| 6 | `#orchestration` | Send helpers wide reading, parallel jobs and fresh-eyes review. Keep small jobs, and jobs that touch the same files, in the lead. | 22 |
| 7 | `#patterns` | Plan, critique, build is the default for most coding. Use a specialist pattern only when your task matches its "Use it when" column. | 23 |
| 8 | `#toolbox` | Start with five features: CLAUDE.md for standing rules, Plan mode, Skills, Subagents and Hooks. Look up the rest when a job needs them. | 23 |
| 9 | `#selfcheck` | The builder never grades its own work. Ask for a receipt: each criterion marked PASS, FAIL or NOT RUN, with its command. | 22 |
| 10 | `#guardrails` | Deny rules win in every mode. Never give one session all three: private data, untrusted content, a way to send data out. | 22 |
| 11 | `#running` | Any run without you needs a stop condition, a retry cap, a cost ceiling and a home for its results. | 20 |
| 12 | `#pipeline` | You act at the edges: write the issue, delegate, approve. Protect the gate files so the agent can't switch off its own checks. | 23 |
| 13 | `#growing` | After ten tasks, the trend in your scorecard shows where to invest. Growing also means pruning rules that never fire. | 20 |
| 14 | `#prompts` | Pick the template for the step you're on; paste Self-check before Claude wraps up and Retro after a real task. | 20 |
| 15 | `#failures` | Match the symptom to its likely cause, then apply the fix. After two failures with the same cause, stop and get a second opinion. | 24 |
| 16 | `#checklist` | Before: a checkable goal. During: an approved plan. After: a receipt with commands and a retro that produces one to three changes. | 22 |
| 17 | `#evidence` | The evidence backs one writer by default, outside checks over self-critique, and measuring repeated runs and cost, not single wins. | 20 |

---

## 2. Lesson 10 starter set (`#guardrails`)

Position: directly after the takeaway, before `p.intro`. Reuse `.panel` styling; no new component.

> **Start with these 3**
> 1. Deny rules for secrets. A deny always beats an allow, in every mode. `P`
> 2. Sandbox on, no unsandboxed retries. It covers shell commands only. `P`
> 3. Remove one leg of the lethal trifecta in every session: private data, untrusted content, or a way to send data out. `P`
>
> **Good enough for a solo developer:** these three are enough to start. The rest of this lesson is for teams and unattended runs. `D`

Where each line comes from (all on the page now):

| Line | Page text it is built from |
|---|---|
| 1 | Prevent list: "Deny rules for secrets". Facts: "an allow can't override a deny, and deny rules hold in every mode". |
| 2 | Prevent list: "Sandbox on, with no unsandboxed retries". Facts: "The sandbox only covers shell commands." |
| 3 | Prevent list: "Drop one trifecta leg per session". Figure caption: private data, untrusted content, a way to send data out; "Remove at least one of the three in every session." |
| solo line | Advice, not page text. It carries a D tag (the page's standard "Our own advice" tag). The page does not say who the other controls are for; see Flags. |

Tags on these four lines (copies of tags that already exist in the lesson; the URL set does not change, but each focusable tag adds a tab stop, so this adds 4):

| Line | Tag | href | data-src |
|---|---|---|---|
| 1 Deny rules | P | `https://code.claude.com/docs/en/permissions` | Claude Code docs: Permissions |
| 2 Sandbox | P | `https://code.claude.com/docs/en/sandboxing` | Claude Code docs: Sandboxing |
| 3 Trifecta | P | `https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/` | Simon Willison: The lethal trifecta (Jun 2025) |
| Solo developer line | D | none (tooltip only) | Our own advice, built from the sources on this page |

---

## 3. Lesson 6 reality check (`#orchestration`)

Position: after the context-chart `<figure>` (the one with `#ctx-chart`), immediately before the `div.two-col` whose first panel is the h3 "Send a helper when". Reuse the existing `.rule-box` markup (a `<span>` label plus a `<p>`), as Lesson 9's "Golden rule" does.

```html
<div class="rule-box">
  <span>Reality check</span>
  <p>One writer by default. Fan out only for parallel, read-heavy work; steps that depend on each other go worse with more agents. External checks beat self-critique. See <a href="#evidence">Lesson 17</a>.</p>
</div>
```

- 31 words including the label (limit 45). Ends with "See Lesson 17."
- It cites only Lesson 17: finding 01, "One writer by default" ("Fan out only for parallel, read-heavy work. Steps that depend on each other go worse with more agents."), and finding 03, "External checks beat self-critique".
- It repeats no number and no tag; those stay in Lesson 17.

---

## 4. Lesson 7 grouping (`#patterns`)

### 4a. The 11 pattern rows

The table has 11 rows (the issue text says 10).

| # | Row | Group | Why (page text) |
|---|---|---|---|
| 1 | Plan, critique, build | **Default, highlighted** | "The default for most coding" |
| 2 | Goal loop | Default | "One session with a provable end state" |
| 3 | Lead + workers | Default | "Wide reading and research" |
| 4 | Prompt chain | Specialist | "The stages are known in advance" |
| 5 | Parallel sections | Specialist | "Parts don't depend on each other" |
| 6 | Evaluator + optimizer | Specialist | "The criteria are clear" |
| 7 | Initializer + worker | Specialist | "Projects that span many sessions" |
| 8 | Ralph loop | Specialist | "A well-specified backlog with strong tests" |
| 9 | Hill-climbing | Specialist | "One cheap, trustworthy metric" |
| 10 | Council | Specialist | "Judgment calls with no test" |
| 11 | Day shift, night shift | Specialist | "A backlog of well-sliced issues" |

- **Row to highlight as the default:** row 1, Plan, critique, build. Mark it with a visible "Default" badge in the name cell as well as an `--accent-soft` row fill, so colour is not the only signal.
- **The one-writer loop is row 2, Goal loop.** No row is literally called that. Goal loop is the only loop row that runs in one session: `/goal` re-checks after each turn until the condition holds. Plan, critique, build is also single-writer, but it is already its own Default row. If the owner reads "one-writer loop" differently, the alternative is row 6, Evaluator + optimizer.
- **Order inside Default:** one-writer shapes first, then the multi-agent one (rows 1, 2, 3).
- **Group-header labels** (a full-width `<tr class="group"><th colspan="4">`):
  - "Default: start with these" (4 words)
  - "Specialist: use when the task fits" (6 words)
- **Disclosure:** Default (3 rows) is visible. The Specialist header and its 8 rows sit inside "Show all 11".
- **Columns:** the fifth column ("Pattern from") merges into the name cell, so the table has 4 columns and the tag sits beside the name. Nothing is lost: the source name stays in each tag's data-src.
- **One-sentence edit** to the note under the table: 'The "watch out for" column is our advice; the tag beside each name shows where the pattern comes from.' (Keep its D tag.)

Tags that move from the last cell into the name cell:

| # | Row | Tag | href | data-src |
|---|---|---|---|---|
| 1 | Plan, critique, build | P | `https://code.claude.com/docs/en/best-practices` | Claude Code docs: Best practices |
| 2 | Goal loop | P | `https://code.claude.com/docs/en/goal` | Claude Code docs: /goal |
| 3 | Lead + workers | P | `https://www.anthropic.com/engineering/multi-agent-research-system` | Anthropic: How we built our multi-agent research system (Jun 2025) |
| 4 | Prompt chain | P | `https://www.anthropic.com/engineering/building-effective-agents` | Anthropic: Building effective agents (Dec 2024) |
| 5 | Parallel sections | P | `https://www.anthropic.com/engineering/building-effective-agents` | Anthropic: Building effective agents (Dec 2024) |
| 6 | Evaluator + optimizer | P | `https://www.anthropic.com/engineering/building-effective-agents` | Anthropic: Building effective agents (Dec 2024) |
| 7 | Initializer + worker | P | `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents` | Anthropic: Effective harnesses for long-running agents (Nov 2025) |
| 8 | Ralph loop | P | `https://ghuntley.com/ralph/` | Geoffrey Huntley: Ralph |
| 9 | Hill-climbing | P | `https://github.com/karpathy/autoresearch` | karpathy/autoresearch on GitHub |
| 10 | Council | P | `https://github.com/karpathy/llm-council` | karpathy/llm-council on GitHub |
| 11 | Day shift, night shift | P | `https://www.youtube.com/watch?v=-QFHIoCo-Ko` | Matt Pocock: full AI coding workflow walkthrough (AI Engineer) |

### 4b. "Pick the shape by the task", short version

Position: after the pattern table's note, before "Named methods, compared". Lesson 17 keeps the full 5-row table. The cell text below is copied from Lesson 17; only the row order changes (the shared-state row goes first because it is the default; highlight it the same way).

| Task shape | Shape that held up | Evidence |
|---|---|---|
| Steps with shared state (most feature work) | One agent writes; helpers only read or review | Multi-agent lost 39–70% on sequential planning `R`; Cognition keeps writes single-threaded `P` |
| Many independent, read-heavy parts | A lead with read-only helpers and a central coordinator | Anthropic's research system won by 90.2% on breadth-first research `P` |
| A large mechanical change across many files | A scripted pipeline; the model edits; checks gate every file | Airbnb, Google, Spotify; Uber's batch AI migration failed `P` |
| A judgment call with no test | Sample several answers and vote, or ask a fresh critic; a person decides | Self-consistency added 17.9 points on a math benchmark `R` |

Closing line under it: `Full table, with sources: <a href="#evidence">Lesson 17</a>.`

Left out of the short version: "Searching for a better solution with a machine score" (AlphaEvolve). It stays in Lesson 17.

Tags in the short table (copies of the Lesson 17 tags; same elements, same URLs):

| Row | Tag | href | data-src |
|---|---|---|---|
| Steps with shared state | R | `https://arxiv.org/abs/2512.08296` | Google Research: Towards a science of scaling agent systems (Dec 2025) |
| Steps with shared state | P | `https://cognition.com/blog/dont-build-multi-agents` | Cognition: Don't build multi-agents (Jun 2025, vendor) |
| Many independent, read-heavy parts | P | `https://www.anthropic.com/engineering/multi-agent-research-system` | Anthropic: How we built our multi-agent research system (Jun 2025) |
| A large mechanical change | P | `https://www.uber.com/us/en/blog/junit-migration/` | Uber Engineering: JUnit migration (Apr 2026) |
| A judgment call with no test | R | `https://arxiv.org/abs/2203.11171` | Self-consistency improves chain-of-thought reasoning (2022) |

---

## 5. Lesson 15 cause chips (`#failures`)

New first column "Cause" holding a text chip. Keep chips neutral (outline, no per-cause colour), so they follow child 6's rule that colour is never the only signal.

| # | What you see | Cause chip | Likely cause (page text) |
|---|---|---|---|
| 1 | Wanders, gold-plates | goal | The goal has no "done when". |
| 2 | "Done!" but broken | check | The builder graded its own work. |
| 3 | Forgets early details | context | The lead's context filled up with raw reading. |
| 4 | Same error, fifth try | goal | No retry cap. |
| 5 | Reviewer always agrees | check | It read your reasoning first. |
| 6 | Huge token bill | goal | Helpers spawned for small jobs, or a loop that runs too often. |
| 7 | Agents overwrite each other | permissions | Two writers on the same files. |
| 8 | Overnight run did something risky | permissions | Too much permission. |
| 9 | Auto mode let something through | permissions | It was treated as a security boundary. |
| 10 | The loop ran all night | goal | No cap on iterations, time or cost. |
| 11 | Tests pass, spec still broken | check | The loop optimized for the tests it had. |
| 12 | Agent turned off its own checks | permissions | It could edit CI, hook or gate files. |
| 13 | CI ran the repo's hooks unexpectedly | permissions | `claude -p` without `--bare`. |
| 14 | Run ended with no receipt | check | An API error or rate limit; the Stop gate never ran. |

Totals: goal 4, check 4, context 1, permissions 5. Five of 14 rows fit none of the three named causes, so the fourth chip is needed.

**Proposed one-sentence change to the intro** (replaces the current sentence; "too much permission" is the page's own wording in row 8):

> Almost every problem with autonomous agents traces back to a missing goal, a missing check, too much in one context, or too much permission.

Basis for the calls. Rows 4, 6 and 10 are `goal` because Lesson 4 lists "Stop and ask if" and "Budget" as parts of a goal. The rows the owner may want to flip:
- Row 5 could be `context` (the reviewer's context held your reasoning). It is tagged `check` because the page's fix is about giving the reviewer only the code and criteria, which is the maker/checker split.
- Row 12 could be `check` (the agent removed its own checks). It is tagged `permissions` because the page's fix is path rules and code-owner review on those files.
- Row 7 could be `goal` (a constraint can name which files). It is tagged `permissions` because the page's fix is one writer per set of files.
- Row 13 is tagged `permissions` because the page's fact is "Headless runs trust the repo": `claude -p` runs the repo's hooks with no prompt.
- Only row 3 is `context`. That is what the page's rows say; the intro's third cause is thinly covered.

Length rule from the issue ("tables longer than 5 rows show Show all N"): show rows 1 to 5 (goal, check, context, goal, check), and put rows 6 to 14 inside "Show all 14". The three causes the intro names stay visible; the `permissions` rows sit behind the toggle.

---

## 6. Disclosure plan (lessons 3, 8, 10, 12)

**Term-count rule** (a hand count by one reader, not a script run). One count per distinct name a reader must learn: a feature, command, flag, file, config key, acronym, framework, or coined stage word. Counted once per lesson, even if an earlier lesson used it. Not counted: product names (Claude, Linear, GitHub), plain tracker words (issue, Todo, In Progress, Done) and Lesson 1-2 words (loop, check, helper, gate). Any other name left out is named in that lesson's section. The reviews' figures are approximate and do not say how they counted, so each lesson shows both numbers.

| Lesson | Review figure | This inventory, before | After (visible) |
|---|---|---|---|
| 3 `#discovery` | about 20 | 28 | **7** |
| 8 `#toolbox` | about 27 | 42 | **6** |
| 10 `#guardrails` | about 18 | 20 | **4** |
| 12 `#pipeline` | about 12 | 24 | **7** |

Child 2 marked lessons 3, 8, 10 and 12 as Builder level. The issue's seven-term check applies to Core lessons only; this plan applies it to these four anyway, as asked.

Use the same markup everywhere: `<details class="reference"><summary>Reference: … (N)</summary>…</details>`. If a glossary link (child 3) points at a term inside a closed Reference, open the block on `hashchange`, or define the term in the visible text.

### Lesson 3, `#discovery` (28 to 7)

| Block | Now | After |
|---|---|---|
| Takeaway (new) | none | visible |
| `p.intro` | visible | visible |
| Pipeline figure and caption | visible | visible |
| Stage table (7 rows, 4 columns) | visible | Reference: "What each stage produces (7 stages)" |
| Note "Our pipeline, built from these sources" | visible | Reference: "Where the pipeline comes from" |
| h3 "Should you grill like Matt Pocock? Yes, with rules", its paragraph and 7 bullets | visible | Reference: "Grilling rules (7)" |
| h3 "How much spec before code?", 3 cards and the note under them | visible | Reference: "How much spec before code" |

- **Visible terms (7):** Frame, Assumptions, Grill, Shape, Bet, Specify, Slice. They are the figure's stage labels, with owner sub-text (you, you rank, agent asks, agent drafts, you decide).
- **Hidden terms (21):**
  - Artifacts (7): decision log, pitch, time budget, rabbit holes, no-gos, spike, Given/When/Then.
  - Frameworks (7): Jobs to Be Done, opportunity solution trees, assumption mapping, Shape Up, EARS, INVEST, tracer bullets.
  - Grilling (3): grill-me skill, design tree, QA loop.
  - Spec cards (4): grill log, one-page spec, research doc, decision record.
- **Not counted:** adversarial review (Lesson 2, rule 7, already shows it).
- **Trade-off:** the stage table is the lesson's main plain-words explanation, and it is now one click away. The figure carries the owner labels.

Tags that move into these Reference blocks (7; move the elements, do not retype):

| Moves into | Tag | href | data-src |
|---|---|---|---|
| Where the pipeline comes from | D | none (tooltip only) | Our own advice, built from the sources on this page |
| Where the pipeline comes from | P | `https://basecamp.com/shapeup` | Basecamp: Shape Up, plus the other discovery sources listed below |
| Where the pipeline comes from | S | `https://tuchizblog.today/en/posts/ai-prd-to-dev-tickets/` | Practitioner post: turning AI-drafted PRDs into tickets |
| Grilling rules | P | `https://github.com/mattpocock/skills/` | Matt Pocock's skills repo (grill-me, PRD and issue skills) |
| Grilling rules | P | `https://www.youtube.com/watch?v=-QFHIoCo-Ko` | Matt Pocock: full AI coding workflow walkthrough (AI Engineer) |
| How much spec before code | P | `https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html` | Birgitta Böckeler: Understanding spec-driven development tools |
| How much spec before code | D | none (tooltip only) | Our own advice, built from the sources on this page |

### Lesson 8, `#toolbox` (42 to 6)

| Block | Now | After |
|---|---|---|
| Takeaway (new) | none | visible |
| `p.intro` | visible | visible |
| Table rows: Standing rules, Think first, Repeat a recipe, Side jobs, Checks it can't skip | visible | visible |
| The other 11 rows | visible | "Show all 16" |
| `details.yours` block (18 names) | already collapsed by child 2, titled "Example: one author's harness (other setups differ)" | stays collapsed; counted here as hidden |

- **Visible terms (6):** CLAUDE.md, Plan mode, Skills, `/name`, Subagents, Hooks.
- **Hidden from the table (18):**
  - 14 feature names: Dynamic workflows, `/batch`, `/loop`, `/goal`, `/schedule`, Background, Monitor, Cloud, Remote Control, Worktrees, Memory, MCP connectors, `claude -p`, Agent SDK.
  - 4 cell terms: `/workflows`, `/deep-research`, `claude --cloud`, `--bare`.
- **Hidden in `details.yours` (18):** `/kickoff`, `/shape`, grilling skill, Explore agent, Haiku scouts, doc-checker, planner agent, ADR, writing-plans skill, adversarial-reviewer, openai-review, audit-reader, `/code-review`, cavecrew-reviewer, Stop gate, pre-push chain, release-verifier, review tiers (T0 to T2).
- **Build:** the 5 visible rows stay in their original order, with Hooks moved up after Side jobs. "Show all 16" opens a `<details>` holding the other 11 rows in their original order, with the same header cells.
- **Editorial choice:** the cut line at five is a choice, not a page claim. Adding `/goal` and Worktrees would make 8.
- **Tags that move:** none. The table has no evidence tags.

### Lesson 10, `#guardrails` (20 to 4)

| Block | Now | After |
|---|---|---|
| Takeaway (new) | none | visible |
| "Start with these 3" and the solo line (new, section 2 above) | none | visible |
| `p.intro` | visible | visible |
| Trifecta figure and caption (with its P tag) | visible | visible |
| h3 "Facts to design around" (6 bullets, 6 tags) | visible | Reference: "6 facts to design around" |
| Prevent / Detect / Recover (6 + 7 + 4 = 17 bullets) | visible | Reference: "17 controls: prevent, detect, recover" |
| h3 "Top mistakes" (7 bullets) | visible | Reference: "7 top mistakes" |

- **Visible terms (4):** deny rules, sandbox, lethal trifecta, injected text.
- **Hidden terms (16):** auto mode, `allowUnsandboxedCommands`, managed settings, `allowManagedPermissionRulesOnly`, headless runs (`claude -p`), `--bare`, MCP server, poisoned tool descriptions, network allowlist, PreToolUse hook, OpenTelemetry, StopFailure hook, dry-run diff, kill switch, scoped tokens, pinning.
- **Not counted:** skills and hooks as general ideas (Lesson 8's visible rows already show them). The two named hooks, PreToolUse and StopFailure, are counted.
- **Bullets hidden:** 6 facts, 17 controls and 7 mistakes, 30 in all.

Tags that move into the first Reference block (6; the trifecta caption's P tag stays visible):

| Fact | Tag | href | data-src |
|---|---|---|---|
| Deny rules win | P | `https://code.claude.com/docs/en/permissions` | Claude Code docs: Permissions |
| Auto mode is a convenience, not a wall | R | `https://arxiv.org/html/2604.04978v1` | arXiv 2604.04978: stress test of Claude Code auto mode |
| The sandbox only covers shell commands | P | `https://code.claude.com/docs/en/sandboxing` | Claude Code docs: Sandboxing |
| Managed settings beat repo settings | P | `https://code.claude.com/docs/en/settings` | Claude Code docs: Settings and managed settings |
| Headless runs trust the repo | P | `https://code.claude.com/docs/en/headless` | Claude Code docs: Headless mode |
| Skills and tools are code you didn't write | R | `https://arxiv.org/abs/2602.06547` | arXiv 2602.06547: malicious community skills (MCPTox figure: AAAI paper in Sources) |

### Lesson 12, `#pipeline` (24 to 7)

| Block | Now | After |
|---|---|---|
| Takeaway (new) | none | visible |
| `p.intro` | visible | visible |
| Sequence figure and caption | visible | visible |
| Panel "Who moves each status" | visible | visible (full width once its neighbour is hidden) |
| Panel "The gate at each step" (6 items) | visible | Reference: "The gate at each step (6)" |
| h3 "Things worth knowing" (7 bullets, 7 tags) | visible | Reference: "7 things worth knowing" |
| `.rule-box` "Protect the gates" | visible | visible |

- **Visible terms (7):** draft PR, required checks, auto-fix, merge queue, "Fixes ID", path rules, code-owner review.
- **Hidden terms (17):**
  - Gate panel (7): bot allow-list, branch prefix, read-only token, network allowlist, ruleset, environment reviewers, admin bypass.
  - Things worth knowing (10): Claude GitHub Action, `/install-github-app`, `@claude`, `.mcp.json`, `pull_request_target`, `env:`, commit-SHA pinning, `merge_group`, agent guidance, commit magic words.
- **Not counted:** sandbox (Lesson 10's starter set already shows it), CI, PR and hooks (earlier lessons already show them).
- **Trade-off:** readers on the "run it unattended" path (10, 11, 12) need the gate list. It is one click away, but child 2 could open Reference blocks by default for that path.

Tags that move into the second Reference block (7):

| Bullet | Tag | href | data-src |
|---|---|---|---|
| Claude GitHub Action and bots | P | `https://github.com/anthropics/claude-code-action` | anthropics/claude-code-action on GitHub |
| PR runs restore from the base branch | P | `https://github.com/anthropics/claude-code-action/blob/main/docs/security.md` | claude-code-action: security notes |
| pull_request_target | P | `https://docs.github.com/en/actions/reference/security/secure-use` | GitHub docs: Secure use of Actions |
| CODEOWNERS and merge queue | P | `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue` | GitHub docs: Managing a merge queue |
| Linear: you stay the assignee | P | `https://linear.app/docs/agents-in-linear` | Linear docs: Agents in Linear |
| Link work with "Fixes ID" | P | `https://linear.app/docs/github` | Linear docs: GitHub integration |
| Field report: small, specific tickets | S | `https://pub.towardsai.net/i-pointed-openais-symphony-at-20-linear-issues-the-15k-star-orchestrator-killed-my-standup-27e19cf85233` | Towards AI: a coding agent on 20 Linear issues |

---

## Flags

1. **Advice, not page text (marked D or editorial).** The Lesson 10 solo-developer line, including "for teams and unattended runs", is the one sentence the page does not support; it carries a D tag. The Lesson 8 cut at five features and all chip assignments in section 5 are editorial choices.
2. **"One-writer loop".** No such row exists. Goal loop is my reading; see section 4a for the alternative.
3. **Term counts differ from the reviews.** The inventory counts are higher than the reviews' approximations because the rule counts every named setting and command. The after-counts are the ones the builder's check needs.
4. **Short table and Lesson 17 must stay in step.** The 39–70%, 90.2% and 17.9-point figures are copied from Lesson 17's "Pick the shape by the task" table. Child 7 has reworked that lesson's chart and finding cards but, as of 13:58, not this table. If child 7 changes it, re-copy the short version from the new text. Child 7's new chart caption says the rows are "different tasks, so a longer line does not mean a bigger effect"; add a matching line under the short table only if child 7 puts one on the shape table too.
5. **Hidden content and links.** Glossary links (child 3) into a closed Reference need it to open on hashchange.
6. **Not covered here.** Tables over 5 rows that are outside this brief: Lesson 7 "Named methods, compared" (7 rows) and Lesson 13's scorecard (6 rows). They would take "Show all N" under the same rule; their tags move with the rows. Lesson 7's visible term count is not computed.

## Check against the issue's Check list

| Check | Where met |
|---|---|
| First paragraph after each h2 is a takeaway of 25 words or fewer | Section 1 (max 24) |
| Lesson 10 opens with "Start with these 3" and a "good enough for a solo developer" line | Section 2 |
| Lesson 7 shows Default and Specialist, default row highlighted, source tag in the name cell | Section 4a |
| Lesson 15 has a cause-chip column | Section 5 |
| Lesson 6 "Reality check" before "Send a helper when", links to Lesson 17 | Section 3 |
| "Pick the shape by the task" appears in Lesson 7 | Section 4b |
| Tables longer than 5 rows show "Show all N" | Sections 4a, 5, 6 (Lesson 7: 11, Lesson 15: 14, Lesson 8: 16; Lesson 3's 7-row table sits in a Reference) |
| 7 or fewer visible new terms in a lesson | Section 6: Lessons 3, 8, 10, 12 show 7, 6, 4, 7 (hand count; not scripted) |
