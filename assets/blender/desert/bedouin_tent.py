import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

TERRA = mat('tent_terracotta', '#c4533a', rough=0.85)
CREAM = mat('tent_cream', '#f0dcb0', rough=0.85)
WOOD = mat('tent_wood', '#6e4a2c', rough=0.85)
TURQ = mat('turquoise', '#27bfb0', rough=0.6)
GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.5)
rnd = random.Random(2)

W, D, H = 1.35, 1.0, 1.85     # halve breedte, halve diepte, nokhoogte
NX, NY = 10, 3
def Z(x, y):
    t = abs(x) / W
    z = H * (1 - t) ** 1.25
    sag = 0.07 * math.sin(math.pi * (y + D) / (2 * D)) * (1 - t)
    return max(z - sag, 0.0)
vs, fs, fm = [], [], []
for j in range(NY + 1):
    y = -D + 2 * D * j / NY
    for i in range(NX + 1):
        x = -W + 2 * W * i / NX
        vs.append(Vector((x, y, Z(x, y) + (0.04 if i in (0, NX) else 0))))
for j in range(NY):
    for i in range(NX):
        a = j * (NX + 1) + i
        fs.append((a, a + 1, a + NX + 2, a + NX + 1)); fm.append(i % 2)
roof = mesh_obj(vs, fs, mats=[TERRA, CREAM], face_mats=fm, name='roof')
fix_normals(roof)
# achterwand
back = [Vector((-W, D, 0))] + [Vector((-W + 2 * W * i / NX, D, Z(-W + 2 * W * i / NX, D))) for i in range(NX + 1)] + [Vector((W, D, 0))]
mesh_obj(back[1:-1], [tuple(range(NX + 1))], CREAM, 'back')
# turkooise zoom langs de onderrand en voorrand
for s in (-1, 1):
    tube([(s * W, -D, 0.06), (s * W, D, 0.06)], [0.035, 0.035], verts=4, material=TURQ)
front = [(-W + 2 * W * i / NX, -D - 0.01, Z(-W + 2 * W * i / NX, -D) + 0.03) for i in range(NX + 1)]
tube(front, [0.03] * len(front), verts=4, material=TURQ)
# opengeslagen voorflappen
for s in (-1, 1):
    p_top = Vector((0, -D, H - 0.05)); p_low = Vector((s * W, -D, 0.05)); p_out = Vector((s * (W * 0.75), -D - 0.55, 0.15))
    mesh_obj([p_top, p_low, p_out], [(0, 1, 2)], CREAM if s < 0 else TERRA, 'flap')
    tube([p_out, p_out + Vector((s * 0.05, -0.05, -0.15))], [0.02, 0.015], verts=3, material=WOOD)
# palen + nokpaal
for y in (-D, D):
    cyl(0.045, H + 0.2, loc=(0, y, (H + 0.2) / 2), verts=6, material=WOOD)
    sphere(0.06, loc=(0, y, H + 0.22), seg=6, rings=4, material=GOLD)
cyl(0.035, 2 * D, loc=(0, 0, H + 0.02), rot=(math.pi / 2, 0, 0), verts=5, material=WOOD)
# scheerlijnen
for y in (-D, D):
    for s in (-1, 1):
        a = Vector((0, y, H + 0.1)); b = Vector((s * 0.4, y + (0.9 if y > 0 else -0.9), 0.0))
        tube([a, b], [0.008, 0.008], verts=3, material=CREAM)
        cyl(0.025, 0.12, loc=b + Vector((0, 0, 0.04)), verts=4, material=WOOD)
# lantaarntje aan de voorpaal
lan = lathe([(0.0, 1.25), (0.07, 1.28), (0.08, 1.38), (0.04, 1.46), (0.0, 1.5)], verts=6, material=GOLD, loc=(0.09, -D - 0.06, 0))
# kleed voor de tent met rand
RX, RY0, RY1 = 0.85, -D - 1.4, -D - 0.1
nu, nv = 5, 4
vs, fs, fm = [], [], []
for j in range(nv + 1):
    for i in range(nu + 1):
        u = [0, 0.1, 0.35, 0.65, 0.9, 1.0][i]; v = [0, 0.1, 0.5, 0.9, 1.0][j]
        vs.append(Vector((-RX + 2 * RX * u, RY0 + (RY1 - RY0) * v, 0.015)))
for j in range(nv):
    for i in range(nu):
        a = j * (nu + 1) + i
        fs.append((a, a + 1, a + nu + 2, a + nu + 1))
        border = i in (0, nu - 1) or j in (0, nv - 1)
        fm.append(2 if border else (1 if i == 2 and j in (1, 2) else 0))
mesh_obj(vs, fs, mats=[TERRA, GOLD, TURQ], face_mats=fm, name='rug')
for x, m in ((-0.45, TURQ), (0.45, GOLD)):
    box((0.42, 0.32, 0.14), loc=(x, -D - 0.35, 0.09), rot=(0, 0, rnd.uniform(-0.3, 0.3)), material=m, bevel=0.05)
# theepotje
pot = lathe([(0.0, 0.0), (0.08, 0.01), (0.09, 0.06), (0.05, 0.12), (0.02, 0.15), (0.0, 0.16)], verts=7, material=GOLD, loc=(0.05, -D - 0.85, 0.02))
tube([(0.12, -D - 0.85, 0.07), (0.2, -D - 0.85, 0.12)], [0.015, 0.01], verts=3, material=GOLD)
join_all('bedouin_tent')
report()
finish('desert', 'bedouin_tent', kind='scatter', footprint=1.4,
       notes='Gestreepte bedoeïenententtent (terracotta/crème) met palen, opengeslagen flappen, scheerlijnen, lantaarntje en een kleed met kussens en theepot voor de ingang (-Y)')
closeup('bedouin_tent')
