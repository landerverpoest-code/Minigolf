// Contactblad: laadt alle GLB's van een thema in three.js r128 (dezelfde versie als de game)
// en rendert ze naast elkaar. Controleert zo dat de modellen echt werken in de game.
// Gebruik: node tools/glb_sheet.js <thema> [uit.png]
const path = require('path'), fs = require('fs');
const PW = '/opt/node22/lib/node_modules/playwright';
const { chromium } = require(PW);
const ROOT = path.resolve(__dirname, '..');
const THREE_DIR = process.env.THREE_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/package';
(async () => {
  const theme = process.argv[2]; if (!theme) { console.log('thema?'); process.exit(1); }
  const out = process.argv[3] || path.join(ROOT, 'assets/previews', theme, '_sheet.png');
  const dir = path.join(ROOT, 'assets/models', theme);
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.glb')).sort();
  const models = files.map(f => ({ name: f.replace('.glb', ''), b64: fs.readFileSync(path.join(dir, f)).toString('base64') }));
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const cols = Math.min(4, models.length), rows = Math.ceil(models.length / cols), cell = 300;
  const page = await browser.newPage({ viewport: { width: cols * cell, height: rows * cell } });
  const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.setContent('<html><body style="margin:0;background:#8fb8de"></body></html>');
  await page.addScriptTag({ path: path.join(THREE_DIR, 'build/three.min.js') });
  await page.addScriptTag({ path: path.join(THREE_DIR, 'examples/js/loaders/GLTFLoader.js') });
  const info = await page.evaluate(async ({ models, cols, rows, cell }) => {
    const W = cols * cell, Hh = rows * cell;
    const r = new THREE.WebGLRenderer({ antialias: true }); r.setSize(W, Hh); r.outputEncoding = THREE.sRGBEncoding; r.toneMapping = THREE.ACESFilmicToneMapping;
    r.setScissorTest(true); document.body.appendChild(r.domElement);
    const loader = new THREE.GLTFLoader(), res = [];
    for (let i = 0; i < models.length; i++) {
      const m = models[i], bin = Uint8Array.from(atob(m.b64), c => c.charCodeAt(0)).buffer;
      const gl = await new Promise((ok, bad) => loader.parse(bin, '', ok, bad)).catch(e => ({ err: String(e) }));
      if (gl.err) { res.push({ name: m.name, err: gl.err }); continue; }
      const sc = new THREE.Scene(); sc.background = new THREE.Color('#8fb8de');
      sc.add(new THREE.HemisphereLight('#ddeeff', '#554433', 0.8)); const sun = new THREE.DirectionalLight('#fff4e0', 1.3); sun.position.set(3, 6, 4); sc.add(sun);
      sc.add(gl.scene);
      const bb = new THREE.Box3().setFromObject(gl.scene), sz = bb.getSize(new THREE.Vector3()), c = bb.getCenter(new THREE.Vector3());
      let tri = 0, mats = new Set(), meshes = 0; gl.scene.traverse(o => { if (o.isMesh) { meshes++; mats.add(o.material.name); tri += (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3; } });
      const cam = new THREE.PerspectiveCamera(40, 1, 0.01, 1000), d = Math.max(sz.length(), 0.5) * 1.35;
      cam.position.set(c.x + d * 0.6, c.y + d * 0.45, c.z + d * 0.75); cam.lookAt(c);
      const x = (i % cols) * cell, y = Hh - (Math.floor(i / cols) + 1) * cell;
      r.setViewport(x, y, cell, cell); r.setScissor(x, y, cell, cell); r.render(sc, cam);
      res.push({ name: m.name, tris: tri, meshes, mats: [...mats], size: [sz.x, sz.y, sz.z].map(v => +v.toFixed(2)), minY: +bb.min.y.toFixed(3) });
    }
    // labels
    const lab = document.createElement('div'); lab.style.cssText = 'position:absolute;left:0;top:0;width:100%;height:100%;font:bold 14px sans-serif;color:#fff;text-shadow:0 1px 2px #000';
    res.forEach((m, i) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;left:${(i % cols) * cell + 6}px;top:${Math.floor(i / cols) * cell + 4}px`; d.textContent = m.name + (m.err ? ' FOUT' : ` (${m.tris} tri)`); lab.appendChild(d); });
    document.body.appendChild(lab);
    return res;
  }, { models, cols, rows, cell });
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await page.screenshot({ path: out });
  info.forEach(m => console.log(JSON.stringify(m)));
  console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'NO ERRORS', '\nsheet:', out);
  await browser.close();
})();
