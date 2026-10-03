import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood', '#8a5a34', rough=0.85)
iron = mat('iron', '#8f949c', rough=0.35, metal=0.5)
red = mat('banner_red', '#c0392f', rough=0.8)
blue = mat('banner_blue', '#2f58ad', rough=0.8)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)

parts = []
# rek: staanders met voetjes, twee liggers
for sx in (-1, 1):
    parts.append(box((0.08, 0.08, 1.05), loc=(sx * 0.55, 0.1, 0.525), material=wood))
    parts.append(box((0.1, 0.5, 0.07), loc=(sx * 0.55, 0.1, 0.035), material=wood))
parts.append(box((1.24, 0.1, 0.07), loc=(0, 0.1, 0.98), material=wood))
parts.append(box((1.18, 0.07, 0.06), loc=(0, 0.1, 0.35), material=wood))
# speren, schuin tegen de bovenste ligger
for k, x in enumerate((-0.35, 0.0, 0.32)):
    b = Vector((x - 0.05, 0.32, 0.0)); t = Vector((x + 0.03, 0.02, 1.55 - 0.08 * k))
    d = (t - b).normalized()
    parts.append(rod(b, t, 0.018, verts=4, material=wood))
    hd = cone(0.045, 0.2, verts=4, material=iron)
    xform(hd, scale=(1.0, 0.35, 1.0))
    q = d.to_track_quat('Z', 'Y')
    hd.data.transform(q.to_matrix().to_4x4()); xform(hd, loc=t + d * 0.1)
    parts.append(hd)
# zwaard in het rek
parts.append(prism([(-0.025, 0), (0.025, 0), (0.02, -0.62), (0, -0.68), (-0.02, -0.62)], 0.012, material=iron))
xform(parts[-1], rot=(0, 0, 0), loc=(0.48, 0.0, 1.1))
parts.append(box((0.16, 0.03, 0.03), loc=(0.48, 0.0, 1.11), material=gold))
parts.append(rod((0.48, 0, 1.12), (0.48, 0, 1.24), 0.015, verts=4, material=wood))
# twee ronde schilden met kwartier-indeling, gouden rand en knop
def shield(m1, m2, r=0.3):
    o = lathe([(0, 0.025), (r * 0.85, 0.025), (r, 0.012), (r, -0.02), (0, -0.02)], seg=8, material=m1, cap_bottom=False, cap_top=False)
    o.data.materials.append(m2); o.data.materials.append(gold)
    for p in o.data.polygons:
        c = p.center
        rr = Vector((c.x, c.y)).length
        if rr > r * 0.86 and c.z > -0.01:
            p.material_index = 2
        elif c.z > 0:
            a = math.atan2(c.y, c.x)
            p.material_index = int(((a + math.pi) / (math.pi / 2))) % 2
    boss = cone(0.07, 0.06, loc=(0, 0, 0.055), verts=6, material=gold)
    return join([o, boss], 'shield')
s1 = shield(red, gold)
xform(s1, rot=(72, 0, 8), loc=(-0.28, -0.12, 0.31))
s2 = shield(blue, gold, r=0.27)
xform(s2, rot=(76, 0, -12), loc=(0.3, -0.1, 0.28))
parts += [s1, s2]
o = join(parts, 'weapon_rack')
report()
finish('castle', 'weapon_rack', kind='edge', footprint=0.6, notes='houten wapenrek met 3 speren, een zwaard en 2 ronde schilden (rood/goud en blauw/goud met gouden knop)')
