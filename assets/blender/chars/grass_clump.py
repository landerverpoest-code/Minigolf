import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

GRASS = mat('grass', '#5cb83a', rough=0.7)
rnd = random.Random(7)


def blade(base, ang, h, w, lean, curl, twist=0.0, fold=0.35, segs=3):
    """V-folded tapered blade: centre rib + 2 edges per row, pointed tip.
    ang: direction (rad) the blade leans toward; lean: horizontal reach at tip; curl: extra bend near tip."""
    bm = bmesh.new()
    d = V(math.cos(ang), math.sin(ang), 0)
    side = V(-d.y, d.x, 0)
    rows = []
    for i in range(segs):
        t = i / segs
        # bend: quadratic lean + curl
        off = d * (lean * t * t + curl * t ** 3)
        p = V(base) + off + V(0, 0, h * (t - 0.12 * t * t * (lean + curl) / max(h, 0.01)))
        ww = w * (1 - t * 0.75)
        s = (Matrix.Rotation(twist * t, 3, 'Z') @ side)
        n_out = d  # fold bulges along the lean direction (spine on the back)
        rows.append([bm.verts.new(p - s * ww), bm.verts.new(p - n_out * ww * fold), bm.verts.new(p + s * ww)])
    tip = V(base) + d * (lean + curl) + V(0, 0, h * (1 - 0.12 * (lean + curl) / max(h, 0.01)))
    tv = bm.verts.new(tip)
    for a, b in zip(rows, rows[1:]):
        bm.faces.new((a[0], a[1], b[1], b[0]))
        bm.faces.new((a[1], a[2], b[2], b[1]))
    a = rows[-1]
    bm.faces.new((a[0], a[1], tv)); bm.faces.new((a[1], a[2], tv))
    bmesh.ops.triangulate(bm, faces=bm.faces)
    return mesh_obj(bm, GRASS)


blades = []
N = 13
for i in range(N):
    a = TAU * i / N + rnd.uniform(-0.25, 0.25)
    rr = rnd.uniform(0.03, 0.08)
    base = V(math.cos(a) * rr, math.sin(a) * rr, -0.01)
    h = rnd.uniform(0.25, 0.55)
    if i % 4 == 0:
        h = rnd.uniform(0.46, 0.55)
    lean = rnd.uniform(0.08, 0.17) * (h / 0.4)
    curl = rnd.uniform(0.02, 0.1) * (h / 0.4)
    blades.append(blade(base, a + rnd.uniform(-0.3, 0.3), h, rnd.uniform(0.032, 0.046), lean, curl, twist=rnd.uniform(-0.6, 0.6)))
body = part(blades, 'body', (0, 0, 0), angle=80)
report()
finish('chars', 'grass_clump', kind='char', footprint=0.15, grounded=False,
       notes='single part body, origin at base centre (0,0,0); 13 V-folded tapered blades (3 segments), material grass; game sways tips in vertex shader')
