async (page) => {
  // Checks docs/orchestrating-claude-compendium.html: no network requests, no script errors, no
  // dangling links or duplicate ids, no sideways scroll at phone width, search finds and marks text, and the
  // long page is built right: six parts, every lesson, runbook and mapped playbook section once and in order,
  // and every contents link lands its heading below the sticky bar.
  // Run with Playwright's run_code (filename = this file).
  // Set ROOT to the absolute path of your clone of this repository.
  const ROOT = '/path/to/claude-guides'; // set to your clone
  const URL = 'file://' + encodeURI(ROOT + '/docs/orchestrating-claude-compendium.html');
  const errors = new Set(), requests = new Set();
  page.on('pageerror', (e) => errors.add(e.message));
  page.on('request', (r) => { const u = r.url(); if (!/^(file|data|about|blob):/.test(u)) requests.add(u); });
  const out = [];
  let fails = 0;
  const line = (ok, id, name, detail) => { if (!ok) fails++; out.push(`${ok ? 'PASS' : 'FAIL'} ${id} ${name}${detail ? ' — ' + detail : ''}`); };

  for (const [w, h, scheme] of [[1280, 900, 'light'], [1280, 900, 'dark'], [375, 812, 'dark'], [320, 700, 'light']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' });
    await page.goto(URL, { waitUntil: 'load' });
    await page.waitForTimeout(300);
    const r = await page.evaluate(() => {
      const ids = [...document.querySelectorAll('[id]')].map((e) => e.id), set = new Set(ids);
      return {
        overflow: document.documentElement.scrollWidth > innerWidth,
        dangling: [...new Set([...document.querySelectorAll('a[href^="#"]')].map((a) => a.getAttribute('href').slice(1)).filter((x) => x && !set.has(x)))],
        dupes: [...new Set(ids.filter((v, i) => ids.indexOf(v) !== i))],
        blocks: document.getElementById('stat-blocks').textContent,
      };
    });
    line(!r.overflow, `c-1 ${w}${scheme[0]}`, 'No sideways scroll');
    if ((w === 1280 && scheme === 'light') || (w === 375 && scheme === 'dark')) {
      // Structure: the map the builder embedded says what is where; the DOM must agree, once each, in order.
      const st = await page.evaluate(() => {
        const map = JSON.parse(document.getElementById('compendium-map').textContent);
        const q = (s) => [...document.querySelectorAll(s)];
        const fails = [];
        const parts = q('main section.sec.part');
        if (parts.length !== 6 || parts.map((p) => p.id).join() !== map.parts.map((p) => p.id).join()) fails.push('parts in the DOM differ from the map');
        const lessonOrder = [], pbOrder = [], wikiOrder = [];
        map.parts.forEach((mp) => {
          const part = document.getElementById(mp.id);
          mp.lessons.forEach((ml) => {
            const found = q(`[data-lesson="${ml.id}"]`);
            if (found.length !== 1) { fails.push(`lesson ${ml.id} appears ${found.length} times`); return; }
            if (!part || !part.contains(found[0])) fails.push(`lesson ${ml.id} is not inside ${mp.id}`);
            lessonOrder.push(ml.id);
            ml.wiki.forEach((w) => { const r = q(`[data-wiki="${w}"]`); if (r.length !== 1 || !found[0].contains(r[0])) fails.push(`runbook ${w} is not once inside lesson ${ml.id}`); wikiOrder.push(w); });
            ml.pb.forEach((k) => { const r = q(`[data-pb="${k}"]`); if (r.length !== 1 || !found[0].contains(r[0])) fails.push(`playbook ${k} is not once inside lesson ${ml.id}`); pbOrder.push(k); });
            ml.pb_refs.forEach((k) => { if (!found[0].querySelector(`[data-pb-ref="${k}"]`)) fails.push(`lesson ${ml.id} lacks its pointer to playbook ${k}`); });
          });
        });
        map.extra_pb.forEach((k) => { if (q(`[data-pb="${k}"]`).length !== 1) fails.push(`playbook ${k} is not shown once in More playbook sections`); pbOrder.push(k); });
        const domLessons = q('[data-lesson]').map((e) => e.getAttribute('data-lesson'));
        if (domLessons.join() !== lessonOrder.join() || domLessons.length !== 18) fails.push(`lessons in the DOM: ${domLessons.length}, not the map's 18 in order`);
        const domPb = q('[data-pb]').map((e) => e.getAttribute('data-pb'));
        if (domPb.join() !== pbOrder.join()) fails.push('playbook sections are not in part order');
        const domWiki = q('[data-wiki]').map((e) => e.getAttribute('data-wiki'));
        if (domWiki.join() !== wikiOrder.join() || domWiki.length !== 11) fails.push(`runbooks in the DOM: ${domWiki.length}, not the map's 11 in order`);
        const asof = document.querySelector('.hero .asof');
        if (!asof || asof.textContent.trim() !== map.asof) fails.push('the as-of line is missing or differs from the page');
        if (!document.querySelector('#whatsnew li')) fails.push("no what's-new block");
        if (document.querySelector('iframe')) fails.push('the page is still embedded in an iframe');
        return { fails, lessons: domLessons.length, pb: domPb.length, wiki: domWiki.length };
      });
      line(!st.fails.length, `c-7 ${w}${scheme[0]}`, 'Parts, lessons, runbooks and playbook sections each appear once, in part order', st.fails.slice(0, 5).join(' | ') || `${st.lessons} lessons, ${st.wiki} runbooks, ${st.pb} playbook sections`);

      // Contents: every TOC and what's-new link lands its heading below the sticky bar, with the hash set.
      const hrefs = await page.evaluate(() => [...new Set([...document.querySelectorAll('.toc a, #whatsnew a')].map((a) => a.getAttribute('href')))]);
      const bad = [];
      for (const href of hrefs) {
        await page.locator(`.toc a[href="${href}"], #whatsnew a[href="${href}"]`).first().click();
        await page.waitForTimeout(80);
        const r = await page.evaluate((href) => {
          const t = document.getElementById(href.slice(1));
          const heading = t && (t.querySelector('h2, h3') || t);
          if (!heading) return { missing: true };
          const hr = heading.getBoundingClientRect(), bar = document.querySelector('.topbar').getBoundingClientRect();
          return { top: Math.round(hr.top), bottom: Math.round(hr.bottom), bar: Math.round(bar.bottom), vh: innerHeight, hash: location.hash };
        }, href);
        if (r.missing || r.top < r.bar - 1 || r.bottom > r.vh || r.hash !== href) bad.push(`${href} ${JSON.stringify(r)}`);
      }
      line(!bad.length, `c-8 ${w}${scheme[0]}`, "Every contents and what's-new link lands its heading below the sticky bar, with the hash set", bad.slice(0, 3).join(' | ') || `${hrefs.length} links clicked`);
    }
    if (w === 1280 && scheme === 'light') {
      line(!r.dangling.length, 'c-2', 'Every #link has a target', r.dangling.slice(0, 8).join(', '));
      line(!r.dupes.length, 'c-3', 'Every id is unique', r.dupes.slice(0, 8).join(', '));
      out.push(`INFO searchable blocks: ${r.blocks}`);
      for (const q of ['lethal trifecta', 'receipt NOT RUN', 'Template L']) {
        await page.locator('#q').fill(q);
        await page.waitForTimeout(120);
        const n = await page.locator('#results li button').count();
        await page.keyboard.press('Enter');
        await page.waitForTimeout(400);
        const marks = await page.evaluate(() => document.querySelectorAll('main mark').length);
        line(n > 0 && marks > 0, 'c-4', `Search "${q}" finds and marks`, `${n} results, ${marks} marks`);
        await page.locator('#q').fill('');
      }
    }
  }
  line(!errors.size, 'c-5', 'No script errors', [...errors].join(' | '));
  line(!requests.size, 'c-6', 'No network requests (works offline)', [...requests].slice(0, 5).join(', '));
  out.unshift(`SUMMARY ${fails ? fails + ' FAIL' : 'all PASS'}`);
  return out.join('\n');
}
