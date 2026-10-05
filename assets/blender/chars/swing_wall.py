import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from b6kit import *

# Haunted-crypt swinging wall. body: X -1..1 (game scales X), Z -0.05..1.25, Y +-0.14, origin = pivot (0,0,0).
# pillar: static central pivot pillar, r 0.27, height 1.6, origin ground centre.
ST1 = mat('crypt_stone', '#9a93a6', rough=0.85)
ST2 = mat('crypt_stone2', '#6c6578', rough=0.88)
DARK = mat('crypt_dark', '#2f2a36', rough=0.9)
MOSS = mat('moss', '#6aa83e', rough=0.9)
RUNE = mat('rune', '#18221c', rough=0.5, emit='#7dff9a', emit_strength=0.9)
IRON = mat('crypt_iron', '#3b3a46', rough=0.45, metal=0.75)

rnd = random.Random(11)
X0, X1, Z0, Z1, T = -1.0, 1.0, -0.05, 1.25, 0.14
G = 0.011                      # half mortar gap
P = []

# mortar core (shows in the joints)
P.append(bx((X0 + 0.004, -0.112, Z0), (X1 - 0.004, 0.112, 1.16), DARK))


def row_cuts(n, off):
    """Block boundaries along X for one course (staggered by off)."""
    w = (X1 - X0) / n
    xs = [X0] + [X0 + w * (i + off) + rnd.uniform(-0.05, 0.05) for i in range(1, n)] + [X1]
    if off > 0.5:
        xs = [X0] + [X0 + w * (i + off - 1) + rnd.uniform(-0.05, 0.05) for i in range(1, n + 1)] + [X1]
    return sorted(set(round(x, 4) for x in xs if X0 <= x <= X1))


def drape(xa, xb, z, L, s, rnd, up=False, th=0.006):
    """Moss sheet on a face (y = s*T): straight edge at z, lobed edge L away (down, or up for foot tufts)."""
    n = 7
    pts = [(xa, 0.0)]
    for i in range(n + 1):                      # lobed edge from xa to xb (CCW: down the left, along the bottom)
        t = i / n
        lob = (0.45 + 0.55 * rnd.random()) * (0.5 if i % 2 else 1.0)
        if i in (0, n):
            lob = 0.12
        pts.append((xa + (xb - xa) * t, -L * lob))
    pts.append((xb, 0.0))
    if up:
        pts = [(x, -v) for (x, v) in pts][::-1]
    if s > 0:
        pts = [(-x, v) for (x, v) in pts][::-1]
    o = relief(pts, 0, th, MOSS)
    if s < 0:
        place(o, (0, -T + 0.0005, z), (90, 0, 0))
    else:
        place(o, (0, T - 0.0005, z), (90, 0, 180))
    return o


rows = [(Z0, 0.25, 4, 0.0), (0.25, 0.53, 5, 0.5), (0.53, 0.8, 4, 0.3)]
k = 0
for (za, zb, n, off) in rows:
    xs = row_cuts(n, off)
    for xa, xb in zip(xs, xs[1:]):
        d = T - rnd.choice((0.0, 0.0, 0.004, 0.008))
        ga = 0.0 if xa <= X0 else G
        gb = 0.0 if xb >= X1 else G
        m = ST1 if (k * 3 + n) % 5 not in (1, 3) else ST2
        P.append(bx((xa + ga, -d, za + (G if za > Z0 else 0)), (xb - gb, d, zb - G), m, 0.024))
        k += 1

# rune band: recessed dark channel with stone lips and glyphs on BOTH faces
BZ0, BZ1 = 0.8, 0.99
P.append(bx((X0, -0.122, BZ0 + 0.004), (X1, 0.122, BZ1 - 0.004), DARK, 0.008))
for s in (-1, 1):
    yy = s * 0.122
    n = Vector((0, s, 0))
    for zl in (0.83, 0.96):                                   # long guide lines along X
        P.append(ribbon([(X0 + 0.03, yy, zl), (X1 - 0.03, yy, zl)], 0.011, n, RUNE, lift=0.003, taper=False))
    # glyphs (drawn narrow in X because the game stretches X ~2x); skip the hidden middle inside the pillar
    GL = [
        [[(0, -1), (0, 1)], [(0, 0.6), (0.5, 0.15)], [(0, 0.1), (0.5, -0.35)]],          # F-like
        [[(-0.45, -1), (0, 1), (0.45, -1)], [(-0.25, -0.15), (0.25, -0.15)]],             # A-like
        [[(0, -1), (0, 1)], [(-0.45, 0.45), (0, 1), (0.45, 0.45)]],                       # arrow
        [[(-0.4, -1), (-0.4, 1), (0.4, -1), (0.4, 1)]],                                    # N-like
        [[(0, -1), (0, 1)], [(-0.4, 0.3), (0.4, -0.3)], [(-0.4, -0.3), (0.4, 0.3)]],     # star
        [[(-0.4, 1), (0.4, 0.3), (-0.4, -0.3), (0.4, -1)]],                               # S-zigzag
    ]
    gx = [-0.9, -0.72, -0.54, -0.36, -0.2, 0.2, 0.36, 0.54, 0.72, 0.9]
    for i, cx in enumerate(gx):
        g = GL[(i * 5 + (s > 0) * 2) % len(GL)]
        for stroke in g:
            pts = [(cx + u * 0.035 * s * -1, yy, 0.895 + v * 0.042) for (u, v) in stroke]
            P.append(ribbon(pts, 0.012, n, RUNE, lift=0.004, taper=False))

