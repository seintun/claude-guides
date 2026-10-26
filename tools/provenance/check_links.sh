#!/usr/bin/env bash
# Checks every external link in the page and prints any that don't return 2xx.
# Usage: check_links.sh <page.html>
page="$1"
grep -oE 'href="https?://[^"]+"' "$page" | sed -E 's/^href="//; s/"$//' | sed 's/&amp;/\&/g' | grep -v "fonts\.g" | sort -u > "${TMPDIR:-/tmp}/page-urls.txt"
total=$(wc -l < "${TMPDIR:-/tmp}/page-urls.txt" | tr -d ' ')
echo "unique external links: $total"
check() {
  url="$1"
  code=$(curl -s -o /dev/null -L --max-time 20 -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36' -w '%{http_code}' "$url")
  echo "$code $url"
}
export -f check
xargs -P 4 -I{} bash -c 'check "$@"' _ {} < "${TMPDIR:-/tmp}/page-urls.txt" | sort > "${TMPDIR:-/tmp}/page-url-status.txt"
echo "--- not 2xx:"
grep -vE '^2[0-9][0-9] ' "${TMPDIR:-/tmp}/page-url-status.txt" || echo "(none)"
echo "--- 2xx count: $(grep -cE '^2[0-9][0-9] ' "${TMPDIR:-/tmp}/page-url-status.txt")"
