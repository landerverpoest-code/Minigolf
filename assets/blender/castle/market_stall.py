import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood', '#9a6538', rough=0.8)
red = mat('cloth_red', '#c0392f', rough=0.85)
cream = mat('cloth_cream', '#f1e6c8', rough=0.85)
green = mat('cabbage', '#6aa83a', rough=0.8)
yellow = mat('bread', '#e0a640', rough=0.8)

rnd = random.Random(2)
parts = []
W, D = 1.9, 0.85
TZ = 0.88
# toonbank met planken voorkant
parts.append(box((W, D, 0.07), loc=(0, 0, TZ), material=wood))
for k in range(4):
    x = -W / 2 + (k + 0.5) * W / 4
    parts.append(box((W / 4 - 0.03, 0.05, TZ - 0.05), loc=(x, -D / 2 + 0.02, (TZ - 0.05) / 2), material=wood))
# palen (achter hoger: schuin dak)
for sx in (-1, 1):
    parts.append(box((0.09, 0.09, 2.0), loc=(sx * (W / 2 - 0.02), -D / 2 + 0.02, 1.0), material=wood))
    parts.append(box((0.09, 0.09, 2.4), loc=(sx * (W / 2 - 0.02), D / 2 - 0.02, 1.2), material=wood))
# luifel: gestreept doek, schuin, met geschulpte voorrand
A0 = Vector((0, D / 2 + 0.05, 2.42)); A1 = Vector((0, -D / 2 - 0.45, 1.98))
n = 7
for k in range(n):
    x = -W / 2 - 0.08 + (k + 0.5) * (W + 0.16) / n
    pl = plank(Vector((x, A0.y, A0.z)), Vector((x, A1.y, A1.z)), w=(W + 0.16) / n + 0.005, t=0.04, up=(0, 0, 1), material=red if k % 2 == 0 else cream)
    parts.append(pl)
    sc = prism([(-(W + 0.16) / n / 2, 0), ((W + 0.16) / n / 2, 0), (0, -0.2)], 0.03, material=red if k % 2 == 0 else cream)
    xform(sc, loc=(x, A1.y - 0.01, A1.z + 0.01))
    parts.append(sc)
# kratten met waren op de toonbank
def crate(cx, cy, cz, w=0.5, d=0.38, h=0.2):
    out = [box((w, d, 0.03), loc=(cx, cy, cz + 0.015), material=wood)]
    for sy in (-1, 1):
        out.append(box((w, 0.03, h), loc=(cx, cy + sy * (d / 2 - 0.015), cz + h / 2), material=wood))
    for sx in (-1, 1):
        out.append(box((0.03, d, h), loc=(cx + sx * (w / 2 - 0.015), cy, cz + h / 2), material=wood))
    return out
def heap(cx, cy, cz, m, r, n, seed, seg=6):
    rr = random.Random(seed)
    out = []
    for k in range(n):
        s_ = sphere(r, seg=seg, rings=4, material=m)
        smooth(s_, 85)
        xform(s_, loc=(cx + rr.uniform(-0.13, 0.13), cy + rr.uniform(-0.08, 0.08), cz + r * 0.8 + rr.uniform(0, 0.05)))
        out.append(s_)
    return out
parts += crate(-0.55, 0.0, TZ + 0.035)
parts += heap(-0.55, 0.0, TZ + 0.1, red, 0.085, 4, 1, seg=5)           # appels
parts += crate(0.05, 0.05, TZ + 0.035)
for k in range(3):                                               # broden
    b = sphere(0.1, seg=6, rings=4, material=yellow, scale=(1.5, 0.8, 0.6))
    smooth(b, 85)
    xform(b, rot=(0, 0, rnd.uniform(-20, 20)), loc=(0.05 + (k - 1) * 0.15, 0.05 + rnd.uniform(-0.05, 0.05), TZ + 0.17 + (0.05 if k == 1 else 0)))
    parts.append(b)
# kazen
for k, (x, y) in enumerate(((0.6, -0.1), (0.72, 0.15))):
    c = cyl(0.13, 0.1, loc=(x, y, TZ + 0.09), verts=8, material=yellow)
    smooth(c, 50)
    parts.append(c)
# krat met kolen op de grond + zakken
parts += crate(0.55, -0.75, 0.0, w=0.55, d=0.42, h=0.26)
for k in range(3):
    cb = ico(0.11, sub=1, material=green)
    jitter(cb, 0.015, seed=k)
    smooth(cb, 85)
    xform(cb, loc=(0.45 + k * 0.11, -0.75 + (k % 2) * 0.06 - 0.03, 0.27))
    parts.append(cb)
for k, (x, y) in enumerate(((-0.75, -0.7), (-1.05, -0.45))):
    sk = ico(0.22, sub=1, material=cream, scale=(1.0, 0.9, 1.25))
    jitter(sk, 0.03, seed=k + 5)
    xform(sk, loc=(x, y, 0.26))
    smooth(sk, 70)
    parts.append(sk)
    parts.append(cone(0.1, 0.12, loc=(x, y, 0.56), verts=5, material=cream))
o = join(parts, 'market_stall')
report()
finish('castle', 'market_stall', kind='scatter', footprint=1.2, notes='houten marktkraam met rood/crème gestreepte luifel en geschulpte rand; kratten met appels en broden, kazen, krat kool en jute zakken')
