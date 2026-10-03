import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

red = mat('cloth_red', '#c0392f', rough=0.85)
cream = mat('cloth_cream', '#f1e6c8', rough=0.85)
blue = mat('banner_blue', '#2f58ad', rough=0.8)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)
dark = mat('wood_dark', '#4a3220', rough=0.85)

SEG = 16
R, WH = 1.5, 1.65
PH = math.pi / SEG
parts = []
# wand: gestreept, met deuropening vooraan
wall = lathe([(R, 0.0), (R * 0.99, WH * 0.5), (R, WH)], seg=SEG, material=red, cap_bottom=False, cap_top=False, phase=PH)
wall.data.materials.append(cream); wall.data.materials.append(dark)
def seg_idx(c):
    a = math.atan2(c.y, c.x)
    return int(((a - PH) % TAU) / TAU * SEG + 0.5) % SEG
for p in wall.data.polygons:
    i = seg_idx(p.center)
    a = math.atan2(p.center.y, p.center.x)
    if abs(a + math.pi / 2) < 0.25:
        p.material_index = 2   # opening (donker interieur)
    else:
        p.material_index = i % 2
parts.append(wall)
# dak: licht hol kegeldak, strepen lopen door
RZ = WH
roof = lathe([(R + 0.18, RZ - 0.05), (R * 0.75, RZ + 0.55), (R * 0.4, RZ + 1.05), (0.06, RZ + 1.5)], seg=SEG, material=red, cap_bottom=True, cap_top=True, phase=PH)
roof.data.materials.append(cream)
for p in roof.data.polygons:
    p.material_index = seg_idx(p.center) % 2
parts.append(roof)
# geschulpte rand (valance) in blauw en goud
for k in range(SEG):
    a = TAU * (k + 0.5) / SEG + PH
    sc = prism([(-0.28, 0), (0.28, 0), (0.22, -0.16), (0, -0.24), (-0.22, -0.16)], 0.03, material=blue if k % 2 else gold)
    xform(sc, rot=(0, 0, 90), loc=(R + 0.19, 0, RZ - 0.03))
    xform(sc, rot=(0, 0, math.degrees(a)))
    parts.append(sc)
# opengeslagen flappen bij de deur
for sx in (-1, 1):
    fl = prism([(0, 0), (sx * 0.4, 0), (sx * 0.03, 1.5)], 0.03, material=cream if sx > 0 else red)
    xform(fl, rot=(0, 0, sx * -12))
    xform(fl, loc=(sx * 0.3, -R + 0.0, 0.0))
    parts.append(fl)
# paal met gouden bol en wimpel
TOP = RZ + 1.5
parts.append(rod((0, 0, TOP - 0.05), (0, 0, TOP + 0.75), 0.035, verts=6, material=dark))
parts.append(sphere(0.09, loc=(0, 0, TOP + 0.04), seg=8, rings=5, material=gold))
parts.append(sphere(0.05, loc=(0, 0, TOP + 0.78), seg=6, rings=4, material=gold))
pen = prism([(0, 0), (0.9, 0.1), (0, 0.24)], 0.02, material=blue)
bend(pen, lambda c: (c.x, c.y + 0.07 * math.sin(c.x * 5), c.z))
xform(pen, loc=(0.03, 0, TOP + 0.45))
parts.append(pen)
# scheerlijnen met haringen
for k in range(4):
    a = TAU * (k + 0.5) / 4 + 0.2
    p0 = Vector(((R + 0.15) * math.cos(a), (R + 0.15) * math.sin(a), RZ - 0.1))
    p1 = Vector(((R + 0.9) * math.cos(a), (R + 0.9) * math.sin(a), 0.08))
    parts.append(rod(p0, p1, 0.012, verts=3, material=cream))
    parts.append(box((0.05, 0.05, 0.18), loc=p1 + Vector((0, 0, -0.02)), material=dark))
o = join(parts, 'tent_striped')
smooth(o, 40)
report()
finish('castle', 'tent_striped', kind='scatter', footprint=2.2, notes='rond toernooitent met rood/crème banen, blauw-gouden geschulpte rand, open deurflappen, gouden bol, blauwe wimpel en scheerlijnen')
