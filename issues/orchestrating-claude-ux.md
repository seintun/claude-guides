# Make "Orchestrating Claude" easy to navigate and understand

Parent issue plus 13 sliced child issues, written to the playbook's Template L (agent-ready issue). The builder's task contract (Template B) and plan table (Template D) are at the end.

- Page under test: https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq (version 11). The v11 source is `site/history/orchestrating-claude-v11.html`; the current source is `site/orchestrating-claude.html`.
- Playbook: `playbook/agent-harness-playbook.md` (v0.3 when this issue was written; the v0.3 copy is in `playbook/history/`).
- Reviews:
  - `reviews/ux.md` covers UI/UX and accessibility (UX-1 to UX-13).
  - `reviews/lx.md` covers learning and cognitive psychology (LX-1 to LX-11).
  - `reviews/vz.md` covers charts and diagrams (VZ-1 to VZ-14) and proposes a visual-language spec.
- Review tier: T1. The change is large but touches no schema, auth, infra or harness config. No adversary is needed; the gate is the check script built in child 0 plus a fresh re-review at the end.

---

## Parent

```
Title: Make the Orchestrating Claude page easy to navigate and understand on any screen
Outcome: A first-time reader on a phone or a desktop knows where to start, can jump to any
  lesson in two taps, meets every term after its definition, reads every figure at 12px or
  larger, and cannot mistake an illustrative chart or a mixed-benchmark chart for a measured
  comparison. The playbook has a table of contents and links both ways with the page.
Today: Three independent reviews (2026-10-24) found:
  - Phones: no lesson navigation below 980px, the h1 clips at 375px, diagram text is 7-10px,
    and every table scrolls sideways.
  - Reading path: no start point and jargon before definitions.
  - Charts: the evidence chart mixes benchmarks, and its caption says 4 when 3 are drawn.
    The context chart reads as data.
  - Diagrams: one colour (orange) means seven different things.
  - Accessibility: light-theme text and field borders fail WCAG AA, and the phase explorer
    loses keyboard focus.
  - Links: zero internal links inside <main>, and the playbook says "16 lessons".
Where: the page source (one HTML file, inline CSS, SVG and JS) and agent-harness-playbook.md
Check: children 1-13 each pass their own Check. checks/static.sh and checks/dom-checks.js pass
  at 375x812 and 1280x900 in light and dark. A fresh reviewer with no prior context
  re-runs the three review briefs and finds no P0 or P1.
Boundary: navigation, layout, figures, tables, interactions, accessibility, plain-language
  scaffolding (glossary, paths, takeaways, recall items), and playbook navigation.
  No-gos:
  - no new factual claims without a primary source
  - no change to evidence-tag URLs
  - no change to lesson section ids (#loop ... #sources), which the playbook map and
    old links use
  - no new runtime dependencies outside the artifact CDN allowlist
  - no renumbering of playbook sections
Depends on: none
Open questions: Q1-Q4 below. The builder follows each recommended default unless the owner
  answers otherwise.
Risk: normal (one static page and one Markdown file; no schema, auth, infra or dependency
  change)
```

### Open questions for the owner

| # | Question | Recommended default | Why |
|---|---|---|---|
| Q1 | Reorder the lessons into a core track (learning review LX-2: 1 loop, 4 goal, 9 self-checks, 6 orchestration, 5 phases, 15 failures, 16 checklist), or keep the order and add reading paths? | Keep the order and numbers; add paths, groups and level badges (child 2). Reorder later only if test readers still lose the thread. | A reorder breaks the playbook §0 map, old links and every "Lesson N" reference. Paths give most of the benefit at low cost. |
| Q2 | On touch screens, should the first tap on a P, S or R tag show a preview and only the second tap open the source (UX-6)? | No. Keep "tap opens the source in a new tab", as you asked earlier. Add a Key chip and a larger hit area instead. | Your earlier instruction was that clicking a tag opens the source. A tap-to-preview step would reverse it. |
| Q3 | Renumber playbook §3A and §17A to 3.1 and 17.1 (UX-11)? | No. Add a table of contents instead. | Renumbering breaks the page↔playbook map for little gain. |
| Q4 | Where should the page link to the playbook? The playbook is a local file, not published. | Name the section in text now ("Playbook §9.1"). Publish the playbook as a second page or a supporting file only once you choose. | Publishing distributes the playbook, which is your call. |

### Conflicts between reviewers, and how this issue resolves them

- **C1. Lesson order.** The learning review (LX-2) wants a reorder; the UX review (UX-5) wants the numbers kept. Resolved by Q1's default.
- **C2. Touch behaviour of evidence tags.** UX-6 conflicts with the owner's earlier instruction. The owner's instruction wins (Q2).
- **C3. Phone figures.** VZ-3 wants vertical variants for every figure; UX-3 wants a scroll cue and larger minimum widths. Resolved in child 9:
  - Vertical variants for the four figures that carry the most text (L3, L5, L12, L17) and for the context chart.
  - A scroll cue and a focusable scroll region for the rest.
  - Text of at least 12px everywhere.
- **C4. Lesson 2 legend.** Both reviews want the key to persist. Resolved in child 10 with a Key chip that is always reachable.

### Triage map: every finding to a child

