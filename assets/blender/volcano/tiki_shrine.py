import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
tiki = mat('tiki_stone', '#7c6654', rough=0.85)
wood = mat('bamboo', '#a27a48', rough=0.8)
lava = mat('glow_lava', '#ff7010', rough=0.4, emit='#ff4c00', emit_strength=3.5)
ash = mat('ash_stone', '#a0968b', rough=0.9)

rnd = random.Random(12)
parts = []
# --- getrapte voet uit blokken ---
tiers = [(4.4, 0.0), (3.4, 0.45), (2.4, 0.9)]
TH = 0.45
for ti, (S, z0) in enumerate(tiers):
    core = box((S - 0.1, S - 0.1, TH), loc=(0, 0, z0 + TH / 2), material=basalt)
    parts.append(core)
    # randblokken (metselwerk), licht verspringend
    n = int(S / 0.75)
    for side in range(4):
        for i in range(n):
            u = -S / 2 + (i + 0.5) * S / n
            w = S / n - 0.05
            d = rnd.uniform(0.02, 0.07)
            hh = TH - 0.04
            b = box((w, 0.2, hh), material=basalt if (i + side + ti) % 4 else ash)
            jitter(b, 0.015, seed=ti * 100 + side * 10 + i)
            xform(b, loc=(u, -S / 2 + 0.08 - d, z0 + TH / 2))
            xform(b, rot=(0, 0, 90 * side))
            parts.append(b)
    # afdekplaat
    parts.append(box((S - 0.02, S - 0.02, 0.06), loc=(0, 0, z0 + TH + 0.0), material=tiki))
TOP = tiers[-1][1] + TH + 0.03
# --- trap aan de voorkant ---
for k in range(6):
    z = k * TOP / 6
    y = -tiers[0][0] / 2 - 0.35 + k * ((tiers[0][0] - tiers[-1][0]) / 2 + 0.35) / 6
    st = box((1.3, 0.5, TOP / 6 + 0.02), loc=(0, y, z + TOP / 12), material=ash if k % 2 else basalt, bevel=0.03)
    parts.append(st)

# --- totem ---
B = TOP
body = box((1.15, 1.0, 1.35), loc=(0, 0, B + 0.67), material=tiki, bevel=0.08)
parts.append(body)
head = box((1.55, 1.25, 1.75), loc=(0, 0, B + 1.35 + 0.85), material=tiki, bevel=0.1)
bend(head, lambda c: (c.x * (1 + 0.06 * (c.z - (B + 1.35)) / 1.75), c.y, c.z))
parts.append(head)
HZ = B + 1.35   # onderkant hoofd
FY = -0.63      # voorkant hoofd
# wenkbrauwboog
parts.append(box((1.5, 0.28, 0.24), loc=(0, FY - 0.08, HZ + 1.25), material=tiki, bevel=0.05))
# oogkassen + gloeiende ogen
for sx in (-1, 1):
    parts.append(box((0.42, 0.06, 0.34), loc=(sx * 0.36, FY - 0.02, HZ + 0.98), material=basalt, bevel=0.02))
    eye = cyl(0.12, 0.08, loc=(sx * 0.36, FY - 0.07, HZ + 0.98), rot=(math.pi / 2, 0, 0), verts=8, material=lava)
    parts.append(eye)
    # wangkrul
    parts.append(torus(0.13, 0.035, loc=(sx * 0.55, FY - 0.03, HZ + 0.55), rot=(math.pi / 2, 0, 0), seg=8, ring=4, material=ash))
# neus: trapezium dat naar voren steekt
nose = prism([(-0.16, 0.0), (0.16, 0.0), (0.3, -0.55), (-0.3, -0.55)], 0.3, material=tiki)
bm = bmesh.new(); bm.from_mesh(nose.data)
for v in bm.verts:
    if v.co.y < 0 and v.co.z > -0.1:
        v.co.y += 0.12   # bovenkant neus minder ver naar voren
bm.to_mesh(nose.data); bm.free()
xform(nose, loc=(0, FY - 0.14, HZ + 1.05))
parts.append(nose)
# mond: brede donkere opening met gloed en tanden
parts.append(box((1.15, 0.08, 0.36), loc=(0, FY - 0.02, HZ + 0.22), material=basalt, bevel=0.02))
parts.append(box((0.95, 0.06, 0.1), loc=(0, FY - 0.05, HZ + 0.22), material=lava))
for k in range(6):
    x = -0.45 + k * 0.18
    parts.append(box((0.11, 0.07, 0.11), loc=(x, FY - 0.08, HZ + 0.34), material=ash))
    parts.append(box((0.11, 0.07, 0.09), loc=(x + 0.09 if k < 5 else x - 0.09, FY - 0.08, HZ + 0.1), material=ash))
# lippen-rand
parts.append(box((1.3, 0.12, 0.08), loc=(0, FY - 0.06, HZ + 0.44), material=tiki, bevel=0.02))
parts.append(box((1.3, 0.12, 0.08), loc=(0, FY - 0.06, HZ + 0.0), material=tiki, bevel=0.02))
# oren
for sx in (-1, 1):
    parts.append(box((0.16, 0.36, 0.7), loc=(sx * 0.86, 0.0, HZ + 0.8), material=tiki, bevel=0.04))
    parts.append(cyl(0.07, 0.06, loc=(sx * 0.95, 0.0, HZ + 0.62), rot=(0, math.pi / 2, 0), verts=6, material=ash))
