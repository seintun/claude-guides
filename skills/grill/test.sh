#!/usr/bin/env bash
# Cold test of the grill skill: one fresh Claude Code session, in a throwaway project
# outside this repository, grills a vague request. check_transcript.py then checks the
# first message against the grill rules.
# Usage: skills/grill/test.sh              the skill's text, sent as the prompt (no install needed)
#        skills/grill/test.sh --installed  call /grill (needs ~/.claude/skills/grill)
# Needs: the claude CLI, signed in. Costs one short session.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
request="I want to add full-text search to our notes service."
# Set GRILL_TEST_DIR where the default temp folder is not writable (a sandbox, say).
# The test works in a new subfolder there and deletes only that subfolder.
if [ -n "${GRILL_TEST_DIR:-}" ]; then
  work="$GRILL_TEST_DIR/grill-test.$$"
  mkdir -p "$work"
else
  work="$(mktemp -d)"
fi
trap 'rm -rf "$work"' EXIT

# The fixture: a project whose README answers two questions the grill must not ask.
mkdir -p "$work/project"
printf "# Notes service\n\nNode 20 and PostgreSQL 16. Run the tests with \`npm test\`.\nDeploys from main through GitHub Actions.\n" > "$work/project/README.md"

if [ "${1:-}" = "--installed" ]; then
  prompt="/grill $request"
else
  body="$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$here/SKILL.md")"
  prompt="${body//\$ARGUMENTS/$request}"
fi

(cd "$work/project" && claude -p "$prompt" --model sonnet \
  --allowedTools "Read,Grep,Glob,Bash(ls:*),Bash(cat:*)" \
  --output-format stream-json --verbose > "$work/transcript.jsonl")

python3 -I "$here/check_transcript.py" "$work/transcript.jsonl"
