import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *
from gkit import _obj

# ---------------------------------------------------------------- materials (6)
SKIN = mat('skin', '#ffb487', rough=0.6)
TABARD = mat('tabard', '#2f6fd6', rough=0.7)              # recoloured by the game
STEEL = mat('steel', '#b9c3cf', rough=0.3, metal=0.8)
BROWN = mat('brown', '#5a3522', rough=0.6)                 # boots, belt, gloves, shaft, moustache, pupils, brows
WHITE = mat('white', '#fbf8f0', rough=0.4)                 # eye whites, highlights, tabard trim + emblem
GLOW = mat('glow_lantern', '#ffd36a', rough=0.4, emit='#ffb53a', emit_strength=2.5)

B = []
# ---------------------------------------------------------------- torso: chubby barrel of chainmail with a tabard
TC = V(0, 0.0, 1.06)
torso = ell(TC, (0.3, 0.24, 0.34), seg=12, rings=8, material=STEEL,
            shape=lambda n: Vector((n.x * (1 + 0.06 * (-n.z)), n.y * (1 + 0.08 * max(0, -n.z)), n.z)))
B.append(torso)
B.append(ell(V(0, 0.0, 0.79), (0.255, 0.21, 0.13), seg=10, rings=5, material=STEEL))   # hips


def panel(front=True):
    bm = bmesh.new()
    zs = [1.34, 1.22, 1.06, 0.9, 0.74, 0.6, 0.53]
    na = 7
    grid = []
    for z in zs:
        t = (z - TC.z) / 0.34
        s = math.sqrt(max(0.0, 1 - min(abs(t), 1) ** 2)) if z > TC.z else 1.0
        s = max(s, 0.55)
        half = math.radians(48)
        row = []
        for i in range(na):
            a = -half + 2 * half * i / (na - 1)
            rx = 0.3 * s * (1.0 + 0.06 * max(0, -t)) + 0.015 + max(0, 0.8 - z) * 0.12
            ry = 0.24 * s * (1.0 + 0.08 * max(0, -t)) + 0.02 + max(0, 0.8 - z) * 0.18
            sgn = -1 if front else 1
            row.append(bm.verts.new((rx * math.sin(a), sgn * ry * math.cos(a), z)))
        grid.append(row)
    for r in range(len(zs) - 1):
        for i in range(na - 1):
            f = (grid[r][i], grid[r][i + 1], grid[r + 1][i + 1], grid[r + 1][i])
            ff = bm.faces.new(f if front else tuple(reversed(f)))
            ff.material_index = 1 if r == len(zs) - 2 else 0
    bm.normal_update()
    o = _obj(bm, TABARD)
    o.data.materials.append(WHITE)
    return o


B += [panel(True), panel(False)]
# white tower emblem on the chest
EM = V(0, -0.27, 1.05)
tower = [(-0.06, -0.08), (0.06, -0.08), (0.06, 0.04), (0.075, 0.04), (0.075, 0.09), (0.045, 0.09), (0.045, 0.065),
         (0.015, 0.065), (0.015, 0.09), (-0.015, 0.09), (-0.015, 0.065), (-0.045, 0.065), (-0.045, 0.09), (-0.075, 0.09),
         (-0.075, 0.04), (-0.06, 0.04)]
B.append(flat_shape(list(reversed(tower)), 0.02, WHITE, M=Matrix.Translation(EM) @ rotm((-8, 0, 0))))
# belt + buckle
B.append(lathe([(0.29, 0.86), (0.3, 0.88), (0.3, 0.92), (0.29, 0.94)], seg=12, material=BROWN,
               M=Matrix.Diagonal((1.0, 0.86, 1, 1))))
B.append(xf(lathe([(0.05, -0.012), (0.055, 0.0), (0.05, 0.012), (0.035, 0.0)], seg=6, material=STEEL),
            Matrix.Translation((0, -0.265, 0.9)) @ rotm((90, 0, 0))))
# shoulder pads (steel)
for sx in (-1, 1):
    B.append(ell(V(sx * 0.29, 0.0, 1.27), (0.12, 0.13, 0.09), seg=8, rings=5, material=STEEL, rot=(0, sx * 30, 0)))
