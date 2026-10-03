import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

G1 = mat('bush_leaf', '#2c8f3c', rough=0.6)
G2 = mat('bush_leaf_light', '#62c340', rough=0.6)
RED = mat('flower_red', '#ec2f4b', rough=0.6)
ORG = mat('flower_orange', '#ff9426', rough=0.6)
YEL = mat('flower_yellow', '#ffdc4a', rough=0.6)
rnd = random.Random(6)

# kern
core = ico(0.3, loc=(0, 0, 0.28), sub=1, material=G1, scale=(1.2, 1.1, 0.9), jitter=0.04, seed=2)
# grote bladeren in drie kransen
rings = [(8, 0.3, 0.62, 0.62, 0.0), (7, 0.6, 0.7, 0.72, 0.4), (8, 0.9, 0.72, 0.72, 0.4), (6, 1.25, 0.62, 0.62, 0.9)]  # n, pitch, lengte, breedte..., hoogte-offset
k = 0
for ri, (n, pitch, L, W, off) in enumerate(rings):
    for i in range(n):
        yaw = 2 * math.pi * i / n + ri * 0.45 + rnd.uniform(-0.15, 0.15)
        p = pitch + rnd.uniform(-0.1, 0.1)
        d = Vector((math.cos(yaw) * math.cos(p), math.sin(yaw) * math.cos(p), math.sin(p)))
        base = Vector((math.cos(yaw) * 0.1, math.sin(yaw) * 0.1, 0.12 + 0.14 * ri))
        lf = leaf(base, d, length=L * rnd.uniform(0.85, 1.1), width=0.24 * rnd.uniform(0.9, 1.15), curl=0.22, fold=0.05,
                  material=G1 if (k % 3) else G2, segs=3)
        shade_smooth(lf, 80)
        k += 1
# hibiscusbloemen
def flower(c, n_dir, col, s=1.0):
    c = Vector(c); nd = Vector(n_dir).normalized()
    sd = nd.cross(UP); sd = sd.normalized() if sd.length > 1e-3 else Vector((1, 0, 0))
    up2 = sd.cross(nd).normalized()
    vs = [c]; fs = []
    for j in range(10):
        a = 2 * math.pi * j / 10
        r = (0.12 if j % 2 == 0 else 0.085) * s
        vs.append(c + (sd * math.cos(a) + up2 * math.sin(a)) * r + nd * (0.05 * s if j % 2 == 0 else 0.02 * s))
    for j in range(10):
        fs.append((0, 1 + j, 1 + (j + 1) % 10))
    f = mesh_obj(vs, fs, col, 'flower')
    st = tube([c, c + nd * 0.1 * s], [0.015, 0.01], verts=3, material=YEL)
    return f
spots = []
for j, (a, h, rr, col) in enumerate([(-0.9, 0.8, 0.36, RED), (2.6, 0.7, 0.4, ORG), (1.3, 0.95, 0.25, RED), (-2.2, 0.55, 0.45, RED), (0.4, 0.62, 0.45, ORG), (-1.6, 0.85, 0.33, ORG), (3.4, 0.5, 0.5, RED), (2.0, 0.6, 0.48, RED)]):
    spots.append(((math.cos(a) * rr, math.sin(a) * rr, h), (math.cos(a) * 0.8, math.sin(a) * 0.8, 0.6), col))
for c, nd, col in spots:
    flower(c, nd, col, s=rnd.uniform(0.9, 1.1))
join_all('tropical_bush')
report()
finish('water', 'tropical_bush', kind='scatter', footprint=0.6,
       notes='Struik met grote tropische bladeren in twee groentinten en rode/oranje hibiscusbloemen')
closeup('tropical_bush')
