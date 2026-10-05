import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *
from okit import _obj

# Painted wooden carousel horse on a brass pole (castle carousel). Origin = ground point under the pole; pole z 1.05..3.25,
# horse z 1.22..1.98 around z 1.5, nose toward -Y (~0.65 long). Materials "coat" (white; game tints) and "saddle" (red; game tints).
COAT = mat('coat', '#f7f3ee', rough=0.4)
SADDLE = mat('saddle', '#d42a2a', rough=0.45)
GOLD = mat('gold', '#ffc23a', rough=0.25, metal=0.9)
DARK = mat('dark', '#2e2422', rough=0.4)
WHITE = mat('white', '#ffffff', rough=0.3)
JEWEL = mat('jewel', '#2f8fe8', rough=0.15, metal=0.3)

P = []
TILT = -7            # galloping: front slightly up


def T(p):
    """tilt a point of the horse around the body centre (front up)."""
    c = V(0, 0.02, 1.5)
    return c + (Matrix.Rotation(math.radians(TILT), 3, 'X') @ (V(p) - c))


# ------------------------------------------------------------------ body (barrel, chest, rump)
def body_shape(n):
    w = 0.9 + 0.1 * min(1.0, abs(n.y) * 1.8)            # slight waist under the saddle
    lift = 0.03 * max(0.0, -n.y) * (1 + n.z)            # deeper, higher chest
    return Vector((n.x * w, n.y, n.z * w + lift))


P.append(ell(T((0, 0.01, 1.515)), (0.094, 0.235, 0.1), seg=14, rings=9, rot=(TILT, 0, 0), material=COAT, p=0.85, shape=body_shape))

# ------------------------------------------------------------------ neck + head
NB = T((0, -0.12, 1.56))
neck_pts = bezier(NB, NB + V(0, -0.06, 0.1), V(0, -0.215, 1.76), V(0, -0.235, 1.82), n=5)
P.append(tube(neck_pts, [0.092, 0.085, 0.076, 0.067, 0.06, 0.055], seg=9, material=COAT, flat=0.8, flat_n=False))
HC = V(0, -0.255, 1.845)
P.append(ell(HC, (0.056, 0.102, 0.062), seg=10, rings=7, rot=(38, 0, 0), material=COAT,
             shape=lambda n: Vector((n.x * (1 - 0.12 * max(0, -n.y)), n.y, n.z))))
MZ = V(0, -0.33, 1.79)
P.append(ell(MZ, (0.05, 0.054, 0.047), seg=9, rings=6, material=COAT))
for sx in (-1, 1):   # nostrils
    P.append(ell(MZ + V(sx * 0.022, -0.046, 0.012), (0.009, 0.006, 0.011), seg=5, rings=3, material=DARK))
# smile
sm = [MZ + V(math.sin(a) * 0.046, -math.cos(a) * 0.047, -0.022 + 0.012 * (a / 1.0) ** 2) for a in [(-1 + 2 * i / 6) * 0.95 for i in range(7)]]
P.append(tube(sm, 0.0045, seg=4, material=DARK, round_end=True))
# big friendly eyes
for sx in (-1, 1):
    ec = HC + V(sx * 0.045, -0.012, 0.024)
    P += eye(ec, V(sx * 0.8, -0.9, 0.12), r=0.034, white=WHITE, black=DARK, depth=0.6, tall=1.2, pupil=0.7,
             look=(-sx * 0.25, 0, 0.05), seg=8, pseg=6, hl=False)
    hd = V(sx * 0.8, -0.9, 0.12).normalized()
    hx = hd.cross(V(0, 0, 1)).normalized(); hz = hx.cross(hd).normalized()
    P.append(ell(ec + hd * 0.0215 + hz * 0.011 + hx * 0.006, (0.0068, 0.0068, 0.0076), seg=6, rings=3, material=WHITE))   # highlight
    # lashes
    for (dy, dz) in ((0.016, 0.026), (0.002, 0.036)):   # two little upturned lashes at the outer top corner
        base = ec + V(sx * 0.024, dy, dz)
        P.append(tube([base, base + V(sx * 0.014, 0.008, 0.008), base + V(sx * 0.02, 0.016, 0.02)], [0.0045, 0.0035, 0.001],
                      seg=4, material=DARK))
    # ears
    eb = HC + V(sx * 0.032, 0.05, 0.06)
    P.append(tube([eb, eb + V(sx * 0.014, -0.004, 0.04), eb + V(sx * 0.02, 0.006, 0.072)], [0.024, 0.019, 0.003], seg=6,
                  flat=0.6, material=COAT))

