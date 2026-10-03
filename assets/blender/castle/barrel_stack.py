import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood', '#9a6538', rough=0.8)
wood_d = mat('wood_dark', '#7c4e2b', rough=0.85)
lidm = mat('wood_light', '#c08c55', rough=0.8)
iron = mat('iron', '#3d3d42', rough=0.5, metal=0.4)
brass = mat('gold', '#e3b23c', rough=0.35, metal=0.4)

def barrel(r=0.3, h=0.78, seed=0, seg=10):
    zs = [0.0, 0.1 * h, 0.5 * h, 0.9 * h, h]
    rs = [r * 0.84, r * 0.93, r, r * 0.93, r * 0.84]
    prof = list(zip(rs, zs)) + [(r * 0.78, h), (r * 0.78, h - 0.025)]
    o = lathe(prof, seg=seg, material=wood, cap_bottom=True, cap_top=True)
    o.data.materials.append(wood_d); o.data.materials.append(lidm)
    for p in o.data.polygons:
        c = p.center
        if p.normal.z > 0.9 and c.z > h * 0.9:
            p.material_index = 2
        elif abs(p.normal.z) < 0.6:
            a = math.atan2(c.y, c.x)
            p.material_index = (int((a + math.pi) / TAU * seg) % 2)
    smooth(o, 30)
    parts = [o]
    for zf in (0.12, 0.88):
        z = zf * h
        rr = (r * 0.93 + (r - r * 0.93) * (1 - abs(zf - 0.5) / 0.4 * 0.0)) + 0.012
        rr = r * (0.84 + (1 - 0.84) * (1 - ((z - 0.5 * h) / (0.5 * h)) ** 2)) + 0.012
        parts.append(lathe([(rr, z - 0.025), (rr, z + 0.025)], seg=seg, material=iron, cap_bottom=False, cap_top=False))
    return join(parts, 'barrel')

parts = []
b1 = barrel(seed=1); xform(b1, rot=(0, 0, 10), loc=(-0.31, 0.0, 0)); parts.append(b1)
b2 = barrel(seed=2); xform(b2, rot=(0, 0, 40), loc=(0.31, 0.05, 0)); parts.append(b2)
# liggend vat bovenop, met kraantje
b3 = barrel(r=0.27, h=0.72, seed=3)
xform(b3, loc=(0, 0, -0.36)); xform(b3, rot=(0, 90, 8), loc=(0.0, 0.02, 0.78 + 0.25))
parts.append(b3)
tap = rod((0.36, -0.01, 1.03), (0.45, -0.01, 1.03), 0.025, verts=6, material=brass)
parts.append(tap)
parts.append(rod((0.44, -0.01, 1.03), (0.44, -0.01, 0.97), 0.018, verts=5, material=brass))
# klein vaatje liggend voor de stapel
b4 = barrel(r=0.2, h=0.45, seed=4, seg=8)
xform(b4, loc=(0, 0, -0.225)); xform(b4, rot=(90, 0, 25), loc=(0.15, -0.55, 0.19))
parts.append(b4)
o = join(parts, 'barrel_stack')
report()
finish('castle', 'barrel_stack', kind='scatter', footprint=0.75, notes='stapel van 4 houten vaten (duigen in 2 tinten, ijzeren hoepels, lichte deksels), liggend vat met koperen kraantje')
