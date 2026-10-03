import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

bark = mat('bark', '#6b4a30', rough=0.95)
dk = mat('cypress_dark', '#24502a', rough=0.85)
lt = mat('cypress_light', '#3a7438', rough=0.85)

parts = []
trunk = lathe([(0.2, 0), (0.13, 0.15), (0.11, 0.9)], seg=6, material=bark, cap_bottom=False)
parts.append(trunk)
# vlamvormige kroon: kern + gestapelde knobbelige lagen, afwisselend van tint
core = lathe([(0.3, 0.55), (0.62, 1.2), (0.66, 2.0), (0.55, 2.9), (0.38, 3.8), (0.18, 4.6), (0, 5.1)], seg=10, material=dk, cap_bottom=True)
lumpy(core, 0.13, 2.2, seed=2)
smooth(core, 60)
parts.append(core)
rnd = random.Random(6)
layers = [(1.0, 0.66), (1.7, 0.7), (2.45, 0.62), (3.2, 0.5), (3.95, 0.36)]
for k, (z, r) in enumerate(layers):
    nb = 2 if r > 0.4 else 1
    for j in range(nb):
        a = TAU * j / nb + k * 1.1
        rr = r * rnd.uniform(0.62, 0.75)
        b = ico(rr, sub=2, material=lt if (j + k) % 2 else dk, scale=(1, 1, 1.5))
        lumpy(b, rr * 0.18, 1.6 / rr, seed=k * 7 + j)
        xform(b, loc=(r * 0.55 * math.cos(a), r * 0.55 * math.sin(a), z + rnd.uniform(-0.1, 0.1)))
        smooth(b, 60)
        parts.append(b)
o = join(parts, 'cypress_tree')
xform(o, rot=(0, 2.5, 0))
report()
finish('castle', 'cypress_tree', kind='scatter', footprint=0.55, notes='hoge smalle cipres: vlamvormige kroon van knobbelige lagen in 2 donkergroene tinten, kort stammetje')
