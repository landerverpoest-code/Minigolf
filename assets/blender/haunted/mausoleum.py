import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
stone = mat('stone', '#8a958a', rough=0.9)
dark = mat('slate', '#5a546c', rough=0.9)
iron = mat('iron', '#2b2733', rough=0.45, metal=0.6)
glow = mat('glow_crypt', '#2f9a1c', rough=0.4, emit='#4ad024', emit_strength=1.5)
moss = mat('moss', '#557f35', rough=1.0)
V = Vector
P = []
# sokkel + traptreden (voorkant -Y)
P.append(box((3.8, 4.3, 0.3), loc=(0, 0.25, 0.15), material=dark, bevel=0.03))
for i, (d, y) in enumerate([(0.45, -2.12), (0.35, -2.42)]):
    P.append(box((2.2 - i * 0.2, 0.32, 0.3 - i * 0.12), loc=(0, y + 0.06 * i, (0.3 - i * 0.12) / 2), material=stone, bevel=0.025))
# grafkamer
P.append(box((3.1, 3.2, 2.6), loc=(0, 0.55, 1.6), material=stone, bevel=0.04))
P.append(box((3.2, 3.3, 0.18), loc=(0, 0.55, 0.39), material=dark, bevel=0.02))
for sx in (-1, 1):
    for y in (-1.02, 2.12):
        P.append(box((0.3, 0.3, 2.6), loc=(sx * 1.52, y, 1.6), material=dark, bevel=0.03))
# zuilen in het portiek
for sx in (-1, 1):
    x, y = sx * 1.15, -1.7
    P.append(box((0.5, 0.5, 0.16), loc=(x, y, 0.38), material=dark, bevel=0.02))
    col = lathe([(0.2, 0.46), (0.19, 0.6), (0.17, 2.3), (0.21, 2.45), (0.21, 2.52)], seg=10, material=stone, smooth=False)
    P.append(col)
    P.append(box((0.52, 0.52, 0.14), loc=(x, y, 2.58), material=dark, bevel=0.02))
    T(col, loc=(x, y, 0))
# hoofdgestel
P.append(box((3.5, 0.75, 0.32), loc=(0, -1.6, 2.81), material=stone, bevel=0.03))
P.append(box((3.6, 4.0, 0.12), loc=(0, 0.25, 3.03), material=dark, bevel=0.02))
plate = box((1.2, 0.04, 0.2), loc=(0, -1.99, 2.81), material=dark)
P.append(plate)
# fronton (driehoek) + dak met barst en afgebroken hoek
tri = prism([(-1.8, 0), (1.8, 0), (0, 1.0)], 0.3, stone, axis='y', loc=(0, -1.75, 3.09), bevel=0.03)
P.append(tri)
tymp = prism([(-1.3, 0), (1.3, 0), (0, 0.68)], 0.06, dark, axis='y', loc=(0, -1.92, 3.17))
P.append(tymp)
ocu = cyl(0.2, 0.08, loc=(0, -1.93, 3.48), rot=(math.pi / 2, 0, 0), verts=10, material=glow)
ring = torus(0.22, 0.05, loc=(0, -1.96, 3.48), rot=(math.pi / 2, 0, 0), seg=10, ring=4, material=stone, smooth=False)
P += [ocu, ring]
ang = math.atan2(1.0, 1.8)
sl = math.hypot(1.8, 1.0) + 0.2
for sx in (-1, 1):
    r = box((sl, 4.1, 0.16), loc=(sx * 0.9, 0.3, 3.62), rot=(0, sx * ang, 0), material=dark, bevel=0.025)
    if sx > 0:   # afgebroken hoek vooraan rechts
        cut = box((0.9, 0.9, 0.9), loc=(1.85, -1.7, 3.3), rot=(0.3, 0.5, 0.7))
        jitter(cut, 0.08, 9)
        boolean(r, cut)
    P.append(r)
P.append(box((0.22, 4.15, 0.18), loc=(0, 0.3, 4.12), material=stone, bevel=0.02))
# barst in het dak (rechterkant) + gat
ztop = lambda x: 3.62 - (x - 0.9) / 1.8 + 0.092
ck = tube([V((x, y, ztop(x))) for x, y in [(0.3, -1.3), (0.55, -0.7), (0.45, -0.1), (0.8, 0.5), (0.95, 1.2), (1.35, 1.75)]],
          r=[0.0, 0.04, 0.045, 0.045, 0.035, 0.0], seg=3, material=iron, smooth=False)
