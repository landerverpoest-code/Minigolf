import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *
from gkit import _obj

# ---------------------------------------------------------------- materials (6)
SKIN = mat('skin', '#ffb487', rough=0.6)
WHITE = mat('white', '#fbf8f0', rough=0.5)       # shirt stripes, eye whites, highlights, teeth
BLUE = mat('stripe_blue', '#1f5fc8', rough=0.6)  # shirt stripes, trouser cuffs
NAVY = mat('navy', '#28304a', rough=0.6)         # trousers, boots, belt, pupils, brows, mouth
STRAW = mat('straw', '#f2cf6b', rough=0.8)
RED = mat('red', '#e0383e', rough=0.6)           # neckerchief, hat band, tongue


def striped_lathe(profile, seg, mats, period, M=None, z0=0.0):
    """Lathe with extra rings at stripe borders; band k gets mats[k % 2]."""
    zs = sorted(set([p[1] for p in profile] + [z0 + k * period / 2 for k in range(-40, 80)
                                               if profile[0][1] < z0 + k * period / 2 < profile[-1][1]]))

    def r_at(z):
        for (r0, a), (r1, b) in zip(profile, profile[1:]):
            if a <= z <= b:
                t = (z - a) / (b - a) if b > a else 0
                return r0 + (r1 - r0) * t
        return profile[-1][0]
    bm = bmesh.new()
    rings = []
    for z in zs:
        r = r_at(z)
        if r < 1e-6:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(TAU * i / seg), r * math.sin(TAU * i / seg), z)) for i in range(seg)])
    for j, (a, b) in enumerate(zip(rings, rings[1:])):
        zm = (zs[j] + zs[j + 1]) / 2
        mi = int(math.floor((zm - z0) / (period / 2))) % 2
        if len(a) == 1:
            fs = [bm.faces.new((a[0], b[(i + 1) % seg], b[i])) for i in range(seg)]
        elif len(b) == 1:
            fs = [bm.faces.new((a[i], a[(i + 1) % seg], b[0])) for i in range(seg)]
        else:
            fs = [bm.faces.new((a[i], a[(i + 1) % seg], b[(i + 1) % seg], b[i])) for i in range(seg)]
        for f in fs:
            f.material_index = mi
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj(bm, mats[0])
    o.data.materials.append(mats[1])
    if M is not None:
        xf(o, M)
    return o


def striped_tube(a, b, ra, rb, seg, period, mats):
    """Striped sleeve from a to b (stripes across the tube)."""
    L = (Vector(b) - Vector(a)).length
    o = striped_lathe([(ra, 0.0), (rb, L)], seg, mats, period)
    q = Vector((0, 0, 1)).rotation_difference((Vector(b) - Vector(a)).normalized())
    return xf(o, Matrix.Translation(a) @ q.to_matrix().to_4x4())


B = []
# ---------------------------------------------------------------- torso: striped sailor shirt
B.append(striped_lathe([(0.0, 0.84), (0.2, 0.845), (0.255, 0.9), (0.28, 1.0), (0.285, 1.1), (0.27, 1.2), (0.23, 1.29),
                        (0.15, 1.35), (0.0, 1.37)], 12, (WHITE, BLUE), 0.1, M=Matrix.Diagonal((1.0, 0.8, 1, 1)), z0=0.86))
# belt + buckle
B.append(lathe([(0.262, 0.86), (0.272, 0.88), (0.272, 0.92), (0.262, 0.94)], seg=14, material=NAVY,
               M=Matrix.Diagonal((1.0, 0.8, 1, 1))))
B.append(flat_shape([(-0.045, -0.035), (0.045, -0.035), (0.045, 0.035), (-0.045, 0.035)], 0.02, STRAW,
                    M=Matrix.Translation((0, -0.222, 0.9))))
# trousers (navy) with rolled-up blue cuffs and chunky boots
B.append(ell(V(0, 0, 0.8), (0.24, 0.19, 0.12), seg=12, rings=6, material=NAVY))
for sx in (-1, 1):
    hp, kn, an = V(sx * 0.12, 0, 0.8), V(sx * 0.13, -0.02, 0.45), V(sx * 0.13, 0, 0.2)
    B.append(tube([hp, kn, an], [0.105, 0.09, 0.085], seg=8, material=NAVY))
    B.append(lathe([(0.088, 0.17), (0.098, 0.18), (0.098, 0.24), (0.088, 0.25)], seg=8, material=BLUE,
                   M=Matrix.Translation((an.x, an.y, 0))))
    B.append(ell(V(an.x, -0.05, 0.075), (0.1, 0.16, 0.085), seg=8, rings=5, material=NAVY,
                 shape=lambda n: Vector((n.x, n.y, max(n.z, -0.88)))))