# collar
B.append(lathe([(0.17, 1.33), (0.15, 1.38), (0.12, 1.4)], seg=10, material=STEEL))

# ---------------------------------------------------------------- head: big round friendly face
HC = V(0, -0.02, 1.53)
head = ell(HC, (0.22, 0.21, 0.22), seg=13, rings=9, material=SKIN)
B.append(head)
for sx in (-1, 1):
    B.append(ell(HC + V(sx * 0.215, 0.02, 0.0), (0.04, 0.03, 0.06), seg=6, rings=4, material=SKIN))   # ears
    B += eye(HC + V(sx * 0.078, -0.185, 0.045), V(sx * 0.3, -1, 0.05), r=0.05, white=WHITE, black=BROWN, depth=0.55,
             tall=1.25, pupil=0.62, look=(-sx * 0.1, 0, 0.05), seg=8, pseg=7)
    # friendly raised brows
    b0, b1 = HC + V(sx * 0.03, -0.205, 0.12), HC + V(sx * 0.13, -0.17, 0.125)
    B.append(tube([b0, (b0 + b1) / 2 + V(0, -0.01, 0.018), b1], [0.012, 0.016, 0.011], seg=5, material=BROWN, round_end=True))
    # rosy cheeks (skin tone bump)
    B.append(ell(HC + V(sx * 0.12, -0.17, -0.04), (0.045, 0.03, 0.035), seg=6, rings=4, material=SKIN))
# big nose
B.append(ell(HC + V(0, -0.225, -0.02), (0.055, 0.05, 0.05), seg=8, rings=6, material=SKIN))
# friendly curled moustache
for sx in (-1, 1):
    pts = bezier(HC + V(sx * 0.01, -0.235, -0.07), HC + V(sx * 0.1, -0.24, -0.1), HC + V(sx * 0.17, -0.2, -0.06),
                 HC + V(sx * 0.19, -0.17, -0.0), n=5)
    B.append(tube(pts, [0.034, 0.04, 0.036, 0.028, 0.02, 0.012], seg=5, material=BROWN, round_end=True))
# smile below the moustache + chin
sm = [HC + V(math.sin(a) * 0.07, -0.2 + 0.03 * abs(math.sin(a)), -0.14 + 0.03 * (a / 0.9) ** 2) for a in
      [(-1 + 2 * i / 4) * 0.9 for i in range(5)]]
B.append(tube(sm, 0.01, seg=4, material=BROWN, round_end=True))
# kettle hat: dome + wide sloping brim + rim + top knob
HAT = HC + V(0, 0.02, 0.12)
HM = Matrix.Translation(HAT) @ rotm((-12, 0, 0))
B.append(lathe([(0.3, -0.02), (0.325, 0.0), (0.31, 0.015), (0.24, 0.05), (0.215, 0.07), (0.215, 0.13), (0.2, 0.22),
                (0.15, 0.29), (0.07, 0.325), (0.0, 0.33)], seg=14, material=STEEL, M=HM))
B.append(lathe([(0.222, 0.08), (0.228, 0.095), (0.222, 0.11)], seg=14, material=BROWN, M=HM))   # leather band
B.append(xf(ell(V(0, 0, 0.34), (0.035, 0.035, 0.03), seg=6, rings=4, material=STEEL), HM))
body = apart(B, 'body', (0, 0, 0))

# ---------------------------------------------------------------- legs (pivot at the hip, boots on z=0)
LEG = {}
for side, sx in (('l', 1), ('r', -1)):
    HP = V(sx * 0.12, 0.0, 0.76)
    kn, an = V(sx * 0.13, -0.02, 0.4), V(sx * 0.13, 0.0, 0.13)
    L = [tube([HP, kn], [0.105, 0.085], seg=7, material=TABARD),
         ell(kn, (0.085, 0.085, 0.08), seg=6, rings=4, material=STEEL),                  # knee cop
         tube([kn, an], [0.08, 0.075], seg=7, material=STEEL)]                           # greave
    # chunky boot
    L.append(ell(an + V(0, -0.06, -0.045), (0.1, 0.16, 0.09), seg=8, rings=5, material=BROWN,
                 shape=lambda n: Vector((n.x, n.y, max(n.z, -0.95)))))
    L.append(lathe([(0.085, 0.12), (0.095, 0.15), (0.09, 0.2)], seg=8, material=BROWN, M=Matrix.Translation((an.x, 0.0, 0))))
    o = apart(L, f'leg_{side}', HP)
    LEG[side] = HP
