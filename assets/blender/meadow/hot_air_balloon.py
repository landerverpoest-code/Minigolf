import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow')
from _lifekit import *
from _lifekit import _obj

# ---------------------------------------------------------------- materials (6)
RED = mat('balloon_red', '#e8322c', rough=0.55)
YEL = mat('balloon_yellow', '#ffc828', rough=0.5)
BLUE = mat('balloon_blue', '#2a7be4', rough=0.55)
WICK = mat('wicker', '#b77a3e', rough=0.85)
SKIN = mat('skin', '#f6c49c', rough=0.6)
FLAME = mat('glow_flame', '#ffb02e', rough=0.4, emit='#ff8a1c', emit_strength=6.0)
GORE = [RED, YEL, BLUE]


def catmull(pts, n):
    """Resample a polyline of (r, z) with a Catmull-Rom spline, n points per segment."""
    P = [Vector(p) for p in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return out


# ---------------------------------------------------------------- envelope
NG, SUB = 9, 4                       # gores, verts per gore
NA = NG * SUB
THROAT_Z = 2.78
prof = [(0.56, THROAT_Z), (0.9, 3.25), (1.6, 3.95), (2.35, 4.8), (2.85, 5.75), (3.02, 6.55),
        (2.92, 7.35), (2.5, 8.08), (1.72, 8.66), (0.8, 8.95)]
ring_rz = catmull(prof[:7], 1)[:-1] + catmull(prof[6:], 2)
BAND = (5.45, 6.25)                   # zig-zag pattern band
ZIG = 0.17
# insert the two band-edge rings at the right z
rings_def = []
for p in ring_rz:
    rings_def.append((p.x, p.y, 0))
for zb, kind in ((BAND[0], 1), (BAND[1], 2)):
    for i in range(len(rings_def) - 1):
        r0, z0, _ = rings_def[i]; r1, z1, _ = rings_def[i + 1]
        if z0 < zb <= z1:
            t = (zb - z0) / (z1 - z0)
            rings_def.insert(i + 1, (r0 + (r1 - r0) * t, zb, kind))
            break
# drop regular rings that sit too close to a band edge
clean = []
for r, z, k in rings_def:
    if k == 0 and any(abs(z - b) < 0.18 for b in BAND):
        continue
    clean.append((r, z, k))
rings_def = clean

bm = bmesh.new()
rings = []
for r, z, k in rings_def:
    ring = []
    rr = r
    bul = 0.045 * min(1.0, rr / 1.5)
    for a in range(NA):
        u = (a % SUB) / SUB
        ang = TAU * a / NA
        rad = rr * (1 + bul * math.sin(math.pi * u))
        zz = z
        if k:
            tri = 1 - 4 * abs(((a % SUB) / SUB + 0.0) - 0.5)   # +1 at seam (u=0), -1 at gore centre
            zz = z + (ZIG * tri if k == 1 else -ZIG * tri)
        ring.append(bm.verts.new((rad * math.cos(ang), rad * math.sin(ang), zz)))
    rings.append(ring)
top = bm.verts.new((0, 0, 9.0))
faces = []
for ri in range(len(rings) - 1):
    a, b = rings[ri], rings[ri + 1]
    for i in range(NA):
        f = bm.faces.new((a[i], a[(i + 1) % NA], b[(i + 1) % NA], b[i]))
        faces.append((f, ri, i))
for i in range(NA):
    f = bm.faces.new((rings[-1][i], rings[-1][(i + 1) % NA], top))
    faces.append((f, len(rings) - 1, i))
# throat cap (recessed cone so we never look into an empty shell)
cin = bm.verts.new((0, 0, THROAT_Z + 0.35))
for i in range(NA):
    f = bm.faces.new((rings[0][(i + 1) % NA], rings[0][i], cin))
    faces.append((f, -1, i))
band_lo = [i for i, (r, z, k) in enumerate(rings_def) if k == 1][0]
band_hi = [i for i, (r, z, k) in enumerate(rings_def) if k == 2][0]
mats_env = [RED, YEL, BLUE]
for f, ri, i in faces:
    g = i // SUB
    c = g % 3
    if ri == -1:
        c = 2
    elif band_lo <= ri < band_hi:
        c = (c + 1) % 3                              # harlequin band: colours shift by one
    elif rings_def[ri][1] > 8.62:
        c = 0                                        # red crown
    f.material_index = c
bmesh.ops.recalc_face_normals(bm, faces=[f for f in bm.faces if f.material_index != 99])
env = _obj(bm, None)
for m in mats_env:
    env.data.materials.append(m)
# make sure the throat cap points down/outwards (it is seen from below)
bm = bmesh.new(); bm.from_mesh(env.data)
bm.faces.ensure_lookup_table()
for f in bm.faces:
    c = f.calc_center_median()
    if c.z < THROAT_Z + 0.36 and (Vector((c.x, c.y, 0)).length < 0.5) and f.normal.z > 0:
        f.normal_flip()
bm.to_mesh(env.data); bm.free()

# load tapes: thin wicker-coloured lines down the gore seams would need a 7th colour, so we use
# small red/yellow/blue skirt (scoop) instead
skirt = lathe([(0.66, THROAT_Z - 0.32), (0.565, THROAT_Z + 0.02)], seg=18, material=RED,
              caps=(False, False), smooth=True)
skirt_in = lathe([(0.55, THROAT_Z + 0.02), (0.645, THROAT_Z - 0.32)], seg=18, material=RED,
                 caps=(False, False), smooth=True)  # inner wall (single-sided materials in three.js)
for o in (skirt, skirt_in):
    bm = bmesh.new(); bm.from_mesh(o.data)
    for f in bm.faces:
        c = f.calc_center_median(); out = Vector((c.x, c.y, 0)).normalized()
        want = 1 if o is skirt else -1
        if f.normal.dot(out) * want < 0:
            f.normal_flip()
    bm.to_mesh(o.data); bm.free()
# crown ring at the very top
crown = lathe([(0.0, 9.0), (0.42, 8.99), (0.45, 9.04), (0.0, 9.08)], seg=12, material=YEL)

# ---------------------------------------------------------------- basket (rounded square, woven ribs)
def rsq(hw, rc=0.2, nc=3):
    pts = []
    for q, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        cx, cy = sx * (hw - rc), sy * (hw - rc)
        a0 = q * math.pi / 2
        for k in range(nc + 1):
            a = a0 + (math.pi / 2) * k / nc
            pts.append((cx + rc * math.cos(a), cy + rc * math.sin(a)))
    return pts


def rsq_loft(profile, material, rc=0.2, nc=2, cap0=False, cap1=False):
    bm = bmesh.new()
    rings = []
    for hw, z in profile:
        rings.append([bm.verts.new((x, y, z)) for x, y in rsq(hw, rc + (hw - 0.7), nc)])
    n = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for i in range(n):
            bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cap0:
        bm.faces.new(list(reversed(rings[0])))
    if cap1:
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(bm, material)


BH = 1.02
prof_b = [(0.6, 0.0), (0.64, 0.025)]
NR = 4
for i in range(NR):
    z0 = 0.06 + (BH - 0.12) * i / NR
    z1 = 0.06 + (BH - 0.12) * (i + 0.5) / NR
    hw = 0.64 + 0.05 * (i / NR)
    prof_b += [(hw - 0.012, z0), (hw + 0.012, z1)]
prof_b += [(0.69, BH - 0.06), (0.69, BH)]
basket = rsq_loft(prof_b, WICK, rc=0.2, nc=2, cap0=True)
inner = rsq_loft([(0.64, BH), (0.6, 0.35)], WICK, rc=0.2, nc=2, cap1=True)   # inside wall + floor
bm = bmesh.new(); bm.from_mesh(inner.data)
for f in bm.faces:
    c = f.calc_center_median()
    if abs(f.normal.z) < 0.7 and f.normal.dot(Vector((c.x, c.y, 0))) > 0:
        f.normal_flip()
    if f.normal.z < -0.7:
        f.normal_flip()
bm.to_mesh(inner.data); bm.free()
# padded red suede rim
rim_prof = []
for k in range(5):
    a = TAU * k / 4 + math.pi / 4
    rim_prof.append((0.665 + 0.065 * math.cos(a), BH + 0.01 + 0.06 * math.sin(a)))
rim = rsq_loft(rim_prof, RED, rc=0.2, nc=2)
bm = bmesh.new(); bm.from_mesh(rim.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(rim.data); bm.free()
# vertical wicker stakes at the corners
stakes = []
for sx in (-1, 1):
    for sy in (-1, 1):
        d = Vector((sx, sy, 0)).normalized()
        b0 = d * (0.64 * 1.414 - 0.2 * 0.414 + 0.005)
        b1 = d * (0.69 * 1.414 - 0.2 * 0.414 + 0.02)
        stakes.append(tube([(b0.x, b0.y, 0.0), (b1.x, b1.y, BH)], [0.035, 0.035], seg=5, material=WICK, cap=False))
# sandbags hanging on the outside
bags = []
for (x, y, s) in ((0.71, -0.25, 1), (-0.71, 0.1, -1), (0.0, -0.71, 0), (-0.3, 0.71, 0)):
    if s == 0:
        c = Vector((x, -0.76 if y < 0 else 0.76, 0.66))
    else:
        c = Vector((0.76 * s, y, 0.66))
    bags.append(ell(c, (0.085, 0.085, 0.11), seg=5, rings=4, material=BLUE if (x + y) > 0 else YEL,
                    shape=lambda n: Vector((n.x * (1 - 0.25 * max(n.z, 0)), n.y * (1 - 0.25 * max(n.z, 0)), n.z))))
    rp = c + Vector((0, 0, 0.1))
    bags.append(tube([rp, Vector((rp.x * 0.93, rp.y * 0.93, BH - 0.06))], 0.012, seg=3, material=WICK, cap=False))

# ---------------------------------------------------------------- burner, frame, poles, cables
FZ = 2.0
fh = 0.36
frame = rsq_loft([(fh + 0.03, FZ - 0.025), (fh + 0.03, FZ + 0.025), (fh - 0.03, FZ + 0.025), (fh - 0.03, FZ - 0.025)],
                 YEL, rc=0.12, nc=1)
bm = bmesh.new(); bm.from_mesh(frame.data)
r = [v for v in bm.verts]
n = len(r) // 4
for i in range(n):  # close the ring loft (last ring -> first ring)
    a, b = r[3 * n + i], r[3 * n + (i + 1) % n]; c, d = r[(i + 1) % n], r[i]
    bm.faces.new((a, b, c, d))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(frame.data); bm.free()
burner = lathe([(0.0, FZ - 0.16), (0.12, FZ - 0.15), (0.14, FZ - 0.05), (0.14, FZ + 0.06), (0.08, FZ + 0.13), (0.0, FZ + 0.14)],
               seg=8, material=YEL)
spokes = [tube([(0, 0, FZ), (sx * (fh - 0.08), sy * (fh - 0.08), FZ)], 0.018, seg=4, material=YEL)
          for sx, sy in ((1, 1), (-1, -1), (1, -1), (-1, 1))]
poles = []
for sx in (-1, 1):
    for sy in (-1, 1):
        cb = Vector((sx * 0.6, sy * 0.6, BH + 0.03))
        cf = Vector((sx * (fh - 0.02), sy * (fh - 0.02), FZ))
        poles.append(tube([cb, cb.lerp(cf, 0.5), cf], [0.03, 0.028, 0.026], seg=5, material=BLUE, cap=False))
cables = []
NCAB = 8
for k in range(NCAB):
    a = TAU * (k + 0.5) / NCAB
    top_p = Vector((0.64 * math.cos(a), 0.64 * math.sin(a), THROAT_Z - 0.3))
    d = Vector((math.cos(a), math.sin(a), 0))
    # nearest frame point
    s = fh / max(abs(d.x), abs(d.y))
    bot_p = Vector((d.x * s, d.y * s, FZ + 0.02))
    cables.append(tube([bot_p, top_p], 0.014, seg=3, material=WICK, cap=False))
    # rope continues from the frame down to the basket rim
    sb = 0.66 / max(abs(d.x), abs(d.y))
    cables.append(tube([Vector((d.x * sb, d.y * sb, BH + 0.05)), bot_p], 0.013, seg=3, material=WICK, cap=False))

# ---------------------------------------------------------------- tiny waving passenger
P = Vector((0.18, -0.12, 0.0))
pas = []
pas.append(ell(P + Vector((0, 0, 1.0)), (0.17, 0.14, 0.24), seg=8, rings=6, material=BLUE))           # jacket
HEADC = P + Vector((0, -0.01, 1.44))
pas.append(ell(HEADC, (0.15, 0.14, 0.145), seg=10, rings=6, material=SKIN))
# red cap with brim
pas.append(ell(HEADC + Vector((0, 0.01, 0.055)), (0.155, 0.148, 0.11), seg=10, rings=4, material=RED,
               shape=lambda n: Vector((n.x, n.y, max(n.z, -0.05)))))
pas.append(ell(HEADC + Vector((0, -0.13, 0.05)), (0.11, 0.08, 0.018), seg=8, rings=3, material=RED, rot=(-12, 0, 0)))
pas.append(ell(HEADC + Vector((0, 0.0, 0.165)), (0.035, 0.035, 0.035), seg=5, rings=3, material=YEL))     # pom-pom
for sx in (-1, 1):  # eyes + cheeks
    pas.append(ell(HEADC + Vector((sx * 0.052, -0.128, 0.005)), (0.022, 0.012, 0.03), seg=5, rings=3, material=WICK))
    pas.append(ell(HEADC + Vector((sx * 0.095, -0.105, -0.045)), (0.03, 0.012, 0.02), seg=5, rings=3, material=RED,
                   rot=(0, 0, sx * 35)))
pas.append(tube(bezier(HEADC + Vector((-0.045, -0.135, -0.05)), HEADC + Vector((0, -0.16, -0.085)), HEADC + Vector((0.045, -0.135, -0.05)), n=4),
                0.011, seg=4, material=RED, round_end=True))
pas.append(ell(HEADC + Vector((0, -0.15, -0.015)), (0.025, 0.022, 0.022), seg=5, rings=3, material=SKIN))  # nose
# waving arm (raised, to the right = -X side seen from the front is +X... arm goes up-outwards)
SH = P + Vector((0.15, 0, 1.15))
EL = SH + Vector((0.14, -0.04, 0.16))
HA = EL + Vector((0.02, -0.03, 0.2))
pas.append(tube([SH, EL, HA], [0.055, 0.05, 0.045], seg=5, material=BLUE, cap=False))
pas.append(ell(HA + Vector((0.005, -0.005, 0.05)), (0.055, 0.04, 0.07), seg=6, rings=4, material=SKIN, rot=(0, -15, 0)))
# other arm resting on the rim
SH2 = P + Vector((-0.15, 0, 1.15))
pas.append(tube([SH2, SH2 + Vector((-0.08, -0.12, -0.1)), Vector((SH2.x - 0.02, -0.54, BH + 0.06))], [0.055, 0.05, 0.045], seg=5, material=BLUE, cap=False))
pas.append(ell(Vector((SH2.x - 0.02, -0.56, BH + 0.08)), (0.05, 0.05, 0.035), seg=6, rings=4, material=SKIN))

PS = Matrix.Translation((P.x, P.y, BH)) @ Matrix.Scale(1.3, 4) @ Matrix.Translation((-P.x, -P.y, -BH))
for o in pas:
    xf(o, PS)

body = part([env, skirt, skirt_in, crown, basket, inner, rim, burner, frame] + stakes + bags + spokes + poles + cables + pas,
            'body', (0, 0, 0), angle=40)

# ---------------------------------------------------------------- flame (separate, origin at its base)
FB = Vector((0, 0, FZ + 0.14))
fl = [lathe([(0.0, 0.0), (0.09, 0.03), (0.15, 0.12), (0.165, 0.25), (0.14, 0.4), (0.09, 0.56), (0.035, 0.7), (0.0, 0.78)],
            seg=9, material=FLAME, M=Matrix.Translation(FB))]
for k in range(3):
    a = TAU * k / 3 + 0.4
    d = Vector((math.cos(a), math.sin(a), 0))
    fl.append(tongue(FB + d * 0.05 + Vector((0, 0, 0.1)), FB + d * 0.16 + Vector((0, 0, 0.3)), FB + d * 0.08 + Vector((0, 0, 0.55)),
                     FB + d * 0.13 + Vector((0, 0, 0.72)), 0.09, seg=4, n=4, material=FLAME))
flame = part(fl, 'flame', FB)

clamp_ground([body])
report(); print_ext()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Parts/pivots (Blender coords, front -Y): body (origin 0,0,0 = basket bottom centre; envelope with 12 red/yellow/blue '
         'gores + harlequin zig-zag band + red crown, skirt, burner frame, poles, ropes, wicker basket 1.4 m wide with red rim, '
         'sandbags, tiny waving passenger); flame (origin = its base at (0,0,%.2f) on top of the burner, material glow_flame, '
         'for flicker scale it around its origin). Total height 9.08 m.' % FB.z)
std_view()
finish('meadow', 'hot_air_balloon', kind='char', footprint=3.1, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('balloon', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'low': (0.5, -1, -0.5)})
    closeup('balloon_basket', (0, 0, 1.4), 4.2, d=(0.5, -1, 0.35))
    closeup('balloon_basket2', (0, 0, 1.6), 4.5, d=(-0.6, -1, -0.15))
    montage_files([f'{SCRATCH}/balloon_{k}.png' for k in ('front', 'side', 'low', 'basket', 'basket2')], f'{SCRATCH}/balloon_views.png')
