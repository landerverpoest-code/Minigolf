import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

WOOD = mat('wood', '#a8743e', rough=0.85)
WOOD2 = mat('wood_dark', '#77502c', rough=0.85)
THATCH = mat('thatch', '#dcb25a', rough=0.95)
WALL = mat('bamboo', '#ead09a', rough=0.8)
TURQ = mat('turq', '#25b3bf', rough=0.55)
rnd = random.Random(2)

ZD = 1.6   # dekhoogte (bovenkant planken)
# --- palen ---
for x in (-1.35, 0, 1.35):
    for y in (-1.35, 0, 1.35):
        if x == 0 and y == 0: continue
        cyl(0.09, ZD, loc=(x, y, ZD / 2 - 0.05), verts=6, material=WOOD2)
# kruisverbanden
for s in (-1, 1):
    for (a, b) in [((-1.35, s * 1.35, 0.25), (0, s * 1.35, ZD - 0.25)), ((1.35, s * 1.35, 0.25), (0, s * 1.35, ZD - 0.25))]:
        tube([a, b], [0.04, 0.04], verts=4, material=WOOD2)
    for (a, b) in [((s * 1.35, -1.35, 0.25), (s * 1.35, 0, ZD - 0.25)), ((s * 1.35, 1.35, 0.25), (s * 1.35, 0, ZD - 0.25))]:
        tube([a, b], [0.04, 0.04], verts=4, material=WOOD2)
# balken onder het dek
for y in (-1.35, 1.35):
    box((3.1, 0.14, 0.16), loc=(0, y, ZD - 0.2), material=WOOD2)
# planken
n = 9
for i in range(n):
    x = -1.5 + (i + 0.5) * 3.0 / n
    box((3.0 / n - 0.035, 3.2 + rnd.uniform(-0.06, 0.06), 0.09), loc=(x, 0, ZD - 0.045), material=WOOD if i % 2 else WOOD2, bevel=0.012)
# --- ronde hut ---
R = 1.05
wall = lathe([(R, ZD), (R, ZD + 1.55), (0, ZD + 1.55)], verts=12, material=WALL, cap1=False, phase=math.pi / 12)
# bamboe-ringen
for z in (ZD + 0.08, ZD + 0.75, ZD + 1.45):
    torus(R + 0.02, 0.04, loc=(0, 0, z), seg=12, ring=4, material=WOOD, smooth=False)
# hoekpalen hut
for k in range(6):
    a = 2 * math.pi * k / 6 + math.pi / 6
    cyl(0.06, 1.6, loc=(math.cos(a) * (R + 0.03), math.sin(a) * (R + 0.03), ZD + 0.8), verts=5, material=WOOD2)
# deur (voor, -Y) en raampjes
box((0.55, 0.16, 1.0), loc=(0, -R + 0.02, ZD + 0.52), material=WOOD2, bevel=0.02)
box((0.45, 0.06, 0.9), loc=(0, -R - 0.05, ZD + 0.48), material=TURQ, bevel=0.015)
for a in (math.pi * 0.15, math.pi * 0.85):
    c = Vector((math.cos(a), -math.sin(a), 0))
    w = box((0.36, 0.1, 0.32), loc=c * R + Vector((0, 0, ZD + 1.0)), rot=(0, 0, math.atan2(c.y, c.x) + math.pi / 2), material=WOOD2)
    sh = box((0.2, 0.05, 0.36), loc=c * (R + 0.06) + Vector((0, 0, ZD + 1.0)) + c.cross(UP) * 0.3,
             rot=(0, 0, math.atan2(c.y, c.x) + math.pi / 2), material=TURQ)
