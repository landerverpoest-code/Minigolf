import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
crimson = mat('crimson', '#b0213a', rough=0.6)
purple = mat('royal_purple', '#5b2a86', rough=0.6)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
steel = mat('steel', '#c9ccd6', rough=0.3, metal=0.3)
V = Vector
P = []
B = []
bag = lathe([(0.175, 0.0), (0.175, 0.12), (0.165, 0.72), (0.19, 0.82)], seg=8, material=crimson, cap_top=False)
set_mat(bag, gold, lambda c, n: (c.z < 0.12 and n.z > -0.5) or c.z > 0.72)
B.append(bag)
B.append(lathe([(0.17, 0.8), (0.0, 0.8)], seg=8, material=purple, cap_top=False, cap_bot=False))
B.append(box((0.2, 0.08, 0.32), loc=(0, -0.19, 0.42), material=purple, bevel=0.02))
B.append(box((0.16, 0.02, 0.03), loc=(0, -0.235, 0.5), material=gold))
B.append(tube([V((0.12, 0.13, 0.7)), V((0.2, 0.22, 0.5)), V((0.18, 0.2, 0.25)), V((0.12, 0.14, 0.15))], r=0.025, seg=3, material=purple, smooth=False))
# clubs
for (x, y, h, kind) in [(-0.07, 0.04, 0.42, 'cover'), (0.07, 0.06, 0.38, 'cover'), (0.0, -0.08, 0.3, 'iron'), (-0.09, -0.06, 0.26, 'iron')]:
    B.append(cyl(0.012, h + 0.1, loc=(x, y, 0.8 + h / 2 - 0.05), verts=3, material=steel))
    top = V((x, y, 0.8 + h))
    if kind == 'cover':
        c = purple if x < 0 else crimson
        B.append(ico(0.075, loc=top, sub=1, material=c, smooth=True, scale=(1.0, 1.25, 0.9)))
        B.append(ico(0.035, loc=top + V((0, 0, 0.075)), sub=1, material=gold, smooth=True))
    else:
        B.append(box((0.09, 0.025, 0.05), loc=top + V((0.03, 0, 0)), rot=(0, 0.2, 0), material=steel))
bagobj = join(B, 'bag')
T(bagobj, rot=(math.radians(-12), 0, 0), pivot=(0, 0, 0))
P.append(bagobj)
# standaard (2 pootjes)
for sx in (-1, 1):
    P.append(tube([V((sx * 0.1, 0.12, 0.55)), V((sx * 0.22, 0.42, 0.0))], r=0.012, seg=3, material=steel, smooth=False))
join(P, 'golf_bag')
report()
finish('finale', 'golf_bag', kind='edge', footprint=0.35, notes='rood/gouden golftas op standaard met clubs en hoofdhoesjes')
