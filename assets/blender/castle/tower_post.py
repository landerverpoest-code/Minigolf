import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_warm', '#a69c8f', rough=0.9)
stone_d = mat('stone_dark', '#867b6f', rough=0.9)
dark = mat('wood_dark', '#4a3220', rough=0.85)
blue = mat('banner_blue', '#2f58ad', rough=0.8)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)
FP = 1.1

rnd = random.Random(5)
SEG = 12
parts = []
# romp: beschoeide voet binnen r=1.1, rechte schacht
body = lathe([(1.07, 0.0), (1.0, 0.35), (0.93, 0.75), (0.92, 3.1)], seg=SEG, material=stone, cap_bottom=False, cap_top=True)
smooth(body, 30)
parts.append(body)
parts.append(lathe([(0.99, 0.72), (0.99, 0.84), (0.92, 0.88)], seg=SEG, material=stone_d, cap_bottom=True, cap_top=False))
# losse stenen
for k in range(10):
    a = rnd.uniform(0, TAU); z = rnd.uniform(1.0, 2.9)
    b = box((0.1, rnd.uniform(0.3, 0.45), rnd.uniform(0.18, 0.26)), material=stone_d if k % 3 == 0 else stone)
    xform(b, loc=(0.92, 0, z)); xform(b, rot=(0, 0, math.degrees(a)))
    parts.append(b)
# kraagstenen + borstwering (iets breder boven, ver boven 0.6 m)
for k in range(SEG):
    a = TAU * (k + 0.5) / SEG
    c = box((0.28, 0.2, 0.3), material=stone_d)
    bend(c, lambda v: (v.x, v.y, v.z + (0.15 * (v.x + 0.14) / 0.28 if v.z < 0 else 0)))
    xform(c, loc=(0.98, 0, 3.05)); xform(c, rot=(0, 0, math.degrees(a)))
    parts.append(c)
RP = 1.12
parts.append(lathe([(RP, 3.15), (RP, 3.6), (RP - 0.2, 3.6), (RP - 0.2, 3.2)], seg=SEG, material=stone, cap_bottom=False, cap_top=False))
parts.append(lathe([(RP + 0.03, 3.12), (RP + 0.03, 3.22), (0.9, 3.22)], seg=SEG, material=stone_d, cap_bottom=True, cap_top=False))
for k in range(8):
    a = TAU * k / 8
    m = box((0.2, 0.4, 0.38), material=stone)
    xform(m, loc=(RP - 0.1, 0, 3.6 + 0.19)); xform(m, rot=(0, 0, math.degrees(a)))
    parts.append(m)
# schietgaten
for (a, z) in ((-90, 1.9), (30, 2.4), (150, 1.6)):
    for (w, d, hh, dy, dz, m) in ((0.12, 0.1, 0.6, 0, 0, dark), (0.34, 0.12, 0.1, 0, 0.35, stone_d), (0.34, 0.12, 0.1, 0, -0.35, stone_d)):
        b = box((d, w, hh), material=m)
        xform(b, loc=(0.93, dy, z + dz)); xform(b, rot=(0, 0, a))
        parts.append(b)
# klein blauw vaandel met gouden ruit (hangt boven de 0.6 m)
ban = prism([(-0.28, 0), (0.28, 0), (0.28, -0.9), (0, -1.1), (-0.28, -0.9)], 0.04, material=blue)
xform(ban, loc=(0, 0, 0)); xform(ban, rot=(0, 0, 0), loc=(0, -RP - 0.04, 3.45))
parts.append(ban)
emb = prism([(0, 0.2), (0.15, 0), (0, -0.2), (-0.15, 0)], 0.03, material=gold)
xform(emb, loc=(0, -RP - 0.08, 2.85))
parts.append(emb)
parts.append(box((0.66, 0.08, 0.07), loc=(0, -RP - 0.07, 3.45), material=gold))
# vlaggenmast met wimpel
parts.append(rod((0, 0, 3.1), (0, 0, 4.9), 0.035, verts=5, material=dark))
parts.append(sphere(0.06, loc=(0, 0, 4.92), seg=6, rings=4, material=gold))
pen = prism([(0, 0), (0.7, 0.13), (0, 0.26)], 0.02, material=blue)
bend(pen, lambda c: (c.x, c.y + 0.05 * math.sin(c.x * 6), c.z))
xform(pen, loc=(0.03, 0, 4.55))
parts.append(pen)
o = join(parts, 'tower_post')
smooth(o, 30)
report()
mr = max(Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z < 0.6)
print('MAXR', round(mr, 3))
finish('castle', 'tower_post', kind='post', footprint=FP, notes='gedrongen ronde hoektoren (binnen r=1.1 tot 0.6 m), kraagstenen, kantelen, schietgaten, blauw vaandel met gouden ruit en wimpel')