# --- rieten dak in drie lagen ---
ZR = ZD + 1.5
tiers = [(2.0, ZR - 0.05, 1.25, ZR + 0.65), (1.4, ZR + 0.5, 0.75, ZR + 1.15), (0.85, ZR + 1.0, 0.0, ZR + 1.85)]
for i, (r0, z0, r1, z1) in enumerate(tiers):
    prof = [(r0 * 0.94, z0 - 0.04), (r0, z0 + 0.06), (r1, z1)]
    if r1 > 0:
        prof.append((r1 * 0.6, z1 - 0.15))
    t = lathe(prof, verts=14, material=THATCH, jitter=0.06, seed=10 + i, phase=i * 0.3, cap0=True, cap1=r1 > 0)
    # rafelige onderrand
    for k, v in enumerate(t.data.vertices):
        if v.co.z < z0 + 0.03:
            v.co.z -= 0.09 * (k % 2)
# topje
cone(0.12, 0.5, loc=(0, 0, ZR + 2.0), verts=6, material=WOOD2)
# --- reling ---
for x in (-1.45, -0.5, 0.5, 1.45):
    for y in (1.45,):
        cyl(0.045, 0.7, loc=(x, y, ZD + 0.35), verts=5, material=WOOD2)
for y in (-0.5, 0.5, 1.45):
    for x in (-1.45, 1.45):
        cyl(0.045, 0.7, loc=(x, y, ZD + 0.35), verts=5, material=WOOD2)
tube([(-1.45, -0.5, ZD + 0.68), (-1.45, 1.45, ZD + 0.68), (1.45, 1.45, ZD + 0.68), (1.45, -0.5, ZD + 0.68)], [0.035] * 4, verts=4, material=WOOD)
for x in (-1.45, -0.5):
    cyl(0.045, 0.7, loc=(x, -1.45, ZD + 0.35), verts=5, material=WOOD2)
tube([(-1.45, -0.5, ZD + 0.68), (-1.45, -1.45, ZD + 0.68), (-0.5, -1.45, ZD + 0.68)], [0.035] * 3, verts=4, material=WOOD)
# --- steiger naar voren (-Y) ---
PX = 0.9
for j in range(7):
    y = -1.6 - j * 0.34
    box((0.95, 0.3, 0.08), loc=(PX, y, ZD - 0.5 - 0.04), rot=(0, 0, rnd.uniform(-0.04, 0.04)), material=WOOD if j % 2 else WOOD2, bevel=0.01)
for y in (-1.75, -3.45):
    for x in (PX - 0.42, PX + 0.42):
        cyl(0.07, ZD - 0.4, loc=(x, y, (ZD - 0.4) / 2 - 0.1), verts=6, material=WOOD2)
for x in (PX - 0.42, PX + 0.42):
    box((0.1, 2.3, 0.1), loc=(x, -2.6, ZD - 0.64), material=WOOD2)
# trapje dek -> steiger
for k in range(3):
    box((0.8, 0.22, 0.07), loc=(PX, -1.45 - k * 0.0 - 0.12, ZD - 0.12 - k * 0.14), material=WOOD)
# ladder aan het eind van de steiger naar het water
LY = -3.62
for x in (PX - 0.22, PX + 0.22):
    cyl(0.035, ZD - 0.3, loc=(x, LY, (ZD - 0.3) / 2 - 0.15), verts=5, material=WOOD2)
for k in range(4):
    cyl(0.025, 0.44, loc=(PX, LY, 0.1 + k * 0.28), rot=(0, math.pi / 2, 0), verts=5, material=WOOD)
# tonnetje en reddingsboei
barrel = lathe([(0.2, ZD), (0.24, ZD + 0.25), (0.2, ZD + 0.5), (0, ZD + 0.5)], verts=8, material=WOOD, cap0=False)
place(barrel, loc=(1.15, 1.05, 0))
torus(0.2, 0.06, loc=(-1.47, -1.0, ZD + 0.38), rot=(0, math.pi / 2, 0), seg=10, ring=5, material=TURQ, smooth=True)
join_all('stilt_hut')
report()
finish('water', 'stilt_hut', kind='hero', footprint=2.2,
       notes='Rieten paalwoning op palen met kruisverbanden, reling, steiger naar voren (-Y) en ladder naar het water')
closeup('stilt_hut')
