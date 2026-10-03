import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

ROCK = mat('ice_rock', '#5a6a7e', rough=0.85)
ROCK2 = mat('ice_rock_dark', '#435062', rough=0.85)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
ICE = mat('ice', '#5fd2f2', rough=0.12, emit='#1aa8e0', emit_strength=0.3)
rnd = random.Random(21)


def snowy_rock(r, loc, scale, seed, sub=2, ice_faces=3, rz=0.0, zc=0.55):
    o = rock(r, loc=loc, scale=scale, seed=seed, sub=sub, jitter=0.16, material=ROCK, rot_z=rz)
    for m in (ROCK2, ICE):
        o.data.materials.append(m)
    rr = random.Random(seed)
    for p in o.data.polygons:
        p.material_index = 0 if rr.random() < 0.6 else 1
    side = [p for p in o.data.polygons if abs(p.normal.z) < 0.4 and p.center.z < loc[2]]
    for p in rr.sample(side, min(ice_faces, len(side))):
        p.material_index = 2
    snow_blanket(o, SNOW, zc_frac=zc, wave=0.08, grow=1.04, lift=0.02 * r, seed=seed)
    return o

snowy_rock(0.8, (0, 0, 0.35), (1.3, 1.0, 1.15), seed=4, ice_faces=2, zc=0.6)
snowy_rock(0.45, (0.95, -0.45, 0.15), (1.2, 1.0, 0.9), seed=7, sub=2, ice_faces=1, rz=0.7)
snowy_rock(0.3, (-0.95, -0.4, 0.1), (1.1, 1.0, 0.9), seed=9, sub=1, ice_faces=0, rz=1.4)
# ijspegels onder de overhang
for k, (x, y) in enumerate([(-0.35, -0.8), (-0.15, -0.86), (0.1, -0.84)]):
    cone(0.05, 0.28 + 0.08 * (k % 2), loc=(x, y, 0.75), rot=(math.pi, 0, 0), verts=5, material=ICE)
# ijskristallen die uit een spleet steken
for k, (x, y, h, tx) in enumerate([(0.55, 0.3, 0.55, 0.4), (0.7, 0.15, 0.4, 0.7)]):
    c = lathe([(0.06, 0), (0.07, h * 0.7), (0, h)], verts=6, material=ICE)
    place(c, loc=(x, y, 0.55), rot=(0, tx, 0.3))
join_all('ice_rock')
report()
finish('ice', 'ice_rock', kind='scatter', footprint=0.9, notes='Grijsblauwe rots met dikke sneeuwkap, ijsvlakken, ijspegels en kristallen')
closeup('ice_rock')
