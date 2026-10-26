# Transcript, run 2b (Dump 2, report)

Request: "Need a write-up for my manager on whether we should move CI from GitHub Actions to Buildkite. Costs have gone up and builds are slow on the monorepo. She wants it next Friday, and she cares most about cost and how much migration work it is. I don't know our actual monthly CI spend."

Today is Saturday 2026-10-24.

## /grill

Grill's opening message to the user:

> I looked in the project folder first. It is empty: no code, no README, no docs, no git repository, and no CI configuration, billing export or build log. So I found nothing about your CI here.
>
> From your request I already have: the question is whether to move CI from GitHub Actions to Buildkite; costs have gone up and builds on the monorepo are slow; your manager cares most about cost and then migration work; she wants it "next Friday"; and you don't know the monthly CI spend. I won't ask any of that again.
>
> I'll ask one question at a time and log each answer in `docs/discovery/ci-buildkite-writeup.md`.

### Q1 (deliverable)

Grill asks:

> What should the write-up be? I recommend the short decision memo, because she asked whether to move, and she cares most about cost and migration work, which a recommendation-first memo puts at the top.
>
> A. Short decision memo (Recommended). It opens with a move, stay or wait call, then the cost case and the migration work, then supporting detail. It costs you a committed call that has to hold up when she challenges it.
> B. Neutral comparison. A side-by-side table with no call. It costs you her question "so should we move?", which it leaves unanswered.
> C. Full migration plan. Steps, order and risks. It costs far more work than a write-up on whether to move, and it presumes the answer is yes.

Simulated user: A. The request asks "whether we should move", which wants a call.

### Q2 (baseline)

Grill asks:

> What should Buildkite be compared against? I recommend staying on GitHub Actions as it runs today, because that is the question she asked and it fits a tight deadline.
>
> A. Buildkite against staying as is (Recommended). It answers "move or not" directly. It costs you any in-place fix for the cost or the slow builds: the memo can only say that one was not evaluated.
> B. Also add one in-place fix for the cost and the slow builds. It answers "why not just fix what we have?" before she asks. It costs a second research branch and more time before the deadline.

Simulated user: A. The request asks "whether we should move", a two-way comparison.

### Q3 (cost scope)

Grill asks:

> Which costs should the write-up count? I recommend everything that changes with the move, kept as separate lines, because she cares about migration work as well as the bill, and a bills-only view would hide the work.
>
> A. Everything that changes with the move, as separate lines (Recommended): vendor charges, the compute the builds run on, and the migration effort in engineer-weeks. It needs more inputs and gives no single total.
> B. Vendor charges only. It is the simplest, from two price pages and one bill. It leaves out the build compute and the migration time, which can cancel a saving.

Simulated user: A, the recommended option.

### Q4 (migration work measure)

Grill asks:

> How should the write-up express the migration work? I recommend a counted inventory with a range in engineer-weeks, because she ranks migration work second, and a range built from counted items can be checked where a size label cannot.
>
> A. Inventory plus a range in engineer-weeks (Recommended). Count the workflow files, third-party actions, secrets and runner types in the monorepo's CI configuration, then give a low-to-high range and its main drivers. It needs the configuration; without it the memo can only list what to count.
> B. A size label (small, medium or large). It is quick and needs no configuration. It gives her nothing to check, and the label hides what drives the effort.

Simulated user: A, the recommended option.

### Q5 (build speed)

Grill asks:

> How much weight should build speed get? I recommend a secondary role, because the request says she cares most about cost and migration work, and a speed gain from a move is the claim least likely to be proven in a desk write-up.
>
> A. Secondary criterion (Recommended). Report the current build times and what a move could change, with no promised gain. It costs you a headline for the slow builds.
> B. Equal weight with cost. The memo argues speed as a full third pillar. It costs you evidence you do not yet have, and risks a claim the move does not deliver.
> C. Leave it out. The memo covers cost and migration only. It costs you the other half of why you raised the move.

Simulated user: A. The request puts cost and migration work first.

### Q6 (decision rule)

Grill asks:

> What decision rule should the memo give her? I recommend showing the net monthly saving and the migration effort side by side, with the payback as a formula she prices herself, because pricing an engineer-week needs a figure only the company holds and you do not have.
>
> A. Side by side, payback as a formula (Recommended). The memo gives the net monthly saving and the effort in engineer-weeks, and a formula for months to repay the work with the cost of an engineer-week left as her input. It gives no single payback number.
> B. A single payback in months. The memo converts the effort to money. It costs a guessed or later-supplied engineer-week rate, and one more unknown.
> C. No rule. The memo lists the numbers and stops. It costs her the step from numbers to a call.

Simulated user: A, the recommended option.

### Q7 (where the code lives, fact question, asked open)

Grill asks:

> The project folder is empty, so I can't read your CI configuration from here, and the migration inventory in your last answer depends on it. Where does the monorepo live: a path on this machine, or a hosted repository?

Simulated user: I don't know.

### Q8 (where the cost data lives, fact question, asked open)

Grill asks:

> The cost case needs your recent GitHub Actions bill and usage, and you said you don't have the monthly spend. Where can those figures be read: a billing page, an export, or a person who holds them?

Simulated user: I don't know.

### Q9 (deadline, fact question, asked open)

Grill asks:

> Today is Saturday 2026-10-24, so "next Friday" could be read two ways. Which calendar date is the deadline?

Simulated user: I don't know. I only said "next Friday".

### Q10 (no-gos)

Grill asks:

