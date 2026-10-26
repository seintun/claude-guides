#!/usr/bin/env bash
# Static checks on the page source, then a wrapped copy for the DOM checks.
# Usage: checks/static.sh [page.html]   (run from the folder that holds checks/ and site/)
set -uo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
page="${1:-$here/site/orchestrating-claude.html}"
python3 -I "$here/checks/static_checks.py" "$page" "$here/checks/urls-v11.txt"
status=$?
# The artifact source has no doctype or body; the viewer adds them. Do the same for local DOM checks.
python3 -I "$here/tools/build_standalone.py" "$page" "$here/build/preview.html" > /dev/null || status=1
echo "INFO wrapped page for DOM checks: build/preview.html"
# site/index.html is the committed standalone copy; it must match a fresh build of the page.
if [ "$page" = "$here/site/orchestrating-claude.html" ]; then
  if cmp -s "$here/build/preview.html" "$here/site/index.html"; then
    echo "PASS static-6 Standalone copy site/index.html is current"
  else
    echo "FAIL static-6 Standalone copy site/index.html is stale: run python3 -I tools/build_standalone.py"
    status=1
  fi
fi
exit $status
