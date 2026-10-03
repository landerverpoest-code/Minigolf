import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#e9edf2', rough=0.45)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
navy = mat('navy', '#1e2a48', rough=0.55)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
glow = mat('glow_ring', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)
P = []
P.append(bev(cyl(0.42, 0.16, loc=(0, 0, 0.08), verts=8, material=navy), 0.025))
P.append(lathe([(0.3, 0.16), (0.22, 0.5), (0.17, 1.15), (0.2, 1.2)], seg=8, material=white, phase=TAU / 16))
P.append(cyl(0.235, 0.08, loc=(0, 0, 0.42), verts=8, material=grey))
P.append(box((0.14, 0.02, 0.22), loc=(0, -0.235, 0.7), rot=(-0.08, 0, 0), material=gold))
P.append(box((0.08, 0.025, 0.04), loc=(0, -0.24, 0.85), material=glow))
P.append(torus(0.27, 0.05, loc=(0, 0, 1.28), seg=12, ring=4, material=glow, smooth=False))
P.append(cyl(0.2, 0.16, loc=(0, 0, 1.28), verts=8, material=grey))
P.append(lathe([(0.24, 1.36), (0.24, 1.42), (0.12, 1.5), (0, 1.52)], seg=8, material=navy))
P.append(cyl(0.015, 0.25, loc=(0, 0, 1.62), verts=4, material=grey))
P.append(ico(0.035, loc=(0, 0, 1.76), sub=1, material=glow))
for k in range(4):
    a = k * TAU / 4 + TAU / 8
    P.append(box((0.08, 0.2, 0.06), loc=(0.38 * math.cos(a), 0.38 * math.sin(a), 0.19), rot=(0, 0, a), material=grey))
join(P, 'beacon_pylon')
report()
finish('space', 'beacon_pylon', kind='scatter', footprint=0.45, notes='korte baken-pyloon met lichtring (glow_ring)')
