import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *
from ship_kit import *

OBS = mat('obsidian', '#2a2433', rough=0.22, metal=0.15)
BAS = mat('basalt', '#5a4448', rough=0.75)
SAILD = mat('sail_dark', '#781818', rough=0.8)
BONE = mat('bone', '#ecdfc2', rough=0.55)
GLOW = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff5200', emit_strength=2.0)
rnd = random.Random(5)

bp = []
hull = hull_mesh(OBS)
bpy.context.view_layer.update()
iso_paint(hull, lambda p: (deck(p.y) - 0.07 - p.z) * 10, BAS)       # basalt deck
bp.append(hull)
bpy.context.view_layer.update()

# glowing waterline seam + jagged cracks + glowing portholes
for sx in (-1, 1):
    pts = []
    for y in [-2.5, -2.2, -1.8, -1.2, -0.5, 0.3, 1.1, 1.8, 2.36]:
        p, n = ring_on(hull, y, 0.1, sx, push=0.004)
        if p is not None:
            pts.append(p)
    bp.append(tube(pts, 0.03, seg=3, material=GLOW, cap=False))
    for (yc, zc_) in ((-1.9, 0.4), (-0.85, 0.55), (0.0, 0.3), (1.0, 0.5), (1.85, 0.35)):
        cr = []
        y, z = yc, zc_
        for k in range(5):
            p, n = ring_on(hull, y, z, sx, push=0.003)
            if p is not None:
                cr.append(p)
            y += rnd.uniform(0.08, 0.18) * (1 if k % 2 else -0.4)
            z += rnd.uniform(-0.12, -0.06) if k % 2 else rnd.uniform(0.02, 0.06)
        if len(cr) > 2:
            bp.append(tube(cr, [0.04, 0.032, 0.025, 0.016, 0.005][:len(cr)], seg=3, material=GLOW, cap=False))
    for y in (-1.35, -0.4, 0.55):
        p, n = ring_on(hull, y, 0.45, sx)
        M = orient(p, n)
        bp.append(xf(torus(0.13, 0.04, seg=8, ring=3, material=BONE), M))
        bp.append(xf(cyl(0.11, 0.04, verts=6, material=GLOW), M))

# bulwark with bone spikes
loop = []
ys_side = [2.3, 1.8, 1.2, 0.5, -0.3, -1.1, -1.7, -2.15, -2.45]
for sx in (-1, 1):
    seq = ys_side if sx == -1 else ys_side[::-1]
    for y in seq:
        x = sx * (beam(y) - 0.07)
        t = top_at(hull, x, y)
        loop.append(V(x, y, t.z + 0.12))
    if sx == -1:
        loop.append(V(0, -2.62, deck(-2.62) + 0.14))
loop.append(loop[0].copy())
bp.append(tube(loop, 0.2, seg=6, material=OBS, flat=0.3, cap=False))
for i, q in enumerate(loop[:-1]):
    if i % 1 == 0:
        bp.append(cone(0.06, 0.26, loc=q + V(0, 0, 0.3), verts=4, material=BONE))

# aft cabin (dark stone with glowing windows) + horns
CY0, CY1 = 1.05, 2.3
cab_w = beam(1.6) - 0.22
ctop = deck(CY1) + 0.72
bp.append(box((cab_w * 2, CY1 - CY0, ctop - 0.5), loc=(0, (CY0 + CY1) / 2, (ctop + 0.5) / 2), material=OBS, bevel=0.06))
bp.append(box((cab_w * 2 + 0.2, CY1 - CY0 + 0.25, 0.12), loc=(0, (CY0 + CY1) / 2 + 0.05, ctop + 0.06), material=BAS, bevel=0.04))
fy = CY0 - 0.005
# pointed arch door (glowing) + windows
bp.append(xf(prism([(-0.2, 0), (0.2, 0), (0.2, 0.42), (0, 0.62), (-0.2, 0.42)], -0.03, 0.03, material=GLOW),
             Matrix.Translation(V(0, fy, deck(CY0) + 0.02)) @ rotm((90, 0, 0))))
for sx in (-1, 1):
    bp.append(xf(prism([(-0.11, 0), (0.11, 0), (0.11, 0.18), (0, 0.3), (-0.11, 0.18)], -0.03, 0.03, material=GLOW),
                 Matrix.Translation(V(sx * 0.55, fy, deck(CY0) + 0.3)) @ rotm((90, 0, 0))))
