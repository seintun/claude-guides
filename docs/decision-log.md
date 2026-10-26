# Decision log

Decisions taken while building the Orchestrating Claude page and the agent harness playbook, on 2026-10-24. Each row says what was decided, why, and who decided. "Owner" means the person this work was done for.

| # | Decision | Why | Decided by |
|---|---|---|---|
| D1 | Grade every claim P (primary), S (second-hand), R (research) or D (our design advice), and show the grade as a small tag beside the claim | Readers need to know how solid each piece of advice is; the playbook uses the same grades | Claude, accepted by the owner |
| D2 | P, S and R tags link to their source and open it in a new tab on click. D tags and the legend show a tooltip only | The owner asked for it after clicking a D tag jumped to Sources. Q2 later kept this on touch screens too | Owner |
| D3 | Tooltips use the page's own tokens, so they match light and dark | Owner request | Owner |
| D4 | Keep the lesson order and numbers. Add reading paths, levels and reading times instead of reordering (Q1) | A reorder would break the playbook map, old links and every "Lesson N" reference; paths give most of the benefit | Owner accepted the default |
| D5 | Don't renumber playbook sections such as §3A and §17A; add a table of contents instead (Q3) | Renumbering breaks the page-to-playbook map for little gain | Owner accepted the default |
| D6 | The page names playbook sections in text and doesn't link to an unpublished file (Q4) | Publishing the playbook is the owner's call | Owner accepted the default |
| D7 | One visual language for every figure: accent pill = you; neutral box = Claude; dashed = automatic or next run; green = pass; orange = sent back and nothing else; red = harm or a worse result | The charts review found orange carrying seven meanings and fail drawn in two colours | Claude, from review VZ-5 |
| D8 | Figures are drawn 880 units wide or less and never scale below 1:1; wider than the column, they scroll sideways and show a cue | Keeps every label at 12px or more; vertical phone variants were deferred | Claude |
| D9 | Light `--ink-3` darkened to #5B6875, and form borders use it | Light-theme text and field borders failed WCAG AA (4.13:1 and 1.28:1) | Claude, from review UX-7 |
| D10 | The S tag moved from orange to its own violet token | Orange is reserved for "sent back" | Claude, from D7 |
| D11 | The evidence chart became a dot plot: every benchmark, best and worst design, exact baselines, a data table, and the words "read the direction, not the size" | The old bar chart drew 3 of the 4 benchmarks its caption named and invited comparing unlike tasks | Claude, from VZ-1 and the fact-check |
| D12 | Cite the Google scaling study as paper version 1 (December 2025); hedge the 45% threshold as a fitted estimate; state 17.2× and 4.4× as relative to one agent | doc-checker found version 3 reports 260 setups and 6 benchmarks, and the paper hedges the threshold | Claude, from `research/google-scaling-check.md` |
| D13 | Blue for better and red for worse on the evidence chart, not green and red | The palette validator failed green against red for colour-blind readers (ΔE 5.6 light, 3.9 dark); blue against red passed | Claude, from the validator |
| D14 | The context chart is marked "Illustrative" inside the drawing, uses dashed lines, and shows values as "about N0%" | A cropped copy must not read as measured data | Claude, from VZ-2 |
| D15 | A 14-term glossary strip, and each term defined where it first appears | Novices met jargon before its definition (LX-1) | Claude |
| D16 | Glossary words in the text show their definition in a tooltip on hover, focus or tap, instead of jumping to the strip | Owner request | Owner |
| D17 | Define "receipt" in Lesson 4's try-now step, not in Lesson 6 | The running example uses the word in Lesson 5 | Claude |
| D18 | Keep Lesson 3's "Should you grill like Matt Pocock?" section visible, though the density plan folded it into Reference | The owner asked that question directly at the start | Claude |
| D19 | One writer for the page file. Subagents work in parallel on separate files (the playbook), drafts (glossary, takeaways, running example, figures) or reviews, and the lead splices their output | Two writers on one file overwrite each other; drafts keep the work parallel | Claude, after the owner asked for parallel subagents |
| D20 | Reviewers are fresh agents that get the files and the brief, never the builder's report | A reviewer that reads the builder's conclusion tends to agree with it | Claude |
| D21 | Under the 30-minute launch window, ship children 0–7, 9, 10 and the takeaways; defer child 8, the rest of 11, and 12 | The time limit; the deferred items shipped in version 15 | Owner set the limit; Claude chose the cut |
| D22 | Phase explorer: buttons sit under the diagram, the detail panel keeps the height of its longest phase, the nav is centered with "← Prev" and "Next →", and the counter is hidden at 340px or less | Owner requests: no moving buttons, no flashing, symmetrical and short | Owner |
| D23 | Quiz answers are scored by a "Check answer" button, never on change | Arrow keys used to select and lock an answer at once (final review, P1) | Claude |
| D24 | Quiz feedback: green outline and "✓ Correct" on the right option; red and "✗ Your answer" on a wrong pick | Owner request; the words keep colour from being the only signal | Owner |
| D25 | Long tables fold after their first group or five rows; Lessons 3, 10 and 12 put detail in "Reference" disclosures; a link into folded content opens it | Density (LX-3) while keeping links working | Claude |
| D26 | Each change is gated by checks: `checks/static.sh` and `checks/run-dom.js` (Playwright, eight views, keyboard scenarios), and new checks are added with each child | Verification first, as the playbook teaches | Claude |
| D27 | Each change is published to the same artifact URL, and nothing is published elsewhere | Keeps one link for the owner | Claude |