# ------------------------------------------------------------------ carved mane + forelock (dark)
mp = bezier(V(0, -0.085, 1.645), V(0, -0.14, 1.745), V(0, -0.2, 1.86), V(0, -0.215, 1.905), n=4)
for i, p in enumerate(mp):
    side = 1 if i % 2 else -1
    q = p + V(side * 0.03, 0.005, 0.0)
    P.append(tongue(q, q + V(side * 0.03, 0.035, 0.01), q + V(side * 0.055, 0.06, -0.04), q + V(side * 0.06, 0.04, -0.09),
                    0.038 - i * 0.002, seg=5, n=3, material=DARK))
# forelock curl between the ears
fl = HC + V(0, -0.02, 0.07)
P.append(tongue(fl, fl + V(0, -0.04, 0.02), fl + V(0.01, -0.07, -0.01), fl + V(0.02, -0.06, -0.045), 0.024, seg=5, n=3, material=DARK))

# ------------------------------------------------------------------ legs in a stretched gallop
def leg(top, knee, fet, r0, r1):
    out = [tube([top, knee], [r0, r1 * 1.12], seg=8, material=COAT, cap=False),
           ell(knee, (r1 * 1.12, r1 * 1.12, r1 * 1.12), seg=7, rings=4, material=COAT),
           tube([knee, fet], [r1, r1 * 0.88], seg=8, material=COAT, cap=False)]
    d = (fet - knee).normalized()
    out.append(ell(fet, (r1 * 1.06, r1 * 1.06, r1 * 1.06), seg=7, rings=4, material=COAT))
    # hoof: short dark cylinder continuing the cannon bone
    h0 = fet + d * 0.006; h1 = fet + d * 0.045
    out.append(tube([h0, h1], [r1 * 1.1, r1 * 1.22], seg=8, material=DARK))
    out.append(tube([fet - d * 0.004, fet + d * 0.01], [r1 * 1.22, r1 * 1.22], seg=8, material=GOLD, cap=False))   # gold fetlock band
    return out


for sx in (-1, 1):
    x = sx * 0.05
    # front legs reaching forward (left one higher and bent)
    if sx > 0:
        P += leg(T((x * 0.8, -0.12, 1.5)), V(x, -0.225, 1.43), V(x, -0.24, 1.33), 0.052, 0.031)
    else:
        P += leg(T((x * 0.8, -0.12, 1.5)), V(x, -0.2, 1.39), V(x, -0.29, 1.305), 0.052, 0.031)
    # hind legs stretched back
    if sx > 0:
        P += leg(T((x * 0.8, 0.15, 1.5)), V(x, 0.215, 1.385), V(x, 0.285, 1.305), 0.06, 0.031)
    else:
        P += leg(T((x * 0.8, 0.15, 1.5)), V(x, 0.195, 1.375), V(x, 0.24, 1.28), 0.06, 0.031)

