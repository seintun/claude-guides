async (page) => {
  // Screenshots every <figure> (and the hero) at desktop and phone width, light and dark,
  // into build/shots/<width><l|d>-<section>-<n>.png, for a visual pass after each change.
  // Set ROOT to the absolute path of your clone of this repository.
  const ROOT = '/path/to/claude-guides'; // set to your clone
  const PAGE = 'file://' + encodeURI(ROOT + '/build/preview.html');
  const views = [[1280, 900, 'light'], [1280, 900, 'dark'], [375, 812, 'light'], [375, 812, 'dark']];
  const saved = [];
  // The page starts dark and remembers the reader's choice: match the page theme to each view's colour scheme.
  await page.addInitScript(() => {
    try { localStorage.setItem('orchestrating-claude-theme', matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); } catch (e) {}
  });
  for (const [w, h, scheme] of views) {
    await page.setViewportSize({ width: w, height: h });
    await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' });
    await page.goto(PAGE, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts && document.fonts.ready);
    const tag = `${w}${scheme[0]}`;
    const hero = `${ROOT}/build/shots/${tag}-hero.png`;
    await page.locator('header.hero').screenshot({ path: hero });
    saved.push(hero.slice(ROOT.length + 1));
    const figs = page.locator('main section figure');
    const n = await figs.count();
    const counts = {};
    for (let i = 0; i < n; i++) {
      const f = figs.nth(i);
      const sec = await f.evaluate((el) => el.closest('section').id);
      counts[sec] = (counts[sec] || 0) + 1;
      const p = `${ROOT}/build/shots/${tag}-${sec}-${counts[sec]}.png`;
      await f.scrollIntoViewIfNeeded();
      await f.screenshot({ path: p });
      saved.push(p.slice(ROOT.length + 1));
    }
  }
  return saved.join('\n');
}
