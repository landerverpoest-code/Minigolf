import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#e9edf2', rough=0.45)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
navy = mat('navy', '#1e2a48', rough=0.55)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
glow = mat('glow', '#40f0ff', rough=0.3, emit='#2ee6ff', emit_strength=2.0)
V = Vector
S = []   # vast deel
# platform + sokkel
S.append(bev(cyl(2.0, 0.35, loc=(0, 0, 0.175), verts=8, material=grey, r2=1.9), 0.04))
S.append(cyl(1.6, 0.12, loc=(0, 0, 0.41), verts=8, material=navy))
for k in range(8):
    a = k * TAU / 8 + TAU / 16
    S.append(box((0.5, 0.06, 0.02), loc=(1.75 * math.cos(a), 1.75 * math.sin(a), 0.355), rot=(0, 0, a + math.pi / 2), material=gold))
ped = lathe([(1.05, 0.45), (0.8, 1.4), (0.55, 2.9), (0.62, 3.0), (0.62, 3.15)], seg=8, material=white, phase=TAU / 16)
S.append(cyl(0.6, 0.12, loc=(0, 0, 2.2), verts=8, material=navy))
S.append(ped)
S.append(box((0.6, 0.04, 0.9), loc=(0, -0.79, 1.15), rot=(-0.25, 0, 0), material=navy))     # deurtje
S.append(box((0.4, 0.05, 0.06), loc=(0, -0.84, 1.05), rot=(-0.25, 0, 0), material=glow))
for k, a in enumerate([0.9, 2.6, 4.2]):
    S.append(box((0.6, 0.45, 0.5), loc=(1.25 * math.cos(a), 1.25 * math.sin(a), 0.72), rot=(0, 0, a), material=white, bevel=0.03))
    S.append(box((0.04, 0.3, 0.06), loc=(1.56 * math.cos(a), 1.56 * math.sin(a), 0.82), rot=(0, 0, a), material=glow))
join(S, 'base')
# draaiend deel: draaischijf + juk + schotel (rond verticale as)
pv = V((0, 0, 3.15))
R = []
R.append(cyl(0.7, 0.25, loc=(0, 0, 3.28), verts=12, material=grey))
R.append(cyl(0.72, 0.06, loc=(0, 0, 3.20), verts=12, material=navy))
for sx in (-1, 1):
    R.append(box((0.18, 0.5, 1.1), loc=(sx * 0.62, 0, 3.85), material=white, bevel=0.03))
R.append(box((1.0, 0.7, 0.5), loc=(0, 0.35, 3.65), material=white, bevel=0.04))
R.append(box((0.9, 0.05, 0.25), loc=(0, 0.71, 3.65), material=gold))
# schotel: paraboloïde, opening naar -Y en omhoog
f = 1.7
prof = [(0.0, 0.0)] + [(r, r * r / (4 * f)) for r in (0.45, 0.9, 1.35, 1.75, 2.0)] + [(2.08, 2.0 ** 2 / (4 * f) - 0.02), (1.75, 0.33), (0.9, 0.0), (0.4, -0.16), (0.0, -0.18)]
dish = lathe(prof, seg=20, material=white, cap_top=False, cap_bot=False)
flip(dish)
set_mat(dish, grey, lambda c, n: n.z < -0.2 and c.z < 0.6)
set_mat(dish, glow, lambda c, n: c.z > 0.57)
set_mat(dish, grey, lambda c, n: n.z > 0.2 and 0.15 < c.z < 0.3)
DS = [dish]
# ribben op de achterkant
for k in range(6):
    a = k * TAU / 6
    DS.append(box((1.6, 0.08, 0.1), loc=(0.95 * math.cos(a), 0.95 * math.sin(a), 0.05), rot=(0, -0.22, a), material=grey))
# voedingshoorn op 3 stangen
for k in range(3):
    a = k * TAU / 3 + 0.5
    DS.append(tube([V((1.65 * math.cos(a), 1.65 * math.sin(a), 0.42)), V((0.12 * math.cos(a), 0.12 * math.sin(a), 1.4))], r=0.03, seg=4, material=grey, smooth=False))
DS.append(cyl(0.15, 0.4, loc=(0, 0, 1.45), verts=8, r2=0.1, material=gold))
DS.append(ico(0.12, loc=(0, 0, 1.7), material=glow, sub=1))
DS.append(cyl(0.25, 0.3, loc=(0, 0, -0.25), verts=8, r2=0.35, material=grey))
D = join(DS, 'dish')
# schotel kantelen: as wijst naar -Y en 35 graden omhoog
T(D, rot=(math.radians(55), 0, 0))
T(D, loc=(0, -0.25, 4.15))
R.append(D)
for sx in (-1, 1):
    R.append(cyl(0.16, 0.25, loc=(sx * 0.62, 0, 4.15), rot=(0, math.pi / 2, 0), verts=8, material=navy))
spin = join(R, 'spin_dish')
origin_to(spin, pv)
report()
finish('space', 'satellite_dish', kind='hero', footprint=2.0, notes='grote schotel op sokkel; spin_dish draait langzaam rond verticale as; glow-rand en voedingspunt',
       spin=[{'node': 'spin_dish', 'axis': 'y', 'speed': 0.25}])