# red neckerchief knotted at the front
B.append(torus(R=0.13, r=0.045, seg=14, ring=6, material=RED))
xf(B[-1], Matrix.Translation((0, -0.01, 1.33)) @ Matrix.Diagonal((1.0, 0.95, 1.0, 1)))
B.append(ell(V(0, -0.14, 1.31), (0.05, 0.04, 0.04), seg=8, rings=5, material=RED))
for sx in (-1, 1):
    B.append(tube([V(sx * 0.02, -0.15, 1.3), V(sx * 0.06, -0.19, 1.2)], [0.035, 0.03], seg=6, flat=0.4, material=RED,
                  round_end=True))
body = apart(B, 'body', (0, 0, 0))

# ---------------------------------------------------------------- head (pivot at the neck)
NECK = V(0, 0, 1.36)
HC = V(0, -0.01, 1.56)
H = [tube([NECK + V(0, 0, -0.04), NECK + V(0, 0, 0.08)], 0.08, seg=8, material=SKIN),
     ell(HC, (0.2, 0.19, 0.21), seg=12, rings=9, material=SKIN,
         shape=lambda n: Vector((n.x * (1 + 0.06 * max(0, -n.z)), n.y, n.z)))]
for sx in (-1, 1):
    H.append(ell(HC + V(sx * 0.195, 0.02, -0.01), (0.04, 0.03, 0.06), seg=6, rings=4, material=SKIN))       # ears
    H += eye(HC + V(sx * 0.072, -0.17, 0.04), V(sx * 0.3, -1, 0.05), r=0.048, white=WHITE, black=NAVY, depth=0.55,
             tall=1.2, pupil=0.62, look=(-sx * 0.08, 0, 0.1), seg=8, pseg=7)
    b0, b1 = HC + V(sx * 0.03, -0.19, 0.125), HC + V(sx * 0.125, -0.15, 0.115)
    H.append(tube([b0, (b0 + b1) / 2 + V(0, -0.012, 0.035), b1], [0.014, 0.018, 0.012], seg=5, material=NAVY, round_end=True))
    H.append(ell(HC + V(sx * 0.11, -0.15, -0.045), (0.045, 0.03, 0.035), seg=6, rings=4, material=SKIN))    # chubby cheeks
    # sideburns
    H.append(ell(HC + V(sx * 0.18, -0.04, 0.02), (0.035, 0.05, 0.08), seg=6, rings=4, material=NAVY))
H.append(ell(HC + V(0, -0.205, -0.01), (0.048, 0.045, 0.045), seg=8, rings=5, material=SKIN))              # nose
# big open grin: dark mouth with teeth row and tongue
mouth = ell(V(0, 0, 0), (0.1, 0.03, 0.056), seg=10, rings=5, material=NAVY,
            shape=lambda n: Vector((n.x, n.y, n.z if n.z < 0 else n.z * 0.25)))
H.append(frame(mouth, HC + V(0, -0.175, -0.095), V(0, -1, -0.35)))
H.append(frame(ell(V(0, 0, 0), (0.075, 0.012, 0.015), seg=8, rings=3, material=WHITE), HC + V(0, -0.193, -0.084), V(0, -1, -0.35)))
H.append(frame(ell(V(0, 0, 0), (0.05, 0.012, 0.022), seg=8, rings=3, material=RED), HC + V(0, -0.19, -0.125), V(0, -1, -0.3)))
# chin stubble-beard ring
# straw hat: wide brim with a slight wave, crown, red band
HAT = HC + V(0, 0.015, 0.145)
bm = bmesh.new()
segs = 20
rings = []
for (r, dz) in ((0.17, 0.0), (0.26, -0.015), (0.34, -0.03), (0.355, -0.02)):
    rings.append([bm.verts.new((math.cos(TAU * i / segs) * r, math.sin(TAU * i / segs) * r,
                                dz + (0.012 * math.cos(3 * TAU * i / segs) if r > 0.3 else 0))) for i in range(segs)])
