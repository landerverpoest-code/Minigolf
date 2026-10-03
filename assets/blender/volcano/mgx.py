"""Extra modelleerhelpers (bovenop mglib) voor de thema's meadow / volcano / castle.
Gebruik na `from mglib import *`:  sys.path.insert(0, os.path.dirname(__file__)); from mgx import *
"""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler, Quaternion, noise
from mglib import mat, box, cyl, cone, sphere, ico, torus, apply, bev, shade_smooth, join, tris, bounds

TAU = math.pi * 2


def V(*a):
    return Vector(a if len(a) > 1 else a[0])


def rod(p0, p1, r=0.05, r2=None, verts=6, material=None, smooth=False):
    """Cilinder/kegelstomp van punt p0 naar p1 (r onderaan, r2 bovenaan)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = cyl(r, d.length, loc=(0, 0, 0), verts=verts, material=material, r2=r2 if r2 is not None else None, smooth=smooth)
    q = d.to_track_quat('Z', 'Y')
    o.data.transform(q.to_matrix().to_4x4())
    o.location = (p0 + p1) / 2
    return o


def plank(p0, p1, w=0.1, t=0.03, up=(0, 0, 1), material=None, bevel=0.0):
    """Balk/plank van p0 naar p1, breedte w, dikte t (dikte langs 'up' x richting)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0)
    L = d.length
    o = box((w, t, L), material=material)
    z = d.normalized()
    u = Vector(up)
    if abs(z.dot(u.normalized())) > 0.99:
        u = Vector((0, 1, 0)) if abs(z.y) < 0.9 else Vector((1, 0, 0))
    x = u.cross(z).normalized()
    y = z.cross(x).normalized()
    m = Matrix((x, y, z)).transposed().to_4x4()
    o.data.transform(m)
    o.location = (p0 + p1) / 2
    if bevel:
        bev(o, bevel)
    return o


def xform(o, loc=None, rot=None, scale=None):
    """Transformatie in de mesh bakken, in wereldruimte (objectlocatie wordt eerst gebakken). rot in graden, XYZ."""
    if o.location.length > 0:
        bake_loc(o)
    M = Matrix.Identity(4)
    if scale is not None:
        if isinstance(scale, (int, float)):
            scale = (scale, scale, scale)
        M = Matrix.Diagonal((*scale, 1)) @ M
    if rot is not None:
        M = Euler([math.radians(a) for a in rot]).to_matrix().to_4x4() @ M
    if loc is not None:
        M = Matrix.Translation(loc) @ M
    o.data.transform(M)
    o.data.update()
    return o


def dup(o, loc=None, rot=None, scale=None, material=None):
    """Kopie (eigen mesh-data) met extra transformatie (rond oorsprong van de mesh)."""
    n = o.copy()
    n.data = o.data.copy()
    bpy.context.scene.collection.objects.link(n)
    if material is not None:
        n.data.materials.clear(); n.data.materials.append(material)
    xform(n, loc, rot, scale)
    return n


def bake_loc(o):
    """Objectlocatie in de mesh bakken (oorsprong naar wereld-0)."""
    o.data.transform(Matrix.Translation(o.location))
    o.location = (0, 0, 0)
    return o


def set_origin(o, p):
    """Oorsprong van het object naar wereldpunt p verplaatsen zonder de mesh te verschuiven."""
    p = Vector(p)
    o.data.transform(Matrix.Translation(o.location - p))
    o.location = p
    return o


def lumpy(o, amp=0.1, freq=1.0, seed=0, axes=(1, 1, 1)):
    """Coherente ruis-vervorming (organische vormen)."""
    off = Vector((seed * 13.1, seed * 7.7, seed * 3.3))
    for v in o.data.vertices:
        n = noise.noise_vector(v.co * freq + off)
        v.co += Vector((n.x * axes[0], n.y * axes[1], n.z * axes[2])) * amp
    o.data.update()
    return o


def jitter(o, amp=0.05, seed=0, axes=(1, 1, 1)):
    rnd = random.Random(seed)
    # zelfde positie -> zelfde verschuiving (geen scheuren in gedeelde hoeken)
    cache = {}
    for v in o.data.vertices:
        k = (round(v.co.x, 4), round(v.co.y, 4), round(v.co.z, 4))
        if k not in cache:
            cache[k] = Vector((rnd.uniform(-1, 1) * axes[0], rnd.uniform(-1, 1) * axes[1], rnd.uniform(-1, 1) * axes[2])) * amp
        v.co += cache[k]
    o.data.update()
    return o


def taper(o, f_top=0.5, z0=None, z1=None):
    """Schaal x/y lineair met hoogte (z0 -> 1, z1 -> f_top)."""
    zs = [v.co.z for v in o.data.vertices]
    z0 = min(zs) if z0 is None else z0
    z1 = max(zs) if z1 is None else z1
    for v in o.data.vertices:
        t = max(0, min(1, (v.co.z - z0) / ((z1 - z0) or 1)))
        s = 1 + (f_top - 1) * t
        v.co.x *= s; v.co.y *= s
    o.data.update()
    return o


