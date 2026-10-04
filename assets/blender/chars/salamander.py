import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *

# ---------------------------------------------------------------- materials (6)
SKIN = mat('sala_black', '#1c1a22', rough=0.3)                     # glossy black skin + pupils
GLOW = mat('glow_spots', '#ff6000', rough=0.5, emit='#ff5a00', emit_strength=1.2)
YEL = mat('eye_yellow', '#ffd21f', rough=0.3)
WHITE = mat('white', '#ffffff', rough=0.3)
BLUSH = mat('blush', '#ff7f8f', rough=0.6)
MOUTH = mat('mouth', '#d9455a', rough=0.5)

rnd = random.Random(7)


def spot_field(centres):
    def f(p):
        return min(((p.x - c.x) / r[0]) ** 2 + ((p.y - c.y) / r[1]) ** 2 + ((p.z - c.z) / r[2]) ** 2 for c, r in centres) - 1
    return f


# ---------------------------------------------------------------- body: head + front torso
TC = V(0, -0.14, 0.16)
torso = ell(TC, (0.155, 0.25, 0.105), seg=14, rings=9, material=SKIN,
            shape=lambda n: Vector((n.x * (1 + 0.05 * n.y), n.y, n.z if n.z > 0 else n.z * 0.75)))
HC = V(0, -0.46, 0.165)


def head_shape(n):
    # flat, wide frog-like head, broad at the back and round at the snout
    k = 1.0 + 0.12 * n.y
    z = n.z * (1.0 if n.z > 0 else 0.7)
    return Vector((n.x * k, n.y, z))


head = ell(HC, (0.16, 0.16, 0.095), seg=14, rings=9, material=SKIN, shape=head_shape)
neck = ell(V(0, -0.33, 0.16), (0.14, 0.1, 0.09), seg=10, rings=6, material=SKIN)
# glowing spots: two rows along the back + a few on the head (paired like a real fire salamander)
spots = [(V(0.07, -0.53, 0.235), (0.045, 0.05, 0.06)), (V(-0.07, -0.53, 0.235), (0.045, 0.05, 0.06)),
         (V(0.1, -0.4, 0.23), (0.055, 0.06, 0.07)), (V(-0.1, -0.4, 0.23), (0.055, 0.06, 0.07)),
         (V(0.075, -0.24, 0.25), (0.05, 0.075, 0.06)), (V(-0.085, -0.19, 0.25), (0.055, 0.06, 0.06)),
         (V(0.08, -0.05, 0.25), (0.05, 0.06, 0.06)), (V(-0.06, 0.0, 0.25), (0.045, 0.05, 0.06)),
         (V(0.15, -0.14, 0.17), (0.04, 0.05, 0.04)), (V(-0.155, -0.08, 0.17), (0.04, 0.045, 0.04))]
Bd = [torso, head, neck]
for c, r in spots:
    Bd.append(surf_blob([torso, head, neck], V(c.x * 1.3, c.y, 0.6) if abs(c.x) < 0.13 else V(c.x * 2.5, c.y, c.z + 0.05),
                        V(-c.x * 0.3, 0, -1) if abs(c.x) < 0.13 else V(-1 if c.x > 0 else 1, 0, -0.1),
                        r=(r[0] * 0.9, r[1] * 0.9), h=0.012, material=GLOW, seg=7, rings=3, spin=rnd.uniform(-30, 30)))
# eyes: big bulging yellow eyes on top of the head, looking forward
for sx in (-1, 1):
    ec = HC + V(sx * 0.082, -0.075, 0.08)
    Bd.append(ell(ec + V(sx * 0.005, 0.025, -0.02), (0.07, 0.06, 0.055), seg=9, rings=6, material=SKIN))   # eye socket bump
    Bd += eye(ec, V(sx * 0.4, -1, 0.2), r=0.066, white=YEL, black=SKIN, depth=0.7, tall=1.1, pupil=0.7,
              look=(-sx * 0.15, 0, 0.0), seg=10, pseg=8, hlmat=WHITE)
    # blush
    Bd.append(ell(HC + V(sx * 0.125, -0.085, 0.02), (0.035, 0.02, 0.022), seg=6, rings=4, material=BLUSH,
                  rot=(0, 0, sx * -50)))
# wide happy smile across the snout
sm = []
for i in range(9):
    t = -1 + 2 * i / 8
    a = t * 0.9
    sm.append(HC + V(math.sin(a) * 0.152, -math.cos(a) * 0.156, -0.018 + 0.022 * t * t))
Bd.append(tube(sm, [0.006, 0.008, 0.009, 0.01, 0.01, 0.01, 0.009, 0.008, 0.006], seg=4, material=MOUTH, round_end=True))
for sx in (-1, 1):  # nostrils
    Bd.append(ell(HC + V(sx * 0.04, -0.155, 0.04), (0.012, 0.008, 0.007), seg=5, rings=3, material=MOUTH))
body = apart(Bd, 'body', (0, 0, 0))

# ---------------------------------------------------------------- tail: rear body + tail (pivot where it joins)
TJ = V(0, 0.03, 0.155)
rear = ell(V(0, 0.12, 0.15), (0.14, 0.17, 0.095), seg=14, rings=9, material=SKIN,
           shape=lambda n: Vector((n.x, n.y, n.z if n.z > 0 else n.z * 0.75)))
