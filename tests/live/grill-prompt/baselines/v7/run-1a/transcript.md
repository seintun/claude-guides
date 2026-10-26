# Dry run 1a transcript: Dump 1 (small task)

Request: "My CLI's --help text is out of date after we renamed the export flag. Fix it so it matches. Should take an hour."

Date: 2026-10-24. Project root: `project/` (empty, no git repository).

## Part 1: /grill

**Look before you ask.** I searched the project root for source code, a README, CLAUDE.md, docs/ and git history. The folder is empty and there is no git repository, so I can't see the CLI, its flag names or its help text, and nothing here says where they live. The request already gives the appetite (an hour) and the scope (the --help text), so I won't ask for those.

### Grill question 1 (fact question, open, no options)

Where does the CLI's source code live (a repository name or a folder path)?

*Why this first:* the flag names, the help text and the tests all live in that code, so every other question depends on it.

**Simulated user:** I don't know.

*Skill's handling:* "I don't know" is not a decision. It goes in the log under open questions as `UNKNOWN: <why>`. The new flag name, the old name, the file that defines the help text and the test command all live in the same code, so I can neither look them up nor usefully ask for them yet. I will not ask the user to recite them. The prompt will make the session read the new name from the CLI's parser (the source of truth) and find the old name in the stale help text or git history.

### Grill question 2 (judgment question)

What should prove that the help text now matches the renamed flag? I recommend A: it is the smallest check that fails if the old name is left behind, and it fits the hour you gave.

- **A. Output check (Recommended).** Run the help for the main command and for every subcommand that takes the export flag. Each output names the new flag and never the old one. Implies: a short, repeatable check with no new test files. Costs: it does not catch other flags whose help has drifted.
- **B. Permanent test.** Add a test that fails whenever any flag listed in the help differs from the parser's flags. Implies: protects against future drift. Costs: new test code, probably more than the hour you gave, and it reaches past the export flag.
- **C. Read-through only.** A person reads the help and agrees it matches. Implies: fastest. Costs: nothing repeatable, and an old mention inside a subcommand's help can slip by.

**Simulated user:** A. (The request says an hour and names only the export flag, so it does not imply B or C.)

### Grill question 3 (judgment question)

If the old flag name also shows up outside the --help output (README, man page, shell completions, example scripts), what should the run do? I recommend A: your request is about the --help text, and an hour leaves no room to audit other docs.

- **A. Leave them and list them (Recommended).** Change only the help text. The report lists each other place by file and line. Implies: a small diff that is easy to review, and you decide about the rest. Costs: those places stay stale until someone fixes them.
- **B. Fix them too.** Implies: one consistent rename everywhere. Costs: more files than the request names, a risk of touching generated files or release docs, and it may overrun the hour.
- **C. Stop and ask.** Implies: you decide place by place. Costs: the run stalls until you answer.

**Simulated user:** A. (The request scopes the fix to the --help text, which agrees with A.)

### Grill stop and confirmation

No branch is open: the problem, appetite and scope come from the request, the code's location is logged as unknown, and the outcome check and the no-go are decided. I did not ask who reads the help or what the stale text has cost, because the fix is the same either way; that is noted in the log.

Decision log: `project/docs/discovery/cli-help-rename.md` (no git repository, so not committed).

Summary for you to confirm:

1. Appetite is one hour, and the scope is the `--help` text only, from your request. No change to flag behavior.
2. Done means: the help for the main command and every subcommand that takes the export flag names the new flag and never the old one.
3. Other places that mention the old name are left alone and listed in the report.

Every UNKNOWN line:
- UNKNOWN: where the CLI's source lives. You said "I don't know".

Every ASSUMED line:
- ASSUMED: the rename is finished in the parser and the new name is final (cheapest test: run the CLI with the new name and confirm it is accepted).
- ASSUMED: the failure cases are every place the help output names the old flag: usage line, examples, other flags' descriptions and subcommand help.
- ASSUMED: a test or stored copy of the help output that fails after the fix is regenerated from the real output; no other test is edited.

Please confirm these. This is not a go-ahead to build anything.

**Simulated user:** Confirmed.

*End of /grill.*

## Part 2: /prompt

Input: the request and the decision log above.

**Step 1, look before you ask.** The project folder is still empty: no README, CLAUDE.md, test command or plans in docs/. The decision log is the only input. Where the work lives is logged there as UNKNOWN (the user did not know), so I do not ask it again.

**Step 2, interview only for gaps.** The outcome, the done-when check and the risk are all settled by the request and the log. No question asked at this step. (Questions used: 0 of 5.)

**Step 3, size.** One slice, low risk: goal, checks, receipt, no plan file. A decision log stands behind the prompt, so step 10 calls for a fresh review.

**Step 4, who does what.** One writer, no helpers. The prompt makes the session run the output check first and see it fail (red), then edit, then see it pass (green). No tests are edited.

**Steps 5 to 7.** Drafted from the parts in order. No helpers, so no briefs and no synthesis step. Not a loop or unattended run, so no Template H.

**Step 8, consistency pass.** Files, helpers, time, transformations, skips, targets, evidence, caps and contradictions all pass, except one:

- The first STOP AND ASK line reads "the working directory does not hold the CLI's source". Tested against what is known now (an empty folder, no repository), that line already holds. The skill says a line that already holds is settled with the user before saving.

### Prompt question 1 (judgment question)

The prompt's first step needs the CLI's source and a git repository, and this project folder holds neither, so the stop line "the CLI is not in the working directory" is true today. How should the prompt treat it? I recommend A: the person who starts the run knows which repository holds the CLI even though you did not have the path to hand just now, and a stop costs little.

- **A. Run from the CLI's repository and stop if it is not there (Recommended).** The prompt tells the session to start in the repository that holds the CLI and to stop with BLOCKED if no parser and no help text are found. Implies: no guessing. Costs: you must start the session in the right folder.
- **B. Ask for the path first.** The run opens by asking you for the repository path or folder. Implies: the path is supplied by you at the start. Costs: the path stays unknown in the prompt, and the run waits on you before any work.

**Simulated user:** A. (The request does not imply B.)

*Applied:* the line stays as a settled start condition. Decision 3 is added to the decision log. (Questions used: 1 of 5.) The draft is written to `prompt-r0.md`. Steps 9 and 10 are run by the lead.

### Step 9 and step 10, round 1

Lead's check_prompt.py output: no FAIL; WARN c-6 on line 17 ("1 or" in "prints 1 or more").

Fresh review r1: one blocker. CONSTRAINTS require covering the old flag "in any spelling or case", but checks 1 and 4 used one case-sensitive `<old-name>`, so a help line with the old flag in another case or form would leave every check green.

Fixes in `prompt-r1.md`, nothing else changed:
- The WARN: "prints 1 or more" now reads "prints a count above zero".
- The blocker: a new term `<old-forms>` (grep options for the dashed form, the underscore form, an upper-case placeholder and any short alias, each matching only the old flag). Checks 1 and 4 now use `grep -ci <old-forms>` and `git grep -n -i <old-forms>`. Steps 2 to 4, the STOP AND ASK line on the premise and the REPORT carry `<old-forms>`.

No new question was needed, so the decision log is unchanged. (Questions used: 1 of 5.)

<!-- end -->
