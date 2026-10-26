# Review: post-launch re-review, page version 12

A fresh independent reviewer (Sonnet, read-only) re-ran the three original review briefs against the launched page. Date: 2026-10-24.

**Tally:** 14 FIXED, 22 PARTLY, 2 OPEN. Still open by severity: P0 0, P1 2, P2 14, P3 about 16.

- **P1 open:** LX-5 (no running example) and LX-6 (no recall practice). Both were deferred at launch as child 12, and both shipped in version 15.
- **P2 open:** LX-2, LX-3, LX-4, UX-6, VZ-3, VZ-4, VZ-7, VZ-10, VZ-12, UX-10/LX-10 and UX-12, plus three new problems (1, 3 and 4 below).

## New problems the launch introduced

| # | Problem | Outcome |
|---|---|---|
| 1 | Glossary links to Lesson 2 rules 4 and 9 pointed at cards hidden by the "show 3 rules" collapse | Fixed in v15: a reveal function opens whatever hides a link's target |
| 2 | The "Where results go" field never hid, because `.field{display:grid}` overrode `[hidden]` | Fixed in v15: the page sets `[hidden]{display:none!important}` itself |
| 3 | Undefined jargon on the core path (CLAUDE.md, CI, PR, ADR; `claude -p`, `--bare` in L15) | Partly: glosses added in v16 where readers meet worktrees, MCP and Stop hook first |
| 4 | On phones the L17 plot started off-screen | Open: vertical variants deferred |
| 5 | Sources was numbered 18 in the rail and menu | Fixed in v15 |
| 6 | Every figure was announced as a scrolling region, even when it did not scroll | Fixed in v15: only figures that actually scroll get the region role |
| 7 | Small text issues (the L17 intro's "only measured results", sample sizes, "fifth try" vs "sixth try") | Fixed in v15 and v16 |
| 8 | Tables between 721 and 980px scrolled sideways with no cue | Fixed in v16: tables wrap to fit |
| 9 | Phase explorer nav wrapped at 375px | Fixed in v13 and v14: buttons under the diagram, centered, "← Prev" and "Next →" |
| 10 | Dead CSS and stale section comments | Partly: `.d-box.parked` is now used by the L3 diagram |
