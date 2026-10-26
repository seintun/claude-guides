# Draft: running example, recall items, quiz, try-now (child 12)

Text only. Nothing here has been applied to `site/orchestrating-claude.html`.

How to apply:
- The page was being edited while this was drafted, so each spot is a quoted anchor, not a line number. "End of lesson" means: before that lesson's `<p class="lesson-end">` footer.
- Example paragraphs reuse the page's own `.note` class plus a hook class (`running-ex`). No new CSS is needed.
- No links are added, so the evidence-URL check is unaffected.
- The story, in order: issue (L3), goal (L4, exists), phases (L5), helpers (L6), scenario (L9, exists), ticket to PR (L12), retro (L13), failure (L15). The failure happens at Verify, so L13 and L15 describe the same event from two sides.

---

## 1. Running example insertions

Goal facts every paragraph stays inside: only change `src/reports/`; no new packages; `npm test` with a new empty-report test; the file opens in Excel with the same columns; exactly the rows on screen; one session, up to 3 helpers; stop if the same test fails twice.

### Lesson 1 (#loop)

Goes after: the `</figure>` that closes the loop figure (its figcaption starts `<strong>The check decides when the loop ends.</strong>`), and before `<p>Three roles keep this loop healthy…`.

```html
<p class="note running-ex"><b>Running example</b> (it comes back in later lessons). Take the goal "Users can export the reports table to CSV." Claude plans a small step and makes the change. Check then runs <code>npm test</code>: a fail sends it back to adjust, and only a pass lets it call the work done, with proof.</p>
```

### Lesson 3 (#discovery)

Goes after: the stage table, the `<div class="tbl-wrap">…</div>` whose last row is `<td class="job">Slice</td><td>Issues with outcome, check, boundary and dependencies</td>`, and before `<p class="note"><span class="ev d"…>Our pipeline, built from these…`.

```html
<p class="note running-ex"><b>Running example.</b> The pain: people want the reports table in a spreadsheet. Slice turns it into one issue: outcome "Users can export the reports table to CSV", boundary "only <code>src/reports/</code>, no new packages", and no dependencies. Its check has three lines: the export has exactly the rows on screen, <code>npm test</code> passes with a new test for an empty report, and the file opens in Excel with the same columns as the table.</p>
```

### Lesson 5 (#phases)

Goes after: the `<ul class="plain">` that ends with `<li><b>Learn</b> turns each run into better rules for the next one…`, at the end of the lesson.

```html
<p class="note running-ex"><b>Running example.</b> For the CSV export, Explore returns a few short reports with file paths: where the reports table gets its rows and its columns. Plan is a plan file in <code>docs/</code> with ordered slices, the test for each, and how to undo each one. Verify ends in a receipt: PASS, FAIL or NOT RUN, with the command, for each of the three Done when lines.</p>
```

### Lesson 6 (#orchestration)

Goes after: the `</figure>` of the context chart (figcaption starts `<strong>Context used by the lead, step by step.</strong>`), and before `<div class="two-col">` ("Send a helper when").

```html
<p class="note running-ex"><b>Running example.</b> The CSV goal allows up to 3 helpers, so the lead sends a scout to read how the table builds its rows and columns, a builder to make the export in its own worktree, and a verifier to re-run the checks. Before and after, with made-up numbers (illustrative, not measured): one session reading everything itself opens about 40 files and its window fills with raw reading; with the scout, the lead receives 3 short summaries. The lead keeps the plan and the final say on "done".</p>
```

### Lesson 12 (#pipeline)

Goes after: the `</figure>` of the sequence diagram (figcaption starts `<strong>You act only at the edges; checks and status moves happen on their own.</strong>`), and before `<div class="two-col">` ("Who moves each status").

```html
<p class="note running-ex"><b>Running example.</b> The CSV issue from Lesson 3 goes into Triage, and you delegate it. The agent opens a branch and a draft PR, and the required checks run <code>npm test</code>, including the empty-report test. Your team's GitHub automation moves the issue to In Review; after you approve, merging the PR that says "Fixes ID" moves it to Done.</p>
```

### Lesson 13 (#growing)

Goes after: the scorecard table, the `<div class="tbl-wrap">…</div>` under `<h3>A scorecard to track per task</h3>` that ends with the "All-runs pass rate" row, at the end of the lesson.

