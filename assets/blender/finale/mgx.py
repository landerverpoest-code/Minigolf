"""Extra modelleer-helpers bovenop mglib (lathe, tube, prism, transformaties, deformaties).
Identieke kopie staat in haunted/, space/ en finale/.

Conventie: objecten die hier gemaakt worden hebben hun geometrie in wereldcoordinaten
(object-transform = identiteit). T() bakt eerst de objecttransform in de mesh en
transformeert dan de mesh-data, zodat mglib-primitieven en mgx-objecten mengbaar zijn.
"""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler, Quaternion
from mglib import *

TAU = math.tau


def _link(bm, name, material=None, smooth=False, recalc=False):
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        me.materials.append(material)
    if smooth:
        shade_smooth(o)
    return o


def bake(o):
    """Objecttransform in de mesh bakken."""
    if o.matrix_world != Matrix.Identity(4):
        o.data.transform(o.matrix_world)
        o.matrix_world = Matrix.Identity(4)
    return o


def _flip(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free()


def T(o, loc=(0, 0, 0), rot=(0, 0, 0), scale=1, pivot=(0, 0, 0)):
    """Mesh transformeren (in wereldruimte): schaal+rotatie rond pivot, dan verschuiven."""
    bake(o)
    s = (scale, scale, scale) if isinstance(scale, (int, float)) else tuple(scale)
    P = Vector(pivot)
    M = Matrix.Translation(Vector(loc) + P) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*s, 1)) @ Matrix.Translation(-P)
    o.data.transform(M)
    if s[0] * s[1] * s[2] < 0:
        _flip(o)
    o.data.update()
    return o


def dup(o, **kw):
    n = o.copy(); n.data = o.data.copy()
    bpy.context.scene.collection.objects.link(n)
    if kw:
        T(n, **kw)
    return n


def deform(o, fn):
    """fn(Vector) -> Vector op elke vertex (wereldcoordinaten)."""
    bake(o)
    for v in o.data.vertices:
        v.co = Vector(fn(v.co.copy()))
    o.data.update()
    return o


def jitter(o, amt=0.05, seed=0, axes=(1, 1, 1)):
    bake(o)
    rnd = random.Random(seed)
    for v in o.data.vertices:
        v.co += Vector((rnd.uniform(-1, 1) * axes[0], rnd.uniform(-1, 1) * axes[1], rnd.uniform(-1, 1) * axes[2])) * amt
    o.data.update()
    return o


def lathe(profile, seg=16, material=None, smooth=False, loc=(0, 0, 0), cap_top=True, cap_bot=True,
          phase=0.0, sx=1.0, sy=1.0, name='lathe', rfn=None):
    """Omwentelingslichaam. profile = [(r, z), ...] van onder naar boven. r=0 -> pool.
    rfn(angle, z) -> extra straalfactor (bv. pompoenribben)."""
    bm = bmesh.new(); rings = []
    for (r, z) in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((loc[0], loc[1], loc[2] + z))])
        else:
            ring = []
            for i in range(seg):
                a = TAU * i / seg + phase
                f = rfn(a, z) if rfn else 1.0
                ring.append(bm.verts.new((loc[0] + r * f * math.cos(a) * sx, loc[1] + r * f * math.sin(a) * sy, loc[2] + z)))
            rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap_bot and len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if cap_top and len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    return _link(bm, name, material, smooth)


def frames(pts):
    """Parallel-transport frames langs een polyline: lijst (T, N, B)."""
    pts = [Vector(p) for p in pts]; n = len(pts); out = []
    Ts = []
    for i in range(n):
        if i == 0:
            t = pts[1] - pts[0]
        elif i == n - 1:
            t = pts[-1] - pts[-2]
        else:
            t = (pts[i + 1] - pts[i]).normalized() + (pts[i] - pts[i - 1]).normalized()
        Ts.append(t.normalized())
    up = Vector((0, 0, 1)) if abs(Ts[0].z) < 0.9 else Vector((1, 0, 0))
    N = Ts[0].cross(up).normalized()
    for i in range(n):
        if i > 0:
            N = Ts[i - 1].rotation_difference(Ts[i]) @ N
            N = (N - Ts[i] * N.dot(Ts[i])).normalized()
        out.append((Ts[i], N, Ts[i].cross(N)))
    return out


