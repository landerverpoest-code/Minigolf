import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akit import *
from ccp_kit import _obj

# ---------------------------------------------------------------- materials (5)
ROCK = mat('rock', '#4b3c35', rough=0.85)
ROCK2 = mat('rock_light', '#665247', rough=0.9)
LAVA = mat('glow_lava', '#ff7a1a', rough=0.5, emit='#ff4a00', emit_strength=3.5)
WHITE = mat('eye_white', '#fffaf0', rough=0.35)
PUPIL = mat('pupil', '#1c1414', rough=0.4)

rnd = random.Random(7)
# ---------------------------------------------------------------- rock: voronoi plates separated by glowing cracks
NCELL = 15
seeds = []
for i in range(NCELL):             # fibonacci sphere + jitter
    z = 1 - 2 * (i + 0.5) / NCELL
    r = math.sqrt(1 - z * z); a = i * 2.39996 + 0.3
    seeds.append((V(math.cos(a) * r, math.sin(a) * r, z) + V(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)) * 0.12).normalized())
cell_r = [rnd.uniform(0.968, 0.992) for _ in seeds]
cell_m = [rnd.random() < 0.35 for _ in seeds]

bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)


def cell_of(p):
    pn = p.normalized()
    nz = noise.noise(pn * 2.3) * 0.1
    best, bi = 9, 0
    for i, s in enumerate(seeds):
        d = (pn - s).length + (noise.noise(pn * 3.1 + V(i, 0, 0)) * 0.08)
        if d < best:
            best, bi = d, i
    return bi


fc = {}
for f in bm.faces:
    fc[f] = cell_of(f.calc_center_median())
bnd = [e for e in bm.edges if len(e.link_faces) == 2 and fc[e.link_faces[0]] != fc[e.link_faces[1]]]
bmesh.ops.split_edges(bm, edges=bnd)
# after the split every vertex belongs to exactly one cell
vcell = {}
for f in bm.faces:
    for v in f.verts:
        vcell[v] = fc[f]
for f in bm.faces:
    f.material_index = 1 if cell_m[fc[f]] else 0
border = set()
for e in bm.edges:
    if len(e.link_faces) == 1:
        border.update(e.verts)
