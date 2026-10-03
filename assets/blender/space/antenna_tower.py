import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#e9edf2', rough=0.45)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
navy = mat('navy', '#1e2a48', rough=0.55)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
glow = mat('glow_beacon', '#ff40c8', rough=0.3, emit='#ff2ab8', emit_strength=2.5)
V = Vector
P = []
P.append(box((1.7, 1.7, 0.2), loc=(0, 0, 0.1), material=grey, bevel=0.03))
P.append(box((1.3, 1.3, 0.06), loc=(0, 0, 0.23), material=navy))
z0, z1, r0, r1 = 0.25, 5.3, 0.62, 0.16
lv = [z0 + (z1 - z0) * (i / 6) ** 0.9 for i in range(7)]
leg = lambda k, z: V(((r0 + (r1 - r0) * (z - z0) / (z1 - z0)) * math.cos(k * TAU / 3 + math.pi / 2), (r0 + (r1 - r0) * (z - z0) / (z1 - z0)) * math.sin(k * TAU / 3 + math.pi / 2), z))
for k in range(3):
    P.append(tube([leg(k, z0), leg(k, z1 + 0.1)], r=[0.05, 0.035], seg=4, material=white, smooth=False))
    P.append(box((0.22, 0.22, 0.12), loc=leg(k, z0 + 0.03), material=navy))
for i in range(6):
    for k in range(3):
        a, b = leg(k, lv[i]), leg((k + 1) % 3, lv[i + 1])
        P.append(tube([a, b], r=0.016, seg=3, material=grey if i % 2 else white, smooth=False, cap=False))
        a2, b2 = leg(k, lv[i + 1]), leg((k + 1) % 3, lv[i + 1])
        P.append(tube([a2, b2], r=0.018, seg=3, material=white, smooth=False, cap=False))
# top: platformpje, paneelantennes, schoteltje, mast met knipperlicht
P.append(cyl(0.32, 0.08, loc=(0, 0, z1 + 0.05), verts=6, material=navy))
for k in range(3):
    a = k * TAU / 3 + math.pi / 2 + math.pi / 3
    P.append(box((0.1, 0.22, 0.6), loc=(0.26 * math.cos(a), 0.26 * math.sin(a), z1 - 0.3), rot=(0, 0, a), material=white, bevel=0.015))
d = lathe([(0.0, 0.0), (0.18, 0.03), (0.26, 0.09), (0.0, 0.02)], seg=8, material=white, cap_top=False)
T(d, rot=(math.radians(70), 0, 0.4), loc=(0.0, -0.36, z1 - 0.9))
P.append(d)
P.append(box((0.12, 0.2, 0.12), loc=(0.0, -0.25, z1 - 0.9), material=gold))
P.append(cyl(0.04, 0.9, loc=(0, 0, z1 + 0.5), verts=5, material=grey))
P.append(cyl(0.07, 0.06, loc=(0, 0, z1 + 0.95), verts=6, material=navy))
P.append(ico(0.11, loc=(0, 0, z1 + 1.07), material=glow, sub=1))
P.append(cyl(0.02, 0.4, loc=(0.1, 0, z1 + 0.35), rot=(0, 0.2, 0), verts=4, material=grey))
join(P, 'antenna_tower')
report()
finish('space', 'antenna_tower', kind='scatter', footprint=0.85, notes='driepotige vakwerkmast met paneelantennes, schoteltje en knipperend glow_beacon-licht')