def bend(o, fn):
    """Vervorm elk vertex via fn(co) -> nieuwe co."""
    for v in o.data.vertices:
        v.co = Vector(fn(v.co.copy()))
    o.data.update()
    return o


def flat(o):
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def smooth(o, angle=40):
    return shade_smooth(o, angle)


def prism(profile, depth, material=None, axis='Y', loc=(0, 0, 0)):
    """Extrudeer een 2D-profiel [(a,b),...] (a=x, b=z) over 'depth' langs Y, gecentreerd. axis='X' -> profiel (y,z) langs X."""
    me = bpy.data.meshes.new('prism')
    bm = bmesh.new()
    h = depth / 2
    if axis == 'Y':
        f = [bm.verts.new((a, -h, b)) for a, b in profile]
        bk = [bm.verts.new((a, h, b)) for a, b in profile]
    elif axis == 'X':
        f = [bm.verts.new((-h, a, b)) for a, b in profile]
        bk = [bm.verts.new((h, a, b)) for a, b in profile]
    else:  # Z: profiel (x,y) over hoogte
        f = [bm.verts.new((a, b, 0)) for a, b in profile]
        bk = [bm.verts.new((a, b, depth)) for a, b in profile]
    n = len(profile)
    bm.faces.new(f[::-1])
    bm.faces.new(bk)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((f[i], f[j], bk[j], bk[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('prism', me)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        me.materials.append(material)
    o.location = loc
    return o


def lathe(profile, seg=12, material=None, loc=(0, 0, 0), cap_bottom=True, cap_top=True, phase=0.0):
    """Draaiprofiel [(r,z),...] rond Z. r=0 punten worden polen."""
    me = bpy.data.meshes.new('lathe')
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(TAU * i / seg + phase), r * math.sin(TAU * i / seg + phase), z)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))
    if cap_bottom and len(rings[0]) > 1:
        bm.faces.new(rings[0][::-1])
    if cap_top and len(rings[-1]) > 1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('lathe', me)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        me.materials.append(material)
    o.location = loc
    return o


def decimate(o, ratio):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def dissolve_flat(o, angle=1.0):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle), verts=bm.verts, edges=bm.edges)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def boolean(o, cutter, op='DIFFERENCE', solver='EXACT'):
    m = o.modifiers.new('bool', 'BOOLEAN'); m.object = cutter; m.operation = op; m.solver = solver
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter)
    return o


def set_mat(o, m):
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons:
        p.material_index = 0
    return o


def tri_count(o):
    return tris([o])


def report(objs=None):
    objs = objs or [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in objs:
        print('  part', o.name, tris([o]))
    print('  TOTAL', tris(objs))


def crenellations(r, z, n, w, h, d, material=None, phase=0.0):
    """Ring van kantelen (blokjes) op straal r, hoogte z (onderkant)."""
    out = []
    for i in range(n):
        a = TAU * i / n + phase
        b = box((d, w, h), material=material)
        xform(b, loc=(r, 0, z + h / 2))
        xform(b, rot=(0, 0, math.degrees(a)))
        out.append(b)
    return out


def ring_place(o_proto, r, n, z=0.0, phase=0.0, face_out=True, keep=False):
    """Kopieën van een prototype (rond eigen oorsprong) in een ring."""
    out = []
    for i in range(n):
        a = TAU * i / n + phase
        c = dup(o_proto)
        xform(c, loc=(r, 0, z))
        xform(c, rot=(0, 0, math.degrees(a)))
        out.append(c)
    if not keep:
        bpy.data.objects.remove(o_proto)
    return out


def surface_points(o, n, seed=0, center=None, zmin=-1e9, up_bias=0.0, tries=2000):
    """Willekeurige punten op het oppervlak van o (stralen van buiten naar het midden). -> [(loc, normal)]"""
    from mathutils.bvhtree import BVHTree
    bake_loc(o)
    bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(Matrix.Identity(4))
    tree = BVHTree.FromBMesh(bm)
    lo, hi = bounds([o])
    c = Vector(center) if center is not None else (lo + hi) / 2
    R = (hi - lo).length * 2
    rnd = random.Random(seed)
    out = []
    k = 0
    while len(out) < n and k < tries:
        k += 1
        d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1) + up_bias)).normalized()
        hit = tree.ray_cast(c + d * R, -d)
        if hit[0] is None or hit[0].z < zmin:
            continue
        out.append((hit[0].copy(), hit[1].copy()))
    bm.free()
    return out


