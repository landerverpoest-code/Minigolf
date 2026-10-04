import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *
from gkit import _obj

# ---------------------------------------------------------------- materials (6)
SAND = mat('sandstone', '#e3bf7f', rough=0.85)
GROOVE = mat('groove', '#7a4f2a', rough=0.9)          # carved hieroglyphs, pupils, elytra seam
LAPIS = mat('lapis', '#2457c5', rough=0.4)
GOLD = mat('gold', '#ffc23a', rough=0.25, metal=0.9)  # the game may tint / flash it
GLOW = mat('glow_eyes', '#3ff2e0', rough=0.3, emit='#2cf5e0', emit_strength=3.0)
WHITE = mat('white', '#ffffff', rough=0.3)

# ================================================================= BASE (round sandstone drum with hieroglyph grooves)
R0, H0 = 0.45, 0.09          # plinth
R1, H1 = 0.415, 0.15         # drum
ZT = H0 + H1                 # top of the base = beetle origin height
Bs = []
Bs.append(bev(cyl(r=R0, h=H0, loc=(0, 0, H0 / 2), verts=24, material=SAND), 0.015))
Bs.append(bev(cyl(r=R1, h=H1, loc=(0, 0, H0 + H1 / 2), verts=24, material=SAND), 0.012))
# lapis inlay band on the plinth top edge with gold studs
Bs.append(lathe([(R1 + 0.002, H0 - 0.001), (R0 - 0.012, H0 - 0.001), (R0 - 0.012, H0 + 0.006), (R1 + 0.002, H0 + 0.006)],
                seg=24, material=LAPIS))
for k in range(12):
    a = TAU * (k + 0.5) / 12
    r = (R1 + R0) / 2 - 0.004
    Bs.append(ell(V(math.cos(a) * r, math.sin(a) * r, H0 + 0.008), (0.011, 0.011, 0.007), seg=6, rings=3, material=GOLD))
# top: carved ring around the beetle + lapis disk under it
Bs.append(lathe([(0.37, ZT + 0.001), (0.39, ZT + 0.001), (0.39, ZT + 0.004), (0.37, ZT + 0.004)], seg=24, material=GROOVE))


def bar(x0, z0, x1, z1, w=0.012):
    d = V(x1 - x0, 0, z1 - z0); L = d.length; d.normalize()
    nrm = V(-d.z, 0, d.x) * (w / 2)
    pts = [(x0 + nrm.x, z0 + nrm.z), (x1 + nrm.x, z1 + nrm.z), (x1 - nrm.x, z1 - nrm.z), (x0 - nrm.x, z0 - nrm.z)]
    return flat_shape(pts, 0.008, GROOVE)


def disc(x, z, r, n=8):
    return flat_shape([(x + math.cos(TAU * i / n) * r, z + math.sin(TAU * i / n) * r) for i in range(n)], 0.008, GROOVE)


def ring(x, z, r, w=0.01, n=8):
    o = lathe([(r - w / 2, -0.004), (r + w / 2, -0.004), (r + w / 2, 0.004), (r - w / 2, 0.004)], seg=n, material=GROOVE)
    return xf(o, Matrix.Translation((x, 0, z)) @ rotm((90, 0, 0)))


def glyph(kind):
    g = []
    if kind == 'ankh':
        g += [bar(0, -0.055, 0, 0.012), bar(-0.032, 0.012, 0.032, 0.012), ring(0, 0.036, 0.02, 0.011)]
    elif kind == 'eye':
        g += [bar(-0.045, 0.01, 0.0, 0.025), bar(0.0, 0.025, 0.045, 0.01), bar(-0.045, 0.01, 0.0, -0.005),
              bar(0.0, -0.005, 0.045, 0.01), disc(0, 0.01, 0.011), bar(0.0, -0.01, -0.01, -0.05), bar(0.012, -0.01, 0.035, -0.04)]
    elif kind == 'water':
        for zz in (0.03, 0.0, -0.03):
            for i in range(4):
                x0 = -0.048 + i * 0.024
                g.append(bar(x0, zz + (0.008 if i % 2 else -0.008), x0 + 0.024, zz + (-0.008 if i % 2 else 0.008), 0.009))
    elif kind == 'sun':
        g += [ring(0, 0.02, 0.03, 0.011, 10), disc(0, 0.02, 0.01, 6), bar(-0.04, -0.035, 0.04, -0.035), bar(0, -0.035, 0, -0.012)]
    elif kind == 'feather':
        g += [bar(0, -0.055, 0.0, 0.05, 0.01)]
        for i in range(4):
            z = -0.035 + i * 0.022
            g.append(bar(0.0, z, 0.022, z + 0.02, 0.008))
    return g


kinds = ['ankh', 'eye', 'water', 'sun', 'feather']
NG = 10
for k in range(NG):
    a = TAU * k / NG + 0.12
    d = V(math.cos(a), math.sin(a), 0)
    for o in glyph(kinds[k % len(kinds)]):
        Bs.append(frame(o, d * (R1 + 0.0015) + V(0, 0, H0 + H1 / 2), d))
# vertical divider lines between glyph columns
for k in range(NG):
    a = TAU * (k + 0.5) / NG + 0.12
    d = V(math.cos(a), math.sin(a), 0)
    Bs.append(frame(bar(0, -0.055, 0, 0.055, 0.008), d * (R1 + 0.0015) + V(0, 0, H0 + H1 / 2), d))
base = apart(Bs, 'base', (0, 0, 0))

# ================================================================= BEETLE (origin at its base centre on top of the drum)
O = V(0, 0, ZT)
Bt = []
# elytra: big glossy dome, slightly pointed at the back
EC = O + V(0, 0.1, 0.03)


