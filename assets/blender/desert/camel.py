import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

FUR = mat('camel_fur', '#d8a463', rough=0.85)
DARK = mat('camel_dark', '#6a4528', rough=0.8)
RED = mat('blanket_red', '#c8323a', rough=0.75)
GOLD = mat('blanket_gold', '#f5c542', rough=0.5, metal=0.2)
TURQ = mat('turquoise', '#27bfb0', rough=0.5)

# kameel loopt langs +X, kop draait iets naar de kijker (-Y)
BZ = 1.2; BL, BW, BH = 0.78, 0.36, 0.36
body = sphere(1.0, loc=(0, 0, BZ), seg=10, rings=7, material=FUR, scale=(BL, BW, BH))
hump = sphere(1.0, loc=(-0.08, 0, BZ + 0.3), seg=8, rings=5, material=FUR, scale=(0.34, 0.27, 0.3))
# nek + kop
neck = tube([(0.6, 0, BZ + 0.05), (0.82, -0.02, BZ + 0.2), (0.95, -0.05, BZ + 0.5), (1.0, -0.08, BZ + 0.72)], [0.17, 0.14, 0.12, 0.11], verts=6, material=FUR)
shade_smooth(neck, 60)
HX, HY, HZ = 1.06, -0.12, BZ + 0.8
head = sphere(1.0, loc=(HX, HY, HZ), seg=8, rings=5, material=FUR, scale=(0.2, 0.13, 0.13))
snout = sphere(1.0, loc=(HX + 0.17, HY - 0.04, HZ - 0.04), seg=7, rings=4, material=FUR, scale=(0.13, 0.1, 0.09))
for s in (-1, 1):
    cone(0.035, 0.09, loc=(HX - 0.1, HY + s * 0.08, HZ + 0.12), rot=(s * 0.4, -0.3, 0), verts=4, material=FUR)    # oren
for s in (-1, 1):
    sphere(0.028, loc=(HX + 0.06, HY + s * 0.115, HZ + 0.04), seg=5, rings=3, material=DARK)   # ogen
    box((0.03, 0.015, 0.012), loc=(HX + 0.27, HY - 0.04 + s * 0.04, HZ - 0.02), material=DARK)  # neusgaten
box((0.12, 0.02, 0.015), loc=(HX + 0.22, HY - 0.135, HZ - 0.09), material=DARK)                # mond
# poten
for x in (0.42, -0.45):
    for s in (-1, 1):
        y = s * 0.17
        tube([(x, y, BZ - 0.12), (x + 0.02, y, 0.65), (x - 0.01, y, 0.36), (x + 0.01, y, 0.06)], [0.085, 0.06, 0.055, 0.05], verts=5, material=FUR)
        cyl(0.075, 0.07, loc=(x + 0.03, y, 0.035), verts=6, material=DARK)          # hoef
# staart
tube([(-0.76, 0, BZ + 0.05), (-0.82, 0, BZ - 0.15), (-0.8, 0, BZ - 0.38)], [0.035, 0.03, 0.02], verts=4, material=FUR)
cone(0.05, 0.14, loc=(-0.8, 0, BZ - 0.45), rot=(math.pi, 0, 0), verts=5, material=DARK)
# zadeldeken: drapeert over het lijf (ellips-doorsnede), met strepen en kwastjes
X0, X1 = -0.42, 0.3
THS = [-105, -97, -88, -55, -20, 20, 55, 88, 97, 105]
NU, NV = 4, len(THS) - 1
vs, fs, fm = [], [], []
for j in range(NV + 1):
    th = math.radians(THS[j])
    for i in range(NU + 1):
        x = X0 + (X1 - X0) * i / NU
        f = math.sqrt(max(0.05, 1 - (x / BL) ** 2))
        y = math.sin(th) * BW * f * 1.06
        z = BZ + math.cos(th) * BH * f * 1.06
        if abs(th) > math.radians(80):
            z -= (abs(th) - math.radians(80)) * 0.25
        vs.append(Vector((x, y, z)))
for j in range(NV):
    for i in range(NU):
        a = j * (NU + 1) + i
        fs.append((a, a + 1, a + NU + 2, a + NU + 1))
        fm.append(1 if j in (0, NV - 1) else (2 if j in (1, NV - 2) else (1 if i in (0, NU - 1) else 0)))
blanket = mesh_obj(vs, fs, mats=[RED, GOLD, TURQ], face_mats=fm, name='blanket')
fix_normals(blanket)
# kwastjes langs de onderrand
for s in (-1, 1):
    j = 0 if s < 0 else NV
    for i in range(NU + 1):
        p = vs[j * (NU + 1) + i]
        cone(0.03, 0.09, loc=p - Vector((0, 0, 0.05)), rot=(math.pi, 0, 0), verts=4, material=GOLD)
# zadel op de bult
seat = box((0.36, 0.3, 0.08), loc=(-0.08, 0, BZ + 0.6), material=RED, bevel=0.03)
for x in (-0.24, 0.08):
    cyl(0.03, 0.22, loc=(x, 0, BZ + 0.66), rot=(math.pi / 2, 0, 0), verts=5, material=GOLD)
join_all('camel')
report()
finish('desert', 'camel', kind='scatter', footprint=0.8,
       notes='Cartoon-dromedaris met rood-goud-turkooise zadeldeken met kwastjes en zadel; loopt langs +X, kop kijkt licht naar -Y')
closeup('camel')