for sx in (-1, 0, 1):
    bp.append(xf(prism([(-0.12, 0), (0.12, 0), (0.12, 0.2), (0, 0.33), (-0.12, 0.2)], -0.03, 0.03, material=GLOW),
                 Matrix.Translation(V(sx * 0.42, CY1 + 0.005, ctop - 0.5)) @ rotm((90, 0, 0))))
# curved bone horns on the stern corners
for sx in (-1, 1):
    hb = V(sx * (cab_w + 0.02), CY1 + 0.05, ctop + 0.1)
    bp.append(tube(bezier(hb, hb + V(sx * 0.25, 0.1, 0.25), hb + V(sx * 0.2, 0.35, 0.6), n=4), [0.11, 0.09, 0.065, 0.035, 0.004], seg=6, material=BONE))
# spiky rail on the quarterdeck
rail = [V(-cab_w - 0.05, CY0 - 0.02, ctop + 0.32), V(-cab_w - 0.05, CY1 + 0.12, ctop + 0.32), V(cab_w + 0.05, CY1 + 0.12, ctop + 0.32),
        V(cab_w + 0.05, CY0 - 0.02, ctop + 0.32)]
bp.append(tube(rail, 0.045, seg=4, material=OBS, round_end=True))
for a, b in zip(rail, rail[1:]):
    n = max(2, int((b - a).length / 0.42))
    for k in range(n + 1):
        q = a.lerp(b, k / n)
        bp.append(cone(0.045, 0.5, loc=(q.x, q.y, ctop + 0.32), verts=4, material=BONE))
# brazier (lava bowl) on the stern
lp = V(0, CY1 - 0.15, ctop + 0.12)
bp.append(lathe([(0.0, lp.z), (0.1, lp.z), (0.07, lp.z + 0.25), (0.24, lp.z + 0.38), (0.2, lp.z + 0.42), (0, lp.z + 0.36)], seg=8, material=OBS,
                M=Matrix.Translation(V(0, lp.y, 0))))
bp.append(ell(lp + V(0, 0, 0.4), (0.19, 0.19, 0.06), seg=8, rings=4, material=GLOW))
# bowsprit + bone skull figurehead
b0 = V(0, -2.45, deck(-2.45) + 0.12)
b1 = V(0, -3.4, deck(-2.45) + 0.62)
bp.append(tube([b0, b1], [0.1, 0.03], seg=6, material=BONE))
SK = V(0, -2.78, deck(-2.6) - 0.08)
bp.append(ell(SK, (0.22, 0.2, 0.2), seg=10, rings=7, material=BONE))
bp.append(ell(SK + V(0, -0.06, -0.15), (0.14, 0.12, 0.08), seg=8, rings=4, material=BONE))
for sx in (-1, 1):
    bp.append(ell(SK + V(sx * 0.085, -0.17, 0.02), (0.06, 0.03, 0.065), seg=6, rings=4, material=GLOW))
    bp.append(tube(bezier(SK + V(sx * 0.15, 0.0, 0.14), SK + V(sx * 0.32, 0.0, 0.2), SK + V(sx * 0.36, -0.12, 0.4), n=3), [0.05, 0.035, 0.02, 0.003], seg=5, material=BONE))
bp.append(cone(0.03, 0.06, loc=SK + V(0, -0.2, -0.05), verts=3, rot=(math.pi, 0, 0), material=OBS))
for k in (-1, 0, 1):
    bp.append(box((0.035, 0.02, 0.05), loc=SK + V(k * 0.045, -0.17, -0.13), material=OBS))
# lava rocks cargo on deck
for (x, y, r) in ((0.5, -1.05, 0.2), (0.25, -1.3, 0.15)):
    bp.append(ico(r, loc=(x, y, deck(y) + r * 0.6), sub=1, material=OBS, jitter=0.03, seed=int(r * 100)))
    bp.append(ico(r * 0.55, loc=(x, y - r * 0.4, deck(y) + r * 0.9), sub=1, material=GLOW, jitter=0.0))
body = part(bp, 'body', (0, 0, 0), angle=50)

# ---------------------------------------------------------------- sail part (mast + yards + tattered sail with glowing edges)
MB = V(0, MAST_Y, deck(MAST_Y) - 0.02)
TOP = 4.55
sp = []
sp.append(tube([MB, V(0, MAST_Y, TOP)], [0.13, 0.085], seg=6, material=OBS))
YT, YB = 3.85, 1.85
for z, w in ((YT, 1.45), (YB, 1.62)):
    sp.append(tube([V(-w, MAST_Y - 0.12, z), V(w, MAST_Y - 0.12, z)], [0.055, 0.055], seg=5, material=OBS))
    for sx in (-1, 1):
        sp.append(cone(0.07, 0.25, loc=(sx * (w + 0.1), MAST_Y - 0.12, z), rot=(0, sx * math.pi / 2, 0), verts=4, material=BONE))
