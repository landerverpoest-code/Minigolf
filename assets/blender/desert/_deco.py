"""Modelleerhelpers voor de extra decoratie (ronde 2), bovenop mglib.
Identieke kopie staat in elke themamap (meadow, volcano, castle, water, ice, desert, haunted, space, finale).

Gebruik:
    import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
    from mglib import *
    reset()
    sys.path.insert(0, '/home/user/Minigolf/assets/blender/<thema>'); from _deco import *
    ...
    done('<thema>', '<naam>', kind='scatter', footprint=0.5, notes='...')

Conventie: alle helpers leveren objecten met de geometrie in wereldcoordinaten (objecttransform = identiteit).
"""
import sys
sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
import mglib
import bpy, bmesh, math, random, os
from mathutils import Vector, Matrix, Euler, Quaternion, noise

V = Vector
TAU = math.tau
UP = Vector((0, 0, 1))
SCRATCH = '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/prev'
LIMITS = {'edge': (300, 25 * 1024), 'scatter': (900, 45 * 1024), 'post': (900, 45 * 1024), 'hero': (5000, 200 * 1024)}


# ---------------------------------------------------------------- basis
def mesh_obj(verts, faces, material=None, name='m', mats=None, face_mats=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update(calc_edges=True)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    if mats:
        for m in mats:
            me.materials.append(m)
        if face_mats:
            for p, i in zip(me.polygons, face_mats):
                p.material_index = i
    elif material is not None:
        me.materials.append(material)
    bpy.context.view_layer.objects.active = o
    return o


def fix_normals(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def bake(o):
    """Objecttransform in de mesh bakken."""
    if o.matrix_basis != Matrix.Identity(4):
        o.data.transform(o.matrix_basis)
        o.matrix_basis = Matrix.Identity(4)
    return o


def T(o, loc=None, rot=None, scale=None, pivot=None):
    """Transformatie in de mesh bakken (wereldruimte). Volgorde: schaal, rotatie (graden XYZ), verplaatsing.
    pivot: schaal/draai rond dit punt i.p.v. de oorsprong."""
    bake(o)
    M = Matrix.Identity(4)
    if scale is not None:
        if isinstance(scale, (int, float)):
            scale = (scale, scale, scale)
        M = Matrix.Diagonal((*scale, 1)) @ M
    if rot is not None:
        M = Euler([math.radians(a) for a in rot]).to_matrix().to_4x4() @ M
    if pivot is not None:
        P = Matrix.Translation(Vector(pivot))
        M = P @ M @ P.inverted()
    if loc is not None:
        M = Matrix.Translation(Vector(loc)) @ M
    o.data.transform(M)
    if M.determinant() < 0:
        fix_normals(o)
    o.data.update()
    return o


def dup(o, loc=None, rot=None, scale=None, material=None, pivot=None):
    n = o.copy(); n.data = o.data.copy()
    bpy.context.scene.collection.objects.link(n)
    if material is not None:
        set_mat(n, material)
    return T(n, loc, rot, scale, pivot)


def set_mat(o, m):
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons:
        p.material_index = 0
    return o


def recolor(o, mats, fn):
    """mats: materialen; fn(polygon) -> index (of None = huidige index houden)."""
    old = [o.data.materials[p.material_index].name if o.data.materials else None for p in o.data.polygons]
    o.data.materials.clear()
    for m in mats:
        o.data.materials.append(m)
    names = [m.name for m in mats]
    for p, on in zip(o.data.polygons, old):
        i = fn(p)
        if i is None:
            i = names.index(on) if on in names else 0
        p.material_index = i
    return o


def flat(o):
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def smooth(o, angle=50):
    return shade_smooth(o, angle)


def deform(o, fn):
    """fn(co: Vector) -> nieuwe co."""
    bake(o)
    for v in o.data.vertices:
        v.co = Vector(fn(v.co.copy()))
    o.data.update()
    return o


def lumpy(o, amp=0.1, freq=1.0, seed=0, axes=(1, 1, 1)):
    bake(o)
    off = Vector((seed * 13.1, seed * 7.7, seed * 3.3))
    for v in o.data.vertices:
        n = noise.noise_vector(v.co * freq + off)
        v.co += Vector((n.x * axes[0], n.y * axes[1], n.z * axes[2])) * amp
    o.data.update()
    return o


def jitter(o, amp=0.05, seed=0, axes=(1, 1, 1)):
    bake(o)
    rnd = random.Random(seed); cache = {}
    for v in o.data.vertices:
        k = (round(v.co.x, 4), round(v.co.y, 4), round(v.co.z, 4))
        if k not in cache:
            cache[k] = Vector((rnd.uniform(-1, 1) * axes[0], rnd.uniform(-1, 1) * axes[1], rnd.uniform(-1, 1) * axes[2])) * amp
        v.co += cache[k]
    o.data.update()
    return o


def taper(o, f_top=0.5, z0=None, z1=None, cx=0.0, cy=0.0):
    bake(o)
    zs = [v.co.z for v in o.data.vertices]
    z0 = min(zs) if z0 is None else z0
    z1 = max(zs) if z1 is None else z1
    for v in o.data.vertices:
        t = max(0, min(1, (v.co.z - z0) / ((z1 - z0) or 1)))
        s = 1 + (f_top - 1) * t
        v.co.x = cx + (v.co.x - cx) * s; v.co.y = cy + (v.co.y - cy) * s
    o.data.update()
    return o


def merge(o, dist=0.0005):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def clip_below(o, z=0.0):
    """Alles onder hoogte z wegsnijden en het gat dichten (half begraven dingen)."""
    bake(o)
    bm = bmesh.new(); bm.from_mesh(o.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    res = bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-5, plane_co=(0, 0, z), plane_no=(0, 0, -1), clear_outer=True)
    edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    if edges:
        bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def decimate(o, ratio):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def boolean(o, cutter, op='DIFFERENCE', solver='EXACT'):
    m = o.modifiers.new('bool', 'BOOLEAN'); m.object = cutter; m.operation = op; m.solver = solver
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter)
    return o


def inset_faces(o, pred, thick=0.02, depth=0.0, mat_index=None):
    """Vlakken waarvoor pred(face) waar is inzetten (bv. ramen, panelen)."""
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    faces = [f for f in bm.faces if pred(f)]
    if faces:
        res = bmesh.ops.inset_individual(bm, faces=faces, thickness=thick, depth=depth)
        if mat_index is not None:
            for f in faces:
                f.material_index = mat_index
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


# ---------------------------------------------------------------- vormen
def rod(p0, p1, r=0.05, r2=None, verts=6, material=None, smooth=False):
    """Cilinder/kegelstomp van p0 naar p1."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = cyl(r, d.length, loc=(0, 0, 0), verts=verts, material=material, r2=r2, smooth=smooth)
    q = d.to_track_quat('Z', 'Y')
    o.data.transform(Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4())
    o.data.update()
    return o


def plank(p0, p1, w=0.1, t=0.03, up=(0, 0, 1), material=None, bevel=0.0):
    """Balk van p0 naar p1: breedte w, dikte t (dikte langs 'up')."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = box((w, t, d.length), material=material)
    z = d.normalized(); u = Vector(up).normalized()
    if abs(z.dot(u)) > 0.99:
        u = Vector((0, 1, 0)) if abs(z.y) < 0.9 else Vector((1, 0, 0))
    y = (u - z * u.dot(z)).normalized()
    x = y.cross(z).normalized()
    m = Matrix((x, y, z)).transposed().to_4x4()
    o.data.transform(Matrix.Translation((p0 + p1) / 2) @ m)
    o.data.update()
    if bevel:
        bev(o, bevel)
    return o


def _perp(t):
    a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
    n = t.cross(a); n.normalize(); return n


def tube(pts, radii, verts=8, material=None, cap0=True, cap1=True, name='tube', mats=None, ring_mats=None,
         squash=None, twist=0.0, smooth=False, phase=0.0):
    """Buis langs een polylijn. radii: getal of straal per punt (0 = punt)."""
    pts = [Vector(p) for p in pts]
    n = len(pts)
    if isinstance(radii, (int, float)):
        radii = [radii] * n
    tans = []
    for i in range(n):
        if i == 0: t = pts[1] - pts[0]
        elif i == n - 1: t = pts[-1] - pts[-2]
        else: t = (pts[i + 1] - pts[i]).normalized() + (pts[i] - pts[i - 1]).normalized()
        tans.append(t.normalized())
    nrm = _perp(tans[0]); frames = []
    for i in range(n):
        if i > 0:
            q = tans[i - 1].rotation_difference(tans[i]); nrm = q @ nrm
            nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
        frames.append((nrm.copy(), tans[i].cross(nrm).normalized()))
    vs, fs, fm, rings = [], [], [], []
    for i, (p, r) in enumerate(zip(pts, radii)):
        if r <= 1e-6:
            rings.append([len(vs)]); vs.append(p); continue
        nn, bb = frames[i]; ring = []
        sx, sy = (squash[i] if isinstance(squash, list) else squash) if squash else (1, 1)
        for k in range(verts):
            a = TAU * k / verts + twist * i + phase
            ring.append(len(vs)); vs.append(p + (nn * math.cos(a) * sx + bb * math.sin(a) * sy) * r)
        rings.append(ring)
    for i in range(n - 1):
        A, B = rings[i], rings[i + 1]; mi = ring_mats[i] if ring_mats else 0
        if len(A) == 1 and len(B) == 1: continue
        for k in range(verts):
            k2 = (k + 1) % verts
            if len(A) == 1: fs.append((A[0], B[k], B[k2]))
            elif len(B) == 1: fs.append((A[k], B[0], A[k2]))
            else: fs.append((A[k], B[k], B[k2], A[k2]))
            fm.append(mi)
    if cap0 and len(rings[0]) > 1: fs.append(tuple(reversed(rings[0]))); fm.append(ring_mats[0] if ring_mats else 0)
    if cap1 and len(rings[-1]) > 1: fs.append(tuple(rings[-1])); fm.append(ring_mats[-1] if ring_mats else 0)
    o = mesh_obj(vs, fs, material, name, mats=mats, face_mats=fm if mats else None)
    fix_normals(o)
    if smooth:
        shade_smooth(o, 60 if smooth is True else smooth)
    return o


def lathe(profile, verts=12, material=None, name='lathe', mats=None, band_mats=None, cap0=True, cap1=True,
          loc=(0, 0, 0), jitter=0.0, seed=1, phase=0.0, smooth=False, sx=1.0, sy=1.0):
    """Omwentelingslichaam rond Z: profile = [(r, z), ...] van onder naar boven (r=0 = pool).
    band_mats: materiaalindex per profielsegment."""
    loc = Vector(loc); rnd = random.Random(seed)
    vs, fs, fm, rings = [], [], [], []
    for (r, z) in profile:
        if r <= 1e-6:
            rings.append([len(vs)]); vs.append(loc + Vector((0, 0, z))); continue
        ring = []
        for k in range(verts):
            a = TAU * k / verts + phase
            j = 1 + (rnd.uniform(-jitter, jitter) if jitter else 0)
            ring.append(len(vs)); vs.append(loc + Vector((math.cos(a) * r * j * sx, math.sin(a) * r * j * sy, z)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]; mi = band_mats[i] if band_mats else 0
        if len(A) == 1 and len(B) == 1: continue
        for k in range(verts):
            k2 = (k + 1) % verts
            if len(A) == 1: fs.append((A[0], B[k2], B[k]))
            elif len(B) == 1: fs.append((A[k], A[k2], B[0]))
            else: fs.append((A[k], A[k2], B[k2], B[k]))
            fm.append(mi)
    if cap0 and len(rings[0]) > 1: fs.append(tuple(reversed(rings[0]))); fm.append(band_mats[0] if band_mats else 0)
    if cap1 and len(rings[-1]) > 1: fs.append(tuple(rings[-1])); fm.append(band_mats[-1] if band_mats else 0)
    o = mesh_obj(vs, fs, material, name, mats=mats, face_mats=fm if mats else None)
    fix_normals(o)
    if smooth:
        shade_smooth(o, 60 if smooth is True else smooth)
    return o


def loft(sections, material=None, mats=None, band_mats=None, cap0=True, cap1=True, closed=True, name='loft', smooth=False):
    """Verbind doorsneden (lijsten punten, gelijke lengte) met quads."""
    vs, fs, fm, rings = [], [], [], []
    for sec in sections:
        r = []
        for p in sec:
            r.append(len(vs)); vs.append(Vector(p))
        rings.append(r)
    n = max(len(s) for s in sections)
    m = n if closed else n - 1
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        for j in range(m):
            j2 = (j + 1) % n; mi = band_mats[j] if band_mats else 0
            if len(A) == 1: f = (A[0], B[j], B[j2])
            elif len(B) == 1: f = (A[j], B[0], A[j2])
            else: f = (A[j], B[j], B[j2], A[j2])
            fs.append(f); fm.append(mi)
    if cap0 and len(rings[0]) > 2: fs.append(tuple(reversed(rings[0]))); fm.append(band_mats[0] if band_mats else 0)
    if cap1 and len(rings[-1]) > 2: fs.append(tuple(rings[-1])); fm.append(band_mats[0] if band_mats else 0)
    o = mesh_obj(vs, fs, material, name, mats=mats, face_mats=fm if mats else None)
    fix_normals(o)
    if smooth:
        shade_smooth(o, 60 if smooth is True else smooth)
    return o


def prism(profile, depth, material=None, axis='Y', loc=(0, 0, 0), name='prism'):
    """2D-profiel [(a, b), ...] extruderen, gecentreerd. axis='Y': (a,b)=(x,z) over Y; 'X': (a,b)=(y,z) over X;
    'Z': (a,b)=(x,y) van z=0 tot depth."""
    h = depth / 2
    if axis == 'Y':
        f = [(a, -h, b) for a, b in profile]; bk = [(a, h, b) for a, b in profile]
    elif axis == 'X':
        f = [(-h, a, b) for a, b in profile]; bk = [(h, a, b) for a, b in profile]
    else:
        f = [(a, b, 0) for a, b in profile]; bk = [(a, b, depth) for a, b in profile]
    n = len(profile)
    vs = f + bk
    fs = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        fs.append((i, j, n + j, n + i))
    o = mesh_obj([Vector(v) + Vector(loc) for v in vs], fs, material, name)
    fix_normals(o)
    return o


def grid_sheet(fn, nu, nv, material=None, name='sheet'):
    """Vel uit fn(u, v) -> punt, u, v in [0, 1]."""
    vs, fs = [], []
    for j in range(nv + 1):
        for i in range(nu + 1):
            vs.append(Vector(fn(i / nu, j / nv)))
    for j in range(nv):
        for i in range(nu):
            a = j * (nu + 1) + i
            fs.append((a, a + 1, a + nu + 2, a + nu + 1))
    return mesh_obj(vs, fs, material, name)


def slab(fn, nu, nv, thick, material=None, name='slab'):
    """Vel met dikte (solidify langs normaal)."""
    o = grid_sheet(fn, nu, nv, material, name)
    m = o.modifiers.new('sol', 'SOLIDIFY'); m.thickness = thick; m.offset = 0
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def rock(r=1.0, loc=(0, 0, 0), scale=(1, 1, 1), seed=0, sub=1, jit=0.25, material=None, flat_bottom=True, rot_z=0.0):
    """Facetrots: vervormde icosfeer, onderkant afgevlakt."""
    o = ico(r, (0, 0, 0), sub=sub, material=material, scale=scale, jitter=jit * r, seed=seed)
    if flat_bottom:
        zmin = -0.35 * r * scale[2]
        for v in o.data.vertices:
            if v.co.z < zmin: v.co.z = zmin + (v.co.z - zmin) * 0.15
    return T(o, loc=loc, rot=(0, 0, math.degrees(rot_z)))


def chunk(r=0.5, scale=(1, 1, 1), cuts=10, seed=0, material=None, depth=(0.55, 0.9), base_sub=2, flat_bottom=None, loc=(0, 0, 0)):
    """Gefacetteerde rots: icosfeer afgesneden met willekeurige vlakken."""
    rnd = random.Random(seed)
    o = ico(r, sub=base_sub, material=material, scale=scale)
    bm = bmesh.new(); bm.from_mesh(o.data)
    planes = []
    for k in range(cuts):
        n = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1) * 0.8)).normalized()
        planes.append((n, rnd.uniform(*depth)))
    if flat_bottom is not None:
        planes.append((Vector((0, 0, -1)), flat_bottom))
    for n, d in planes:
        ext = Vector((abs(n.x) * scale[0], abs(n.y) * scale[1], abs(n.z) * scale[2])).length
        co = n * d * r * ext
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        res = bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-5, plane_co=co, plane_no=n, clear_outer=True)
        cut_edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
        if cut_edges:
            bmesh.ops.holes_fill(bm, edges=cut_edges, sides=0)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(2), verts=bm.verts, edges=bm.edges)
    bm.to_mesh(o.data); bm.free()
    o.data.update(); flat(o)
    return T(o, loc=loc)


