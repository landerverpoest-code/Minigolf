import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

ICE = mat('ice_deep', '#38b4e2', rough=0.15, emit='#1690d0', emit_strength=0.25)
ICE2 = mat('ice_pale', '#a6e6ff', rough=0.15, emit='#6fd0ff', emit_strength=0.2)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
GLOW = mat('glow_ice', '#7ff4ff', rough=0.1, emit='#22d8ff', emit_strength=1.8)
rnd = random.Random(44)

SPAN, HGT = 3.2, 5.8
N = 22
pts, rad, sq = [], [], []
for i in range(N + 1):
    t = i / N; th = math.pi * t
    x = -SPAN * math.cos(th)
    z = HGT * math.sin(th) - 0.3
    pts.append((x + 0.2 * math.sin(th * 2), 0.2 * math.sin(th * 3), z))
    edge = min(t, 1 - t)
    r = 0.6 + 0.85 * (max(0, 0.3 - edge) / 0.3) ** 1.4
    rad.append(r)
    sq.append((1.5, 1.0))
arch = tube(pts, rad, verts=9, mats=[ICE, ICE2, SNOW], squash=sq, jitter=0.15, seed=3, name='arch')
for v in arch.data.vertices:
    v.co += Vector((rnd.uniform(-0.1, 0.1), rnd.uniform(-0.1, 0.1), rnd.uniform(-0.08, 0.08)))
for v in arch.data.vertices:
    v.co.z = max(v.co.z, 0.0)
for p in arch.data.polygons:
    f = p.center.z / HGT
    p.material_index = 1 if rnd.random() < 0.15 + 0.6 * f else 0
arch.data.update()
snow_cap(arch, 2, thresh=0.5, lift=0.12, grow=1.03, zmin=HGT * 0.62)
# ijspegels onder de boog
for i in range(5, N - 4, 2):
    t = i / N; th = math.pi * t
    x = -SPAN * math.cos(th) + 0.2 * math.sin(th * 2)
    z = HGT * math.sin(th) - 0.3
    r0 = rad[i]
    # binnenkant van de boog: richting middelpunt
    inward = Vector((-x, 0, -(z - 0.0))).normalized()
    p = Vector((x, 0.2 * math.sin(th * 3), z)) + inward * r0 * 0.85
    if p.z < 2.0: continue
    for k in range(3):
        h = rnd.uniform(0.4, 1.0)
        cone(0.11, h, loc=p + Vector((rnd.uniform(-0.15, 0.15), rnd.uniform(-0.35, 0.35), -h / 2 + 0.1)), rot=(math.pi, 0, 0), verts=5, material=ICE2 if k else ICE)
# ijsschotsen en kristallen rond de voeten
for i in range(10):
    side = -1 if i % 2 == 0 else 1
    a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(1.2, 2.1); s = rnd.uniform(0.35, 0.75)
    fl = rock(s, loc=(side * SPAN + math.cos(a) * d, math.sin(a) * d, 0.25 * s), scale=(1.3, 1.0, rnd.uniform(0.7, 1.2)), seed=50 + i,
              jitter=0.2, material=ICE if i % 3 else ICE2, rot_z=a)
    for v in fl.data.vertices: v.co.z = max(v.co.z, 0.0)
for k in range(6):
    side = -1 if k % 2 == 0 else 1
    c = lathe([(0.18, 0), (0.22, 1.0), (0, 1.5)], verts=6, material=GLOW if k % 2 == 0 else ICE2)
    place(c, loc=(side * (SPAN + 1.0) + rnd.uniform(-0.5, 0.5), rnd.uniform(-1.2, 1.2), 0.0), rot=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), 0), scale=rnd.uniform(0.7, 1.3))
# sneeuwhopen
for (x, y, sx, sy) in [(-SPAN - 0.2, -1.0, 1.2, 0.8), (SPAN + 0.3, 0.9, 1.1, 0.9)]:
    m = rock(1.0, loc=(x, y, 0.0), scale=(sx, sy, 0.35), seed=int(abs(x) * 10 + y * 3), sub=1, jitter=0.05, material=SNOW)
    for v in m.data.vertices: v.co.z = max(v.co.z, 0.0)
    shade_smooth(m, 60)
join_all('ice_arch')
report()
finish('ice', 'ice_arch', kind='hero', footprint=3.2,
       notes='Grote bevroren ijsboog met gelaagd ijs, sneeuwkap, ijspegels, ijsschotsen en gloeiende kristallen (glow_ice)')
closeup('ice_arch')
