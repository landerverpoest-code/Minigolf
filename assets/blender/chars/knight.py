import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akit import *
from ccp_kit import _obj

# ---------------------------------------------------------------- materials (6)
ARMOR = mat('armor', '#bcc7d4', rough=0.3, metal=0.75)
TABARD = mat('tabard', '#7a3cc2', rough=0.75)
SHIELD = mat('shield', '#1f6fe0', rough=0.45, metal=0.15)
GOLD = mat('gold', '#ffc93a', rough=0.28, metal=0.85)
PLUME = mat('plume', '#ec3340', rough=0.7)
STAR = mat('star', '#3b3e46', rough=0.35, metal=0.7)   # morning star; also the dark visor slit (glows with it)

B = []
# ---------------------------------------------------------------- legs + boots
for sx in (-1, 1):
    x = sx * 0.155
    # sabaton: rounded boot, flat sole, pointing -Y
    boot = ell(V(x, -0.05, 0.0), (0.105, 0.175, 0.13), seg=9, rings=5, material=ARMOR,
               shape=lambda n: Vector((n.x, n.y, max(n.z, 0.0))))
    B.append(boot)
    B.append(lathe([(0.112, 0.085), (0.118, 0.11), (0.1, 0.13)], seg=8, material=GOLD, M=Matrix.Translation((x, 0.0, 0))))
    # greave
    B.append(lathe([(0.085, 0.1), (0.1, 0.3), (0.1, 0.56)], seg=8, material=ARMOR,
                   M=Matrix.Translation((x, 0.01, 0))))
    # knee cop
    B.append(ell(V(x, -0.07, 0.33), (0.075, 0.05, 0.07), seg=6, rings=4, material=ARMOR))

# ---------------------------------------------------------------- fauld (armoured skirt lames)
for i, (z0, z1, r0, r1) in enumerate(((0.5, 0.64, 0.29, 0.265),)):
    B.append(lathe([(r0 - 0.02, z0), (r0, z0 + 0.01), (r1 + 0.01, z1), (r1 - 0.03, z1 + 0.01)], seg=12, material=ARMOR,
                   M=Matrix.Diagonal((1.0, 0.85, 1, 1))))

# ---------------------------------------------------------------- torso (breastplate)
TC, TA, TB, TH = 0.95, 0.33, 0.275, 0.36


def chest(n):
    k = 1.0 + 0.10 * max(0.0, -n.y) * max(0.0, 1 - abs(n.z - 0.15) * 1.4)   # pigeon chest
    return Vector((n.x * (1 + 0.05 * n.z), n.y * k, n.z))


torso = ell(V(0, 0, TC), (TA, TB, TH), seg=14, rings=10, p=0.9, material=ARMOR, shape=chest)
B.append(torso)
# gorget
B.append(lathe([(0.2, 1.22), (0.17, 1.3), (0.12, 1.34)], seg=12, material=ARMOR))


# ---------------------------------------------------------------- tabard (front + back panels following the torso)
def torso_r(z):
    t = (z - TC) / TH
    s = max(0.0, 1 - min(abs(t), 1.0) ** (2 / 0.9)) ** (0.9 / 2)
    return s


def panel(front=True):
    bm = bmesh.new()
    zs = [1.2, 1.08, 0.94, 0.8, 0.66, 0.53, 0.4]
    na = 7
    grid = []
    for z in zs:
        s = max(torso_r(z), 0.82 if z < TC else 0.0)
        flare = max(0.0, 0.66 - z) * 0.35
        half = math.radians(52 if z > 0.75 else 50)
        row = []
        for i in range(na):
            a = -half + 2 * half * i / (na - 1)
            rx = TA * s * 1.04 + 0.012 + flare * 0.6
            ry = TB * s * 1.08 + 0.016 + flare
            if front:
                ry *= 1.0 + 0.10 * max(0.0, 1 - abs(z - TC - 0.05) * 1.4) * math.cos(a)
            sgn = -1 if front else 1
            wave = 0.008 * math.sin(i * 1.7) * max(0.0, 0.7 - z) * 4
            row.append(bm.verts.new((rx * math.sin(a), sgn * (ry * math.cos(a) + wave), z)))
        grid.append(row)
    for r in range(len(zs) - 1):
        for i in range(na - 1):
            f = (grid[r][i], grid[r][i + 1], grid[r + 1][i + 1], grid[r + 1][i])
            bm.faces.new(f if front else tuple(reversed(f)))
    bm.normal_update()
    # thickness
    o = _obj(bm, TABARD)
    return o


