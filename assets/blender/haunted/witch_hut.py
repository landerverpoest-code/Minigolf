import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
wood = mat('wood', '#6b5040', rough=0.85)
wdark = mat('wood_dark', '#3d2e2c', rough=0.9)
roof = mat('roof', '#54456a', rough=0.85)
stone = mat('stone', '#7f8a80', rough=0.9)
glow = mat('glow_window', '#ffc44a', rough=0.4, emit='#ffaa22', emit_strength=2.0)
V = Vector
rnd = random.Random(3)
P = []
W, D, H, z0 = 2.4, 2.2, 2.1, 0.32
# fundering van ruwe stenen
f = box((W + 0.3, D + 0.3, z0), loc=(0, 0, z0 / 2), material=stone, bevel=0.04); jitter(f, 0.03, 1); P.append(f)
# muren: kern + losse planken (voor, links, rechts)
core = box((W, D, H), loc=(0, 0, z0 + H / 2), material=wdark); P.append(core)
def plank(x, y, w, h, axis, seed):
    r = random.Random(seed)
    if axis == 'y':
        b = box((w * 0.94, 0.05, h), loc=(x, y, z0 + h / 2), material=wood if seed % 3 else wdark)
    else:
        b = box((0.05, w * 0.94, h), loc=(x, y, z0 + h / 2), material=wood if seed % 3 else wdark)
    T(b, rot=(r.uniform(-0.03, 0.03), r.uniform(-0.03, 0.03), 0), pivot=(x, y, z0 + h / 2))
    return b
n = 8
for i in range(n):
    x = -W / 2 + (i + 0.5) * W / n
    if abs(x - 0.35) < 0.36:   # deur
        continue
    P.append(plank(x, -D / 2 - 0.02, W / n, H + rnd.uniform(-0.05, 0.08), 'y', i))
for sx in (-1, 1):
    for i in range(7):
        y = -D / 2 + (i + 0.5) * D / 7
        P.append(plank(sx * (W / 2 + 0.02), y, D / 7, H + rnd.uniform(-0.05, 0.08), 'x', 20 + i + (sx > 0) * 10))
for sx in (-1, 1):
    for sy in (-1, 1):
        P.append(box((0.16, 0.16, H + 0.1), loc=(sx * W / 2, sy * D / 2, z0 + H / 2), material=wdark))
# geveldriehoeken
RH = 1.9
for sy in (-1, 1):
    g = prism([(-W / 2 - 0.05, 0), (W / 2 + 0.05, 0), (0.05, RH)], 0.1, wood, axis='y', loc=(0, sy * (D / 2 + 0.0), z0 + H))
    P.append(g)
# rond zolderraampje
P.append(cyl(0.22, 0.06, loc=(0.05, -D / 2 - 0.06, z0 + H + 0.65), rot=(math.pi / 2, 0, 0), verts=8, material=glow))
P.append(torus(0.24, 0.05, loc=(0.05, -D / 2 - 0.08, z0 + H + 0.65), rot=(math.pi / 2, 0, 0), seg=8, ring=4, material=wdark, smooth=False))
P.append(box((0.04, 0.03, 0.44), loc=(0.05, -D / 2 - 0.1, z0 + H + 0.65), material=wdark))
P.append(box((0.44, 0.03, 0.04), loc=(0.05, -D / 2 - 0.1, z0 + H + 0.65), material=wdark))
# dak: dakpanrijen, steil, overstek, met lapjes
roofp = []
half = W / 2 + 0.35
ang = math.atan2(RH, W / 2)
L = math.hypot(half, RH * half / (W / 2)) + 0.1
rows = 5
for sx in (-1, 1):
    for r in range(rows):
        t = (r + 0.5) / rows
        x = sx * (0.05 + t * half)
        z = z0 + H + RH + 0.12 - t * half * math.tan(ang) + 0.03 * r / rows
        nseg = 4
        for k in range(nseg):
            yl = -(D + 0.7) / 2 + (k + 0.5) * (D + 0.7) / nseg + rnd.uniform(-0.04, 0.04)
            b = box(((L / rows) * 1.25, (D + 0.7) / nseg + 0.04, 0.08), loc=(x, yl, z + rnd.uniform(-0.01, 0.02)),
                    rot=(rnd.uniform(-0.04, 0.04), sx * (ang + 0.13 + rnd.uniform(-0.03, 0.03)), rnd.uniform(-0.04, 0.04)), material=roof)
            roofp.append(b)
# lapjes
for (sx, t, y, m, s) in [(-1, 0.42, -0.4, wood, 0.42), (-1, 0.78, 0.6, stone, 0.36), (1, 0.62, 0.15, wood, 0.42), (1, 0.3, -0.8, wdark, 0.32), (1, 0.82, 0.95, stone, 0.3)]:
    x = sx * (0.05 + t * half); z = z0 + H + RH + 0.27 - t * half * math.tan(ang)
    pb = box((s * 1.15, s * 1.25, 0.04), loc=(x, y, z), rot=(0, sx * (ang + 0.13), rnd.uniform(-0.2, 0.2)), material=m)
    roofp.append(pb)
    for (dx, dy) in [(-s * 0.4, -s * 0.45), (s * 0.4, s * 0.45)]:
        pass
