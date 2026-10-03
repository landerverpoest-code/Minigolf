import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

green = mat('stem_green', '#3f8f2c', rough=0.8)
red = mat('petal_red', '#e8433a', rough=0.6)
purple = mat('petal_purple', '#9466d8', rough=0.6)
white = mat('petal_white', '#fbf6ee', rough=0.6)
yellow = mat('petal_yellow', '#ffcd2e', rough=0.5)

rnd = random.Random(7)
parts = []
# (x, y, hoogte, kleur, grootte)
fl = [(0.0, 0.0, 0.3, red, 1.1), (0.09, 0.06, 0.24, yellow, 0.9), (-0.08, 0.07, 0.26, purple, 1.0),
      (0.05, -0.09, 0.2, white, 1.0), (-0.1, -0.06, 0.18, red, 0.85), (0.13, -0.03, 0.15, purple, 0.8),
      (-0.03, 0.13, 0.21, white, 0.9), (0.02, -0.02, 0.12, yellow, 0.75)]
for i, (x, y, h, m, s) in enumerate(fl):
    lean = Vector((x, y, 0)) * 0.6
    top = Vector((x, y, 0)) + lean + Vector((0, 0, h))
    parts.append(rod((x * 0.5, y * 0.5, 0), top, 0.007, 0.005, verts=3, material=green))
    heart = yellow if m is not yellow else red
    f = flower_head(0.05 * s, 0.016 * s, 5, 0.014 * s, petal_mat=m, heart_mat=heart, both_sides=False)
    xform(f, rot=(0, 0, rnd.uniform(0, 72)))
    nrm = (Vector((x, y, 0)) * 1.2 + Vector((0, 0, 1))).normalized()
    orient(f, nrm, top)
    parts.append(f)
# bladeren rond de voet
for i in range(7):
    a = i * 360 / 7 + rnd.uniform(-15, 15)
    l = leaf(rnd.uniform(0.1, 0.14), 0.06, 0.01, material=green, droop=0.02)
    xform(l, rot=(rnd.uniform(25, 45), 0, 0))
    xform(l, rot=(0, 0, a))
    parts.append(l)
# grassprietjes
for i in range(5):
    a = i * 72 + 30
    g = leaf(rnd.uniform(0.14, 0.2), 0.02, 0.004, material=green)
    xform(g, rot=(65, 0, 0))
    xform(g, rot=(0, 0, a), loc=(0.03 * math.cos(math.radians(a)), 0.03 * math.sin(math.radians(a)), 0))
    parts.append(g)
join(parts, 'flower_patch')
report()
finish('meadow', 'flower_patch', kind='edge', footprint=0.18, notes='plukje van 8 bloemen (rood/geel/paars/wit) met stelen, blaadjes en grassprieten')