def leaf(base, direction, length=0.5, width=0.2, curl=0.15, fold=0.06, material=None, name='leaf', segs=2):
    """Breed blad met middennerf-vouw, licht doorbuigend."""
    base = Vector(base); d = Vector(direction).normalized()
    sd = d.cross(UP); sd = sd.normalized() if sd.length > 1e-4 else Vector((1, 0, 0))
    nu = sd.cross(d).normalized()
    vs, fs, mid = [], [], []
    for i in range(segs + 1):
        t = i / segs
        p = base + d * (length * t) - nu * (curl * t * t * length / 0.5)
        mid.append(len(vs)); vs.append(p)
    L, R = [], []
    for i in range(1, segs):
        t = i / segs
        w = width * math.sin(math.pi * (0.15 + 0.7 * t)) if segs > 1 else width
        p = vs[mid[i]]
        L.append(len(vs)); vs.append(p - sd * w - nu * fold)
        R.append(len(vs)); vs.append(p + sd * w - nu * fold)
    fs.append((mid[0], mid[1], L[0])); fs.append((mid[0], R[0], mid[1]))
    for i in range(1, segs - 1):
        fs.append((mid[i], mid[i + 1], L[i], L[i - 1])); fs.append((mid[i], R[i - 1], R[i], mid[i + 1]))
    fs.append((mid[segs - 1], mid[segs], L[-1])); fs.append((mid[segs - 1], R[-1], mid[segs]))
    return mesh_obj(vs, fs, material, name)


