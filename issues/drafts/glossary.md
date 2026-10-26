# Draft: "Words you'll meet" strip and first-use definitions (child 3, LX-1)

Draft text only. Nothing here has been applied to `site/orchestrating-claude.html`.

- Source analysed: `site/orchestrating-claude.html` as of Oct 24 13:58 (213,949 bytes, sha1 `01003120d25553f062bcf92274ef5475c4dd1049`). The file was still changing while this was drafted; see note 1 at the end.
- Method: visible text only, in document order. Counted: the hero, every `<section>`, SVG `<text>`, figcaptions and tables. Not counted: `nav.rail`, `nav.paths` (the new path picker, which lists lesson names), `<title>`, scripts, attributes. Lesson ids are the `<section id>` values (#loop is Lesson 1, #rules 2, #patterns 7, #toolbox 8, #guardrails 10, #orchestration 6).
- The table is in the suggested strip order (section 3). Every definition is 22 words or fewer (counted by script) and uses only words that are either everyday English, defined by an earlier strip row, or already used on the page.
- In the table, a regex pipe is written `\|` so the Markdown table survives. Section 4 has the same regexes ready to copy. All regexes are JavaScript/PCRE syntax with the `i` flag.

## 1. Term table

| term | definition (22 words or fewer) | data-term regex | first use (document order) | proposed first-use edit |
|---|---|---|---|---|
| goal | What you want done, how you will know it is done, and the limits Claude works within. | `(?<!/)\bgoals?\b`. Specific sense: mostly. It skips the `/goal` slash command (a different feature, L7 and L8). It cannot skip "Goal loop" or "goal prompt", which are the same idea, so that is harmless. | **Hero.** Eyebrow: "Field guide · goals, agents, loops". First sentence: "How to give Claude a goal it can check, let it explore and plan with helper agents, make it prove its own work, and keep it running when you step away." Thesis: "You own the goal and the bar for done." First use after the hero, #loop: "A sharper goal makes the check honest." | Hero stays (section 2). In #loop, rewrite R1 adds "(what you want done, and how you will know)" after "A sharper goal". |
| check or gate | A test, command or observation that decides if the work is done. A gate runs one automatically, so Claude can't skip it. | `\b(?:the\|a\|an\|each\|every\|one\|stricter\|real\|your\|any\|good\|these\|missing\|runnable\|required\|automatic\|no) checks?\b\|\bchecks\b\|\bgates?\b`. Specific sense: cannot be done by regex. A noun ("the check") and a verb ("check the result") look the same, and "check" is also a normal verb. This version matches the noun forms, plural "checks", and gate. It still catches a few verbs ("the agent checks feasibility", "Claude Code checks deny, then ask") and "permission checks". None of them come before the first use, so first-use detection is right. Do not use it to link every occurrence. | **Hero** (plain verb, same idea): the lede sentence above, "a goal it can check". **First use in the glossary sense, #loop:** "An AI agent is a loop: plan a step, do it, check the result, and adjust." (first noun use: "A sharper goal makes the check honest."). **Gate, #loop:** "Helpers and gates do side work and run checks the lead can't skip." | Hero stays. R1 adds "(with a test, a command or an observation)" after "check the result", using the words of the Lesson 1 figure caption. For gate, add a closing clause to the #loop roles line: "Helpers and gates do side work and run checks the lead can't skip; a gate is a check that runs on its own." |
| context window | Claude's working memory. Every file it reads fills it, and when it gets full, early details fade. | `context windows?\|(?:own\|fresh\|clean\|main\|one\|lead's\|only) context\b\|window (?:fills\|gets full)\|own windows`. Bare "context" is left out on purpose: "gather context" and "context engineering" are different senses. | **#rules, card 04.** Heading: "Treat context as a budget". Body: "Load what the next step needs, not everything." Its source line then says "recall drops as the window fills". The exact phrase "context window" first appears in #orchestration. | Body of card 04: "Load what the next step needs into the context window (Claude's working memory), not everything." The heading above it uses bare "context" and is not matched. |
| subagent (helper) | A helper agent that does one narrow job in its own context window and sends back a short summary. | `sub-?agents?\|\bhelpers?\b`. Every "helper" on the page means this. | **Hero:** "…explore and plan with helper agents…" (lede sentence above). **First use in a lesson, #loop:** "Orchestration, subagents, hooks and schedules are all ways to run this loop better." | Hero stays. R1 adds "(helpers that each take one job)" after "subagents". #loop's roles list already uses "Helpers" two lines later. |
| orchestrator (lead) | The main Claude session. It holds the goal and plan, makes the calls, and hands jobs to helpers. That is orchestration. | `orchestrators?\|\blead\b`. "Orchestration" and "Orchestrating" are left out: they match the page title and the L1 intro, not the role. Today every "lead" is this role; a future verb "lead" would match too. | #loop: "The lead session (the orchestrator) holds the plan and makes the calls." | Already defined here. |
| hook | A script of yours that runs on its own when a set event happens, so Claude can't skip it. | `\bhooks?\b`. Also matches "Stop hook", "PreToolUse hook" and "StopFailure hook", which are all hooks. | #loop: "Orchestration, subagents, hooks and schedules are all ways to run this loop better." | R1 adds "(scripts that run on their own)" after "hooks". The wording matches the Lesson 6 "Hooks and gates" label. |
| Stop hook | A hook that runs when Claude tries to finish, for example to rerun the tests. It can block Claude from finishing. | `\bstop (?:hooks?\|gates?)\b`. "Stop gate" is the same thing under the name L8 and L15 use. "StopFailure hook" (L10) is a different hook and is not matched. | #rules, card 09, source line: "A Stop hook exiting with code 2 blocks Claude from finishing." | Define it in the card's first sentence, so the sourced line stays untouched: "Anything that must happen every time lives in a hook (such as a Stop hook, which runs when Claude tries to finish), CI or a permission rule, not only in prose." |
| harness | Everything wrapped around the model to steer it: its tools, rules and checks. Each piece should prevent a named failure. | `harness(?:es)?`. Also matches the source title "Effective harnesses…" in #sources, which is fine. | #rules, card 01. Heading: "Keep the harness thin". | Card 01 body: "Let the model do the thinking. The harness is the scaffolding around it: tools, rules and checks. Every piece should name the failure it prevents, and go when a newer model no longer needs it." The heading comes one line before the definition; see note 4 for a strict alternative. |
| receipt | A closing report: each check from your goal marked PASS, FAIL or NOT RUN, with the command behind it. | `\breceipts?\b` | #orchestration, figure label (arrow from the lead back to You): "receipt". Lesson 9 defines it later. | Keep the label. Add to the Lesson 6 intro, before the figure: "The lead sees the conclusion, not the pile of reading behind it, and ends by giving you a receipt: each success criterion marked PASS, FAIL or NOT RUN, with the command behind it." That puts the first occurrence in the defining sentence. |
| worktree | A separate copy of your project's code, so two agents never edit the same files. | `\bworktrees?\b` | #orchestration, figure label on the Builder box: "one slice, in its own worktree". Lesson 8 defines it later. | Keep the label. In the same Lesson 6 intro: "Each helper starts with a clean memory, does one job (a builder works in its own worktree, a separate copy of the project's code), and sends back a short summary." |
| MCP | Short for Model Context Protocol. Plug-ins that connect Claude to outside tools such as GitHub, Linear and browsers. | `\bMCP\b\|model context protocol` | #toolbox, row "Reach other tools", Feature cell: "MCP connectors". Its plain-words cell already says "Plug-ins for GitHub, Linear, browsers, docs and more." The name is never expanded anywhere. | Feature cell: "MCP (Model Context Protocol) connectors". The expansion is not on the page; see note 5. |
| headless | Claude running with no chat window, called from a script (claude -p) instead of you typing to it. | `\bheadless\b` | #guardrails, "Facts to design around": "Headless runs trust the repo." The idea is taught earlier in #toolbox ("Claude without the chat window, called from a script or CI") without the word. | "Headless runs (Claude called from a script, with no chat window) trust the repo." |
| sandbox | A restricted space for shell commands, limiting the files and network they can reach. Edits, hooks and MCP servers run outside it. | `\b(?:un)?sandbox(?:es\|ed)?\b`. Covers "sandboxed", and "unsandboxed" in L10. | **#patterns (L7), not L10:** table row "Day shift, night shift": "You grill and plan by day; a sandboxed loop builds the issues overnight; QA findings become new issues". The issue text says L10, but the word is used three lessons earlier. | Same cell: "…a sandboxed loop (its shell commands run in a restricted space) builds the issues overnight…". The L10 text stays as the detailed treatment. |
| lethal trifecta | An agent that holds private data, reads untrusted content and can send data out can be steered into leaking it. | `lethal trifecta\|\btrifecta\b` | #guardrails, "Prevent" list: "Drop one trifecta leg per session". The figure caption just above defines the idea but never names it: "Simon Willison's warning: an agent that holds private data, reads untrusted content, and can send data out can be steered by injected text into leaking it." The full name first appears in #sources. | Name it in the caption: "Simon Willison's warning, the lethal trifecta: an agent that holds private data, reads untrusted content, and can send data out can be steered by injected text into leaking it." The figure's `aria-label` already says "The lethal trifecta", so screen-reader users get the name today and sighted readers do not. |

### R1: Lesson 1 intro rewrite (covers goal, check, subagent, hook in one paragraph)

Original (#loop, intro):

> An AI agent is a loop: plan a step, do it, check the result, and adjust. Orchestration, subagents, hooks and schedules are all ways to run this loop better. A sharper goal makes the check honest. A better plan makes each step smaller. A stricter check stops the loop from ending early.

Proposed:

> An AI agent is a loop: plan a step, do it, check the result (with a test, a command or an observation), and adjust. Orchestration, subagents (helpers that each take one job), hooks (scripts that run on their own) and schedules are all ways to run this loop better. A sharper goal (what you want done, and how you will know) makes the check honest. A better plan makes each step smaller. A stricter check stops the loop from ending early.

If four parentheses in one paragraph is too dense, drop the `goal` one first: the roles list below the figure ("You set the goal, the bar for done…") and the strip already cover it, and the hero has already used the word.

## 2. Terms whose first use is in the hero

Three terms are used in the hero, before the strip, which sits after it:

| term | where in the hero | verdict |
|---|---|---|
| goal | eyebrow ("goals"), lede ("a goal it can check"), thesis ("You own the goal and the bar for done.") | Keep. It is everyday English at that point, and the thesis is the page's one-line idea. Rewording it ("what you want done") would weaken that line. The strip's first row defines it right after. |
| subagent (helper) | lede: "helper agents" | Keep. "Helper agents" explains itself, and the strip's fourth row defines it. |
| check | lede: "a goal it can check" (verb) | Keep. It is the plain verb. The strip's second row defines the noun and gate. |

The hero stays as it is. These three count as defined by the strip right after it, with one condition on the check script:

- **`static.sh` check 3 has to skip the hero.** Otherwise it fails on goal, helper and check by construction. Make it start at the first element after the strip, or exempt `header.hero`.
- It also has to skip `nav.paths`, `nav.rail`, `details.lessons-menu`, the `a.skip` link and the "Next: 04 Goals →" links. They are navigation labels, not teaching text, but they contain "Goals", "Self-checks" and "Orchestration", so without the skip they look like early uses.
- `nav.paths` and `.thesis` are both inside `header.hero`. The strip goes directly under the paths: either inside the header after `nav.paths`, or just after `</header>`. Do not put it between the lede and the thesis.
- For the strip's "links to first use" requirement, link these three terms to their first use after the strip (#loop), not to the hero.

`Orchestrating` in the h1 and "loop" are not on the 14-term list, so they are not touched.

## 3. Suggested strip order (simple to advanced)

Each term depends only on rows above it. The table in section 1 is already in this order.

1. goal: the thing you hand over. No dependencies.
2. check or gate: what decides "done".
3. context window: Claude's working memory.
4. subagent (helper): uses "context window".
5. orchestrator (lead): uses goal and helpers.
6. hook: a script Claude can't skip.
7. Stop hook: uses hook.
8. harness: the umbrella over tools, rules and checks, so it comes after the pieces.
9. receipt: uses goal and check.
10. worktree: plain, but only matters once there are several helpers.
11. MCP: the first tool-specific term.
12. headless: needs "script".
13. sandbox: uses hook and MCP.
14. lethal trifecta: the security idea, last.

## 4. Regexes, copy-paste ready (JavaScript/PCRE, flag `i`)

```text
goal                 (?<!/)\bgoals?\b
check or gate        \b(?:the|a|an|each|every|one|stricter|real|your|any|good|these|missing|runnable|required|automatic|no) checks?\b|\bchecks\b|\bgates?\b
context window       context windows?|(?:own|fresh|clean|main|one|lead's|only) context\b|window (?:fills|gets full)|own windows
subagent (helper)    sub-?agents?|\bhelpers?\b
orchestrator (lead)  orchestrators?|\blead\b
hook                 \bhooks?\b
Stop hook            \bstop (?:hooks?|gates?)\b
harness              harness(?:es)?
receipt              \breceipts?\b
worktree             \bworktrees?\b
MCP                  \bMCP\b|model context protocol
headless             \bheadless\b
sandbox              \b(?:un)?sandbox(?:es|ed)?\b
lethal trifecta      lethal trifecta|\btrifecta\b
```

`goal` uses a lookbehind (Safari 16.4 or later in a browser; fine in Node and `grep -P`). Without one, use `(?:^|[^/\w])goals?\b` and drop the leading character from the match.

## 5. Notes for the builder

1. **The page changed while this was drafted.** Between my reads, a skip link, a phone lesson menu, "Next: NN …" links, the hero path picker and "Core · N min" badges were added, the Lesson 17 chart was rebuilt as a table, and Lesson 8's "In your setup" block became "Example: one author's harness". None of that touched a first-use sentence, and the checks in note 2 pass on the latest copy. Re-run the first-use search after each landing. Line numbers are not given, because they shift.
2. **Checked on an edited copy.** I applied every edit above to a scratch copy of the page and re-ran the regexes. For 13 of 14 terms, the first match outside the hero is the sentence that defines the term. For the other, harness, the first match is the card heading and the definition is the next sentence in the same card.
3. **Text built by scripts is not counted, but readers see it earlier.** The L4 prompt builder says "You are the lead (orchestrator) on this task…", and the L5 phase explorer (script array `PH`) uses "MCP connectors", "worktrees", "a Stop hook that reruns checks" and "receipt" before Lessons 6 and 8. The explorer's Verify phase already defines receipt in place ("A receipt: PASS, FAIL or NOT RUN, with the command, for each criterion."). If you want in-place glosses there too, edit the array. A static check will not see them.
4. **Heading as first use (harness).** If check 3 is later made to require the definition at or before the first mention, change the card 01 heading to "Keep the harness (everything around the model) thin". I did not propose it as the default because the heading mirrors the playbook's "Law 1".
5. **MCP expansion is from outside the page.** "Model Context Protocol" appears nowhere on the page and the Sources lesson has no MCP source. It is confirmed by `https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro` ("MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems"). No new evidence tag is needed for a name expansion. If you want one, that URL is the P source.
6. **The sandbox definition leans on Lesson 10's bullets**: it covers only shell commands, restricts files and network ("a tiny network allowlist", "block reads of SSH and cloud keys"), and edits, hooks and MCP servers run outside it. I have not checked it against the Claude Code sandbox docs. Run `doc-checker` on it if the strip should carry it as a firm claim.
7. **Sandbox depends on child 11.** If the Lesson 7 "Day shift, night shift" row is removed rather than collapsed, the first use moves to #guardrails: "The sandbox only covers shell commands." Collapsed content is still in the source, so nothing changes in that case.
8. **"Orchestration" is not one of the 14 terms,** but the word appears in the h1 and the Lesson 1 intro before Lesson 6 defines it. The orchestrator row's last sentence ("That is orchestration.") covers it in the strip. Add a parenthesis in R1 only if test readers still stumble.
