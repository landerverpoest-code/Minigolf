import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/water'); from _deco import *

BAMBOO = mat('bamboo', '#ead09a', rough=0.8)
WOOD = mat('wood_dark', '#77502c', rough=0.85)
THATCH = mat('thatch', '#dcb25a', rough=0.95)
TURQ = mat('turq', '#25b3bf', rough=0.55)
GLOW = mat('glow_lamp', '#fff3c4', rough=0.3, emit='#ffd860', emit_strength=6.0)

rnd = random.Random(3)
W, D = 3.0, 2.2          # vloer
FZ = 0.18


def bamboo(p0, p1, r=0.06, nodes=4, verts=6):
    p0, p1 = Vector(p0), Vector(p1)
    pts, rad, rm = [], [], []
    for i in range(nodes + 1):
        t = i / nodes
        q = p0.lerp(p1, t)
        if 0 < i < nodes:
            d = (p1 - p0).normalized() * 0.02
            pts += [q - d, q, q + d]; rad += [r, r * 1.15, r]; rm += [0, 1, 1]
        else:
            pts.append(q); rad.append(r); rm.append(0)
    rm = rm[:len(pts) - 1]
    o = tube(pts, rad, verts=verts, mats=[BAMBOO, WOOD], ring_mats=[0 if k % 3 == 0 else (1 if k % 3 == 1 else 0) for k in range(len(pts) - 1)])
    return o


# --- houten vlonder op paaltjes
for x in (-W / 2 + 0.1, 0, W / 2 - 0.1):
    for y in (-D / 2 + 0.1, D / 2 - 0.1):
        box((0.14, 0.14, FZ), loc=(x, y, FZ / 2), material=WOOD)
NPl = 10
for i in range(NPl):
    y = -D / 2 + (i + 0.5) * D / NPl
    box((W + rnd.uniform(-0.05, 0.05), D / NPl - 0.02, 0.06), loc=(rnd.uniform(-0.02, 0.02), y, FZ + 0.03), material=BAMBOO if i % 2 else WOOD)
FZ += 0.06
# --- vier bamboe hoekpalen
PH = 2.35
posts = [(-W / 2 + 0.15, -D / 2 + 0.15), (W / 2 - 0.15, -D / 2 + 0.15), (-W / 2 + 0.15, D / 2 - 0.15), (W / 2 - 0.15, D / 2 - 0.15)]
for x, y in posts:
    bamboo((x, y, FZ), (x, y, FZ + PH), r=0.08, nodes=4, verts=6)
# --- rieten dak: schilddak met twee lagen en gerafelde rand
RZ = FZ + PH - 0.05
def roof_layer(z, sx, sy, h, frz):
    prof = [(1.0, 0.0), (0.0, h)]
    prof = [(1.0, z)]
    for k, f in enumerate((0.72, 0.45)):
        zz = z + h * (1 - f)
        prof += [(f + 0.03, zz - 0.02), (f + 0.07, zz - 0.06)]
    prof.append((0.0, z + h))
    prof.sort(key=lambda p: p[1])
    prof = [(1.0, z)] + [(f + 0.0, zz) for f, zz in []] + prof[1:]
    r = lathe(prof, verts=4, material=THATCH, phase=math.pi / 4, sx=sx, sy=sy, cap0=True)
    # nokrollen op de hoekgraten
    top = Vector((0, 0, z + h))
    for k in range(4):
        c = Vector((sx * math.cos(math.pi / 4 + k * math.pi / 2), sy * math.sin(math.pi / 4 + k * math.pi / 2), z))
        tube([c + Vector((0, 0, 0.03)), top.lerp(c, 0.5) + Vector((0, 0, 0.05)), top + Vector((0, 0, 0.03))], 0.05, verts=4, material=WOOD, smooth=True)
    # gerafelde franje: zaagtand rondom
    vs, fs = [], []
    corners = [Vector((sx * math.cos(math.pi / 4 + k * math.pi / 2), sy * math.sin(math.pi / 4 + k * math.pi / 2), z)) for k in range(4)]
    for k in range(4):
        a, b = corners[k], corners[(k + 1) % 4]
        n = max(4, int((b - a).length / 0.28))
        for i in range(n):
            p0 = a.lerp(b, i / n); p1 = a.lerp(b, (i + 1) / n); pm = (p0 + p1) / 2
            out = Vector((pm.x, pm.y, 0)).normalized() * 0.05
            tip = pm + out - Vector((0, 0, frz * (0.8 + 0.4 * rnd.random())))
            base = len(vs); vs += [p0, p1, tip]
            fs.append((base, base + 1, base + 2))
    return [r, mesh_obj(vs, fs, THATCH, 'fringe')]
roof_layer(RZ, 2.3, 1.85, 1.0, 0.28)
roof_layer(RZ + 0.55, 1.2, 0.97, 0.75, 0.22)
# nokpunt met turquoise bol
cyl(0.05, 0.4, loc=(0, 0, RZ + 1.4), verts=5, material=WOOD)
ico(0.1, loc=(0, 0, RZ + 1.62), sub=2, material=TURQ, smooth=True)
# --- bar aan de voorkant (-Y): bamboe gevel + dik werkblad
CY = -D / 2 + 0.45
box((W - 0.5, 0.4, 1.0), loc=(0, CY + 0.05, FZ + 0.5), material=WOOD)
for i in range(13):
    x = -(W - 0.55) / 2 + i * (W - 0.55) / 12
    cyl(0.055, 1.0, loc=(x, CY - 0.17, FZ + 0.5), verts=5, material=BAMBOO)
