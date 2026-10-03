import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

bark = mat('bark', '#6e4a2c', rough=0.95)
wood = mat('wood_light', '#e6bd80', rough=0.8)
ring = mat('wood_ring', '#bf8a4e', rough=0.85)
leafm = mat('leaf', '#5aa832', rough=0.8)
cap = mat('cap_red', '#e0302a', rough=0.45)

FP = 0.32
SEG = 16
H = 0.46
prof = [(0.235, 0.0), (0.228, 0.05), (0.218, 0.14), (0.212, 0.3), (0.218, H - 0.03), (0.222, H),
        (0.19, H + 0.012), (0.15, H + 0.004), (0.105, H + 0.012), (0.065, H + 0.004), (0.028, H + 0.01), (0, H + 0.006)]
st = lathe(prof, seg=SEG, material=bark, cap_bottom=False)
st.data.materials.append(wood); st.data.materials.append(ring)
# wortels: lobben aan de voet, binnen de botsstraal blijven; bastgroeven
roots = [0.3, 1.9, 3.3, 4.8]
for v in st.data.vertices:
    r = Vector((v.co.x, v.co.y)).length
    if r < 1e-4:
        continue
    a = math.atan2(v.co.y, v.co.x)
    if v.co.z < H - 0.02:
        lobe = max(max(0, math.cos(a - ra)) ** 6 for ra in roots)
        t = max(0, 1 - v.co.z / 0.2)
        k = 1 + (0.3 * lobe * t * t)
        idx = round(a / (TAU / SEG))
        k *= 1 + (0.05 if idx % 2 else -0.04) * (1 - 0.5 * t)   # groeven in de bast
        v.co.x *= k; v.co.y *= k
for p in st.data.polygons:
    if p.normal.z > 0.8:
        rr = Vector((p.center.x, p.center.y)).length
        p.material_index = 2 if (0.15 < rr < 0.19 or 0.065 < rr < 0.105 or rr < 0.028) else 1
# top iets scheef afgezaagd
bend(st, lambda c: (c.x, c.y, c.z + (0.03 * c.x / 0.25 if c.z > H - 0.04 else 0)))
smooth(st, 25)
parts = [st]
# wortels die net de grond in duiken
for i, ra in enumerate(roots):
    p0 = Vector((0.17 * math.cos(ra), 0.17 * math.sin(ra), 0.17))
    p1 = Vector((0.28 * math.cos(ra), 0.28 * math.sin(ra), -0.01))
    parts.append(rod(p0, p1, 0.06, 0.03, verts=6, material=bark))
# scheutje met twee blaadjes op de rand
p0 = Vector((0.1, 0.12, H - 0.005))
p1 = p0 + Vector((0.01, 0.0, 0.11))
parts.append(rod(p0, p1, 0.008, 0.005, verts=3, material=leafm))
for k, a in enumerate((20, 200)):
    l = leaf(0.085, 0.05, 0.01, material=leafm)
    xform(l, rot=(30, 0, a), loc=p1)
    parts.append(l)
# twee paddenstoeltjes tegen de voet
for (a, h, R) in ((5.45, 0.085, 0.04), (5.85, 0.055, 0.028)):
    base = Vector((0.235 * math.cos(a), 0.235 * math.sin(a), 0.0))
    s_ = lathe([(R * 0.35, 0), (R * 0.3, h)], seg=5, material=wood, cap_bottom=False)
    c_ = lathe([(R * 0.3, h * 0.95), (R, h * 0.92), (R * 0.6, h * 1.22), (0, h * 1.3)], seg=7, material=cap)
    xform(s_, loc=base); xform(c_, loc=base)
    smooth(c_, 60)
    parts += [s_, c_]
o = join(parts, 'tree_stump')
report()
lo, hi = bounds([o])
import bmesh as _b
mr = max(Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z + o.location.z < 0.6 + lo.z)
print('MAXR', round(mr, 3))
finish('meadow', 'tree_stump', kind='post', footprint=FP, notes='boomstronk met jaarringen, wortels, scheutje en paddenstoeltjes; binnen r=0.32')
