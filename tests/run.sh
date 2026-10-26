#!/usr/bin/env bash
# Runs every offline check and test in one go. Exit 1 if anything fails.
# Usage: tests/run.sh        (from anywhere; takes a few seconds and needs no network)
#        tests/run.sh -v     also print each test's name and result
# The browser checks (checks/run-dom.js, checks/compendium-check.js) and the live tests in
# tests/live/ cost a browser or a model session, so they run separately; see tests/README.md.
set -uo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root" || exit 1
export TEST_TMP="$root/build/test-tmp"   # build/ is git-ignored; temp files stay inside the clone
mkdir -p "$TEST_TMP"
verbose="${1:-}"
failed=0
# A stray `exit 0` further down cannot hide a recorded failure; a crash keeps its own non-zero code.
trap 'code=$?; if [ "$code" -eq 0 ]; then exit "$failed"; fi' EXIT
now() { python3 -I -c 'import time; print(f"{time.time():.3f}")'; }
secs() { python3 -I -c "import sys; print(f'{float(sys.argv[2]) - float(sys.argv[1]):.1f}s')" "$1" "$2"; }
start_all="$(now)"

step() {
  local name="$1"; shift
  local out rc t0
  t0="$(now)"
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "PASS $name ($(secs "$t0" "$(now)"))"
  else
    echo "FAIL $name ($(secs "$t0" "$(now)"))"
    printf '%s\n' "$out" | grep -E "FAIL|ERROR|Error|Traceback|AssertionError|stale|broken" | head -25 | sed 's/^/    /'
    failed=1
  fi
  if [ "$verbose" = "-v" ]; then printf '%s\n' "$out" | sed 's/^/    | /'; fi
  return 0
}

step "page source: static checks, standalone copy current" checks/static.sh
step "links and anchors in every Markdown file" python3 -I tools/check_links.py
step "privacy: no personal paths, emails or private terms" python3 -I tools/check_privacy.py
step "ENTRY.md router: size, rows, section ids" python3 -I tools/check_entry.py
step "runner integrity: run.sh and the commit hook still run every check" python3 -I tests/test_harness.py RunnerIntegrityTests

t0="$(now)"
out="$(python3 -I -m unittest discover -s tests -p 'test_*.py' 2>&1)"; rc=$?
took="$(secs "$t0" "$(now)")"
summary="$(printf '%s\n' "$out" | grep -E '^(Ran |OK|FAILED)' | tr '\n' ' ')"
if [ "$rc" -eq 0 ]; then echo "PASS unit and guard tests ($took) — $summary"; else
  echo "FAIL unit and guard tests ($took) — $summary"
  printf '%s\n' "$out" | grep -E '^(FAIL|ERROR):|AssertionError' | head -25 | sed 's/^/    /'
  failed=1
fi
skipped="$(printf '%s\n' "$out" | grep -c 'skipped .NOT RUN' || true)"
if [ "$skipped" != "0" ]; then printf '%s\n' "$out" | grep 'skipped .NOT RUN' | sed 's/^/    NOT RUN /' | head -10; fi
if [ "$verbose" = "-v" ]; then printf '%s\n' "$out" | sed 's/^/    | /'; fi

total="$(secs "$start_all" "$(now)")"
if [ "$failed" -eq 0 ]; then echo "SUMMARY all PASS in $total"; else echo "SUMMARY FAIL in $total"; fi
exit "$failed"
