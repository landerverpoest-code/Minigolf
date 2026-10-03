import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

bark = mat('birch_bark', '#f1ede4', rough=0.7)
mark = mat('birch_mark', '#2a2622', rough=0.9)
leaf_a = mat('leaf_birch', '#6fae2e', rough=0.8)
leaf_b = mat('leaf_birch_light', '#9ccb3f', rough=0.8)

def tx(z):  # stam-x op hoogte z (lichte S-bocht)
    return 0.16 * math.sin(z * 0.75)

parts = []
# slanke witte stam; dunne ringen worden donkere horizontale streepjes
H = 4.5
marks_z = [0.4, 0.95, 1.4, 1.9, 2.45, 3.1]
zs = sorted(set([0.0, 0.12, H] + [m for m in marks_z] + [m + 0.07 for m in marks_z]))
prof = [(0.19 if z == 0 else 0.15 - 0.09 * (z / H), z) for z in zs]
trunk = lathe(prof, seg=6, material=bark, cap_bottom=False)
trunk.data.materials.append(mark)
rnd = random.Random(5)
for p in trunk.data.polygons:
    zc = p.center.z
    for m in marks_z:
        if m < zc < m + 0.07 and rnd.random() < 0.55:
            p.material_index = 1
# een paar grotere donkere plekken
for p in trunk.data.polygons:
    if p.material_index == 0 and 0.15 < p.center.z < 0.35 and rnd.random() < 0.5:
        p.material_index = 1
bend(trunk, lambda c: (c.x + tx(c.z), c.y, c.z))
smooth(trunk, 60)
parts.append(trunk)

# takken met bladclusters aan de uiteinden (luchtig, takken blijven zichtbaar)
blobs = []
for i, (a, z0, L, up) in enumerate(((15, 2.5, 0.72, 0.6), (135, 2.7, 0.7, 0.7), (250, 2.95, 0.68, 0.65), (75, 3.35, 0.6, 0.6), (195, 3.65, 0.55, 0.55))):
    ra = math.radians(a)
    p0 = Vector((tx(z0), 0, z0))
    p1 = p0 + Vector((L * math.cos(ra), L * math.sin(ra), up))
    parts.append(rod(p0, p1, 0.045, 0.018, verts=4, material=bark))
    blobs.append((p1.x, p1.y, p1.z + 0.05, 0.6 - 0.03 * i, i % 2))
blobs += [(tx(3.9) - 0.1, -0.15, 3.95, 0.62, 0), (tx(4.6) + 0.05, 0.1, 4.6, 0.5, 1), (tx(3.3)-0.1, 0.35, 3.3, 0.5, 0)]
for i, (x, y, z, r, l) in enumerate(blobs):
    b = ico(r, sub=2, material=leaf_b if l else leaf_a, scale=(1.05, 1.05, 1.1))
    lumpy(b, r * 0.25, 1.4 / r, seed=i * 3 + 7)
    # licht hangend: onderkant iets naar beneden getrokken
    bend(b, lambda c, r=r: (c.x * (1 - 0.15 * max(0, -c.z / r)), c.y * (1 - 0.15 * max(0, -c.z / r)), c.z * (1.25 if c.z < 0 else 1)))
    xform(b, loc=(x, y, z), rot=(0, 0, i * 41))
    smooth(b, 55)
    parts.append(b)

join(parts, 'birch_tree')
report()
finish('meadow', 'birch_tree', kind='scatter', footprint=0.35, notes='berk: witte stam met donkere streepjes, lichte luchtige kruin aan zichtbare takken')
