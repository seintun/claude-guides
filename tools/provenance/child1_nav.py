"""Child 1: skip link, phone lesson menu, Next and Contents links at the end of each lesson, footer link."""
import re
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"expected {count} of {old[:70]!r}, found {n}")
    s = s.replace(old, new)


rep('<div class="shell">\n\n<header class="hero">',
    '<a class="skip" href="#main">Skip to the lessons</a>\n<div class="shell">\n\n<header class="hero" id="top">')
rep('<nav class="rail" aria-label="Lessons">',
    '<details class="lessons-menu" id="lessons-menu">\n'
    '  <summary><span class="lm-label">Lessons</span><span class="lm-cur" id="lm-cur">01 The loop</span></summary>\n'
    '</details>\n\n'
    '<nav class="rail" aria-label="Lessons">')
rep('<main>', '<main id="main" tabindex="-1">')

# Lesson names and order come from the rail.
rail = s[s.index('<nav class="rail"'):s.index('</nav>', s.index('<nav class="rail"'))]
items = re.findall(r'<a href="#([^"]+)">([^<]+)</a>', rail)
if len(items) != 18:
    raise SystemExit(f"expected 18 rail items, found {len(items)}")
for i, (sid, name) in enumerate(items):
    start = s.index(f'<section id="{sid}"')
    end = s.index('</section>', start)
    if i + 1 < len(items):
        nid, nname = items[i + 1]
        nxt = f'<a href="#{nid}">Next: {i + 2:02d} {nname} →</a>'
    else:
        nxt = ''
    block = f'  <p class="lesson-end">{nxt}<a href="#top" class="to-contents">↑ Contents</a></p>\n'
    s = s[:end] + block + s[end:]

rep('<footer>Features and research checked', '<footer><a href="#top" class="to-top">↑ Back to top</a><br>Features and research checked')

open(path, "w", encoding="utf-8").write(s)
print("ok", len(items), "lesson ends")