sail, border, left, right = sail_grid(2.7, 3.05, YB + 0.18, YT - 0.03, MAST_Y - 0.18, 0.45, nu=8, nv=6, material=SAILD,
                                      jag=0.28, holes=((2, 3), (5, 1), (6, 4)), seed=3)
sp.append(sail)
# glowing edges: bottom jagged hem + sides
sp.append(tube([q + V(0, -0.01, 0) for q in border], 0.03, seg=3, material=GLOW, cap=False))
sp.append(tube([q + V(0, -0.01, 0) for q in left], 0.025, seg=3, material=GLOW, cap=False))
sp.append(tube([q + V(0, -0.01, 0) for q in right], 0.025, seg=3, material=GLOW, cap=False))
# skull emblem on the sail (bone)
bz = (YB + YT) / 2 + 0.15
em_y = MAST_Y - 0.18 - 0.45 * 0.93 - 0.05
sp.append(xf(ell((0, 0, 0), (0.34, 0.3, 0.06), seg=10, rings=5, material=BONE), Matrix.Translation(V(0, em_y, bz)) @ rotm((90, 0, 0))))
sp.append(xf(ell((0, 0, 0), (0.2, 0.13, 0.05), seg=8, rings=4, material=BONE), Matrix.Translation(V(0, em_y, bz - 0.3)) @ rotm((90, 0, 0))))
for sx in (-1, 1):
    sp.append(xf(ell((0, 0, 0), (0.09, 0.1, 0.03), seg=6, rings=3, material=GLOW), Matrix.Translation(V(sx * 0.12, em_y - 0.045, bz - 0.02)) @ rotm((90, 0, 0))))
    sp.append(tube([V(sx * 0.42, em_y + 0.02, bz - 0.55), V(-sx * 0.42, em_y + 0.02, bz - 0.05)], 0.045, seg=4, material=BONE, round_end=True))
# crow's nest (dark) + top spike
cz = 4.08
sp.append(lathe([(0.0, cz), (0.3, cz), (0.36, cz + 0.28), (0.3, cz + 0.28), (0.26, cz + 0.06), (0, cz + 0.06)], seg=8, material=OBS,
                M=Matrix.Translation(V(0, MAST_Y, 0))))
sp.append(cone(0.08, 0.3, loc=(0, MAST_Y, TOP + 0.12), verts=5, material=BONE))
for z, w in ((YT, 1.45), (YB, 1.62)):
    for sx in (-1, 1):
        sp.append(tube([V(0, MAST_Y, TOP - 0.1), V(sx * w * 0.97, MAST_Y - 0.12, z + 0.03)], 0.012, seg=3, material=OBS, cap=False))
sail_o = part(sp, 'sail', MB, angle=50)

# ---------------------------------------------------------------- flag
FP = V(0, MAST_Y + 0.08, TOP - 0.12)
fl = flag_mesh(0.8, 0.45, 0, MAST_Y + 0.08, TOP - 0.55, SAILD, notch=True)
fe = tube([V(0, MAST_Y + 0.08, TOP - 0.55 + 0.45)] + [V(0.08 * math.sin(u * math.pi * 2.4) * u, MAST_Y + 0.08 + u * 0.8, TOP - 0.1 - 0.08 * u * u) for u in (0.33, 0.66, 1.0)],
          0.018, seg=3, material=GLOW, cap=False)
flag_o = part([fl, fe], 'flag', FP, angle=50)

report()
views('ship_lava')
montage('ship_lava')
finish('chars', 'ship_lava', kind='char', footprint=1.6, grounded=False,
       notes=f'origin at lava-line centre (0,0,0), bow -Y, keel to z=-0.55. parts: body (pivot 0,0,0, obsidian hull, glow_lava cracks/portholes, bone skull figurehead); '
             f'sail = mast+yards+tattered sail with glowing edges, pivot at mast base ({MB.x:.2f},{MB.y:.2f},{MB.z:.2f}); '
             f'flag pivot at its pole attachment ({FP.x:.2f},{FP.y:.2f},{FP.z:.2f}) (top level, flies toward +Y)')