| Child | Findings |
|---|---|
| 0 Check script | Gate for all of the below; no finding of its own |
| 1 Phone navigation and wayfinding | UX-1, UX-2, LX-11, plus a deep link on load that may not scroll on a phone (seen in the browser pane, not confirmed; see child 1) |
| 2 Reading paths and grouped rail | UX-5, LX-7, LX-2 (partly, per Q1), LX-3 (L2 collapse) |
| 3 Glossary and first-use definitions | LX-1 |
| 4 Cross-links and one home per concept | UX-10 (page side), LX-4, LX-10 (page side), UX-13 (repeated rules) |
| 5 Playbook navigation | UX-11, LX-10 (playbook side) |
| 6 Visual language and contrast | VZ-4, VZ-5, VZ-14 (halos, claim titles), UX-7, VZ-12 (header contrast) |
| 7 Honest charts | VZ-1, VZ-2, VZ-14 (L17 table, chart keyboard and touch), LX-9 |
| 8 Diagram corrections | VZ-6, VZ-7, VZ-8, VZ-9, VZ-10, VZ-11, VZ-13, VZ-14 (L1 Check emphasis) |
| 9 Phone figures and tables | VZ-3, UX-3, UX-4, VZ-12 (phone part) |
| 10 Interaction and accessibility fixes | UX-6 (per Q2), UX-8, UX-9, UX-12 |
| 11 Density: takeaways, starter sets, grouping | LX-3, LX-8, UX-13, VZ-12 (grouping, cause chips) |
| 12 Running example and recall practice | LX-5, LX-6 |

Not taken: the reviewer limits are noted, not acted on.
- The UX reviewer could not render the page, so desktop hero overlap at 981-1280px is unverified. Child 1 checks it.
- The VZ reviewer could not verify the fourth Google benchmark. Child 7 must check the primary source.

### Severity after triage

- **P0:** child 7. The evidence chart's caption says 4 benchmarks when 3 are drawn, and the chart invites comparing unlike results. That is a correctness problem on the page's trust lesson.
- **P1:** children 1, 2, 3, 6, 9 and 10.
- **P2:** children 4, 5, 8 and 11.
- **P3:** child 12. It has high learning value but is the largest content change, so it goes last.

---

## Children

### 0. Build the check script first

```
Title: Add a repeatable check script for page layout, text size, contrast and links
Outcome: One command and one browser snippet report PASS or FAIL for every Check in this
  issue, and the first run against v11 records the failing baseline.
Today: Checks are manual screenshots. Earlier sessions found hash navigation unreliable and the
  viewer fade-in dimming screenshots.
Where: new checks/static.sh, checks/dom-checks.js, checks/README.md (beside the page source)
Check: run both against v11 and save the output as checks/baseline-v11.txt. These must FAIL
  on v11:
  - h1 overflow at 375
  - a .tbl-wrap that scrolls at 375
  - SVG text under 12px
  - zero internal links in <main>
  - a phase arrow key that moves focus to the wrong node
  - L17 benchmark rows (3) not matching its caption (4)
Boundary: the scripts only, plus a wrapper that turns the page into a full HTML document for
  local testing (the artifact source has no doctype or body). No-gos: no page edits.
Depends on: none
Open questions: how to run the DOM checks.
  1. Try first: Playwright on the wrapped file, with viewports 375x812 and 1280x900 and
     emulate_media for light and dark.
  2. Fallback: inject dom-checks.js with the built-in browser's javascript_tool on the
     published page. This only works if the artifact iframe is reachable; say which worked.
Risk: trivial
```

What `dom-checks.js` asserts (each line prints PASS or FAIL with the failing element):

1. `document.documentElement.scrollWidth <= innerWidth` at 320, 375 and 414 px.
2. `h1.scrollWidth <= h1.clientWidth`.
3. Each SVG `<text>` renders at 12px or more. Measure it as computed font-size × `svg.getScreenCTM().a`. Axis ticks with `class="tick"` may be 11px.
4. No `.tbl-wrap` or `.scroll` element has `scrollWidth > clientWidth` at 375 px, except a scroller marked `data-scroll-ok` that has a visible cue.
5. Text contrast is at least 4.5:1, or 3:1 for text 24px and up or 18.66px bold. Field borders and figure strokes that carry meaning are at least 3:1. Run this in both themes.
6. Every `href="#x"` resolves to an element. Every "Lesson N" text inside `<main>`, outside the `.kicker` lines, sits inside an `<a href="#…">`.
7. Every `<svg>` has `role` and `aria-label`. No heading skips a level. No h3 is nested under another h3's card.
8. Every `a.ev` has `target="_blank"`, `rel` containing `noopener`, and `data-src`. Every `span.ev` has `tabindex="0"`.

What `static.sh` asserts (grep over the source):

1. `var(--loop)` appears only in selectors on the loop-back allowlist (child 6).
2. `--series-` is gone.
3. Each glossary term's first occurrence comes after the glossary or inside it (child 3).
4. The L17 chart's row count equals the benchmark count in its caption.
5. The external URL set is unchanged from v11. Diff it against `checks/urls-v11.txt`.

### 1. Phone navigation and wayfinding

