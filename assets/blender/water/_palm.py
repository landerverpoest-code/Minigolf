"""Gedeelde palmboom-bouwer voor het water-thema."""
from _kit import *


def palm_mats():
    return dict(
        bark=mat('bark', '#b38a55', rough=0.9),
        bark2=mat('bark_dark', '#83603a', rough=0.9),
        leaf=mat('palm_leaf', '#2f9a3e', rough=0.65),
        leaf2=mat('palm_leaf_light', '#6cc244', rough=0.65),
        nut=mat('coconut', '#6b4526', rough=0.55),
    )


def palm(M, base=(0, 0, 0), height=4.4, lean=(0.7, 0.0), r0=0.2, r1=0.12, segs=9, verts=7, fronds=8,
         flen=2.2, fwidth=0.42, nuts=3, seed=1, fsegs=7, flare=True, frise=0.5, fdroop=1.3, up_fronds=0,
         straight=0.0, nut_seg=(7, 5)):
    rnd = random.Random(seed)
    base = Vector(base)
    lx, ly = lean

    def P(t):
        k = t * t * (1 - straight) + t * straight
        return base + Vector((lx * k, ly * k, height * t))
    pts, rad, rm = [], [], []
    if flare:
        pts += [base + Vector((0, 0, -0.02)), base + Vector((0, 0, 0.12))]
        rad += [r0 * 1.6, r0 * 1.12]
        rm += [0, 0]
    for i in range(segs):
        t0, t1 = i / segs, (i + 1) / segs
        rb = r0 + (r1 - r0) * t1
        ra = r0 + (r1 - r0) * t0
        p0, p1 = P(t0), P(t1)
        if not (flare and i == 0):
            pts.append(p0); rad.append(ra * 0.9); rm.append(i % 2)
        else:
            rm[-1] = 0
        pts.append(p1 - (p1 - p0) * 0.08); rad.append(rb * 1.12); rm.append(i % 2)
    rm = rm[:len(pts) - 1]
    trunk = tube(pts, rad, verts=verts, mats=[M['bark'], M['bark2']], ring_mats=rm, name='trunk', twist=0.3)
    shade_smooth(trunk, 40)
    top = P(1.0)
    tdir = (P(1.0) - P(0.96)).normalized()
    parts = [trunk]
    knob = tube([top - tdir * 0.12, top + tdir * 0.12, top + tdir * 0.3], [r1 * 1.15, r1 * 1.0, r1 * 0.45], verts=verts,
                material=M['bark2'], name='knob')
    parts.append(knob)
    ctop = top + tdir * 0.22
    nf = fronds + up_fronds
    for k in range(nf):
        young = k >= fronds
        yaw = 2 * math.pi * k / fronds + rnd.uniform(-0.2, 0.2) + seed if not young else rnd.uniform(0, 6.28)
        L = flen * rnd.uniform(0.85, 1.08) * (0.5 if young else 1)
        f = frond2(ctop, yaw, length=L, width=fwidth * rnd.uniform(0.9, 1.1) * (0.8 if young else 1),
                   rise=(frise * rnd.uniform(0.75, 1.3)) * (1.4 if young else 1),
                   droop=fdroop * rnd.uniform(0.75, 1.2) * (0.35 if young else 1), segs=fsegs if not young else max(4, fsegs - 2),
                   leaf_drop=0.55, material=M['leaf'] if k % 2 == 0 else M['leaf2'], name='frond%d' % k)
        shade_smooth(f, 70)
        parts.append(f)
    for k in range(nuts):
        a = 2 * math.pi * k / max(nuts, 1) + seed * 0.7
        c = top + Vector((math.cos(a) * r1 * 1.7, math.sin(a) * r1 * 1.7, -0.22 - 0.07 * (k % 2)))
        parts.append(sphere(0.15, loc=c, seg=nut_seg[0], rings=nut_seg[1], material=M['nut']))
    return parts, top
