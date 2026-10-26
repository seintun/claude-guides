async (page) => {
  // Checks docs/orchestrating-claude-compendium.html: no network requests, no script errors, no
  // dangling links or duplicate ids, no sideways scroll at phone width, and search finds and marks text.
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
    await page.emulateMedia({ colorScheme: scheme });
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