P.append(ck)
# afgebroken stuk op de grond
for (x, y, rz, s) in [(2.05, -1.6, 0.6, 1), (2.3, -1.1, 1.4, 2)]:
    b = box((0.35, 0.25, 0.18), loc=(x, y, 0.09), rot=(0.1, 0.15, rz), material=dark); jitter(b, 0.03, s); P.append(b)
# kruis op de top
P.append(box((0.12, 0.12, 0.7), loc=(0, -1.75, 4.45), material=stone, bevel=0.015))
P.append(box((0.42, 0.12, 0.12), loc=(0, -1.75, 4.55), material=stone, bevel=0.015))
# deuropening met groene gloed + ijzeren hekdeuren (linker op een kier)
dw, dh, dy = 1.3, 1.9, -1.06
arch = [(-dw / 2, 0), (dw / 2, 0)] + [(x, dh - dw / 2 + z) for x, z in arc2d(0, 0, dw / 2, 0, math.pi, 7)]
frame = prism([(x * 1.25, z * 1.08) for x, z in arch], 0.12, dark, axis='y', loc=(0, dy - 0.04, 0.48))
P.append(frame)
P.append(prism(arch, 0.04, glow, axis='y', loc=(0, dy - 0.11, 0.48)))
for side in (-1, 1):
    bars = []
    w = dw / 2 - 0.04
    for k in range(4):
        x = side * (0.06 + k * (w - 0.06) / 3)
        hh = dh - 0.08 - (0.25 * (abs(x) / w) ** 2 if True else 0)
        bars.append(cyl(0.022, hh, loc=(x, 0, 0.52 + hh / 2), verts=4, material=iron))
        bars.append(cone(0.045, 0.1, loc=(x, 0, 0.52 + hh + 0.04), verts=4, material=iron))
    for z in (0.62, 1.2, 1.8):
        bars.append(box((w, 0.04, 0.05), loc=(side * w / 2, 0, z), material=iron))
    pts = [V((side * (0.06 + (w - 0.06) * (0.5 + 0.35 * math.cos(t))), 0, 1.5 + 0.22 * math.sin(t))) for t in [k * TAU / 8 for k in range(9)]]
    bars.append(tube(pts, r=0.015, seg=3, material=iron, smooth=False, cap=False))
    g = join(bars, 'gate')
    T(g, loc=(0, dy - 0.2, 0))
    if side < 0:
        T(g, rot=(0, 0, 0.55), pivot=(-dw / 2 + 0.02, dy - 0.2, 0))
    P.append(g)
# smalle zijramen met gloed
for sx in (-1, 1):
    for y in (0.0, 1.1):
        P.append(box((0.04, 0.16, 0.7), loc=(sx * 1.56, y + 0.1, 1.9), material=glow))
        P.append(box((0.05, 0.3, 0.84), loc=(sx * 1.555, y + 0.1, 1.9), material=dark))
        T(P[-1], loc=(sx * -0.005, 0, 0))
# vuurschalen met groene vlammen naast de trap
for sx in (-1, 1):
    x, y = sx * 1.45, -2.3
    P.append(cyl(0.12, 0.6, loc=(x, y, 0.3), verts=6, r2=0.08, material=dark))
    P.append(lathe([(0.08, 0.6), (0.26, 0.75), (0.24, 0.82)], seg=8, material=iron, cap_top=True))
    T(P[-1], loc=(x, y, 0))
    fl = tube([V((x, y, 0.78)), V((x + 0.03, y, 0.95)), V((x - 0.02, y + 0.01, 1.1)), V((x + 0.02, y, 1.22))], r=[0.18, 0.13, 0.07, 0.0], seg=5, material=glow, smooth=False)
    P.append(fl)
# mos
for (x, y, z, s, sc) in [(-1.2, -1.6, 3.32, 1, 1.4), (1.6, 1.6, 3.3, 2, 1.2), (-1.7, -1.0, 0.33, 3, 1.5), (0.8, -2.3, 0.31, 4, 1.0), (-0.3, 2.3, 3.75, 5, 1.0)]:
    P.append(shade_smooth(ico(0.18 * sc, loc=(x, y, z), material=moss, scale=(1.5, 1.2, 0.4), jitter=0.03, seed=s)))
# barst in de muur
P.append(tube([V((1.0, -1.25, 2.5)), V((0.85, -1.25, 2.2)), V((0.95, -1.25, 1.9)), V((0.8, -1.25, 1.6))], r=[0.0, 0.025, 0.02, 0.0], seg=3, material=iron, smooth=False))
join(P, 'mausoleum')
report()
finish('haunted', 'mausoleum', kind='hero', footprint=2.3, notes='kleine crypte met zuilen, ijzeren hekdeuren (één op een kier), gebarsten dak; groene gloed binnen, oculus, zijramen en vuurschalen = glow_crypt')