def orient(o, normal, loc):
    """Object (gemaakt rond oorsprong, as = +Z) naar normal draaien en op loc zetten."""
    q = Vector(normal).to_track_quat('Z', 'Y')
    if o.location.length > 0:
        bake_loc(o)
    o.data.transform(Matrix.Translation(loc) @ q.to_matrix().to_4x4())
    o.data.update()
    return o


def mesh_obj(verts, faces, material=None, name='mesh'):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        me.materials.append(material)
    return o


def flower_head(R=0.05, rc=0.015, petals=5, cup=0.012, petal_mat=None, heart_mat=None, both_sides=False, wide=0.75):
    """Bloemhoofdje rond de oorsprong, kijkt naar +Z: hartje (vlak) + brede bloemblaadjes."""
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
    if both_sides:
        fs += [tuple(reversed(f)) for f in fs[1:]]
    o = mesh_obj(vs, fs, petal_mat, 'flower')
    if heart_mat is not None:
        o.data.materials.append(heart_mat)
        o.data.polygons[0].material_index = 1
    return o


def leaf(L=0.12, W=0.05, ridge=0.01, material=None, droop=0.0):
    """Ruitvormig blad langs +Y vanaf de oorsprong, dubbelzijdig, met middennerf-knik."""
    vs = [(0, 0, 0), (-W / 2, L * 0.42, 0), (0, L, -droop), (W / 2, L * 0.42, 0), (0, L * 0.45, ridge)]
    # nerf: bovenkant iets omhoog
    fs = [(0, 4, 1), (1, 4, 2), (2, 4, 3), (3, 4, 0), (0, 1, 2, 3)]
    o = mesh_obj(vs, fs, material, 'leaf')
    return o


def chunk(r=0.5, scale=(1, 1, 1), cuts=10, seed=0, material=None, depth=(0.55, 0.9), base_sub=2, flat_bottom=None):
    """Gefacetteerde rots: icosfeer afgesneden met willekeurige vlakken (grote platte facetten)."""
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
    o.data.update()
    flat(o)
    return o


def surf_tree(o):
    from mathutils.bvhtree import BVHTree
    bm = bmesh.new(); bm.from_mesh(o.data)
    bm.transform(o.matrix_world)
    t = BVHTree.FromBMesh(bm); bm.free()
    return t


def crack_ribbon(tree, start, direction, length=1.0, width=0.05, steps=8, seed=0, material=None, lift=0.012, wiggle=0.6, branch=0):
    """Gloeiende scheur: lint dat over het oppervlak kronkelt (tree = surf_tree(rots))."""
    rnd = random.Random(seed)
    p, n, _, _ = tree.find_nearest(Vector(start))
    t = Vector(direction)
    t = (t - n * t.dot(n)).normalized()
    pts = []
    stepL = length / steps
    for i in range(steps + 1):
        pts.append((p.copy(), n.copy(), t.copy()))
        ang = rnd.uniform(-wiggle, wiggle)
        b = n.cross(t)
        t = (t * math.cos(ang) + b * math.sin(ang)).normalized()
        q = p + t * stepL
        p2, n2, _, _ = tree.find_nearest(q)
        if p2 is None:
            break
        t = (p2 - p).normalized() if (p2 - p).length > 1e-6 else t
        p, n = p2, n2
        t = (t - n * t.dot(n)).normalized()
    vs, fs = [], []
    N = len(pts)
    for i, (p, n, t) in enumerate(pts):
        f = math.sin(math.pi * (i + 0.5) / (N)) ** 0.6
        w = width * max(0.15, f)
        b = n.cross(t).normalized()
        vs += [p + n * lift + b * w / 2, p + n * lift - b * w / 2]
    for i in range(N - 1):
        fs.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
    o = mesh_obj(vs, fs, material, 'crack')
    # normalen naar buiten richten
    me = o.data
    for poly in me.polygons:
        c = poly.center
        _, nn, _, _ = tree.find_nearest(c)
        if poly.normal.dot(nn) < 0:
            poly.flip()
    out = [o]
    if branch and N > 3:
        for k in range(branch):
            i = rnd.randint(1, N - 2)
            p, n, t = pts[i]
            b = n.cross(t)
            d = (t * 0.5 + b * rnd.choice((-1, 1))).normalized()
            out += crack_ribbon(tree, p, d, length * 0.4, width * 0.6, max(3, steps // 2), seed + 17 * (k + 1), material, lift, wiggle, 0)
    return out


def dust(o, material, thresh=0.7, noise_amt=0.0, seed=0):
    """Vlakken die naar boven wijzen krijgen een ander materiaal (as, sneeuw, mos)."""
    if material.name not in [m.name for m in o.data.materials]:
        o.data.materials.append(material)
    idx = [m.name for m in o.data.materials].index(material.name)
    off = Vector((seed * 1.3, seed * 0.7, 0))
    for p in o.data.polygons:
        if p.normal.z + noise_amt * noise.noise(p.center * 2 + off) > thresh:
            p.material_index = idx
    return o
