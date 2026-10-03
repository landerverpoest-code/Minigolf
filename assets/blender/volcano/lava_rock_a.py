import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
ash = mat('ash', '#7d7570', rough=1.0)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
lava = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff4800', emit_strength=3.0)

# hoge gekartelde spits met twee kleinere brokken
parts = []
spire = chunk(0.6, (0.9, 0.8, 2.4), cuts=16, seed=4, material=basalt, flat_bottom=0.75, depth=(0.4, 0.8), base_sub=1)
taper(spire, 0.55)
xform(spire, rot=(4, -6, 15), loc=(0, 0, 1.0))
parts.append(spire)
b2 = chunk(0.45, (1.1, 1.0, 1.3), cuts=11, seed=9, material=basalt_l, flat_bottom=0.5, depth=(0.45, 0.8), base_sub=1)
xform(b2, rot=(0, 12, 40), loc=(0.55, -0.25, 0.45))
parts.append(b2)
b3 = chunk(0.3, (1.2, 1.0, 0.8), cuts=9, seed=12, material=basalt, flat_bottom=0.4, depth=(0.45, 0.8), base_sub=1)
xform(b3, rot=(0, 0, 10), loc=(-0.5, -0.35, 0.18))
parts.append(b3)
sp2 = chunk(0.35, (0.8, 0.8, 2.6), cuts=12, seed=21, material=basalt_l, flat_bottom=0.7, depth=(0.4, 0.8), base_sub=1)
taper(sp2, 0.4)
xform(sp2, rot=(-14, -20, 30), loc=(-0.35, 0.3, 0.75))
parts.append(sp2)
# gloeiende scheuren over de spits
tree = surf_tree(spire)
parts += crack_ribbon(tree, (0.3, -0.5, 0.3), (0.1, 0, 1), length=1.6, width=0.06, steps=12, seed=3, material=lava, branch=2)
parts += crack_ribbon(tree, (-0.4, -0.3, 1.3), (0.2, -0.3, 1), length=0.8, width=0.045, steps=7, seed=8, material=lava, branch=1)
tree2 = surf_tree(b2)
parts += crack_ribbon(tree2, (0.6, -0.8, 0.9), (1, 0.2, -0.3), length=0.6, width=0.045, steps=6, seed=5, material=lava)
for o in (spire, b2, b3, sp2):
    dust(o, ash, 0.6)
join(parts, 'lava_rock_a')
report()
finish('volcano', 'lava_rock_a', kind='scatter', footprint=0.75, notes='hoge gekartelde basaltspits met 2 brokken en gloeiende scheuren (glow_lava)')
