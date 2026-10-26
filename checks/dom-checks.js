/* In-page checks for the Orchestrating Claude page.
   Load this file into the page, then call window.__uxChecks({width}).
   Returns [{id, name, status, detail}], status is PASS, FAIL or INFO. */
(function () {
  var MAX_SAMPLES = 6;

  /* ---------- colour helpers ---------- */
  var ctx = document.createElement('canvas').getContext('2d');
  function parseColor(str) {
    if (!str || str === 'none' || str === 'transparent') return [0, 0, 0, 0];
    var m = str.match(/^rgba?\(([^)]+)\)$/);
    if (!m) {
      var c = str.match(/^color\(srgb ([\d.]+) ([\d.]+) ([\d.]+)(?: \/ ([\d.]+))?\)$/);
      if (c) return [c[1] * 255, c[2] * 255, c[3] * 255, c[4] === undefined ? 1 : +c[4]];
      ctx.fillStyle = '#000'; ctx.fillStyle = str;
      var hex = ctx.fillStyle;
      if (hex[0] === '#') return [parseInt(hex.substr(1, 2), 16), parseInt(hex.substr(3, 2), 16), parseInt(hex.substr(5, 2), 16), 1];
      return parseColor(hex);
    }
    var p = m[1].split(/[\s,/]+/).filter(Boolean).map(parseFloat);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  }
  function blend(top, bottom) {
    var a = top[3];
    return [top[0] * a + bottom[0] * (1 - a), top[1] * a + bottom[1] * (1 - a), top[2] * a + bottom[2] * (1 - a), 1];
  }
  function lum(c) {
    var v = [c[0], c[1], c[2]].map(function (x) { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  }
  function ratio(a, b) {
    var l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function htmlBg(el) {
    var layers = [];
    for (var e = el; e && e.nodeType === 1; e = e.parentElement) {
      var c = parseColor(getComputedStyle(e).backgroundColor);
      if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    var base = [255, 255, 255, 1];
    for (var i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return base;
  }
  var SHAPES = { rect: 1, circle: 1, ellipse: 1, path: 1, polygon: 1 };
  function svgBg(textEl) {
    textEl.scrollIntoView({ block: 'center', inline: 'center' });
    var r = textEl.getBoundingClientRect();
    var stack = document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    var layers = [], base = null;
    for (var i = 0; i < stack.length; i++) {
      var e = stack[i];
      if (e === textEl || textEl.contains(e) || e.tagName === 'text' || e.tagName === 'tspan') continue;
      if (e instanceof SVGElement && SHAPES[e.tagName]) {
        var cs = getComputedStyle(e);
        var f = parseColor(cs.fill);
        var op = parseFloat(cs.fillOpacity) * parseFloat(cs.opacity);
        if (f[3] > 0 && op > 0) { f[3] *= op; layers.push(f); if (f[3] >= 1) break; }
        continue;
      }
      if (e instanceof SVGElement) continue;
      base = htmlBg(e); break;
    }
    if (!base) base = htmlBg(textEl.ownerSVGElement || document.body);
    if (layers.length && layers[layers.length - 1][3] >= 1) base = [0, 0, 0, 1];
    for (var j = layers.length - 1; j >= 0; j--) base = blend(layers[j], base);
    return base;
  }
  function fmt(c) { return 'rgb(' + c.slice(0, 3).map(Math.round).join(',') + ')'; }

  /* ---------- misc helpers ---------- */
  function visible(el) {
    if (!el.getClientRects().length) return false;
    var cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none';
  }
  function where(el) {
    var s = el.closest('section[id]');
    return s ? '#' + s.id : (el.closest('header, .hero') ? 'hero' : el.closest('nav') ? 'nav' : 'page');
  }
  function snip(t) { t = (t || '').replace(/\s+/g, ' ').trim(); return t.length > 40 ? t.slice(0, 40) + '…' : t; }
  function result(id, name, fails, extra) {
    var detail = fails.length ? fails.length + ' fail: ' + fails.slice(0, MAX_SAMPLES).join(' | ') : (extra || '');
    return { id: id, name: name, status: fails.length ? 'FAIL' : 'PASS', detail: detail };
  }
  function directText(el) {
    var t = '';
    for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3) t += n.nodeValue;
    return t.trim();
  }

  /* ---------- checks ---------- */
  function c1Overflow(o) {
    var fails = [];
    var sw = document.documentElement.scrollWidth;
    if (sw > window.innerWidth) fails.push('page scrollWidth ' + sw + ' > ' + window.innerWidth);
    return result('dom-1', 'No page-level horizontal overflow', fails);
  }
  function c2Title() {
    var h1 = document.querySelector('h1'), fails = [];
    if (!h1) fails.push('no h1');
    else {
      var r = h1.getBoundingClientRect();
      if (h1.scrollWidth > h1.clientWidth + 1) fails.push('h1 scrollWidth ' + h1.scrollWidth + ' > clientWidth ' + h1.clientWidth);
      if (r.right > window.innerWidth + 1) fails.push('h1 right edge ' + Math.round(r.right) + ' > viewport ' + window.innerWidth);
      var thesis = document.querySelector('.thesis');
      if (thesis && visible(thesis)) {
        var t = thesis.getBoundingClientRect();
        var overlap = r.right > t.left && r.left < t.right && r.bottom > t.top && r.top < t.bottom;
        var spans = [].slice.call(h1.getClientRects());
        if (overlap && spans.some(function (s) { return s.right > t.left && s.left < t.right && s.bottom > t.top && s.top < t.bottom; })) fails.push('h1 overlaps .thesis');
      }
    }
    return result('dom-2', 'Title fits its column', fails);
  }
  function c3SvgText() {
    var fails = [], minBy = {};
    document.querySelectorAll('svg text').forEach(function (t) {
      if (!visible(t) || !t.textContent.trim()) return;
      var svg = t.ownerSVGElement; if (!svg || !visible(svg)) return;
      var ctm = t.getScreenCTM(); if (!ctm) return;
      var scale = Math.sqrt(ctm.a * ctm.a + ctm.b * ctm.b);
      var px = parseFloat(getComputedStyle(t).fontSize) * scale;
      var min = t.classList.contains('tick') ? 11 : 12;
      var key = where(t);
      if (!(key in minBy) || px < minBy[key]) minBy[key] = px;
      if (px < min - 0.05) fails.push(key + ' "' + snip(t.textContent) + '" ' + px.toFixed(1) + 'px');
    });
    var summary = Object.keys(minBy).map(function (k) { return k + ' ' + minBy[k].toFixed(1); }).join(', ');
    var r = result('dom-3', 'SVG text renders at 12px or more (ticks 11px)', fails, 'min px: ' + summary);
    if (fails.length) r.detail += ' || min px: ' + summary;
    return r;
  }
  function c4Scrollers() {
    var fails = [], ok = [];
    document.querySelectorAll('.tbl-wrap, .scroll').forEach(function (el) {
      if (!visible(el)) return;
      if (el.scrollWidth > el.clientWidth + 1) {
        var label = where(el) + ' ' + (el.className || el.tagName) + ' ' + el.scrollWidth + '>' + el.clientWidth;
        if (el.hasAttribute('data-scroll-ok')) {
          var cued = el.querySelector('.scroll-cue') || (el.parentElement && el.parentElement.querySelector('.scroll-cue'));
          var focusable = el.getAttribute('tabindex') === '0' && el.getAttribute('role') === 'region' && el.getAttribute('aria-label');
          if (cued && focusable) ok.push(label); else fails.push(label + ' (scroll-ok without cue, tabindex, role or label)');
        } else fails.push(label);
      }
    });
    return result('dom-4', 'No inner horizontal scroll (except cued scrollers)', fails, ok.length ? 'cued scrollers: ' + ok.join(', ') : '');
  }
  function c5Contrast() {
    var fails = [], n = 0;
    var els = document.querySelectorAll('body *');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.closest('svg') || el.closest('script, style, noscript, title, .ev-tip')) continue;
      var txt = directText(el); if (!txt) continue;
      if (!visible(el) || el.matches(':disabled')) continue;
      var cs = getComputedStyle(el);
      if (parseFloat(cs.opacity) === 0) continue;
      var bg = htmlBg(el), fg = parseColor(cs.color);
      if (fg[3] < 1) fg = blend(fg, bg);
      var size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
      var need = (size >= 24 || (bold && size >= 18.66)) ? 3 : 4.5;
      var r = ratio(fg, bg); n++;
      if (r < need - 0.005) fails.push(where(el) + ' <' + el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + '> "' + snip(txt) + '" ' + r.toFixed(2) + ':1 (' + size + 'px) ' + fmt(fg) + ' on ' + fmt(bg));
    }
    var svgTexts = document.querySelectorAll('svg text');
    for (var k = 0; k < svgTexts.length; k++) {
      var t = svgTexts[k];
      if (!t.textContent.trim() || !visible(t) || !visible(t.ownerSVGElement)) continue;
      var tcs = getComputedStyle(t);
      var tf = parseColor(tcs.fill); if (tf[3] === 0) continue;
      tf[3] *= parseFloat(tcs.fillOpacity);
      var tbg = svgBg(t); if (tf[3] < 1) tf = blend(tf, tbg);
      var ctm = t.getScreenCTM(), sc = ctm ? Math.sqrt(ctm.a * ctm.a + ctm.b * ctm.b) : 1;
      var tsize = parseFloat(tcs.fontSize) * sc, tbold = parseInt(tcs.fontWeight, 10) >= 700;
      var tneed = (tsize >= 24 || (tbold && tsize >= 18.66)) ? 3 : 4.5;
      var tr = ratio(tf, tbg); n++;
      if (tr < tneed - 0.005) fails.push(where(t) + ' svg "' + snip(t.textContent) + '" ' + tr.toFixed(2) + ':1 ' + fmt(tf) + ' on ' + fmt(tbg));
    }
    window.scrollTo(0, 0);
    return result('dom-5a', 'Text contrast meets WCAG AA', fails, n + ' text elements checked');
  }
  function c5NonText() {
    var fails = [];
    document.querySelectorAll('input:not([type=checkbox]):not([type=radio]), select, textarea').forEach(function (f) {
      if (!visible(f)) return;
      var cs = getComputedStyle(f);
      var r = ratio(parseColor(cs.borderTopColor), htmlBg(f.parentElement));
      if (r < 3) fails.push(where(f) + ' field border ' + r.toFixed(2) + ':1');
    });
    document.querySelectorAll('svg .d-edge, svg .d-arrow').forEach(function (e) {
      if (!visible(e)) return;
      var cs = getComputedStyle(e);
      var c = parseColor(e.classList.contains('d-arrow') ? cs.fill : cs.stroke); if (c[3] === 0) return;
      var r = ratio(c, htmlBg(e.ownerSVGElement));
      if (r < 3) fails.push(where(e) + ' ' + e.getAttribute('class') + ' ' + r.toFixed(2) + ':1');
    });
    return result('dom-5b', 'Field borders and diagram edges reach 3:1', fails);
  }
  function c6Links() {
    var fails = [];
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var h = a.getAttribute('href'); if (h.length < 2) return;
      if (!document.getElementById(decodeURIComponent(h.slice(1)))) fails.push('dangling ' + h);
    });
    var main = document.querySelector('main');
    if (main) {
      var w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT), node;
      while ((node = w.nextNode())) {
        var m = node.nodeValue.match(/Lesson \d+/g); if (!m) continue;
        var p = node.parentElement;
        if (p.closest('a, .kicker, script, style')) continue;
        fails.push(where(p) + ' plain "' + m[0] + '"');
      }
    }
    var internal = main ? main.querySelectorAll('a[href^="#"]').length : 0;
    return result('dom-6', 'Internal links resolve; lesson references are links', fails, internal + ' internal links in <main>');
  }
  function c7Structure() {
    var fails = [];
    document.querySelectorAll('svg').forEach(function (s) {
      if (s.parentElement && s.parentElement.closest('svg')) return;
      if (s.getAttribute('aria-hidden') === 'true') return;
      if (!s.getAttribute('role') || !(s.getAttribute('aria-label') || s.getAttribute('aria-labelledby'))) fails.push(where(s) + ' svg missing role or label');
    });
    var hs = [].slice.call(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    var prev = 0;
    hs.forEach(function (h) {
      var lv = +h.tagName[1];
      if (prev && lv > prev + 1) fails.push(where(h) + ' h' + prev + '→h' + lv + ' "' + snip(h.textContent) + '"');
      prev = lv;
    });
    var CARD = 'li, .panel, .card, .layer';
    hs.forEach(function (h, i) {
      if (h.tagName !== 'H3') return;
      var box = h.closest(CARD); if (!box || !box.closest('main')) return;
      for (var j = i - 1; j >= 0; j--) {
        var o = hs[j];
        if (box.contains(o) || o.closest(CARD)) continue;
        if (o.tagName === 'H3') fails.push(where(h) + ' card h3 "' + snip(h.textContent) + '" under h3 "' + snip(o.textContent) + '"');
        break;
      }
    });
    return result('dom-7', 'SVG labels, heading order, no card h3 under an h3', fails);
  }
  function c8Tags() {
    var fails = [], a = document.querySelectorAll('a.ev'), s = document.querySelectorAll('span.ev');
    a.forEach(function (t) {
      if (t.getAttribute('target') !== '_blank' || !/noopener/.test(t.getAttribute('rel') || '') || !t.getAttribute('data-src')) fails.push(where(t) + ' a.ev ' + t.getAttribute('href'));
    });
    s.forEach(function (t) {
      if (t.getAttribute('aria-hidden') === 'true') return;
      if (t.getAttribute('tabindex') !== '0') fails.push(where(t) + ' span.ev without tabindex 0');
    });
    return result('dom-8', 'Evidence tags: links open new tab, spans focusable', fails, a.length + ' links, ' + s.length + ' spans');
  }
  function c9Glossary() {
    var g = document.getElementById('glossary');
    if (!g) return { id: 'dom-9', name: 'Terms defined before first use', status: 'FAIL', detail: 'no #glossary' };
    var fails = [], terms = [].slice.call(g.querySelectorAll('[data-term]'));
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), node, texts = [];
    while ((node = w.nextNode())) {
      var p = node.parentElement;
      if (!p || p.closest('script, style, title, nav, header, .skip, .lesson-end, .lessons-menu, .ev-tip, [aria-hidden=true]')) continue;
      texts.push(node);
    }
    // Navigation and the hero are skipped. After the strip, a term's first use must sit in the
    // same block as its defining link (#fu-<term>).
    terms.forEach(function (t) {
      var re = new RegExp('(' + t.getAttribute('data-term') + ')', 'i');
      var label = t.querySelector('dt').textContent;
      for (var i = 0; i < texts.length; i++) {
        if (g.contains(texts[i]) || !re.test(texts[i].nodeValue)) continue;
        if (!(g.compareDocumentPosition(texts[i]) & Node.DOCUMENT_POSITION_FOLLOWING)) { fails.push('"' + label + '" used before the glossary: "' + snip(texts[i].nodeValue) + '"'); return; }
        var def = document.getElementById(t.getAttribute('data-first'));
        var block = texts[i].parentElement.closest('li, p, td, figcaption, dd');
        if (!def || !block || !block.contains(def)) fails.push('"' + label + '" first used without its definition: ' + where(texts[i].parentElement) + ' "' + snip(texts[i].nodeValue) + '"');
        return;
      }
      fails.push('"' + label + '" never used');
    });
    return result('dom-9', 'Terms defined before first use', fails, terms.length + ' terms');
  }
  var WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6 };
  function c10Benchmarks() {
    var sec = document.getElementById('evidence'), fails = [];
    var fig = sec && [].slice.call(sec.querySelectorAll('figure')).filter(function (f) { return /benchmark/i.test(f.textContent); })[0];
    if (!fig) return { id: 'dom-10', name: 'Evidence chart shows every benchmark its caption names', status: 'FAIL', detail: 'no benchmark figure in #evidence' };
    var cap = (fig.querySelector('figcaption') || fig).textContent;
    var m = cap.match(/(\d+|one|two|three|four|five|six) of the (\d+|one|two|three|four|five|six) benchmarks/i);
    var named = m ? m[1] : (cap.match(/(\d+|one|two|three|four|five|six) benchmarks/i) || [])[1];
    var expected = named ? (WORDS[named.toLowerCase()] || +named) : NaN;
    var set = {};
    var tagged = fig.querySelectorAll('[data-benchmark]');
    if (tagged.length) tagged.forEach(function (e) { set[e.getAttribute('data-benchmark')] = 1; });
    else fig.querySelectorAll('svg text').forEach(function (t) { var x = t.textContent.split(' · '); if (x.length > 1) set[x[0].trim()] = 1; });
    var drawn = Object.keys(set).length;
    if (drawn !== expected) fails.push('caption names ' + expected + ', chart draws ' + drawn + ' (' + Object.keys(set).join('; ') + ')');
    return result('dom-10', 'Evidence chart shows every benchmark its caption names', fails, drawn + ' benchmarks drawn');
  }

  function c11Wayfinding() {
    var fails = [];
    var secs = [].slice.call(document.querySelectorAll('main section[id]'));
    secs.forEach(function (sec, i) {
      var end = sec.querySelector('.lesson-end');
      if (!end) { fails.push('#' + sec.id + ' has no .lesson-end'); return; }
      var next = secs[i + 1];
      if (next && !end.querySelector('a[href="#' + next.id + '"]')) fails.push('#' + sec.id + ' has no Next link to #' + next.id);
      if (!end.querySelector('a.to-contents')) fails.push('#' + sec.id + ' has no Contents link');
    });
    var skip = document.querySelector('a.skip[href="#main"]');
    if (!skip || document.querySelector('a, button, input, select, textarea, summary, [tabindex="0"]') !== skip) fails.push('skip link missing or not first');
    var menu = document.getElementById('lessons-menu');
    if (window.innerWidth <= 980) {
      if (!menu || !visible(menu)) fails.push('no visible lessons menu at ' + window.innerWidth);
      else if (getComputedStyle(menu).position !== 'sticky') fails.push('lessons menu is not sticky');
      else if (menu.querySelectorAll('a').length !== document.querySelectorAll('.rail a').length) fails.push('menu and rail list differ');
    }
    var cur = document.querySelectorAll('.rail a[aria-current="location"]').length;
    if (cur !== 1) fails.push(cur + ' rail links marked current');
    return result('dom-11', 'Wayfinding: skip link, phone menu, Next and Contents on every lesson', fails, secs.length + ' sections');
  }

  function c12Paths() {
    var fails = [];
    var paths = document.querySelectorAll('#paths .path');
    if (paths.length !== 3) fails.push(paths.length + ' reading paths');
    paths.forEach(function (p) {
      var links = p.querySelectorAll('ol a');
      if (!links.length) fails.push('path without lessons');
      links.forEach(function (a) { if (!document.querySelector(a.getAttribute('href'))) fails.push('path link ' + a.getAttribute('href') + ' dangles'); });
      var m = p.querySelector('.path-min');
      if (!m || !/about [1-9]\d* min/.test(m.textContent)) fails.push('path without minutes: ' + (m ? m.textContent : 'none'));
    });
    document.querySelectorAll('main section[id]').forEach(function (sec) {
      if (sec.id === 'sources') return;
      var lv = sec.querySelector('.kicker .lv');
      if (!lv || !/^(Core|Builder|Reference) · \d+ min$/.test(lv.textContent)) fails.push('#' + sec.id + ' kicker lacks level and minutes');
    });
    if (window.innerWidth > 980 && document.querySelectorAll('.rail .rail-group').length !== 4) fails.push('rail does not show 4 groups');
    var rules = document.getElementById('rules-list');
    var shown = rules ? [].filter.call(rules.children, visible).length : 0;
    var btn = document.querySelector('#rules .more-btn[aria-expanded="false"]');
    if (shown !== 3 || !btn) fails.push('Lesson 2 shows ' + shown + ' rules, toggle ' + (btn ? 'present' : 'missing'));
    var yours = document.querySelector('details.yours');
    if (!yours || yours.open) fails.push('author setup block not a closed <details>');
    return result('dom-12', 'Reading paths, levels and minutes, grouped rail, collapsed extras', fails);
  }

  window.__uxChecks = function (o) {
    o = o || {};
    var out = [];
    [c1Overflow, c2Title, c3SvgText, c4Scrollers, c5Contrast, c5NonText, c6Links, c7Structure, c8Tags, c9Glossary, c10Benchmarks, c11Wayfinding, c12Paths].forEach(function (fn) {
      try { out.push(fn(o)); } catch (e) { out.push({ id: fn.name, name: fn.name, status: 'FAIL', detail: 'check threw: ' + e.message }); }
    });
    return out;
  };
})();
