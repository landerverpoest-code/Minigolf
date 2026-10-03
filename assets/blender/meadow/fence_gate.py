import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood_warm', '#a8733e', rough=0.85)
wood_d = mat('wood_weathered', '#87592f', rough=0.9)
metal = mat('iron', '#3a3836', rough=0.6, metal=0.3)
grass = mat('grass', '#4f9c33', rough=0.85)

rnd = random.Random(3)
parts = []
# palen met puntdakje
for i, x in enumerate((-1.5, -0.62, 0.62, 1.5)):
    big = abs(x) < 1
    w = 0.14 if big else 0.12
    h = 1.12 if big else 1.0
    p = box((w, w, h), loc=(x, 0, h / 2), rot=(0, 0, math.radians(rnd.uniform(-4, 4))), material=wood_d, bevel=0.015)
    jitter(p, 0.006, seed=i)
    parts.append(p)
    c = cone(w * 0.78, 0.09, loc=(x, 0, h + 0.045), verts=4, rot=(0, 0, math.radians(45)), material=wood_d)
    parts.append(c)
    # graspluk aan de voet
    for k in range(4):
        a = k * 90 + rnd.uniform(0, 50)
        g = leaf(rnd.uniform(0.22, 0.32), 0.07, 0.015, material=grass)
        xform(g, rot=(rnd.uniform(40, 60), 0, a - 90), loc=(x + 0.06 * math.cos(math.radians(a)), 0.06 * math.sin(math.radians(a)), 0))
        parts.append(g)
# liggers van de zijstukken, licht scheef (rustiek)
for (x0, x1) in ((-1.5, -0.62), (0.62, 1.5)):
    for z in (0.38, 0.78):
        dz = rnd.uniform(-0.04, 0.04)
        parts.append(plank((x0 - 0.04, 0.075, z - dz), (x1 + 0.04, 0.075, z + dz), w=0.11, t=0.04, up=(0, 1, 0), material=wood, bevel=0.008))
# hek (licht open), scharnier bij x=-0.55
gate = []
gx0, gx1 = -0.53, 0.53
for z in (0.25, 0.85):
    gate.append(plank((gx0, -0.02, z), (gx1, -0.02, z), w=0.1, t=0.04, up=(0, 1, 0), material=wood, bevel=0.008))
for k in range(5):
    x = gx0 + 0.08 + k * (gx1 - gx0 - 0.16) / 4
    top = 0.98 - 0.08 * abs(k - 2) / 2 + 0.04
    pl = plank((x, 0.02, 0.12), (x, 0.02, top), w=0.13, t=0.03, up=(0, 1, 0), material=wood if k % 2 else wood_d, bevel=0.006)
    gate.append(pl)
gate.append(plank((gx0 + 0.06, -0.035, 0.3), (gx1 - 0.06, -0.035, 0.8), w=0.09, t=0.03, up=(0, 1, 0), material=wood_d, bevel=0.006))
# scharnieren en klink
for z in (0.25, 0.85):
    gate.append(box((0.2, 0.012, 0.035), loc=(gx0 + 0.07, -0.05, z), material=metal))
gate.append(box((0.12, 0.02, 0.03), loc=(gx1 - 0.02, -0.05, 0.6), material=metal))
g = join(gate, 'gate')
xform(g, loc=(0.55, 0, 0)); xform(g, rot=(0, 0, 18)); xform(g, loc=(-0.55, 0, 0))
parts.append(g)
smooth(join(parts, 'fence_gate'), 50)
report()
finish('meadow', 'fence_gate', kind='scatter', footprint=1.5, notes='rustiek houten hekwerk (3 m) met half open poortje, ijzeren scharnieren en grasplukjes')
