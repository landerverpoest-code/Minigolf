import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_warm', '#a69c8f', rough=0.9)
wood = mat('wood', '#8a5a34', rough=0.85)
roofm = mat('roof_tile', '#a9452f', rough=0.75)
water = mat('water', '#2c5e93', rough=0.08)
iron = mat('iron', '#3d3d42', rough=0.5, metal=0.4)
FP = 0.75

rnd = random.Random(3)
def wedge(a0, a1, r0, r1, z0, z1, material):
    vs = []
    for z in (z0, z1):
        for (r, a) in ((r0, a0), (r1, a0), (r1, a1), (r0, a1)):
            vs.append((r * math.cos(a), r * math.sin(a), z))
    fs = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_obj(vs, fs, material, 'wedge')
parts = []
# twee lagen stenen blokken, verspringend, plus dekstenen
RI, RO = 0.5, 0.7
n = 9
for c, (z0, z1) in enumerate(((0.0, 0.32), (0.32, 0.62))):
    off = (0.5 if c else 0) * TAU / n
    for i in range(n):
        a0 = TAU * i / n + off + 0.012
        a1 = TAU * (i + 1) / n + off - 0.012
        d = rnd.uniform(-0.015, 0.02)
        w = wedge(a0, a1, RI, RO + d, z0 + 0.008, z1 - 0.008, stone)
        jitter(w, 0.008, seed=c * 20 + i)
        parts.append(w)
for i in range(n):
    a0 = TAU * (i + 0.25) / n + 0.01
    a1 = TAU * (i + 1.25) / n - 0.01
    parts.append(wedge(a0, a1, RI - 0.04, RO + 0.02, 0.62, 0.74, stone))
# binnenkant + water
parts.append(lathe([(RI - 0.01, 0.0), (RI - 0.01, 0.62)], seg=n * 2, material=stone, cap_bottom=False, cap_top=False))
parts[-1].data.polygons.foreach_set('use_smooth', [False] * len(parts[-1].data.polygons))
bm = bmesh.new(); bm.from_mesh(parts[-1].data); bmesh.ops.reverse_faces(bm, faces=bm.faces); bm.to_mesh(parts[-1].data); bm.free()
parts.append(cyl(RI - 0.01, 0.02, loc=(0, 0, 0.42), verts=n * 2, material=water))
# palen, dwarsbalk, dak
PX = 0.6
for sx in (-1, 1):
    parts.append(box((0.1, 0.12, 1.15), loc=(sx * PX, 0, 0.74 + 0.575), material=wood))
    # schoren
    parts.append(plank((sx * PX, 0, 1.75), (sx * PX, -0.25, 1.5), w=0.06, t=0.06, material=wood))
    parts.append(plank((sx * PX, 0, 1.75), (sx * PX, 0.25, 1.5), w=0.06, t=0.06, material=wood))
parts.append(box((1.36, 0.12, 0.1), loc=(0, 0, 1.92), material=wood))
for sy in (-1, 1):
    sl = box((1.62, 0.56, 0.05), material=roofm, bevel=0.012)
    xform(sl, rot=(sy * -38, 0, 0), loc=(0, sy * 0.22, 2.1))
    parts.append(sl)
parts.append(box((1.66, 0.09, 0.09), loc=(0, 0, 2.31), rot=(math.pi / 4, 0, 0), material=wood))
# windas met touw en emmer
parts.append(rod((-PX + 0.05, 0, 1.45), (PX - 0.05, 0, 1.45), 0.07, verts=8, material=wood))
parts.append(rod((PX, 0, 1.45), (PX + 0.15, 0, 1.45), 0.025, verts=5, material=iron))
parts.append(rod((PX + 0.15, 0, 1.45), (PX + 0.15, 0, 1.25), 0.02, verts=5, material=iron))
parts.append(rod((PX + 0.12, 0, 1.25), (PX + 0.27, 0, 1.25), 0.03, verts=5, material=wood))
parts.append(rod((0.05, -0.07, 1.42), (0.05, -0.07, 0.98), 0.012, verts=4, material=wood))
bucket = lathe([(0.1, 0.0), (0.13, 0.22)], seg=8, material=wood, cap_bottom=True, cap_top=False)
bk = [bucket]
for z in (0.04, 0.17):
    rr = 0.1 + 0.03 * z / 0.22 + 0.008
    bk.append(lathe([(rr, z - 0.015), (rr, z + 0.015)], seg=8, material=iron, cap_bottom=False, cap_top=False))
bk.append(torus(0.12, 0.008, loc=(0, 0, 0.22), rot=(math.pi / 2, 0, 0), seg=8, ring=3, material=iron))
b = join(bk, 'bucket')
bpy.data.objects['bucket'].data.polygons.foreach_set('use_smooth', [False] * len(b.data.polygons))
xform(b, rot=(0, 0, 10), loc=(0.05, -0.07, 0.72))
parts.append(b)
o = join(parts, 'well')
smooth(o, 35)
report()
mr = max(Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z < 0.6)
print('MAXR', round(mr, 3))
finish('castle', 'well', kind='post', footprint=FP, notes='stenen waterput (blokken in verspringende lagen, voet binnen r=0.75), water, houten palen met pannendakje, windas met touw en emmer')
