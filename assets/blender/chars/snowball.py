import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *
from gkit import _obj

# ---------------------------------------------------------------- materials (6)
SNOW = mat('snow', '#f4f8ff', rough=0.75)
COAL = mat('coal', '#1b1c22', rough=0.25)
CARROT = mat('carrot', '#ff7a1a', rough=0.5)
TWIG = mat('twig', '#6b4426', rough=0.75)
STONE = mat('stone', '#8a8f9a', rough=0.6)
MOUTH = mat('mouth', '#6e1c2c', rough=0.5)

rnd = random.Random(11)
# ---------------------------------------------------------------- ball: lumpy snow sphere, max radius exactly 1.0
bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
off = Vector((3.1, 7.7, 1.3))
for v in bm.verts:
    n = v.co.normalized()
    lump = 0.5 + 0.5 * noise.noise(n * 2.2 + off)              # 0..1 big soft lumps
    fine = 0.5 + 0.5 * noise.noise(n * 5.5 + off * 2)
    v.co = n * (1.0 - 0.085 * (1 - lump) - 0.025 * (1 - fine))
ball_core = _obj(bm, SNOW)
# rescale so the furthest vertex is exactly 1.0
mx = max(v.co.length for v in ball_core.data.vertices)
xf(ball_core, Matrix.Diagonal((1 / mx, 1 / mx, 1 / mx, 1)))
Bl = [ball_core]


def rdir():
    while True:
        d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
        if 0.2 < d.length < 1:
            return d.normalized()


def frame_n(o, n, at):
    """local +Z -> n, then move to at."""
    q = Vector((0, 0, 1)).rotation_difference(n)
    return xf(o, Matrix.Translation(at) @ q.to_matrix().to_4x4())


# twigs stuck in the snow (avoid the face zone on -Y)
twig_dirs = [V(0.8, 0.3, 0.5), V(-0.6, 0.5, 0.6), V(0.3, 0.9, -0.3), V(-0.9, -0.1, -0.4), V(0.7, -0.2, -0.7)]
for d in twig_dirs:
    d = d.normalized()
    side = d.cross(V(0, 0, 1) if abs(d.z) < 0.9 else V(1, 0, 0)).normalized()
    p0 = d * 0.9
    p1 = d * 1.2 + side * 0.06
    p2 = d * 1.42 + side * 0.02
    Bl.append(tube([p0, p1, p2], [0.05, 0.038, 0.015], seg=5, material=TWIG, round_end=True))
    f0 = d * 1.2 + side * 0.06
    Bl.append(tube([f0, f0 + d * 0.12 + side * 0.13], [0.026, 0.01], seg=4, material=TWIG, round_end=True))
    f1 = d * 1.08 + side * 0.03
    Bl.append(tube([f1, f1 + d * 0.08 - side * 0.11], [0.024, 0.009], seg=4, material=TWIG, round_end=True))
# pebbles half embedded
for d in (V(0.9, -0.3, 0.1), V(-0.4, 0.8, -0.2), V(0.1, 0.4, 0.9), V(-0.7, 0.2, 0.0), V(0.5, 0.6, 0.4), V(0.2, 0.3, -0.95),
          V(-0.3, -0.5, -0.8), V(0.95, 0.2, -0.2)):
    d = d.normalized()
    r = rnd.uniform(0.08, 0.13)
    pb = ico(r=r, sub=1, material=STONE, scale=(1.0, 1.2, 0.6), jitter=r * 0.15, seed=rnd.randint(0, 999))
    pb.location = (0, 0, 0)
    frame_n(pb, d, d * 0.985)
    for p in pb.data.polygons:
        p.use_smooth = True
    Bl.append(pb)
# little stuck-on snow clumps for a rolled look
for k in range(10):
    d = rdir()
    if d.y < -0.5:
        d.y = -d.y
    Bl.append(frame_n(ell(V(0, 0, 0), (0.16, 0.13, 0.08), seg=8, rings=5, material=SNOW), d, d * 0.955))
ball = apart(Bl, 'ball', (0, 0, 0))

# ---------------------------------------------------------------- face (stays upright), everything just outside r=1.0
F = []


def on_sphere(d, r=1.0):
    return Vector(d).normalized() * r


