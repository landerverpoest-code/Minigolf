import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
wood = mat('wood', '#6a4630', rough=0.85)
wdark = mat('wood_dark', '#3b2820', rough=0.9)
satin = mat('satin', '#5a2a6a', rough=0.5)
bone = mat('bone', '#e6dcc0', rough=0.7)
V = Vector
# klassieke zeshoekige kist (bovenaanzicht), lengte langs X
L, W1, W2 = 1.2, 0.26, 0.2
hexa = [(-L / 2, -W2 * 0.75), (-L / 2 + 0.36, -W1), (L / 2, -W2 * 0.55), (L / 2, W2 * 0.55), (-L / 2 + 0.36, W1), (-L / 2, W2 * 0.75)]
base = prism(hexa, 0.3, wood, axis='z', loc=(0, 0, 0))
inset(base, lambda c, n: n.z > 0.9, thick=0.035, depth=-0.24, mat_index=None)
# binnenkant satijn: bodem van de holte + wanden waarvan de normaal naar binnen wijst
def inner(c, n):
    if c.z > 0.295:
        return False
    if n.z > 0.9:
        return True
    return abs(n.z) < 0.2 and n.dot(-V((c.x + 0.05, c.y, 0))) > 0
set_mat(base, satin, inner)
band = prism(hexa, 0.04, wdark, axis='z', loc=(0, 0, 0.0))
T(band, scale=(1.02, 1.06, 1.0))
# deksel, scheef opengeschoven
lid = prism(hexa, 0.06, wood, axis='z', loc=(0, 0, 0), bevel=0.012)
c1 = box((0.5, 0.06, 0.025), loc=(-0.05, 0, 0.07), material=wdark)
c2 = box((0.06, 0.26, 0.025), loc=(-0.15, 0, 0.07), material=wdark)
lid = join([lid, c1, c2], 'lid')
T(lid, rot=(math.radians(6), 0, math.radians(-14)), loc=(0.06, 0.1, 0.3))
# handgrepen
hs = [box((0.1, 0.03, 0.03), loc=(x, sy * (0.23 if x < -0.1 else 0.18), 0.17), material=wdark) for x in (-0.3, 0.2) for sy in (-1, 1)]
# benige vingers die uit de kier piepen
fingers = []
for k in range(4):
    x0 = 0.05 + k * 0.045
    pts = [V((x0, -0.1, 0.25)), V((x0 + 0.01, -0.19, 0.33)), V((x0 + 0.015, -0.24, 0.34)), V((x0 + 0.02, -0.27, 0.31))]
    fingers.append(tube(pts, r=[0.012, 0.011, 0.009, 0.0], seg=3, material=bone, smooth=False))
fingers.append(tube([V((0.0, -0.12, 0.25)), V((-0.02, -0.2, 0.31)), V((-0.04, -0.24, 0.31))], r=[0.013, 0.011, 0.0], seg=3, material=bone, smooth=False))
join([base, band, lid] + hs + fingers, 'coffin')
report()
finish('haunted', 'coffin', kind='edge', footprint=0.62, notes='oude houten doodskist, deksel scheef open, paars satijn binnenin, benige vingers')
