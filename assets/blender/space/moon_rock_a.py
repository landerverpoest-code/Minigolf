import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
moon = mat('moon_rock', '#8f9098', rough=0.95)
crat = mat('moon_crater', '#45474f', rough=1.0)
dust = mat('moon_dust', '#7a7c86', rough=1.0)
V = Vector
r = rock(0.75, sub=2, material=moon, scale=(1.3, 1.05, 0.75), jit=0.1, seed=7)
chop(r, 7, seed=3, depth=(0.78, 0.92), minz=0.0)
P = [r]
for (d, rc, sp) in [((0.25, -0.5, 1), 0.26, 0.2), ((-0.75, -0.2, 0.55), 0.2, 0.5), ((0.6, 0.4, 0.6), 0.16, 0.1), ((0.8, -0.5, 0.25), 0.13, 0.7)]:
    P.append(place_on(crater(rc, moon, crat, seg=8, h=0.04), r, d, center=(0, 0, 0.1), sink=0.01, spin=sp))
for (x, y, s, sd) in [(1.0, -0.55, 0.16, 1), (-0.95, -0.5, 0.12, 2), (0.3, 0.88, 0.1, 3)]:
    P.append(chop(rock(s, loc=(x, y, 0), sub=1, material=moon, scale=(1.2, 1, 0.7), jit=0.2, seed=sd), 2, seed=sd))
for o in [o for o in P if not o.name.startswith('lathe')]:
    rnd = random.Random(1 + len(o.data.polygons))
    set_mat(o, dust, lambda c, n: rnd.random() < 0.3 and n.z > -0.5)
join(P, 'moon_rock_a')
report()
finish('space', 'moon_rock_a', kind='scatter', footprint=0.95, notes='gefacetteerde maanrots met kraters (geometrie) en kiezels')
