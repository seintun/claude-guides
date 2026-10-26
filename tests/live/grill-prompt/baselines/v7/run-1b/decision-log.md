# Export flag help text: decision log

Opened: 2026-10-24
Request (the user's words): "My CLI's --help text is out of date after we renamed the export flag. Fix it so it matches. Should take an hour."
Status: grill finished 2026-10-24, summary shown to the user for confirmation

## Decisions

Each entry: date, question, answer, reason.

- 2026-10-24 | Problem | The CLI's --help text still names the export flag by its old name after the rename. | Given in the request, so not asked.
- 2026-10-24 | Wanted outcome | Make the --help text match the renamed flag. | Given in the request ("Fix it so it matches"), so not asked.
- 2026-10-24 | Appetite (time budget) | One hour. | The user's words: "Should take an hour."
- 2026-10-24 | Which help text to update | Every --help screen (root command and every subcommand, including usage lines and examples) that names the old flag. README, man page, shell completions and error messages are out of scope. | A reader may land on any screen, and one stale screen leaves the problem in place. The user picked the recommended option (option A of three).
- 2026-10-24 | No-gos and rabbit holes | Rename mentions only: replace the old flag name with the new one inside help strings. No change to flag parsing or behaviour, no deprecated alias for the old name, no rewording of the help. | The flag is already renamed (per the request), so the problem is stale text; code changes add risk the request does not ask for. The user picked the recommended option (option A of three).
- 2026-10-24 | Outcome metric (how to show the help matches) | Capture every --help screen and search for the old name: it appears on no screen, and the new name appears on the export flag's screen. A capture taken before the edit must show the old name, so the search is known to be able to fail. | Anyone can rerun it, it needs no test setup, and it fails while any screen still shows the old name. The user picked the recommended option (option A of three). It proves the help text only, not that the flag works.
- 2026-10-24 | Where the session that runs the prompt starts (settled during /prompt, question P1) | Inside the CLI's own git repository (option A of three). Not a copy or export of the source without history, and not a first step that clones the repository. | Every check reads the source and a git diff from the working directory, and the empty project root here can supply neither. The user picked the recommended option. This settles the starting folder only: where the source lives stays UNKNOWN (first open question), and the prompt stops if the working directory is not a git repository or holds no CLI source.
<!-- decisions-end -->

## Open questions

- UNKNOWN: where the CLI's source code lives. The user does not know (asked 2026-10-24), and the project root is empty: no source, README, CLAUDE.md, build files or git repository.
- UNKNOWN: the export flag's current (new) name. The user does not know (asked 2026-10-24) and the code is not available to read.
- UNKNOWN: the export flag's previous (old) name, as the current help text shows it. The user does not know (asked 2026-10-24) and the code is not available to read.
- ASSUMED: the people who struggle are CLI users who copy the flag name from --help, so a stale name points them at the wrong flag. The request does not say who they are or what the stale text has cost them, and the work does not depend on it.
- ASSUMED: the parser already defines the export flag under its new name and only the help text lags (the request says the flag was renamed). This is the riskiest assumption. Cheapest test: read the parser's definition of the export flag and compare it with the help text as it is now, before editing.
- ASSUMED: the changes stay uncommitted for the user to review, because committing waits for the user's explicit yes and the request does not ask for it.
- Not done: this log is not committed and not linked from an issue, because the project root has no git repository and the request names no issue.
<!-- open-end -->
