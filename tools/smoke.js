// Laadt holes en meldt consolefouten. Gebruik: node tools/smoke.js [0,1,2] [shots-map]
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'), fs = require('fs');
const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html'));
const THREE_DIR = process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 900, height: 560 } }); page.setDefaultTimeout(120000);
  const errs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_DIR + '/build/three.min.js', contentType: 'application/javascript' }));
  await page.route('**/GLTFLoader.js', r => r.fulfill({ path: THREE_DIR + '/examples/js/loaders/GLTFLoader.js', contentType: 'application/javascript' }));
  await page.goto(GAME); await page.waitForTimeout(2500);
  const n = await page.evaluate(() => window.__mg.HOLES.length);
  const list = process.argv[2] ? process.argv[2].split(',').map(Number) : [...Array(n).keys()];
  const shots = process.argv[3]; if (shots) fs.mkdirSync(shots, { recursive: true });
  await page.evaluate(() => window.__mg.startGame(1, 'single', 0));
  for (const i of list) {
    await page.evaluate(i => window.__mg.loadHole(i), i);
    await page.waitForTimeout(shots ? 1200 : 1500);
    if (shots) {
      await page.screenshot({ path: `${shots}/h${i + 1}_overview.png` }); // overzicht tijdens de intro
      await page.waitForTimeout(5500); await page.screenshot({ path: `${shots}/h${i + 1}_start.png` }); // camera achter de bal
    }
  }
  console.log(`holes: ${n}`); console.log(errs.slice(0, 20).join('\n') || 'NO ERRORS');
  await browser.close();
})();
