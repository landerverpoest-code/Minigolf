// Sfeerbeelden zonder UI: per hole een paar camerastandpunten (om de decoratie te beoordelen).
// Gebruik: node tools/beauty.js 0,3 <map>
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'), fs = require('fs');
const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html'));
const THREE_DIR = process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1000, height: 600 } }); page.setDefaultTimeout(180000);
  const errs = []; page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_DIR + '/build/three.min.js', contentType: 'application/javascript' }));
  await page.route('**/GLTFLoader.js', r => r.fulfill({ path: THREE_DIR + '/examples/js/loaders/GLTFLoader.js', contentType: 'application/javascript' }));
  await page.goto(GAME); await page.waitForTimeout(1500);
  await page.addStyleTag({ content: '.screen,#hud,#banner,#toast{display:none!important}' });
  const list = (process.argv[2] || '0').split(',').map(Number), out = process.argv[3] || 'beauty'; fs.mkdirSync(out, { recursive: true });
  for (const i of list) {
    const env = await page.evaluate(i => window.__mg.HOLES[i].theme.env, i);
    await page.evaluate(env => Promise.all([loadThemeModels('chars'), loadThemeModels(env)]), env);
    await page.evaluate(i => { window.__mg.buildHole(i); applyEnvMaps(); window.__mg.G.state = 'menu'; }, i);
    await page.waitForTimeout(800);
    for (const [k, yaw] of [[0, 0.6], [1, 2.4], [2, 4.2]]) {
      await page.evaluate(([yaw, k]) => { Cam.orbit = yaw; Cam.ov = Cam.ovTarget = 0; Cam.menuPitch = [0.32, 0.22, 0.45][k]; Cam.menuDist = [0.55, 0.42, 0.7][k]; }, [yaw, k]);
      await page.waitForTimeout(700);
      await page.screenshot({ path: `${out}/h${i + 1}_${k}.png` });
    }
  }
  console.log(errs.join('\n') || 'NO ERRORS'); await browser.close();
})();
