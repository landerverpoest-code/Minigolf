import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
basalt = mat('basalt', '#3d3648', rough=0.9)
purple = mat('royal_purple', '#6a2fa0', rough=0.45)
crimson = mat('crimson', '#b0213a', rough=0.45)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
glow = mat('glow_egg', '#ff8a20', rough=0.3, emit='#ff6a10', emit_strength=2.2)
V = Vector
P = []
# ring van rotsen + bodem
P.append(lathe([(0.55, 0.0), (0.45, 0.08), (0.0, 0.1)], seg=10, material=basalt))
for k in range(9):
    a = k * TAU / 9 + 0.2
    rr = 0.16 + 0.05 * math.sin(k * 2.7)
    P.append(chop(rock(rr, loc=(0.55 * math.cos(a), 0.55 * math.sin(a), 0), sub=1, material=basalt, scale=(1.2, 1.0, 0.9), jit=0.25, seed=k), 2, seed=k))
# goudstukken
for k, (x, y, rx) in enumerate([(0.2, -0.32, 0.3), (-0.3, -0.25, -0.2), (0.35, 0.1, 0.4), (-0.12, 0.33, 0.1), (0.05, -0.42, 0.6), (-0.4, 0.05, -0.5)]):
    P.append(cyl(0.06, 0.02, loc=(x, y, 0.11), rot=(rx * 0.5, rx * 0.4, 0), verts=6, material=gold))
# eieren
def egg(h=0.4, r=0.17, seg=8):
    prof = [(0, 0)] + [(r * math.sin(math.pi * t) ** 0.9 * (1 - 0.18 * t), h * (1 - math.cos(math.pi * t)) / 2) for t in (0.15, 0.32, 0.5, 0.68, 0.85)] + [(0, h)]
    return lathe(prof, seg=seg, smooth=True)
e1 = egg(0.46, 0.18); e1.data.materials.append(purple); e1.data.materials.append(gold)
for p in e1.data.polygons:   # harlekijnpatroon
    a = math.atan2(p.center.y, p.center.x); ring = int(p.center.z / 0.46 * 6)
    p.material_index = (int((a + math.pi) / (TAU / 8)) + ring) % 2
T(e1, rot=(0.15, -0.2, 0), loc=(-0.13, 0.08, 0.07))
e2 = egg(0.4, 0.16); e2.data.materials.append(crimson); e2.data.materials.append(gold)
for p in e2.data.polygons:
    if 0.15 < p.center.z < 0.24:
        p.material_index = 1
T(e2, rot=(-0.25, 0.3, 0.5), loc=(0.17, 0.12, 0.06))
e3 = egg(0.42, 0.17); e3.data.materials.append(glow)
T(e3, rot=(0.2, 0.15, 0), loc=(0.03, -0.17, 0.06))
P += [e1, e2, e3]
join(P, 'dragon_egg_nest')
report()
finish('finale', 'dragon_egg_nest', kind='scatter', footprint=0.7, notes='nest van rotsen met goudstukken en drie drakeneieren (paars/goud, rood/goud, gloeiend = glow_egg)')