```html
<p class="note running-ex"><b>Running example.</b> The CSV row in the log shows one rework loop: Verify sent the work back to Build once, because the first file held a row the filter had hidden. The retro picks one change: turn the check "3 rows filtered to 2" into a test in <code>npm test</code>, so the gate catches it on the next run.</p>
```

### Lesson 15 (#failures)

Goes after: the failures table, the `<div class="tbl-wrap">…</div>` whose last row is `<td class="job">Run ended with no receipt</td>`, at the end of the lesson.

```html
<p class="note running-ex"><b>Running example.</b> The CSV builder said "Done!", but the file had 3 rows when the screen showed 2: it included the row the filter had hidden. That is the "Done!" but broken row: the builder graded its own work, so nobody ran the check. The fix was a fresh verifier running "Given 3 rows filtered to 2…" and recording FAIL; the work went back to Build, and the receipt now shows PASS with the command.</p>
```

Count after insertion: the example appears in lessons 1, 3, 4, 5, 6, 9, 12, 13, 15 (9 lessons; `grep CSV` finds it in each).

---

## 2. Recall items

Optional style, using tokens already on the page (same pattern as `details.table-view`). The "Predict, then open" label comes from CSS so each summary stays a plain question:

```css
details.recall{margin:18px 0;border:1px solid var(--rule);border-radius:8px;padding:10px 14px;font-size:15px}
details.recall summary{cursor:pointer;font-weight:600;color:var(--accent)}
details.recall summary::before{content:"Predict, then open: ";font-weight:400;color:var(--ink-2)}
details.recall p{margin:8px 0 0}
```

### Lesson 1: after the roles list

Goes after: the `<ul class="plain">` that ends `<li><b>Helpers and gates</b> do side work and run checks the lead can't skip.</li>`, at the end of the lesson.

```html
<details class="recall"><summary>What happens if Check is missing?</summary><p>Claude stops when it feels finished, which is not the same as done. Why: the loop ends well only when Check is real, such as a test, a command or an observation.</p></details>
```

### Lesson 4: after the weak and strong goals

Goes after: the `<div class="compare">…</div>` block, and before `<h3>Build your goal prompt</h3>`.

```html
<details class="recall"><summary>In the CSV goal, "up to 3 helper agents" belongs under which of the five parts, and "No new packages" under which?</summary><p>Budget, then Constraints. Why: Budget is how much effort to spend; Constraints is what is off limits, such as files and packages.</p></details>
```

### Lesson 5: after the running example

Goes after: the Lesson 5 running-example paragraph above (so at the end of the lesson).

```html
<details class="recall"><summary>Which of the ten phases comes before anything is built and has a fresh reviewer argue against the plan?</summary><p>Critique. Why: a reviewer that never saw Claude's reasoning argues against the plan before building starts.</p></details>
```

### Lesson 6: after the two panels

Goes after: the `<div class="two-col">…</div>` holding "Send a helper when" and "Do it in the lead when", and before `<p><b>Brief a helper like a capable colleague…`.

```html
<details class="recall"><summary>Sort these 6 jobs into lead or helper: (a) read many files and report only the conclusion; (b) change one line in a file you already have open; (c) fix a failing test from the exact error text you just saw; (d) review a finished change you did not write; (e) list every place a name appears; (f) two jobs that would both edit the same file.</summary><p>Helper: a, d, e. Lead: b, c, f. Why: a is wide reading where only the conclusion matters, d needs a judge who didn't do the work, e is a cheap list job; b would take longer to brief than to do, c needs every detail, f would have two helpers editing the same file.</p></details>
```

### Lesson 9: between the receipt paragraph and the pass^k paragraph

Goes after: `<p>Ask for a <b>receipt</b> at the end of every task…`, and before `<p>For anything that runs unattended, measure how often <b>every</b> run succeeds…` (that next paragraph states the 42%, so the question comes first).

```html
<details class="recall"><summary>75% per run: what's the chance 3 runs in a row all pass?</summary><p>About 42% (0.75 × 0.75 × 0.75 ≈ 0.42). Why: for unattended work, what counts is how often every run succeeds, not whether one did.</p></details>
```

### Lesson 15: before the table

Goes after: `<p class="intro">Almost every problem with autonomous agents traces back to…`, and before the `<div class="tbl-wrap">` failures table (so the reader predicts before seeing the cause column).

```html
<details class="recall"><summary>Claude keeps retrying the CSV export test and has failed with the same error five times. What is the likely cause?</summary><p>No retry cap. Why: the fix is a rule to stop after 2 failures with the same cause and ask a fresh agent for a second opinion, like the "same test fails twice" line in the Lesson 4 goal.</p></details>
```