for fr in (True, False):
    p = panel(fr)
    iso_paint(p, lambda q: q.z - 0.445, GOLD)          # gold hem
    B.append(p)
# chest emblem: little gold crown on the tabard front
EM = V(0, -0.325, 1.0)
cro = [(-0.085, -0.045), (0.085, -0.045), (0.085, 0.02), (0.1, 0.06), (0.055, 0.025), (0.0, 0.075), (-0.055, 0.025),
       (-0.1, 0.06), (-0.085, 0.02)]
crown = [flat_shape([(x, z) for x, z in reversed(cro)], 0.02, GOLD, M=Matrix.Translation(EM) @ rotm((-12, 0, 0)))]
for (x, z) in ((-0.1, 0.06), (0.0, 0.075), (0.1, 0.06)):
    crown.append(ell(EM + V(x, -0.01 - z * 0.2, z + 0.012), (0.017, 0.017, 0.017), seg=5, rings=3, material=GOLD))
B += crown
# belt over the tabard + buckle
belt = lathe([(0.0, 0.0)], seg=4) if False else None
B.append(lathe([(0.315, 0.645), (0.322, 0.67), (0.322, 0.71), (0.315, 0.735)], seg=10, material=ARMOR,
               M=Matrix.Diagonal((1.0, 0.92, 1, 1))))
B.append(ell(V(0, -0.305, 0.69), (0.065, 0.025, 0.055), seg=6, rings=4, p=0.7, material=GOLD))

# ---------------------------------------------------------------- pauldrons
for sx in (-1, 1):
    c = V(sx * 0.33, 0.0, 1.19)
    d1 = ell(c, (0.175, 0.19, 0.13), seg=10, rings=6, material=ARMOR, rot=(0, sx * 28, 0),
             shape=lambda n: Vector((n.x, n.y, n.z if n.z > -0.2 else -0.2 + (n.z + 0.2) * 0.3)))
    B.append(d1)
    rim = lathe([(0.17, -0.02), (0.18, 0.0), (0.17, 0.02)], seg=10, material=GOLD,
                M=Matrix.Translation(c + V(sx * 0.0, 0, -0.025)) @ rotm((0, sx * 28, 0)) @ Matrix.Diagonal((1.0, 1.1, 1, 1)))
    B.append(rim)
    B.append(ell(c + V(sx * 0.06, 0, 0.115), (0.025, 0.025, 0.025), seg=5, rings=3, material=GOLD))

# ---------------------------------------------------------------- left arm (+X) holding the shield
SHL = V(0.37, 0.0, 1.13)
ELB = V(0.47, -0.05, 0.87)
WRI = V(0.42, -0.25, 0.8)
B.append(tube([SHL, ELB], [0.085, 0.075], seg=8, material=ARMOR))
B.append(ell(ELB, (0.075, 0.075, 0.075), seg=6, rings=4, material=ARMOR))
B.append(tube([ELB, WRI], [0.072, 0.065], seg=8, material=ARMOR))
B.append(ell(WRI + V(-0.02, -0.04, 0), (0.07, 0.065, 0.06), seg=6, rings=4, material=ARMOR))

# heater shield: flat top, round sides, pointed bottom; slightly curved, facing front-left
outline = []
W, Ht = 0.29, 0.72
for i in range(5):  # top edge (slightly arched) from right to left
    x = W - 2 * W * i / 4
    outline.append((x, 0.30 + 0.025 * (1 - (x / W) ** 2)))
for i in range(1, 10):  # left side down to the point
    t = i / 9
    a = t * math.pi / 2
    x = -W * math.cos(a) ** 0.8 if t < 1 else 0.0
    z = 0.30 - (Ht) * math.sin(a) ** 1.6
    outline.append((x, z))
