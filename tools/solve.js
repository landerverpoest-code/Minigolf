const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path'); const GAME = 'file://' + (process.env.GAME || path.resolve(__dirname, '..', 'index.html')); const THREE_JS = (process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package') + '/build/three.min.js';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 400, height: 300 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await page.route('**/three.min.js', r => r.fulfill({ path: THREE_JS, contentType: 'application/javascript' }));
  await page.goto(GAME);
  await page.waitForTimeout(1500);
  await page.click('#bStart').catch(()=>page.evaluate(()=>window.__mg.startGame(1)));
  const holes = process.argv[2] ? process.argv[2].split(',').map(Number) : [0,1,2,3,4,5,6,7,8];
  for (const i of holes) {
    const res = await page.evaluate((i) => {
      const m = window.__mg; m.loadHole(i); m.G.paused = true; m.G.state = 'play';
      const H = m.H(), b = m.ball, def = m.HOLES[i], R = 0.22;
      // geodetisch afstandsveld vanaf het gat
      const cs = 0.25, bb = H.bounds, W = Math.ceil((bb[2] - bb[0]) / cs) + 1, D = Math.ceil((bb[3] - bb[1]) / cs) + 1;
      const pip = (x, z, poly) => { let ins = false; for (let a = 0, c = poly.length - 1; a < poly.length; c = a++) { const xi = poly[a][0], zi = poly[a][1], xj = poly[c][0], zj = poly[c][1]; if (((zi > z) !== (zj > z)) && (x < (xj - xi) * (z - zi) / (zj - zi) + xi)) ins = !ins; } return ins; };
      const dseg = (x, z, p) => { const abx = p.bx - p.ax, abz = p.bz - p.az, L2 = abx * abx + abz * abz; let u = L2 > 1e-9 ? ((x - p.ax) * abx + (z - p.az) * abz) / L2 : 0; u = Math.max(0, Math.min(1, u)); return Math.hypot(x - p.ax - abx * u, z - p.az - abz * u); };
      const free = new Uint8Array(W * D), dist = new Float32Array(W * D).fill(1e9);
      for (let gz = 0; gz < D; gz++) for (let gx = 0; gx < W; gx++) {
        const x = bb[0] + gx * cs, z = bb[1] + gz * cs;
        if (!H.floors.some(F => pip(x, z, F.poly))) continue;
        if (H.zones.some(Z => ['water', 'quicksand'].includes(Z.type) && pip(x, z, Z.poly))) continue;
        if (H.statics.some(p => dseg(x, z, p) < p.r + R * 0.6)) continue;
        free[gz * W + gx] = 1;
      }
      const hx = Math.round((H.hole.x - bb[0]) / cs), hz = Math.round((H.hole.z - bb[1]) / cs);
      const q = [[hx, hz]]; dist[hz * W + hx] = 0;
      while (q.length) { const [x, z] = q.shift(); const d0 = dist[z * W + x]; for (const [dx, dz, c] of [[1, 0, 1], [-1, 0, 1], [0, 1, 1], [0, -1, 1], [1, 1, 1.414], [1, -1, 1.414], [-1, 1, 1.414], [-1, -1, 1.414]]) { const nx = x + dx, nz = z + dz; if (nx < 0 || nz < 0 || nx >= W || nz >= D || !free[nz * W + nx]) continue; const nd = d0 + c * cs; if (nd < dist[nz * W + nx]) { dist[nz * W + nx] = nd; q.push([nx, nz]); } } }
      const geo = (x, z) => { const gx = Math.round((x - bb[0]) / cs), gz = Math.round((z - bb[1]) / cs); let best = 1e9; for (let dz = -2; dz <= 2; dz++) for (let dx = -2; dx <= 2; dx++) { const k = (gz + dz) * W + gx + dx; if (gx + dx >= 0 && gz + dz >= 0 && gx + dx < W && gz + dz < D) best = Math.min(best, dist[k] + Math.hypot(dx, dz) * cs); } return best; };
      const startGeo = geo(def.start[0], def.start[1]);
      function snap() { return { t: H.t, kins: H.kins.map(k => { const o = {}; for (const key in k) { const v = k[key]; if (['number', 'boolean', 'string'].includes(typeof v)) o[key] = v; } if (k.items) o.__items = k.items.map(i => i.until); if (k.rows) o.__rows = k.rows.map(r => [r.F.ox, r.F.vel[0]]); o.__prims = k.prims.map(p => [p.ax, p.az, p.bx, p.bz, p.on]); return o; }) }; }
      function restore(S) { H.t = S.t; H.kins.forEach((k, i) => { const o = S.kins[i]; for (const key in o) if (!key.startsWith('__')) k[key] = o[key]; if (o.__items) k.items.forEach((it, j) => it.until = o.__items[j]); if (o.__rows) k.rows.forEach((r, j) => { r.F.ox = o.__rows[j][0]; r.F.vel[0] = o.__rows[j][1]; }); k.prims.forEach((p, j) => { const q = o.__prims[j]; p.ax = q[0]; p.az = q[1]; p.bx = q[2]; p.bz = q[3]; p.on = q[4]; }); }); b.held = null; b.air = 0; }
      function sim(node, wait, a, pw) {
        restore(node.snap); m.resetBall(node.x, node.z);
        for (let s = 0; s < wait * 120; s++) { m.physicsStep(1 / 120); if (b.state !== 'rest' && b.state !== 'moving') return { st: b.state }; }
        if (b.state !== 'rest' && b.state !== 'moving') return { st: b.state };
        const sx = b.x, sz = b.z; const sp = 1 + pw * 23; b.vx = Math.cos(a) * sp; b.vz = Math.sin(a) * sp; b.state = 'moving'; b.lastX = sx; b.lastZ = sz;
        for (let s = 0; s < 120 * 15; s++) { m.physicsStep(1 / 120); if (b.state !== 'moving' || b.held || b.air > 0) { if (b.state !== 'moving') break; } }
        return { st: b.state, x: b.x, z: b.z, snap: snap() };
      }
      let beam = [{ x: def.start[0], z: def.start[1], snap: snap(), g: startGeo }], found = null, bestG = startGeo, path = null;
      for (let depth = 1; depth <= def.par + 2 && !found; depth++) {
        const cand = [];
        for (const node of beam) {
          for (const wait of [0, 4.5]) for (let ai = 0; ai < 28; ai++) for (const pw of [0.15, 0.3, 0.5, 0.75, 0.95]) {
            const a = ai / 28 * Math.PI * 2 + depth * 0.37;
            const r = sim(node, wait, a, pw);
            if (r.st === 'sink') { found = depth; break; }
            if (r.st !== 'rest') continue;
            const g = geo(r.x, r.z); cand.push({ x: r.x, z: r.z, snap: r.snap, g }); bestG = Math.min(bestG, g);
          }
          if (found) break;
        }
        cand.sort((p, q) => p.g - q.g);
        beam = []; for (const c of cand) { if (beam.every(o => Math.hypot(o.x - c.x, o.z - c.z) > 1.2)) beam.push(c); if (beam.length >= 6) break; }
        if (!beam.length) break;
      }
      return { par: def.par, solvedIn: found, startGeo: startGeo.toFixed(1), bestGeo: bestG.toFixed(1) };
    }, i);
    console.log('hole', i + 1, JSON.stringify(res));
  }
  console.log(errs.join('\n') || 'no errors');
  await browser.close();
})();