---

## 3. Lesson 16 quiz

Goes after: `<p class="progress" id="check-progress">0 of 12 done</p>`, at the end of Lesson 16, under a heading such as `<h3>Check what stuck</h3>`. Scores live in memory only: no localStorage, sessionStorage or cookies, so a reload starts fresh.

Questions (correct answer marked):

1. Lesson 1. Claude changes the CSV export, runs the tests, and they fail. In the loop, what happens next?
   - A. It stops and reports that it tried
   - B. It adjusts, fixing the cause, and plans again (correct)
   - C. It skips the check and ships anyway
   - D. It asks you to write a new goal
   - Why: Lesson 1 says a failed check sends Claude to Adjust and then back to Plan, and only a pass ends the loop, with proof.
2. Lesson 4. Which line is a good "Done when" for the CSV export?
   - A. The export works well and feels fast.
   - B. Claude is confident the export is finished.
   - C. npm test passes, with a new test for an empty report. (correct)
   - D. The code follows good practice.
   - Why: Lesson 4 defines Done when as 2 to 5 checks that a command or a person can run, and says a goal without a test is a wish.
3. Lesson 6. You ask a helper to review your change. What should its brief hand over?
   - A. The code and the criteria (correct)
   - B. The code and your conclusion that it is fine
   - C. The criteria only, without the code
   - D. Only the words "please review"
   - Why: Lesson 6 says to hand over the code and the criteria, because a reviewer that reads your conclusion tends to agree with it and the brief is all the context a helper gets.
4. Lesson 9. In the chain from criterion to scenario to gate, which line is the gate?
   - A. Export downloads exactly the rows on screen.
   - B. Given 3 rows filtered to 2, when I click Export, then the CSV has a header and 2 rows.
   - C. A test in npm test, rerun by a Stop hook and by CI on every push. (correct)
   - D. Claude reports that the export works.
   - Why: Lesson 9 turns the scenario into a gate, something that runs every time, whether or not anyone remembers.
5. Lesson 15. Claude says "Done!" but the feature is broken. What is the likely cause?
   - A. The builder graded its own work. (correct)
   - B. The lead's context filled up with raw reading.
   - C. The goal had no budget.
   - D. Two writers edited the same files.
   - Why: Lesson 15 traces "Done!" but broken to the builder grading its own work, and the fix is command output plus a hook or a fresh verifier.

Answer positions: B, C, A, C, A.

### Data (JSON array, `lesson` is the lesson number)

```json
[
  {
    "q": "Claude changes the CSV export, runs the tests, and they fail. In the loop, what happens next?",
    "options": [
      "It stops and reports that it tried",
      "It adjusts, fixing the cause, and plans again",
      "It skips the check and ships anyway",
      "It asks you to write a new goal"
    ],
    "answer": 1,
    "why": "Lesson 1 says a failed check sends Claude to Adjust and then back to Plan, and only a pass ends the loop, with proof.",
    "lesson": 1
  },
  {
    "q": "Which line is a good \"Done when\" for the CSV export?",
    "options": [
      "The export works well and feels fast.",
      "Claude is confident the export is finished.",
      "npm test passes, with a new test for an empty report.",
      "The code follows good practice."
    ],
    "answer": 2,
    "why": "Lesson 4 defines Done when as 2 to 5 checks that a command or a person can run, and says a goal without a test is a wish.",
    "lesson": 4
  },
  {
    "q": "You ask a helper to review your change. What should its brief hand over?",
    "options": [
      "The code and the criteria",
      "The code and your conclusion that it is fine",
      "The criteria only, without the code",
      "Only the words \"please review\""
    ],
    "answer": 0,
    "why": "Lesson 6 says to hand over the code and the criteria, because a reviewer that reads your conclusion tends to agree with it and the brief is all the context a helper gets.",
    "lesson": 6
  },
  {
    "q": "In the chain from criterion to scenario to gate, which line is the gate?",
    "options": [
      "Export downloads exactly the rows on screen.",
      "Given 3 rows filtered to 2, when I click Export, then the CSV has a header and 2 rows.",
      "A test in npm test, rerun by a Stop hook and by CI on every push.",
      "Claude reports that the export works."
    ],
    "answer": 2,
    "why": "Lesson 9 turns the scenario into a gate, something that runs every time, whether or not anyone remembers.",
    "lesson": 9
  },
  {
    "q": "Claude says \"Done!\" but the feature is broken. What is the likely cause?",
    "options": [
      "The builder graded its own work.",
      "The lead's context filled up with raw reading.",
      "The goal had no budget.",
      "Two writers edited the same files."
    ],
    "answer": 0,
    "why": "Lesson 15 traces \"Done!\" but broken to the builder grading its own work, and the fix is command output plus a hook or a fresh verifier.",
    "lesson": 15
  }
]
```

