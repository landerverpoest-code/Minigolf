import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *

# ---------------------------------------------------------------- materials (6)
WHITE = mat('goose_white', '#f6f3ea', rough=0.6)
GREY = mat('goose_grey', '#c9ccd6', rough=0.6)        # wing feather tips, tail shading
ORANGE = mat('goose_orange', '#ff8a1c', rough=0.45)
EYEW = mat('eye_white', '#ffffff', rough=0.3)
DARK = mat('goose_dark', '#1d1f2b', rough=0.4)         # pupils, brows, nostrils
BLUSH = mat('blush', '#ff97ad', rough=0.6)

# ---------------------------------------------------------------- body (plump, breast low at the front, tail up at the back)
BC = V(0, 0.05, 0.44)


def goose_body(n):
    y = n.y
    # tail end: taper and lift; breast: fuller and lower
    k = 1.0 - 0.32 * max(0.0, y) ** 2
    z = n.z * k + 0.42 * max(0.0, y) ** 2.2
    z -= 0.12 * max(0.0, -y) ** 2 * (1 - n.z) * 0.6
    x = n.x * (1.0 - 0.25 * max(0.0, y) ** 2)
    return Vector((x, y, z))


torso = ell(BC, (0.245, 0.34, 0.21), seg=18, rings=11, material=WHITE, shape=goose_body)
B = [torso]
# tail tuft: three pointy feathers fanning up/back
for dx, a in ((0.0, 0), (0.05, 22), (-0.05, -22)):
    p0 = V(dx * 0.5, 0.3, 0.57)
    tip = p0 + V(dx, 0.13, 0.09 if dx == 0 else 0.06)
    B.append(tube(bezier(p0, p0 + V(dx * 0.4, 0.07, 0.01), tip, n=3), [0.065, 0.055, 0.035, 0.008], seg=6, flat=0.45,
                  material=WHITE))
# chest fluff (a few soft bumps at the breast)
for (x, z) in ((0.0, 0.38), (0.09, 0.42), (-0.09, 0.42)):
    B.append(ell(V(x, -0.255 + abs(x) * 0.35, z), (0.08, 0.05, 0.07), seg=8, rings=5, material=WHITE))
body = apart(B, 'body', (0, 0, 0))

# ---------------------------------------------------------------- neck + head (pivot at neck base on the body front)
NECK = V(0, -0.2, 0.5)
npts = bezier(NECK + V(0, 0.04, -0.04), V(0, -0.36, 0.56), V(0, -0.2, 0.7), V(0, -0.3, 0.8), n=6)
H = [tube(npts, [0.1, 0.075, 0.062, 0.058, 0.058, 0.062, 0.07], seg=9, material=WHITE)]
HC = V(0, -0.31, 0.82)
skull = ell(HC, (0.125, 0.135, 0.12), seg=13, rings=9, material=WHITE,
            shape=lambda n: Vector((n.x * (1 - 0.15 * max(0, -n.y)), n.y, n.z * (1 + 0.08 * n.z))))
H.append(skull)
# beak: chunky orange wedge with a knob, slightly open grin line made by a darker lower mandible gap
BK0 = HC + V(0, -0.11, -0.025)
H.append(tube([BK0, BK0 + V(0, -0.07, -0.01), BK0 + V(0, -0.14, -0.025), BK0 + V(0, -0.175, -0.035)],
              [0.068, 0.06, 0.045, 0.014], seg=8, flat=0.62, flat_n=True, material=ORANGE, round_end=True))
H.append(ell(BK0 + V(0, 0.005, 0.045), (0.035, 0.04, 0.03), seg=8, rings=5, material=ORANGE))   # knob
# lower mandible (separate wedge below, makes a "honk" grin)
H.append(tube([BK0 + V(0, 0.0, -0.04), BK0 + V(0, -0.08, -0.05), BK0 + V(0, -0.13, -0.055)],
              [0.042, 0.03, 0.01], seg=7, flat=0.5, flat_n=True, material=ORANGE, round_end=True))
for sx in (-1, 1):  # nostrils
    H.append(ell(BK0 + V(sx * 0.02, -0.065, 0.022), (0.009, 0.014, 0.006), seg=5, rings=3, material=DARK))
# big angry-cute eyes + brows
for sx in (-1, 1):
    ec = HC + V(sx * 0.072, -0.093, 0.035)
    H += eye(ec, V(sx * 0.5, -1, 0.08), r=0.052, white=EYEW, black=DARK, depth=0.6, tall=1.22, pupil=0.66,
             look=(-sx * 0.25, 0, -0.05), seg=9, pseg=7)
    # angry brow: thick dark bar slanting down toward the beak
    b0 = HC + V(sx * 0.125, -0.07, 0.12)
    b1 = HC + V(sx * 0.03, -0.12, 0.088)
    H.append(tube([b0, (b0 + b1) / 2 + V(0, -0.012, 0.01), b1], [0.014, 0.017, 0.013], seg=5, material=DARK,
                  round_end=True))
    H.append(ell(HC + V(sx * 0.095, -0.08, -0.035), (0.03, 0.012, 0.018), seg=6, rings=4, material=BLUSH,
                 rot=(0, 0, sx * -40)))