for i in range(8, 0, -1):
    t = i / 9
    a = t * math.pi / 2
    x = W * math.cos(a) ** 0.8
    z = 0.30 - (Ht) * math.sin(a) ** 1.6
    outline.append((x, z))
SC = V(0.6, -0.27, 0.88)
SD = V(0.62, -0.78, 0.0)       # shield faces this way (front-left)


def shield_xf(o, push=0.0):
    frame(o, SC + SD.normalized() * push, SD)
    return o


sh_face = flat_shape(outline, 0.045, SHIELD, curve=0.55, bevel=0.0)
xf(sh_face, Matrix.Translation((0, 0, 0.1)))
B.append(shield_xf(sh_face))
# steel rim = slightly larger plate behind the blue face
rim_o = flat_shape([(x * 1.13, z * 1.08 + 0.012) for (x, z) in outline], 0.03, ARMOR, curve=0.55)
xf(rim_o, Matrix.Translation((0, 0.014, 0.1)))
B.append(shield_xf(rim_o))
# gold cross (flat, follows the shield curve) + boss
cw = 0.042
cross = [(-cw, 0.36), (cw, 0.36), (cw, 0.14 + cw), (0.255, 0.14 + cw), (0.255, 0.14 - cw), (cw, 0.14 - cw), (cw, -0.5),
         (-cw, -0.5), (-cw, 0.14 - cw), (-0.255, 0.14 - cw), (-0.255, 0.14 + cw), (-cw, 0.14 + cw)]
cr = flat_shape(cross, 0.02, GOLD, curve=0.55)
# subdivide the long arms so they follow the curve: re-bend every vertex after a simple subdivision
bm = bmesh.new(); bm.from_mesh(cr.data)
bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if e.calc_length() > 0.12], cuts=2, use_grid_fill=False)
for v in bm.verts:
    v.co.y = (-0.01 if v.co.y < 0.0 + 0.55 * v.co.x ** 2 - 0.0 else 0.01)
for v in bm.verts:
    v.co.y += 0.55 * v.co.x ** 2 - 0.03
bm.to_mesh(cr.data); bm.free()
B.append(shield_xf(cr))
B.append(shield_xf(ell(V(0, -0.045, 0.14), (0.06, 0.035, 0.06), seg=6, rings=4, material=GOLD)))

body = apart(B, 'body', (0, 0, 0))

# ---------------------------------------------------------------- right arm (reaching out to -X), pivot = shoulder
SHR = V(-0.37, 0.0, 1.13)
E2 = V(-0.64, -0.03, 1.06)
W2 = V(-0.86, -0.05, 1.02)
FI = V(-0.94, -0.055, 1.01)
A = [tube([SHR + V(0.05, 0, 0), E2], [0.085, 0.077], seg=8, material=ARMOR),
     ell(E2, (0.08, 0.08, 0.08), seg=6, rings=4, material=ARMOR),
     spike(E2 + V(0, 0.05, 0.0), (0.0, 1, 0.3), r=0.05, h=0.09, seg=5, material=ARMOR),
     ell(E2 + V(0, 0.035, 0.0), (0.06, 0.03, 0.06), seg=6, rings=4, material=GOLD, rot=(0, 0, 0)),
     tube([E2, W2], [0.074, 0.068], seg=8, material=ARMOR),
     # flared gauntlet cuff
     tube([W2 + V(0.04, 0, 0), W2 + V(-0.035, 0, 0)], [0.07, 0.092], seg=8, material=ARMOR),
     tube([W2 + V(0.045, 0, 0), W2 + V(0.025, 0, 0)], [0.077, 0.079], seg=8, material=GOLD),
     # fist
     ell(FI, (0.085, 0.08, 0.078), seg=7, rings=5, p=0.85, material=ARMOR),
     ell(FI + V(-0.035, -0.06, 0.0), (0.05, 0.03, 0.065), seg=6, rings=4, material=ARMOR),     # curled fingers
     ell(FI + V(0.0, -0.045, 0.06), (0.04, 0.035, 0.028), seg=5, rings=3, material=ARMOR)]      # thumb
