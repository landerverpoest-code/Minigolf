import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert'); from _deco import *

SAND = mat('sand', '#e6c48a', rough=0.95)
WATER = mat('oasis_water', '#27bfb0', rough=0.08)
REED = mat('pear_green', '#62a94a', rough=0.7)
ROCK = mat('rock_sandstone', '#e8b679', rough=0.9)
FLOWER = mat('pear_fruit', '#e2336f', rough=0.5)

rnd = random.Random(6)
# zandige oever (ring) en waterspiegel, onregelmatige vorm
def shape(a):
    return 1 + 0.12 * math.sin(3 * a + 0.5) + 0.07 * math.sin(5 * a + 1.3)
N = 18
outer, inner, edge = [], [], []
for i in range(N):
    a = TAU * i / N; s = shape(a)
    outer.append(Vector((1.35 * s * math.cos(a), 1.05 * s * math.sin(a), 0.0)))
    edge.append(Vector((1.12 * s * math.cos(a), 0.86 * s * math.sin(a), 0.1)))
    inner.append(Vector((0.95 * s * math.cos(a), 0.72 * s * math.sin(a), 0.05)))
bank = loft([outer, edge, inner], material=SAND, closed=True, cap0=False, cap1=False)
flat(bank)
water = mesh_obj([p + Vector((0, 0, 0.012)) for p in inner] + [Vector((0, 0, 0.062))], [(i, (i + 1) % N, N) for i in range(N)], WATER, 'water')
fix_normals(water)
# zandsteentjes langs de rand
for k in range(7):
    a = k * TAU / 7 + 0.4; s = shape(a)
    c = chunk(0.13 + 0.05 * (k % 2), (1.3, 1.0, 0.7), cuts=4, seed=30 + k, material=ROCK, flat_bottom=0.3, base_sub=1)
    T(c, rot=(0, 0, k * 50), loc=(1.15 * s * math.cos(a), 0.9 * s * math.sin(a), 0.07))
# rietpollen (dunne gebogen sprieten met bruine sigaren)
def reed_clump(cx, cy, n, h):
    for i in range(n):
        a = rnd.uniform(0, TAU); r = rnd.uniform(0, 0.07)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        hh = h * rnd.uniform(0.7, 1.1)
        lean = Vector((math.cos(a), math.sin(a), 0)) * rnd.uniform(0.05, 0.18)
        top = Vector((x, y, hh)) + lean
        mesh_obj([(x - 0.025, y, 0.05), (x + 0.025, y, 0.05), top], [(0, 1, 2)], REED, 'blade')
        if i % 3 == 0:
            p = Vector((x, y, 0.05)).lerp(top, 0.82)
            cyl(0.022, 0.13, loc=p, verts=4, material=ROCK)
reed_clump(-0.95, 0.35, 9, 0.85)
reed_clump(0.85, 0.5, 7, 0.7)
reed_clump(0.2, -0.85, 6, 0.6)
# waterlelieblaadjes met een bloem
for k, (x, y, r) in enumerate(((-0.3, -0.2, 0.13), (0.15, 0.15, 0.11), (0.45, -0.25, 0.1))):
    pad = cyl(r, 0.012, verts=7, material=REED, loc=(x, y, 0.075))
    if k != 1:
        f = flower_head(R=0.06, rc=0.02, petals=6, cup=0.03, petal_mat=FLOWER, heart_mat=SAND)
        T(f, loc=(x, y, 0.085))
o = join_all('oasis_pond')
report()
done('desert', 'oasis_pond', kind='scatter', footprint=1.4,
     notes='Oasevijvertje: onregelmatige zandoever met turquoise waterspiegel, zandsteentjes langs de rand, drie rietpollen met lisdoddes, waterlelieblaadjes met roze bloemen')