def flower_head(R=0.05, rc=0.015, petals=5, cup=0.012, petal_mat=None, heart_mat=None, wide=0.75):
    """Bloemhoofdje rond de oorsprong, kijkt naar +Z."""
    vs, fs = [], []
    for i in range(petals):
        a = TAU * i / petals
        vs.append((rc * math.cos(a), rc * math.sin(a), 0.004))
    half = math.pi / petals * 0.85
    for i in range(petals):
        a = TAU * (i + 0.5) / petals
        vs.append((R * math.cos(a - half * wide), R * math.sin(a - half * wide), cup))
        vs.append((R * math.cos(a + half * wide), R * math.sin(a + half * wide), cup))
    fs.append(list(range(petals)))
    for i in range(petals):
        j = (i + 1) % petals
        fs.append((i, petals + 2 * i, petals + 2 * i + 1, j))
    o = mesh_obj(vs, fs, petal_mat, 'flower')
    if heart_mat is not None:
        o.data.materials.append(heart_mat)
        o.data.polygons[0].material_index = 1
    return o


def dust(o, material, thresh=0.7, noise_amt=0.0, seed=0):
    """Vlakken die naar boven wijzen krijgen een ander materiaal (sneeuw, mos, as)."""
    if material.name not in [m.name for m in o.data.materials]:
        o.data.materials.append(material)
    idx = [m.name for m in o.data.materials].index(material.name)
    off = Vector((seed * 1.3, seed * 0.7, 0))
    for p in o.data.polygons:
        if p.normal.z + noise_amt * noise.noise(p.center * 2 + off) > thresh:
            p.material_index = idx
    return o


