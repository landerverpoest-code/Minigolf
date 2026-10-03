import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

STAR = mat('starfish', '#ff6f3c', rough=0.7)
DOTS = mat('starfish_dots', '#ffe0a8', rough=0.7)
SHELL = mat('shell', '#fbecd8', rough=0.45)
PINK = mat('shell_pink', '#f48a9a', rough=0.45)

# --- zeester: ster met bolle armen ---
R = 0.11
vs = [Vector((0, 0, R * 0.36))]; fs = []
outer = []
for k in range(10):
    a = 0.3 + math.pi * k / 5
    if k % 2 == 0:
        outer.append(len(vs)); vs.append(Vector((math.cos(a) * R * 0.5, math.sin(a) * R * 0.5, R * 0.24)))
        outer.append(len(vs)); vs.append(Vector((math.cos(a) * R, math.sin(a) * R, R * 0.06)))
    else:
        outer.append(len(vs)); vs.append(Vector((math.cos(a) * R * 0.46, math.sin(a) * R * 0.46, R * 0.08)))
# extra breedtepunten naast de arm-middens
n = len(outer); ring = []
for i in range(n):
    ring.append(outer[i])
bot = []
for vi in ring:
    p = vs[vi]; bot.append(len(vs)); vs.append(Vector((p.x * 0.92, p.y * 0.92, 0)))
for i in range(n):
    j = (i + 1) % n
    fs.append((0, ring[i], ring[j]))
    fs.append((ring[j], ring[i], bot[i], bot[j]))
fs.append(tuple(reversed(bot)))
star = mesh_obj(vs, fs, STAR, 'star')
# arm-middens wat verbreden: valleipunten (k oneven) iets naar buiten trekken
for k in range(5):
    a = 0.3 + 2 * math.pi * k / 5
    d = 0.052
    cone(0.009, 0.008, loc=(math.cos(a) * d, math.sin(a) * d, R * 0.25 + 0.002), verts=4, material=DOTS)
cone(0.012, 0.008, loc=(0, 0, R * 0.36 + 0.001), verts=5, material=DOTS)
# --- sint-jakobsschelp met ribben (gestreept) ---
N = 10; SR = 0.065
vs = [Vector((0, -SR * 0.15, 0.006))]; fs = []; fm = []
mid, arc = [], []
for i in range(N + 1):
    a = math.pi * (0.1 + 0.8 * i / N)
    rib = 0.006 if i % 2 == 0 else 0.0
    mid.append(len(vs)); vs.append(Vector((math.cos(a) * SR * 0.5, math.sin(a) * SR * 0.5 - SR * 0.1, 0.022 + rib)))
    arc.append(len(vs)); vs.append(Vector((math.cos(a) * SR, math.sin(a) * SR * 0.92 - SR * 0.1, 0.004 + rib * 0.6)))
for i in range(N):
    fs.append((0, mid[i], mid[i + 1])); fm.append(i % 2)
    fs.append((mid[i], arc[i], arc[i + 1], mid[i + 1])); fm.append(i % 2)
e = len(vs); vs += [Vector((-SR * 0.3, -SR * 0.25, 0.004)), Vector((SR * 0.3, -SR * 0.25, 0.004))]
fs.append((0, arc[-1], e)); fm.append(0); fs.append((0, e + 1, arc[0])); fm.append(0)
sc = mesh_obj(vs, fs, mats=[PINK, SHELL], face_mats=fm, name='scallop')
place(sc, loc=(0.135, 0.06, 0), rot=(0, 0, 2.4))
# --- torenschelp: getrapte windingen in twee tinten, op zijn kant ---
prof = [(0.0, 0.0), (0.021, 0.006), (0.026, 0.02), (0.017, 0.033), (0.019, 0.037), (0.014, 0.05), (0.011, 0.055),
        (0.009, 0.066), (0.0, 0.082)]
bm = [1, 0, 0, 1, 0, 0, 1, 0]
conch = lathe(prof, verts=6, mats=[SHELL, PINK], band_mats=bm, name='conch', phase=0.3)
ap = sphere(0.016, loc=(0.0, -0.017, 0.016), seg=5, rings=3, material=PINK, scale=(1, 0.4, 1.25), smooth=False)
cj = join([conch, ap], 'conch')
place(cj, rot=(math.pi / 2 - 0.12, 0, 2.3), loc=(-0.13, 0.08, 0.02))
join_all('starfish_shells')
report()
finish('water', 'starfish_shells', kind='edge', footprint=0.16,
       notes='Oranje zeester met lichte bultjes, gestreepte sint-jakobsschelp en een spiraalschelp')
closeup('starfish_shells')
