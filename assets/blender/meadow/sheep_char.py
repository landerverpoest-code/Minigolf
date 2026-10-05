import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow')
from _lifekit import *

# ---------------------------------------------------------------- materials (6)
WOOL = mat('wool', '#fbf8f0', rough=0.95)
WOOL_SH = mat('wool_shade', '#dccfb8', rough=0.95)
BLACK = mat('sheep_black', '#2b2727', rough=0.6)
EYEW = mat('eye_white', '#ffffff', rough=0.35)
PINK = mat('sheep_pink', '#f49ab0', rough=0.6)
HOOF = mat('hoof', '#6a5444', rough=0.6)


def fib_dirs(n, seed=0, zmin=-1.0):
    rnd = random.Random(seed)
    out = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        if z < zmin:
            continue
        r = math.sqrt(1 - z * z); a = ga * i + rnd.uniform(-0.25, 0.25)
        out.append(Vector((r * math.cos(a), r * math.sin(a), z + rnd.uniform(-0.06, 0.06))).normalized())
    return out


def cloud(c, r, n=22, amp=0.13, th0=0.62, seg=30, rings=16, seed=1, material=WOOL, flat_bottom=None):
    """Cauliflower / cloud ellipsoid: max of round domes over fibonacci directions -> creased lumps.
    Returns the object; obj['bump'] is not storable, so the bump function is kept in CLOUD_FN[obj.name]."""
    dirs = fib_dirs(n, seed)
    rnd = random.Random(seed + 7)
    sizes = [th0 * rnd.uniform(0.85, 1.15) for _ in dirs]
    c = Vector(c)

    def bump(v):
        v = v.normalized() if v.length > 1e-6 else Vector((0, 0, 1))
        b = 0.0
        for d, t0 in zip(dirs, sizes):
            th = math.acos(max(-1.0, min(1.0, v.dot(d))))
            if th < t0:
                b = max(b, (1 - (th / t0) ** 2) ** 0.6)
        return b

    def shape(v):
        v = v.normalized() if v.length > 1e-6 else Vector((0, 0, 1))
        s = 1 + amp * (bump(v) - 0.35)
        if flat_bottom is not None and v.z < flat_bottom:
            s *= 1 - 0.25 * (flat_bottom - v.z)
        return v * s
    o = ell(c, r, seg=seg, rings=rings, material=material, shape=shape)
    o['_c'] = list(c)
    CLOUD_FN[o.name] = lambda p: bump(Vector(((p - c).x / r[0], (p - c).y / r[1], (p - c).z / r[2])))
    return o


CLOUD_FN = {}


def paint_creases(o, thr=0.35, extra=None):
    f = CLOUD_FN[o.name]
    iso_paint(o, lambda p: (f(p) - thr) if extra is None else min(f(p) - thr, extra(p)), WOOL_SH)


def union_all(objs):
    base = objs[0]
    for o in objs[1:]:
        m = base.modifiers.new('u', 'BOOLEAN'); m.operation = 'UNION'; m.solver = 'EXACT'; m.object = o
        m.material_mode = 'TRANSFER'
        bpy.context.view_layer.objects.active = base
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.data.objects.remove(o)
    return base


