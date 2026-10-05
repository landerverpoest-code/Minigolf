import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow')
from _lifekit import *
from _lifekit import _obj

# ---------------------------------------------------------------- materials (5)
BLUE = mat('dolphin_blue', '#5b8cbb', rough=0.35)
BELLY = mat('dolphin_belly', '#e9f1f6', rough=0.4)
EYEW = mat('eye_white', '#ffffff', rough=0.3)
DARK = mat('eye_dark', '#1b2333', rough=0.3)
PINK = mat('blush', '#f59cb4', rough=0.5)

# ---------------------------------------------------------------- body loft (stations: y, rx, rz, zc)
ST = [(-1.10, 0.012, 0.012, -0.075), (-1.09, 0.035, 0.032, -0.072), (-1.05, 0.055, 0.048, -0.07), (-0.98, 0.07, 0.06, -0.068),
      (-0.91, 0.085, 0.075, -0.06), (-0.85, 0.118, 0.13, -0.025), (-0.78, 0.165, 0.19, 0.0), (-0.66, 0.205, 0.235, 0.012),
      (-0.5, 0.235, 0.262, 0.012), (-0.3, 0.252, 0.278, 0.004), (-0.1, 0.248, 0.272, 0.0), (0.1, 0.222, 0.248, 0.004),
      (0.28, 0.172, 0.204, 0.014), (0.43, 0.115, 0.155, 0.025), (0.56, 0.072, 0.112, 0.032), (0.66, 0.052, 0.088, 0.035)]


ST = [(y, rx * (1.1 if -0.86 < y < 0.45 else 1.0), rz * (1.1 if -0.86 < y < 0.45 else 1.0), zc) for (y, rx, rz, zc) in ST]


def station(y):
    """Linear interpolation of the station table (smooth enough with the dense sampling below)."""
    if y <= ST[0][0]:
        return ST[0][1:]
    for a, b in zip(ST, ST[1:]):
        if a[0] <= y <= b[0]:
            t = (y - a[0]) / (b[0] - a[0])
            t = t * t * (3 - 2 * t) * 0.5 + t * 0.5
            return tuple(a[i] + (b[i] - a[i]) * t for i in (1, 2, 3))
    return ST[-1][1:]


def S(y, phi, off=0.0):
    """Point on the body surface at station y, angle phi (0 = +X side, 90 = top)."""
    rx, rz, zc = station(y)
    a = math.radians(phi)
    return Vector(((rx + off) * math.cos(a), y, zc + (rz + off) * math.sin(a)))


