# Learning-science review (LX), v11

Basis: the full page text (not the JS), 14 of the 20 dark-theme screenshots, and playbook §0–5 and §17–18. Interactive features were not run.

- **LX-1 P0. Jargon before definitions; no glossary.**
  - Terms used before they are defined: harness (L2, never defined on the page), receipt (L6 diagram, defined in L9), worktree (L6 diagram, defined in L8), Stop gate/hook, MCP (never expanded), sandbox (L10).
  - Fix: add a 10–12 term "Words you'll meet" strip after the hero, and define each term at first use. Make the L1 diagram a big-picture map (You, lead, helpers, gates).
  - Check: each term's first occurrence is at or after its definition (grep). A test reader can explain harness, gate and context window after L1.
- **LX-2 P0. Order goes from abstract to concrete; L3 is heavy product discovery.**
  - Fix: make a core track of L1 loop, L4 goal, L9 self-checks, L6 orchestration, L5 phases, L15 failures and L16 checklist. Move L2 after L9 as a synthesis. Make L3 a "Going deeper" block. Update the playbook §0 map.
  - Check: no lesson before L6 introduces more than 6 new terms. A reader who stops after L6 can write a valid goal and name the three roles.
- **LX-3 P1. Term density.**
  - Counts of new terms: L3 ≈ 20, L7 ≈ 20, L8 15 features plus about 12 commands, L10 ≈ 18 terms plus 21 bullets, L12 ≈ 12.
  - Fix: show 3–4 items per lesson. L7 shows three patterns with pictures and collapses the rest. L10 adds a "Start with these 3" block. Flags and attribution go in "Reference" disclosures.
  - Check: about 7 or fewer visible new terms per core lesson.
- **LX-4 P1. Redundancy.**
  - Maker/checker is taught in L2 r07, L6, L7, L8, L9, L15 and L17. Lifecycle is taught in both L3 (8 stages) and L5 (10 phases). "Ten" is overloaded (rules, phases, patterns, laws).
  - Fix: give each concept one home and a one-line callback with a link elsewhere. Merge the L3 strip with the L5 phases. Rename "rules" to "principles".
  - Check: each core concept has exactly one defining paragraph.
- **LX-5 P1. No running example and no "try this now".**
  - The CSV export appears only in L4 and L9.
  - Fix: carry it through L3, L5, L6, L12, L13 and L15. Add a before/after in L6. Add one 10-minute try-now task.
  - Check: the example appears in at least 8 lessons.
- **LX-6 P1. No retrieval practice.**
  - Fix: add predict-then-reveal items. In L9, "75% per run, so the chance 3 runs all pass is?" (42%). In L6, sort jobs into lead or helper. In L15, hide the cause and fix. In L1, ask what happens if Check is missing. Add a 5-question quiz at the end of L16.
  - Check: each core lesson has at least 1 recall item.
- **LX-7 P1. No audience paths, and L8 "In your setup" assumes the author's private harness.**
  - Fix: add a path picker under the hero (New reader / Builder / Engineer), plus a level badge and minutes on each lesson. Move "In your setup" to the playbook, or label it "Example: one author's harness".
  - Check: every lesson shows a level and minutes. The core path has no unexplained slash command.
- **LX-8 P1. Counter-evidence comes late.**
  - L6 and L7 teach multi-agent; L17 then says one writer by default.
  - Fix: add a "Reality check" callout in L6 before "Send a helper when", and move "Pick the shape by the task" to L7.
  - Check: L6 states the caveat.
- **LX-9 P2. Trust calibration.**
  - About 80 tags with a legend only in L2. L17 finding 02 packs in 5 numbers. The L17 chart mixes tasks. L10 stacks 5 stats.
  - Fix: add a persistent mini-legend; allow at most 2 stats per finding and fold the rest; caption the chart "different tasks, not comparable"; add a "good enough for a solo dev" line in L10.
- **LX-10 P2. Playbook link and findability.**
  - Playbook §0 says "16 lessons" but the map runs to 17. The page never links or introduces the playbook. The playbook has no TOC, and each Law gives evidence before "Build it". The §17 roadmap sits late. Vocabulary differs between the two (Laws/rules, appetite/time budget).
  - Fix: add a TOC and an "I want to… go to §" table. Put "Build it" first in each Law. Add a "Deeper: playbook §X" footer to each lesson. Align the vocabulary. Fix 16 to 17.
- **LX-11 P3. The "plain words" promise breaks in L10 and L12; no phone navigation confirmed.**
  - Fix: tag expert blocks "Engineer detail", and add a phone lesson menu.
  - Check: at 375px, any lesson is reachable in 2 taps.

Top 3: a core track with paths, levels and minutes (LX-2/3/7); a glossary with definitions at first use (LX-1); a running CSV example plus recall items (LX-5/6).
