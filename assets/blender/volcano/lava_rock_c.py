import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
ash = mat('ash', '#7d7570', rough=1.0)
lava = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff4800', emit_strength=3.0)

# groepje scherpe, schuin opstekende scherven met een klein gloeiend gat aan de voet
parts = []
spec = [(0.0, 0.0, 0.32, (0.8, 0.7, 2.2), (12, -8, 0), 0), (0.32, -0.12, 0.25, (0.8, 0.8, 1.7), (-10, 22, 40), 1),
        (-0.3, -0.1, 0.22, (0.9, 0.8, 1.5), (16, -24, 70), 0), (0.08, 0.3, 0.2, (0.9, 0.9, 1.3), (-20, 4, 15), 1),
        (-0.15, -0.38, 0.14, (1.1, 1.0, 0.9), (0, 0, 30), 1)]
for k, (x, y, r, sc, rot, l) in enumerate(spec):
    c = chunk(r, sc, cuts=10, seed=50 + k * 3, material=basalt_l if l else basalt, flat_bottom=0.6, depth=(0.4, 0.8), base_sub=1)
    taper(c, 0.45)
    zs = [v.co.z for v in c.data.vertices]
    xform(c, loc=(0, 0, -min(zs) - 0.05))
    xform(c, rot=rot, loc=(x, y, 0))
    dust(c, ash, 0.6)
    parts.append(c)
# gloeiende plas tussen de voeten
pool = lathe([(0.17, 0.0), (0.15, 0.04), (0, 0.045)], seg=7, material=lava)
jitter(pool, 0.02, seed=3, axes=(1, 1, 0))
xform(pool, loc=(0.05, -0.2, 0))
parts.append(pool)
tree = surf_tree(parts[0])
parts += crack_ribbon(tree, (0.05, -0.25, 0.3), (0, 0, 1), length=0.5, width=0.035, steps=6, seed=2, material=lava)
join(parts, 'lava_rock_c')
report()
finish('volcano', 'lava_rock_c', kind='scatter', footprint=0.5, notes='groepje scherpe basaltscherven met as op de toppen en een klein gloeiend lavaplasje')