```
Title: Add lesson navigation for phones and fix the clipped title
Outcome: On any width a reader can see which lesson they are in, jump to any lesson in two
  taps, and move to the next lesson or back to the contents from the end of every lesson.
Today: Phone navigation and reading position are both missing or broken:
  - `.rail{display:none}` below 980px, with no replacement.
  - No Next, Contents or Back-to-top links anywhere.
  - The h1 "Orchestrating" is cut at 375px (screenshot vns3bm).
  - The rail has no aria-current.
  - A lesson link loaded on a phone did not scroll to its lesson in the browser pane. This is
    not confirmed: it may be the claude.ai viewer, not the page.
Where: h1 rule (line 52), .rail rules (lines 60-67, 252, 314-316), markRail script
  (around line 2048), end of each <section>, footer
Check: dom-checks 1-2 pass at 320, 375 and 414.
  - At 375 a "Lessons" control stays visible at every scroll depth. It shows the current
    lesson number and name, and choosing "17 Evidence" leaves that h2 fully visible below
    the control.
  - Every lesson ends with "Next: <n> <name> →" and "↑ Contents".
  - The current rail link has aria-current="location".
  - At 981-1280 the h1 does not overlap .thesis.
Boundary: a sticky <details class="lessons-menu"> at ≤980px that reuses the rail's list and
  markRail; section scroll-margin-top; Next and Contents links; Back to top in the footer;
  a skip link to <main>; the h1 clamp fix. If a deep link on load fails in the viewer, add a
  small on-load scroll to location.hash after fonts load, and note whether the viewer passes
  the hash at all.
  No-gos: no change to section ids or rail order.
Depends on: 0
Open questions: none
Risk: normal
```

### 2. Reading paths, grouped rail, levels and minutes

```
Title: Tell readers where to start, what is optional and how long each lesson takes
Outcome: Under the hero a reader picks one of three paths. Each lesson shows its level and
  reading time, the rail is grouped, and optional or author-specific material is
  visibly optional.
Today: Nothing on the page tells a reader where to start or what to skip:
  - The rail is a flat list of 18 items.
  - Lesson 2 is a wall of 10 cards with 16 tags before any mechanism is shown.
  - Lesson 3 (product discovery, about 20 new terms) comes before Goals.
  - The "In your setup" block in Lesson 8 names one author's private tools (/kickoff,
    cavecrew-reviewer, T0-T2).
Where: hero .thesis area, nav.rail, each section's kicker, Lesson 2 card grid, .yours block
  (lines 869-881)
Check: the paths, labels and collapsed blocks are in place:
  - Three paths appear under the hero, each with lesson links and total minutes:
    - New to this: 1 → 4 → 9 → 6 → 5 → 15 → 16, about 25 min.
    - Run it unattended: 10 → 11 → 12.
    - Check the evidence: 17 → Sources.
  - Every lesson kicker shows a level (Core, Builder or Reference) and minutes. Minutes are
    words / 200, rounded up.
  - At 1280x900 the rail shows four labelled groups and keeps the numbers.
  - Lesson 2 shows 3 cards and a "Show all 10" toggle.
  - .yours is collapsed by default and titled "Example: one author's harness".
  - A test reader (fresh subagent given only the page text) names the next lesson on the
    New path from any lesson on it.
Boundary: paths, groups, badges, collapses. No-gos: no reorder or renumbering (Q1 default).
Depends on: 1 (shares the menu and rail markup)
Open questions: Q1
Risk: normal
```

### 3. Glossary and definitions at first use

```
Title: Define every orchestration term before or at its first use
Outcome: A "Words you'll meet" strip after the hero defines 10-14 terms in one line each, and
  each term is defined where it first appears in a lesson.
Today: Several terms are used before they are defined, or never defined:
  - "harness" is used in Lesson 2 and never defined on the page.
  - "receipt" and "worktree" appear in the Lesson 6 diagram but are defined in Lessons 9
    and 8.
  - "MCP" is never expanded.
  - "sandbox" is used in Lesson 10 without a definition.
  - "Stop hook" and "gate" are used before they are explained.
Where: new block after .thesis; first-use sentences in lessons 1, 2, 6, 8 and 10
Check: static.sh check 3 passes for the term list.
  - Terms: harness, orchestrator (lead), subagent (helper), context window, goal, check or
    gate, hook, Stop hook, receipt, worktree, MCP, sandbox, headless, lethal trifecta.
  - Each glossary entry links to its first use, and the first use links back.
  - A fresh subagent given only lessons 1-2 can define harness, gate and context window
    in one sentence each.
Boundary: definitions and links. No-gos: no glossary longer than 14 terms on the page. The
  long list belongs in the playbook.
Depends on: 2 (the strip sits under the paths)
Open questions: none
Risk: normal
```

### 4. Cross-links and one home per concept

```
Title: Link every lesson reference and give each repeated idea one home
Outcome: Every "Lesson N" in the text is a working link. Each lesson ends with its playbook
  section. Ideas taught in several places (maker and checker; stop after two failures) are
  defined once and referenced elsewhere in one linked sentence.
Today: <main> has zero internal links. Four "Lesson N" cross-references are plain text: lines
  652, 663 and 1307, plus the JS string at line 1776 that refills line 663.
  - Maker and checker is taught in lessons 2, 6, 7, 8, 9, 15 and 17.
  - "Stop after 2 failures" is restated in lessons 4, 11, 14 and 15.
  - Lesson 17 says "the playbook" with no pointer.
Where: text across lessons; the JS that builds strings; the Lesson 8 and Lesson 15 tables;
  each section's closing line
Check: dom-checks 6 passes, and every lesson's closing line names its playbook section using
  the map below.
  - Map: 1-2 → §1-2; 3 → §5.1-5.3; 4 → Template B; 5 → §5.4; 6 → §3 and §7;
    7 → §5.3 and §6; 8 → §3A; 9 → §9; 10 → §10; 11 → §11; 12 → §12; 13 → §13;
    14 → §16; 15 → §14-15; 16 → §9 and §13; 17 → §19.
  - grep shows one defining paragraph each for maker-checker (Lesson 9) and the two-failure
    stop rule (Lesson 15). Every other mention is one sentence or less, with a link.
Boundary: links, callbacks, playbook references (text only, per Q4).
  No-gos: no deletion of a lesson's unique content.
Depends on: 1 (closing-line layout), 2
Open questions: Q4
Risk: normal
```

