"""Kit for goose/salamander/horse_rider/guard/snowball/scarab/ferryman (copy of ccp_kit + akit helpers)."""
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix, Euler, Quaternion, noise
from mglib import ROOT, _lin, shade_smooth, bounds

TAU = math.pi * 2
SCRATCH = '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/gkit'
os.makedirs(SCRATCH, exist_ok=True)


def V(*a):
    return Vector(a if len(a) > 1 else a[0])


def _obj(bm, material, name='p', smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        me.materials.append(material)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


def rotm(rot):
    """rot: (x,y,z) degrees -> 4x4."""
    return Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()


def xf(o, M):
    o.data.transform(M); o.data.update(); return o


def ell(c=(0, 0, 0), r=(0.5, 0.5, 0.5), seg=16, rings=10, p=1.0, rot=None, material=None, smooth=True, shape=None):
    """(Super)ellipsoid. p<1 -> boxier. shape(v) optional deform on unit-sphere coords."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in bm.verts:
        n = v.co.copy()
        if p != 1.0:
            n = Vector([math.copysign(abs(k) ** p, k) for k in n])
        if shape:
            n = shape(n)
        v.co = Vector((n.x * r[0], n.y * r[1], n.z * r[2]))
    o = _obj(bm, material, smooth=smooth)
    M = Matrix.Translation(c)
    if rot is not None:
        M = M @ rotm(rot)
    return xf(o, M)


def lathe(profile, seg=16, material=None, M=None, smooth=True):
    """Surface of revolution around local Z. profile = [(r, z), ...] bottom->top. r=0 -> pole."""
    bm = bmesh.new()
    rings = []
    for (r, z) in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(TAU * i / seg), r * math.sin(TAU * i / seg), z)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        if len(a) == 1:
            for i in range(seg):
                bm.faces.new((a[0], b[i], b[(i + 1) % seg]))
        elif len(b) == 1:
            for i in range(seg):
                bm.faces.new((a[i], b[0], a[(i + 1) % seg]))
        else:
            for i in range(seg):
                bm.faces.new((a[i], b[i], b[(i + 1) % seg], a[(i + 1) % seg]))
    if len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    if len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj(bm, material, smooth=smooth)
    if M is not None:
        xf(o, M)
    return o


def tube(pts, radii, seg=8, material=None, cap=True, smooth=True, flat=1.0, round_end=False, flat_n=False):
    """Sweep a circle along a polyline. radii: one per point. flat scales the circle's 2nd axis."""
    pts = [Vector(p) for p in pts]
    if not isinstance(radii, (list, tuple)):
        radii = [radii] * len(pts)
    bm = bmesh.new()
    # tangents
    T = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        T.append((b - a).normalized())
    # initial normal
    up = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    N = (up - T[0] * up.dot(T[0])).normalized()
    rings = []
    for i, p in enumerate(pts):
        if i > 0:  # parallel transport
            q = T[i - 1].rotation_difference(T[i]); N = (q @ N).normalized()
        B = T[i].cross(N)
        ring = []
        for k in range(seg):
            a = TAU * k / seg
            fa, fb = (flat, 1.0) if flat_n else (1.0, flat)
            ring.append(bm.verts.new(p + (N * math.cos(a) * fa + B * math.sin(a) * fb) * radii[i]))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for k in range(seg):
            bm.faces.new((a[k], a[(k + 1) % seg], b[(k + 1) % seg], b[k]))
    if cap:
        for ring, sgn, i in ((rings[0], -1, 0), (rings[-1], 1, len(pts) - 1)):
            if round_end and radii[i] > 1e-5:
                c = bm.verts.new(pts[i] + T[i] * sgn * radii[i] * 0.8)
            else:
                c = bm.verts.new(pts[i])
            for k in range(seg):
                f = (ring[k], ring[(k + 1) % seg], c) if sgn > 0 else (ring[(k + 1) % seg], ring[k], c)
                bm.faces.new(f)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(bm, material, smooth=smooth)


def bezier(p0, p1, p2, p3=None, n=8):
    p0, p1, p2 = Vector(p0), Vector(p1), Vector(p2)
    out = []
    for i in range(n + 1):
        t = i / n
        if p3 is None:
            out.append(p0 * (1 - t) ** 2 + p1 * 2 * (1 - t) * t + p2 * t * t)
        else:
            P3 = Vector(p3)
            out.append(p0 * (1 - t) ** 3 + p1 * 3 * (1 - t) ** 2 * t + p2 * 3 * (1 - t) * t * t + P3 * t ** 3)
    return out


def add_mat(o, m):
    for i, s in enumerate(o.data.materials):
        if s == m:
            return i
    o.data.materials.append(m)
    return len(o.data.materials) - 1


def iso_paint(o, field, m, cut=True):
    """Assign material m to all faces where field(world_co) < 0, after cutting the mesh exactly
    along the field=0 contour (smooth spot / patch borders without extra objects)."""
    mi = add_mat(o, m)
    Mw = o.matrix_world
    bm = bmesh.new(); bm.from_mesh(o.data)
    val = {}
    for v in bm.verts:
        val[v] = field(Mw @ v.co)
    if cut:
        newv = set()
        for e in list(bm.edges):
            a, b = e.verts
            fa, fb = val[a], val[b]
            if (fa < 0) != (fb < 0):
                t = fa / (fa - fb)
                t = min(max(t, 0.08), 0.92)
                pa, pb = a.co.copy(), b.co.copy()
                ne, nv = bmesh.utils.edge_split(e, a, t)
                nv.co = pa.lerp(pb, t)
                val[nv] = 0.0; newv.add(nv)
        for f in list(bm.faces):
            vs = [v for v in f.verts if v in newv]
            if len(vs) == 2:
                try:
                    bmesh.ops.connect_verts(bm, verts=vs)
                except Exception:
                    pass
    for f in bm.faces:
        c = Vector((0, 0, 0))
        for v in f.verts:
            c += v.co
        c /= len(f.verts)
        # use mean of vertex values, ties broken by centroid
        vals = [val.get(v, 0.0) for v in f.verts]
        s = sum(vals) / len(vals)
        if abs(s) < 1e-9:
            s = field(Mw @ c)
        if s < 0:
            f.material_index = mi
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def join(objs, name):
    objs = [o for o in objs if o is not None]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    o = bpy.context.active_object
    o.name = name; o.data.name = name
    return o


def part(objs, name, pivot=(0, 0, 0)):
    """Join into one object called `name`, origin exactly at `pivot` (world), rotation 0."""
    if os.environ.get('CCP_DEBUG'):
        for k in objs:
            k.data.calc_loop_triangles(); print('  SUB', name, len(k.data.loop_triangles), [m.name for m in k.data.materials][:2])
    o = join(objs, name)
    bpy.context.scene.cursor.location = Vector(pivot)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = (0, 0, 0)
    for p in o.data.polygons:
        p.use_smooth = True
    try:
        o.data.set_sharp_from_angle(angle=math.radians(70))
    except Exception:
        pass
    return o


def parent_keep(child, parent):
    """Parent without changing world placement; child keeps zero rotation (parent has none)."""
    w = child.location.copy()
    child.parent = parent
    child.matrix_parent_inverse = Matrix.Identity(4)
    child.location = w - parent.location
    bpy.context.view_layer.update()


def cap(radii, alpha, G=None, seg=10, rings=6, material=None, outer=1.03, inner=0.98):
    """Lens-shaped cap lying ON an ellipsoid (radii) around local -Y, half-angle alpha (rad),
    rotated by G (on the unit sphere, before scaling) -> pupils, highlights, patches."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    G = G or Matrix.Identity(3)
    for v in bm.verts:
        n = v.co.normalized()
        th = math.acos(max(-1.0, min(1.0, -n.y))); ph = math.atan2(n.z, n.x)
        if th <= math.pi / 2 + 1e-6:
            t, rad = th / (math.pi / 2), outer
        else:
            t, rad = (math.pi - th) / (math.pi / 2), inner
        a = alpha * t
        p = G @ (Vector((math.sin(a) * math.cos(ph), -math.cos(a), math.sin(a) * math.sin(ph))) * rad)
        v.co = Vector((p.x * radii[0], p.y * radii[1], p.z * radii[2]))
    return _obj(bm, material)


def eye(c, d=(0, -1, 0), r=0.08, white=None, black=None, depth=0.55, tall=1.15, pupil=0.58, look=(0, 0, 0),
        hl=True, seg=14, up=(0, 0, 1), lid=None, lid_angle=0.0, pseg=10, hlmat=None):
    """Cartoon eye: white ellipsoid + dark pupil lens + white highlight lenses, facing direction d.
    look = (x, _, z) gaze offset in -1..1 (x = toward the eye's local +X)."""
    c = Vector(c); d = Vector(d).normalized(); upv = Vector(up)
    xax = d.cross(upv).normalized()
    zax = xax.cross(d).normalized()
    R = Matrix((xax, -d, zax)).transposed().to_4x4()  # local -Y -> d
    M = Matrix.Translation(c) @ R
    radii = (r, r * depth, r * tall)
    out = [xf(ell((0, 0, 0), radii, seg=seg, rings=seg // 2 + 1, material=white), M)]
    lk = Vector(look)
    G = (Matrix.Rotation(-lk.z * 0.6, 3, 'X') @ Matrix.Rotation(lk.x * 0.6, 3, 'Z'))
    alpha = math.asin(min(pupil, 0.95))
    out.append(xf(cap(radii, alpha, G, seg=pseg, rings=6, material=black, outer=1.03, inner=0.97), M))
    if hl:
        H1 = G @ Matrix.Rotation(-alpha * 0.42, 3, 'X') @ Matrix.Rotation(alpha * 0.4, 3, 'Z')
        out.append(xf(cap(radii, alpha * 0.32, H1, seg=6, rings=4, material=hlmat or white, outer=1.06, inner=1.0), M))
        H2 = G @ Matrix.Rotation(alpha * 0.5, 3, 'X') @ Matrix.Rotation(-alpha * 0.38, 3, 'Z')
        out.append(xf(cap(radii, alpha * 0.14, H2, seg=5, rings=4, material=hlmat or white, outer=1.055, inner=1.0), M))
    if lid is not None:
        L = cap((r * 1.06, r * depth * 1.06, r * tall * 1.06), math.radians(lid_angle), Matrix.Rotation(-math.pi / 2, 3, 'X'),
                seg=seg, rings=6, material=lid, outer=1.0, inner=0.96)
        out.append(xf(L, M))
    return out


# ------------------------------------------------------------------ extra previews
def views(name, pose=None, size=320, samples=16, dirs=None):
    """Extra Cycles renders into the scratchpad: front, side, back; optional posed test."""
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs); c = (lo + hi) / 2; ext = max((hi - lo).length, 0.5)
    cam = bpy.data.objects.new('vcam', bpy.data.cameras.new('vcam')); scene.collection.objects.link(cam)
    cam.data.lens = 50; scene.camera = cam
    sun = bpy.data.objects.new('vsun', bpy.data.lights.new('vsun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    if scene.world is None:
        scene.world = bpy.data.worlds.new('w')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (*_lin('#8fb8de'), 1)
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = samples
    scene.render.resolution_x = scene.render.resolution_y = size
    dirs = dirs or {'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.5), 'top': (0.2, -0.4, 1)}
    for k, dv in dirs.items():
        cam.location = c + Vector(dv).normalized() * ext * 1.6
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = f'{SCRATCH}/{name}_{k}.png'
        bpy.ops.render.render(write_still=True)
    if pose:
        pose()
        bpy.context.view_layer.update()
        cam.location = c + Vector((1.0, -1.25, 0.8)).normalized() * ext * 1.6
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = f'{SCRATCH}/{name}_pose.png'
        bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam); bpy.data.objects.remove(sun)


def report():
    for o in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        if o.type != 'MESH':
            continue
        dg = bpy.context.evaluated_depsgraph_get(); me = o.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
        n = len(me.loop_triangles); o.evaluated_get(dg).to_mesh_clear()
        print('PART', o.name, 'origin', tuple(round(v, 3) for v in o.matrix_world.translation),
              'parent', o.parent.name if o.parent else '-', 'rot', tuple(round(v, 4) for v in o.rotation_euler),
              'tris', n, 'mats', [m.name for m in o.data.materials])



def T(o, loc=(0, 0, 0), rot=(0, 0, 0), scale=None):
    """Bake a transform into the mesh (rot in degrees, applied before loc)."""
    M = Matrix.Translation(Vector(loc)) @ rotm(rot)
    if scale is not None:
        s = scale if isinstance(scale, (tuple, list)) else (scale, scale, scale)
        M = M @ Matrix.Diagonal((*s, 1))
    return xf(o, M)


def frame(o, origin, d, up=(0, 0, 1)):
    """Map local -Y to direction d, local Z ~ up, then move to origin."""
    d = Vector(d).normalized(); upv = Vector(up)
    xax = d.cross(upv).normalized(); zax = xax.cross(d).normalized()
    R = Matrix((xax, -d, zax)).transposed().to_4x4()
    return xf(o, Matrix.Translation(Vector(origin)) @ R)


def flat_shape(points2d, depth, material, M=None, bevel=0.0, smooth=False, curve=0.0):
    """Extrude a closed 2D outline (x, z) along Y (front face at y=-depth/2). curve bends faces (y += curve*x^2)."""
    bm = bmesh.new()
    n = len(points2d)
    fr = [bm.verts.new((x, -depth / 2 + curve * x * x, z)) for x, z in points2d]
    bk = [bm.verts.new((x, depth / 2 + curve * x * x, z)) for x, z in points2d]
    cf = bm.verts.new((sum(p[0] for p in points2d) / n, -depth / 2, sum(p[1] for p in points2d) / n))
    cb = bm.verts.new((cf.co.x, depth / 2, cf.co.z))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((fr[i], fr[j], bk[j], bk[i]))
        bm.faces.new((cf, fr[j], fr[i]))
        bm.faces.new((cb, bk[i], bk[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj(bm, material, smooth=smooth)
    if bevel > 0:
        m = o.modifiers.new('b', 'BEVEL'); m.width = bevel; m.segments = 1; m.limit_method = 'ANGLE'
        bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    if M is not None:
        xf(o, M)
    return o


def gear(R=0.4, r_in=0.12, teeth=10, depth=0.1, tooth=0.08, material=None, holes=0):
    """Flat spur gear lying in XZ plane facing -Y (axle along Y)."""
    pts = []
    for i in range(teeth):
        a0 = TAU * i / teeth
        for (da, rr) in ((0.0, R), (0.18, R), (0.25, R + tooth), (0.5, R + tooth), (0.57, R), (1.0, R)):
            if da == 1.0:
                continue
            a = a0 + da * TAU / teeth
            pts.append((math.cos(a) * rr, math.sin(a) * rr))
    return flat_shape(pts, depth, material)


def spike(base, d, r=0.06, h=0.2, seg=6, material=None):
    """Cone from base along direction d."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=0.0, depth=h)
    o = _obj(bm, material, smooth=False)
    xf(o, Matrix.Translation((0, 0, h / 2)))
    q = Vector((0, 0, 1)).rotation_difference(Vector(d).normalized())
    return xf(o, Matrix.Translation(Vector(base)) @ q.to_matrix().to_4x4())


def cyl_between(a, b, r, seg=8, material=None, r2=None, smooth=True):
    a, b = Vector(a), Vector(b)
    return tube([a, b], [r, r if r2 is None else r2], seg=seg, material=material, smooth=smooth)


def dup_baked(o, name='dup'):
    me = o.data.copy()
    me.transform(o.matrix_world)
    d = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(d)
    return d


def views2(name, dirs=None, size=360, samples=20, pose=None, focus=None, dist=1.6):
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.type == 'MESH' and not o.hide_render]
    lo, hi = bounds(objs); c = (lo + hi) / 2; ext = max((hi - lo).length, 0.5)
    if focus is not None:
        c = Vector(focus[0]); ext = focus[1]
    cam = bpy.data.objects.new('vcam', bpy.data.cameras.new('vcam')); scene.collection.objects.link(cam)
    cam.data.lens = 50; scene.camera = cam
    sun = bpy.data.objects.new('vsun', bpy.data.lights.new('vsun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    if scene.world is None:
        scene.world = bpy.data.worlds.new('w')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (*_lin('#8fb8de'), 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = samples
    scene.render.resolution_x = scene.render.resolution_y = size
    dirs = dirs or {'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (-0.7, 1, 0.5)}
    if pose:
        pose(); bpy.context.view_layer.update()
    for k, dv in dirs.items():
        cam.location = c + Vector(dv).normalized() * ext * dist
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = f'{SCRATCH}/{name}_{k}.png'
        bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam); bpy.data.objects.remove(sun)


def smooth_sharp(o, angle=55):
    for p in o.data.polygons:
        p.use_smooth = True
    try:
        o.data.set_sharp_from_angle(angle=math.radians(angle))
    except Exception:
        pass
    return o


def fmt(v):
    return '(%s)' % ','.join(('%.3f' % x).rstrip('0').rstrip('.') if abs(x) > 1e-9 else '0' for x in v)


def clean(o, dist=1e-4, angle=1.0):
    """Merge duplicate verts and dissolve coplanar faces (flattened poles, lathe caps) to save triangles."""
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle), verts=bm.verts, edges=bm.edges,
                             delimit={'MATERIAL'})
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def decimate(o, ratio):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio; m.use_collapse_triangulate = True
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def apart(objs, name, pivot=(0, 0, 0), angle=1.0, ratio=None):
    for k in objs:
        if k is not None:
            clean(k, angle=angle)
    o = part(objs, name, pivot)
    if ratio:
        decimate(o, ratio)
        smooth_sharp(o, 70)
    return o


def tri_count(o):
    o.data.calc_loop_triangles(); return len(o.data.loop_triangles)


def scale_all(s):
    """Uniformly scale the whole character about the world origin (geometry + part origins)."""
    for o in bpy.context.scene.objects:
        if o.type != 'MESH':
            continue
        o.data.transform(Matrix.Diagonal((s, s, s, 1)))
        if o.parent is None:
            o.location = o.location * s
        else:
            o.location = o.location * s
    bpy.context.view_layer.update()


def surf_blob(targets, origin, direction, r=(0.05, 0.05), h=0.012, material=None, seg=8, rings=4, sink=0.35, spin=0.0):
    """Flattened ellipsoid 'decal' stuck onto the first surface hit by a ray (origin -> direction) on any target.
    r = radii along the surface, h = thickness. Returns the object or None."""
    best = None
    for t in targets:
        bpy.context.view_layer.update()
        ok, loc, nrm, idx = t.ray_cast(Vector(origin), Vector(direction).normalized())
        if ok:
            d = (loc - Vector(origin)).length
            if best is None or d < best[0]:
                best = (d, loc, nrm)
    if best is None:
        return None
    _, loc, nrm = best
    o = ell((0, 0, 0), (r[0], h, r[1]), seg=seg, rings=rings, material=material)
    xf(o, rotm((0, spin, 0)))
    return frame(o, loc - nrm * h * sink, -nrm, up=(0, 1, 0) if abs(nrm.z) > 0.9 else (0, 0, 1))