### Reference markup and script (no storage)

Radios give keyboard and screen-reader support for free. Each answer locks its question and shows the explanation; the score appears once all five are answered.

```html
<h3>Check what stuck</h3>
<div id="quiz"></div>
<p class="progress" id="quiz-score" aria-live="polite"></p>
<script type="application/json" id="quiz-data">
  PASTE THE JSON ARRAY ABOVE HERE
</script>
<script>
(function () {
  var Q = JSON.parse(document.getElementById('quiz-data').textContent);
  var root = document.getElementById('quiz');
  var score = document.getElementById('quiz-score');
  var answered = 0, right = 0;
  Q.forEach(function (item, i) {
    var f = document.createElement('fieldset');
    var l = document.createElement('legend');
    l.textContent = (i + 1) + '. ' + item.q;
    f.appendChild(l);
    var fb = document.createElement('p');
    fb.className = 'note';
    fb.setAttribute('aria-live', 'polite');
    item.options.forEach(function (text, j) {
      var lab = document.createElement('label');
      var r = document.createElement('input');
      r.type = 'radio';
      r.name = 'quiz-q' + i;
      r.value = String(j);
      r.addEventListener('change', function () {
        f.querySelectorAll('input').forEach(function (x) { x.disabled = true; });
        var ok = j === item.answer;
        if (ok) right++;
        answered++;
        fb.textContent = (ok ? 'Correct. ' : 'Not quite. ') + item.why;
        if (answered === Q.length) score.textContent = 'Score: ' + right + ' of ' + Q.length;
      });
      lab.appendChild(r);
      lab.appendChild(document.createTextNode(' ' + text));
      f.appendChild(lab);
    });
    f.appendChild(fb);
    root.appendChild(f);
  });
})();
</script>
```

---

## 4. Try now (10 min), Lesson 4

Goes after: the `<div class="builder" data-copy-wrap>…</div>` (the prompt builder), at the end of Lesson 4, before its `<p class="lesson-end">`. It defines receipt in the page's own words, because Lesson 9 is the first place the page does.

```html
<h3>Try now (10 min)</h3>
<ol>
  <li>Pick a small task of your own that you can check in a minute or two.</li>
  <li>Write a goal with the five parts: Outcome, Done when (2 to 5 checks), Constraints, Stop and ask if, Budget. The builder above can help.</li>
  <li>Paste it into Claude and add: "At the end, give me a receipt: each Done when line marked PASS, FAIL or NOT RUN, with the command behind it."</li>
  <li>Let Claude work. If it reaches a Stop and ask if line, answer it.</li>
  <li>Read the receipt. You are done when every line shows PASS with its command; FAIL or NOT RUN means it is not done, so paste the receipt back and name the line to fix.</li>
</ol>
```

What you end up with that you can see: the receipt, with PASS, FAIL or NOT RUN beside each of your Done when lines.

---

## Where each claim comes from on the page (no new facts)

- Goal constraints, Excel columns, empty-report test, up to 3 helpers, "same test fails twice": Lesson 4 strong goal.
- "3 rows filtered to 2" scenario, gate = test in `npm test` rerun by a Stop hook and CI, receipt wording, 42%: Lesson 9.
- Explore reports with file paths; plan file with slices, tests, undo; Verify receipt; failure goes back to Build: Lesson 5 phase data.
- Scout, builder (own worktree), verifier (re-runs checks), lead keeps plan and final say: Lesson 6 diagram. "Illustrative" matches the page's own "Illustrative shape, not measured data" tag.
- Triage, delegate, branch and draft PR, required checks, GitHub automation to In Review, "Fixes ID" to Done: Lesson 12 diagram and status panel.
- Rework loops, retro picks 1 to 3 changes, update tests: Lesson 13 scorecard and diagram.
- "Done!" but broken, builder graded its own work, retry cap, second opinion: Lesson 15 table.
- The only invented story details are the example's own setup: people want the table in a spreadsheet, and the first file held one hidden row. The "about 40 files" and "3 summaries" are marked illustrative.
