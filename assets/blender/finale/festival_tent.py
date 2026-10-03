import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
purple = mat('royal_purple', '#5b2a86', rough=0.6)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#b0213a', rough=0.6)
dark = mat('tent_inside', '#2a1838', rough=0.9)
V = Vector
P = []
seg, R, Hw = 12, 1.6, 1.7
door = lambda a: abs(math.atan2(math.sin(a + math.pi / 2), math.cos(a + math.pi / 2))) < TAU / seg * 0.99
# wand met verticale strepen (paars/goud), deuropening vooraan (-Y)
bm = bmesh.new()
for i in range(seg):
    a0, a1 = i * TAU / seg - math.pi / 2 - TAU / seg / 2, (i + 1) * TAU / seg - math.pi / 2 - TAU / seg / 2
    am = (a0 + a1) / 2
    if abs(math.atan2(math.sin(am + math.pi / 2), math.cos(am + math.pi / 2))) < 0.1:
        continue
    vs = [bm.verts.new((R * math.cos(a0), R * math.sin(a0), 0)), bm.verts.new((R * math.cos(a1), R * math.sin(a1), 0)),
          bm.verts.new((R * math.cos(a1), R * math.sin(a1), Hw)), bm.verts.new((R * math.cos(a0), R * math.sin(a0), Hw))]
    f = bm.faces.new(vs); f.material_index = i % 2
wall = link_bm(bm, 'wall', purple)
wall.data.materials.append(gold)
for f in wall.data.polygons:
    f.material_index = 0 if f.index % 2 == 0 else 1
inner = dup(wall); flip(inner); T(inner, scale=(0.99, 0.99, 1))
inner.data.materials.clear(); inner.data.materials.append(dark)
P += [wall, inner]
P.append(cyl(R * 0.98, 0.02, loc=(0, 0, 0.02), verts=seg, material=dark))
# dak: kegel met strepen
roof = lathe([(R + 0.25, Hw - 0.05), (R * 0.55, Hw + 0.95), (0.0, Hw + 1.75)], seg=seg, material=purple, phase=-math.pi / 2 - TAU / seg / 2, cap_bot=False)
roof.data.materials.append(gold)
for f in roof.data.polygons:
    a = math.atan2(f.center.y, f.center.x) + math.pi / 2 + TAU / seg / 2
    f.material_index = int(round((a % TAU) / (TAU / seg) - 0.5)) % 2
rin = dup(roof); flip(rin); rin.data.materials.clear(); rin.data.materials.append(dark)
T(rin, loc=(0, 0, -0.03))
P += [roof, rin]
# geschulpte rand (driehoekige flapjes)
for i in range(seg * 2):
    a = i * TAU / (seg * 2) - math.pi / 2
    fl = prism([(-0.25, 0), (0.25, 0), (0, -0.32)], 0.02, crimson if i % 2 else gold, axis='y')
    T(fl, rot=(0.08, 0, a + math.pi / 2), loc=((R + 0.26) * math.cos(a), (R + 0.26) * math.sin(a), Hw - 0.03))
    P.append(fl)
# opgebonden deurflappen
for sx in (-1, 1):
    a = -math.pi / 2 + sx * TAU / seg * 0.5
    x, y = R * math.cos(a), R * math.sin(a)
    fl = prism([(0, 0), (sx * 0.35, 0), (sx * 0.12, Hw)], 0.04, gold, axis='y', loc=(x, y - 0.03, 0))
    P.append(fl)
    P.append(cyl(0.04, 0.05, loc=(x + sx * 0.12, y - 0.06, 0.9), rot=(math.pi / 2, 0, 0), verts=6, material=crimson))
# paal + wimpel
P.append(cyl(0.04, 0.9, loc=(0, 0, Hw + 2.1), verts=6, material=gold))
P.append(ico(0.08, loc=(0, 0, Hw + 2.58), sub=1, material=gold, smooth=True))
pn = prism([(0, 0), (0.75, -0.12), (0, -0.28)], 0.02, crimson, axis='y', loc=(0.03, 0, Hw + 2.5))
deform(pn, lambda v: V((v.x, v.y + 0.07 * math.sin(v.x * 7), v.z)))
P.append(pn)
join(P, 'festival_tent')
report()
finish('finale', 'festival_tent', kind='scatter', footprint=1.9, notes='rond paars/goud gestreept paviljoen met geschulpte rand, open deur en wimpel')
