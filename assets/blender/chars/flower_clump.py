import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

STEM = mat('stem', '#3f9a35', rough=0.7)
PINK = mat('petal_pink', '#ff4f93', rough=0.55)
VIOLET = mat('petal_violet', '#7b55ff', rough=0.55)
CENTER = mat('center', '#ffc21f', rough=0.5)
rnd = random.Random(3)
parts = []


def stem(pts, r0=0.009, r1=0.006):
    n = len(pts)
    return tube(pts, [r0 + (r1 - r0) * i / (n - 1) for i in range(n)], seg=3, material=STEM, cap=False)


def head(pos, nrm, npet, R, petm, cup=0.3, phase=0.0):
    """Flower head facing nrm: npet diamond petals (2 tris each) + low pyramid centre."""
    bm = bmesh.new()
    c = bm.verts.new((0, 0, 0))
    for k in range(npet):
        a = phase + TAU * k / npet
        da = math.pi / npet * 0.92
        P = lambda rr, aa, zz: bm.verts.new((rr * R * math.cos(a + aa), rr * R * math.sin(a + aa), zz * R))
        b0 = P(0.15, 0, 0)
        l = P(0.62, -da, cup * 0.4); r = P(0.62, da, cup * 0.4)
        tl = P(1.0, -da * 0.5, cup * 0.85); tr = P(1.0, da * 0.5, cup * 0.85)
        bm.faces.new((b0, r, tr, tl, l))
    bm.verts.remove(c)
    o = mesh_obj(bm, petm)
    cen = cone(r=0.36 * R, h=0.26 * R, loc=(0, 0, 0.1 * R), verts=6, material=CENTER)
    # cone_add makes a base cap: drop it (keep 6 side tris only)
    bm2 = bmesh.new(); bm2.from_mesh(cen.data)
    bmesh.ops.delete(bm2, geom=[f for f in bm2.faces if len(f.verts) > 3], context='FACES_ONLY')
    bm2.to_mesh(cen.data); bm2.free()
    q = Vector(nrm).normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
    M = Matrix.Translation(Vector(pos)) @ q
    xf(o, M); xf(cen, M)
    return [o, cen]


FL = [  # (base offset, tip, petals, radius, mat)
    (V(0.0, 0.0, 0), V(0.01, -0.03, 0.35), 6, 0.085, PINK),
    (V(0.02, 0.01, 0), V(0.14, 0.03, 0.26), 5, 0.075, VIOLET),
    (V(-0.02, 0.0, 0), V(-0.13, -0.06, 0.29), 6, 0.08, PINK),
    (V(0.0, 0.02, 0), V(-0.03, 0.13, 0.21), 5, 0.07, VIOLET),
]
for base, tip, n, R, m in FL:
    mid = base.lerp(tip, 0.5) + V(0, 0, 0.02) - (tip - base) * 0.0
    ctrl = V(base.x, base.y, tip.z * 0.55)
    pts = bezier(base + V(0, 0, -0.01), ctrl, tip, n=3)
    parts.append(stem(pts))
    out = V(tip.x, tip.y, 0)
    nrm = (V(0, 0, 1) + out * 3.5).normalized()
    parts += head(tip, nrm, n, R, m, phase=rnd.uniform(0, 1))

# leaves: long folded tapered blades from the base
for k, a in enumerate((0.4, 2.3, 3.9, 5.3)):
    d = V(math.cos(a), math.sin(a), 0); s = V(-d.y, d.x, 0)
    L = 0.12 + 0.03 * (k % 2)
    bm = bmesh.new()
    p0 = bm.verts.new(V(0, 0, 0.0))
    m1 = d * L * 0.45 + V(0, 0, L * 0.45)
    ml = bm.verts.new(m1 - s * 0.022); mr = bm.verts.new(m1 + s * 0.022); mc = bm.verts.new(m1 - d * 0.008 + V(0, 0, 0.008))
    tp = bm.verts.new(d * L * 1.0 + V(0, 0, L * 0.6))
    bm.faces.new((p0, mc, ml)); bm.faces.new((p0, mr, mc)); bm.faces.new((ml, mc, tp)); bm.faces.new((mc, mr, tp))
    parts.append(mesh_obj(bm, STEM))

body = part(parts, 'body', (0, 0, 0), angle=60)
report()
finish('chars', 'flower_clump', kind='char', footprint=0.15, grounded=False,
       notes='single part body, origin at base centre (0,0,0); 4 flowers on curved stems + 4 leaves; materials stem, petal_pink, petal_violet, center')
