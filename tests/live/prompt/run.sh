#!/usr/bin/env bash
# A/B battle test of the /prompt skill. Each scenario runs in a fresh claude -p session, in a
# throwaway project outside the repository:
#   skill    - the skill's text as the prompt, with the scenario as its argument
#   baseline - "Write me a prompt for Claude Code to do this: <scenario>"
# Both are told to skip questions and draft now. score.py grades each draft.
# The skill arm gets its own throwaway guide repository (a git repo holding skills/prompt/SKILL.md
# and the prompts/ ignore rule), so the test also checks where the prompt is saved: in
# <guide>/prompts/<project>/, with nothing written into the project.
# Usage: run.sh <work dir> [round]      ARMS="skill" to run one arm (default: "skill baseline")
# Needs: the claude CLI, signed in. Costs one short session per scenario and arm.
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
work="$1/prompt-ab-${2:-1}"
arms="${ARMS:-skill baseline}"
mkdir -p "$work"

run_one() {  # arm id text
  local arm="$1" id="$2" text="$3" dir="$work/$1-$2"
  rm -rf "$dir"; mkdir -p "$dir/project"
  printf '# Acme app\n\nNode 20 service with a Postgres database. Run the tests with `npm test`. Deploys from main through GitHub Actions.\n' > "$dir/project/README.md"
  local req="$text Skip any questions and draft the prompt now; list your assumptions at the top."
  local prompt extra=()
  if [ "$arm" = skill ]; then
    mkdir -p "$dir/guide/skills/prompt"
    cp "$here/../../../skills/prompt/SKILL.md" "$dir/guide/skills/prompt/SKILL.md"
    printf 'prompts/*\n!prompts/README.md\n' > "$dir/guide/.gitignore"
    # Like the real clone: a commit on main, then a work branch. A checkout left on its default
    # branch can be write-protected by a worktree hook, which would block the save.
    git -C "$dir/guide" init -q -b main
    git -C "$dir/guide" -c user.name=test -c user.email=test@example.com commit -q --allow-empty -m init
    git -C "$dir/guide" switch -q -c work
    local body
    body="$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$here/../../../skills/prompt/SKILL.md")"
    body="${body//\$\{CLAUDE_SKILL_DIR\}/$dir/guide/skills/prompt}"
    prompt="${body//\$ARGUMENTS/$req}"
    extra=(--add-dir "$dir/guide")
  else
    prompt="Write me a prompt for Claude Code to do this: $req"
  fi
  ( cd "$dir/project" && timeout 400 claude -p "$prompt" --model sonnet "${extra[@]}" \
      --allowedTools "Read,Grep,Glob,Write,Bash(git:*),Bash(basename:*),Bash(pwd),Bash(mkdir:*),Bash(date:*)" \
      --output-format json > "$dir/out.json" 2> "$dir/err.txt" )
  python3 -I - "$dir" <<'PY'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
try:
    res = json.loads((d / "out.json").read_text()).get("result", "")
except Exception:
    res = ""
saved = sorted((d / "guide" / "prompts").rglob("*.md")) if (d / "guide" / "prompts").exists() else []
leaked = sorted(str(p.relative_to(d / "project")) for p in (d / "project").rglob("*") if p.is_file() and p.name != "README.md")
(d / "draft.md").write_text(saved[0].read_text() if saved else res)
(d / "saved.txt").write_text(str(saved[0].relative_to(d / "guide")) if saved else "")
(d / "leaked.txt").write_text("\n".join(leaked))
PY
}

while IFS=$'\t' read -r id text; do
  for arm in $arms; do run_one "$arm" "$id" "$text" & done
done < <(python3 -I -c 'import json,sys; [print(s["id"]+"\t"+s["text"]) for s in json.load(open(sys.argv[1]))]' "$here/scenarios.json")
wait

printf '%-10s %-9s %-7s %-45s %s\n' scenario arm score "saved in guide" "written in project"
for d in "$work"/*-*/; do
  name="$(basename "$d")"; arm="${name%%-*}"; id="${name#*-}"
  score="$(python3 -I "$here/score.py" "$here/scenarios.json" "$id" "$d/draft.md" | tail -1 | cut -d' ' -f2)"
  printf '%-10s %-9s %-7s %-45s %s\n' "$id" "$arm" "$score" "$(cat "$d/saved.txt")" "$(tr '\n' ' ' < "$d/leaked.txt")"
done