# armen in reliëf op het lijf, handen op de buik
for sx in (-1, 1):
    parts.append(plank((sx * 0.5, -0.5, B + 1.25), (sx * 0.48, -0.53, B + 0.7), w=0.2, t=0.12, up=(0, 1, 0), material=tiki, bevel=0.03))
    parts.append(plank((sx * 0.48, -0.53, B + 0.7), (sx * 0.12, -0.55, B + 0.55), w=0.18, t=0.12, up=(0, 1, 0), material=tiki, bevel=0.03))
    hand = box((0.22, 0.14, 0.2), loc=(sx * 0.12, -0.56, B + 0.56), material=tiki, bevel=0.04)
    parts.append(hand)
# buikband met ruitjes
parts.append(box((1.22, 1.07, 0.14), loc=(0, 0, B + 0.25), material=ash, bevel=0.03))
for k in range(5):
    d = box((0.12, 0.05, 0.12), loc=(-0.4 + k * 0.2, -0.54, B + 0.25), rot=(0, math.pi / 4, 0), material=basalt)
    parts.append(d)
# --- hoofdtooi: waaier van stenen veren ---
parts.append(box((1.65, 1.3, 0.2), loc=(0, 0, HZ + 1.82), material=ash, bevel=0.04))
for k in range(7):
    a = math.radians(-60 + k * 20)
    L = 1.45 if k % 2 == 0 else 1.1
    f = prism([(-0.17, 0), (0.17, 0), (0.15, L * 0.75), (0, L), (-0.15, L * 0.75)], 0.14, material=tiki if k % 2 == 0 else ash)
    # profiel in xz -> naar voren gericht, waaier rond y-as
    xform(f, rot=(0, math.degrees(a), 0), loc=(0, 0.05, HZ + 1.88))
    parts.append(f)
    # gloeiend puntje op de middelste veer
    if k % 2 == 0:
        tip = ico(0.09 if k != 3 else 0.12, sub=1, material=lava)
        xform(tip, loc=(0, -0.05, L * 0.82)); xform(tip, rot=(0, math.degrees(a), 0), loc=(0, 0.0, HZ + 1.88))
        parts.append(tip)

# achterplaat van de waaier (vult de ruimte tussen de veren)
fan = prism([(0.95 * math.sin(math.radians(a)), 0.95 * math.cos(math.radians(a))) for a in range(-70, 71, 20)] + [(0, 0)], 0.1, material=ash)
xform(fan, loc=(0, 0.16, HZ + 1.88))
parts.append(fan)
# --- fakkels op de tweede trede ---
for sx in (-1, 1):
    x, y, z0 = sx * 1.35, -1.35, tiers[1][1] + TH + 0.03
    parts.append(rod((x, y, z0), (x, y, z0 + 1.6), 0.06, 0.05, verts=6, material=wood))
    for k in range(3):
        parts.append(cyl(0.07, 0.05, loc=(x, y, z0 + 0.4 + k * 0.45), verts=6, material=wood))
    bowl = lathe([(0.06, z0 + 1.55), (0.22, z0 + 1.72), (0.24, z0 + 1.82), (0.2, z0 + 1.8), (0.0, z0 + 1.76)], seg=8, material=basalt)
    xform(bowl, loc=(x, y, 0))
    parts.append(bowl)
    for k, (h, r) in enumerate(((0.55, 0.2), (0.4, 0.13))):
        fl = cone(r, h, loc=(0, 0, h / 2), verts=6, material=lava)
        bend(fl, lambda c: (c.x + 0.05 * math.sin(c.z * 8), c.y, c.z))
        xform(fl, rot=(0, 0, k * 30), loc=(x + (0.05 if k else 0), y, z0 + 1.78))
        parts.append(fl)
# offerschaal met lava voor het beeld
ob = lathe([(0.15, 0), (0.28, 0.12), (0.36, 0.25), (0.31, 0.27), (0, 0.22)], seg=10, material=ash)
xform(ob, loc=(0, -0.95, TOP))
parts.append(ob)
parts.append(cyl(0.3, 0.02, loc=(0, -0.95, TOP + 0.235), verts=10, material=lava))
# achterkant: gekerfde banden
for z in (HZ + 0.4, HZ + 1.0):
    parts.append(box((1.3, 0.08, 0.1), loc=(0, 0.66, z), material=ash))
parts.append(torus(0.25, 0.05, loc=(0, 0.66, HZ + 0.7), rot=(math.pi / 2, 0, 0), seg=10, ring=4, material=ash))
s = join(parts, 'tiki_shrine')
smooth(s, 40)
report()
finish('volcano', 'tiki_shrine', kind='hero', footprint=2.6, notes='stenen tiki op getrapte basaltvoet met trap; gloeiende ogen, mond, veerpunt, fakkelvlammen en offerschaal (glow_lava); wangkrullen, tanden, armen in reliëf, verentooi')
