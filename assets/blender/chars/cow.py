import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ccp_kit import *

# ---------------------------------------------------------------- materials
WHITE = mat('cow_white', '#fbf7ee', rough=0.65)
BLACK = mat('cow_black', '#2b2523', rough=0.55)
PINK = mat('cow_pink', '#f59fb3', rough=0.6)
HORN = mat('horn', '#f3e2b8', rough=0.5)
GOLD = mat('gold', '#f2bd2c', rough=0.28, metal=1.0)
COLLAR = mat('collar', '#d6352b', rough=0.6)

# ---------------------------------------------------------------- body
TC = V(0, 0.03, 0.9)          # torso centre
TR = (0.40, 0.70, 0.36)


def torso_shape(n):
    # slightly fuller chest, a little dip in the back, rounder belly
    y = n.y
    k = 1.0 + 0.06 * (-y)          # chest (y<0) a bit wider
    z = n.z
    if z > 0:
        z *= 1.0 - 0.07 * math.cos(y * math.pi / 2) ** 2   # back dips a bit in the middle
    else:
        z *= 1.0 + 0.08 * math.cos(y * math.pi / 2) ** 2   # belly hangs a little
    return Vector((n.x * k, y, z))


torso = ell(TC, TR, seg=18, rings=12, p=0.78, material=WHITE, shape=torso_shape)

SPOTS = [  # (centre on/near surface, radius)
    (V(0.38, -0.18, 1.02), 0.24), (V(0.36, 0.38, 0.86), 0.2), (V(0.30, 0.16, 1.18), 0.12),
    (V(-0.38, -0.30, 0.86), 0.2), (V(-0.36, 0.22, 1.05), 0.26), (V(-0.2, 0.5, 1.2), 0.13),
    (V(0.05, 0.05, 1.27), 0.17), (V(0.12, 0.72, 0.98), 0.14),
]


def spot_field(p, spots=SPOTS, wob=0.22):
    best = 1e9
    for c, r in spots:
        best = min(best, (p - c).length / r - 1.0)
    return best + noise.noise(p * 5.0) * wob


iso_paint(torso, spot_field, BLACK)

body_parts = [torso]
# udder + teats
body_parts.append(ell((0, 0.34, 0.57), (0.17, 0.15, 0.12), seg=9, rings=6, material=PINK))
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * 0.07, 0.34 + sy * 0.065
        body_parts.append(tube([(x, y, 0.52), (x * 1.08, y, 0.45)], [0.028, 0.022], seg=6, material=PINK, round_end=True))
# collar + bell
collar_c = V(0, -0.6, 1.06)
col = torus(R=0.215, r=0.04, loc=(0, 0, 0), seg=14, ring=4, material=COLLAR)
col.data.transform(Matrix.Rotation(math.radians(62), 4, 'X')); col.data.transform(Matrix.Translation(collar_c)); col.location = (0, 0, 0)
col.data.update()
body_parts.append(col)
bell_top = V(0, -0.72, 0.9)
bell = lathe([(0.0, -0.13), (0.085, -0.13), (0.09, -0.115), (0.072, -0.09), (0.058, -0.04), (0.052, 0.0), (0.035, 0.03), (0.0, 0.04)],
             seg=10, material=GOLD, M=Matrix.Translation(bell_top) @ Matrix.Rotation(math.radians(-12), 4, 'X'))
body_parts.append(bell)
body_parts.append(torus(R=0.025, r=0.009, loc=tuple(bell_top + V(0, 0.0, 0.05)), rot=(0, math.radians(90), 0), seg=6, ring=3, material=GOLD))
body_parts.append(ell(bell_top + V(0, -0.03, -0.145), (0.025, 0.025, 0.025), seg=6, rings=4, material=BLACK))
DROP = Matrix.Translation((0, 0, -0.06))  # lower the whole cow a bit (shorter, chunkier legs)
for o in body_parts:
    xf(o, DROP)
body = part(body_parts, 'body', (0, 0, 0))