# ------------------------------------------------------------------ carved flowing tail (dark)
TR = T((0, 0.235, 1.56))
for k, (dx, L) in enumerate(((0.012, 1.0), (-0.02, 0.85))):
    pts = bezier(TR, TR + V(dx * 0.5, 0.07, 0.07 * L), TR + V(dx, 0.14 * L, -0.02), TR + V(dx * 1.4, 0.1 * L, -0.17 * L), n=4)
    rs = [0.03, 0.036, 0.03, 0.018, 0.004]
    P.append(tube(pts, [r * (1.1 if k == 0 else 0.85) for r in rs], seg=6, material=DARK, round_end=True))

# ------------------------------------------------------------------ saddle blanket, saddle, stirrups
# blanket: a curved sheet over the back with a scalloped gold edge
BC = T((0, 0.0, 1.5))
bm = bmesh.new()
NA, NYb = 6, 3
A0 = math.radians(78)
rows = []
for iy in range(NYb + 1):
    y = -0.09 + 0.2 * iy / NYb
    row = []
    for ia in range(NA + 1):
        a = -A0 + 2 * A0 * ia / NA
        row.append(bm.verts.new((math.sin(a) * 0.094, y, math.cos(a) * 0.1)))
    rows.append(row)
for iy in range(NYb):
    for ia in range(NA):
        bm.faces.new((rows[iy][ia], rows[iy][ia + 1], rows[iy + 1][ia + 1], rows[iy + 1][ia]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bl = _obj(bm, SADDLE)
bmesh_s = bl.modifiers.new('s', 'SOLIDIFY'); bmesh_s.thickness = 0.008; bmesh_s.offset = 1
bpy.context.view_layer.objects.active = bl; bpy.ops.object.modifier_apply(modifier='s')
xf(bl, Matrix.Translation(BC) @ rotm((TILT, 0, 0)))
P.append(bl)
for sx in (-1, 1):   # gold trim along the lower edges + jewel
    a = sx * A0
    e0 = BC + Matrix.Rotation(math.radians(TILT), 3, 'X') @ V(math.sin(a) * 0.103, -0.09, math.cos(a) * 0.109)
    e1 = BC + Matrix.Rotation(math.radians(TILT), 3, 'X') @ V(math.sin(a) * 0.103, 0.11, math.cos(a) * 0.109)
    P.append(tube([e0, e1], 0.009, seg=5, material=GOLD))
    mid = e0.lerp(e1, 0.5) + V(sx * 0.012, 0, 0.035)
    P.append(xf(ell((0, 0, 0), (0.006, 0.018, 0.022), seg=6, rings=3, material=JEWEL), Matrix.Translation(mid)))
    P.append(xf(ell((0, 0, 0), (0.004, 0.026, 0.03), seg=6, rings=3, material=GOLD), Matrix.Translation(mid - V(sx * 0.004, 0, 0))))
# saddle seat with pommel and cantle
SC = T((0, 0.005, 1.6))
P.append(ell(SC, (0.068, 0.075, 0.026), seg=10, rings=5, rot=(TILT, 0, 0), material=SADDLE))
P.append(ell(T((0, 0.075, 1.625)), (0.055, 0.018, 0.035), seg=8, rings=4, rot=(TILT - 15, 0, 0), material=SADDLE))   # cantle
P.append(ell(T((0, -0.07, 1.62)), (0.04, 0.02, 0.03), seg=7, rings=4, rot=(TILT + 15, 0, 0), material=SADDLE))      # pommel
P.append(ell(T((0, -0.078, 1.655)), (0.017, 0.017, 0.017), seg=8, rings=5, material=GOLD))                           # horn knob
P.append(tube([T((-0.075, 0.08, 1.625)), T((0, 0.098, 1.66)), T((0.075, 0.08, 1.625))], 0.006, seg=4, material=GOLD))  # cantle trim
for sx in (-1, 1):   # stirrup straps + gold stirrups
    s0 = T((sx * 0.07, 0.0, 1.585)); s1 = T((sx * 0.1, -0.005, 1.43))
    P.append(tube([s0, s1], 0.008, seg=4, flat=0.4, material=SADDLE))
    P.append(xf(torus(R=0.02, r=0.0055, seg=8, ring=3, material=GOLD), Matrix.Translation(s1 + V(0, 0, -0.018)) @ rotm((0, 90, 0))))
    P.append(bx(s1 + V(-0.008, -0.016, -0.042), s1 + V(0.008, 0.016, -0.034), GOLD))

# ------------------------------------------------------------------ bridle, reins, breast collar (gold, jewels)
P.append(xf(torus(R=1.0, r=0.1, seg=12, ring=3, material=GOLD),
            Matrix.Translation(MZ + V(0, 0.01, 0.004)) @ rotm((70, 0, 0)) @ Matrix.Diagonal((0.052, 0.046, 0.052, 1))))   # noseband
for sx in (-1, 1):
    P.append(tube([MZ + V(sx * 0.048, 0.01, 0.01), HC + V(sx * 0.054, 0.02, -0.01), HC + V(sx * 0.044, 0.065, 0.05)], 0.0055, seg=4,
                  material=GOLD))   # cheek strap
    P.append(xf(ell((0, 0, 0), (0.006, 0.015, 0.015), seg=6, rings=3, material=JEWEL), Matrix.Translation(HC + V(sx * 0.058, 0.025, -0.008))))
    P.append(tube([MZ + V(sx * 0.05, 0.015, -0.002), T((sx * 0.07, -0.13, 1.62)), T((sx * 0.03, -0.075, 1.645))], 0.0045, seg=4,
                  material=GOLD))   # reins
P.append(tube([HC + V(-0.046, 0.06, 0.055), HC + V(0, 0.03, 0.08), HC + V(0.046, 0.06, 0.055)], 0.0055, seg=4, material=GOLD))  # browband
# breast collar
bc = [T((math.sin(a) * 0.086, -0.115 - math.cos(a) * 0.092, 1.5 + 0.035 * math.cos(a))) for a in [(-1 + 2 * i / 6) * 1.45 for i in range(7)]]
P.append(tube(bc, 0.009, seg=4, material=GOLD))
med = T((0, -0.212, 1.535))
P.append(xf(ell((0, 0, 0), (0.026, 0.008, 0.026), seg=10, rings=4, material=GOLD), Matrix.Translation(med)))
P.append(xf(ell((0, 0, 0), (0.014, 0.008, 0.014), seg=6, rings=3, material=JEWEL), Matrix.Translation(med + V(0, -0.007, 0))))

# ------------------------------------------------------------------ brass pole with decorative rings
PR = 0.035
prof = [(0.0, 1.05), (0.045, 1.06), (0.05, 1.09), (PR, 1.12)]
for zc in (1.33, 1.69, 2.6):
    prof += [(PR, zc - 0.025), (0.05, zc), (PR, zc + 0.025)]
prof += [(PR, 3.16), (0.06, 3.2), (0.055, 3.235), (0.0, 3.25)]
P.append(lathe(prof, seg=8, material=GOLD))

body = part(P, 'body', (0, 0, 0), angle=60)
report()
std_view()
lo, hi = bounds([body]); print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Painted carousel horse on a brass pole. Part: body (origin (0,0,0) = ground point under the pole, no rotation). '
         'Brass pole r 0.035 (rings r 0.05) from z 1.05 to 3.25 on the Z axis; horse around z 1.5 (hooves z ~1.22 .. ear tips ~1.98), '
         'nose toward -Y, ~0.66 long (y -0.38..+0.28), galloping with stretched legs, carved dark mane/tail, big eyes. '
         'Materials: coat (white, game tints), saddle (red, game tints; saddle, blanket, stirrup straps), gold (pole, bridle, trim), '
         'dark, white, jewel.')
finish('chars', 'carousel_horse', kind='char', footprint=0.4, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('carousel_horse', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.5), 'face': (0.6, -1, 0.3)})
    montage('carousel_horse', keys=('front', 'side', 'back', 'face'))
