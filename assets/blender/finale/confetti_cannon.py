import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale'); from _deco import *

PURPLE = mat('royal_purple', '#5b2a86', rough=0.55)
CRIMSON = mat('crimson', '#b0213a', rough=0.55)
GOLD = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
WHITE = mat('marble', '#efe9f2', rough=0.35)
WOOD = mat('wood', '#8a5a34', rough=0.85)

# houten affuit met twee wielen, loop schuin omhoog naar -Y
box((0.3, 0.5, 0.08), loc=(0, 0.05, 0.16), material=WOOD)
for s in (-1, 1):
    prism([(-0.25, 0.12), (0.15, 0.12), (0.15, 0.42), (0.05, 0.42), (-0.25, 0.2)], 0.04, material=WOOD, axis='X', loc=(s * 0.13, 0, 0))
    w = cyl(0.17, 0.05, verts=7, material=GOLD, rot=(0, math.pi / 2, 0), loc=(s * 0.19, -0.02, 0.17))
# loop: gestreept (paars/goud ringen), trompetmond
barrel = lathe([(0.1, -0.15), (0.11, 0.0), (0.1, 0.2), (0.1, 0.3), (0.12, 0.42), (0.17, 0.5), (0.15, 0.5), (0.1, 0.42)], verts=6,
               mats=[PURPLE, GOLD], band_mats=[0, 1, 0, 1, 0, 1, 1], cap0=True, cap1=False)
T(barrel, rot=(55, 0, 0), loc=(0, 0.04, 0.38))
# confetti-uitbarsting: losse snippers in een kegel boven de mond
rnd = random.Random(5)
mouth = Vector((0, -0.38, 0.68))
dirn = Vector((0, -0.8, 0.6)).normalized()
for k in range(12):
    t = rnd.uniform(0.1, 1.0)
    side = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1) * 0.3, rnd.gauss(0, 1))) * 0.1 * (0.3 + t)
    p = mouth + dirn * t * 0.45 + side
    m = (CRIMSON, GOLD, WHITE, PURPLE)[k % 4]
    q = mesh_obj([(-0.03, 0, -0.018), (0.03, 0, -0.018), (0.03, 0, 0.018), (-0.03, 0, 0.018)], [(0, 1, 2, 3), (3, 2, 1, 0)], m, 'conf')
    T(q, rot=(rnd.uniform(0, 360), rnd.uniform(0, 360), rnd.uniform(0, 360)), loc=p)
# krullende serpentines
for k, (m, ph) in enumerate(((CRIMSON, 0.0), (GOLD, 2.1), (WHITE, 4.2))):
    pts = []
    for i in range(5):
        t = i / 4
        c = mouth + dirn * t * 0.55 + Vector((0, 0, 0.08 * t))
        u = Vector((1, 0, 0)); v = dirn.cross(u)
        r = 0.04 + 0.06 * t
        a = ph + t * 9
        pts.append(c + (u * math.cos(a) + v * math.sin(a)) * r)
    vs, fs = [], []
    for i, p in enumerate(pts):
        vs += [p - Vector((0, 0, 0.014)), p + Vector((0, 0, 0.014))]
    for i in range(len(pts) - 1):
        fs += [(2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1), (2 * i + 1, 2 * i + 3, 2 * i + 2, 2 * i)]
    mesh_obj(vs, fs, m, 'streamer')
# lont
tube([(0, 0.32, 0.36), (0.03, 0.38, 0.32), (0.05, 0.42, 0.36)], 0.012, verts=3, material=WHITE, cap0=False)
o = join_all('confetti_cannon')
report()
done('finale', 'confetti_cannon', kind='edge', footprint=0.38,
     notes='Confettikanon: paars-goud gestreepte loop met trompetmond op een houten affuit met gouden wieltjes, uitbarsting van rode/gouden/witte/paarse snippers, lontje; schiet naar -Y')
