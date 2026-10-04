import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/volcano'); from _deco import *

ASH = mat('ash', '#8a827c', rough=1.0)
ROCK = mat('rock_brown', '#5e4a3c', rough=0.9)
BONE = mat('bone', '#ecdfc0', rough=0.6)
BONE_D = mat('bone_old', '#c9b48e', rough=0.7)
DARK = mat('socket_dark', '#2a1d19', rough=0.9)

rnd = random.Random(5)
# --- lage aarden plek (lang langs X); kop naar -X
ground = lathe([(1.0, 0.0), (0.85, 0.05), (0.5, 0.085), (0.0, 0.095)], verts=11, material=ROCK, sx=1.35, sy=0.75, jitter=0.1, seed=3)
lumpy(ground, amp=0.04, freq=2.5, seed=1, axes=(1, 1, 0.5))
flat(ground)
recolor(ground, [ROCK, ASH], lambda f: 1 if noise.noise(f.center * 2.2) > 0.1 and f.normal.z > 0.8 else 0)
GZ = 0.1

# --- wervelkolom: boog van de kop omhoog over de ribbenkast en de staart weer de grond in
def spine_pt(t):
    x = -0.7 + t * 1.85
    z = GZ + 0.05 + 0.48 * math.sin(min(1, t * 1.25) * math.pi) ** 0.8 * (1 if t < 0.8 else max(0, 1 - (t - 0.8) * 5))
    return Vector((x, 0.03 * math.sin(t * 4), z))


N = 12
bpts = [spine_pt(i / (N - 1)) for i in range(N)]
tube(bpts, [0.055 * (1 - 0.6 * i / (N - 1)) for i in range(N)], verts=4, material=BONE_D, smooth=True)
for i in range(1, N - 1):
    t = i / (N - 1)
    p = bpts[i]; q = bpts[i + 1] - bpts[i - 1]
    s = 1 - 0.55 * t
    v = cyl(0.068 * s, 0.05 * s, verts=5, material=BONE)
    T(v, rot=(0, 90, 0))
    sp = cone(0.028 * s, 0.12 * s, verts=3, material=BONE, loc=(0, 0, 0.08 * s))
    o = join([v, sp], 'vert')
    ang = math.degrees(math.atan2(q.z, q.x))
    T(o, rot=(0, -ang, 0), loc=p)

# --- ribbenkast: bogen van de ruggengraat tot in de grond
for k in range(4):
    t = 0.2 + k * 0.1
    sp = spine_pt(t)
    for side in (-1, 1):
        pts = []
        for j in range(4):
            u = j / 3
            a = u * math.pi * 0.75
            y = sp.y + side * (0.05 + 0.34 * math.sin(a)) * (1 - 0.08 * k)
            z = sp.z + 0.05 - (sp.z - GZ + 0.05) * (1 - math.cos(a)) / (1 - math.cos(math.pi * 0.75))
            pts.append(Vector((sp.x + 0.06 * u, y, z)))
        tube(pts, [0.03, 0.027, 0.025, 0.024], verts=4, material=BONE, cap0=False, cap1=False, smooth=True)

# --- schedel (T-rex-achtig), rust op de grond, bek open
SX, SZ = -0.95, GZ + 0.2
cran = sphere(1.0, seg=7, rings=5, material=BONE, scale=(0.21, 0.18, 0.17), smooth=False)
T(cran, loc=(SX + 0.14, 0, SZ + 0.05))
snout = lathe([(0.16, 0.0), (0.14, 0.2), (0.09, 0.36), (0.0, 0.4)], verts=6, material=BONE, sx=0.75, sy=1.0)
T(snout, rot=(0, -98, 0), loc=(SX + 0.03, 0, SZ))
for s in (-1, 1):
    sphere(0.065, loc=(SX + 0.12, s * 0.14, SZ + 0.1), seg=5, rings=3, material=DARK, scale=(1, 0.45, 1))
    sphere(0.028, loc=(SX - 0.32, s * 0.055, SZ + 0.06), seg=4, rings=3, material=DARK)
    box((0.14, 0.05, 0.035), loc=(SX + 0.12, s * 0.12, SZ + 0.18), rot=(s * 0.3, 0, 0), material=BONE_D)
    for i in range(4):
        cone(0.018, 0.08, verts=3, material=BONE, loc=(SX - 0.3 + i * 0.08, s * 0.085, SZ - 0.085), rot=(math.pi, 0, 0))
# onderkaak open op de grond
jaw = plank((SX + 0.2, 0, SZ - 0.13), (SX - 0.38, 0, GZ + 0.02), w=0.2, t=0.05, material=BONE_D)
taper(jaw, 0.8)
for i in range(3):
    for s in (-1, 1):
        x = SX - 0.25 + i * 0.1
        cone(0.016, 0.06, verts=3, material=BONE, loc=(x, s * 0.07, GZ + 0.04 + (i * 0.035) + 0.04))

# --- dijbeen en losse botjes
fem = rod((0.45, -0.38, GZ + 0.02), (0.75, -0.22, GZ + 0.1), r=0.035, verts=5, material=BONE)
for e, p in enumerate(((0.43, -0.39, GZ + 0.03), (0.77, -0.21, GZ + 0.11))):
    sphere(0.055, loc=p, seg=5, rings=3, material=BONE)
for k, (x, y, a) in enumerate(((0.95, 0.42, 30), (-0.4, 0.52, -50))):
    b = rod((-0.12, 0, 0), (0.12, 0, 0), r=0.022, verts=4, material=BONE_D)
    T(b, rot=(0, 0, a), loc=(x, y, GZ + 0.02))
o = join_all('fossil_skeleton')
shade_smooth(o, 46)
report()
done('volcano', 'fossil_skeleton', kind='scatter', footprint=1.35, center=True,
     notes='Dinosaurusfossiel half in de grond: T-rex-schedel met oogkassen, tanden en open onderkaak, boogvormige wervelkolom met doornuitsteeksels, ribbenkast die uit de aarde steekt, dijbeen en losse botjes')