for sx in (-1, 1):
    d = V(sx * 0.37, -1, 0.3).normalized()
    # big round coal eyes (slightly lumpy) with a glint
    e = ico(r=0.17, sub=2, material=COAL, scale=(1.0, 1.22, 0.5), jitter=0.006, seed=3 + sx)
    e.location = (0, 0, 0)
    frame_n(e, d, d * 1.065)
    for p in e.data.polygons:
        p.use_smooth = True
    F.append(e)
    g = ell(V(0, 0, 0), (0.045, 0.04, 0.02), seg=6, rings=4, material=SNOW)
    F.append(frame_n(g, d, d * 1.135 + V(-sx * 0.035, 0, 0.08)))
    F.append(frame_n(ell(V(0, 0, 0), (0.02, 0.018, 0.01), seg=5, rings=3, material=SNOW), d, d * 1.135 + V(sx * 0.045, 0, -0.06)))
    # raised surprised brows: arched coal bars high above the eyes
    pts = []
    for i in range(5):
        t = -1 + 2 * i / 4
        dd = V(sx * 0.37 + t * 0.19, -1, 0.68 + 0.08 * (1 - t * t)).normalized()
        pts.append(dd * 1.045)
    F.append(tube(pts, [0.04, 0.052, 0.055, 0.052, 0.04], seg=5, material=COAL, round_end=True))
# carrot nose
nd = V(0, -1, 0.02).normalized()
nb = nd * 0.99
F.append(tube([nb, nb + V(0.01, -0.14, -0.01), nb + V(0.02, -0.33, -0.035), nb + V(0.03, -0.52, -0.07)],
              [0.14, 0.115, 0.075, 0.012], seg=8, material=CARROT))
for k, t in enumerate((0.12, 0.22, 0.32)):     # carrot ridges
    c = nb + V(0.01 + t * 0.05, -t * 1.15 - 0.02, -0.01 - t * 0.11)
    rr = 0.135 - t * 0.3
    ring = lathe([(rr, -0.008), (rr + 0.012, 0.0), (rr, 0.008)], seg=8, material=CARROT)
    F.append(xf(ring, Matrix.Translation(c) @ rotm((90, 0, 0))))
# big surprised "O" mouth: dark oval with a snow lip around it
md = V(0, -1, -0.5).normalized()
mo2 = ell(V(0, 0, 0), (0.19, 0.24, 0.03), seg=14, rings=6, material=MOUTH)
frame_n(mo2, md, md * 1.005)
F.append(mo2)
lip = lathe([(0.2, -0.035), (0.245, 0.0), (0.2, 0.045), (0.165, 0.0)], seg=14, material=SNOW,
            M=Matrix.Diagonal((1.0, 1.24, 1, 1)))
F.append(frame_n(lip, md, md * 1.01))
# tongue
tg = ell(V(0, 0, 0), (0.1, 0.075, 0.02), seg=8, rings=4, material=CARROT)
F.append(frame_n(tg, md, md * 1.03 + V(0, 0.0, -0.11)))
# coal "teeth"? keep it clean. Rosy cheeks as snow puffs
for sx in (-1, 1):
    d = V(sx * 0.62, -1, -0.12).normalized()
    F.append(frame_n(ell(V(0, 0, 0), (0.12, 0.09, 0.04), seg=8, rings=4, material=SNOW), d, d * 1.0))
face = apart(F, 'face', (0, 0, 0))

report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
mn = min(v.co.length for v in face.data.vertices)
print('FACE min r', mn)
notes = ('De reuzensneeuwbal. Parts/pivots (Blender coords, front -Y): ball (origin = centre (0,0,0); lumpy snow sphere, max radius '
         'exactly 1.0, with twigs, pebbles and stuck-on snow clumps; rotate it to roll); face (origin = ball centre (0,0,0); on the -Y side '
         'just outside r=1.0: big coal eyes with glints, raised coal brows, carrot nose, big surprised "O" mouth with snow lip and tongue, '
         'snow cheeks; keep it upright). Materials: snow, coal, carrot, twig, stone, mouth.')
finish('chars', 'snowball', kind='char', footprint=1.0, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['ball'].rotation_euler = (1.0, 0, 0)
    views2('snowball', dirs={'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (0.7, 1, 0.5)}, dist=1.4)
    views2('snowball_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose)
