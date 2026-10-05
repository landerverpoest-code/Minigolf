import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from dkit import *
from dkit import _obj

# Cute chunky floating astronaut (LIFE_BRIEF "space/astronaut"). Origin = body centre, front = -Y, left = +X.

# ---------------------------------------------------------------- materials (5)
WHITE = mat('suit_white', '#f3f3ee', rough=0.55)
ORANGE = mat('suit_orange', '#ff7417', rough=0.5)
GREY = mat('suit_grey', '#76808f', rough=0.45, metal=0.25)
VISOR = mat('visor', '#ffb62a', rough=0.14, metal=0.85)
GLOW = mat('glow_suit', '#60f6ff', rough=0.4, emit='#3fe9ff', emit_strength=2.5)

# ---------------------------------------------------------------- body: torso, belt, chest box, legs, boots, backpack
B = []
TC = V(0, 0, -0.1)
torso = ell(TC, (0.3, 0.25, 0.31), seg=12, rings=8, p=0.85, material=WHITE,
            shape=lambda n: Vector((n.x * (1 - 0.08 * n.z), n.y * (1 - 0.05 * n.z), n.z)))
B.append(torso)
# belt
B.append(lathe([(0.3, -0.27), (0.315, -0.235), (0.3, -0.2)], seg=12, material=GREY, caps=(False, False),
               M=Matrix.Translation((0, 0, 0)) @ Matrix.Diagonal((1.0, 0.84, 1, 1))))
B.append(ell(V(0, -0.255, -0.235), (0.06, 0.02, 0.045), seg=6, rings=4, p=0.6, material=ORANGE))     # buckle
# chest control box with buttons
B.append(ell(V(0, -0.24, -0.04), (0.14, 0.05, 0.09), seg=6, rings=4, p=0.55, material=GREY))
for k, m in enumerate((GLOW, ORANGE, GLOW)):
    B.append(ell(V(-0.07 + k * 0.07, -0.29, -0.02), (0.022, 0.012, 0.022), seg=6, rings=4, material=m))
B.append(ell(V(0.0, -0.29, -0.085), (0.075, 0.01, 0.016), seg=6, rings=3, material=ORANGE))
# round mission patch (orange) on the left chest + stripe on the right
B.append(ell(V(0.165, -0.215, 0.075), (0.07, 0.035, 0.07), seg=8, rings=5, material=ORANGE, rot=(0, 0, 32)))
B.append(ell(V(0.17, -0.236, 0.075), (0.03, 0.03, 0.03), seg=6, rings=4, material=WHITE, rot=(0, 0, 32)))
for k in range(2):
    B.append(ell(V(-0.165, -0.21 - 0.01 * k, 0.1 - 0.05 * k), (0.075, 0.035, 0.016), seg=6, rings=3, material=ORANGE, rot=(0, 0, -30)))

# legs (floating: left leg straighter, right leg bent back a little)
for sx, bend in ((1, 0.02), (-1, 0.12)):
    hip = V(sx * 0.14, 0.0, -0.3)
    knee = V(sx * 0.16, bend * 0.4, -0.52)
    ank = V(sx * 0.17, bend, -0.68)
    B.append(tube([hip, knee, ank], [0.135, 0.125, 0.115], seg=8, material=WHITE, cap=False))
    B.append(band(knee, ank - hip, 0.125, 0.08, seg=8, material=ORANGE))   # knee band
    # boot: chunky with a grey sole
    bc = ank + V(0, -0.04, -0.06)
    B.append(ell(bc, (0.125, 0.17, 0.1), seg=8, rings=6, p=0.8, material=WHITE, rot=(-bend * 60, 0, 0)))
    B.append(ell(bc + V(0, 0.0, -0.075), (0.13, 0.178, 0.04), seg=8, rings=4, p=0.7, material=GREY, rot=(-bend * 60, 0, 0)))
    B.append(band(ank + V(0, 0, 0.02), ank - knee, 0.118, 0.06, seg=8, material=ORANGE))     # boot cuff

# backpack (life support) with tanks and vents
BP = V(0, 0.33, -0.05)
B.append(ell(BP, (0.27, 0.12, 0.3), seg=8, rings=6, p=0.55, material=WHITE))
for sx in (-1, 1):
    B.append(lathe([(0.0, -0.22), (0.07, -0.2), (0.075, 0.18), (0.0, 0.23)], seg=8, material=GREY,
                   M=Matrix.Translation(BP + V(sx * 0.14, 0.11, 0))))
    B.append(lathe([(0.077, 0.08), (0.077, 0.13)], seg=8, material=ORANGE, caps=(False, False),
                   M=Matrix.Translation(BP + V(sx * 0.14, 0.11, 0))))
for k in range(2):
    B.append(ell(BP + V(0, 0.1, 0.16 - k * 0.07), (0.06, 0.03, 0.012), seg=6, rings=3, material=GREY))
B.append(ell(BP + V(0, 0.115, -0.15), (0.03, 0.02, 0.03), seg=6, rings=4, material=GLOW))
# hose from backpack into the chest box side
B.append(tube(bezier(BP + V(-0.27, -0.02, -0.05), V(-0.4, 0.05, -0.15), V(-0.22, -0.26, -0.09), n=5), 0.025, seg=4, material=GREY))

