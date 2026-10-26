#!/usr/bin/env bash
# Installs the /guide skill as a symlink, then prints the CLAUDE.md snippet and the
# paste-in prompt with this clone's root filled in.
# Usage: skills/guide/install.sh            dry run: show the change, write nothing
#        skills/guide/install.sh --apply    create or update the symlink
# Undo:  rm ~/.claude/skills/guide
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# A git hook in a linked worktree exports GIT_DIR, which makes rev-parse report $here as the root.
unset GIT_DIR GIT_WORK_TREE
GUIDE="$(git -C "$here" rev-parse --show-toplevel)"   # the repo root, found the same way the skill finds it
skills_dir="$HOME/.claude/skills"
link="$skills_dir/guide"
target="$GUIDE/skills/guide"

if [ -e "$link" ] && [ ! -L "$link" ]; then
  echo "STOP: $link exists and is not a symlink. Move it aside first." >&2
  exit 1
fi
current="$(readlink "$link" 2>/dev/null || true)"

echo "Guide root: $GUIDE"
if [ "$current" = "$target" ]; then
  echo "No change: $link -> $target"
else
  echo "Change to ~/.claude:"
  if [ -n "$current" ]; then echo "- $link -> $current"; fi
  echo "+ $link -> $target"
  if [ "${1:-}" = "--apply" ]; then
    mkdir -p "$skills_dir"
    ln -sfn "$target" "$link"
    echo "Applied. Start a new Claude Code session, then type /guide."
  else
    echo "Dry run: nothing written. Rerun with --apply to make the change."
  fi
fi

echo
echo "CLAUDE.md snippet (one line, for any project):"
sed "s|{{GUIDE}}|$GUIDE|g" "$here/snippet.md"
echo
echo "Paste-in prompt (one-off sessions):"
sed "s|{{GUIDE}}|$GUIDE|g" "$here/prompt.md"
