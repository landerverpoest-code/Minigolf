"""Agent A kit (knight, dragon, drone, boulder) on top of mglib + ccp_kit (read-only use of ccp_kit)."""
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix, Euler, noise
from mglib import ROOT, _lin, bounds, render_preview
from ccp_kit import (V, _obj, rotm, xf, ell, lathe, tube, bezier, add_mat, iso_paint, join, part, parent_keep, cap,
                     report, TAU)

SCRATCH = '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/agentA'
os.makedirs(SCRATCH, exist_ok=True)


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


def views(name, dirs=None, size=360, samples=20, pose=None, focus=None, dist=1.6):
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
