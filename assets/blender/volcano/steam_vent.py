import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
sulfur = mat('sulfur', '#d8c040', rough=0.8)
lava = mat('glow_lava', '#ff7a10', rough=0.5, emit='#ff5000', emit_strength=4.0)

# kegeltje met ondiepe krater; gloeiende opening; zwavelkorstjes op de rand
seg = 9
cone_ = lathe([(0.3, 0.0), (0.24, 0.14), (0.15, 0.32), (0.12, 0.37), (0.09, 0.36), (0.075, 0.31)], seg=seg, material=basalt, cap_bottom=False, cap_top=False)
jitter(cone_, 0.015, seed=2)
cone_.data.materials.append(basalt_l)
cone_.data.materials.append(sulfur)
for p in cone_.data.polygons:
    if p.center.z > 0.33:
        p.material_index = 2 if p.index % 4 == 1 else 1
parts = [cone_]
glow = lathe([(0.085, 0.31), (0.04, 0.325), (0, 0.33)], seg=seg, material=lava, cap_bottom=False)
parts.append(glow)
# gloeiende stroompjes over de rand naar beneden
tree = surf_tree(cone_)
parts += crack_ribbon(tree, (0.05, -0.12, 0.36), (0.1, -0.5, -1), length=0.3, width=0.035, steps=4, seed=1, material=lava, lift=0.008, wiggle=0.4)
parts += crack_ribbon(tree, (0.13, 0.02, 0.35), (1, 0.1, -1), length=0.22, width=0.03, steps=3, seed=6, material=lava, lift=0.008, wiggle=0.4)
# steentjes rondom
for k, (a, d, r) in enumerate(((0.3, 0.32, 0.06), (3.6, 0.32, 0.065))):
    c = chunk(r, (1.3, 1, 0.8), cuts=4, seed=k + 3, material=basalt_l if k % 2 else basalt, base_sub=1)
    xform(c, loc=(d * math.cos(a), d * math.sin(a), r * 0.3))
    parts.append(c)
o = join(parts, 'steam_vent')
xform(o, scale=1.45)
report()
finish('volcano', 'steam_vent', kind='edge', footprint=0.5, notes='rotskegeltje met gloeiende opening (glow_lava), zwavelkorstjes op de rand, lavastroompjes over de flank')
