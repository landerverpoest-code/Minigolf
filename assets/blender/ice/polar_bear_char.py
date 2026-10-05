import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow')
from _lifekit import *

# ---------------------------------------------------------------- materials (5)
CREAM = mat('bear_cream', '#f8f2e4', rough=0.75)
SHADE = mat('bear_shade', '#e4d9c3', rough=0.8)
BLACK = mat('bear_black', '#24262c', rough=0.45)
EYEW = mat('eye_white', '#ffffff', rough=0.3)
PINK = mat('bear_pink', '#f2a0b4', rough=0.6)

# ---------------------------------------------------------------- body
TC = Vector((0, 0.1, 0.63))


def torso_shape(n):
    y = n.y
    k = 1.0 + 0.08 * max(-y, 0)                       # broader shoulders
    z = n.z
    if z > 0:
        z *= 1.0 + 0.08 * max(-y, 0) - 0.05 * max(y, 0)   # shoulder hump, lower rump
    else:
        z *= 1.0 + 0.06 * math.cos(y * math.pi / 2) ** 2  # round belly
    return Vector((n.x * k, y, z))


torso = ell(TC, (0.37, 0.6, 0.34), seg=18, rings=12, p=0.82, material=CREAM, shape=torso_shape)
iso_paint(torso, lambda p: (p.z - 0.42) * 5 + noise.noise(p * 4) * 0.25, SHADE)
tail = ell(Vector((0, 0.71, 0.76)), (0.08, 0.07, 0.075), seg=8, rings=6, material=CREAM)
body = part([torso, tail], 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- head (pivot at the neck)
NECK = Vector((0, -0.4, 0.8))
HC = Vector((0, -0.66, 0.84))
hp = []
hp.append(tube([NECK + Vector((0, 0.06, -0.04)), NECK, HC + Vector((0, 0.08, -0.03))], [0.25, 0.25, 0.22], seg=9, material=CREAM, cap=False))
skull = ell(HC, (0.25, 0.24, 0.23), seg=14, rings=9, p=0.9, material=CREAM,
            shape=lambda n: Vector((n.x * (1 + 0.1 * max(-n.z, 0)), n.y, n.z)))   # chubby cheeks
hp.append(skull)
MZ = HC + Vector((0, -0.2, -0.065))
muzzle = ell(MZ, (0.13, 0.12, 0.1), seg=10, rings=7, material=SHADE)
hp.append(muzzle)
# black nose
hp.append(ell(MZ + Vector((0, -0.105, 0.045)), (0.058, 0.04, 0.038), seg=10, rings=6, material=BLACK,
              shape=lambda n: Vector((n.x * (1 + 0.25 * max(n.z, 0)), n.y, n.z))))
# smile: little "w" mouth under the nose
mpts = [MZ + Vector((x, -0.105 + 0.03 * abs(x) / 0.06, z)) for x, z in ((-0.06, -0.015), (-0.03, -0.04), (0.0, -0.022), (0.03, -0.04), (0.06, -0.015))]
hp.append(tube(mpts, 0.008, seg=4, material=BLACK, round_end=True))
hp.append(tube([MZ + Vector((0, -0.11, 0.01)), MZ + Vector((0, -0.112, -0.022))], 0.007, seg=4, material=BLACK, round_end=True))
for sx in (-1, 1):
    # big eyes
    ec = HC + Vector((sx * 0.1, -0.205, 0.06))
    hp += eye(ec, Vector((sx * 0.4, -1, 0.15)), r=0.055, white=EYEW, black=BLACK, look=(-sx * 0.15, 0, 0.05), tall=1.2,
              pupil=0.62, seg=9, pseg=8)
    # small round ears with pink inside
    ea = HC + Vector((sx * 0.17, 0.02, 0.19))
    ear = ell(ea, (0.075, 0.04, 0.07), seg=8, rings=6, material=CREAM, rot=(0, sx * -30, 0))
    iso_paint(ear, lambda p, c=ea: (p - (c + Vector((0, -0.05, 0.005)))).length / 0.05 - 1, PINK)
    hp.append(ear)
    # rosy cheeks
    hp.append(ell(HC + Vector((sx * 0.165, -0.175, -0.05)), (0.04, 0.015, 0.025), seg=6, rings=4, material=PINK,
                  rot=(0, 0, sx * 35)))
head = part(hp, 'head', NECK, angle=60)

# ---------------------------------------------------------------- legs (pivot at the hip/shoulder, paws at z=0)
HIP_Z = 0.55
LEGS = {'leg_fl': (0.21, -0.3), 'leg_fr': (-0.21, -0.3), 'leg_bl': (0.21, 0.45), 'leg_br': (-0.21, 0.45)}
for name, (x, y) in LEGS.items():
    lp = []
    front = y < 0
    r0 = 0.15 if front else 0.165
    lp.append(tube([(x, y + (0 if front else 0.02), HIP_Z + 0.08), (x * 1.02, y, 0.32), (x * 1.04, y - 0.01, 0.1)],
                   [r0, r0 * 0.88, r0 * 0.85], seg=10, material=CREAM, cap=False))
    lp.append(ell(Vector((x, y + (0 if front else 0.02), HIP_Z + 0.06)), (r0 * 1.04, r0 * 1.1, r0 * 1.25), seg=10, rings=5, material=CREAM))
    # big round paw with a flat sole
    pc = Vector((x * 1.04, y - 0.04, 0.0))
    paw = ell(pc + Vector((0, 0, 0.08)), (0.15, 0.18, 0.09), seg=10, rings=5, material=CREAM,
              shape=lambda n: Vector((n.x, n.y, max(n.z, -0.85))))
    lp.append(paw)
    # three toe bumps + sole pad (seen when the leg swings)
    for k, tx in enumerate((-0.07, 0.0, 0.07)):
        lp.append(ell(pc + Vector((tx, -0.155, 0.055)), (0.045, 0.042, 0.042), seg=6, rings=3, material=CREAM))
    lp.append(ell(pc + Vector((0, 0.0, 0.006)), (0.09, 0.1, 0.012), seg=8, rings=3, material=BLACK))
    part(lp, name, (x, y, HIP_Z), angle=60)

clamp_ground()
report(); print_ext()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Parts/pivots (Blender coords, front -Y, left = +X): body (origin 0,0,0; creamy white chunky torso, shaded belly, tail); '
         f'head (pivot neck {tuple(round(v, 3) for v in NECK)}; black nose, smile, small round ears, big eyes, cheeks); '
         + ', '.join(f'{k} ({x},{y},{HIP_Z})' for k, (x, y) in LEGS.items()) + ' - pivot at the shoulder/hip, paws at z=0.')
std_view()
finish('ice', 'polar_bear_char', kind='char', footprint=0.8, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['head'].rotation_euler = (0.3, 0, 0.3)
        bpy.data.objects['leg_fl'].rotation_euler = (0.45, 0, 0)
        bpy.data.objects['leg_br'].rotation_euler = (0.45, 0, 0)
        bpy.data.objects['leg_fr'].rotation_euler = (-0.45, 0, 0)
        bpy.data.objects['leg_bl'].rotation_euler = (-0.45, 0, 0)
    closeup('bear_face', (0, -0.75, 0.85), 1.6, d=(0.3, -1, 0.15))
    views('bear', pose)
    montage_files([f'{SCRATCH}/bear_{k}.png' for k in ('face', 'front', 'side', 'back', 'pose')], f'{SCRATCH}/bear_views.png')
