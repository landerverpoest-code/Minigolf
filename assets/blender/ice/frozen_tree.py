import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

BARK = mat('frozen_bark', '#4d5566', rough=0.8)
FROST = mat('frost', '#e8f3ff', rough=0.6)
ICE = mat('ice', '#62d4f4', rough=0.12, emit='#1aa8e0', emit_strength=0.3)
ICE2 = mat('ice_pale', '#bdeeff', rough=0.15, emit='#6fd0ff', emit_strength=0.2)
SNOW = mat('snow', '#f4f8ff', rough=0.7)
rnd = random.Random(17)
tips = []
icicle_spots = []


def branch(p0, d, L, r, depth, verts):
    p0 = Vector(p0); d = Vector(d).normalized()
    n = 3 if depth > 1 else 2
    pts = [p0]; p = p0.copy(); dd = d.copy()
    for i in range(n):
        dd = (dd + Vector((rnd.uniform(-0.25, 0.25), rnd.uniform(-0.25, 0.25), rnd.uniform(-0.05, 0.15)))).normalized()
        p = p + dd * (L / n); pts.append(p.copy())
    rads = [r * (1 - 0.75 * i / n) for i in range(n + 1)]
    rads[-1] = r * 0.18 if depth > 0 else 0.0
    t = tube(pts, rads, verts=verts, mats=[BARK, FROST], cap0=False)
    for poly in t.data.polygons:
        poly.material_index = 1 if poly.normal.z > 0.35 else 0
    shade_smooth(t, 70)
    if depth > 0:
        kids = 3 if depth >= 2 else 2
        for k in range(kids):
            i = 1 + (k % (len(pts) - 1)) if depth >= 2 else len(pts) - 2 + (k % 2)
            i = min(i, len(pts) - 1)
            base = pts[i]
            a = rnd.uniform(0, 2 * math.pi)
            nd = (dd * 0.6 + Vector((math.cos(a), math.sin(a), 0.35)) * 0.8).normalized()
            branch(base, nd, L * rnd.uniform(0.5, 0.65), rads[min(i, len(rads) - 1)] * 0.7 + 0.01, depth - 1, max(3, verts - 1) if depth > 1 else 3)
        # ijspegel onder het midden van de tak
        if depth <= 2 and rnd.random() < 0.8:
            icicle_spots.append(pts[1] - Vector((0, 0, rads[1])))
    else:
        tips.append(pts[-1])

# stam met wortelvoet
trunk_pts = [(0, 0, 0), (0.0, 0.0, 0.45), (0.08, 0.05, 1.0), (0.05, 0.12, 1.45)]
tr = tube(trunk_pts, [0.28, 0.2, 0.16, 0.13], verts=6, mats=[BARK, FROST], cap0=True)
shade_smooth(tr, 60)
for poly in tr.data.polygons:
    poly.material_index = 1 if poly.normal.z > 0.35 else 0
for k in range(4):
    a = k * math.pi / 2 + 0.4
    tube([(math.cos(a) * 0.12, math.sin(a) * 0.12, 0.25), (math.cos(a) * 0.42, math.sin(a) * 0.42, 0.0)], [0.08, 0.03], verts=4, material=BARK)
for k, a in enumerate((0.3, 2.4, 4.4)):
    d = Vector((math.cos(a) * 0.95, math.sin(a) * 0.95, 0.9))
    branch(Vector(trunk_pts[-1]) - Vector((0, 0, 0.12 * k)), d, 1.75, 0.11, 2, 5)
branch(Vector(trunk_pts[-1]), (0.05, 0.1, 1), 1.7, 0.1, 1, 4)
# ijspegels
for p in icicle_spots[:9]:
    cone(0.035, rnd.uniform(0.18, 0.32), loc=p - Vector((0, 0, 0.12)), rot=(math.pi, 0, 0), verts=4, material=ICE)
# rijp-klompjes aan de takpunten
for i, p in enumerate(tips[::3][:6]):
    ico(0.09, loc=p, sub=1, material=ICE2 if i % 2 else ICE, scale=(1, 1, 1.2), jitter=0.02, seed=i)
# sneeuwhoopje
mound = lathe([(0.7, 0.0), (0.55, 0.09), (0.3, 0.15), (0.0, 0.16)], verts=9, material=SNOW, jitter=0.07, seed=5)
join_all('frozen_tree')
report()
finish('ice', 'frozen_tree', kind='scatter', footprint=0.6,
       notes='Kale bevroren boom: rijp op de bovenkant van de takken, ijspegels en ijsklompjes aan de takpunten')
closeup('frozen_tree')
