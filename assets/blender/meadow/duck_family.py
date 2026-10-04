import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow'); from _deco import *

WHITE = mat('duck_white', '#f7f4ec', rough=0.6)
YEL = mat('duckling_yellow', '#ffd23a', rough=0.7)
ORANGE = mat('bill_orange', '#ff9426', rough=0.5)
BLACK = mat('eye_black', '#1e1c22', rough=0.3)
GRASS = mat('grass', '#4f9c33', rough=0.85)


def duck(pos, yaw, s=1.0, body_mat=WHITE, baby=False, seg=8, rings=6):
    """Eend rond de oorsprong, kijkt naar -Y. s = schaal (moeder ~0.5 m hoog)."""
    P = []
    # lijf: ei-vorm met opgewipt staartje
    b = sphere(1.0, seg=seg, rings=rings, material=body_mat, scale=(0.15, 0.22, 0.12))
    deform(b, lambda c: Vector((c.x * (1 - 0.35 * max(0, c.y / 0.22) ** 2), c.y, c.z + 0.12 * max(0, c.y / 0.22) ** 2.2 + (0.02 if c.z > 0 else 0))))
    T(b, loc=(0, 0.02, 0.15))
    P.append(b)
    if not baby:
        # vleugels: platte druppels tegen de flanken
        for sx in (-1, 1):
            w = sphere(1.0, seg=6, rings=4, material=body_mat, scale=(0.03, 0.15, 0.06))
            T(w, rot=(14, 0, sx * -4), loc=(sx * 0.125, 0.05, 0.18))
            P.append(w)
    # nek + kop
    hz = 0.36 if not baby else 0.29
    hr = 0.085 if not baby else 0.105
    P.append(tube([(0, -0.1, 0.18), (0, -0.14, hz - 0.06)], [0.07, 0.05], verts=6 if not baby else 4, material=body_mat, smooth=True))
    P.append(sphere(hr, loc=(0, -0.15, hz), seg=seg, rings=rings, material=body_mat))
    # snavel
    bill = sphere(1.0, seg=6 if not baby else 4, rings=4 if not baby else 3, material=ORANGE, scale=(0.045, 0.06, 0.018) if not baby else (0.04, 0.045, 0.017))
    T(bill, rot=(-8, 0, 0), loc=(0, -0.15 - hr - 0.025, hz - 0.025))
    P.append(bill)
    # oogjes
    for sx in (-1, 1):
        P.append(sphere(0.016 if not baby else 0.019, loc=(sx * hr * 0.62, -0.15 - hr * 0.68, hz + hr * 0.25), seg=4, rings=3, material=BLACK))
    if baby:
        # donskuifje
        P.append(cone(0.025, 0.05, loc=(0, -0.15, hz + hr + 0.015), rot=(-0.3, 0, 0), verts=4, material=body_mat))
    # zwemvliezen
    for sx in (-1, 1):
        P.append(mesh_obj([(sx * 0.06, -0.02, 0.005), (sx * 0.02, -0.12, 0.005), (sx * 0.1, -0.12, 0.005)], [(0, 1, 2)], ORANGE, 'foot'))
        P.append(rod((sx * 0.06, -0.03, 0.0), (sx * 0.06, 0.0, 0.08), r=0.014, verts=4, material=ORANGE))
    o = join(P, 'duck')
    return T(o, scale=s, rot=(0, 0, yaw), loc=pos)


duck((0.12, -0.32, 0), -12, 1.0)
duck((-0.13, 0.1, 0), 18, 0.56, YEL, baby=True, seg=6, rings=4)
duck((0.1, 0.38, 0), -10, 0.52, YEL, baby=True, seg=6, rings=4)
duck((-0.17, 0.64, 0), 25, 0.5, YEL, baby=True, seg=6, rings=4)

# graspolletjes langs het pad
rnd = random.Random(7)
for cx, cy in ((0.33, 0.05), (-0.35, -0.25), (0.28, 0.58)):
    for i in range(5):
        a = rnd.uniform(0, TAU); r = rnd.uniform(0, 0.05)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        h = rnd.uniform(0.09, 0.16)
        lean = Vector((rnd.uniform(-0.04, 0.04), rnd.uniform(-0.04, 0.04), 0))
        mesh_obj([(x - 0.016, y, 0), (x + 0.016, y, 0), Vector((x, y, h)) + lean], [(0, 1, 2)], GRASS, 'blade')

join_all('duck_family')
report()
done('meadow', 'duck_family', kind='scatter', footprint=0.7, center=True,
     notes='Witte moedereend met oranje snavel en zwemvliezen, gevolgd door drie gele eendjes met donskuifje op een rijtje, graspolletjes; lopen richting -Y')
