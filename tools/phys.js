const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'); const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html')); const THREE_JS = (process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package') + '/build/three.min.js';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 600, height: 400 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  await page.goto(GAME);
  await page.waitForTimeout(1500);
  await page.click('#bStart').catch(()=>page.evaluate(()=>window.__mg.startGame(1)));
  for (const i of (process.argv[2]||"0,1,2,3,4,5,6,7,8").split(",").map(Number)) {
    const res = await page.evaluate((i) => {
      const m = window.__mg; m.loadHole(i); m.G.paused = true; m.G.state = 'play';
      const H = m.H(), b = m.ball, def = m.HOLES[i];
      const walls = H.statics.filter(p => Math.hypot(p.bx - p.ax, p.bz - p.az) > 1e-6);
      const R = 0.22;
      function cross(x1, z1, x2, z2, p) { // segment intersection with wall centerline
        const d = (x2 - x1) * (p.bz - p.az) - (z2 - z1) * (p.bx - p.ax); if (Math.abs(d) < 1e-12) return false;
        const t = ((p.ax - x1) * (p.bz - p.az) - (p.az - z1) * (p.bx - p.ax)) / d, u = ((p.ax - x1) * (z2 - z1) - (p.az - z1) * (x2 - x1)) / d;
        return t > 0 && t < 1 && u > 0 && u < 1;
      }
      let rng = 12345 + i; const rnd = () => { rng = (rng * 16807) % 2147483647; return rng / 2147483647; };
      function randomFloorPoint() {
        for (let k = 0; k < 500; k++) {
          const bb = H.bounds; const x = bb[0] + rnd() * (bb[2] - bb[0]), z = bb[1] + rnd() * (bb[3] - bb[1]);
          const F = H.floors.find(F => !F.active && pointInPolyT(x, z, F.poly)); if (!F) continue;
          if (H.zones.some(Z => (Z.type === 'lava' || Z.type === 'water' || Z.type === 'quicksand') && pointInPolyT(x, z, Z.poly))) continue;
          if (H.statics.some(p => distSeg(x, z, p) < p.r + R + 0.05)) continue;
          return [x, z];
        }
        return def.start;
      }
      function pointInPolyT(x, z, poly) { let ins = false; for (let a = 0, c = poly.length - 1; a < poly.length; c = a++) { const xi = poly[a][0], zi = poly[a][1], xj = poly[c][0], zj = poly[c][1]; if (((zi > z) !== (zj > z)) && (x < (xj - xi) * (z - zi) / (zj - zi) + xi)) ins = !ins; } return ins; }
      function distSeg(x, z, p) { const abx = p.bx - p.ax, abz = p.bz - p.az, L2 = abx * abx + abz * abz; let u = L2 > 1e-9 ? ((x - p.ax) * abx + (z - p.az) * abz) / L2 : 0; u = Math.max(0, Math.min(1, u)); return Math.hypot(x - p.ax - abx * u, z - p.az - abz * u); }
      const stats = { trials: 0, tunnel: 0, pen: 0, kinPenMax: 0, notStopped: 0, oob: 0, sink: 0, rest: 0, tunnelInfo: [] };
      for (let tr = 0; tr < 70; tr++) {
        const p0 = tr < 10 ? def.start : randomFloorPoint();
        const a = rnd() * Math.PI * 2, sp = tr % 3 === 0 ? 32 : 24 * (0.3 + rnd() * 0.7);
        m.resetBall(p0[0], p0[1]); b.vx = Math.cos(a) * sp; b.vz = Math.sin(a) * sp; b.state = 'moving';
        stats.trials++; let kinRun = 0, outcome = 'timeout';
        for (let s = 0; s < 120 * 25; s++) {
          const px = b.x, pz = b.z; m.physicsStep(1 / 120);
          if (b.state === 'oob' || b.state === 'sink') { outcome = b.state; }
          if (b.held || b.air > 0) { continue; }
          for (const w of walls) if (cross(px, pz, b.x, b.z, w)) { stats.tunnel++; if (stats.tunnelInfo.length < 5) stats.tunnelInfo.push([px.toFixed(2), pz.toFixed(2), b.x.toFixed(2), b.z.toFixed(2), Math.hypot(b.vx, b.vz).toFixed(1)].join(',')); break; }
          for (const w of H.statics) if (distSeg(b.x, b.z, w) < w.r + R - 0.03) { stats.pen++; break; }
          let kp = false; for (const k of H.kins) for (const p of k.prims) if (p.on && distSeg(b.x, b.z, p) < p.r + R - 0.05) { kp = true; if (kinRun === 30) stats.tunnelInfo.push('KIN ' + H.kins.indexOf(k) + ' ' + b.x.toFixed(2) + ',' + b.z.toFixed(2) + ' d=' + distSeg(b.x, b.z, p).toFixed(2) + ' r=' + p.r + ' st=' + b.state + ' v=' + Math.hypot(b.vx,b.vz).toFixed(2) + ' p=' + [p.ax,p.az,p.bx,p.bz].map(v=>v.toFixed(2)).join(',')); }
          kinRun = kp ? kinRun + 1 : 0; stats.kinPenMax = Math.max(stats.kinPenMax, kinRun);
          if (outcome !== 'timeout') break;
          if (b.state === 'rest') { outcome = 'rest'; break; }
        }
        if (outcome === 'timeout') { stats.notStopped++; stats.tunnelInfo.push('TO ' + b.x.toFixed(2) + ',' + b.z.toFixed(2) + ' v=' + Math.hypot(b.vx,b.vz).toFixed(3) + ' st=' + b.state); } else stats[outcome]++;
      }
      return stats;
    }, i);
    console.log('hole', i + 1, JSON.stringify(res));
  }
  console.log(errs.join('\n') || 'no errors');
  await browser.close();
})();
