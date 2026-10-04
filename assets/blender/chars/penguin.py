import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ccp_kit import *

# ---------------------------------------------------------------- materials
BLACK = mat('penguin_black', '#1f2638', rough=0.45)
BELLY = mat('belly', '#fbfbf7', rough=0.55)          # the game makes this one glow when it is about to slide
WHITE = mat('white', '#ffffff', rough=0.35)          # face patches, eye whites, highlights, scarf stripes
ORANGE = mat('orange', '#ff9a1f', rough=0.45)
SCARF = mat('scarf', '#e2343f', rough=0.7)
BLUSH = mat('blush', '#ff8fa8', rough=0.6)

# ---------------------------------------------------------------- body
BC = V(0, 0.02, 0.53)
BR = (0.41, 0.38, 0.51)


def egg(n):
    k = 1.0 - 0.16 * n.z            # fatter at the bottom, slimmer at the top
    z = n.z if n.z > 0 else n.z * 0.92
    return Vector((n.x * k, n.y * k, z))


torso = ell(BC, BR, seg=20, rings=14, material=BLACK, shape=egg)
iso_paint(torso, lambda p: (p.x / 0.3) ** 2 + ((p.z - 0.47) / 0.44) ** 2 - 1 + max(0.0, p.y + 0.1) * 9, BELLY)
body_parts = [torso]
# feet
for sx in (-1, 1):
    fc = V(sx * 0.15, -0.2, 0.045)
    foot = ell(fc, (0.12, 0.16, 0.05), seg=10, rings=6, material=ORANGE, rot=(0, 0, sx * -14),
               shape=lambda n: Vector((n.x, n.y, n.z if n.z > 0 else n.z * 0.9)))
    body_parts.append(foot)
    for k in (-1, 0, 1):   # toes
        a = math.radians(sx * -14 + k * 28)
        tc = fc + V(math.sin(a) * 0.12 + 0.0, -math.cos(a) * 0.14, 0.0)
        body_parts.append(ell(tc, (0.045, 0.05, 0.04), seg=6, rings=4, material=ORANGE))
# little tail
body_parts.append(tube([BC + V(0, 0.3, -0.38), BC + V(0, 0.45, -0.48)], [0.1, 0.02], seg=6, flat=0.5, material=BLACK))
# scarf: ring around the neck + a hanging end, with white stripes
NZ = 0.93
ring = torus(R=0.255, r=0.07, loc=(0, 0, 0), seg=18, ring=6, material=SCARF)
xf(ring, Matrix.Translation((0, -0.01, NZ)) @ Matrix.Rotation(math.radians(-6), 4, 'X'))
body_parts.append(ring)
tail_pts = bezier(V(0.17, -0.22, NZ - 0.02), V(0.24, -0.3, NZ - 0.12), V(0.26, -0.33, NZ - 0.28), V(0.27, -0.3, NZ - 0.4), n=5)
scarf_end = tube(tail_pts, [0.06, 0.065, 0.068, 0.07, 0.07, 0.07], seg=6, flat=0.35, material=SCARF)
iso_paint(scarf_end, lambda p: abs(math.sin((p.z - NZ) * 26)) - 0.45, WHITE)
body_parts.append(scarf_end)
body_parts.append(ell(V(0.17, -0.24, NZ - 0.01), (0.07, 0.06, 0.06), seg=8, rings=5, material=SCARF))  # knot
body = part(body_parts, 'body', (0, 0, 0))

# ---------------------------------------------------------------- head (pivot = neck)
NECK = V(0, 0.0, 0.94)
HC = V(0, -0.02, 1.14)
skull = ell(HC, (0.3, 0.29, 0.285), seg=18, rings=12, material=BLACK,
            shape=lambda n: Vector((n.x, n.y, n.z * (1.0 + 0.04 * n.z))))
# white face patches around the eyes (heart-like mask)
FE = [V(0.112, -0.25, 1.155), V(-0.112, -0.25, 1.155)]


def face_field(p):
    d = min((p - c).length / 0.165 for c in FE) - 1
    return d + max(0.0, p.y + 0.05) * 6 + noise.noise(p * 6) * 0.0


iso_paint(skull, face_field, WHITE)
head_parts = [skull]
for sx in (-1, 1):
    ec = V(sx * 0.11, -0.255, 1.165)
    head_parts += eye(ec, V(sx * 0.38, -1, 0.05), r=0.085, white=WHITE, black=BLACK, depth=0.6, tall=1.22, pupil=0.7,
                      look=(-sx * 0.12, 0, 0.05), seg=10, pseg=9)
    head_parts.append(ell(V(sx * 0.19, -0.22, 1.06), (0.055, 0.02, 0.032), seg=6, rings=4, material=BLUSH,
                          rot=(0, 0, sx * -35)))
# beak: little rounded cone, slightly open smile line
bk = [V(0, -0.255, 1.085), V(0, -0.335, 1.08), V(0, -0.395, 1.072), V(0, -0.43, 1.066)]
head_parts.append(tube(bk, [0.08, 0.064, 0.038, 0.008], seg=8, flat=0.62, flat_n=True, material=ORANGE))
# hair tuft
for (x, a, l) in ((0.0, 0, 0.1), (-0.04, -28, 0.075), (0.04, 28, 0.075)):
    b = HC + V(x, 0.02, 0.27)
    tip = b + V(math.sin(math.radians(a)) * l, 0.03, math.cos(math.radians(a)) * l)
    head_parts.append(tube(bezier(b, b + V(0, 0, l * 0.6), tip, n=2), [0.035, 0.02, 0.004], seg=5, material=BLACK))
head = part(head_parts, 'head', NECK)

# ---------------------------------------------------------------- flippers (pivot = shoulder, hanging down)
FLIP = {}
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.34, 0.03, 0.78)
    pts = [SH + V(-sx * 0.04, 0, 0.02), SH + V(sx * 0.04, -0.01, -0.12), SH + V(sx * 0.09, -0.01, -0.28), SH + V(sx * 0.12, 0.0, -0.42)]
    fl = tube(pts, [0.075, 0.1, 0.085, 0.03], seg=8, flat=0.42, flat_n=True, material=BLACK, round_end=True)
    # orient the flat side to face outwards: rotate cross-section so the thin axis points along X
    part([fl], f'flipper_{side}', SH)
    FLIP[side] = SH

report()
fmt = lambda v: '(%.3g,%.3g,%.3g)' % tuple(v)
notes = ('Parts/pivots (Blender coords, front -Y, left=+X): body (origin 0,0,0; black egg body, white belly material "belly", '
         f'orange feet, red scarf); head (pivot neck {fmt(NECK)}; white face patches, eyes, beak, blush, tuft); '
         f'flipper_l shoulder {fmt(FLIP["l"])}, flipper_r shoulder {fmt(FLIP["r"])} (hanging down along the body). '
         'Materials: penguin_black, belly, white, orange, scarf, blush.')
finish('chars', 'penguin', kind='char', footprint=0.42, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['head'].rotation_euler = (0, 0, 0.5)
        bpy.data.objects['flipper_l'].rotation_euler = (0, -0.9, 0)
        bpy.data.objects['flipper_r'].rotation_euler = (0.8, 0, 0)
    views('penguin', pose)
