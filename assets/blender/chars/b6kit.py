"""Wave-6 agent-B kit (gong, swing_wall, lava_bridge_rune): okit + a few extras."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
from okit import *          # noqa: F401,F403  (bx, lathe, tube, prism, part, report, views, montage, std_view, ...)
from okit import _obj


def ribbon(pts, width, normal, material=None, lift=0.003, taper=True):
    """Flat strip along a 3D polyline lying on a plane with the given normal (cracks, inlays).
    width: scalar or list per point. lift: offset along the normal (sits just proud of the surface)."""
    pts = [Vector(p) for p in pts]
    n = Vector(normal).normalized()
    if not isinstance(width, (list, tuple)):
        width = [width] * len(pts)
        if taper:
            width = [w * (0.35 + 0.65 * (1 - i / max(len(pts) - 1, 1)) ** 0.7) for i, w in enumerate(width)]
    bm = bmesh.new()
    L, R = [], []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        t = (b - a).normalized()
        side = t.cross(n).normalized() * width[i] * 0.5
        q = p + n * lift
        L.append(bm.verts.new(q - side)); R.append(bm.verts.new(q + side))
    for i in range(len(pts) - 1):
        f = bm.faces.new((L[i], R[i], R[i + 1], L[i + 1]))
        if f.normal.dot(n) < 0:
            f.normal_flip()
    return _obj(bm, material, smooth=False)


def crack_paths(rnd, u0, u1, v0, v1, n_main=2, steps=7, branch=0.5):
    """Random zig-zag crack polylines inside a (u,v) rectangle, returned as lists of (u,v)."""
    out = []
    for k in range(n_main):
        u = rnd.uniform(u0 + 0.25 * (u1 - u0), u1 - 0.25 * (u1 - u0))
        v = v0 + rnd.uniform(0, 0.15) * (v1 - v0)
        span = (v1 - v0) * rnd.uniform(0.55, 0.95)
        path = [(u, v)]
        for s in range(steps):
            v += span / steps
            u = min(max(u + rnd.uniform(-1, 1) * (u1 - u0) * 0.28, u0), u1)
            path.append((u, min(v, v1)))
        out.append(path)
        # branches
        for s in range(1, steps - 1):
            if rnd.random() < branch:
                bu, bv = path[s]
                d = rnd.choice((-1, 1))
                br = [(bu, bv)]
                for j in range(3):
                    bu = min(max(bu + d * (u1 - u0) * rnd.uniform(0.12, 0.25), u0), u1)
                    bv = bv + span / steps * rnd.uniform(0.3, 0.8)
                    br.append((bu, min(bv, v1)))
                out.append(br)
    return out


def ext(o):
    """World-space bbox of one object -> ((x0,x1),(y0,y1),(z0,z1)) rounded to mm."""
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return tuple((round(min(p[i] for p in pts), 3), round(max(p[i] for p in pts), 3)) for i in range(3))


def print_ext():
    for o in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        if o.type == 'MESH':
            print('EXT', o.name, 'origin', tuple(round(v, 3) for v in o.location), 'x/y/z', ext(o))


def relief(pts2d, z0, z1, material=None):
    """Like prism() but without the bottom cap (for reliefs glued onto a surface)."""
    o = prism(pts2d, z0, z1, material)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bot = [f for f in bm.faces if all(abs(v.co.z - z0) < 1e-7 for v in f.verts)]
    bmesh.ops.delete(bm, geom=bot, context='FACES_ONLY')
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o
