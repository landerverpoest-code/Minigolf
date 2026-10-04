import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow'); from _deco import *

WOOD = mat('wood', '#9a6538', rough=0.85)
YEL = mat('hive_yellow', '#f2c14e', rough=0.6)
WHITE = mat('hive_white', '#f6f0e2', rough=0.6)
DARK = mat('hive_dark', '#2e2622', rough=0.7)
ROOF = mat('roof_red', '#c8402f', rough=0.55, metal=0.1)

parts = []
# --- houten onderstel
for x in (-0.2, 0.2):
    for y in (-0.16, 0.16):
        parts.append(box((0.06, 0.06, 0.28), loc=(x, y, 0.14), material=WOOD))
parts.append(box((0.56, 0.5, 0.05), loc=(0, 0, 0.305), material=WOOD, bevel=0.01))
# landingsplankje voor de vliegopening
parts.append(box((0.46, 0.12, 0.025), loc=(0, -0.24, 0.34), rot=(-0.12, 0, 0), material=WOOD))

# --- drie bakken boven elkaar (afwisselend geel / wit), met handgrepen
z = 0.33
H = [0.2, 0.2, 0.15]
for i, h in enumerate(H):
    m = YEL if i % 2 == 0 else WHITE
    b = box((0.46, 0.4, h - 0.008), loc=(0, 0, z + h / 2), material=m, bevel=0.012)
    parts.append(b)
    # handgreep-latjes aan de zijkanten
    for s in (-1, 1):
        parts.append(box((0.02, 0.18, 0.025), loc=(s * 0.235, 0, z + h * 0.62), material=WOOD))
    # voor: houten lijstje
    parts.append(box((0.3, 0.012, 0.022), loc=(0, -0.205, z + h * 0.7), material=WOOD))
    z += h
# vliegopening (donkere spleet onderaan)
parts.append(box((0.28, 0.02, 0.035), loc=(0, -0.196, 0.352), material=DARK))

# --- puntdak (gebogen tinnen dak) met overstek
roofz = z + 0.02
parts.append(box((0.5, 0.44, 0.04), loc=(0, 0, roofz), material=WHITE, bevel=0.008))
prof = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.025), (0.0, 0.14), (-0.3, 0.025)]
roof = prism(prof, 0.52, material=ROOF, axis='Y', loc=(0, 0, roofz + 0.02))
T(roof, rot=(0, 0, 90))
parts.append(roof)
# nok
parts.append(box((0.54, 0.035, 0.025), loc=(0, 0, roofz + 0.158), material=DARK))

# --- honingdruppel over de voorkant
drip = tube([(0.12, -0.205, z - 0.02), (0.12, -0.21, z - 0.08), (0.125, -0.212, z - 0.12)], [0.02, 0.015, 0.0], verts=5, material=YEL, cap0=False, smooth=True)
parts.append(drip)


# --- bijtjes
def bee(p, yaw):
    o = []
    body = sphere(1.0, seg=6, rings=3, material=YEL, scale=(0.035, 0.05, 0.035))
    band = cyl(0.037, 0.022, verts=5, material=DARK, rot=(math.pi / 2, 0, 0))
    tail = cone(0.03, 0.03, verts=4, material=DARK, loc=(0, 0.055, 0), rot=(-math.pi / 2, 0, 0))
    head = sphere(0.024, loc=(0, -0.055, 0.008), seg=4, rings=3, material=DARK)
    w1 = mesh_obj([(0.005, 0, 0.03), (0.07, 0.02, 0.07), (0.075, -0.025, 0.055)], [(0, 1, 2)], WHITE, 'wing')
    w2 = mesh_obj([(-0.005, 0, 0.03), (-0.07, 0.02, 0.07), (-0.075, -0.025, 0.055)], [(0, 2, 1)], WHITE, 'wing')
    b = join([body, band, tail, head, w1, w2], 'bee')
    return T(b, rot=(0, 0, yaw), loc=p)


bees = [((0.32, -0.38, 0.62), 40), ((-0.28, -0.42, 0.48), -60), ((0.05, -0.5, 0.8), 10),
        ((0.24, -0.3, 1.18), 70)]
for p, yaw in bees:
    parts.append(bee(p, yaw))

join_all('beehive_box')
report()
done('meadow', 'beehive_box', kind='scatter', footprint=0.4,
     notes='Bijenkast: houten onderstel, drie gestapelde bakken (geel/wit) met handgrepen, vliegopening met landingsplankje, rood puntdak, honingdruppel, vier zoemende bijtjes')
