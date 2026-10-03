import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
ash = mat('ash', '#7d7570', rough=1.0)
lava = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff4800', emit_strength=3.0)
FP = 0.45

# stevig blok basalt dat binnen de botsstraal blijft
main = chunk(0.55, (0.95, 0.92, 1.05), cuts=18, seed=77, material=basalt, flat_bottom=0.6, depth=(0.6, 0.9), base_sub=2)
zs = [v.co.z for v in main.data.vertices]
xform(main, loc=(0, 0, -min(zs)))
# bovenop een kleiner, schuin brok (karakter)
top = chunk(0.26, (0.6, 1.1, 1.5), cuts=9, seed=81, material=basalt_l, flat_bottom=0.5, base_sub=1)
xform(top, rot=(18, -22, 30), loc=(-0.22, 0.2, 0.55))
parts = [main, top]
tree = surf_tree(main)
parts += crack_ribbon(tree, (0.2, -0.45, 0.6), (0.3, 0.1, -1), length=0.6, width=0.045, steps=7, seed=5, material=lava, branch=1)
parts += crack_ribbon(tree, (-0.3, -0.35, 0.75), (-0.2, 0, -1), length=0.45, width=0.035, steps=5, seed=12, material=lava)
parts += crack_ribbon(tree, (0.42, 0.1, 0.5), (0, 1, -0.6), length=0.4, width=0.035, steps=5, seed=19, material=lava)
for o in (main, top):
    dust(o, ash, 0.7)
o = join(parts, 'rock_post')
# alles onder 0.6 m binnen de straal houden (met wat marge)
for v in o.data.vertices:
    d = Vector((v.co.x, v.co.y)).length
    lim = FP - 0.015 if v.co.z < 0.65 else FP + 0.03
    if d > lim:
        v.co.x *= lim / d; v.co.y *= lim / d
report()
mr = max(Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z < 0.6)
print('MAXR', round(mr, 3))
finish('volcano', 'rock_post', kind='post', footprint=FP, notes='stevige vulkanische kei (binnen r=0.45) met schuin brok erop, as op de toppen en gloeiende scheuren')