box((W - 0.3, 0.6, 0.08), loc=(0, CY, FZ + 1.04), material=WOOD, bevel=0.02)
# turquoise band onder het blad
box((W - 0.45, 0.02, 0.1), loc=(0, CY - 0.235, FZ + 0.9), material=TURQ)
# kokosnootbekers met rietje op het blad
for k, x in enumerate((-0.8, -0.2, 0.55)):
    sphere(0.08, loc=(x, CY - 0.05, FZ + 1.14), seg=6, rings=4, material=WOOD, scale=(1, 1, 0.8))
    rod((x, CY - 0.05, FZ + 1.15), (x + 0.04, CY - 0.07, FZ + 1.33), r=0.008, verts=3, material=TURQ)
# --- achterwand met plank en flessen
box((W - 0.4, 0.06, 1.7), loc=(0, D / 2 - 0.2, FZ + 0.85), material=BAMBOO)
for z in (FZ + 1.1, FZ + 1.5):
    box((W - 0.6, 0.22, 0.04), loc=(0, D / 2 - 0.32, z), material=WOOD)
    for k in range(7):
        x = -1.05 + k * 0.35 + rnd.uniform(-0.05, 0.05)
        h = rnd.uniform(0.18, 0.28)
        m = TURQ if k % 2 else GLOW if k % 3 == 0 else BAMBOO
        lathe([(0.045, z + 0.02), (0.045, z + h * 0.65), (0.015, z + h * 0.85), (0.015, z + h)], verts=5, material=m, cap1=True)
# --- uithangbord boven de bar (touwen)
sign = box((1.3, 0.06, 0.32), loc=(0, -D / 2 + 0.05, RZ - 0.35), material=WOOD, bevel=0.02)
box((1.1, 0.02, 0.08), loc=(0, -D / 2 + 0.015, RZ - 0.35), material=TURQ)
for x in (-0.5, 0.5):
    rod((x, -D / 2 + 0.05, RZ - 0.19), (x, -D / 2 + 0.05, RZ + 0.05), r=0.012, verts=3, material=WOOD)
# --- drie barkrukken
for k, x in enumerate((-0.9, 0.0, 0.9)):
    y = CY - 0.65
    for a in range(3):
        ang = a * TAU / 3 + 0.3
        rod((x + 0.17 * math.cos(ang), y + 0.17 * math.sin(ang), FZ), (x + 0.07 * math.cos(ang), y + 0.07 * math.sin(ang), FZ + 0.68), r=0.025, verts=4, material=BAMBOO)
    cyl(0.2, 0.08, loc=(x, y, FZ + 0.72), verts=10, material=TURQ if k % 2 == 0 else WOOD)
# --- hangende lampionnen onder het dak
for x, y in ((-0.9, -0.3), (0.9, -0.3), (0, 0.4)):
    rod((x, y, RZ - 0.05), (x, y, RZ - 0.35), r=0.01, verts=3, material=WOOD)
    sphere(0.12, loc=(x, y, RZ - 0.45), seg=6, rings=4, material=GLOW, scale=(1, 1, 1.2))
# --- tiki-fakkels naast de bar
for s in (-1, 1):
    x = s * (W / 2 + 0.35); y = -D / 2 + 0.1
    bamboo((x, y, 0), (x, y, 1.7), r=0.045, nodes=3, verts=5)
    cyl(0.08, 0.18, loc=(x, y, 1.75), verts=6, material=WOOD, r2=0.1)
    flame = lathe([(0.07, 1.82), (0.08, 1.92), (0.04, 2.05), (0.0, 2.18)], verts=6, material=GLOW)
    T(flame, loc=(x, y, 0))
# --- tiki-masker op de linker voorpaal
mx, my = posts[0]
mask = box((0.3, 0.12, 0.5), loc=(mx, my - 0.1, FZ + 1.5), material=WOOD, bevel=0.03)
for s in (-1, 1):
    box((0.08, 0.04, 0.05), loc=(mx + s * 0.07, my - 0.17, FZ + 1.6), material=GLOW)
box((0.18, 0.04, 0.05), loc=(mx, my - 0.17, FZ + 1.38), material=TURQ)
box((0.06, 0.06, 0.14), loc=(mx, my - 0.18, FZ + 1.5), material=WOOD)
o = join_all('tiki_bar')
shade_smooth(o, 40)
report()
done('water', 'tiki_bar', kind='hero', footprint=2.2, center=True,
     notes='Tiki-strandbar: vlonder van planken, bamboe hoekpalen met knopen, dubbel rieten schilddak met gerafelde franje en turquoise nokbol, bar met bamboe gevel, kokosnootbekers met rietjes, achterwand met flessen, uithangbord, drie barkrukken, gloeiende lampionnen (glow_lamp), twee tiki-fakkels en een tiki-masker')
