import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

BARK = mat('date_bark', '#9a7550', rough=0.9)
BARK2 = mat('date_bark_dark', '#6f5236', rough=0.9)
LEAF = mat('date_leaf', '#5c8f45', rough=0.7)
LEAF2 = mat('date_leaf_light', '#86ab5a', rough=0.7)
DATES = mat('dates', '#d9792a', rough=0.5)
rnd = random.Random(8)

H = 4.9; r0, r1 = 0.26, 0.2
segs = 10; verts = 6
pts, rad, rm = [], [], []
pts += [(0, 0, -0.02), (0, 0, 0.15)]; rad += [r0 * 1.5, r0 * 1.1]; rm += [0, 0]
for i in range(segs):
    t0, t1 = i / segs, (i + 1) / segs
    z0, z1 = 0.15 + (H - 0.15) * t0, 0.15 + (H - 0.15) * t1
    ra = r0 + (r1 - r0) * t0; rb = r0 + (r1 - r0) * t1
    x0 = 0.04 * math.sin(t0 * 3); x1 = 0.04 * math.sin(t1 * 3)
    if i > 0:
        pts.append((x0, 0, z0)); rad.append(ra * 0.88); rm.append(i % 2)
    pts.append((x1, 0, z1 - (z1 - z0) * 0.12)); rad.append(rb * 1.12); rm.append(i % 2)
rm = rm[:len(pts) - 1]
trunk = tube(pts, rad, verts=verts, mats=[BARK, BARK2], ring_mats=rm, twist=0.45, jitter=0.05, seed=3)
top = Vector(pts[-1])
knob = tube([top - Vector((0, 0, 0.1)), top + Vector((0, 0, 0.25)), top + Vector((0, 0, 0.45))], [r1 * 1.25, r1 * 1.1, r1 * 0.5], verts=verts, material=BARK2)
ct = top + Vector((0, 0, 0.35))
# bladeren: stijf, boogvormig, veel stuks
nf = 12
for k in range(nf):
    layer = k % 3
    yaw = 2 * math.pi * k / nf + rnd.uniform(-0.15, 0.15)
    rise = [1.25, 0.85, 0.5][layer] * rnd.uniform(0.85, 1.15)
    droop = [0.3, 0.9, 1.5][layer] * rnd.uniform(0.8, 1.2)
    L = [2.0, 2.4, 2.5][layer] * rnd.uniform(0.9, 1.08)
    f = frond2(ct - Vector((0, 0, 0.08 * layer)), yaw, length=L, width=0.46, rise=rise, droop=droop, segs=6, leaf_drop=0.5,
               material=LEAF if k % 2 else LEAF2, notch=0.42, tipw=0.18)
    shade_smooth(f, 70)
# dode, hangende bladeren
for k in range(2):
    yaw = 2 * math.pi * k / 2 + 0.5
    f = frond2(top - Vector((0, 0, 0.15)), yaw, length=1.4, width=0.25, rise=-0.2, droop=1.6, segs=4, leaf_drop=0.3,
               material=BARK, notch=0.35, tipw=0.2)
# dadeltrossen
for k in range(3):
    a = 2 * math.pi * k / 3 + 1.1
    c = top + Vector((math.cos(a) * 0.45, math.sin(a) * 0.45, -0.5))
    tube([top + Vector((math.cos(a) * 0.15, math.sin(a) * 0.15, 0.05)), c + Vector((0, 0, 0.18))], [0.025, 0.02], verts=4, material=DATES)
    ico(0.2, loc=c, sub=1, material=DATES, scale=(1, 1, 1.5), jitter=0.045, seed=k)
join_all('date_palm')
report()
finish('desert', 'date_palm', kind='scatter', footprint=0.5,
       notes='Rechte dadelpalm met ruwe geschubde stam, stijve boogbladeren, dode hangbladeren en oranje dadeltrossen')
closeup('date_palm')