tilt = [V(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in seeds]
newco = {}
for v in bm.verts:
    ci = vcell[v]; c = seeds[ci]
    d = v.co.normalized()
    rr = cell_r[ci] + noise.noise(d * 3.0 + V(ci, ci, 0)) * 0.03 + 0.035 * max(0.0, d.dot(c)) + 0.03 * (d - c).dot(tilt[ci])
    if v in border:
        t = c - d * d.dot(c)
        if t.length > 1e-6:
            d = (d + t.normalized() * 0.03).normalized()
        rr -= 0.035
    newco[v] = (d, rr)
rmax = max(r for d, r in newco.values())
for v, (d, r) in newco.items():
    v.co = d * (r / rmax)               # outermost point exactly at r = 1.0
# side walls: extrude the open borders inward
bedges = [e for e in bm.edges if len(e.link_faces) == 1]
ret = bmesh.ops.extrude_edge_only(bm, edges=bedges)
for v in [g for g in ret['geom'] if isinstance(g, bmesh.types.BMVert)]:
    v.co = v.co.normalized() * 0.86
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
rock = _obj(bm, ROCK)
rock.data.materials.append(ROCK2)
smooth_sharp(rock, 40)
core = ell(V(0, 0, 0), (0.9, 0.9, 0.9), seg=14, rings=9, material=LAVA)
rock_o = part([rock, core], 'rock', (0, 0, 0))
smooth_sharp(rock_o, 40)

# ---------------------------------------------------------------- face (origin = rock centre, sits just outside r=1)
F = []


def sph(x, z, r=1.0):
    """Point on the sphere of radius r on the -Y side at (x, z)."""
    y = -math.sqrt(max(r * r - x * x - z * z, 1e-6))
    return V(x, y, z)


def strip(cols, r, material):
    bm = bmesh.new(); grid = []
    for x, zs in cols:
        grid.append([bm.verts.new(sph(x, z, r)) for z in zs])
    for i in range(len(grid) - 1):
        for j in range(len(grid[i]) - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    return _obj(bm, material)


# eyes: big bulging whites (left one a bit bigger = funny), small angry pupils
for sx, er in ((1, 0.25), (-1, 0.22)):
    c = sph(sx * 0.33, 0.24, 0.93)
    d = c.normalized()
    F.append(frame(ell(V(0, 0, 0), (er, er * 0.6, er * 1.12), seg=14, rings=8, material=WHITE), c, d))
    pc = c + d * (er * 0.6) + V(-sx * 0.04, 0, -0.03)
    F.append(frame(ell(V(0, 0, 0), (er * 0.36, 0.03, er * 0.4), seg=10, rings=5, material=PUPIL), pc, d))
    F.append(frame(ell(V(0, 0, 0), (er * 0.11, 0.012, er * 0.12), seg=6, rings=3, material=WHITE),
                   pc + d * 0.025 + V(sx * 0.03, 0, 0.04), d))
    # angry brow slab (rock), tilted down toward the nose, overlapping the top of the eye
    bc = sph(sx * 0.33, 0.45, 1.06)
    brow = ell(V(0, 0, 0), (0.3, 0.1, 0.085), seg=8, rings=5, p=0.7, material=ROCK2)
    frame(brow, V(0, 0, 0), bc.normalized())
    xf(brow, Matrix.Translation(bc) @ Matrix.Rotation(math.radians(sx * 26), 4, bc.normalized()))
    F.append(brow)
# mouth: wide grimace, dark inside with lava glowing at the bottom, a row of white teeth on top
MZ, MW = -0.33, 0.42


def top(x):
    return MZ + 0.1 - 0.13 * (x / MW) ** 2


def bot(x):
    return MZ - 0.15 + 0.14 * (x / MW) ** 2


cols = []
for i in range(13):
    x = -MW + 2 * MW * i / 12
    t, b = top(x), bot(x)
    if i in (0, 12):
        m = (t + b) / 2; t, b = m + 0.01, m - 0.01
    cols.append((x, [b, (b + t) / 2, t]))
F.append(strip(cols, 1.012, PUPIL))
lava = []
for i in range(1, 12):
    x = -MW + 2 * MW * i / 12
    b = bot(x)
    lava.append((x * 0.85, [b + 0.015, b + 0.06 - 0.03 * (x / MW) ** 2]))
F.append(strip(lava, 1.018, LAVA))
for k in range(6):
    x0 = -0.3 + k * 0.105
    tt = top(x0 + 0.04)
    F.append(strip([(x0 + 0.008, [tt - 0.085, tt + 0.005]), (x0 + 0.088, [tt - 0.085, tt + 0.005])], 1.024, WHITE))
# rocky lips above and below
for zf, wsc in ((top, 1.0), (bot, 0.92)):
    pts = [sph(x * wsc, zf(x * wsc) + (0.02 if zf is top else -0.02), 1.02) for x in [-MW + 2 * MW * i / 8 for i in range(9)]]
    F.append(tube(pts, 0.035, seg=5, material=ROCK2, flat=0.6))
face = apart(F, 'face', (0, 0, 0))

report()
notes = ('Parts/pivots (Blender coords, front -Y): rock (origin = centre (0,0,0); voronoi plates of rock / rock_light, max radius '
         'exactly 1.0, separated by glowing cracks = inner lava core glow_lava (r 0.9); rotate it to roll); face (origin = rock centre '
         '(0,0,0); on the -Y side, everything outside r=1.0: two bulging eyes (left bigger), small pupils with highlights, angry '
         'rock brows, wide grimace with white teeth and lava glowing in the mouth; keep it upright and yaw it toward the motion). '
         'Materials: rock, rock_light, glow_lava, eye_white, pupil.')
finish('chars', 'boulder', kind='char', footprint=1.0, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['rock'].rotation_euler = (0.7, 0.3, 0)
    views('boulder', dirs={'front': (0, -1, 0.15), 'side': (1, -0.2, 0.1), 'back': (-0.7, 1, 0.5)}, pose=pose)
