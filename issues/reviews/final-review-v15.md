# Review: final independent review, page version 15

A fresh reviewer (Sonnet, read-only) checked the page source against all 38 original findings and the Check lines for children 8, 11 and 12. It did not use a browser. Date: 2026-10-24.

**Verdict: not ready.** The quiz could not be answered by keyboard. That was fixed in version 16, together with every other item below.

**Tally:** 27 FIXED, 11 PARTLY, 0 OPEN. P0 open: 0. P1 open: 0. Five P1 findings are PARTLY: UX-3, UX-6, LX-4, VZ-3 and VZ-4.

Structure was clean:
- tags balanced
- no block element inside a `<p>`
- 133 unique ids
- all 102 `#` links resolve
- no skipped heading levels

Every number on the evidence chart matched `research/google-scaling-check.md`.

## Findings by status

| Finding | Status | Note |
|---|---|---|
| UX-1, 2, 4, 5, 7, 10, 11 | FIXED | Phone menu, title, cards, paths, contrast, links, playbook TOC |
| UX-3 | PARTLY | Mid-width shrink fixed in v16; vertical phone variants deferred |
| UX-6 | PARTLY | Tap-to-preview declined (Q2); the tooltip itself is not hoverable |
| UX-8 | PARTLY | `disabled` kept rather than `aria-disabled`; focus survives in Chromium |
| UX-9 | PARTLY | Captions and row headers on some tables only |
| UX-12 | PARTLY | Placeholder marks, Reset and Clear deferred |
| UX-13 | PARTLY | No back-links on repeated rules; the two long tables were folded in v16 |
| LX-1, 3, 5, 6, 7, 8, 9, 10, 11 | FIXED | Glossary, density, running example, recall and quiz, levels, reality check, trust, playbook link, menu |
| LX-2 | PARTLY | Reorder declined (Q1); reading paths added |
| LX-4 | PARTLY | The stop-after-two-failures rule is still restated; "rules" not renamed |
| VZ-1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 14 | FIXED | Evidence chart, context chart, colour roles, all diagrams, tables |
| VZ-3 | PARTLY | Vertical phone variants deferred |
| VZ-4 | PARTLY | Fixed at all widths in v16 (checked at 768 and 1024) |
| VZ-13 | PARTLY | Risk chips and `role=img` done; cost not drawn |

## New problems and what was done (all in version 16)

1. **P1, blocking:** the quiz's `change` listener locked a question on the first arrow key. Fixed with a "Check answer" button per question. Check `quiz-1` now verifies that arrows only select and Check scores.
2. **P2:** figure text fell below 12px between 721 and 1230px. Figures now keep their drawn size at every width and show the cue only when they scroll. Checks run at 768 and 1024.
3. **P3:** the phase explorer used "worktrees" and "MCP" before their definitions. Plain-word glosses were added.
4. **P3:** "Stop hook" was unexplained on the New path. A gloss was added in Lesson 9.
5. **P3:** reading minutes ignored the quiz. `tools/lesson_meta.py` now counts it, and the New path mentions the 10-minute exercise.
6. **P3:** three small contradictions were fixed (sample sizes, the src/reports boundary, "sixth try").
7. **P3:** a malformed `#hash` could throw. It is now caught.

Not yet run: a blind test-reader check. The reviewer's 5/5 on the quiz does not count, because it saw the answers in the source first.