for a, b in zip(rings, rings[1:]):
    for i in range(segs):
        bm.faces.new((a[i], b[i], b[(i + 1) % segs], a[(i + 1) % segs]))
bot = [bm.verts.new((v.co.x, v.co.y, v.co.z - 0.02)) for v in rings[-1]]
for i in range(segs):
    bm.faces.new((rings[-1][i], bot[i], bot[(i + 1) % segs], rings[-1][(i + 1) % segs]))
bot2 = [bm.verts.new((v.co.x, v.co.y, v.co.z - 0.02)) for v in rings[0]]
for i in range(segs):
    bm.faces.new((bot[i], bot2[i], bot2[(i + 1) % segs], bot[(i + 1) % segs]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
brim = _obj(bm, STRAW)
xf(brim, Matrix.Translation(HAT) @ rotm((-8, 0, 0)))
H.append(brim)
H.append(lathe([(0.18, -0.01), (0.175, 0.08), (0.16, 0.14), (0.0, 0.15)], seg=14, material=STRAW,
               M=Matrix.Translation(HAT) @ rotm((-8, 0, 0))))
H.append(lathe([(0.183, 0.0), (0.18, 0.05)], seg=14, material=RED, M=Matrix.Translation(HAT) @ rotm((-8, 0, 0))))
# straw weave rings on the brim
for r in (0.27,):
    H.append(lathe([(r - 0.006, 0.0), (r, 0.004), (r + 0.006, 0.0)], seg=20, material=STRAW,
                   M=Matrix.Translation(HAT + V(0, 0, -0.012 - 0.01 * (r - 0.24) / 0.07)) @ rotm((-8, 0, 0))))
head = apart(H, 'head', NECK)

# ---------------------------------------------------------------- arms (pivot at the shoulders), reaching forward/up to pull a rope
ARM = {}
for side, sx in (('l', 1), ('r', -1)):
    S = V(sx * 0.27, 0.0, 1.27)
    E = V(sx * 0.32, -0.26, 1.2)
    Hd = V(sx * 0.17, -0.55, 1.24) if side == 'r' else V(sx * 0.17, -0.55, 1.36)
    A = [ell(S, (0.095, 0.1, 0.1), seg=7, rings=5, material=WHITE),
         striped_tube(S, E + (E - S).normalized() * 0.02, 0.09, 0.08, 8, 0.1, (BLUE, WHITE)),
         tube([E, Hd], [0.065, 0.055], seg=8, material=SKIN),
         ell(E, (0.068, 0.068, 0.068), seg=6, rings=4, material=SKIN)]
    # fist gripping (with thumb on top)
    d = (Hd - E).normalized()
    A.append(ell(Hd + d * 0.04, (0.07, 0.07, 0.065), seg=7, rings=5, material=SKIN))
    A.append(ell(Hd + d * 0.05 + V(0, 0, 0.055), (0.03, 0.04, 0.025), seg=6, rings=4, material=SKIN))
    apart(A, f'arm_{side}', S)
    ARM[side] = (S, Hd + d * 0.04)

report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('De veerman. Parts/pivots (Blender coords, front -Y, left=+X; ~1.8 m incl. straw hat): body (origin 0,0,0; blue/white '
         'striped shirt, red neckerchief, navy trousers with rolled cuffs, boots on z=0); '
         f'head (pivot neck {fmt(NECK)}; big grin, eyes, brows, rosy cheeks, straw hat with red band); '
         f'arm_l (pivot shoulder {fmt(ARM["l"][0])}, fist at {fmt(ARM["l"][1])}), arm_r (pivot shoulder {fmt(ARM["r"][0])}, fist at '
         f'{fmt(ARM["r"][1])}): striped sleeves, arms reaching forward/up, fists one above the other as if pulling a rope '
         '(rope runs along X in front of him). Materials: skin, white, stripe_blue, navy, straw, red.')
finish('chars', 'ferryman', kind='char', footprint=0.35, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['arm_l'].rotation_euler = (0.5, 0, 0)
        bpy.data.objects['arm_r'].rotation_euler = (-0.4, 0, 0)
        bpy.data.objects['head'].rotation_euler = (0, 0, 0.4)
    views2('ferryman', dirs={'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (0.7, 1, 0.5)}, dist=1.2)
    views2('ferryman_face', dirs={'f': (0.2, -1, 0.15)}, focus=((0, -0.1, 1.55), 0.8), dist=1.2)
    views2('ferryman_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose)