tp = bezier(V(0, 0.2, 0.15), V(0, 0.38, 0.13), V(0, 0.5, 0.07), V(0, 0.68, 0.08), n=7)
tail = tube(tp, [0.11, 0.1, 0.085, 0.07, 0.055, 0.04, 0.025, 0.006], seg=10, flat=1.25, flat_n=False, material=SKIN,
            round_end=True)
tspots = [(V(0.06, 0.12, 0.24), (0.05, 0.06, 0.06)), (V(-0.07, 0.17, 0.235), (0.05, 0.055, 0.06)),
          (V(0.05, 0.3, 0.22), (0.045, 0.05, 0.06)), (V(-0.04, 0.4, 0.2), (0.04, 0.05, 0.06)),
          (V(0.03, 0.5, 0.16), (0.032, 0.04, 0.05)), (V(-0.02, 0.6, 0.13), (0.025, 0.035, 0.05)),
          (V(0.14, 0.1, 0.16), (0.04, 0.04, 0.04)), (V(-0.14, 0.06, 0.16), (0.04, 0.04, 0.04))]
T = [rear, tail]
for c, r in tspots:
    T.append(surf_blob([rear, tail], V(c.x * 1.3, c.y, 0.6) if abs(c.x) < 0.13 else V(c.x * 2.5, c.y, c.z + 0.05),
                       V(-c.x * 0.3, 0, -1) if abs(c.x) < 0.13 else V(-1 if c.x > 0 else 1, 0, -0.1),
                       r=(r[0] * 0.9, r[1] * 0.9), h=0.012, material=GLOW, seg=7, rings=3, spin=rnd.uniform(-30, 30)))
apart(T, 'tail', TJ)

# ---------------------------------------------------------------- legs (pivot at shoulder / hip), splayed lizard legs
LEGS = {}
for name, sx, sy in (('fl', 1, -0.21), ('fr', -1, -0.21), ('bl', 1, 0.1), ('br', -1, 0.1)):
    P = V(sx * 0.12, sy, 0.14)
    back = name[0] == 'b'
    elb = V(sx * 0.25, sy + (0.02 if back else -0.02), 0.12)
    hand = V(sx * 0.28, sy + (0.05 if back else -0.06), 0.03)
    L = [tube([P, elb, hand], [0.055, 0.046, 0.04], seg=7, material=SKIN),
         ell(elb, (0.048, 0.048, 0.048), seg=6, rings=4, material=SKIN)]
    foot_c = hand + V(sx * 0.02, -0.02, -0.012)
    L.append(ell(foot_c, (0.055, 0.05, 0.022), seg=7, rings=4, material=SKIN))
    # four chubby toes fanned forward/outward
    for k in range(3):
        a = math.radians(-40 + k * 40) * sx + (math.radians(25) * sx if back else 0)
        tc = foot_c + V(math.sin(a) * 0.062, -math.cos(a) * 0.062, -0.004)
        L.append(ell(tc, (0.022, 0.022, 0.017), seg=7, rings=4, material=SKIN))
    sp = (P + elb) / 2
    L.append(surf_blob([L[0]], sp + V(0, 0, 0.3), V(0, 0, -1), r=(0.03, 0.035), h=0.01, material=GLOW, seg=7, rings=3))
    apart(L, f'leg_{name}', P)
    LEGS[name] = P

# scale to ~1.2 m long, then bring the feet exactly to z=0 (body origin stays at 0,0,0)
KS = 0.915
scale_all(KS)
LEGS = {k: v * KS for k, v in LEGS.items()}
TJ = TJ * KS
lo, hi = bounds()
dz = -lo.z
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        if o.name == 'body':
            o.data.transform(Matrix.Translation((0, 0, dz)))
        else:
            o.location.z += dz
for k in LEGS:
    LEGS[k] = LEGS[k] + V(0, 0, dz)
TJ = TJ + V(0, 0, dz)
bpy.context.view_layer.update()
report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('De vuursalamander. Parts/pivots (Blender coords, front -Y, left=+X; ~1.2 m long, low): '
         'body (origin 0,0,0; flat head with big yellow eyes, smile, blush + front torso); '
         f'tail (pivot at the join {fmt(TJ)}; rear body + tapering tail toward +Y, sway about Z); '
         f'leg_fl {fmt(LEGS["fl"])}, leg_fr {fmt(LEGS["fr"])}, leg_bl {fmt(LEGS["bl"])}, leg_br {fmt(LEGS["br"])} '
         '(pivot shoulder/hip, splayed legs, feet on z=0). Glowing orange spots = material glow_spots. '
         'Materials: sala_black, glow_spots, eye_yellow, white, blush, mouth.')
finish('chars', 'salamander', kind='char', footprint=0.4, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['tail'].rotation_euler = (0, 0, 0.5)
        bpy.data.objects['leg_fl'].rotation_euler = (0, 0, 0.4)
    views2('salamander', dirs={'front': (0, -1, 0.3), 'side': (-1, 0, 0.2), 'top': (0.2, 0.3, 1), 'face': (0.3, -1, 0.5)})
    views2('salamander_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose)
