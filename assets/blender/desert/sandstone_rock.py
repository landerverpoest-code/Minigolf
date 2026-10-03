import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

C1 = mat('rock_terracotta', '#d4834a', rough=0.9)
C2 = mat('rock_sandstone', '#e8b679', rough=0.9)
C3 = mat('rock_red', '#b5623a', rough=0.9)
SAND = mat('sand', '#e6c48a', rough=0.95)
rnd = random.Random(14)

# lagen: (straal, dikte, materiaal) van onder naar boven; zachte lagen springen in
layers = [(1.3, 0.5, C3), (1.12, 0.26, C2), (1.2, 0.42, C1), (0.92, 0.22, C2), (1.0, 0.48, C3), (0.78, 0.2, C2),
          (0.88, 0.36, C1), (1.08, 0.2, C3)]
NV = 10
ph = rnd.uniform(0, 6.28)
def outline(k):
    a = 2 * math.pi * k / NV
    return 1 + 0.22 * math.sin(2 * a + ph) + 0.12 * math.sin(3 * a + 1.0) + rnd.uniform(-0.06, 0.06)
z = 0.0
for i, (r, h, m) in enumerate(layers):
    prof = [(r, z), (r * 0.9, z + h * 0.85), (r * 0.86, z + h)] if h > 0.3 else [(r, z), (r * 0.9, z + h)]
    o = lathe(prof, verts=NV, material=m)
    drift = Vector((0.05 * i, -0.03 * i, 0))
    for k, v in enumerate(o.data.vertices):
        kk = k % NV
        f = outline(kk)
        v.co.x = v.co.x * f * 1.25 + drift.x; v.co.y = v.co.y * f * 0.9 + drift.y
        v.co.z += v.co.x * 0.06   # scheve lagen
    if i == len(layers) - 1:
        bev(o, 0.05)
    z += h
# afgebroken brokken aan de voet en een losse zuil
for k in range(5):
    a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(1.5, 2.0)
    rock(rnd.uniform(0.18, 0.38), loc=(math.cos(a) * d * 1.1, math.sin(a) * d * 0.85, 0.08), scale=(1.3, 1.0, 0.8), seed=k + 3, jitter=0.2,
         material=[C1, C2, C3][k % 3], rot_z=a)
pz = 0.0
for i, (r, h, m) in enumerate([(0.32, 0.3, C3), (0.25, 0.25, C2), (0.3, 0.32, C1), (0.36, 0.12, C2)]):
    lathe([(r, pz), (r * 0.95, pz + h)], verts=6, material=m, loc=(1.95, -0.6, 0), jitter=0.08, seed=i)
    pz += h
# zand rond de voet
dune = lathe([(1.75, 0.0), (1.45, 0.1), (1.2, 0.14)], verts=10, material=SAND, jitter=0.1, seed=3, cap0=False, cap1=True)
place(dune, scale=(1.25, 0.9, 1.0))
join_all('sandstone_rock')
report()
finish('desert', 'sandstone_rock', kind='scatter', footprint=1.5,
       notes='Gelaagde, uitgesleten mesa-rots in terracotta en zandsteen met losse brokken en een kleine rotszuil')
closeup('sandstone_rock')