# flail handle gripped in the fist, chain ring at the outer end
HA0, HA1 = FI + V(0.0, 0.0, 0.12), FI + V(-0.1, 0.0, -0.14)
A.append(cyl_between(HA0, HA1, 0.027, seg=6, material=GOLD))
A.append(ell(HA0, (0.035, 0.035, 0.035), seg=6, rings=4, material=GOLD))
RING = HA1 + V(-0.03, 0, -0.04)
ring = bpy.data.objects.new('r', bpy.data.meshes.new('r'))
rg = lathe([(0.045, -0.012), (0.052, 0.0), (0.045, 0.012), (0.038, 0.0)], seg=6, material=STAR)
xf(rg, Matrix.Translation(RING) @ rotm((90, 0, -30)))
A.append(rg)
arm_r = apart(A, 'arm_r', SHR)

# ---------------------------------------------------------------- head (pivot = neck)
NECK = V(0, 0.0, 1.3)
HC = V(0, -0.01, 1.6)
HR = (0.3, 0.3, 0.31)


def helm(n):
    # bucket helm: boxy sides, rounded dome, slightly flared bottom
    z = n.z
    k = 1.0
    if z < 0:
        k = 1.0 + 0.07 * (-z) ** 2
        z = z * 0.95
    return Vector((n.x * k, n.y * k, z))


skull = ell(HC, HR, seg=16, rings=11, p=0.78, material=ARMOR, shape=helm)
SZ, SH, SW = 1.6, 0.06, 0.205


H = [skull]


def on_helm(x, z, depth=0.0):
    """Point on the helmet front surface at (x, z) and its normal."""
    ok, loc, nrm, idx = skull.ray_cast(V(x, -1.0, z), V(0, 1, 0))
    return loc - nrm * depth, nrm


