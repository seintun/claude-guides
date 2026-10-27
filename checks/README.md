# Checks for the Orchestrating Claude page

Two layers. Both must print only PASS before a child issue is marked done.

## 1. Static checks

```bash
checks/static.sh
```

- Reads `site/orchestrating-claude.html`, or the page you pass as the first argument.
- Prints PASS or FAIL for static-1 to static-5:
  - loop-colour roles
  - no `--series-*` tokens
  - the artifact page contract
  - external links open in a new tab
  - no baseline source URL dropped (`checks/urls-v11.txt`)
- Writes `build/preview.html`, a copy wrapped in a doctype and body as the artifact viewer does, for the DOM checks.
- Exits 1 on any FAIL.

## 2. DOM checks

Before you run any of the three Playwright scripts (`run-dom.js`, `shots.js`, `compendium-check.js`), set the `ROOT` constant at the top of the file to the absolute path of your clone. It ships as the placeholder `/path/to/claude-guides`, so the repository holds no personal path. Do not commit your edit.

Run `checks/run-dom.js` with Playwright's `browser_run_code_unsafe` tool, passing it as `filename` (or pasting its code as `code` if the tool refuses files outside its allowed folders).

- Loads `build/preview.html` in Chromium in eight views:
  - 320 light
  - 375 light and dark
  - 414 light
  - 768 light
  - 1024 dark
  - 1280 light and dark
- Injects `checks/dom-checks.js` and runs it in each view.
- Runs the phase-explorer keyboard scenarios.
- Output is one line per check, naming the views it fails in.

`dom-checks.js` also works on its own in any browser console. Load the file, then run `window.__uxChecks()`.

| Check | What it asserts |
|---|---|
| dom-1 | No page-level horizontal overflow |
| dom-2 | The h1 fits its column and does not overlap `.thesis` |
| dom-3 | Every visible SVG `<text>` renders at 12px or more (11px for `.tick`) |
| dom-4 | No `.tbl-wrap` or `.scroll` scrolls sideways, unless it has `data-scroll-ok`, a `.scroll-cue`, `tabindex=0`, `role=region` and an `aria-label` |
| dom-5a | Text contrast is AA: 4.5:1, or 3:1 for large text. SVG text is measured against the shape beneath it |
| dom-5b | Form-field borders and diagram edges reach 3:1 |
| dom-6 | Every `#` link resolves, and every "Lesson N" outside a kicker is a link |
| dom-7 | Every SVG has a role and label, headings never skip a level, and no card h3 sits under an h3 subhead |
| dom-8 | Every `a.ev` opens in a new tab with noopener and `data-src`, and every `span.ev` is focusable |
| dom-9 | Each `#glossary [data-term]` is first used after or inside the glossary |
| dom-10 | The evidence chart draws as many benchmarks as its caption names |
| kbd-1 to kbd-3 | Phase explorer: arrow keys move from the focused node, the group is one tab stop, and focus survives at phase 10 |
| dom-11 | Skip link, phone lesson menu, and Next and Contents on every lesson |
| dom-12 | Reading paths, levels and minutes, grouped rail, collapsed extras |
| nav-1, nav-2 | Phone menu stays at the top; choosing Lesson 17 shows its heading below the menu |
| quiz-1 | Quiz: arrow keys choose without scoring; Check answer scores |
| dom-13 | The theme toggle is a 44px `<button>`; the page is dark or light; the sun shows in dark and the moon in light, each with the matching aria-label; two clicks restore the theme |
| theme-1 to theme-5 | With empty storage the page loads dark even when the system prefers light; one click gives light; the choice survives a reload; a viewer's own `data-theme` gives way to it; a second click gives dark |
| page-1, page-2 | Every id is unique; no script errors in any view |

`run-dom.js` also covers 768 and 1024px, so eight views in all. The page starts dark and remembers the reader's choice, so `run-dom.js` and `shots.js` set the page theme to match each view's emulated colour scheme; the theme scenario opts out with `?theme-test`.

The v11 baseline is in `baseline-v11.txt`. Version 17, last updated 2026-10-27, passes all 27 checks.

## 3. Compendium check

`compendium-check.js` checks `docs/orchestrating-claude-compendium.html`:

- no sideways scroll at 1280, 375 and 320px
- every `#` link has a target
- unique ids
- search finds and marks text
- no script errors
- no network requests, so it works offline

The Playwright tool may only load script files from its allowed folders. If it refuses the file, paste the script's code into `browser_run_code_unsafe` as `code`.
