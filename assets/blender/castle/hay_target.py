import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/castle'); from _deco import *

HAY = mat('hay', '#e2bf58', rough=0.95)
WOOD = mat('wood_dark', '#6e4528', rough=0.85)
RED = mat('banner_red', '#c0392f', rough=0.8)
CREAM = mat('cloth_cream', '#f1e6c8', rough=0.85)
GOLD = mat('gold', '#e3b23c', rough=0.35, metal=0.4)

# schuine houten bok (3 poten)
for p0, p1 in (((-0.32, 0.0, 0), (-0.2, 0.1, 0.95)), ((0.32, 0.0, 0), (0.2, 0.1, 0.95)), ((0, 0.5, 0), (0, 0.15, 0.9))):
    plank(p0, p1, w=0.05, t=0.05, material=WOOD)
plank((-0.34, 0.03, 0.25), (0.34, 0.03, 0.25), w=0.04, t=0.04, material=WOOD)
# strooien schijf (rond, licht naar achter gekanteld) met roos aan de voorkant
disc = lathe([(0.4, -0.06), (0.42, 0.0), (0.4, 0.06)], verts=12, material=HAY, cap0=True, cap1=False)
face = lathe([(0.4, 0.06), (0.31, 0.065), (0.31, 0.065), (0.21, 0.07), (0.21, 0.07), (0.11, 0.075), (0.11, 0.075), (0.0, 0.08)],
             verts=12, mats=[HAY, CREAM, RED, GOLD], band_mats=[1, 2, 1, 3, 3, 3, 3], cap0=False, cap1=False)
recolor(face, [HAY, CREAM, RED, GOLD], lambda f: (1 if math.hypot(f.center.x, f.center.y) > 0.31 else 2 if math.hypot(f.center.x, f.center.y) > 0.21 else 1 if math.hypot(f.center.x, f.center.y) > 0.11 else 3))
for o in (disc, face):
    T(o, rot=(90 - 12, 0, 0), loc=(0, -0.05, 0.62))
# pijlen in de roos
for k, (x, z, ax, az) in enumerate(((0.06, 0.66, -8, 10), (-0.17, 0.52, 6, -14))):
    tip = Vector((x, -0.11 - (z - 0.62) * 0.2, z))
    d = Vector((math.sin(math.radians(az)), -1, math.sin(math.radians(ax)))).normalized()
    tail = tip + d * 0.42
    rod(tip, tail, r=0.009, verts=3, material=WOOD)
    for s in (-1, 1):
        mesh_obj([tail - d * 0.02, tail - d * 0.12, tail - d * 0.04 + Vector((s * 0.035, 0, 0.02))], [(0, 1, 2)], RED, 'fletch')
o = join_all('hay_target')
report()
done('castle', 'hay_target', kind='edge', footprint=0.42,
     notes='Boogschietdoel: ronde strooien schijf met rood-witte ringen en gouden roos op een houten driepoot, twee pijlen met rode veren')
