import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

G1 = mat('pear_green', '#62a94a', rough=0.7)
G2 = mat('pear_green_blue', '#4e9a5a', rough=0.7)
FRUIT = mat('pear_fruit', '#e2336f', rough=0.5)
YEL = mat('flower_yellow', '#ffcc33', rough=0.6)
SAND = mat('sand', '#e6c48a', rough=0.95)
rnd = random.Random(5)


def paddle(base, up, normal, L, W, T, material):
    up = Vector(up).normalized(); nrm = Vector(normal); nrm = (nrm - up * nrm.dot(up)).normalized(); side = up.cross(nrm)
    c = Vector(base) + up * (L / 2)
    vs = [c + nrm * T / 2, c - nrm * T / 2]
    n = 8
    for k in range(n):
        a = 2 * math.pi * k / n
        vs.append(c + up * (-math.cos(a) * L / 2) + side * (math.sin(a) * W / 2))
    fs = []
    for k in range(n):
        a, b = 2 + k, 2 + (k + 1) % n
        fs.append((0, a, b)); fs.append((1, b, a))
    o = mesh_obj(vs, fs, material, 'pad')
    fix_normals(o)
    # rim punten (voor het aanhechten): bovenkant
    def rim(a):
        return c + up * (-math.cos(a) * L / 2) + side * (math.sin(a) * W / 2)
    return o, rim, up, nrm


pads = []
def P(base, up, nrm, L, k, fruits=0):
    o, rim, u, n = paddle(base, up, nrm, L, L * 0.8, L * 0.15, G1 if k % 2 == 0 else G2)
    pads.append(rim)
    for j in range(fruits):
        ang = math.pi + (j - (fruits - 1) / 2) * 0.55
        sphere(0.03, loc=rim(ang) + u * 0.022, seg=4, rings=3, material=FRUIT, scale=(1, 1, 1.3))
    return rim, u, n

# hoofdschijf (naar voren, -Y)
r0, u0, n0 = P((0, 0, 0), (0.0, 0.0, 1), (0, -1, 0), 0.34, 0)
# twee schijven op de bovenrand, in een V
r1, u1, n1 = P(r0(math.pi * 0.8) - Vector((0, 0, 0.03)), (-0.55, 0.0, 1), (0.2, -1, 0), 0.27, 1, fruits=2)
r2, u2, n2 = P(r0(math.pi * 1.2) - Vector((0, 0, 0.03)), (0.6, 0.05, 1), (-0.3, -1, 0.0), 0.28, 1)
# derde laag
r3, u3, n3 = P(r2(math.pi * 0.95) - u2 * 0.03, (0.15, 0.1, 1), (-0.1, -1, 0), 0.22, 0, fruits=3)
# zijschijf vanaf de grond
r4, u4, n4 = P((0.12, 0.1, 0), (0.6, 0.5, 0.8), (0.8, -0.6, 0), 0.24, 1, fruits=1)
r5, u5, n5 = P((-0.1, 0.12, 0), (-0.5, 0.6, 0.8), (-0.8, -0.4, 0), 0.22, 0)
# geel bloemetje
cone(0.035, 0.04, loc=r1(math.pi * 1.2) + u1 * 0.02, verts=5, material=YEL)
# zandhoopje
lathe([(0.24, 0.0), (0.18, 0.025), (0.0, 0.035)], verts=7, material=SAND, jitter=0.1, seed=2)
join_all('prickly_pear')
report()
finish('desert', 'prickly_pear', kind='edge', footprint=0.3, notes='Schijfcactus (vijgcactus) met roze vruchten en een geel bloemetje')
closeup('prickly_pear')
