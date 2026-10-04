import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert'); from _deco import *

WOOD = mat('tent_wood', '#6e4a2c', rough=0.85)
RED = mat('blanket_red', '#c8323a', rough=0.75)
TURQ = mat('turquoise', '#27bfb0', rough=0.5)
GOLD = mat('flower_yellow', '#ffcc33', rough=0.6)
CREAM = mat('tent_cream', '#f0dcb0', rough=0.85)
MATS = [RED, TURQ, GOLD, CREAM]

rnd = random.Random(2)
W, H = 2.6, 2.1
# --- houten frame: twee staanders per kant en een bovenbalk
for x in (-W / 2, W / 2):
    rod((x, -0.05, 0), (x, -0.05, H), r=0.05, verts=6, material=WOOD)
    rod((x, 0.6, 0), (x, 0.6, H - 0.1), r=0.045, verts=6, material=WOOD)
    plank((x, -0.05, H - 0.05), (x, 0.65, H - 0.15), w=0.06, t=0.06, material=WOOD)
rod((-W / 2 - 0.12, -0.05, H - 0.08), (W / 2 + 0.12, -0.05, H - 0.08), r=0.045, verts=6, material=WOOD)
rod((-W / 2 - 0.05, 0.6, 1.25), (W / 2 + 0.05, 0.6, 1.25), r=0.035, verts=5, material=WOOD)
# --- gestreept zonnedoek als dak
roof = grid_sheet(lambda u, v: Vector((-W / 2 - 0.15 + u * (W + 0.3), -0.25 + v * 1.0, H + 0.08 - v * 0.15 + 0.05 * math.sin(u * math.pi))), 8, 2, CREAM, 'awning')
recolor(roof, [CREAM, RED], lambda f: 1 if int((f.center.x + W) / (W + 0.3) * 8) % 2 else 0)
# franje-randje
for i in range(8):
    x0 = -W / 2 - 0.15 + i * (W + 0.3) / 8
    mesh_obj([(x0, -0.25, H + 0.08), (x0 + (W + 0.3) / 8, -0.25, H + 0.08), (x0 + (W + 0.3) / 16, -0.26, H - 0.06)], [(0, 1, 2)], RED if i % 2 else CREAM, 'flap')


# --- tapijten over de balken (vel met patroon: rand, veld, ruit in het midden)
def rug(x0, x1, ztop, length, y, scheme, nu=5, nv=7, sway=0.0):
    c0, c1, c2 = scheme
    def f(u, v):
        x = x0 + u * (x1 - x0)
        z = ztop - v * length
        return Vector((x, y - 0.03 * math.sin(v * math.pi) - sway * v * v, z))
    o = grid_sheet(f, nu, nv, None, 'rug')
    def col(p):
        u = (p.center.x - x0) / (x1 - x0); v = (ztop - p.center.z) / length
        if u < 1 / nu or u > 1 - 1 / nu or v < 1 / nv or v > 1 - 1 / nv:
            return c0
        du, dv = abs(u - 0.5) * 2, abs(v - 0.5) * 2
        return c2 if du + dv * 0.8 < 0.55 else c1
    recolor(o, MATS, lambda p: col(p))
    # franjes onderaan
    return o


rug(-1.2, -0.45, H - 0.08, 1.55, -0.1, (2, 0, 1))
rug(-0.38, 0.38, H - 0.08, 1.75, -0.1, (1, 3, 0))
rug(0.45, 1.2, H - 0.08, 1.45, -0.1, (0, 2, 1))
# kleed over de achterste balk (dubbel gevouwen)
for side, mats in ((-1, (3, 0, 2)), (1, (3, 0, 2))):
    pass
back = rug(-1.1, 1.1, 1.26, 0.9, 0.62, (3, 0, 1), nu=7, nv=4)
# --- opgerolde tapijten op de grond en een stapel gevouwen kleden
for k, (x, y, r, m) in enumerate(((-0.6, -0.6, 0.11, RED), (-0.35, -0.65, 0.1, TURQ), (-0.48, -0.62, 0.1, GOLD))):
    z = r if k < 2 else 0.29
    roll = cyl(r, 1.0, verts=8, material=m, rot=(0, math.pi / 2, 0.15), loc=(x if k < 2 else -0.47, y, z))
    for s in (-1, 1):
        cyl(r * 0.5, 0.01, verts=6, material=CREAM, rot=(0, math.pi / 2, 0.15), loc=((x if k < 2 else -0.47) + s * 0.5 * math.cos(0.15), y + s * 0.5 * math.sin(0.15), z))
for k in range(4):
    box((0.7 - k * 0.04, 0.5 - k * 0.03, 0.07), loc=(0.75, -0.55, 0.035 + k * 0.07), rot=(0, 0, 0.1 * k), material=MATS[k % 4])
# kruk
cyl(0.18, 0.05, loc=(1.6, 0.0, 0.4), verts=8, material=WOOD)
for k in range(3):
    a = k * TAU / 3
    rod((1.6 + 0.14 * math.cos(a), 0.14 * math.sin(a), 0), (1.6 + 0.08 * math.cos(a), 0.08 * math.sin(a), 0.38), r=0.02, verts=4, material=WOOD)
o = join_all('market_rugs')
report()
done('desert', 'market_rugs', kind='scatter', footprint=1.5, center=True,
     notes='Tapijtkraam: houten frame met rood-crème gestreept zonnedoek en franje, drie hangende tapijten en een kleed achter met rand- en ruitpatroon (rood, turquoise, goud, crème), opgerolde tapijten, stapel gevouwen kleden, krukje')