def elytra_shape(n):
    t = max(0.0, n.y)
    return Vector((n.x * (1 - 0.18 * t * t), n.y, max(n.z, -0.25)))


ely = ell(EC, (0.27, 0.31, 0.2), seg=16, rings=10, material=GOLD, shape=elytra_shape)
Bt.append(ely)
# seam down the middle + two engraved lines per wing
seam = [EC + V(0, -0.27 + 0.56 * i / 6, 0) for i in range(7)]
seam = [p + V(0, 0, 0.2 * math.sqrt(max(0.0, 1 - ((p.y - EC.y) / 0.31) ** 2)) - 0.002) for p in seam]
Bt.append(tube(seam, 0.011, seg=4, material=GROOVE))
for sx in (-1, 1):
    ln = []
    for i in range(7):
        y = -0.24 + 0.46 * i / 6
        xx = sx * 0.12 * (1 - 0.3 * max(0.0, y / 0.31) ** 2)
        nz = 1 - (xx / 0.27) ** 2 - (y / 0.31) ** 2
        ln.append(EC + V(xx, y, 0.2 * math.sqrt(max(0.0, nz)) - 0.003))
    Bt.append(tube(ln, 0.006, seg=3, material=GROOVE))
# pronotum (front shield), wide and rounded
PC = O + V(0, -0.2, 0.05)
pro = ell(PC, (0.25, 0.14, 0.15), seg=14, rings=8, material=GOLD,
          shape=lambda n: Vector((n.x * (1 + 0.12 * n.y), n.y, max(n.z, -0.3))))
Bt.append(pro)
# lapis collar between pronotum and elytra
Bt.append(tube([O + V(math.sin(a) * 0.235, -0.08 + 0.02 * math.cos(a), 0.035 + 0.17 * math.cos(a) ** 0.8) for a in
                [(-1 + 2 * i / 8) * 1.45 for i in range(9)]], 0.018, seg=5, material=LAPIS))
# head with a toothed clypeus
HC = O + V(0, -0.36, 0.05)
head = ell(HC, (0.16, 0.1, 0.075), seg=12, rings=6, material=GOLD,
           shape=lambda n: Vector((n.x, n.y, max(n.z, -0.4))))
Bt.append(head)
for i in range(6):
    a = math.radians(-62 + 124 * i / 5)
    base_p = HC + V(math.sin(a) * 0.15, -math.cos(a) * 0.09, -0.005)
    Bt.append(spike(base_p, V(math.sin(a), -math.cos(a), 0.15), r=0.026, h=0.06, seg=4, material=GOLD))
# big glowing turquoise eyes with a dark pupil and glint
for sx in (-1, 1):
    ec = HC + V(sx * 0.075, -0.05, 0.065)
    Bt.append(ell(ec, (0.055, 0.05, 0.06), seg=10, rings=7, material=GLOW))
    Bt.append(ell(ec + V(-sx * 0.004, -0.044, 0.0), (0.024, 0.012, 0.03), seg=8, rings=4, material=GROOVE))
    Bt.append(ell(ec + V(sx * 0.008, -0.05, 0.022), (0.011, 0.006, 0.012), seg=5, rings=3, material=WHITE))
    # little antennae clubs
    a0 = HC + V(sx * 0.12, -0.05, 0.03)
    Bt.append(tube([a0, a0 + V(sx * 0.07, -0.06, 0.03)], 0.01, seg=4, material=GOLD))
    Bt.append(ell(a0 + V(sx * 0.08, -0.07, 0.035), (0.025, 0.018, 0.018), seg=6, rings=4, material=GOLD))
# six legs splayed onto the base top, toothed front legs
LEGS = [(-0.22, 0.2, -0.36, -0.36), (0.0, 0.22, 0.38, -0.08), (0.2, 0.2, 0.33, 0.32)]
for sx in (-1, 1):
    for k, (y0, x0, xf_, yf) in enumerate(LEGS):
        p0 = O + V(sx * x0, y0, 0.03)
        knee = O + V(sx * (x0 + xf_) * 0.62, (y0 + yf) / 2, 0.11)
        foot = O + V(sx * abs(xf_) * 0.95 if k else sx * 0.24, yf, 0.012)
        Bt.append(tube([p0, knee, foot], [0.03, 0.026, 0.018], seg=5, material=GOLD, round_end=True))
        Bt.append(ell(knee, (0.03, 0.03, 0.03), seg=6, rings=4, material=GOLD))
        if k == 0:    # teeth on the front tibia
            for t in (0.3, 0.55, 0.8):
                q = knee.lerp(foot, t)
                Bt.append(spike(q, V(sx * 1, -0.2, 0.3), r=0.014, h=0.035, seg=4, material=GOLD))
beetle = apart(Bt, 'beetle', O)

report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('De gouden skarabee. Parts/pivots (Blender coords, front -Y): base (origin 0,0,0; round sandstone base r=0.45, plinth + drum '
         f'with carved hieroglyph grooves (ankh, eye, water, sun, feather), lapis band with gold studs, top at z={ZT:.2f}); '
         f'beetle (origin at its base centre {fmt(O)} on top of the base; golden scarab in material "gold" ~0.85 m long, glowing turquoise '
         'eyes "glow_eyes", lapis collar, toothed head and legs; press it down along -Z). '
         'Materials: sandstone, groove, lapis, gold, glow_eyes, white.')
finish('chars', 'scarab', kind='char', footprint=0.45, grounded=False, notes=notes)
if '--views' in sys.argv:
    views2('scarab', dirs={'front': (0, -1, 0.4), 'side': (-1, 0, 0.3), 'top': (0.1, 0.2, 1), 'face': (0.3, -1, 0.5)}, dist=1.3)