# little head crest feathers
for dx, a in ((0, 0), (0.025, 25), (-0.025, -25)):
    b = HC + V(dx, 0.02, 0.11)
    tip = b + V(math.sin(math.radians(a)) * 0.06, 0.04, 0.05)
    H.append(tube(bezier(b, b + V(0, 0, 0.04), tip, n=2), [0.022, 0.014, 0.003], seg=5, material=WHITE))
neck = apart(H, 'neck', NECK)

# ---------------------------------------------------------------- wings (pivot at the shoulder, folded along the body)
WING = {}
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.2, -0.12, 0.53)
    W = []
    wc = SH + V(sx * 0.055, 0.2, 0.0)

    def wshape(n):
        # teardrop: round at the front (shoulder), pointed toward the back
        t = max(0.0, n.y)
        return Vector((n.x * (1 - 0.5 * t ** 2), n.y, n.z * (1 - 0.55 * t ** 1.5) + 0.25 * t ** 2))

    w = ell(wc, (0.052, 0.26, 0.14), seg=12, rings=8, material=WHITE, shape=wshape, rot=(-8, 0, 0))
    W.append(w)
    # long primary feathers at the trailing edge (grey tips)
    for k, (dz, ln) in enumerate(((0.04, 0.17), (0.0, 0.21), (-0.04, 0.16))):
        p0 = wc + V(sx * 0.0, 0.1, dz + 0.04)
        p1 = p0 + V(-sx * 0.04, ln, 0.05 + dz * 0.4)
        f = tube([p0, (p0 + p1) / 2 + V(sx * 0.008, 0, 0.012), p1], [0.045, 0.04, 0.008], seg=6, flat=0.4,
                 material=GREY, round_end=True)
        W.append(f)
    # covert feather scallops on the wing face
    for k, (dy, dz) in enumerate(((-0.02, 0.04), (0.06, 0.01), (-0.02, -0.05))):
        W.append(ell(wc + V(sx * 0.04, dy, dz), (0.022, 0.055, 0.04), seg=6, rings=4, material=WHITE))
    apart(W, f'wing_{side}', SH)
    WING[side] = SH

# ---------------------------------------------------------------- legs (pivot at the hip, webbed feet on z=0)
LEG = {}
for side, sx in (('l', 1), ('r', -1)):
    HP = V(sx * 0.1, 0.08, 0.3)
    L = [ell(HP + V(0, 0, -0.04), (0.06, 0.07, 0.06), seg=8, rings=5, material=WHITE)]   # feathered thigh
    knee = V(sx * 0.105, 0.06, 0.14)
    ank = V(sx * 0.11, 0.02, 0.035)
    L.append(tube([HP + V(0, 0, -0.07), knee, ank], [0.032, 0.028, 0.03], seg=7, material=ORANGE))
    L.append(ell(knee, (0.03, 0.03, 0.03), seg=6, rings=4, material=ORANGE))
    # webbed foot outline (x, forward)
    outline = [(-0.035, 0.0), (-0.1, 0.13), (-0.04, 0.11), (0.0, 0.17), (0.04, 0.11), (0.1, 0.13), (0.035, 0.0),
               (0.0, -0.035)]
    foot = flat_shape(outline, 0.028, ORANGE, bevel=0.008)
    xf(foot, Matrix.Translation((ank.x, ank.y + 0.01, 0.014)) @ rotm((0, 0, sx * -8)) @ rotm((90, 0, 0)))
    L.append(foot)
    for (tx, tf) in ((-0.1, 0.13), (0.0, 0.17), (0.1, 0.13)):   # rounded toe tips
        p = Matrix.Translation((ank.x, ank.y + 0.01, 0.0)) @ rotm((0, 0, sx * -8)) @ Vector((tx, -tf, 0.0))
        L.append(ell(p + V(0, 0, 0.016), (0.024, 0.024, 0.016), seg=6, rings=4, material=ORANGE))
    apart(L, f'leg_{side}', HP)
    LEG[side] = HP

report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('Gans Gerda. Parts/pivots (Blender coords, front -Y, left=+X; ~0.95 m tall to the head): '
         f'body (origin 0,0,0; plump white body, fanned tail, chest fluff); neck (pivot neck base {fmt(NECK)}; S-neck, '
         'head with orange beak + knob, big angry-cute eyes with brows, blush, crest); '
         f'wing_l (pivot shoulder {fmt(WING["l"])}), wing_r (pivot shoulder {fmt(WING["r"])}) folded along the body, '
         f'flap by rotating about Y; leg_l (pivot hip {fmt(LEG["l"])}), leg_r (pivot hip {fmt(LEG["r"])}) orange legs with '
         'webbed feet on z=0. Collision radius 0.34. Materials: goose_white, goose_grey, goose_orange, eye_white, goose_dark, blush.')
finish('chars', 'goose', kind='char', footprint=0.34, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['wing_l'].rotation_euler = (0, -1.0, 0)
        bpy.data.objects['wing_r'].rotation_euler = (0, 1.0, 0)
        bpy.data.objects['neck'].rotation_euler = (0.3, 0, 0)
        bpy.data.objects['leg_l'].rotation_euler = (0.5, 0, 0)
    views2('goose', dirs={'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (0.7, 1, 0.5), 'face': (0.3, -1, 0.2)})
    views2('goose_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose)
