import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood_dark', '#5e3f26', rough=0.9)
straw = mat('straw', '#e8c45c', rough=0.9)
shirt = mat('shirt_red', '#c8402f', rough=0.85)
denim = mat('denim', '#3f5f9a', rough=0.85)
burlap = mat('burlap', '#d9bf8c', rough=0.95)

parts = []
# paal + dwarslat
parts.append(box((0.08, 0.08, 1.62), loc=(0, 0.04, 0.81), material=wood, bevel=0.012))
parts.append(box((1.5, 0.07, 0.07), loc=(0, 0.04, 1.42), material=wood, bevel=0.01))

# hemd: taps toelopend lijf
body = cyl(0.2, 0.62, loc=(0, 0, 1.12), verts=8, r2=0.24, material=shirt)
xform(body, scale=(1.15, 0.75, 1))
jitter(body, 0.012, seed=1)
smooth(body, 50)
parts.append(body)
# mouwen langs de dwarslat (licht hangend)
for sx in (-1, 1):
    sl = rod((sx * 0.18, 0.0, 1.38), (sx * 0.6, -0.01, 1.33), 0.1, 0.075, verts=7, material=shirt)
    jitter(sl, 0.01, seed=2 + sx)
    parts.append(sl)
    # stro uit de mouw
    for k in range(4):
        a = k * TAU / 4 + 0.4
        p0 = Vector((sx * 0.6, -0.01 + 0.04 * math.cos(a), 1.33 + 0.04 * math.sin(a)))
        p1 = p0 + Vector((sx * 0.14, 0.05 * math.cos(a), 0.05 * math.sin(a) - 0.03))
        parts.append(rod(p0, p1, 0.024, 0.0, verts=3, material=straw))
# stro onder het hemd
for k in range(7):
    a = k * TAU / 7
    p0 = Vector((0.2 * math.cos(a), 0.14 * math.sin(a), 0.84))
    p1 = p0 + Vector((0.05 * math.cos(a), 0.04 * math.sin(a), -0.13))
    parts.append(rod(p0, p1, 0.032, 0.0, verts=3, material=straw))
# lapje op het hemd + knopen
parts.append(box((0.1, 0.02, 0.09), loc=(0.08, -0.17, 1.02), rot=(0, 0.15, 0), material=denim))
for z in (1.3, 1.18, 1.06):
    parts.append(cyl(0.018, 0.02, loc=(-0.01, -0.165 + (1.3 - z) * 0.05, z), rot=(math.pi / 2, 0, 0), verts=6, material=wood))
# broek: twee bungelende pijpen met stro
for sx in (-1, 1):
    leg = rod((sx * 0.09, 0.0, 0.9), (sx * 0.12, -0.03, 0.42), 0.085, 0.075, verts=7, material=denim)
    parts.append(leg)
    for k in range(4):
        a = k * TAU / 4
        p0 = Vector((sx * 0.12 + 0.04 * math.cos(a), -0.03 + 0.04 * math.sin(a), 0.42))
        p1 = p0 + Vector((0.03 * math.cos(a), 0.03 * math.sin(a), -0.12))
        parts.append(rod(p0, p1, 0.024, 0.0, verts=3, material=straw))
# broekband
parts.append(cyl(0.21, 0.07, loc=(0, 0, 0.88), verts=8, material=denim))
xform(parts[-1], scale=(1.12, 0.78, 1))

# hoofd: jute zak met gestikt gezicht
head = sphere(0.19, loc=(0, 0, 1.66), seg=10, rings=7, material=burlap, scale=(1, 0.95, 1.08))
jitter(head, 0.01, seed=4)
smooth(head, 60)
parts.append(head)
# toefje/zakje dicht onder het hoofd (touw)
parts.append(cyl(0.07, 0.06, loc=(0, 0, 1.47), verts=6, material=straw))
# ogen (kruisjes) en mond
for sx in (-1, 1):
    for r in (45, -45):
        parts.append(box((0.07, 0.015, 0.016), loc=(sx * 0.07, -0.175, 1.7), rot=(0, math.radians(r), 0), material=wood))
for k in range(5):
    x = -0.08 + k * 0.04
    parts.append(box((0.03, 0.015, 0.012), loc=(x, -0.172, 1.58 + 0.012 * math.cos(x * 15)), material=wood))
nose = cone(0.03, 0.08, loc=(0, -0.21, 1.64), rot=(math.pi / 2, 0, 0), verts=5, material=shirt)
parts.append(nose)
# strohoed met rode band
brim = cyl(0.33, 0.025, loc=(0, 0, 1.8), verts=12, material=straw)
bend(brim, lambda c: (c.x, c.y, c.z + 0.06 * (Vector((c.x, c.y)).length / 0.33) ** 2 * (1 if c.x > 0 else 0.4)))
parts.append(brim)
parts.append(cyl(0.17, 0.2, loc=(0, 0, 1.9), verts=10, r2=0.14, material=straw))
parts.append(cyl(0.172, 0.05, loc=(0, 0, 1.84), verts=10, r2=0.165, material=shirt))
for o in parts[-3:]:
    xform(o, loc=(0, 0, -1.84))
    xform(o, rot=(-6, 8, 0))
    xform(o, loc=(0.02, 0, 1.84))
join(parts, 'scarecrow')
report()
finish('meadow', 'scarecrow', kind='scatter', footprint=0.45, notes='vogelverschrikker: jute hoofd met gestikt gezicht, strohoed, rood hemd met lapje, spijkerbroek, stro')