> What is out of bounds while the write-up is prepared? I recommend desk research only, because the memo is advice and a trial or a sales contact would commit the company to something before she has seen the numbers.
>
> A. Desk research only (Recommended). Read public pricing and documentation and any data you supply. No vendor sign-ups, trials or sales contact, no change to any CI configuration, no pilot pipeline, and no message sent to your manager or anyone else. It costs you any figure that only a vendor quote or a pilot would give.
> B. Allow a vendor quote request. It could replace list prices with a real quote. It costs a contact made in your company's name before she has asked for it.
> C. Allow a pilot pipeline on Buildkite. It would give a measured build time. It costs setup time, an account and a risk of touching live CI, none of which fits a write-up.

Simulated user: A, the recommended option.

### Q11 (riskiest assumption)

Grill asks:

> Which assumption is riskiest, so the cheapest test goes first? I recommend the cost saving, because it is what she cares about most, and the cheapest test needs only public prices and your own usage.
>
> A. The saving is real once the build compute and the migration effort are counted (Recommended). Cheapest test: price your last full billing period of GitHub Actions usage against Buildkite's published pricing, before any other analysis. It costs you nothing until the usage figures arrive, and the test is empty without them.
> B. The slow builds are caused by the CI service, not by the monorepo's own build design. Cheapest test: split a few recent runs into queue wait and build steps. It costs you the same missing data, and it only bears on the secondary criterion.

Simulated user: A, the recommended option.

### Grill's close: summary for confirmation

> Here is what I have. Please confirm or correct.
>
> Decisions:
> 1. A short decision memo that opens with a move, stay or wait call.
> 2. Buildkite is compared only against staying on GitHub Actions as it runs today; no in-place fix.
> 3. Costs counted as separate lines: vendor charges, build compute, migration effort in engineer-weeks.
> 4. Migration work is a counted inventory from the monorepo's CI configuration plus a low-to-high range in engineer-weeks; without the configuration, only the list of what to count.
> 5. Build speed is a secondary criterion: current times reported, no promised gain.
> 6. Net monthly saving and engineer-weeks side by side, with payback as a formula and her price for an engineer-week as the input.
> 7. Desk research only: no sign-ups, trials, sales contact, CI changes, pilot pipeline or messages sent.
> 8. Riskiest assumption is the cost saving; cheapest test is last billing period's usage priced against published Buildkite pricing.
>
> ASSUMED:
> - ASSUMED: "build time" means wall-clock time from a push to the last check finishing on the monorepo's main pipeline; no check depends on it.
>
> UNKNOWN:
> - UNKNOWN: location of the monorepo and its CI configuration.
> - UNKNOWN: where the GitHub Actions bill and usage figures can be read.
> - UNKNOWN: the deadline's calendar date, 2026-10-30 or 2026-11-06.
> - UNKNOWN: the monthly CI spend.
>
> Four unknowns means the next step, the prompt, will say it is not ready to run.

Simulated user: Confirmed, no changes. This is a confirmation of the summary, not a go-ahead to build anything.

End of /grill.

## /prompt

Input: the request and `docs/discovery/ci-buildkite-writeup.md`.

Step 1 (look before asking): the project folder holds only the decision log. The log answers the outcome, the cost scope, the effort measure, the decision rule, the no-gos and the riskiest assumption, so none of those is asked again. Three gaps remain that the log does not settle.

### P-Q1 (how the prompt treats missing inputs)

Prompt-writer asks:

> Your folder is empty and four things are unknown (where the monorepo lives, where the bill can be read, the deadline's date and the monthly spend), so a line saying "stop if the data is missing" would fire the moment the prompt starts. How should the prompt treat missing inputs? I recommend asking once at the start and carrying on with what arrives, because a memo with labelled gaps is still something you can finish before the deadline.
>
> A. Ask once, then carry on (Recommended). Each missing input becomes a labelled gap in the memo with the exact figure needed. The call is Wait unless the cost lines and the effort range both rest on supplied data. It costs you a Wait where you hoped for a clean Move or Stay.
> B. Stop until every input is supplied. The call is always Move or Stay. It costs you any draft at all if the figures take long to find.

Simulated user: A, the recommended option.

### P-Q2 (where the memo is saved)

Prompt-writer asks:

> Where should the finished memo be saved? I recommend one Markdown file in the project's docs folder, because it needs no tooling and you can paste it into whatever your manager reads.
>
> A. `docs/ci-migration-memo.md` in the project (Recommended). A check can read it. The folder is not a git repository yet, so nothing tracks the file until you add one.
> B. In the chat only. It leaves no file to maintain. It costs you a saved copy, and no check can read it.

Simulated user: A, the recommended option.

### P-Q3 (plan in use, fact question, asked open)

Prompt-writer asks:

> The Actions prices and allowances depend on the GitHub plan your team is on. Which plan is it?

Simulated user: I don't know.

Step 3 (size by risk) and step 10 (review): one deliverable with a research step and a fresh reviewer, because the memo rests on sourced prices and a decision log sits behind it. The draft is written to `prompt-r0.md`; the lead runs the checker and the review.

### Round 1 fixes (no new question asked)

The checker's FAIL (relative terms) and WARN (unlabelled counts) and the reviewer's three blockers were fixed in `prompt-r1.md` without a new question to the simulated user: computed figures are allowed when shown with inputs and arithmetic; usage inputs (people using CI, builds running at once) are folded into the existing "where can the bill and usage be read" gap, which the simulated user already answered "I don't know"; `GAP:` lines live only in one section; a cost-lines check was added by merging the heading check and the sources check.

<!-- transcript-end -->