def orient(o, normal, loc):
    """Object (gemaakt rond de oorsprong, as = +Z) naar normal draaien en op loc zetten."""
    bake(o)
    q = Vector(normal).normalized().to_track_quat('Z', 'Y')
    o.data.transform(Matrix.Translation(Vector(loc)) @ q.to_matrix().to_4x4())
    o.data.update()
    return o


def blob(spheres, center=None, sub=2, material=None, name='blob', smooth=True, angle=38):
    """Wolkvorm: unie van bollen [(centrum, straal), ...] als één icosfeer (stralen vanuit 'center').
    Mooi voor wol, bladkruinen, sneeuwhopen, rook."""
    cs = [(Vector(c), r) for c, r in spheres]
    if center is None:
        center = sum((c for c, _ in cs), Vector()) / len(cs)
    center = Vector(center)
    o = ico(1.0, sub=sub, material=material)
    for v in o.data.vertices:
        d = v.co.normalized(); best = 0.0
        for c, r in cs:
            oc = center - c
            b = oc.dot(d); disc = b * b - (oc.dot(oc) - r * r)
            if disc >= 0:
                t = -b + math.sqrt(disc)
                best = max(best, t)
        v.co = center + d * max(best, 0.02)
    o.data.update(); o.name = name
    if smooth:
        shade_smooth(o, angle)
    return o


