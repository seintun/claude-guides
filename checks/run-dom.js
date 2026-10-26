async (page) => {
  // Runs dom-checks.js against build/preview.html at phone and desktop widths, light and dark,
  // plus the phase-explorer keyboard scenarios. Run with Playwright's run_code (filename = this file).
  // Set ROOT to the absolute path of your clone of this repository.
  const ROOT = '/path/to/claude-guides'; // set to your clone
  const PAGE = 'file://' + encodeURI(ROOT + '/build/preview.html');
  const CHECKS = ROOT + '/checks/dom-checks.js';
  const combos = [
    [320, 700, 'light'], [375, 812, 'light'], [375, 812, 'dark'], [414, 896, 'light'],
    [768, 1024, 'light'], [1024, 768, 'dark'], [1280, 900, 'light'], [1280, 900, 'dark'],
  ];
  const out = [];
  let pass = 0, fail = 0;
  const pageErrors = new Set();
  page.on('pageerror', (e) => pageErrors.add(e.message));
  const line = (status, id, name, detail) => {
    if (status === 'PASS') pass++; else if (status === 'FAIL') fail++;
    out.push(`${status} ${id} ${name}${detail ? ' — ' + detail : ''}`);
  };
  const load = async (w, h, scheme) => {
    await page.setViewportSize({ width: w, height: h });
    await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' });
    await page.goto(PAGE, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts && document.fonts.ready);
  };

  // One line per check: the views it fails in, and the detail from the first failing view.
  const byId = new Map();
  for (const [w, h, scheme] of combos) {
    await load(w, h, scheme);
    await page.addScriptTag({ path: CHECKS });
    const res = await page.evaluate((o) => window.__uxChecks(o), { width: w });
    const view = `${w}${scheme[0]}`;
    for (const r of res) {
      if (!byId.has(r.id)) byId.set(r.id, { name: r.name, failed: [], detail: '', info: r.detail });
      const e = byId.get(r.id);
      if (r.status === 'FAIL') { e.failed.push(view); if (!e.detail) e.detail = `[${view}] ${r.detail}`; }
    }
  }
  for (const [id, e] of byId) {
    if (e.failed.length) line('FAIL', id, `${e.name} (fails in ${e.failed.join(', ')})`, e.detail);
    else line('PASS', id, e.name, e.info);
  }

  // Phase explorer keyboard scenarios (desktop, light).
  out.push('== phase explorer keyboard (1280x900)');
  await load(1280, 900, 'light');
  const nodes = page.locator('#phase-svg .node');
  if (await nodes.count() === 10) {
    await nodes.nth(6).focus();
    await page.keyboard.press('ArrowRight');
    const focusedI = await page.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-i'));
    line(focusedI === '7' ? 'PASS' : 'FAIL', 'kbd-1', 'Arrow key moves from the focused phase', `focus on node 7, ArrowRight → focused data-i=${focusedI}`);
    const tabStops = await page.evaluate(() => [...document.querySelectorAll('#phase-svg .node')].filter((n) => n.tabIndex >= 0).length);
    line(tabStops === 1 ? 'PASS' : 'FAIL', 'kbd-2', 'Phase explorer is one tab stop', `${tabStops} nodes are tab stops`);
    await nodes.nth(0).click();
    const next = page.locator('#pd-next');
    await next.focus();
    for (let i = 0; i < 12; i++) await page.keyboard.press('Enter');
    const lost = await page.evaluate(() => !document.activeElement || document.activeElement === document.body);
    line(lost ? 'FAIL' : 'PASS', 'kbd-3', 'Focus survives reaching phase 10', lost ? 'focus fell to <body>' : 'focus kept');
  } else {
    out.push('INFO kbd phase explorer replaced or missing at this width; skipped');
  }

  // Phone menu scenario: from deep in the page, open the menu and jump to lesson 17.
  out.push('== phone menu (375x812)');
  await load(375, 812, 'light');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.6));
  await page.waitForTimeout(150);
  const menuTop = await page.evaluate(() => { const m = document.getElementById('lessons-menu'); return m ? m.getBoundingClientRect().top : null; });
  line(menuTop !== null && menuTop >= 0 && menuTop < 2 ? 'PASS' : 'FAIL', 'nav-1', 'Lessons menu stays at the top while scrolling', `menu top ${menuTop}`);
  if (menuTop !== null) {
    await page.locator('#lessons-menu summary').click();
    await page.locator('#lessons-menu a[href="#evidence"]').click();
    await page.waitForTimeout(900);
    const r = await page.evaluate(() => {
      const h = document.querySelector('#evidence h2').getBoundingClientRect();
      const m = document.getElementById('lessons-menu').getBoundingClientRect();
      return { h2top: Math.round(h.top), h2bottom: Math.round(h.bottom), menuBottom: Math.round(m.bottom), open: document.getElementById('lessons-menu').open, cur: document.getElementById('lm-cur').textContent };
    });
    const ok = r.h2top >= r.menuBottom && r.h2bottom <= 812 && !r.open && /17/.test(r.cur);
    line(ok ? 'PASS' : 'FAIL', 'nav-2', 'Choosing 17 Evidence shows its h2 below the menu', JSON.stringify(r));
  }

  // Quiz by keyboard: arrow keys move the choice without scoring; Check answer scores it.
  out.push('== quiz keyboard (1280x900)');
  await load(1280, 900, 'light');
  await page.locator('#quiz-q1-0').focus();
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('ArrowDown');
  const mid = await page.evaluate(() => ({ picked: (document.querySelector('input[name="quiz-q1"]:checked') || {}).id, locked: document.getElementById('quiz-q1-0').disabled }));
  await page.locator('#quiz fieldset').nth(1).locator('.q-check').focus();
  await page.keyboard.press('Enter');
  const end = await page.evaluate(() => ({ locked: document.getElementById('quiz-q1-0').disabled, correct: !!document.querySelector('#quiz fieldset:nth-child(2) label.is-correct'), wrong: !!document.querySelector('#quiz fieldset:nth-child(2) label.is-wrong') }));
  const qok = mid.picked === 'quiz-q1-2' && !mid.locked && end.locked && end.correct && !end.wrong;
  line(qok ? 'PASS' : 'FAIL', 'quiz-1', 'Quiz: arrows choose without scoring, Check answer scores', JSON.stringify({ mid, end }));

  const dupes = await page.evaluate(() => { const seen = {}, d = []; document.querySelectorAll('[id]').forEach((e) => { if (seen[e.id]) d.push(e.id); seen[e.id] = 1; }); return d; });
  line(dupes.length ? 'FAIL' : 'PASS', 'page-1', 'Every id is unique', dupes.join(', '));
  line(pageErrors.size ? 'FAIL' : 'PASS', 'page-2', 'No script errors in any view', [...pageErrors].join(' | '));

  out.unshift(`SUMMARY ${pass} PASS, ${fail} FAIL`);
  return out.join('\n');
}
