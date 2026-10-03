import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

SAND = mat('sandstone', '#e3bb7c', rough=0.85)
DARK = mat('sandstone_groove', '#9c7146', rough=0.9)
GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.55)
TURQ = mat('turquoise', '#27bfb0', rough=0.45)
BASE = mat('sandstone_base', '#c99a62', rough=0.9)
rnd = random.Random(9)

# --- getrapte sokkel ---
steps = [(2.3, 0.35, BASE), (1.85, 0.35, SAND), (1.45, 0.4, BASE)]
z = 0
for w, h, m in steps:
    box((w, w, h), loc=(0, 0, z + h / 2), material=m, bevel=0.04)
    z += h
ZB = z
# turkooise inleg-band op de bovenste trede
for s in (-1, 1):
    box((1.0, 0.03, 0.12), loc=(0, s * 0.725, ZB - 0.2), material=TURQ)
    box((0.03, 1.0, 0.12), loc=(s * 0.725, 0, ZB - 0.2), material=TURQ)
# --- naald (afgeknotte vierkante zuil) ---
W0, W1, HS = 0.62, 0.42, 7.0
secs = []
for zz, w in ((ZB, W0), (ZB + HS, W1)):
    secs.append([(-w, -w, zz), (w, -w, zz), (w, w, zz), (-w, w, zz)])
shaft = loft(secs, material=SAND, closed=True, cap0=True, cap1=True)
bev(shaft, 0.035)
# piramidion (goud)
ZT = ZB + HS
gold_band = loft([[(-W1 - 0.02, -W1 - 0.02, ZT), (W1 + 0.02, -W1 - 0.02, ZT), (W1 + 0.02, W1 + 0.02, ZT), (-W1 - 0.02, W1 + 0.02, ZT)],
                  [(-W1 - 0.02, -W1 - 0.02, ZT + 0.08), (W1 + 0.02, -W1 - 0.02, ZT + 0.08), (W1 + 0.02, W1 + 0.02, ZT + 0.08), (-W1 - 0.02, W1 + 0.02, ZT + 0.08)]],
                 material=GOLD, closed=True)
pyr = loft([[(-W1, -W1, ZT + 0.08), (W1, -W1, ZT + 0.08), (W1, W1, ZT + 0.08), (-W1, W1, ZT + 0.08)], [(0, 0, ZT + 0.85)]],
           material=GOLD, closed=True, cap0=True)


# --- hiërogliefen op elke zijde ---
def wz(zz):
    return W0 + (W1 - W0) * (zz - ZB) / HS


slope = math.atan2(W0 - W1, HS)


def glyph(face, u, zz, sx, sz, m=DARK, depth=0.03):
    """face: 0..3 (−Y, +X, +Y, −X); u = horizontale positie op het vlak."""
    w = wz(zz)
    rotz = [0, math.pi / 2, math.pi, -math.pi / 2][face]
    # in lokaal vlak (−Y): x=u, y=-w
    loc = Vector((u, -w - depth * 0.15, zz))
    o = box((sx, depth, sz), loc=(0, 0, 0), rot=(0, 0, 0), material=m)
    o.rotation_euler = (-slope, 0, 0); apply(o)
    o.location = loc
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    o.rotation_euler = (0, 0, rotz); apply(o)
    return o


for f in range(4):
    zz = ZB + 0.6
    # kaderlijnen van de kolom
    for s in (-1, 1):
        L = HS - 1.4
        zc = ZB + 0.6 + L / 2
        glyph(f, s * 0.24 * (wz(zc) / W0 + 0.15), zc, 0.035, L, depth=0.025)
    # cartouche bovenaan
    glyph(f, 0, ZB + HS - 1.3, 0.28, 0.9, m=DARK)
    glyph(f, 0, ZB + HS - 1.3, 0.18, 0.75, m=SAND, depth=0.04)
    glyph(f, 0, ZB + HS - 1.15, 0.1, 0.1, m=GOLD, depth=0.05)
    glyph(f, 0, ZB + HS - 1.45, 0.12, 0.05, m=DARK, depth=0.05)
    # kolom met tekens
    zz = ZB + 0.8
    k = 0
    while zz < ZB + HS - 2.0:
        kind = (k + f) % 5
        if kind == 0:   # zonneschijf
            glyph(f, 0, zz, 0.16, 0.16, m=GOLD if f % 2 == 0 else DARK)
        elif kind == 1:  # vogel (L-vorm)
            glyph(f, -0.03, zz, 0.18, 0.06); glyph(f, 0.06, zz + 0.08, 0.06, 0.16)
        elif kind == 2:  # golflijnen (water)
            glyph(f, 0, zz - 0.05, 0.24, 0.035); glyph(f, 0, zz + 0.05, 0.24, 0.035)
        elif kind == 3:  # oog / ankh-achtig
            glyph(f, 0, zz + 0.04, 0.06, 0.18); glyph(f, 0, zz, 0.2, 0.05)
        else:          # staf
            glyph(f, 0, zz, 0.05, 0.24)
        zz += 0.42
        k += 1
# --- puinbrokjes rond de voet ---
for k in range(6):
    a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(1.4, 1.9)
    rock(rnd.uniform(0.1, 0.2), loc=(math.cos(a) * d, math.sin(a) * d, 0.05), scale=(1.3, 1.0, 0.8), seed=k, jitter=0.2,
         material=BASE if k % 2 else SAND)
join_all('obelisk')
report()
finish('desert', 'obelisk', kind='hero', footprint=1.3,
       notes='Obelisk op getrapte sokkel met turkooise inleg, hiërogliefen-groeven op elke zijde en gouden piramidion')
closeup('obelisk')