# top course: crumbled blocks (XZ outline extruded through Y), heights vary, chipped corners
xs = row_cuts(4, 0.65)
TOPZ = [1.255, 1.21, 1.235, 1.19, 1.25, 1.22]
for i, (xa, xb) in enumerate(zip(xs, xs[1:])):
    ga = 0.0 if xa <= X0 else G
    gb = 0.0 if xb >= X1 else G
    a, b = xa + ga, xb - gb
    zt = TOPZ[i % len(TOPZ)]
    za = BZ1 + G
    chip = rnd.choice(('l', 'r', 'n', 'lr'))
    w = b - a
    pts = [(a, za), (b, za)]
    if 'r' in chip:
        pts += [(b, zt - 0.075), (b - w * 0.18, zt - 0.02), (b - w * 0.3, zt)]
    else:
        pts += [(b, zt)]
    pts += [(a + w * 0.55, zt - 0.012)]
    if 'l' in chip:
        pts += [(a + w * 0.25, zt), (a + w * 0.12, zt - 0.045), (a, zt - 0.06)]
    else:
        pts += [(a, zt - 0.005)]
    d = T - rnd.choice((0.0, 0.004))
    o = prism(pts, -d, d, ST1 if i % 2 else ST2)
    place(o, (0, 0, 0), (90, 0, 0)); bevel_obj(o, 0.022, angle=30)
    P.append(o)
    # moss cushion on top of the lower blocks
    if zt < 1.24:
        cx = a + w * rnd.uniform(0.35, 0.6)
        mz = zt - 0.012
        P.append(ico(r=1, loc=(0, 0, 0), sub=1, material=MOSS, smooth=True, scale=(w * 0.26, 0.13, 0.05), jitter=0.03, seed=i))
        o = P[-1]
        lo = min(v.co.z for v in o.data.vertices); hi = max(v.co.z for v in o.data.vertices)
        sc = (Z1 - 0.002 - mz) / max(hi, 1e-3)
        for v in o.data.vertices:
            v.co.z = max(v.co.z, lo * 0.3) * (sc if v.co.z > 0 else 1.0)
            v.co.y = max(-T - 0.003, min(T + 0.003, v.co.y))
            v.co += Vector((cx, 0, mz))
        o.data.update()
        # moss draping down both faces from the cushion
        for s in (-1, 1):
            P.append(drape(cx - w * 0.22, cx + w * 0.22, mz + 0.012, 0.13, s, rnd))

# moss tufts creeping up from the foot of the wall
for (xa, xb, s) in ((-0.95, -0.6, -1), (0.3, 0.55, -1), (0.55, 0.92, 1), (-0.5, -0.25, 1), (0.85, 1.0, -1)):
    P.append(drape(xa, xb, -0.03, 0.1, s, rnd, up=True))
P.append(drape(-0.62, -0.46, 0.52, 0.07, -1, rnd))
P.append(drape(0.56, 0.7, 0.8, 0.09, 1, rnd))
# a few dark cracks in the stone faces
for s in (-1, 1):
    for (x, z) in ((-0.62, 0.42), (0.3, 0.12), (0.8, 0.66)):
        pts = [(x + s * 0.02, s * T, z + 0.1), (x - 0.02, s * T, z + 0.04), (x + 0.03, s * T, z - 0.02), (x, s * T, z - 0.08)]
        P.append(ribbon(pts, 0.012, (0, s, 0), DARK, lift=0.002))

body = part(P, 'body', (0, 0, 0), angle=50)

# ------------------------------------------------------------------ pillar
Q = []
R = 0.27
prof = [(0.0, 0.0), (0.3, 0.0), (0.3, 0.1), (0.285, 0.125), (R, 0.135),
        (R, 0.43), (R - 0.014, 0.44), (R - 0.014, 0.455), (R, 0.465),
        (R, 0.79), (R - 0.014, 0.8), (R - 0.014, 0.815), (R, 0.825),
        (R, 1.27), (0.0, 1.27)]
