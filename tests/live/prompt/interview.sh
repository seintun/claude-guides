#!/usr/bin/env bash
# Interview check: given a vague request and no "skip questions", the skill's first message
# should look things up, then ask exactly one question with the recommendation first, and write nothing.
# Reuses the grill transcript checker's question rules (grill-4 to grill-7).
# Usage: interview.sh <work dir>
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo="$(git -C "$here" rev-parse --show-toplevel)"
dir="$1/prompt-interview"
rm -rf "$dir"; mkdir -p "$dir/project"
printf '# Notes service\n\nNode 20 and PostgreSQL 16. Run the tests with `npm test`.\nDeploys from main through GitHub Actions.\n' > "$dir/project/README.md"
body="$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$here/../../../skills/prompt/SKILL.md")"
prompt="${body//\$ARGUMENTS/I want search in our notes service to be better.}"
( cd "$dir/project" && timeout 400 claude -p "$prompt" --model sonnet \
    --allowedTools "Read,Grep,Glob" --output-format stream-json --verbose > "$dir/transcript.jsonl" )
python3 -I "$repo/skills/grill/check_transcript.py" "$dir/transcript.jsonl"
