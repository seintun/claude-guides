# Charts and diagrams review (VZ), v11

Basis: the page source and all screenshots. The phone screenshots come from v4, but the SVG code is unchanged. Contrast was computed from the tokens. The figure inner width is about 880px at a 1280px viewport.

- **VZ-1 P0. L17 diverging bars mix benchmarks, configs and baselines.**
  - Problems:
    - The finance and web rows each show 1 winning setup, while planning shows best and worst. The chart reads as 2 big wins versus 2 big losses.
    - The caption says 4 benchmarks, but only 3 are drawn.
    - Equal-length bars invite comparing +80.9 with −70 across unlike metrics.
    - The real finding (gains turn negative above about 45% single-agent score) is not drawn.
    - There are no ticks and no table alternative.
  - Fix: use a dot plot with 1 row per benchmark (all 4) and a zero line. Show best and worst dots, labelled with config and n, plus a single-agent score column. Title it "Selected results, not an average: read direction, not size." Add a `<details>` data table. Fallback: label each bar "benchmark · config · best/worst", add ticks at −100/−50/0/+50/+100, and add a table.
  - Check: the row count equals the benchmark count in the caption, and every row names its config and baseline.
- **VZ-2 P1. L6 context chart reads as data.**
  - Problems: the "illustrative" pill sits outside the SVG. The tooltip, table, end labels and y-ticks show exact integers. The solo line reaches 99% with no compaction drop.
  - Fix: add an in-SVG watermark and dashed lines. Prefix the tooltip and table caption with "Illustrative:". Use empty/half/full ticks. Add the axis title "Context used (% of window)". Draw the compaction drop, and give the chart a claim title.
  - Check: a crop of the SVG alone still says illustrative.
- **VZ-3 P1. Every SVG on phones.**
  - Problems: `.scroll > svg{min-width:640px}` shows about 47% of each figure at 375px, with text at 7–10px. L17's zero line sits at the edge. L5 shows 4 of 10 phases. There is no scroll cue, and the scroller is not focusable.
  - Fix: below 720px, use vertical variants:
    - L3 and L5: a stepper list with ↩ badges.
    - L12: a numbered list.
    - L17 and the L6 chart: HTML bars.
    - L1 and L13: 2×2 grids.
    - Any scroller that stays gets an edge fade, a "scroll →" cue, and `tabindex=0 role=region aria-label`.
  - Check: at 375px there is no inner horizontal scroll, and rendered text is at least 12px.
- **VZ-4 P1. Text scale is inconsistent on desktop.**
  - Problem: `.d-label` 12px renders at 10.8px (L3, L5), 13.7px (L1) and 14.7px (L17). Band text is 9.9px.
  - Fix: use 880-wide viewBoxes, or set `svg{max-width:<vbw>px}`.
  - Check: `.d-label` computes to 12–13px in every figure at 1280.
- **VZ-5 P1. Colour roles collide.**
  - Problems:
    - Orange means fail, a decision (Bet), loop-back, the positive learning loop, Critic, untrusted content, event dots, the desired "Down" in the L13 table, and the S tag.
    - There are 2 blues (accent, series-1).
    - Fail is orange in L1 and L12 but red in L17. The red and orange luminance contrast is 1.06:1.
  - Fix: apply the spec below. Add a mini-legend under each figure, drop `--series-*`, and use neutral ↑↓→ glyphs in L13.
  - Check: `var(--loop)` appears only on loop-back marks.
- **VZ-6 P2. L10 Venn.**
  - Problems: the "danger" label overflows the triple overlap. The circles reuse role colours, and the pair overlaps are blank.
  - Fix: use neutral circles and fill the triple overlap red (clipPath). Add a leader line, and caption the pair overlaps. Optionally, clicking a leg removes it.
- **VZ-7 P2. L3 pipeline.**
  - Problems: the "park it" arrow points at empty space. There is no Deliver→Frame outcome arc. Owner shows only as sub-text. Bet orange and Deliver blue are unexplained. Band text is ink-3 at 4.13:1.
  - Fix: add a dashed "Parked" terminal and a "measured outcome" arc. Show owner by shape. Draw Bet as a diamond, and use ink-2.