Q.append(lathe(prof, seg=16, material=ST2, phase=TAU / 32))
# vertical joints between the pillar blocks (staggered)
for (z0, z1, ph) in ((0.135, 0.44, 0.0), (0.455, 0.8, 0.5), (0.815, 1.27, 0.25)):
    for kk in range(3):
        a = TAU * (kk + ph) / 3 + 0.3
        n = Vector((math.cos(a), math.sin(a), 0))
        c = n * R
        Q.append(ribbon([c + Vector((0, 0, z0 + 0.01)), c + Vector((0, 0, z1 - 0.01))], 0.014, n, DARK, lift=0.002, taper=False))
# iron band (ring) with rivets, just above the wall top
Q.append(lathe([(0.0, 1.265), (0.284, 1.265), (0.284, 1.305), (0.0, 1.305)], seg=16, material=IRON, smooth=False))
for kk in range(6):
    a = TAU * kk / 6 + TAU / 4 + TAU / 12
    Q.append(ell((math.cos(a) * 0.286, math.sin(a) * 0.286, 1.285), (0.013, 0.013, 0.013), seg=5, rings=3, material=IRON))
# upper drum + stone cap
Q.append(lathe([(0.0, 1.305), (R, 1.305), (R, 1.515), (0.0, 1.515)], seg=16, material=ST2, phase=TAU / 32))
Q.append(lathe([(0.0, 1.51), (0.29, 1.51), (0.305, 1.525), (0.305, 1.575), (0.285, 1.6), (0.0, 1.6)], seg=16,
               material=ST1, phase=TAU / 32, smooth=False))
# carved skull on the front (-Y) above the wall top, glowing rune eyes, iron knocker ring in its teeth
SK = Vector((0, -0.215, 1.425))
Q.append(ell(SK, (0.12, 0.085, 0.105), seg=12, rings=7, material=ST1))                                    # cranium
Q.append(ell(SK + Vector((0, -0.025, -0.07)), (0.078, 0.06, 0.05), seg=10, rings=5, material=ST1))       # cheeks/jaw
for sx in (-1, 1):
    Q.append(ell(SK + Vector((sx * 0.047, -0.07, 0.005)), (0.036, 0.022, 0.04), seg=8, rings=5, material=DARK))   # socket
    Q.append(ell(SK + Vector((sx * 0.047, -0.085, 0.006)), (0.016, 0.01, 0.018), seg=6, rings=4, material=RUNE))  # eye glow
Q.append(relief([(-0.017, 0.0), (0.017, 0.0), (0.0, 0.034)], 0, 0.02, DARK))                             # nose
place(Q[-1], SK + Vector((0, -0.078, -0.058)), (90, 0, 0))
for kk in range(4):
    tx = (kk - 1.5) * 0.026
    Q.append(bx((tx - 0.011, -0.307, 1.322), (tx + 0.011, -0.285, 1.354), ST1))                           # teeth
Q.append(torus(R=0.045, r=0.009, loc=(0, -0.314, 1.3), rot=(math.pi / 2, 0, 0), seg=10, ring=4, material=IRON))
# moss cushions around the foot
for kk, a in enumerate((0.9, 2.3, 4.0, 5.3)):
    o = ico(r=1, loc=(0, 0, 0), sub=1, material=MOSS, smooth=True, scale=(0.11, 0.055, 0.06), jitter=0.018, seed=40 + kk)
    xf(o, Matrix.Translation((math.cos(a) * 0.285, math.sin(a) * 0.285, 0.1)) @ rotm((0, 0, math.degrees(a) + 90)))
    Q.append(o)
pillar = part(Q, 'pillar', (0, 0, 0), angle=50)

report(); print_ext()
std_view()
notes = ('Haunted-crypt swinging wall. Parts: body = the wall, origin (0,0,0) = ground centre = pivot (rotate around Blender Z '
         '= three.js y); spans X -1..1 (scale X to the real length), Z -0.05..1.25, Y -0.14..0.14 (moss up to +-0.143); '
         'stone block courses with staggered joints, crumbled mossy top course, recessed rune band z 0.80..0.99 on both faces '
         'with glyph strokes in material "rune" (dark base, green emissive driven by the game). '
         'pillar = static central pivot pillar, origin ground centre: shaft r 0.27, height 1.6, foot r 0.30, stone cap r 0.305 '
         '(z 1.51..1.6), iron band at z 1.265..1.305, carved skull with glowing rune eyes on the front (-Y) above the wall top '
         '(z 1.32..1.53, front to y -0.31) holding an iron knocker ring (bottom z 1.246), moss at the foot.')
finish('chars', 'swing_wall', kind='char', footprint=1.0, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('swing_wall'); montage('swing_wall', keys=('front', 'side', 'back', 'top'))
if '--big' in sys.argv:
    views('swing_wall_big', size=640, dirs={'f': (0.5, -1, 0.35), 'b': (-0.5, 1, 0.35)})