### 5. Playbook navigation

```
Title: Add a table of contents and a find-it-fast index to the playbook
Outcome: A builder reaches any section or template from the top of the playbook in one click,
  and the playbook's map of the page is correct.
Today: The playbook is hard to navigate and out of step with the page:
  - About 1,256 lines with no TOC; §0 routes only in prose.
  - §0 says the page has "16 lessons" (line 18).
  - Evidence tags sit inside headings (for example "### 11.1 … [P: …]").
  - Each Law gives evidence before "Build it".
  - The §3 Mermaid block has no text fallback.
  - The vocabulary differs from the page ("Ten laws" against "Ten rules"; appetite against
    time budget).
Where: agent-harness-playbook.md §0, the heading lines, §2 Laws, §3, §16
Check: the TOC, map and tables are in place:
  - Every "##" heading appears in a two-level TOC after §0.
  - §0's page map is a table with 17 lessons plus Sources.
  - A "Find it fast" table (task → section) has at least 12 rows.
  - §16 opens with a template index: Template | Use when | Page counterpart.
  - No heading line contains "[P", "[S", "[R" or "[D" (the tag moves to the first line
    under the heading).
  - Each Law shows "Build it" before its evidence.
  - §3 has a 5-line text description under the Mermaid block.
  - The page's terms appear in the playbook as aliases, for example "Ten laws (the page's
    'Ten rules')".
Boundary: navigation and ordering inside the playbook. No-gos: no renumbering (Q3); no change
  to template text or to facts.
Depends on: none. It is a different file, so it can run in parallel with the page children.
Open questions: Q3
Risk: trivial
```

### 6. One visual language and AA contrast

```
Title: Apply one colour, shape and type grammar to every figure and pass AA contrast
Outcome: Every figure uses the same meaning for each colour, shape and line style and has a
  mini-legend. Diagram text renders at 12-13px on desktop. Light and dark themes pass WCAG AA
  for text and for meaningful non-text marks.
Today: Colour, size and contrast are inconsistent:
  - Orange (--loop) means fail, decision, loop-back, the positive learning loop, Critic,
    untrusted content, event dots, the desired "Down" in the Lesson 13 table, and the S tag.
  - There are two blues (--accent and --series-1).
  - Fail is orange in lessons 1 and 12 but red in Lesson 17; in light mode red and orange
    differ by 1.06:1 in luminance.
  - .d-label 12px renders at 10.8-14.7px depending on the viewBox, and band text at 9.9px.
  - Light --ink-3 (#6B7885) is 4.13:1 on paper, which fails for th, .hint, the footer and band
    text.
  - Field borders are 1.40:1.
Where: :root tokens in both themes (lines 9, 21, 31); th (line 194); .scroll > svg (line 86);
  every <svg> viewBox; .d-* classes; td.want.down
Check: static.sh checks 1-2 pass, dom-checks 3 (desktop) and 5 pass in both themes, and every
  <figure> has a legend row. The spec to apply (from reviews/vz.md):
  - Shapes:
    - You or your decision: pill, accent outline, accent-soft fill.
    - Agent step: neutral rect, rx 8.
    - Hook or gate: dashed neutral rect.
    - External system or lifeline head: rect, rx 2.
    - Done: green outline.
    - Parked: dashed grey.
  - Lines:
    - Handoff: solid grey 1.6px.
    - Human-initiated: accent.
    - Pass: green.
    - Loop-back only: curved orange 2px with a "↩" label.
    - Automatic or async: dashed grey.
    - Lifelines: 1px.
    - One shared arrowhead set.
  - Colour:
    - Accent is the only blue.
    - Neutral for agent and system.
    - Green for pass, orange for loop-back only, red for harm or a negative result only.
    - Always pair colour with a label, shape or dash.
  - Text: viewBox 880 wide (1 unit = 1px), or svg max-width set to the viewBox width.
    - Titles 14-15px at weight 700, nodes 13px, edge labels 12px.
    - 11px for axis ticks only.
    - A halo on every label (paint-order:stroke; stroke:var(--surface); stroke-width:4).
  - Tokens:
    - Light --ink-3 becomes #5B6875 (5.22:1 on paper; check it on --code-bg too).
    - th and band text use --ink-2.
    - input, select and textarea borders use --ink-3.
    - Remove --series-*.
    - Lesson 13's better/worse direction uses neutral ↑ ↓ → glyphs with hidden text.
  - Captions: each figure gets a claim-sentence title, such as "The check is what makes the
    loop safe", not a label.
Boundary: tokens, shared CSS and per-figure colour and shape swaps. No-gos: no layout or
  content changes to figures (children 7-9 do those).
Depends on: 0
Open questions: none
Risk: normal
```

### 7. Honest charts (P0)

