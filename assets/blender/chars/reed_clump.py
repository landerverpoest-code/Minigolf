import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

STEM = mat('stem', '#5d9a3a', rough=0.7)
HEAD = mat('head', '#7a4a26', rough=0.85)
rnd = random.Random(11)
parts = []

REEDS = [  # base, tip of head-stalk, head length
    (V(0.0, 0.0, 0), V(0.03, -0.02, 1.12), 0.2),
    (V(0.04, 0.03, 0), V(0.2, 0.06, 0.92), 0.17),
    (V(-0.04, 0.01, 0), V(-0.17, -0.07, 0.98), 0.18),
]
for base, top, hl in REEDS:
    ctrl = V(base.x, base.y, top.z * 0.6)
    pts = bezier(base + V(0, 0, -0.02), ctrl, top, n=3)
    parts.append(tube(pts, [0.012, 0.01, 0.008, 0.006], seg=3, material=STEM, cap=False))
    # head: rounded sausage along the top segment direction, just below the tip spike
    d = (pts[-1] - pts[-2]).normalized()
    hc = top - d * (0.07 + hl * 0.5)
    q = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    r = 0.036
    prof = [(0, -hl * 0.5), (r, -hl * 0.36), (r, hl * 0.36), (0, hl * 0.5)]
    parts.append(lathe(prof, seg=5, material=HEAD, M=Matrix.Translation(hc) @ q))
    # tip spike
    bm = bmesh.new(); b0 = top - d * 0.075
    sd = d.orthogonal().normalized(); sd2 = d.cross(sd)
    ring = [bm.verts.new(b0 + (sd * math.cos(TAU * i / 3) + sd2 * math.sin(TAU * i / 3)) * 0.006) for i in range(3)]
    tv = bm.verts.new(top)
    for i in range(3):
        bm.faces.new((ring[i], ring[(i + 1) % 3], tv))
    parts.append(mesh_obj(bm, STEM))

# strap leaves
for k in range(5):
    a = TAU * k / 5 + rnd.uniform(-0.3, 0.3)
    h = rnd.uniform(0.6, 0.85)
    parts.append(blade(V(math.cos(a) * 0.03, math.sin(a) * 0.03, -0.01), a, h, rnd.uniform(0.038, 0.048),
                       rnd.uniform(0.12, 0.2), rnd.uniform(0.08, 0.16), STEM, twist=rnd.uniform(-0.5, 0.5), segs=3, taper=0.6))

body = part(parts, 'body', (0, 0, 0), angle=60)
report()
finish('chars', 'reed_clump', kind='char', footprint=0.2, grounded=False,
       notes='single part body, origin at base centre (0,0,0); 3 cattails (brown heads) + 5 strap leaves; materials stem, head')
