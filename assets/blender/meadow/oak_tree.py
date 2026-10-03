import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

bark = mat('bark', '#6e4a2c', rough=0.95)
leaf_d = mat('leaf_dark', '#2f7d27', rough=0.85)
leaf_l = mat('leaf_light', '#68b02c', rough=0.8)

parts = []
# stam met wortelvoet, licht gebogen
trunk = lathe([(0.44, 0), (0.32, 0.12), (0.25, 0.45), (0.21, 1.2), (0.19, 1.75), (0.12, 2.6)], seg=7, material=bark, cap_bottom=False)
lumpy(trunk, 0.035, 2.0, seed=3)
bend(trunk, lambda c: (c.x + 0.04 * max(c.z, 0) ** 1.5, c.y, c.z))
smooth(trunk, 70)
parts.append(trunk)
# wortels
for i, a in enumerate((20, 140, 255)):
    ra = math.radians(a)
    parts.append(rod((0.12 * math.cos(ra), 0.12 * math.sin(ra), 0.2), (0.6 * math.cos(ra), 0.6 * math.sin(ra), -0.03), 0.11, 0.035, verts=4, material=bark))
# dikke takken (vork) die zichtbaar de kruin in lopen
for (a, z0, L, up, r0) in ((20, 1.5, 1.05, 1.15, 0.11), (165, 1.65, 1.0, 1.2, 0.1), (280, 1.85, 0.8, 1.0, 0.08)):
    ra = math.radians(a)
    p0 = Vector((0.06, 0, z0))
    p1 = p0 + Vector((L * math.cos(ra), L * math.sin(ra), up))
    parts.append(rod(p0, p1, r0, r0 * 0.45, verts=5, material=bark))
    p2 = p0 + (p1 - p0) * 0.5
    p3 = p2 + Vector((0.42 * math.cos(ra + 1.0), 0.42 * math.sin(ra + 1.0), 0.3))
    parts.append(rod(p2, p3, r0 * 0.5, r0 * 0.22, verts=4, material=bark))

# kruin: gelaagde klodders, donker onder/binnen, licht boven
blobs = [
    (0.0, 0.0, 3.25, 1.2, 0),
    (1.05, 0.3, 2.95, 0.85, 0),
    (-0.9, 0.55, 3.0, 0.88, 0),
    (-0.15, -1.0, 2.9, 0.82, 0),
    (0.55, -0.45, 3.75, 0.85, 1),
    (-0.6, -0.3, 3.8, 0.78, 1),
    (0.25, 0.65, 3.9, 0.8, 1),
    (0.05, 0.0, 4.35, 0.62, 1),
]
for i, (x, y, z, r, l) in enumerate(blobs):
    b = ico(r, loc=(0, 0, 0), sub=2, material=leaf_l if l else leaf_d, scale=(1, 1, 0.8))
    lumpy(b, r * 0.2, 1.5 / r, seed=i * 5 + 1)
    # onderkant iets afvlakken (cartoon-wolkje)
    bend(b, lambda c, r=r: (c.x, c.y, max(c.z, -0.45 * r) if c.z < 0 else c.z))
    xform(b, loc=(x, y, z), rot=(0, 0, i * 37))
    smooth(b, 55)
    parts.append(b)

tree = join(parts, 'oak_tree')
report()
finish('meadow', 'oak_tree', kind='scatter', footprint=0.55, notes='eik: gelaagde kruin in 2 groentinten, stam met wortels en takken')