def tube(pts, r=0.1, seg=6, material=None, smooth=True, cap=True, name='tube', sx=1.0, phase=0.0):
    """Buis langs punten. r = getal of lijst (r=0 -> punt). sx = afplatting."""
    pts = [Vector(p) for p in pts]; n = len(pts)
    rs = r if isinstance(r, (list, tuple)) else [r] * n
    bm = bmesh.new(); rings = []
    for (p, (t, N, B), rr) in zip(pts, frames(pts), rs):
        if rr <= 1e-6:
            rings.append([bm.verts.new(p)])
        else:
            rings.append([bm.verts.new(p + (N * math.cos(TAU * k / seg + phase) * sx + B * math.sin(TAU * k / seg + phase)) * rr) for k in range(seg)])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[j], b[i]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap and len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if cap and len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    return _link(bm, name, material, smooth)


def prism(poly, depth=0.1, material=None, axis='y', loc=(0, 0, 0), name='prism', bevel=0.0, taper=1.0):
    """2D-polygoon (u, v) extruderen. axis 'y': u->x, v->z, dikte langs y (gecentreerd).
    axis 'z': u->x, v->y, dikte langs z (van 0 tot depth). taper schaalt de achterkant."""
    bm = bmesh.new()
    def P(u, v, w):
        if axis == 'y':
            return Vector((u, w, v))
        if axis == 'x':
            return Vector((w, u, v))
        return Vector((u, v, w))
    w0, w1 = (-depth / 2, depth / 2) if axis != 'z' else (0, depth)
    cu = sum(p[0] for p in poly) / len(poly); cv = sum(p[1] for p in poly) / len(poly)
    f = [bm.verts.new(P(u, v, w0)) for u, v in poly]
    b = [bm.verts.new(P(cu + (u - cu) * taper, cv + (v - cv) * taper, w1)) for u, v in poly]
    n = len(poly)
    bm.faces.new(f); bm.faces.new(list(reversed(b)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((f[i], f[j], b[j], b[i]))
    o = _link(bm, name, material, False, recalc=True)
    T(o, loc=loc)
    if bevel > 0:
        bev(o, bevel)
    return o


def circle_pts(r, n, z=0.0, phase=0.0, cx=0.0, cy=0.0):
    return [(cx + r * math.cos(TAU * i / n + phase), cy + r * math.sin(TAU * i / n + phase), z) for i in range(n)]


def arc2d(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / (n - 1)), cy + r * math.sin(a0 + (a1 - a0) * i / (n - 1))) for i in range(n)]


def boolean(o, cutter, op='DIFFERENCE', remove=True):
    m = o.modifiers.new('bool', 'BOOLEAN'); m.object = cutter; m.operation = op; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=m.name)
    if remove:
        bpy.data.objects.remove(cutter)
    return o


