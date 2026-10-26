@AGENTS.md

## Claude Code notes

- **Browser checks:** run `checks/run-dom.js` and `checks/shots.js` with the Playwright MCP tool `browser_run_code_unsafe`, passing the file as `filename`. Both read `build/preview.html`, which `checks/static.sh` writes. Reviewing the published page needs the built-in browser pane, signed in to claude.ai.
- **Subagent roles that worked here:**
  - Sonnet subagents for reviews and drafts.
  - `doc-checker` for primary-source fact checks.
  - Haiku scouts for read-only sweeps.
  - Independent reviewers get files and a brief, never the builder's report.
- **Publishing:** use the Artifact tool with `url` set to the live artifact, and only when the owner asks.
- **Scratch files:** go in the session scratchpad, not in this repository. `build/` is ignored.
