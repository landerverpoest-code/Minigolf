import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
moon = mat('moon_rock', '#8f9098', rough=0.95)
crat = mat('moon_crater', '#45474f', rough=1.0)
V = Vector
r = rock(0.7, sub=2, material=moon, scale=(0.85, 0.72, 2.1), jit=0.12, seed=21)
deform(r, lambda v: V((v.x + 0.14 * max(0, v.z) ** 1.5, v.y, v.z)))
chop(r, 6, seed=8, depth=(0.8, 0.93), minz=-0.3)
r2 = rock(0.45, loc=(0.8, 0.3, 0), sub=2, material=moon, scale=(1.3, 1.1, 0.75), jit=0.08, seed=22)
chop(r2, 4, seed=9, depth=(0.75, 0.9), minz=0.2)
P = [r, r2]
for (d, rc, sp) in [((0.2, -1, 0.15), 0.2, 0.3), ((-0.8, -0.5, 0.5), 0.16, 0.9), ((0.3, 0.9, -0.1), 0.18, 0.1)]:
    P.append(place_on(crater(rc, moon, crat, seg=8, h=0.028), r, d, center=(0.05, 0, 0.75), sink=0.01, spin=sp))
P.append(place_on(crater(0.17, moon, crat, seg=8, h=0.028), r2, (0.1, -0.4, 1), center=(0.8, 0.3, 0.1), sink=0.01))
for (x, y, s, sd) in [(-0.75, -0.4, 0.22, 5), (0.4, -0.8, 0.14, 6), (-0.4, 0.62, 0.12, 8)]:
    P.append(chop(rock(s, loc=(x, y, 0), sub=1, material=moon, scale=(1.2, 1, 0.7), jit=0.2, seed=sd), 2, seed=sd))
join(P, 'moon_rock_b')
report()
finish('space', 'moon_rock_b', kind='scatter', footprint=0.95, notes='hoge scheve gefacetteerde maanrots + kraterrots en kiezels')