def faces_where(o, pred, fn):
    """bmesh-bewerking op faces waarvoor pred(face_center, normal) waar is. fn(bm, faces)."""
    bake(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    fs = [f for f in bm.faces if pred(f.calc_center_median(), f.normal)]
    fn(bm, fs)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def inset(o, pred, thick=0.02, depth=0.0, mat_index=None, individual=True):
    def fn(bm, fs):
        r = bmesh.ops.inset_individual(bm, faces=fs, thickness=thick, depth=depth) if individual else \
            bmesh.ops.inset_region(bm, faces=fs, thickness=thick, depth=depth)
        if mat_index is not None:
            for f in fs:
                f.material_index = mat_index
    return faces_where(o, pred, fn)


def extrude(o, pred, dist=0.1, mat_index=None):
    def fn(bm, fs):
        r = bmesh.ops.extrude_discrete_faces(bm, faces=fs)
        for f in r['faces']:
            for v in f.verts:
                v.co += f.normal * dist
            if mat_index is not None:
                f.material_index = mat_index
    return faces_where(o, pred, fn)


def set_mat(o, material, pred=None):
    """Materiaal toevoegen en (deels) toewijzen."""
    me = o.data
    idx = list(me.materials).index(material) if material.name in [m.name for m in me.materials if m] else None
    if idx is None:
        me.materials.append(material); idx = len(me.materials) - 1
    bake(o)
    for p in me.polygons:
        if pred is None or pred(Vector(p.center), Vector(p.normal)):
            p.material_index = idx
    return o


def flat(o):
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def origin_to(o, point):
    """Oorsprong van object op point zetten (wereld) zonder geometrie te verplaatsen."""
    bake(o)
    p = Vector(point)
    o.data.transform(Matrix.Translation(-p))
    o.location = p
    return o


def decimate(o, ratio=0.5):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def merge(o, dist=0.001):
    bake(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def report():
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    print('TRIS', tris(objs), [(o.name, tris([o])) for o in objs])


def rock(r=1.0, loc=(0, 0, 0), sub=1, material=None, scale=(1, 1, 1), jit=0.15, seed=0, flatbot=True):
    o = ico(r, loc=(0, 0, 0), sub=sub, material=material, scale=scale, jitter=jit * r, seed=seed)
    if flatbot:
        deform(o, lambda v: Vector((v.x, v.y, max(v.z, -0.35 * r * scale[2]))))
        merge(o, 0.02 * r)
    T(o, loc=loc)
    return o


def poly_face(pts, material=None, name='face', y=0.0):
    """Enkel vlak in het XZ-vlak (pts = [(x, z)]), normaal naar -Y."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, z in pts]
    f = bm.faces.new(vs); f.normal_update()
    if f.normal.y > 0:
        f.normal_flip()
    return _link(bm, name, material)


def project(o, target, direction=(0, 1, 0), offset=0.003):
    """Vertices van o langs direction op het oppervlak van target projecteren (decals, gezichten)."""
    from mathutils.bvhtree import BVHTree
    bake(o); bake(target)
    dg = bpy.context.evaluated_depsgraph_get()
    tree = BVHTree.FromObject(target, dg)
    d = Vector(direction).normalized()
    for v in o.data.vertices:
        hit = tree.ray_cast(v.co - d * 10, d)
        if hit[0] is not None:
            v.co = hit[0] - d * offset
    o.data.update()
    return o


def grow(p0, d0, L, n, axis, bend0=0.0, bend1=0.6, seed=0, wob=0.08, shrink=0.4):
    """Punten langs een krullende tak: richting draait per stap rond axis met hoek die van bend0
    naar bend1 loopt (kwadratisch -> krul aan het eind)."""
    rnd = random.Random(seed)
    pts = [Vector(p0)]; d = Vector(d0).normalized(); ax = Vector(axis).normalized(); step = L / n
    for i in range(n):
        t = i / max(n - 1, 1)
        d = Quaternion(ax, bend0 + (bend1 - bend0) * t * t) @ d
        d = (d + Vector((rnd.uniform(-wob, wob), rnd.uniform(-wob, wob), rnd.uniform(-wob, wob)))).normalized()
        pts.append(pts[-1] + d * step * (1 - shrink * t))
    return pts


def taper(n, r0, r1, end=0.0):
    """n stralen van r0 naar r1, laatste = end."""
    return [r0 + (r1 - r0) * i / max(n - 2, 1) for i in range(n - 1)] + [end]


def flip(o):
    """Normalen omdraaien (binnenkant zichtbaar maken)."""
    bake(o); _flip(o); o.data.update()
    return o


def chop(o, cuts=5, seed=0, depth=(0.72, 0.9), minz=-0.2):
    """Willekeurige vlakke afsnijdingen (facetten) -> strakke low-poly rots."""
    bake(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    rnd = random.Random(seed)
    cen = sum((v.co for v in bm.verts), Vector()) / len(bm.verts)
    for i in range(cuts):
        n = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(minz, 1))).normalized()
        mx = max((v.co - cen).dot(n) for v in bm.verts)
        co = cen + n * mx * rnd.uniform(*depth)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=n, clear_outer=True)
        edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
        if edges:
            bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def surface_hit(target, d, center=(0, 0, 0)):
    """Punt + normaal op het oppervlak van target in richting d vanaf center."""
    from mathutils.bvhtree import BVHTree
    bake(target)
    tree = BVHTree.FromObject(target, bpy.context.evaluated_depsgraph_get())
    d = Vector(d).normalized(); c = Vector(center)
    loc, nor, _, _ = tree.ray_cast(c + d * 50, -d)
    return loc, nor


def place_on(o, target, d, center=(0, 0, 0), sink=0.0, spin=0.0):
    """Object (gebouwd rond oorsprong, as +Z) op het oppervlak van target zetten, uitgelijnd op de normaal."""
    loc, nor = surface_hit(target, d, center)
    if loc is None:
        return o
    q = Vector((0, 0, 1)).rotation_difference(nor)
    T(o, rot=(0, 0, spin))
    T(o, rot=q.to_euler(), loc=loc - nor * sink)
    return o


def crater(rc=0.2, material=None, inner=None, seg=8, h=0.05):
    """Kratertje rond oorsprong (as +Z): opstaande rand + kom (binnenkant optioneel donker)."""
    o = lathe([(rc * 1.6, -h * 0.8), (rc, h), (rc * 0.75, -h * 0.2), (0, -h * 1.4)], seg=seg, material=material, cap_bot=False)
    if inner is not None:
        set_mat(o, inner, lambda c, n: math.hypot(c.x, c.y) < rc * 0.8)
    return o
