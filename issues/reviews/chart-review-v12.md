# Review: honest charts (child 7), page version 12

Independent data-visualization reviewer, Sonnet, read-only. It ran the page in Chromium with touch emulation. Date: 2026-10-24.

**Verdict: FAIL.** All of Chart 1's numbers matched the fact-check, and every SVG label was at least 12px at 1:1. Three blocking items remained.

## Blocking (all fixed in version 15)

1. **The context chart's touch readout was broken.**
   - A tap showed step 0, because the focus handler replayed the keyboard step.
   - The readout vanished when the finger lifted, because touch fires `pointerleave`.
   - A drag scrolled the page instead of scrubbing the chart.
   - Fix shipped: the pointer sets the step; `pointerleave` hides the readout for a mouse only; the focus readout runs only on `:focus-visible`; `touch-action: pan-y`; a tap outside closes it.
2. **The evidence table missed two Check items.** It did not say "not comparable" and had no source tag. Fix shipped: the caption now reads "Different tasks, not comparable in size", and the R tag sits in the table's note.
3. **The context chart lacked its "Illustrative:" wording.** Fix shipped:
   - The tooltip begins "Illustrative: step N".
   - The table caption begins "Illustrative: values, not measurements".
   - The axis reads "% of window".

## Other defects and what happened to them

| # | Defect | Outcome |
|---|---|---|
| 4 | "Setup" meant both a configuration (180 setups) and one of four designs | Now "best and worst of four multi-agent designs, pooled over 3 model families" |
| 5 | The axis invited a percentage-point reading | Now "relative change in tasks solved; 0 = same as one agent alone" |
| 6 | Baselines rounded without ≈ | Exact: 34.9%, 31.8%, 62.9%, 56.8% |
| 7 | "50 to 100 tasks per benchmark" supported for three benchmarks only; "Workbench still gained" true only of its best design | Both reworded |
| 8 | The connecting line was unexplained | Key item "Spread from worst to best" |
| 9 | Findings 05 and 06 showed three numbers | Finding 05 fixed. Finding 06 keeps "early-2025" as a date, not a statistic |
| 10 | The "Illustrative" mark could be cropped away; the tooltip had no live region; table headers lacked `scope` | Mark moved inside the plot; readout written to a live region; `scope="col"` added |
| 11 | On phones the dot plot's first view showed no dots | Open: vertical phone variants were deferred (VZ-3) |