ridge = box((0.22, D + 0.8, 0.2), loc=(0.05, 0, z0 + H + RH + 0.14), rot=(0, math.pi / 4, 0), material=wdark)
roofp.append(ridge)
R = join(roofp, 'roof')
# scheef zakkende nok + twist
def sag(v):
    k = (v.y / (D / 2 + 0.4))
    v.z -= 0.22 * (1 - k * k) * max(0, (v.z - (z0 + H)) / RH)
    v.x += 0.12 * k * max(0, (v.z - (z0 + H)) / RH)
    return v
deform(R, sag)
P.append(R)
# schoorsteen (scheef gestapeld)
cz = z0 + H + 0.9
for i in range(4):
    b = box((0.5 - i * 0.02, 0.5 - i * 0.02, 0.45), loc=(0.85 + i * 0.05, 0.45, cz + i * 0.42), rot=(0.03 * (i % 2), 0.06 * i, 0.12 * i), material=stone, bevel=0.03)
    P.append(b)
P.append(box((0.6, 0.6, 0.1), loc=(1.03, 0.45, cz + 1.66), rot=(0, 0.2, 0.4), material=wdark))
for k, (dx, dz, r) in enumerate([(0.0, 1.9, 0.16), (0.1, 2.12, 0.2), (0.28, 2.4, 0.25)]):
    P.append(ico(r, loc=(1.06 + dx, 0.45, cz + dz), material=stone, smooth=True, jitter=0.03, seed=k))
# raam voor met kruisroede en scheef luik
wx, wz = -0.6, z0 + 1.25
P.append(box((0.62, 0.06, 0.62), loc=(wx, -D / 2 - 0.06, wz), rot=(0, 0.08, 0), material=glow))
for b in [box((0.74, 0.08, 0.08), loc=(wx, -D / 2 - 0.1, wz + 0.34)), box((0.74, 0.08, 0.08), loc=(wx, -D / 2 - 0.1, wz - 0.34)),
          box((0.08, 0.08, 0.74), loc=(wx - 0.34, -D / 2 - 0.1, wz)), box((0.08, 0.08, 0.74), loc=(wx + 0.34, -D / 2 - 0.1, wz)),
          box((0.04, 0.06, 0.62), loc=(wx, -D / 2 - 0.1, wz)), box((0.62, 0.06, 0.04), loc=(wx, -D / 2 - 0.1, wz))]:
    b.data.materials.append(wdark); T(b, rot=(0, 0.08, 0), pivot=(wx, 0, wz)); P.append(b)
sh = box((0.34, 0.05, 0.7), loc=(wx - 0.58, -D / 2 - 0.12, wz), material=wood)
T(sh, rot=(0, -0.35, 0.25), pivot=(wx - 0.42, -D / 2 - 0.12, wz + 0.35)); P.append(sh)
# zijraam
P.append(box((0.06, 0.5, 0.5), loc=(-W / 2 - 0.06, 0.2, z0 + 1.3), material=glow))
P.append(box((0.08, 0.04, 0.6), loc=(-W / 2 - 0.1, 0.2, z0 + 1.3), material=wdark))
P.append(box((0.08, 0.6, 0.04), loc=(-W / 2 - 0.1, 0.2, z0 + 1.3), material=wdark))
# scheve deur met maansikkel-kijkgat
dx = 0.35
door = [(-0.33, 0), (0.33, 0), (0.33, 1.25)] + [(0.33 * math.cos(a) + 0.03, 1.25 + 0.38 * math.sin(a)) for a in [0.6, 1.2, 1.9, 2.5]] + [(-0.33, 1.25)]
dd = prism(door, 0.08, wdark, axis='y', loc=(dx, -D / 2 - 0.04, z0))
T(dd, rot=(0, 0.06, 0), pivot=(dx, 0, z0)); P.append(dd)
moon = poly_face([(0.07 * math.cos(a), 0.07 * math.sin(a)) for a in [i * TAU / 10 for i in range(-2, 7)]] +
                 [(0.03 + 0.05 * math.cos(a), 0.02 + 0.05 * math.sin(a)) for a in [i * TAU / 10 for i in range(6, -3, -1)]], glow)
T(moon, loc=(dx + 0.12, -D / 2 - 0.085, z0 + 1.25)); P.append(moon)
for z in (0.35, 1.05):
    P.append(box((0.5, 0.03, 0.06), loc=(dx - 0.05, -D / 2 - 0.095, z0 + z), material=stone))
P.append(ico(0.04, loc=(dx + 0.22, -D / 2 - 0.11, z0 + 0.7), material=stone))
# traptreden
P.append(box((0.9, 0.35, 0.16), loc=(dx, -D / 2 - 0.32, 0.08), rot=(0, 0, 0.05), material=stone, bevel=0.02))
# bezem tegen de muur
P.append(cyl(0.025, 1.6, loc=(-1.05, -D / 2 - 0.3, 0.78), rot=(0.25, -0.12, 0), verts=5, material=wdark))
P.append(cone(0.16, 0.4, loc=(-1.0, -D / 2 - 0.12, 0.18), rot=(0.25, -0.12, 0), verts=7, material=wood))
H_ = join(P, 'witch_hut')
# hele huisje scheef: afschuiving naar +x met de hoogte
deform(H_, lambda v: V((v.x + 0.07 * max(0, v.z - z0) - 0.004 * max(0, v.z - z0) ** 2 * 6, v.y, v.z)))
report()
finish('haunted', 'witch_hut', kind='hero', footprint=1.9, notes='scheef heksenhuisje met gelapt dak, schoorsteen, verlichte ramen + maansikkel in de deur (glow_window)')