```
Title: Make the evidence chart and the context chart impossible to misread
Outcome: The Lesson 17 chart shows every benchmark its caption names. Each result is labelled
  with its configuration and baseline, and the chart says it shows selected results whose
  direction, not size, is the point. The Lesson 6 chart reads as illustrative even when
  cropped. Both charts have a data table and work by keyboard and touch.
Today: Both charts invite misreading:
  - Lesson 17 caption: "Google Research ran 180 setups across 4 benchmarks". Only 3 benchmarks
    are drawn (finance +80.9%, web navigation +9.2%, planning best −39% and worst −70%).
  - The bars invite comparing unlike results.
  - The 45% single-agent threshold that the text states is not drawn.
  - No ticks and no table.
  - The "illustrative" pill sits outside the Lesson 6 SVG, while the tooltip, ticks and end
    labels show exact integers.
  - The solo line rises to 99% with no compaction drop.
  - The Lesson 6 tooltip responds only to pointermove.
  - Lesson 17's findings pack up to five numbers each.
Where: Lesson 17 <figure> (around line 1500-1520); #ctx-chart and its script (around line
  1890+); #ctx-table; Lesson 17 finding cards
Check: static.sh check 4 passes. The Lesson 17 chart and its findings must meet all of these:
  - Each Lesson 17 row names benchmark, configuration and best or worst.
  - The title says the results are selected, not averaged.
  - A <details> table lists every plotted value with its source tag.
  - doc-checker confirms every number against the Google Research primary source (paper
    or blog), including the fourth benchmark's result.
  - No Lesson 17 finding shows more than 2 numbers before a "More numbers" disclosure.
  - The Lesson 17 table states "different tasks; not comparable in size".
  The Lesson 6 chart and the figure check must meet all of these:
  - The SVG contains an "Illustrative" mark, and its lines are dashed.
  - Its tooltip and table caption start with "Illustrative:".
  - Its y-axis reads empty, half and full, with the axis title "Context used (% of window)".
  - The solo line shows a drop at compaction.
  - Arrow keys on the focused chart move the readout.
  - dom-checks 7 passes for both figures.
Boundary: the two charts and the Lesson 17 finding cards. Recommended form for Lesson 17: a
  dot plot with one row per benchmark, best and worst dots, a zero line, and faint "helps" and
  "hurts" shading. The builder may keep bars if every row is labelled and ticks are added.
  No-gos: no number without a primary source; no change to the finding's conclusion
  ("one writer by default; multi-agent helps parallel work").
Depends on: 6
Open questions: if the fourth benchmark's per-configuration result can't be verified, change
  the caption to "3 of the 4 benchmarks shown" rather than plot an unverified number.
Risk: normal (factual content: route the numbers through doc-checker)
```

### 8. Diagram corrections

```
Title: Fix what each diagram draws, so it shows the claim its caption makes
Outcome: Each diagram draws the mechanism its text describes, with no label collisions,
  piled-up arrowheads or arrows that end in empty space.
Today (from reviews/vz.md):
  - L1: Check is not emphasised, although the caption says Check is what matters.
  - L3:
    - The "park it" arrow ends in empty space.
    - There is no Deliver → Frame "measured outcome" arc.
    - Owner (you or agent) appears only as 12px sub-text.
  - L5: the Review → Build loop is described but not drawn.
  - L6 hub:
    - Five arrowheads pile up at (420,188).
    - "own context" appears 5 times.
    - The "many files in, one summary out" reduction is not drawn.
  - L9: .meter has no role; bars show one attribute while the text claims two; the risk
    guidance (typo fix at rung 2, login or payments at 5-6) is not drawn.
  - L10 Venn:
    - The "danger" label overflows the triple overlap.
    - The pairwise overlaps are blank.
  - L11:
    - No laptop-awake band.
    - The 09:00-17:00 window is unlabelled.
    - The gridline at x=413 cuts "CI fails".
  - L12:
    - Steps are unnumbered.
    - The merge-queue arrow loops on GitHub instead of going through CI.
    - Its label crosses the CI lifeline at x=800.
    - The panels below are not tied to the steps.
Where: the <svg> in lessons 1, 3, 5, 6, 9, 10, 11 and 12; .meter spans in Lesson 9
Check: every item in Today is visibly fixed in a 1280x900 screenshot of each figure, in light
  and dark. dom-checks 3 and 7 pass. A fresh reviewer given only the screenshot and caption
  states each figure's claim.
Boundary: the drawings and their labels, following child 6's spec.
  Specific fixes:
  - L3: a dashed "Parked" terminal, and Bet drawn as a diamond.
  - L5: a nested Review → Build arc labelled "findings".
  - L6: elbow connectors from distinct y values, one "each helper has its own context
    window" bracket, and "reads many → returns 1 summary".
  - L9: role="img" on meters, and brackets for the risk guidance.
  - L10: neutral circles, the triple overlap filled red via clipPath, and a leader line.
  - L12: steps numbered 1-12 and matched to the panels, and a status strip on the Linear
    lifeline.
  No-gos: no new figures; no change to the facts the figures show.
Depends on: 6
Open questions: none
Risk: normal
```

### 9. Phone layouts for figures and tables

