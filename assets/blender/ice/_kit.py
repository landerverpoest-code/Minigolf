"""Extra vorm-helpers (bovenop mglib) voor de thema's water / ice / desert."""
import sys
sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Quaternion

V = Vector
UP = Vector((0, 0, 1))


def mesh_obj(verts, faces, material=None, name='m', mats=None, face_mats=None):
    """Object uit ruwe verts/faces. mats = lijst materialen, face_mats = index per face."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
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


def _perp(t):
    a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
    n = t.cross(a); n.normalize(); return n


def tube(pts, radii, verts=8, material=None, cap0=True, cap1=True, name='tube', mats=None, ring_mats=None,
         squash=None, twist=0.0, jitter=0.0, seed=1):
    """Buis langs een polylijn. radii = straal per punt (0 aan het eind = punt).
    ring_mats: materiaalindex per segment (len(pts)-1). squash: (sx, sy) ellips-factor per ring (optioneel lijst)."""
    pts = [Vector(p) for p in pts]
    n = len(pts)
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
    rnd = random.Random(seed)
    vs, fs, fm = [], [], []
    rings = []
    for i, (p, r) in enumerate(zip(pts, radii)):
        if r <= 1e-6:
            rings.append([len(vs)]); vs.append(p); continue
        nn, bb = frames[i]; ring = []
        sx, sy = (squash[i] if isinstance(squash, list) else squash) if squash else (1, 1)
        for k in range(verts):
            a = 2 * math.pi * k / verts + twist * i
            j = 1 + (rnd.uniform(-jitter, jitter) if jitter else 0)
            ring.append(len(vs)); vs.append(p + (nn * math.cos(a) * sx + bb * math.sin(a) * sy) * r * j)
        rings.append(ring)
    for i in range(n - 1):
        A, B = rings[i], rings[i + 1]; mi = ring_mats[i] if ring_mats else 0
        if len(A) == 1 and len(B) == 1: continue
        if len(A) == 1:
            for k in range(verts): fs.append((A[0], B[k], B[(k + 1) % verts])); fm.append(mi)
        elif len(B) == 1:
            for k in range(verts): fs.append((A[k], B[0], A[(k + 1) % verts])); fm.append(mi)
        else:
            for k in range(verts): fs.append((A[k], B[k], B[(k + 1) % verts], A[(k + 1) % verts])); fm.append(mi)
    if cap0 and len(rings[0]) > 1: fs.append(tuple(reversed(rings[0]))); fm.append(ring_mats[0] if ring_mats else 0)
    if cap1 and len(rings[-1]) > 1: fs.append(tuple(rings[-1])); fm.append(ring_mats[-1] if ring_mats else 0)
    o = mesh_obj(vs, fs, material, name, mats=mats, face_mats=fm if mats else None)
    _fix_normals(o)
    return o


def lathe(profile, verts=12, material=None, name='lathe', mats=None, band_mats=None, cap0=True, cap1=True,
          loc=(0, 0, 0), jitter=0.0, seed=1, phase=0.0):
    """Omwentelingslichaam rond Z. profile = [(r, z), ...] van onder naar boven. r=0 -> pool.
    band_mats: materiaalindex per profielsegment."""
    loc = Vector(loc); rnd = random.Random(seed)
    vs, fs, fm, rings = [], [], [], []
    for (r, z) in profile:
        if r <= 1e-6:
            rings.append([len(vs)]); vs.append(loc + Vector((0, 0, z))); continue
        ring = []
        for k in range(verts):
            a = 2 * math.pi * k / verts + phase
            j = 1 + (rnd.uniform(-jitter, jitter) if jitter else 0)
            ring.append(len(vs)); vs.append(loc + Vector((math.cos(a) * r * j, math.sin(a) * r * j, z)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]; mi = band_mats[i] if band_mats else 0
        if len(A) == 1 and len(B) == 1: continue
        if len(A) == 1:
            for k in range(verts): fs.append((A[0], B[(k + 1) % verts], B[k])); fm.append(mi)
        elif len(B) == 1:
            for k in range(verts): fs.append((A[k], A[(k + 1) % verts], B[0])); fm.append(mi)
        else:
            for k in range(verts): fs.append((A[k], A[(k + 1) % verts], B[(k + 1) % verts], B[k])); fm.append(mi)
    if cap0 and len(rings[0]) > 1: fs.append(tuple(reversed(rings[0]))); fm.append(band_mats[0] if band_mats else 0)
    if cap1 and len(rings[-1]) > 1: fs.append(tuple(rings[-1])); fm.append(band_mats[-1] if band_mats else 0)
    o = mesh_obj(vs, fs, material, name, mats=mats, face_mats=fm if mats else None)
    _fix_normals(o)
    return o


def _fix_normals(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free(); o.data.update()


def fix_normals(o):
    _fix_normals(o); return o


def frond(base, yaw, length=2.0, width=0.5, rise=0.6, droop=1.2, segs=7, leaf_drop=0.35, material=None,
          name='frond', sweep=1.4, rib=None, roll=0.0):
    """Palmblad: ruggengraat (parabool) met blaadjes-driehoeken aan weerszijden.
    yaw in radialen (richting in XY), rise = beginhelling omhoog, droop = hoe ver de tip onder de basis zakt."""
    base = Vector(base); d = Vector((math.cos(yaw), math.sin(yaw), 0)); side = Vector((-math.sin(yaw), math.cos(yaw), 0))

    def S(t):
        return base + d * (length * t) + UP * (rise * t * 2 - (rise * 2 + droop) * t * t)

    vs, fs = [], []
    sp = [S(i / segs) for i in range(segs + 1)]
    idx = []
    for p in sp: idx.append(len(vs)); vs.append(p)
    for i in range(segs):
        t0 = i / segs; tm = (i + sweep) / segs
        w = width * (math.sin(math.pi * min(0.98, (i + 0.7) / segs)) ** 0.7)
        if i == segs - 1: w *= 0.6
        tip_c = S(min(tm, 1.0))
        tan = (S(min(t0 + 0.01, 1)) - S(t0)).normalized()
        sd = tan.cross(UP).normalized() if abs(tan.z) < 0.99 else side
        for s in (-1, 1):
            off = sd * s * w
            # roll: blad iets gedraaid (één kant hoger)
            tip = tip_c + off - UP * (w * leaf_drop) + UP * (roll * s * w)
            ti = len(vs); vs.append(tip)
            if s > 0: fs.append((idx[i], idx[i + 1], ti))
            else: fs.append((idx[i + 1], idx[i], ti))
    o = mesh_obj(vs, fs, material, name)
    return o


def leaf(base, direction, length=0.5, width=0.2, curl=0.15, fold=0.06, material=None, name='leaf', segs=2):
    """Breed blad (ruit) met middennerf-vouw, licht doorbuigend. direction = Vector (hoeft niet genormaliseerd)."""
    base = Vector(base); d = Vector(direction).normalized()
    sd = d.cross(UP); sd = sd.normalized() if sd.length > 1e-4 else Vector((1, 0, 0))
    nu = sd.cross(d).normalized()
    vs, fs = [], []
    mid = []
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
    # faces
    fs.append((mid[0], mid[1], L[0])); fs.append((mid[0], R[0], mid[1]))
    for i in range(1, segs - 1):
        fs.append((mid[i], mid[i + 1], L[i], L[i - 1])); fs.append((mid[i], R[i - 1], R[i], mid[i + 1]))
    fs.append((mid[segs - 1], mid[segs], L[-1])); fs.append((mid[segs - 1], R[-1], mid[segs]))
    return mesh_obj(vs, fs, material, name)


def rock(r=1.0, loc=(0, 0, 0), scale=(1, 1, 1), seed=0, sub=1, jitter=0.25, material=None, flat_bottom=True, rot_z=0.0):
    """Facetrots: vervormde icosfeer, onderkant afgevlakt."""
    o = ico(r, (0, 0, 0), sub=sub, material=material, scale=scale, jitter=jitter * r, seed=seed)
    if flat_bottom:
        zmin = -0.35 * r * scale[2]
        for v in o.data.vertices:
            if v.co.z < zmin: v.co.z = zmin + (v.co.z - zmin) * 0.15
    o.rotation_euler = (0, 0, rot_z); apply(o)
    o.location = loc
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    return o


def place(o, loc=None, rot=(0, 0, 0), scale=None):
    """Verplaats/draai een object (rond zijn oorsprong) en pas alles toe (ook locatie). loc=None: locatie houden."""
    o.rotation_euler = rot
    if loc is not None: o.location = loc
    if scale is not None: o.scale = scale if hasattr(scale, '__len__') else (scale,) * 3
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def dup(o):
    n = o.copy(); n.data = o.data.copy(); bpy.context.scene.collection.objects.link(n); return n


def set_mat(o, material):
    o.data.materials.clear(); o.data.materials.append(material); return o


def recolor_faces(o, mats, fn):
    """mats: lijst materialen die het object krijgt; fn(polygon) -> index."""
    o.data.materials.clear()
    for m in mats: o.data.materials.append(m)
    for p in o.data.polygons: p.material_index = fn(p)
    return o


def decimate(o, ratio):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def flat(o):
    for p in o.data.polygons: p.use_smooth = False
    return o


def frond2(base, yaw, length=2.0, width=0.5, rise=0.6, droop=1.2, segs=7, leaf_drop=0.4, material=None,
           name='frond', notch=0.45, tipw=0.25):
    """Palmblad als gevouwen strook met zaagtand-rand (blaadjes wijzen naar de tip).
    Rand ligt lager dan de nerf (omgekeerde V)."""
    base = Vector(base); d = Vector((math.cos(yaw), math.sin(yaw), 0))

    def S(t):
        return base + d * (length * t) + UP * (rise * t * 2 - (rise * 2 + droop) * t * t)

    def W(t):
        return width * (tipw + (1 - tipw) * math.sin(math.pi * min(1.0, 0.12 + t * 0.95)) ** 0.8) if t < 1 else 0

    vs, fs = [], []
    sp = []
    for i in range(segs + 1):
        sp.append(len(vs)); vs.append(S(i / segs))
    for i in range(segs):
        t0, t1 = i / segs, (i + 1) / segs
        p0, p1 = S(t0), S(t1)
        tan = (p1 - p0).normalized()
        sd = tan.cross(UP).normalized()
        w1 = W(min(t1, 0.97)) * (0.55 if i == segs - 1 else 1)
        w0 = W(t0) * notch
        for s in (-1, 1):
            n0 = p0 + sd * s * w0 - UP * (w0 * leaf_drop)
            tip = p1 + sd * s * w1 - UP * (w1 * leaf_drop) - tan * (0.15 * length / segs)
            a = len(vs); vs.append(n0); b = len(vs); vs.append(tip)
            if i == segs - 1:
                q = (sp[i], a, b, sp[i + 1])
            else:
                q = (sp[i], a, b, sp[i + 1])
            fs.append(q if s > 0 else tuple(reversed(q)))
    return mesh_obj(vs, fs, material, name)


def join_all(name='model', smooth=None):
    """Alle mesh-objecten behalve spin_* samenvoegen tot één object."""
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.name.startswith('spin_')]
    o = join(objs, name)
    return o


def report():
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    print('TRIS', tris(objs), [(o.name, tris([o])) for o in objs])


SCRATCH = '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/prev'


def closeup(name, size=480, samples=20, dirs=((1.0, -1.25, 0.8), (-1.2, -0.9, 0.35)), fac=0.78, bg='#8fb8de'):
    """Extra controle-render (niet het officiële preview): twee aanzichten naast elkaar, strakker ingekaderd."""
    import os
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs); c = (lo + hi) / 2; dd = hi - lo; ext = max(max(dd.x, dd.y, dd.z), 0.3)
    os.makedirs(SCRATCH, exist_ok=True)
    sun = bpy.data.objects.new('cusun', bpy.data.lights.new('cusun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    if scene.world is None:
        scene.world = bpy.data.worlds.new('w')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (*mglib_lin(bg), 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = samples
    scene.render.resolution_x = scene.render.resolution_y = size
    scene.render.image_settings.file_format = 'PNG'
    for i, dv in enumerate(dirs):
        cam = bpy.data.objects.new('cucam', bpy.data.cameras.new('cucam')); scene.collection.objects.link(cam)
        cam.data.lens = 50
        cam.location = c + Vector(dv).normalized() * ext * fac * 2.0
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler(); scene.camera = cam
        scene.render.filepath = f'{SCRATCH}/{name}_{i}.png'
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(cam)
    bpy.data.objects.remove(sun)


def mglib_lin(c):
    import mglib
    return mglib._lin(c)


def loft(sections, material=None, mats=None, band_mats=None, cap0=True, cap1=True, closed=False, name='loft'):
    """Verbind doorsneden (lijsten punten, gelijke lengte) met quads. Een doorsnede van 1 punt = punt.
    band_mats[j] = materiaalindex voor de strook tussen punt j en j+1 van de doorsnede."""
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
    _fix_normals(o)
    return o


def grid_sheet(corners_fn, nu, nv, material=None, name='sheet'):
    """Vel uit een functie f(u, v) -> Vector, u,v in [0,1]."""
    vs, fs = [], []
    for j in range(nv + 1):
        for i in range(nu + 1):
            vs.append(corners_fn(i / nu, j / nv))
    for j in range(nv):
        for i in range(nu):
            a = j * (nu + 1) + i
            fs.append((a, a + 1, a + nu + 2, a + nu + 1))
    return mesh_obj(vs, fs, material, name)


def snow_cap(o, snow_mat_index, thresh=0.5, lift=0.06, grow=1.03, zmin=-1e9):
    """Bovenvlakken (normaal.z > thresh) uitextruderen als sneeuwlaag met dikte."""
    bm = bmesh.new(); bm.from_mesh(o.data)
    bm.faces.ensure_lookup_table()
    sel = [f for f in bm.faces if f.normal.z > thresh and f.calc_center_median().z > zmin]
    if not sel:
        bm.free(); return o
    res = bmesh.ops.extrude_face_region(bm, geom=sel)
    verts = [e for e in res['geom'] if isinstance(e, bmesh.types.BMVert)]
    faces = [e for e in res['geom'] if isinstance(e, bmesh.types.BMFace)]
    c = sum((v.co for v in verts), Vector()) / max(len(verts), 1)
    for v in verts:
        d = v.co - c; d.z = 0
        v.co += d * (grow - 1) + Vector((0, 0, lift))
    for f in faces:
        f.material_index = snow_mat_index
    # zijkanten van de extrusie ook sneeuw
    for f in bm.faces:
        if all(v in set(verts) or any(e for e in v.link_edges) for v in f.verts) and f not in faces:
            pass
    bmesh.ops.delete(bm, geom=sel, context='FACES')
    for f in bm.faces:
        if any(v in verts for v in f.verts) and f.material_index != snow_mat_index:
            f.material_index = snow_mat_index
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def snow_blanket(o, material, zc_frac=0.55, wave=0.08, grow=1.05, lift=0.03, seed=0, smooth=False):
    """Sneeuwdeken: kopie van het bovenste deel van o (boven zc), iets opgeblazen."""
    s = dup(o)
    s.data.materials.clear(); s.data.materials.append(material)
    lo, hi = bounds([o]); c = (lo + hi) / 2
    zc = lo.z + (hi.z - lo.z) * zc_frac
    rr = random.Random(seed)
    ph = rr.uniform(0, 6.28)
    bm = bmesh.new(); bm.from_mesh(s.data)
    dele = []
    for f in bm.faces:
        m = f.calc_center_median()
        a = math.atan2(m.y - c.y, m.x - c.x)
        if m.z < zc + wave * (hi.z - lo.z) * math.sin(3 * a + ph) or f.normal.z < -0.1:
            dele.append(f)
    bmesh.ops.delete(bm, geom=dele, context='FACES')
    for v in bm.verts:
        d = v.co - Vector((c.x, c.y, c.z - (hi.z - lo.z) * 0.2))
        v.co = Vector((c.x, c.y, c.z - (hi.z - lo.z) * 0.2)) + d * grow + Vector((0, 0, lift))
    # dikte: rand iets naar beneden extruderen
    edges = [e for e in bm.edges if e.is_boundary]
    res = bmesh.ops.extrude_edge_only(bm, edges=edges)
    for v in [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= 0.06 * (hi.z - lo.z)
        v.co.x = c.x + (v.co.x - c.x) * 0.985; v.co.y = c.y + (v.co.y - c.y) * 0.985
    bm.to_mesh(s.data); bm.free(); s.data.update()
    if smooth:
        shade_smooth(s, 45)
    return s
