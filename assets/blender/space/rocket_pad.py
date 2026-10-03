import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#eef1f5', rough=0.4)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
navy = mat('navy', '#1e2a48', rough=0.5)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
glow = mat('glow_window', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)
V = Vector
P = []
# lanceerplatform
P.append(bev(cyl(3.3, 0.6, loc=(0, 0, 0.3), verts=8, material=grey, r2=3.1), 0.05))
P.append(cyl(2.7, 0.06, loc=(0, 0, 0.63), verts=8, material=white))
P.append(cyl(1.0, 0.08, loc=(0, 0, 0.64), verts=8, material=navy))
for k in range(16):
    a = k * TAU / 16
    P.append(box((0.5, 0.18, 0.02), loc=(2.95 * math.cos(a), 2.95 * math.sin(a), 0.6), rot=(0, 0, a + math.pi / 2 + 0.6), material=gold))
for k, (a, r) in enumerate([(2.4, 2.4), (3.4, 2.4)]):
    P.append(cyl(0.35, 1.1, loc=(r * math.cos(a), r * math.sin(a), 1.15), verts=8, material=white))
    P.append(lathe([(0.35, 1.7), (0.25, 1.85), (0.0, 1.9)], seg=8, material=white))
    T(P[-1], loc=(r * math.cos(a), r * math.sin(a), 0))
    P.append(cyl(0.36, 0.1, loc=(r * math.cos(a), r * math.sin(a), 1.3), verts=8, material=navy))
# raket (retro): romp, neuskegel, banden
z0 = 2.1
prof = [(0.0, -0.05), (0.62, 0.0), (0.95, 0.45), (1.05, 1.5), (1.0, 3.4), (0.86, 5.0), (0.58, 6.3), (0.26, 7.25), (0.0, 7.6)]
body = lathe(prof, seg=16, material=white, smooth=True, loc=(0, 0, z0))
shade_smooth(body, 35)
set_mat(body, navy, lambda c, n: c.z > z0 + 6.0)
set_mat(body, gold, lambda c, n: z0 + 0.9 < c.z < z0 + 1.6)
P.append(body)
P.append(cyl(1.06, 0.18, loc=(0, 0, z0 + 3.4), verts=16, material=navy, r2=1.0))
P.append(cyl(0.03, 1.0, loc=(0, 0, z0 + 7.9), verts=4, material=grey))
P.append(ico(0.08, loc=(0, 0, z0 + 8.4), sub=1, material=glow))
# straalpijp
P.append(lathe([(0.35, 0.0), (0.45, -0.25), (0.62, -0.7), (0.55, -0.72), (0.38, -0.3), (0.0, -0.25)], seg=12, material=grey, loc=(0, 0, z0), cap_top=False))
P.append(lathe([(0.5, -0.6), (0.0, -0.5)], seg=12, material=glow, loc=(0, 0, z0), cap_top=False, cap_bot=False))
# vinnen = poten
fin = [(0.0, 0.0), (0.0, 2.4), (0.7, 1.2), (1.5, -0.2), (1.65, -1.45), (1.25, -1.45), (1.0, -0.55)]
for k in range(4):
    a = k * TAU / 4 + math.pi / 4
    f = prism([(0.9 + u, z0 + 0.6 + v) for u, v in fin], 0.18, navy, axis='y', bevel=0.035)
    T(f, rot=(0, 0, a))
    P.append(f)
    P.append(cyl(0.2, 0.1, loc=(2.45 * math.cos(a), 2.45 * math.sin(a), 0.7), verts=8, material=grey))
# patrijspoorten (voorkant -Y)
for z in (z0 + 4.4, z0 + 3.0, z0 + 2.1):
    w = cyl(0.22, 0.08, verts=10, material=glow)
    rim = torus(0.26, 0.055, seg=10, ring=4, material=grey, smooth=False)
    place_on(w, body, (0, -1, 0), center=(0, 0, z), sink=0.0)
    place_on(rim, body, (0, -1, 0), center=(0, 0, z), sink=0.0)
    P += [w, rim]
# luikje
hatch = box((0.5, 0.06, 0.7), material=grey)
place_on(hatch, body, (1, -0.3, 0), center=(0, 0, z0 + 5.4), sink=0.0)
P.append(hatch)
# lanceertoren (vakwerk) met loopbrug
gx, gy, gs, gh = 2.75, 0.6, 1.0, 9.6
G = []
for sx in (-1, 1):
    for sy in (-1, 1):
        G.append(box((0.12, 0.12, gh), loc=(gx + sx * gs / 2, gy + sy * gs / 2, 0.6 + gh / 2), material=gold))
n = 8
for i in range(n + 1):
    z = 0.6 + 0.3 + i * (gh - 0.4) / n
    for (dx, dy, w, d) in [(0, -gs / 2, gs, 0.07), (0, gs / 2, gs, 0.07), (-gs / 2, 0, 0.07, gs), (gs / 2, 0, 0.07, gs)]:
        G.append(box((w, d, 0.07), loc=(gx + dx, gy + dy, z), material=gold))
    if i < n:
        z2 = z + (gh - 0.4) / n
        for (sx, sgn) in [(-1, 1), (1, -1)]:
            G.append(tube([V((gx + sx * gs / 2, gy - gs / 2 * sgn, z)), V((gx + sx * gs / 2, gy + gs / 2 * sgn, z2))], r=0.03, seg=3, material=gold, smooth=False, cap=False))
        G.append(tube([V((gx + gs / 2 * (1 if i % 2 else -1), gy - gs / 2, z)), V((gx - gs / 2 * (1 if i % 2 else -1), gy - gs / 2, z2))], r=0.03, seg=3, material=gold, smooth=False, cap=False))
G.append(box((1.4, 1.4, 0.12), loc=(gx, gy, 0.6 + gh), material=grey))
G.append(cyl(0.05, 1.0, loc=(gx, gy, 0.6 + gh + 0.5), verts=4, material=grey))
G.append(ico(0.09, loc=(gx, gy, 0.6 + gh + 1.05), sub=1, material=glow))
# loopbrug naar het luik
bz = z0 + 5.4
G.append(box((1.6, 0.6, 0.08), loc=(gx - 1.15, gy - 0.25, bz - 0.38), material=grey))
G.append(box((1.6, 0.04, 0.04), loc=(gx - 1.15, gy - 0.53, bz - 0.0), material=white))
G.append(box((1.6, 0.04, 0.04), loc=(gx - 1.15, gy + 0.03, bz - 0.0), material=white))
G.append(box((0.6, 0.7, 0.9), loc=(gx - 0.1, gy - 0.25, bz + 0.1), material=white, bevel=0.03))
G.append(box((0.04, 0.4, 0.2), loc=(gx - 0.41, gy - 0.25, bz + 0.3), material=glow))
P.append(join(G, 'gantry'))
join(P, 'rocket_pad')
report()
finish('space', 'rocket_pad', kind='hero', footprint=3.3, notes='retro raket met vinnen-poten, patrijspoorten (glow_window) op lanceerplatform met vakwerktoren en loopbrug')