# put the boot soles exactly on z=0
lo = min((o.matrix_world @ v.co).z for o in bpy.context.scene.objects if o.name.startswith('leg_') for v in o.data.vertices)
for k in ('l', 'r'):
    o = bpy.data.objects[f'leg_{k}']
    o.data.transform(Matrix.Translation((0, 0, -lo)))

# ---------------------------------------------------------------- right arm with the halberd (pivot at the shoulder)
SR = V(-0.32, 0.0, 1.25)
ER, HR = V(-0.4, -0.04, 1.05), V(-0.38, -0.2, 0.95)
A = [tube([SR, ER], [0.085, 0.075], seg=7, material=TABARD), ell(ER, (0.075, 0.075, 0.075), seg=6, rings=4, material=TABARD),
     tube([ER, HR + V(0, 0.06, 0.02)], [0.072, 0.065], seg=7, material=TABARD),
     tube([HR + V(0, 0.09, 0.02), HR + V(0, 0.04, 0.01)], [0.06, 0.075], seg=7, material=WHITE),       # cuff
     ell(HR, (0.075, 0.07, 0.075), seg=7, rings=4, material=BROWN)]                                   # glove fist
# halberd: tall shaft, spear point, axe blade facing front (-Y), back spike
SX, SY = HR.x, HR.y
A.append(cyl_between(V(SX, SY, 0.06), V(SX, SY, 2.18), 0.028, seg=7, material=BROWN))
A.append(cone(0.035, 0.06, loc=(SX, SY, 0.05), verts=7, material=STEEL, rot=(math.pi, 0, 0)))          # butt cap
blade = [(0.0, 0.0), (-0.02, -0.05), (-0.16, -0.12), (-0.24, -0.02), (-0.26, 0.09), (-0.24, 0.2), (-0.16, 0.27),
         (-0.06, 0.2), (0.0, 0.22)]
bl = flat_shape([(y, z) for (y, z) in blade], 0.022, STEEL, bevel=0.0)
# outline is in (x,z): map local x -> world y (front), so rotate 90 deg about Z
xf(bl, Matrix.Translation((SX, SY - 0.02, 1.88)) @ rotm((0, 0, 90)))
A.append(bl)
spk = [(0.0, 0.0), (0.18, 0.03), (0.0, 0.08)]
sp = flat_shape(spk, 0.02, STEEL)
xf(sp, Matrix.Translation((SX, SY + 0.02, 1.94)) @ rotm((0, 0, 90)))
A.append(sp)
A.append(spike(V(SX, SY, 2.14), (0, 0, 1), r=0.04, h=0.28, seg=6, material=STEEL))                   # spear point
A.append(xf(lathe([(0.04, -0.03), (0.045, 0.0), (0.04, 0.03)], seg=8, material=STEEL), Matrix.Translation((SX, SY, 2.13))))
A.append(xf(lathe([(0.036, -0.12), (0.04, 0.0), (0.036, 0.12)], seg=8, material=STEEL), Matrix.Translation((SX, SY, 1.96))))
# tassel in tabard colour under the blade
A.append(tube([V(SX, SY, 1.83), V(SX, SY - 0.01, 1.72)], [0.04, 0.06], seg=6, material=TABARD, round_end=True))
apart(A, 'arm_r', SR)