def body_loft(ys, n=16):
    bm = bmesh.new()
    rings = []
    for y in ys:
        rx, rz, zc = station(y)
        ring = []
        for k in range(n):
            a = TAU * k / n
            # slightly flatter belly, fuller back
            s = 1.0 if math.sin(a) > 0 else 0.93
            ring.append(bm.verts.new((rx * math.cos(a), y, zc + rz * math.sin(a) * s)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for k in range(n):
            bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    tip = bm.verts.new((0, ys[0] - 0.012, station(ys[0])[2]))
    for k in range(n):
        bm.faces.new((rings[0][(k + 1) % n], rings[0][k], tip))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(bm, BLUE)


ys = [-1.10, -1.085, -1.06, -1.02, -0.97, -0.92, -0.885, -0.85, -0.81, -0.76, -0.7, -0.62, -0.52, -0.4, -0.27, -0.13, 0.0,
      0.13, 0.25, 0.36, 0.46, 0.55, 0.62, 0.66]
torso = body_loft(ys, n=18)


def belly_field(p):
    rx, rz, zc = station(p.y)
    wave = 0.12 * math.sin((p.y + 0.4) * 5.0) * (1 if p.y > -0.8 else 0)
    lift = 0.12 if -0.85 < p.y < 0.1 else 0.0
    return (p.z - zc) / max(rz, 1e-3) + 0.28 - lift + wave


iso_paint(torso, belly_field, BELLY)
parts = [torso]

# dorsal fin: swept-back curved fin on the back
DF = S(0.02, 90, -0.04)
dorsal = ell((0, 0, 0), (0.028, 0.15, 0.2), seg=10, rings=8, material=BLUE,
             shape=lambda n: Vector((n.x * (1 - 0.75 * max(n.z, 0)), n.y * (1 - 0.55 * max(n.z, 0)) + 0.85 * max(n.z, 0) ** 1.6 - 0.1 * max(n.z, 0), n.z)))
xf(dorsal, Matrix.Translation(DF + Vector((0, 0.02, 0.06))))
parts.append(dorsal)
# pectoral flippers
for sx in (-1, 1):
    fl = ell((0, 0, 0), (0.17, 0.075, 0.022), seg=10, rings=6, material=BLUE,
             shape=lambda n: Vector((n.x, n.y * (1 - 0.45 * abs(n.x)) + 0.55 * n.x * n.x, n.z)))
    xf(fl, Matrix.Translation((0.15, 0, 0)))
    M = (Matrix.Translation(S(-0.45, -40, -0.04) * Vector((sx, 1, 1))) @ Matrix.Rotation(math.radians(sx * -34), 4, 'Y')
         @ Matrix.Rotation(math.radians(sx * 28), 4, 'Z'))
    if sx < 0:
        M = M @ Matrix.Scale(-1, 4, Vector((1, 0, 0)))
    xf(fl, M)
    if sx < 0:
        bm = bmesh.new(); bm.from_mesh(fl.data); bmesh.ops.reverse_faces(bm, faces=bm.faces); bm.to_mesh(fl.data); bm.free()
    parts.append(fl)

# face: big eyes, smile, blush, blowhole
for sx in (-1, 1):
    ec = S(-0.72, 22, -0.012) * Vector((sx, 1, 1))
    nrm = Vector((sx * 0.9, -0.35, 0.3))
    parts += eye(ec, nrm, r=0.058, white=EYEW, black=DARK, look=(sx * 0.35, 0, 0.1), tall=1.15, pupil=0.62, seg=10, pseg=8)
    # smile along the beak, curling up at the corner
    pts = []
    for k in range(8):
        t = k / 7
        y = -1.045 + t * 0.23
        phi = -30 + 34 * t ** 2.2 + (-10 * math.sin(math.pi * t))
        p = S(y, phi, 0.002)
        pts.append(Vector((sx * p.x, p.y, p.z)))
    end = pts[-1]
    pts.append(end + Vector((sx * 0.006, 0.02, 0.03)))
    parts.append(tube(pts, [0.006] + [0.0085] * (len(pts) - 2) + [0.007], seg=4, material=DARK, round_end=True))
    bl = S(-0.8, -12, 0.004)
    parts.append(ell(Vector((sx * bl.x, bl.y, bl.z)), (0.012, 0.04, 0.026), seg=8, rings=5, material=PINK,
                     rot=(0, 0, sx * -18)))
bh = S(-0.5, 90, 0.0)
parts.append(ell(bh + Vector((0, 0, -0.004)), (0.026, 0.014, 0.008), seg=8, rings=4, material=DARK))
body = part(parts, 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- tail (pivot at the tail stock)
TS = Vector((0, 0.6, station(0.6)[2]))
tp = []
# peduncle continuation (overlaps the body end so the joint stays closed while beating)
rx0, rz0, zc0 = station(0.58)
ped = []
bm = bmesh.new()
rings = []
for (y, rx, rz) in ((0.56, rx0 * 1.04, rz0 * 1.04), (0.66, 0.054, 0.09), (0.76, 0.04, 0.062), (0.86, 0.03, 0.034), (0.94, 0.012, 0.016)):
    rings.append([bm.verts.new((rx * math.cos(TAU * k / 12), y, zc0 + rz * math.sin(TAU * k / 12))) for k in range(12)])
for a, b in zip(rings, rings[1:]):
    for k in range(12):
        bm.faces.new((a[k], a[(k + 1) % 12], b[(k + 1) % 12], b[k]))
bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
tp.append(_obj(bm, BLUE))


def fluke_shape(n):
    ax = abs(n.x)
    y = n.y * (1 - 0.55 * ax) + 0.62 * ax ** 1.7          # swept-back tips
    if n.y > 0:
        y -= 0.42 * max(0.0, 1 - ax * 3.2) ** 2 * n.y          # notch in the trailing edge
    return Vector((n.x, y, n.z * (1 - 0.6 * ax)))


fluke = ell((0, 0, 0), (0.34, 0.15, 0.035), seg=16, rings=8, material=BLUE, shape=fluke_shape)
xf(fluke, Matrix.Translation((0, 0.9, zc0)))
iso_paint(fluke, lambda p: p.z - zc0 + 0.004, BELLY)
tp.append(fluke)
tail = part(tp, 'tail', TS, angle=60)

# overall scale so nose-to-fluke length is 2.2 m (origin and pivots scale with it)
lo, hi = bounds()
K = 2.2 / (hi.y - lo.y)
for o in (body, tail):
    o.data.transform(Matrix.Scale(K, 4)); o.location = o.location * K
TS = TS * K
bpy.context.view_layer.update()
report(); print_ext()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Parts/pivots (Blender coords, nose to -Y): body (origin 0,0,0 = body centre; grey-blue top, pale belly, smiling beak, '
         f'big eyes, dorsal fin, flippers); tail (pivot at the tail stock {tuple(round(v, 3) for v in TS)}; flukes; rotate about X to beat up/down). '
         'Not grounded: the game moves it in leaping arcs.')
std_view()
finish('water', 'dolphin', kind='char', footprint=1.1, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['tail'].rotation_euler = (0.45, 0, 0)
    closeup('dolphin_face', (0, -0.8, 0.0), 1.6, d=(0.8, -1, 0.3))
    views('dolphin', pose, dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.05), 'top': (0.01, 0.01, 1), 'under': (0.6, -0.5, -0.8)})
    montage_files([f'{SCRATCH}/dolphin_{k}.png' for k in ('face', 'front', 'side', 'top', 'under', 'pose')], f'{SCRATCH}/dolphin_views.png')
