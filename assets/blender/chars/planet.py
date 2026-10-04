import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
V = Vector

# ---------- materialen (6) ----------
purple = mat('purple', '#7b3fe0', rough=0.55, emit='#3a1070', emit_strength=0.25)
pink = mat('pink', '#ff6fb8', rough=0.5, emit='#5a1040', emit_strength=0.15)
gold = mat('gold', '#ffcf6e', rough=0.4, metal=0.15)
white = mat('eye_white', '#ffffff', rough=0.25)
dark = mat('pupil', '#1f0f30', rough=0.2)
moon_m = mat('moon', '#cfcadc', rough=0.85)


def part(objs, name, pivot):
    o = join(objs if isinstance(objs, list) else [objs], name)
    bake(o); o.data.name = name
    origin_to(o, pivot)
    return o


def on_sphere(o, d, R=1.0, sink=0.0, center=(0, 0, 0)):
    """Object gebouwd rond de oorsprong (as +Z) op een bol (straal R) zetten in richting d."""
    n = V(d).normalized()
    q = V((0, 0, 1)).rotation_difference(n)
    T(o, rot=q.to_euler(), loc=V(center) + n * (R - sink))
    return o


def decal(poly, r_front, r_back, material, name='decal'):
    """2D-vorm (u, v) op het -Y-vlak, radiaal op de bol geprojecteerd tot een dun schelpje."""
    o = prism(poly, depth=0.02, material=material, axis='y', name=name)
    def f(v):
        rr = r_front if v.y < 0 else r_back
        return V((v.x, -1.0, v.z)).normalized() * rr
    deform(o, f)
    return o


# ---------- planeet: bol r=1.0 met golvende banden ----------
pl = sphere(1.0, seg=28, rings=16, material=purple, smooth=True)
pl.data.materials.append(pink); pl.data.materials.append(gold)
bake(pl)
# banden per ring (ring-index van het originele bolnet) -> grenzen volgen de golvende ringlijnen netjes
RINGS = 16
band_of_ring = [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0]      # 0 paars, 1 roze, 2 goud
for poly in pl.data.polygons:
    lat = math.asin(max(-1, min(1, poly.center.normalized().z)))
    k = min(RINGS - 1, max(0, int((math.pi / 2 - lat) / (math.pi / RINGS))))
    poly.material_index = band_of_ring[k]
for v in pl.data.vertices:
    p = v.co.normalized()
    lat = math.asin(max(-1, min(1, p.z))); lon = math.atan2(p.y, p.x)
    if abs(lat) < 1.45:
        lat += 0.05 * math.sin(3 * lon + 2.1 * lat) + 0.03 * math.sin(5 * lon - 1.3)
    v.co = V((math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)))
pl.data.update()
shade_smooth(pl, 80)
P = [pl]

# ---------- gezicht (-Y) ----------
for sx in (-1, 1):
    d = V((sx * 0.31, -1, 0.2))
    P.append(on_sphere(sphere(1.0, seg=12, rings=8, material=white, scale=(0.165, 0.2, 0.06)), d, sink=0.02))
    P.append(on_sphere(sphere(1.0, seg=10, rings=7, material=dark, scale=(0.115, 0.145, 0.05)), V((sx * 0.29, -1, 0.17)), R=1.04, sink=0.0))
    P.append(on_sphere(sphere(1.0, seg=6, rings=4, material=white, scale=(0.04, 0.048, 0.02)), V((sx * 0.29 + 0.035, -1, 0.24)), R=1.085))
    P.append(on_sphere(sphere(1.0, seg=6, rings=3, material=white, scale=(0.02, 0.02, 0.012)), V((sx * 0.29 - 0.04, -1, 0.115)), R=1.08))
    # blosjes
    P.append(on_sphere(sphere(1.0, seg=8, rings=5, material=pink, scale=(0.11, 0.065, 0.025)), V((sx * 0.58, -1, -0.06)), sink=0.012))
# open lach: D-vorm met tongetje
mouth_poly = [(0.19 * math.cos(math.pi * i / 6), -0.09 + 0.012 * math.sin(math.pi * i / 6)) for i in range(7)]
mouth_poly += [(-0.19 * math.cos(math.pi * i / 10), -0.09 - 0.17 * math.sin(math.pi * i / 10)) for i in range(1, 10)]
P.append(decal(mouth_poly, 1.012, 0.99, dark, 'mouth'))
tongue = [(0.09 * math.cos(math.pi * i / 8), -0.215 + 0.055 * math.sin(math.pi * i / 8)) for i in range(9)]
tongue += [(-0.09 + 0.18 * i / 6, -0.215 - 0.03 * math.sin(math.pi * i / 6)) for i in range(1, 6)]
P.append(decal(tongue, 1.018, 1.0, pink, 'tongue'))
planet = part(P, 'planet', (0, 0, 0))