# ---------------------------------------------------------------- left arm with the lantern (pivot at the shoulder)
SL = V(0.32, 0.0, 1.25)
EL, HL = V(0.42, -0.06, 1.06), V(0.4, -0.24, 1.02)
A = [tube([SL, EL], [0.085, 0.075], seg=7, material=TABARD), ell(EL, (0.075, 0.075, 0.075), seg=6, rings=4, material=TABARD),
     tube([EL, HL + V(0, 0.06, 0.0)], [0.072, 0.065], seg=7, material=TABARD),
     tube([HL + V(0, 0.09, 0.0), HL + V(0, 0.04, 0.0)], [0.06, 0.075], seg=7, material=WHITE),
     ell(HL, (0.075, 0.07, 0.075), seg=7, rings=4, material=BROWN)]
# lantern hanging from the fist
LC = HL + V(0, -0.02, -0.25)
ring = xf(lathe([(0.04, -0.008), (0.048, 0.0), (0.04, 0.008), (0.032, 0.0)], seg=8, material=STEEL),
          Matrix.Translation(HL + V(0, -0.02, -0.05)) @ rotm((0, 90, 0)))
A.append(ring)
A.append(lathe([(0.0, 0.17), (0.04, 0.165), (0.1, 0.12), (0.105, 0.1)], seg=8, material=STEEL, M=Matrix.Translation(LC)))   # roof
A.append(lathe([(0.085, -0.13), (0.1, -0.12), (0.1, -0.09), (0.0, -0.09)], seg=8, material=STEEL, M=Matrix.Translation(LC)))  # base
A.append(lathe([(0.07, -0.09), (0.085, -0.04), (0.085, 0.05), (0.07, 0.1)], seg=8, material=GLOW, M=Matrix.Translation(LC)))  # glass
for k in range(4):   # cage bars
    a = TAU * (k + 0.5) / 4
    p = V(math.cos(a) * 0.088, math.sin(a) * 0.088, 0)
    A.append(cyl_between(LC + p + V(0, 0, -0.1), LC + p + V(0, 0, 0.11), 0.012, seg=4, material=STEEL))
A.append(cyl_between(LC + V(0, 0, 0.16), HL + V(0, -0.02, -0.05), 0.01, seg=4, material=STEEL))
apart(A, 'arm_l', SL)

KS = 0.96
scale_all(KS)
SR, SL, LC = SR * KS, SL * KS, LC * KS
SX, SY = SX * KS, SY * KS
LEG = {k: v * KS for k, v in LEG.items()}
lo = min((o.matrix_world @ v.co).z for o in bpy.context.scene.objects if o.name.startswith('leg_') for v in o.data.vertices)
for k in ('l', 'r'):
    bpy.data.objects[f'leg_{k}'].data.transform(Matrix.Translation((0, 0, -lo)))
report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('De wachter. Parts/pivots (Blender coords, front -Y, left=+X; ~1.9 m incl. kettle hat): '
         'body (origin 0,0,0; chainmail barrel torso, tabard front+back panels in material "tabard" with white hem + tower emblem, '
         'belt, big friendly face with moustache, kettle hat); '
         f'leg_l (pivot hip {fmt(LEG["l"])}), leg_r (pivot hip {fmt(LEG["r"])}) boots on z=0; '
         f'arm_r (pivot shoulder {fmt(SR)}; holds a tall halberd, shaft at x={SX:.2f} y={SY:.2f}, z 0.06-2.33); '
         f'arm_l (pivot shoulder {fmt(SL)}; holds a small lantern, glass = material glow_lantern, centre {fmt(LC)}). '
         'Materials: skin, tabard, steel, brown, white, glow_lantern.')
finish('chars', 'guard', kind='char', footprint=0.4, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['arm_r'].rotation_euler = (0.4, 0, 0)
        bpy.data.objects['arm_l'].rotation_euler = (-0.4, 0, 0)
        bpy.data.objects['leg_l'].rotation_euler = (0.4, 0, 0)
        bpy.data.objects['leg_r'].rotation_euler = (-0.4, 0, 0)
    views2('guard', dirs={'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (0.7, 1, 0.5), 'face': (0.3, -1, 0.1)}, dist=1.2)
    views2('guard_face', dirs={'f': (0.2, -1, 0.1)}, focus=((0, -0.1, 1.55), 0.8), dist=1.2)
    views2('guard_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose)
