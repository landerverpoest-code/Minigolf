import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice'); from _deco import *

SNOW = mat('snow', '#f2f7ff', rough=0.7)
ICE = mat('ice', '#62d4f4', rough=0.12, emit='#1aa8e0', emit_strength=0.3)
WATER = mat('ice_water', '#123a5c', rough=0.05)
WOOD = mat('sled_wood', '#c08850', rough=0.75)
RED = mat('sled_red', '#d8323a', rough=0.45, metal=0.1)

rnd = random.Random(4)
# ijsvlakte (schijf) met sneeuwrand
floe = lathe([(1.0, 0.0), (0.98, 0.05), (0.9, 0.07), (0.0, 0.07)], verts=12, material=ICE, sx=1.1, sy=0.95, jitter=0.06, seed=3)
snow = lathe([(1.08, 0.0), (1.02, 0.1), (0.9, 0.12), (0.82, 0.08)], verts=12, material=SNOW, sx=1.1, sy=0.95, jitter=0.07, seed=5, cap0=False, cap1=False)
# wak: donker water met rand van ijsbrokjes
HX, HY = -0.1, 0.05
lathe([(0.26, 0.072), (0.0, 0.073)], verts=9, material=WATER, cap0=False, loc=(HX, HY, 0))
for k in range(7):
    a = k * TAU / 7 + rnd.uniform(-0.1, 0.1)
    c = chunk(0.07, (1.3, 1.0, 0.7), cuts=3, seed=10 + k, material=ICE if k % 2 else SNOW, base_sub=1)
    T(c, rot=(0, 0, math.degrees(a)), loc=(HX + 0.3 * math.cos(a), HY + 0.3 * math.sin(a), 0.09))
# hengel op een gevorkt stokje, lijn in het wak met rood dobbertje
rod((0.45, -0.3, 0.07), (0.4, -0.25, 0.42), r=0.02, verts=4, material=WOOD)
rod((0.4, -0.25, 0.42), (0.36, -0.28, 0.52), r=0.012, verts=3, material=WOOD)
rod((0.4, -0.25, 0.42), (0.45, -0.21, 0.52), r=0.012, verts=3, material=WOOD)
rod((0.75, -0.48, 0.12), (-0.02, 0.05, 0.85), r=0.015, verts=4, material=WOOD)
cyl(0.035, 0.08, loc=(0.62, -0.39, 0.22), rot=(0.5, -0.9, 0), verts=6, material=RED)   # molentje
tube([(-0.02, 0.05, 0.85), (-0.06, 0.06, 0.5), (-0.08, 0.06, 0.12)], 0.004, verts=3, material=WATER, cap0=False, cap1=False)
sphere(0.03, loc=(-0.08, 0.06, 0.1), seg=5, rings=3, material=RED)
# rode emmer met vis die eruit steekt
bk = lathe([(0.12, 0.07), (0.15, 0.36), (0.13, 0.36), (0.1, 0.09), (0.0, 0.09)], verts=9, material=RED)
T(bk, loc=(-0.6, -0.35, 0))
torus(0.13, 0.008, loc=(-0.6, -0.35, 0.42), rot=(0, 1.2, 0), seg=6, ring=3, material=WATER)
fish = sphere(1.0, seg=6, rings=4, material=ICE, scale=(0.04, 0.1, 0.05))
tail = mesh_obj([(0, 0.09, 0), (0.0, 0.17, 0.05), (0.0, 0.17, -0.05)], [(0, 1, 2)], ICE, 'tail')
f = join([fish, tail], 'fish')
T(f, rot=(-60, 0, 20), loc=(-0.6, -0.36, 0.42))
# vis op het ijs
fish2 = sphere(1.0, seg=6, rings=4, material=ICE, scale=(0.05, 0.12, 0.035))
tail2 = mesh_obj([(0, 0.11, 0.0), (0.06, 0.2, 0.01), (-0.06, 0.2, 0.01)], [(0, 1, 2)], ICE, 'tail')
f2 = join([fish2, tail2], 'fish')
T(f2, rot=(0, 0, 70), loc=(0.35, 0.45, 0.11))
# klein houten krukje
for k in range(3):
    a = k * TAU / 3 + 0.4
    rod((0.62 + 0.14 * math.cos(a), 0.28 + 0.14 * math.sin(a), 0.07), (0.62 + 0.06 * math.cos(a), 0.28 + 0.06 * math.sin(a), 0.38), r=0.02, verts=4, material=WOOD)
cyl(0.16, 0.05, loc=(0.62, 0.28, 0.4), verts=8, material=WOOD)
o = join_all('ice_fishing_spot')
report()
done('ice', 'ice_fishing_spot', kind='scatter', footprint=1.0, center=True,
     notes='IJsvisplek: ijsvlakte met sneeuwrand en een wak met ijsbrokjes, hengel op gevorkt stokje met lijn en rood dobbertje, rode emmer met vis, vis op het ijs, houten krukje')