# ---------- ring: binnen 1.3, buiten 1.8, gekleurde banden, 20 graden gekanteld rond X ----------
RSEG = 40
H = 0.022
mats_r = [pink, gold, purple, white]
bm = bmesh.new()
def ring_verts(r, z):
    return [bm.verts.new((r * math.cos(TAU * i / RSEG), r * math.sin(TAU * i / RSEG), z)) for i in range(RSEG)]
def quads(A, Bv, mi, flipit=False):
    for i in range(RSEG):
        j = (i + 1) % RSEG
        f = bm.faces.new((A[i], A[j], Bv[j], Bv[i]) if not flipit else (A[i], Bv[i], Bv[j], A[j]))
        f.material_index = mi
# stukken ring: (straal, materiaal van de band die hier begint); laatste = buitenrand
pieces = [[(1.30, 0), (1.42, 1), (1.45, 2), (1.60, None)], [(1.635, 1), (1.72, 3), (1.80, None)]]
for pc in pieces:
    tops, bots = [], []
    for (r, mi) in pc:
        tops.append(ring_verts(r, H)); bots.append(ring_verts(r, -H))
    # binnen- en buitenrand
    quads(bots[0], tops[0], pc[0][1])
    quads(tops[-1], bots[-1], pc[-2][1])
    for k in range(len(pc) - 1):
        mi = pc[k][1]
        quads(tops[k], tops[k + 1], mi, flipit=False)
        quads(bots[k], bots[k + 1], mi, flipit=True)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
ring = link_bm(bm, 'ring')
for m in mats_r:
    ring.data.materials.append(m)
T(ring, rot=(math.radians(20), 0, 0))
ring = part([ring], 'ring', (0, 0, 0))
shade_smooth(ring, 30)

# ---------- maantje (r 0.22) met kratertjes en een slaperig gezichtje ----------
MC = V((1.6, 0, 1.0))
M = [ico(0.22, sub=2, material=moon_m, smooth=True)]
rnd = random.Random(3)
for (d, rc) in [((0.5, -0.6, 0.6), 0.06), ((0.9, 0.2, -0.2), 0.075), ((-0.3, 0.5, 0.8), 0.055), ((-0.6, 0.3, -0.7), 0.06)]:
    c = crater(rc, material=moon_m, seg=8, h=0.016)
    M.append(on_sphere(c, d, R=0.22, sink=0.004))
# gezichtje naar -Y (gesloten lachende oogjes ^ ^ en mini-glimlach)
for sx in (-1, 1):
    arc = [V((sx * 0.065 + 0.035 * math.cos(math.pi * t / 4), 0, 0.035 + 0.03 * math.sin(math.pi * t / 4))) for t in range(5)]
    pts = [(V((p.x, -0.3, p.z)) - V((0, 0, 0))).normalized() * 0.225 for p in [V((a.x, -0.3, a.z)) for a in arc]]
    M.append(tube(pts, r=0.011, seg=5, material=dark, smooth=True))
    M.append(on_sphere(sphere(1.0, seg=8, rings=5, material=pink, scale=(0.032, 0.02, 0.008)), V((sx * 0.13, -0.3, -0.02)), R=0.22, sink=0.002))
sm = [V((0.04 * math.cos(math.pi + math.pi * t / 4), -0.3, -0.035 + 0.025 * math.sin(math.pi + math.pi * t / 4))).normalized() * 0.224 for t in range(5)]
M.append(tube(sm, r=0.01, seg=5, material=dark, smooth=True))
moon = part(M, 'moon', (0, 0, 0))
T(moon, loc=(0, 0, 0))
moon.location = MC
shade_smooth(moon, 60)

report()
notes = ('parts (pivot): planet (sphere radius exactly 1.0 centred on its origin 0,0,0; banded purple/pink/gold; face with big eyes, blush and an open smile on the -Y side, face features stick out up to ~0.09 beyond r=1); '
         'ring (origin 0,0,0 = planet centre, flat banded ring r 1.30-1.80 with a small gap at 1.60-1.635, tilted 20 deg around X (front edge low), tilt baked into the mesh, rotation zero); '
         'moon (radius 0.22, origin at its centre, placed at x=1.6 z=1.0; craters + sleepy smiling face toward -Y). '
         'Materials: purple, pink, gold, eye_white, pupil, moon.')
finish('chars', 'planet', kind='char', footprint=1.0, grounded=False, notes=notes)
if os.environ.get('VIEWS'):
    sys.path.insert(0, '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad')
    from views import views
    views('planet', dirs=((0, -1, 0.25), (0.3, -1, 0.9), (1, -0.3, 0.3)))