# ---------------------------------------------------------------- head (pivot = neck)
NECK = V(0, -0.58, 1.12)
HC = V(0, -0.9, 1.3)
head_parts = []
neck = tube([NECK + V(0, 0.1, -0.06), NECK, HC + V(0, 0.1, -0.08)], [0.19, 0.2, 0.2], seg=10, material=WHITE)
head_parts.append(neck)
skull = ell(HC, (0.26, 0.26, 0.25), seg=13, rings=10, p=0.85, material=WHITE,
            shape=lambda n: Vector((n.x * (1 + 0.08 * n.z), n.y, n.z)))
# spot over the left eye (cow's left = +X) running over the top
iso_paint(skull, lambda p: spot_field(p, [(V(0.16, -1.08, 1.43), 0.15), (V(0.2, -0.9, 1.52), 0.12)], 0.15), BLACK)
head_parts.append(skull)
MZ = V(0, -1.11, 1.15)
muzzle = ell(MZ, (0.24, 0.17, 0.155), seg=12, rings=7, p=0.82, material=PINK)
head_parts.append(muzzle)
for sx in (-1, 1):  # nostrils
    head_parts.append(ell(MZ + V(sx * 0.085, -0.165, 0.035), (0.03, 0.02, 0.022), seg=6, rings=4, material=BLACK,
                          rot=(0, 0, sx * -20)))
# little smile
smile = tube(bezier(MZ + V(-0.08, -0.155, -0.06), MZ + V(0, -0.2, -0.115), MZ + V(0.08, -0.155, -0.06), n=4), 0.011, seg=4,
             material=BLACK, round_end=True)
head_parts.append(smile)
# eyes
for sx in (-1, 1):
    ec = V(sx * 0.115, -1.105, 1.37)
    d = V(sx * 0.42, -1, 0.12)
    head_parts += eye(ec, d, r=0.072, white=WHITE, black=BLACK, look=(-sx * 0.15, 0, 0.05), tall=1.2, seg=10)
    # lashes
    for k, a in enumerate((-0.6, 0.0, 0.6)):
        base = ec + V(sx * (0.035 + 0.035 * a), -0.03, 0.082 - 0.018 * abs(a))
        tip = base + V(sx * (0.02 + 0.03 * a), -0.025, 0.04)
        head_parts.append(tube([base, tip], [0.009, 0.003], seg=4, material=BLACK))
    # ears (white outside, pink inside)
    ear = ell((0, 0, 0), (0.15, 0.04, 0.075), seg=8, rings=6, material=WHITE)
    iso_paint(ear, lambda p: p.y + 0.018, PINK)
    xf(ear, Matrix.Translation(V(sx * 0.105, 0, 0)))
    xf(ear, Matrix.Translation(HC + V(sx * 0.21, 0.04, 0.08)) @ Matrix.Rotation(math.radians(sx * -25), 4, 'Y') @ Matrix.Rotation(math.radians(sx * 15), 4, 'Z'))
    head_parts.append(ear)
    # horns
    hb = HC + V(sx * 0.13, 0.04, 0.2)
    pts = bezier(hb, hb + V(sx * 0.1, 0, 0.06), hb + V(sx * 0.15, -0.01, 0.17), hb + V(sx * 0.12, -0.03, 0.25), n=5)
    head_parts.append(tube(pts, [0.055, 0.05, 0.042, 0.032, 0.02, 0.006], seg=7, material=HORN))
# hair tuft between the horns
for (x, y, z, s) in ((0, -0.05, 0.245, 0.07), (-0.06, 0.0, 0.225, 0.06), (0.06, 0.0, 0.225, 0.06)):
    head_parts.append(ell(HC + V(x, y, z), (s, s * 0.9, s * 0.8), seg=7, rings=4, material=WHITE))
HEADSCALE = Matrix.Translation(HC + V(0, -0.03, 0.02)) @ Matrix.Scale(1.16, 4) @ Matrix.Translation(-HC)
for o in head_parts[1:]:
    xf(o, HEADSCALE)
for o in head_parts:
    xf(o, DROP)