def circle_pts(r, n, z=0.0, phase=0.0, cx=0.0, cy=0.0):
    return [Vector((cx + r * math.cos(TAU * i / n + phase), cy + r * math.sin(TAU * i / n + phase), z)) for i in range(n)]


# ---------------------------------------------------------------- afronden
def join_all(name='model'):
    """Alle mesh-objecten behalve spin_* samenvoegen."""
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.name.startswith('spin_')]
    if os.environ.get('PARTS'):
        from collections import Counter
        c = Counter()
        for o in objs:
            c[o.name.split('.')[0] + ':' + (o.data.materials[0].name if o.data.materials else '-')] += tris([o])
        print('PARTS', c.most_common(25))
    return join(objs, name)


def report():
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    print('TRIS', tris(objs))


def _load_px(path):
    import numpy as np
    im = bpy.data.images.load(path)
    w, h = im.size
    px = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return px.reshape(h, w, 4)


def _save_px(arr, path):
    h, w = arr.shape[:2]
    im = bpy.data.images.new('comb', w, h, alpha=True)
    im.pixels.foreach_set(arr.ravel())
    im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    bpy.data.images.remove(im)


def closeup(theme, name, size=384, samples=20, views=((-1.1, 0.9, 0.55), (0.15, -1.0, 0.35)), fac=0.8, bg='#8fb8de'):
    """Controle-renders (niet het officiele preview): extra aanzichten, samen met het preview in één PNG in SCRATCH."""
    import numpy as np
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs); c = (lo + hi) / 2; dd = hi - lo; ext = max(max(dd.x, dd.y, dd.z), 0.3)
    os.makedirs(SCRATCH, exist_ok=True)
    sun = bpy.data.objects.new('cusun', bpy.data.lights.new('cusun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    if scene.world is None:
        scene.world = bpy.data.worlds.new('w')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (*mglib._lin(bg), 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = samples
    scene.render.resolution_x = scene.render.resolution_y = size
    scene.render.image_settings.file_format = 'PNG'
    paths = [f'{ROOT}/previews/{theme}/{name}.png']
    for i, dv in enumerate(views):
        cam = bpy.data.objects.new('cucam', bpy.data.cameras.new('cucam')); scene.collection.objects.link(cam)
        cam.data.lens = 50
        cam.location = c + Vector(dv).normalized() * ext * fac * 2.0
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler(); scene.camera = cam
        p = f'{SCRATCH}/{theme}_{name}_{i}.png'
        scene.render.filepath = p
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(cam)
        paths.append(p)
    bpy.data.objects.remove(sun)
    arrs = [_load_px(p) for p in paths]
    h = min(a.shape[0] for a in arrs)
    comb = np.concatenate([a[:h, :h] for a in arrs], axis=1)
    out = f'{SCRATCH}/{theme}_{name}_all.png'
    _save_px(comb, out)
    print('CLOSEUP', out)


def center_xy():
    """Alles verschuiven zodat het midden van de bounding box (x, y) op de oorsprong ligt."""
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs); c = (lo + hi) / 2
    for o in objs:
        o.location.x -= c.x; o.location.y -= c.y
    bpy.context.view_layer.update()


def done(theme, name, kind='scatter', footprint=0.5, notes='', check=True, center=False, **extra):
    """finish() + budgetcontrole + controle-renders. center=True: bounding box in x/y centreren."""
    if center:
        center_xy()
    e = finish(theme, name, kind=kind, footprint=footprint, notes=notes, **extra)
    lt, lb = LIMITS[kind]
    ok = e['tris'] <= lt and e['bytes'] <= lb
    print(f"BUDGET {'OK' if ok else 'OVER'}: {e['tris']}/{lt} tris, {e['bytes']}/{lb} bytes, h={e['height']} size={e['size']} fp={footprint}")
    if check:
        closeup(theme, name)
    return e
