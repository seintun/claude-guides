"""Make evidence tags that have no outside source tooltip-only.

Tags pointing at "#sources" (every D tag, plus the legend) become a focusable
<span> that shows the tooltip but never navigates.
"""
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
pattern = re.compile(r'<a class="(ev [psrd])" href="#sources" (data-src="[^"]*") (aria-label="[^"]*")>([PSRD])</a>')
out, n = pattern.subn(r'<span class="\1" tabindex="0" role="note" \2 \3>\4</span>', src)
left = src.count('href="#sources"') - n
open(path, "w", encoding="utf-8").write(out)
print(f"converted {n} tags; other #sources links left: {left}")