- **VZ-8 P2. L5 explorer.**
  - Problem: the Review→Build loop is described but not drawn. Bands are 9.9px at 4.13:1, and nodes 11.7px.
  - Fix: add a nested Review→Build arc, use ink-2 for bands, and make nodes at least 13px.
- **VZ-9 P2. L6 hub.**
  - Problems: 5 arrowheads pile up at (420,188). "Own context" appears 5 times. The reduction claim (many files in, 1 summary out) is not drawn. Critic orange and Verifier green are unexplained.
  - Fix: elbow connectors from distinct y values, one bracket label, the annotation "reads many → returns 1 summary", and a legend.
- **VZ-10 P2. L12 sequence.**
  - Problems: steps are unnumbered, and blue = you is undocumented. The merge-queue text crosses the CI lifeline at x=800. The merge arrow loops on GitHub instead of going through CI. The panels below are not tied to the diagram.
  - Fix: number steps 1–12 to match the panels, add a status strip on the Linear lifeline, route GitHub→CI→GitHub, and add label halos globally (`paint-order:stroke`).
- **VZ-11 P2. L11 timeline.**
  - Problems: there is no laptop-awake band, and the shaded window is unlabelled. The gridline at x=413 cuts "CI fails". Lane colours are arbitrary.
  - Fix: add an awake band and window label, and use halos.
- **VZ-12 P2. Tables.**
  - Problems: `th` is ink-3 at 4.13:1, which fails AA at 12px. `.tbl-wrap table{min-width:720px}` forces scroll on 3-column tables. L7 and L8 have ungrouped rows and repeated P tags. L15 rows carry no cause tag.
  - Fix: use ink-2 for headers, show cards below 720px (`data-label`), add group header rows, highlight the default row, add a cause-chip column in L15, and merge the source tag into the name cell.
- **VZ-13 P2. L9 ladder.**
  - Problems: `.meter` has no `role`. The bars show one attribute while the text claims two. The risk guidance is not drawn.
  - Fix: add `role=img`, brackets for risk guidance, a retitled or cost marker, and thicker chain connectors.
- **VZ-14 P3. Accessibility, titles and L1.**
  - Problems: L17 has no table alternative. The L6 tooltip is `pointermove`-only. `.scroll` is not focusable. Captions are labels, not claims. L1 does not emphasise Check.
  - Fix: add claim titles, and give Check a thick border and badge.

## Visual-language spec (proposed)

- **Shapes:**
  - You or a human decision: pill, accent outline, accent-soft fill.
  - Agent step: neutral rect, rx 8.
  - Hook or gate: dashed neutral border.
  - External system or lifeline: rect, rx 2.
  - Done: green outline.
  - Parked: dashed grey.
- **Lines:**
  - Solid grey 1.6px: handoff.
  - Accent: human-initiated.
  - Green: pass.
  - Orange curved 2px with a ↩ label: loop-back only.
  - Dashed grey: automatic or async.
  - Lifelines: 1px.
  - One shared arrowhead set.
- **Colour:**
  - Accent blue: you, and the only blue.
  - Neutral: agent and system.
  - Green: pass.
  - Orange: loop-back only.
  - Red: harm or a negative result only.
  - Data series: accent versus ink-2.
  - Always pair colour with a label, shape or dash.
  - Non-text contrast at least 3:1. Use ink-2 instead of ink-3 on paper.
- **Text:**
  - viewBox 880 wide.
  - Titles 14–15px at weight 700, nodes 13px, edges 12px.
  - 11px is for ticks only.
  - Every text element gets a halo.
- **Layout:**
  - Read left to right and top to bottom, with loop-backs below.
  - Put a mini-legend under each figure.
  - Below 720px, use vertical variants.
  - Every figure gets `role=img`, an `aria-label`, and a text alternative.

Top 3: phone variants plus 880 normalisation (VZ-3/4); an honest L17 dot plot and an in-chart "illustrative" mark (VZ-1/2); one colour and shape grammar (VZ-5).

Note: this reviewer wrote `scratchpad/cr.py`, a contrast script, even though its brief said to write nothing.