def decimate_to(o, target):
    o.data.calc_loop_triangles(); n = len(o.data.loop_triangles)
    if n <= target:
        return o
    m = o.modifiers.new('d', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = target / n
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def puff_cloud(c, r, n, pr, seed=0, seg=9, rings=6, shade_z=None, zmin=-0.75, core=0.82):
    """Lumpy wool: overlapping smooth spheres on an ellipsoid shell, boolean-unioned (crisp creases)."""
    c = Vector(c); rnd = random.Random(seed)
    objs = [ell(c, tuple(k * core for k in r), seg=10, rings=6, material=WOOL_SH)]
    for d in fib_dirs(n, seed, zmin=zmin):
        p = c + Vector((d.x * r[0], d.y * r[1], d.z * r[2])) * 0.78
        rr = pr * rnd.uniform(0.85, 1.15)
        m = WOOL if (shade_z is None or p.z > shade_z) else WOOL_SH
        objs.append(ell(p, (rr, rr, rr * 0.92), seg=seg, rings=rings, material=m,
                        rot=(rnd.uniform(0, 90), rnd.uniform(0, 90), 0)))
    return union_all(objs)


# ---------------------------------------------------------------- body (wool puffs + tail)
BC = Vector((0, 0.06, 0.5))
wool = puff_cloud(BC, (0.27, 0.35, 0.21), 19, 0.145, seed=4, shade_z=0.36, zmin=-0.8)
tail = puff_cloud(Vector((0, 0.45, 0.6)), (0.06, 0.05, 0.06), 4, 0.05, seed=5, seg=7, rings=5)
# wool ruff round the neck so the head sits in a fluffy collar
collar = puff_cloud(Vector((0, -0.24, 0.57)), (0.15, 0.08, 0.14), 6, 0.085, seed=9, seg=8, rings=5, zmin=-0.6)
decimate_to(wool, 1000); decimate_to(collar, 240); decimate_to(tail, 110)
body = part([wool, tail, collar], 'body', (0, 0, 0), angle=72)

# ---------------------------------------------------------------- head (pivot at the neck)
NECK = Vector((0, -0.28, 0.58))
HC = Vector((0, -0.46, 0.6))
hp = []
face = ell(HC, (0.115, 0.15, 0.125), seg=12, rings=9, material=BLACK, rot=(28, 0, 0),
           shape=lambda n: Vector((n.x * (1 + 0.12 * n.z) * (1 - 0.12 * max(-n.y, 0)), n.y, n.z * (1 - 0.06 * max(-n.y, 0)))))
hp.append(face)
hp.append(tube([NECK + Vector((0, 0.02, -0.02)), HC + Vector((0, 0.04, 0.0))], [0.09, 0.1], seg=8, material=BLACK, cap=False))
# fluffy wool tuft on the crown
for (x, y, z, s, sd) in ((0, -0.46, 0.735, 0.08, 1), (-0.06, -0.41, 0.715, 0.065, 2), (0.06, -0.41, 0.715, 0.065, 3)):
    hp.append(cloud(Vector((x, y, z)), (s, s, s * 0.85), n=7, amp=0.3, th0=0.9, seg=8, rings=5, seed=sd))
# big eyes
for sx in (-1, 1):
    ec = Vector((sx * 0.058, -0.565, 0.645))
    hp += eye(ec, Vector((sx * 0.45, -1, 0.1)), r=0.04, white=EYEW, black=BLACK, look=(-sx * 0.2, 0, 0.05), tall=1.25,
              pupil=0.6, seg=8, pseg=7)
    # ears: black, drooping sideways, pink inside
    ear = ell((0, 0, 0), (0.085, 0.028, 0.04), seg=7, rings=5, material=BLACK)
    iso_paint(ear, lambda p: p.y + 0.012, PINK)
    xf(ear, Matrix.Translation((sx * 0.07, 0, 0)))
    xf(ear, Matrix.Translation(HC + Vector((sx * 0.075, 0.03, 0.06))) @ Matrix.Rotation(math.radians(sx * -28), 4, 'Y')
       @ Matrix.Rotation(math.radians(sx * 20), 4, 'Z'))
    hp.append(ear)
    # rosy cheeks
    hp.append(ell(Vector((sx * 0.085, -0.565, 0.565)), (0.025, 0.012, 0.016), seg=6, rings=4, material=PINK, rot=(0, 0, sx * 40)))
# pink nose + smile on the snout
hp.append(ell(Vector((0, -0.605, 0.555)), (0.032, 0.02, 0.018), seg=8, rings=4, material=PINK, rot=(25, 0, 0)))
hp.append(tube(bezier(Vector((-0.03, -0.592, 0.522)), Vector((0, -0.608, 0.505)), Vector((0.03, -0.592, 0.522)), n=4), 0.006,
               seg=4, material=PINK, round_end=True))
head = part(hp, 'head', NECK)

# ---------------------------------------------------------------- legs (pivot at the hip, hooves at z=0)
HIP_Z = 0.34
LEGS = {'leg_fl': (0.14, -0.2), 'leg_fr': (-0.14, -0.2), 'leg_bl': (0.14, 0.25), 'leg_br': (-0.14, 0.25)}
for name, (x, y) in LEGS.items():
    lp = [tube([(x, y, HIP_Z + 0.03), (x, y, 0.18), (x, y - 0.005, 0.06)], [0.062, 0.055, 0.05], seg=8, material=BLACK, cap=False)]
    lp.append(lathe([(0.0, 0.0), (0.06, 0.0), (0.063, 0.015), (0.056, 0.075), (0.0, 0.08)], seg=8, material=HOOF,
                    M=Matrix.Translation((x, y - 0.005, 0))))
    part(lp, name, (x, y, HIP_Z))

clamp_ground()
report(); print_ext()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Parts/pivots (Blender coords, front -Y, left = +X): body (origin 0,0,0; cloud-like lumpy wool, tail puff, wool ruff '
         f'round the neck); head (pivot neck {tuple(round(v, 3) for v in NECK)}; black face, wool tuft, ears, big eyes, pink nose; '
         'rotate +X to graze/nod down); ' + ', '.join(f'{k} ({x},{y},{HIP_Z})' for k, (x, y) in LEGS.items()) +
         ' - pivot at the hip, black legs, hooves at z=0.')
std_view()
finish('meadow', 'sheep_char', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['head'].rotation_euler = (0.6, 0, 0)
        bpy.data.objects['leg_fl'].rotation_euler = (0.4, 0, 0)
        bpy.data.objects['leg_br'].rotation_euler = (0.4, 0, 0)
        bpy.data.objects['leg_fr'].rotation_euler = (-0.4, 0, 0)
        bpy.data.objects['leg_bl'].rotation_euler = (-0.4, 0, 0)
    closeup('sheep_face', (0, -0.45, 0.6), 1.2, d=(0.25, -1, 0.15))
    views('sheep', pose)
    montage_files([f'{SCRATCH}/sheep_{k}.png' for k in ('face', 'front', 'side', 'back', 'pose')], f'{SCRATCH}/sheep_views.png')