body = part(B, 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- head: helmet + gold visor, pivot at the neck
NECK = V(0, 0, 0.19)
HC = V(0, 0, 0.5)
R = 0.36
H = []
H.append(lathe([(0.21, 0.13), (0.235, 0.17), (0.2, 0.235)], seg=14, material=GREY))   # neck ring
H.append(ell(HC, (R, R * 0.97, R), seg=14, rings=9, material=WHITE))
VR = (R, R * 0.97, R)
G = Matrix.Rotation(math.radians(-6), 3, 'X')
vis = cap(VR, math.radians(58), G, seg=16, rings=5, material=VISOR, outer=1.035, inner=0.99)
xf(vis, Matrix.Translation(HC) @ Matrix.Diagonal((1.0, 1.0, 1.0, 1)))
H.append(vis)
# white rim around the visor
a = math.radians(61)
rim = []
for i in range(17):
    ph = TAU * i / 16
    n = G @ Vector((math.sin(a) * math.cos(ph), -math.cos(a), math.sin(a) * math.sin(ph)))
    rim.append(HC + Vector((n.x * VR[0], n.y * VR[1], n.z * VR[2])) * 1.03)
H.append(tube(rim, 0.032, seg=5, material=WHITE, cap=False))
# visor glints (white)
gl = cap(VR, math.radians(9), G @ Matrix.Rotation(math.radians(-28), 3, 'X') @ Matrix.Rotation(math.radians(-28), 3, 'Z'),
         seg=8, rings=3, material=WHITE, outer=1.045, inner=1.037)
H.append(xf(gl, Matrix.Translation(HC)))
gl2 = cap(VR, math.radians(4), G @ Matrix.Rotation(math.radians(-6), 3, 'X') @ Matrix.Rotation(math.radians(-38), 3, 'Z'),
          seg=6, rings=3, material=WHITE, outer=1.045, inner=1.037)
H.append(xf(gl2, Matrix.Translation(HC)))
# ear pucks + antenna with a glowing tip
for sx in (-1, 1):
    H.append(lathe([(0.1, 0.0), (0.105, 0.04), (0.085, 0.07), (0.0, 0.075)], seg=10, material=GREY, caps=(False, True),
                   M=Matrix.Translation(HC + V(sx * (R - 0.04), 0.02, 0)) @ rotm((0, sx * 90, 0))))
    H.append(lathe([(0.062, 0.073), (0.0, 0.082)], seg=10, material=ORANGE, caps=(False, False),
                   M=Matrix.Translation(HC + V(sx * (R - 0.04), 0.02, 0)) @ rotm((0, sx * 90, 0))))
ant = bezier(HC + V(R + 0.02, 0.04, 0.04), HC + V(R + 0.05, 0.08, 0.2), HC + V(R + 0.03, 0.12, 0.33), n=4)
H.append(tube(ant, [0.016, 0.013, 0.011, 0.01, 0.009], seg=5, material=GREY))
H.append(ell(ant[-1] + V(0, 0, 0.02), (0.035, 0.035, 0.035), seg=6, rings=4, material=GLOW))
# small helmet lamp on top-front-right
H.append(ell(HC + V(-0.25, -0.07, 0.24), (0.05, 0.035, 0.04), seg=6, rings=4, p=0.7, material=GREY, rot=(30, -35, 50)))
H.append(ell(HC + V(-0.27, -0.1, 0.25), (0.03, 0.012, 0.025), seg=6, rings=4, material=GLOW, rot=(30, -35, 50)))
head = part(H, 'head', NECK, angle=60)

# ---------------------------------------------------------------- arms: pivot at the shoulder, hanging out ~35 degrees
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.31, 0.0, 0.08)
    A = []
    A.append(ell(SH, (0.12, 0.12, 0.12), seg=7, rings=5, material=WHITE))
    EL = SH + V(sx * 0.12, -0.03, -0.2)
    WR = EL + V(sx * 0.09, -0.06, -0.17)
    A.append(tube([SH, EL, WR], [0.1, 0.09, 0.085], seg=8, material=WHITE, cap=False))
    A.append(band(SH + (EL - SH) * 0.55, EL - SH, 0.1, 0.07, seg=8, material=ORANGE))   # upper-arm band
    d = (WR - EL).normalized()
    A.append(band(WR, d, 0.092, 0.06, seg=8, material=ORANGE))   # cuff
    GC = WR + d * 0.085
    glove = ell(V(0, 0, 0), (0.088, 0.072, 0.098), seg=8, rings=5, material=GREY)
    xf(glove, Matrix.Translation(GC) @ Vector((0, 0, -1)).rotation_difference(d).to_matrix().to_4x4())
    A.append(glove)
    A.append(ell(GC + V(-sx * 0.05, -0.06, 0.02), (0.035, 0.035, 0.05), seg=6, rings=4, material=GREY, rot=(30, 0, 0)))   # thumb
    part(A, f'arm_{side}', SH, angle=60)

std_view()
print_ext()
if '--close' in sys.argv:
    closeup('astronaut', (0, 0, 0.5), 1.6, d=(0.3, -1, 0.35))
    sys.exit()
notes = ('Cute chunky floating astronaut ~1.7 m tall, origin (0,0,0) = body CENTRE, front -Y, left = +X. Parts/pivots: '
         'body (origin 0,0,0; white suit with orange patches/knee pads/boot cuffs, grey belt and chest box with glowing buttons, '
         'backpack with tanks); head (helmet + gold visor material `visor`, ear pucks, antenna with glow tip; pivot at the neck '
         '%s); arm_l (+X) / arm_r (-X) (pivot at the shoulder %s / %s, arms hang ~35 deg outwards, grey gloves). '
         'Materials: suit_white, suit_orange, suit_grey, visor, glow_suit.' % (fmt(NECK), fmt((0.31, 0, 0.08)), fmt((-0.31, 0, 0.08))))
finish('space', 'astronaut', kind='char', footprint=0.6, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('astronaut', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.4), 'top': (0.2, -0.4, 1)})
    montage('astronaut', keys=('front', 'side', 'back', 'top'))