```
Title: Make every figure and table readable at 375px without sideways scrolling
Outcome: On a 375px phone every figure is legible at 12px or more. The text-heavy figures
  switch to vertical layouts, any scroller left has a visible cue and keyboard focus, and
  tables become stacked cards.
Today: Phone layouts are unreadable or need sideways scrolling:
  - `.scroll > svg{min-width:640px}` shows about 47% of each figure, with text at 7-10px.
    - Lesson 5 shows 4 of 10 phases.
    - The Lesson 17 zero line sits at the edge.
  - There is no scroll cue, and the scrollers are not focusable.
  - `.tbl-wrap table{min-width:720px}` and `td.job{white-space:nowrap}` force sideways
    scrolling, even for 3-column tables.
  - #ctx-table inherits the 720px minimum.
  - The phase explorer's show() never scrolls the selected node into view.
Where: line 86, line 193, line 197, the figures in lessons 1, 3, 5, 6, 10, 11, 12, 13 and 17,
  and all .tbl-wrap tables
Check: dom-checks 1, 3 and 4 pass at 375x812 in light and dark.
  - Lesson 5 at 375 shows all 10 phases as buttons that wrap, and pressing Next through to
    phase 10 keeps the selected phase visible.
  - Each table at 375 shows one card per row, labelled with the column names.
Boundary: at ≤720px:
  - Lessons 3 and 5 become a stepper list with "↩ back to <phase>: <reason>" badges.
  - Lesson 12 becomes a numbered list matching child 8's step numbers.
  - The Lesson 17 chart and the Lesson 6 chart become HTML bars.
  - Lessons 1 and 13 become 2x2 grids.
  - Remaining scrollers get tabindex=0, role="region", an aria-label, an edge fade and a
    "swipe →" hint.
  - Tables become cards via data-label, filled by JS from <th>.
  - #ctx-table gets min-width:0, and the first column becomes th scope="row".
  - show() calls scrollIntoView({inline:'center', block:'nearest'}).
  No-gos: no desktop layout changes; no content changes.
Depends on: 6, 7, 8 (build the phone variants from the final figures)
Open questions: none
Risk: normal
```

### 10. Interaction and accessibility fixes

```
Title: Fix keyboard, screen-reader and touch problems in the interactive parts
Outcome: Every interactive part works by keyboard, screen reader and touch. The P/S/R/D key is
  always reachable, and the heading outline is clean.
Today: There are keyboard, structure and feedback problems throughout:
  - Phase explorer:
    - The arrow-key handler uses the selected index (cur), not the focused node. Tab to
      node 7, press →, and focus jumps to node 2.
    - All ten nodes are tab stops.
    - "Next phase" becomes disabled while focused at phase 10, so focus is lost.
    - aria-live covers all of #phase-detail.
  - Evidence tags:
    - The legend appears only in Lesson 2.
    - The tooltip has no Esc dismiss (WCAG 1.4.13).
    - aria-describedby repeats aria-label.
    - Tags are about 16x21px.
  - Structure:
    - 56 h3 elements, with card titles nested under h3 subheads.
    - About 244 tab stops, and no skip link.
    - Every Sources entry is linked twice, giving about 45 duplicate stops.
    - No table captions or row headers.
  - Feedback:
    - Copy feedback is silent.
    - The goal builder's placeholders are unmarked and it has no reset.
    - "Where results go" shows in every mode.
    - The checklist has no clear button and its progress is not announced.
Where: phase script (lines 1876-1890); showTip and tooltip CSS (line 255, lines 2003-2045);
  card markup (lines 549-553, 1522-1524, .surfaces); Sources (lines 1575-1649); goal builder
  (lines 1322-1431); prompts (lines 593-645); checklist (lines 1468-1491)
Check: dom-checks 7-8 pass. Each part must behave as follows:
  - Phase explorer: Tab enters it once; arrow keys and Home/End move selection and focus
    together from any node; focus survives reaching phase 10.
  - Evidence tags:
    - With a tag focused, Esc hides the tooltip.
    - A "Key" chip in the rail and in the phone menu opens the P/S/R/D legend from any
      lesson.
    - At (pointer:coarse) each tag's hit area is at least 24x24px.
    - A tap on P, S or R still opens the source in a new tab (Q2).
  - Feedback: a screen reader announces "Copied" and checklist progress; unfilled
    placeholders in the goal builder are highlighted with an "n left" count; "Reset to
    example" and "Clear checklist" work.
  - Structure: the heading outline has no h3 inside an h3 card; Sources has one tab stop per
    source.
Boundary: listed behaviours only. No-gos: no change to tag click behaviour (Q2); no new
  libraries.
Depends on: 1 (Key chip in the menu), 4
Open questions: Q2
Risk: normal
```

### 11. Density: takeaways, starter sets and grouping

```
Title: Lead each lesson with its takeaway and hide reference detail until asked
Outcome: The first screen of each lesson shows a one-line takeaway and its main visual. Dense
  lessons open with a 3-item starter set, and long tables and flag lists sit behind
  disclosures.
Today: Dense lessons show everything at once:
  - New terms per lesson: Lesson 3 ≈ 20, Lesson 7 ≈ 20, Lesson 8 ≈ 27, Lesson 10 ≈ 18
    (plus 21 control bullets), Lesson 12 ≈ 12.
  - Lesson 7 has 10 ungrouped patterns, with a "P" tag in every row.
  - Lesson 15's intro names three causes (goal, check, context) but its rows are untagged.
  - Lessons 6-7 teach multi-agent patterns before Lesson 17 says one writer by default.
Where: each section's opening; lessons 3, 7, 8, 10, 12, 15 and 6
Check: each lesson's opening, the starter blocks and the tables must meet all of these:
  - Each lesson's first paragraph after the h2 is a takeaway of 25 words or fewer.
  - Lesson 10 opens with "Start with these 3" (deny rules, sandbox, remove one leg of the
    trifecta) and a "good enough for a solo developer" line.
  - Lesson 7 shows Default (plan-critique-build, lead and helpers, one-writer loop) and
    Specialist groups; the default row is highlighted; the source tag sits in the name
    cell.
  - Lesson 15 has a cause-chip column.
  - Lesson 6 has a "Reality check" callout before "Send a helper when", saying one writer by
    default and that outside checks beat self-critique, with a link to Lesson 17.
  - "Pick the shape by the task" appears in Lesson 7.
  - Tables longer than 5 rows show "Show all N".
  - A term count by two readers, or a script, finds 7 or fewer visible new terms per Core
    lesson.
Boundary: ordering, disclosure and short new text. No-gos: no deletion of facts or sources;
  hidden material stays one click away.
Depends on: 2 (levels), 3 (glossary), 4 (one home per concept)
Open questions: none
Risk: normal
```

