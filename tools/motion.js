const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'); const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html')); const THREE_JS = (process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package') + '/build/three.min.js';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 500, height: 320 } }); page.setDefaultTimeout(300000);
  const errs = []; page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message)); page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  await page.goto(GAME); await page.waitForTimeout(1500);
  await page.evaluate(() => __mg.startGame(1));
  for (let i = 0; i < 9; i++) {
    const r = await page.evaluate((i) => {
      const m = __mg; m.loadHole(i); m.G.paused = true; m.G.state = 'play';
      const H = m.H();
      // speler richt, camera in overzicht, bal ligt stil: mag allemaal geen invloed hebben
      m.G.aim = { id: 1, dir: [0, -1], power: 0.5 }; Cam.ovTarget = 1; Cam.yaw += 1;
      const sig = (k) => { const v = []; k.prims.forEach(p => v.push(p.ax, p.az, p.bx, p.bz, p.on ? 1 : 0)); for (const key of ['ox', 'angle', 'duneS', 's', 'x', 'z']) if (typeof k[key] === 'number') v.push(k[key]); if (k.rows) k.rows.forEach(r => v.push(r.F.ox)); if (k.level) v.push(k.level(H.t)); if (k.def && k.def.river) { const Z = H.zonesById[k.def.river]; v.push(Z.mesh.material.emissiveIntensity, Z.typeAt(H.t) === 'lava' ? 1 : 0); } if (k.group) { k.group.updateMatrixWorld(true); k.group.traverse(o => { if (o.isMesh || o.isGroup) v.push(...o.matrixWorld.elements.slice(12, 15), o.matrixWorld.elements[0], o.matrixWorld.elements[2], o.matrixWorld.elements[5]); if (o.material && o.material.emissiveIntensity !== undefined) v.push(o.material.emissiveIntensity); if (o.material && o.material.opacity !== undefined) v.push(o.material.opacity); }); } return v; };
      const step = (sec) => { for (let s = 0; s < sec * 120; s++) { m.physicsStep(1 / 120); if (s % 12 === 0) for (const k of H.kins) if (k.visual) k.visual(H.t, 0.1); } };
      step(60);
      const t60 = H.t, res = [];
      const base = H.kins.map(sig);
      const changed = H.kins.map(() => false);
      if (H.byId.bridge) H.byId.bridge.trigger(H.t); // schild geraakt
      for (let j = 0; j < 80; j++) { step(0.25); H.kins.forEach((k, n) => { const s2 = sig(k); if (s2.length !== base[n].length || s2.some((v, q) => Math.abs(v - base[n][q]) > 1e-3)) changed[n] = true; }); }
      H.kins.forEach((k, n) => res.push((k.def ? k.def.type : 'bumper') + ':' + (changed[n] ? 'beweegt' : 'STIL')));
      m.G.aim = null; Cam.ovTarget = 0;
      return { hole: i + 1, t: t60.toFixed(1), res: res.join(' ') };
    }, i);
    console.log(JSON.stringify(r));
  }
  // echte hoofdlus: spelklok loopt door, ook na een tabwissel
  const t0 = await page.evaluate(() => { __mg.G.paused = false; document.dispatchEvent(new Event('visibilitychange')); return __mg.H().t; });
  await page.waitForTimeout(8000);
  const t1 = await page.evaluate(() => __mg.H().t);
  console.log('hoofdlus: H.t van', t0.toFixed(2), 'naar', t1.toFixed(2));
  console.log(errs.join('\n') || 'NO ERRORS'); await browser.close();
})();