NECK = NECK + V(0, 0, -0.06)
head = part(head_parts, 'head', NECK)

# ---------------------------------------------------------------- legs (pivot = hip/shoulder)
HIP_Z = 0.68
LEGS = {'leg_fl': (0.235, -0.4), 'leg_fr': (-0.235, -0.4), 'leg_bl': (0.235, 0.42), 'leg_br': (-0.235, 0.42)}
for name, (x, y) in LEGS.items():
    lp = []
    leg = tube([(x, y, HIP_Z + 0.05), (x, y, 0.42), (x, y - 0.005, 0.13)], [0.13, 0.115, 0.105], seg=10, material=WHITE)
    if name == 'leg_fl':   # spots on two legs
        iso_paint(leg, lambda p: (0.36 - p.z) * 4 + noise.noise(p * 9) * 0.3, BLACK)
    if name == 'leg_br':
        iso_paint(leg, lambda p, c=V(x - 0.11, y + 0.02, 0.3): (p - c).length / 0.11 - 1 + noise.noise(p * 9) * 0.2, BLACK)
    lp.append(leg)
    # hoof: chunky dark cylinder with a rounded top and a tiny cleft
    hoof = lathe([(0.0, 0.0), (0.118, 0.0), (0.122, 0.025), (0.112, 0.12), (0.0, 0.15)], seg=10, material=BLACK,
                 M=Matrix.Translation((x, y - 0.005, 0)))
    lp.append(hoof)
    part(lp, name, (x, y, HIP_Z))

# ---------------------------------------------------------------- tail (pivot = tail root)
TROOT = V(0, 0.69, 1.14)
tp = bezier(TROOT + V(0, -0.04, 0.0), TROOT + V(0, 0.15, 0.03), TROOT + V(0, 0.17, -0.25), TROOT + V(0, 0.15, -0.5), n=6)
tail_parts = [tube(tp, [0.035 - 0.002 * i for i in range(7)], seg=6, material=WHITE)]
tc = TROOT + V(0, 0.15, -0.55)
tail_parts.append(ell(tc + V(0, 0, -0.02), (0.065, 0.065, 0.12), seg=8, rings=6, material=BLACK,
                      shape=lambda n: Vector((n.x * (1 - 0.35 * max(0, n.z)), n.y * (1 - 0.35 * max(0, n.z)), n.z + 0.15 * noise.noise(n * 3)))))
for o in tail_parts:
    xf(o, DROP)
TROOT = TROOT + V(0, 0, -0.06)
part(tail_parts, 'tail', TROOT)

report()
notes = ('Parts/pivots (Blender coords, front -Y): body (origin 0,0,0; torso, spots, udder, collar+golden bell); '
         f'head (pivot neck {tuple(NECK)}); leg_fl ({LEGS["leg_fl"][0]},{LEGS["leg_fl"][1]},{HIP_Z}), leg_fr ({LEGS["leg_fr"][0]},{LEGS["leg_fr"][1]},{HIP_Z}), '
         f'leg_bl ({LEGS["leg_bl"][0]},{LEGS["leg_bl"][1]},{HIP_Z}), leg_br ({LEGS["leg_br"][0]},{LEGS["leg_br"][1]},{HIP_Z}) - hip/shoulder, hooves at z=0; '
         f'tail (pivot root {tuple(TROOT)}, hangs down). Left = +X. Materials: cow_white, cow_black, cow_pink, horn, gold, collar.')
finish('chars', 'cow', kind='char', footprint=0.6, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['head'].rotation_euler = (0.35, 0, 0.3)
        bpy.data.objects['leg_fl'].rotation_euler = (0.5, 0, 0)
        bpy.data.objects['leg_br'].rotation_euler = (0.5, 0, 0)
        bpy.data.objects['leg_fr'].rotation_euler = (-0.5, 0, 0)
        bpy.data.objects['leg_bl'].rotation_euler = (-0.5, 0, 0)
        bpy.data.objects['tail'].rotation_euler = (0, 0.6, 0)
    views('cow', pose)
