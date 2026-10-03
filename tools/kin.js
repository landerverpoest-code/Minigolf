const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'); const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html')); const THREE_JS = (process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package') + '/build/three.min.js';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 400, height: 300 } }); page.setDefaultTimeout(600000);
  const errs = []; page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  await page.goto(GAME); await page.waitForTimeout(1500); await page.click('#bStart');
  for (const i of (process.argv[2]||'0,1,2,3,4,5,6,7,8').split(',').map(Number)) {
    const r = await page.evaluate((i) => {
      const m = window.__mg; m.loadHole(i); m.G.paused = true; m.G.state = 'play';
      const H = m.H(), b = m.ball, R = 0.22; let worst = 0, trials = 0, hits = 0, maxOut = 0, minKickOut = 99;
      const dseg = (x, z, p) => { const abx = p.bx - p.ax, abz = p.bz - p.az, L2 = abx * abx + abz * abz; let u = L2 > 1e-9 ? ((x - p.ax) * abx + (z - p.az) * abz) / L2 : 0; u = Math.max(0, Math.min(1, u)); return Math.hypot(x - p.ax - abx * u, z - p.az - abz * u); };
      for (let k = 0; k < 40; k++) {
        H.t = k * 0.73; for (let s = 0; s < 3; s++) m.physicsStep(1 / 120);
        const prims = []; H.kins.forEach(kn => kn.prims.forEach(p => { if (p.on) prims.push(p); }));
        if (!prims.length) continue; const p = prims[k % prims.length];
        const u = (k * 0.37) % 1; m.resetBall(p.ax + (p.bx - p.ax) * u + 0.01, p.az + (p.bz - p.az) * u); trials++;
        let run = 0, maxRun = 0, sp0 = 0;
        for (let s = 0; s < 240; s++) {
          m.physicsStep(1 / 120); if (s === 0) sp0 = Math.hypot(b.vx, b.vz);
          if (b.state === 'oob' || b.state === 'sink') break;
          let ov = false; for (const kn of H.kins) for (const q of kn.prims) if (q.on && dseg(b.x, b.z, q) < q.r + R - 0.05) ov = true;
          run = ov ? run + 1 : 0; maxRun = Math.max(maxRun, run);
        }
        if (maxRun > 60) (window.__stk = window.__stk || []).push([(H.kins.find(kn => kn.prims.includes(p)).def||{type:'bumper'}).type, b.x.toFixed(2), b.z.toFixed(2), b.state].join(' ')); worst = Math.max(worst, maxRun); if (sp0 > 0.5) hits++; maxOut = Math.max(maxOut, sp0); if (p.kick) minKickOut = Math.min(minKickOut, sp0);
      }
      const stk = window.__stk; window.__stk = []; return { stk, trials, launched: hits, worstOverlapSteps: worst, maxLaunch: maxOut.toFixed(1), minLaunchKick: minKickOut.toFixed(1) };
    }, i);
    console.log('hole', i + 1, JSON.stringify(r));
  }
  console.log(errs.join('\n') || 'no errors'); await browser.close();
})();