def decal(cols, off=0.004, material=STAR):
    """cols = [(x, [z0, z1, ...]), ...] -> surface-following grid strip just above the helmet."""
    bm = bmesh.new()
    grid = []
    for x, zs in cols:
        col = []
        for z in zs:
            p, n = on_helm(x, z)
            col.append(bm.verts.new(p + n * off))
        grid.append(col)
    for i in range(len(grid) - 1):
        for j in range(len(grid[i]) - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    return _obj(bm, material)


bar = []
for i in range(13):
    x = -SW + 2 * SW * i / 12
    h = SH * max(0.25, (1 - (abs(x) / SW) ** 3)) ** 0.5
    bar.append((x, [SZ - h, SZ, SZ + h]))
H.append(decal(bar))
stem = []
for i in range(4):
    x = -0.034 + 0.068 * i / 3
    lo = SZ - 0.19
    stem.append((x, [lo, SZ - 0.12, SZ - SH + 0.005]))
H.append(decal(stem))


# gold brow band around the visor top + chin edge
brow = []
for i in range(9):
    x = -0.25 + i * 0.5 / 8
    p, n = on_helm(x, SZ + SH + 0.022)
    brow.append(p + n * 0.006)
H.append(tube(brow, 0.02, seg=4, material=GOLD, flat=0.6))
ridge = []
for z in (SZ + SH + 0.03, 1.75, 1.84):
    p, n = on_helm(0.0, z); ridge.append(p + n * 0.006)
ridge.append(HC + V(0, -0.05, 0.31))
H.append(tube(ridge, [0.02, 0.022, 0.022, 0.018], seg=5, material=GOLD, flat=0.7))
# eyes glowing in the visor bar (gold) with a little silver glint
for sx in (-1, 1):
    p, n = on_helm(sx * 0.098, SZ - 0.004)
    e = ell(V(0, 0, 0), (0.05, 0.016, 0.062), seg=8, rings=5, material=GOLD)
    H.append(frame(e, p + n * 0.006, -n))
    p2, n2 = on_helm(sx * 0.098 - 0.018, SZ + 0.022)
    g = ell(V(0, 0, 0), (0.014, 0.008, 0.016), seg=5, rings=3, material=ARMOR)
    H.append(frame(g, p2 + n2 * 0.017, -n2))
# plume holder + red plume (three fluffy feathers sweeping back)
H.append(lathe([(0.045, 1.87), (0.055, 1.91), (0.045, 1.96)], seg=8, material=GOLD, M=Matrix.Translation((0, 0.02, 0))))
for (dx, L, rr) in ((0.0, 1.0, 0.1), (0.08, 0.82, 0.075), (-0.08, 0.82, 0.075)):
    p0 = V(dx * 0.3, 0.02, 1.93)
    pts = bezier(p0, p0 + V(dx * 0.4, -0.14 * L, 0.2 * L), p0 + V(dx * 1.6, 0.36 * L, 0.24 * L), p0 + V(dx * 2.1, 0.6 * L, -0.1 * L), n=5)
    radii = [rr * (0.7 + 0.6 * math.sin(math.pi * min(1, (i / 5) * 1.1))) * (1 - (i / 5) ** 3 * 0.75) for i in range(6)]
    H.append(tube(pts, radii, seg=6, material=PLUME, flat=0.6, round_end=True))
head = apart(H, 'head', NECK)

# ---------------------------------------------------------------- morning star (origin at the ball centre)
SCN = V(-1.25, -0.2, 0.43)
S = [ell(V(0, 0, 0), (0.3, 0.3, 0.3), seg=11, rings=7, material=STAR)]
phi = (1 + 5 ** 0.5) / 2
ico_v = [V(a, b, c) for a, b, c in ((-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0), (0, -1, phi), (0, 1, phi),
                                       (0, -1, -phi), (0, 1, -phi), (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1))]
# rotate so it rests on three spikes: put a face normal straight down
fn = (ico_v[2] + ico_v[3] + ico_v[6]).normalized()
q = fn.rotation_difference(V(0, 0, -1))
for v in ico_v:
    d = (q @ v).normalized()
    S.append(spike(d * 0.27, d, r=0.075, h=0.22, seg=5, material=STAR))
eyelet = lathe([(0.05, -0.014), (0.06, 0.0), (0.05, 0.014), (0.04, 0.0)], seg=6, material=STAR)
xf(eyelet, Matrix.Translation((0, 0, 0.33)) @ rotm((90, 0, 0)))
S.append(eyelet)
S.append(lathe([(0.06, 0.27), (0.055, 0.31), (0.0, 0.315)], seg=6, material=STAR)) if False else None
star = apart(S, 'star', (0, 0, 0))
star.location = SCN

KS = 0.9
scale_all(KS)
star.data.transform(Matrix.Diagonal((1 / KS, 1 / KS, 1 / KS, 1)))   # keep the ball at r=0.30
NECK, SHR, FI, RING, SCN = (v * KS for v in (NECK, SHR, FI, RING, SCN))
SCN = SCN + V(-0.05, 0, 0.395 - SCN.z)
star.location = SCN
report()
notes = ('Parts/pivots (Blender coords, front -Y, left=+X; whole knight ~1.93 m incl. plume): body (origin 0,0,0: boots, '
         'greaves, fauld, breastplate, purple tabard with gold crown, pauldrons, left arm with blue heater shield + gold cross); '
         'head (pivot neck %s; bucket helm with dark T-visor, golden eyes, red plume); arm_r (pivot shoulder %s, reaches out to -X, '
         'gauntlet fist at %s gripping a gold flail handle; chain ring (attach the chain here) at %s); star (spiked ball r=0.30, '
         '12 spikes to r~0.49, origin at its centre, placed on the ground at %s; small eyelet on top). '
         'Materials: armor, tabard, shield, gold, plume, star (the dark T-visor and the chain ring also use material star, '
         'so with charModel(.., [\'star\']) the visor glows red together with the ball before a swing).'
         % (fmt(NECK), fmt(SHR), fmt(FI), fmt(RING), fmt(SCN)))
finish('chars', 'knight', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['head'].rotation_euler = (0, 0, 0.0)
        bpy.data.objects['arm_r'].rotation_euler = (0, 0.6, 0)
    views('knight', dirs={'front': (0, -1, 0.15), 'side': (-1, -0.2, 0.2), 'back': (-0.7, 1, 0.5),
                          'face': (0.2, -1, 0.1)}, pose=pose)