### 12. Running example and recall practice

```
Title: Carry one example through the lessons and let readers test themselves
Outcome: One small task (the CSV export) runs through at least 8 lessons, from issue to
  retro. Each Core lesson has one predict-then-reveal question, and the checklist ends with
  a 5-question recall quiz.
Today: The page shows only one task in action, and only twice:
  - The CSV export appears only in lessons 4 and 9.
  - The page has no recall or prediction items.
  - The checklist is an action list, not a test of understanding.
Where: lessons 1, 3, 4, 5, 6, 9, 12, 13, 15 and 16
Check: the example, the recall items and the readers' results must meet all of these:
  - grep finds the running example in at least 8 lessons.
  - Each Core lesson on the New path has one <details> recall item with its answer hidden.
    Examples:
    - Lesson 9: "75% per run: what's the chance 3 runs all pass?" (about 42%).
    - Lesson 6: sort 6 jobs into lead or helper.
    - Lesson 15: show the symptom, then reveal the cause.
    - Lesson 1: "What happens if Check is missing?"
  - Lesson 16 ends with a 5-question quiz that scores itself and works without storage.
  - Lesson 4 or Lesson 9 has one "Try now (10 min)" task that ends in a goal and a receipt
    the reader can see.
  - Three fresh test readers (subagents given only the page text) score at least 4/5 on the
    quiz without searching.
Boundary: short example paragraphs and recall items.
  No-gos: no new claims; no stored scores (no localStorage requirement).
Depends on: 3, 11
Open questions: none
Risk: normal
```

---

## Plan (Template D)

```markdown
# Plan: Orchestrating Claude navigation and comprehension
Goal: A first-time reader on any screen can find, read and understand every lesson, and no
  chart can be misread.
Risk: normal    Status: draft
```

| # | Change | Test that proves it | Rollback | Status |
|---|---|---|---|---|
| 0 | Check script and v11 baseline | `checks/static.sh`; dom-checks at 375 and 1280, light and dark; baseline saved | delete `checks/` | PASS: scripts run on v11 and record the expected FAILs in `checks/baseline-v11.txt` (Playwright on `build/preview.html`) |
| 5 | Playbook TOC and index (parallel; other file) | child 5 Check | restore playbook v0.3 copy | PASS: independent reviewer, all 9 Check items plus diff, anchors (150 resolve), fences identical; its 3 low nits fixed; Google-study wording corrected to paper version 1 |
| 6 | Visual language and contrast | static 1-2; dom 3, 5 | republish v11 | PASS: static-1, static-2; dom-3 at 1280 light and dark; dom-5a (1,262 texts) and dom-5b in all 6 views. Keys added where a figure mixes encodings (L1, L3, L5, L6, L11, L12); L10 and L13 label marks directly. Palette validator: blue/red pass CVD; orange/green WARN (labelled, so legal); red/green FAIL, so L17 will not use green |
| 1 | Phone navigation, h1 | dom 1-2; menu scenario | republish previous version | PASS: dom-1 and dom-2 at 320/375/414/1280 (desktop h1 overflow fixed too); dom-11; nav-1 menu sticky at top; nav-2 menu → 17 shows h2 at 144px below the 49px menu; deep-link scroll added after fonts load |
| 2 | Paths, groups, levels | child 2 Check | republish previous version | PASS: dom-12 (3 paths with minutes, level and minutes on 17 kickers, 4 rail groups, Lesson 2 shows 3 + toggle, author block closed); path-aware Next links. Test-reader check not run |
| 3 | Glossary | static 3; test reader | republish previous version | PASS: dom-9, 14 terms each first used in the block that defines it (check moved from static to DOM). Test-reader check not run |
| 7 | Honest charts (P0) | static 4; doc-checker on numbers; dom 7 | republish previous version | PASS: dom-10 (4 of 4 benchmarks), dom-7; numbers from doc-checker (paper v1); context chart illustrative in-SVG, keyboard and touch readout. Independent chart review running |
| 8 | Diagram corrections | screenshots plus fresh reader | republish previous version | PASS (v15): L1 Check emphasis; L3 Parked terminal and outcome arc; L5 Review→Build arc; L6 one connector per helper, one bracket, reduction note; L9 meters role=img, risk chips; L10 Venn; L11 "Computer on?" column, labelled window; L12 steps 1–12, merge via CI, status strip, panels cite steps. dom-3, dom-5, dom-7 pass; screenshots checked light and dark. L3, L6, L11 and L12 redrawn by two parallel agents, spliced with tools/splice_figs.py |
| 9 | Phone figures and tables | dom 1, 3, 4 at 375 | republish previous version | PASS: dom-1, dom-3 (min 12.0px), dom-4 at 320/375/414; figures keep drawn size and scroll with cue, tables become labelled cards. Vertical figure variants deferred |
| 10 | Interaction and accessibility | dom 7-8; keyboard scenarios | republish previous version | PASS: dom-7, dom-8, kbd-1..3, page-1 unique ids, page-2 no script errors; Esc hides tooltip, tag key in rail and menu, coarse-pointer hit area, live regions. Placeholder highlighting and reset buttons deferred |
| 4 | Cross-links and one home | dom 6; grep for "Lesson \d" | republish previous version | PASS: dom-6 (53 internal links, no plain Lesson N), playbook section on every lesson end. Merging repeated rules into one home deferred |
| 11 | Density | child 11 Check | republish previous version | PASS (v15): takeaways, L10 starter set, L6 reality check; L7 Default/Specialist groups with the default row marked and a short "Pick the shape" table; L8 five features first; L15 cause column (fourth cause: permissions); long tables fold after the first group; Reference disclosures in L3, L10, L12 (L3 grilling section kept visible on purpose). Glossary links open folded content. Scripted term count not run |
| 12 | Running example and recall | grep; 3 test readers ≥ 4/5 | republish previous version | PASS (v15): CSV example in 9 lessons; 6 predict-then-reveal items; L4 "Try now (10 min)"; L16 5-question quiz, no storage, green/red answer marks with words. Test-reader score: from the final independent review |

