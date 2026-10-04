import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice'); from _deco import *

ROCK = mat('ice_rock', '#5a6a7e', rough=0.85)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
ICE = mat('ice', '#62d4f4', rough=0.12, emit='#1aa8e0', emit_strength=0.3)
ICE_P = mat('ice_pale', '#b8ecff', rough=0.12, emit='#6fd0ff', emit_strength=0.2)
GLOW = mat('glow_ice', '#7ff4ff', rough=0.1, emit='#22d8ff', emit_strength=1.6)

rnd = random.Random(8)
# --- rotswand: hoefijzer van gefacetteerde blokken, open naar -Y
blocks = []
spec = [((-1.6, 0.6, 0.0), 1.0, (1.0, 1.0, 1.9)), ((-1.0, 1.1, 0.0), 1.1, (1.1, 0.9, 2.3)), ((0.0, 1.35, 0.0), 1.2, (1.4, 0.8, 2.6)),
        ((1.05, 1.05, 0.0), 1.1, (1.0, 0.9, 2.25)), ((1.65, 0.5, 0.0), 0.95, (1.0, 1.0, 1.7)), ((0.0, 1.3, 2.95), 1.0, (1.7, 0.75, 0.55)), ((-1.3, 1.0, 2.0), 0.8, (1.0, 0.9, 1.2)),
        ((1.3, 0.95, 1.9), 0.8, (1.0, 0.9, 1.1)), ((-2.2, 0.0, 0.0), 0.65, (1.0, 1.0, 1.2)), ((2.15, -0.1, 0.0), 0.6, (1.0, 1.0, 1.1))]
for k, (p, r, sc) in enumerate(spec):
    c = chunk(r, sc, cuts=9, seed=20 + k, material=ROCK, flat_bottom=0.0 if p[2] == 0 else None, base_sub=2)
    T(c, loc=(p[0], p[1], p[2] + (r * sc[2] * 0.0)))
    dust(c, SNOW, thresh=0.55)
    blocks.append(c)
# --- bevroren waterval: brede bevroren 'gordijnen' van ijsbuizen die van de rand naar beneden vloeien
TOP = 2.85
for i in range(9):
    x = -0.85 + i * 0.21 + rnd.uniform(-0.04, 0.04)
    y0 = 0.72 + 0.05 * math.cos(x)
    pts = []
    n = 6
    for j in range(n + 1):
        t = j / n
        z = TOP * (1 - t) + 0.15
        y = y0 - 0.35 * math.sin(t * math.pi * 0.5) ** 2 - 0.12 * t + 0.06 * math.sin(i * 1.3 + t * 4)
        pts.append(Vector((x + 0.05 * math.sin(t * 3 + i), y, z)))
    rad = [0.12 + 0.03 * math.sin(i * 2.1 + j) + 0.05 * (j / n) for j in range(n + 1)]
    tube(pts, rad, verts=6, material=ICE if i % 3 else ICE_P, smooth=True, cap0=False)
# ijspegels die over de bovenrand hangen
for k in range(12):
    x = -1.3 + k * 0.24 + rnd.uniform(-0.05, 0.05)
    z = TOP + 0.05 + rnd.uniform(-0.1, 0.05) - abs(x) * 0.15
    y = 0.78 + abs(x) * 0.1
    L = rnd.uniform(0.35, 0.8)
    cone(0.06, L, loc=(x, y, z - L / 2), rot=(math.pi, 0, 0), verts=5, material=ICE_P)
# ijspegels langs de zijblokken
for k, (x, y, z) in enumerate(((-1.45, 0.05, 1.5), (-1.25, 0.2, 1.75), (1.4, 0.0, 1.3), (1.25, 0.25, 1.6))):
    L = rnd.uniform(0.3, 0.6)
    cone(0.05, L, loc=(x, y, z - L / 2), rot=(math.pi, 0, 0), verts=4, material=ICE_P)
# --- bevroren vijver met gebroken schotsen en scheurtjes
pool = lathe([(1.45, 0.0), (1.4, 0.08), (0.0, 0.1)], verts=14, material=ICE, sx=1.2, sy=0.75, loc=(0, -0.35, 0), jitter=0.06, seed=4)
for k in range(5):
    a = rnd.uniform(0, TAU); r = rnd.uniform(0.3, 1.1)
    f = chunk(0.18, (1.4, 1.0, 0.3), cuts=4, seed=60 + k, material=ICE_P, base_sub=1)
    T(f, rot=(rnd.uniform(-10, 10), rnd.uniform(-10, 10), rnd.uniform(0, 180)), loc=(r * math.cos(a) * 1.1, -0.45 + r * math.sin(a) * 0.55, 0.12))
# opspattend ijs aan de voet van de val
foot = blob([((0, 0.25, 0.25), 0.4), ((0.45, 0.2, 0.2), 0.3), ((-0.45, 0.22, 0.2), 0.3), ((0.0, -0.05, 0.12), 0.3)], center=(0, 0.15, 0.18), sub=2, material=ICE_P, angle=45)
deform(foot, lambda c: Vector((c.x, c.y, max(c.z, 0.0))))
# gloeiende kristallen in de rotsen
for k, (x, y, z, a) in enumerate(((-1.55, -0.2, 0.25, -20), (1.6, -0.25, 0.25, 25), (-0.95, 0.35, 0.2, -10), (1.0, 0.3, 0.25, 15), (1.75, -0.15, 0.5, 35))):
    h = rnd.uniform(0.35, 0.6)
    c = lathe([(0.07, 0.0), (0.08, h * 0.7), (0.0, h)], verts=5, material=GLOW)
    T(c, rot=(rnd.uniform(-20, 20), a, 0), loc=(x, y, z))
# sneeuwhopen aan de voet
for k, (x, y, s) in enumerate(((-1.9, -0.6, 0.45), (1.85, -0.65, 0.42), (-2.5, 0.3, 0.35), (2.5, 0.2, 0.33))):
    sm = blob([((0, 0, 0), s), ((s * 0.7, 0.1, -s * 0.15), s * 0.7)], center=(s * 0.2, 0, 0), sub=2, material=SNOW, angle=50)
    deform(sm, lambda c: Vector((c.x, c.y, max(c.z, 0.0))))
    T(sm, loc=(x, y, 0))
o = join_all('frozen_waterfall')
report()
done('ice', 'frozen_waterfall', kind='hero', footprint=2.7, center=True,
     notes='Bevroren waterval: hoefijzervormige rotswand van gefacetteerde blokken met sneeuw bovenop, gordijn van bevroren ijsstromen, hangende ijspegels, bevroren vijver met schotsen, opgespat ijs aan de voet, gloeiende ijskristallen (glow_ice) en sneeuwhopen')