Order note:
- Child 7 is the only P0 but depends on 6, so 6 goes first; 6 is also the base for 8 and 9.
- Child 5 touches only the playbook and can run in its own session at the same time.
- All page children edit one file, so they run one at a time: one writer.

Decisions:
- 2026-10-24 keep the lesson numbers and ids; add paths instead of reordering (Q1 default),
  because the playbook map and the links depend on them.
- 2026-10-24 keep "tap opens source" (Q2 default), because the owner asked for it.

Open questions: Q1-Q4 (owner: human).

---

## Builder task contract (Template B)

```text
You are the lead on this task. Plan first, use helper agents for side work, and prove every result.

GOAL
Ship the 13 child issues in issues/orchestrating-claude-ux.md so a first-time reader on any
screen can find, read and understand every lesson of the Orchestrating Claude page, and no
chart can be misread.

DONE WHEN (each line must be checkable)
1. checks/static.sh prints only PASS.
2. checks/dom-checks.js prints only PASS at 375x812 and 1280x900, in light and dark.
3. Every child's Check line is marked PASS with the command or scenario that proved it, in
   the plan table.
4. doc-checker confirms every number in the Lesson 17 chart and its table against the primary
   source.
5. The page is published to https://claude.ai/artifact/8q1jNZyZ1HTjDBvqgBWMLq (same URL).
   A screenshot of every lesson at 375 and 1280, in light and dark, has been looked at in the
   built-in browser.
6. A fresh reviewer with none of this context re-runs the three review briefs (UX,
   learning, charts) and reports no P0 or P1.

CONSTRAINTS
- Artifact page contract:
  - no doctype, html or body tags
  - title and viewport metas kept
  - colours as tokens on :root, with dark mode under prefers-color-scheme and
    [data-theme] as today
  - scripts only from the CDN allowlist, pinned versions
  - links open in a new tab
- Keep the section ids (#loop ... #sources) and the lesson numbers.
- Keep every evidence-tag URL; static.sh check 5 diffs the URL set.
- Keep "click or tap a P, S or R tag opens the source in a new tab". D tags stay
  tooltip-only.
- No new factual claims without a primary source. No numbers from memory.
- Before changing a figure, load the artifact-diagramming and dataviz skills. Before
  publishing, load artifact-design.
- Write normal prose in page text. No AI attribution anywhere.

BUDGET
- One child per working block; at most 3 helpers at a time (reviewers and test readers on
  Sonnet; read-only scouts on Haiku).
- Stop after 2 failed attempts at the same check, or after 13 publishes without a new PASS.

STOP AND ASK ME IF
- Q1-Q4 need a different answer than the default, or a child can't meet its Check without
  breaking a CONSTRAINT.
- A primary source contradicts a number on the page.
- You are about to remove content (not hide it behind a disclosure), delete files, or
  publish to a different URL.
- you are about to do something hard to undo (delete data, deploy, force-push, push to the
  main branch, pay)

HOW TO WORK
1. Read this issue, the three reviews in issues/reviews/, and the playbook's §9 and §16
   (templates B, D, L).
2. Do child 0 first. Record the v11 baseline: which checks fail and why.
3. Keep issues/orchestrating-claude-ux.md's plan table current; it is the source of truth.
4. For each child in plan order:
   - Make the change.
   - Run its Check.
   - Publish to the same URL with a label naming the child.
   - Screenshot the touched lessons at 375 and 1280.
   - Mark PASS, FAIL or NOT RUN with the command.
5. Child 5 (playbook) touches another file. If a second session is available, run it there;
   otherwise do it between page children.
6. After child 12, run DONE WHEN 1-6. A fresh reviewer gets the page and the review briefs,
   not your conclusions.
7. Report what changed, what passed, what is not done, and up to 3 harness improvements.

RULES
- NOT RUN is not PASS.
- If the same check fails twice for the same reason, stop and ask for a second opinion.
- The plan table is the source of truth; keep it current.
- When the BUDGET runs out, stop and report, even if not done.
```
