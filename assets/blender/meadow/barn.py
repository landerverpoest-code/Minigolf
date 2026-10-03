import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

red = mat('barn_red', '#b5332b', rough=0.8)
white = mat('trim_white', '#f4efe2', rough=0.7)
roof = mat('roof_dark', '#56504e', rough=0.75)
hay = mat('hay', '#e2bf58', rough=0.95)
stone = mat('stone_grey', '#a8a49c', rough=0.9)

W2, D = 3.0, 7.0          # halve breedte (x), diepte (y)
Y0, Y1 = -D / 2, D / 2
# gambrel-profiel (x, z)
P = [(-W2, 0.3), (W2, 0.3), (W2, 3.4), (2.15, 5.35), (0, 6.35), (-2.15, 5.35), (-W2, 3.4)]
parts = []
body = prism(P, D, material=red)
parts.append(body)
# stenen fundering
parts.append(box((2 * W2 + 0.16, D + 0.16, 0.32), loc=(0, 0, 0.16), material=stone, bevel=0.03))

def roof_side(sx):
    """Dakvlakken met 3 overlappende rijen 'pannen' per vlak, overstek."""
    out = []
    segs = [((W2 + 0.3, 3.2), (2.15 + 0.08, 5.42)), ((2.15 + 0.08, 5.42), (0, 6.52))]
    for (a, b) in segs:
        a = Vector((a[0] * sx, 0, a[1])); b = Vector((b[0] * sx, 0, b[1]))
        n = 3
        for k in range(n):
            p0 = a + (b - a) * (k / n) - (b - a) * 0.04
            p1 = a + (b - a) * ((k + 1) / n) + (b - a) * 0.02
            d = (p1 - p0).normalized()
            nrm = Vector((-d.z, 0, d.x)) * (1 if sx < 0 else -1)
            if nrm.z < 0: nrm = -nrm
            off = nrm * (0.09 + 0.02 * (n - k))
            pl = plank(Vector((0, Y0 - 0.35, 0)) + (p0 + p1) / 2 + off - Vector((0, 0, 0)), Vector((0, Y1 + 0.35, 0)) + (p0 + p1) / 2 + off, w=(p1 - p0).length, t=0.16, up=nrm, material=roof)
            out.append(pl)
    return out
# NB plank gaat van p0->p1 langs de lengte; hier bouwen we strips langs Y
def strip(c, length_y, width, nrm, t, material):
    o = box((width, length_y, t), material=material)
    # lokaal: x = breedte, y = lengte, z = dikte -> draai zodat z langs nrm ligt
    ang = math.atan2(nrm.x, nrm.z)
    xform(o, rot=(0, math.degrees(ang), 0), loc=c)
    bev(o, 0.025)
    return o
for sx in (-1, 1):
    segs = [((W2 + 0.35, 3.17), (2.15 + 0.06, 5.45)), ((2.15 + 0.06, 5.45), (0, 6.5))]
    for si, (a, b) in enumerate(segs):
        a = Vector((a[0] * sx, 0, a[1])); b = Vector((b[0] * sx, 0, b[1]))
        n = 3
        for k in range(n):
            t0, t1 = k / n - 0.03, (k + 1) / n + 0.02
            p0 = a + (b - a) * t0; p1 = a + (b - a) * min(t1, 1.0)
            d = (p1 - p0)
            nrm = Vector((-d.z, 0, d.x)).normalized()
            if nrm.z < 0: nrm = -nrm
            c = (p0 + p1) / 2 + nrm * (0.1 + 0.035 * (n - k))
            parts.append(strip(c, D + 0.7, d.length, nrm, 0.14, roof))
# nokbalk
parts.append(box((0.32, D + 0.8, 0.2), loc=(0, 0, 6.66), material=roof, bevel=0.04))

# planken (latten) op de muren
for x in [i * 0.5 - 2.75 for i in range(12)]:
    if abs(x) < 1.35:   # niet over de grote deur
        top = 3.4 + (min(abs(x), 2.15) <= 2.15) * 0
    zt = 3.35 if abs(x) > 2.15 else (3.4 + (2.15 - abs(x)) * (1.95 / 0.85) if abs(x) > 2.15 else 5.3 + (2.15 - abs(x)) / 2.15 * 0.95)
    zb = 3.15 if abs(x) < 1.35 else 0.35
    for y, s in ((Y0 - 0.02, 1), (Y1 + 0.02, -1)):
        if y > 0 or abs(x) >= 1.35 or True:
            zb2 = 0.35 if y > 0 else zb
            if y < 0 and abs(x) < 0.75:   # hooizolderdeur
                for (z0, z1) in ((zb2, 3.85), (5.25, zt)):
                    if z1 - z0 > 0.1:
                        parts.append(box((0.06, 0.04, z1 - z0), loc=(x, y, (z0 + z1) / 2), material=red))
                continue
            parts.append(box((0.06, 0.04, zt - zb2 - 0.05), loc=(x, y, (zt + zb2) / 2 - 0.02), material=red))
for y in [i * 0.5 - 3.25 for i in range(14)]:
    for x in (-W2 - 0.02, W2 + 0.02):
        if abs(y - (-1.6)) < 0.45 or abs(y - 1.4) < 0.45:
            continue   # ramen
        parts.append(box((0.04, 0.06, 3.0), loc=(x, y, 1.88), material=red))

# witte hoekplanken en gevelrand
for x in (-W2, W2):
    for y in (Y0, Y1):
        parts.append(box((0.2, 0.2, 3.15), loc=(x, y, 1.88), material=white, bevel=0.02))
for y in (Y0 - 0.06, Y1 + 0.06):
    for i in range(len(P) - 1):
        if i == 0: continue
        a, b = Vector((P[i][0], y, P[i][1])), Vector((P[(i + 1) % len(P)][0], y, P[(i + 1) % len(P)][1]))
        if i == len(P) - 1: break
        parts.append(plank(a + (a - b).normalized() * 0.12, b + (b - a).normalized() * 0.12, w=0.22, t=0.08, up=(0, 1, 0), material=white, bevel=0.015))
    a, b = Vector((P[-1][0], y, P[-1][1])), Vector((P[2][0], y, P[2][1]))
    parts.append(plank(a, b, w=0.16, t=0.08, up=(0, 1, 0), material=white, bevel=0.015))   # dwarsband op 3.4 m

# grote dubbele schuifdeur met wit kader en X
DW, DH = 2.5, 2.85
yF = Y0 - 0.06
parts.append(box((DW, 0.08, DH), loc=(0, yF, 0.3 + DH / 2), material=red, bevel=0.02))
for sx in (-1, 1):
    cx = sx * DW / 4
    fr = []
    for (dx, dz, w, h) in ((0, DH / 2 - 0.07, DW / 2, 0.14), (0, -DH / 2 + 0.07, DW / 2, 0.14), (-DW / 4 + 0.07, 0, 0.14, DH), (DW / 4 - 0.07, 0, 0.14, DH)):
        fr.append(box((w, 0.08, h), loc=(cx + dx, yF - 0.06, 0.3 + DH / 2 + dz), material=white, bevel=0.015))
    for s2 in (-1, 1):
        a = Vector((cx - DW / 4 + 0.12, yF - 0.06, 0.3 + 0.12)); b = Vector((cx + DW / 4 - 0.12, yF - 0.06, 0.3 + DH - 0.12))
        if s2 < 0:
            a.x, b.x = b.x, a.x
        fr.append(plank(a, b, w=0.13, t=0.07, up=(0, 1, 0), material=white))
    parts += fr
# deurrail
parts.append(box((DW * 2 + 0.4, 0.1, 0.12), loc=(DW / 4, yF - 0.08, 0.3 + DH + 0.12), material=roof, bevel=0.02))

# hooizolder: open luik, donker binnen, hooi steekt uit, met kader
parts.append(box((1.3, 0.1, 1.4), loc=(0, Y0 + 0.01, 4.55), material=roof))
for (dx, dz, w, h) in ((0, 0.72, 1.6, 0.16), (0, -0.72, 1.6, 0.16), (-0.72, 0, 0.16, 1.6), (0.72, 0, 0.16, 1.6)):
    parts.append(box((w, 0.1, h), loc=(dx, Y0 - 0.08, 4.55 + dz), material=white, bevel=0.015))
# open luikdeur tegen de muur (rood met wit X)
ld = box((0.62, 0.06, 1.3), loc=(-1.15, Y0 - 0.12, 4.55), material=red, bevel=0.015)
parts.append(ld)
parts.append(plank((-1.4, Y0 - 0.16, 4.0), (-0.9, Y0 - 0.16, 5.1), w=0.09, t=0.04, up=(0, 1, 0), material=white))
parts.append(plank((-0.9, Y0 - 0.16, 4.0), (-1.4, Y0 - 0.16, 5.1), w=0.09, t=0.04, up=(0, 1, 0), material=white))
# hooi in de opening
hb = ico(0.5, sub=2, material=hay, scale=(1.2, 0.6, 0.55))
jitter(hb, 0.06, seed=3)
xform(hb, loc=(0.05, Y0 - 0.05, 4.05))
parts.append(hb)
for k in range(7):
    a = -1.0 + k * 0.33
    p0 = Vector((0.4 * math.sin(a * 1.4), Y0 - 0.1, 4.0 + 0.1 * math.cos(a)))
    p1 = p0 + Vector((0.25 * math.sin(a), -0.25, -0.15 + 0.08 * k % 0.2))
    parts.append(rod(p0, p1, 0.035, 0.0, verts=3, material=hay))
# takelbalk onder de nok
parts.append(box((0.16, 1.0, 0.16), loc=(0, Y0 - 0.3, 5.75), material=white, bevel=0.02))
parts.append(rod((0, Y0 - 0.72, 5.67), (0, Y0 - 0.72, 5.25), 0.012, verts=4, material=roof))
parts.append(torus(0.06, 0.015, loc=(0, Y0 - 0.72, 5.2), rot=(0, math.pi / 2, 0), seg=8, ring=4, material=roof))

# zolderraam op de achtergevel
parts.append(box((0.9, 0.06, 0.9), loc=(0, Y1 + 0.03, 4.6), material=roof))
for (dx, dz, w, h) in ((0, 0.5, 1.12, 0.14), (0, -0.5, 1.12, 0.14), (-0.5, 0, 0.14, 1.12), (0.5, 0, 0.14, 1.12), (0, 0, 0.07, 0.9), (0, 0, 0.9, 0.07)):
    parts.append(box((w, 0.08, h), loc=(dx, Y1 + 0.08, 4.6 + dz), material=white))
# ramen op de zijmuren
for x in (-W2 - 0.06, W2 + 0.06):
    for y in (-1.6, 1.4):
        sx = 1 if x > 0 else -1
        parts.append(box((0.06, 0.8, 0.8), loc=(x - sx * 0.04, y, 2.0), material=roof))
        for (dy, dz, w, h) in ((0, 0.44, 1.0, 0.12), (0, -0.44, 1.0, 0.12), (-0.44, 0, 0.12, 1.0), (0.44, 0, 0.12, 1.0), (0, 0, 0.06, 0.8), (0, 0, 0.8, 0.06)):
            parts.append(box((0.08, w, h), loc=(x + sx * 0.01, y + dy, 2.0 + dz), material=white))
        # vensterbank
        parts.append(box((0.16, 1.05, 0.06), loc=(x + sx * 0.05, y, 1.53), material=white))

# koepeltje (cupola) op de nok met windhaan
cz = 6.75
parts.append(box((0.9, 0.9, 0.7), loc=(0, 0.5, cz + 0.35), material=white, bevel=0.03))
for sy in (-1, 1):
    for k in range(3):
        parts.append(box((0.6, 0.04, 0.05), loc=(0, 0.5 + sy * 0.46, cz + 0.2 + k * 0.15), material=roof))
for sx in (-1, 1):
    for k in range(3):
        parts.append(box((0.04, 0.6, 0.05), loc=(sx * 0.46, 0.5, cz + 0.2 + k * 0.15), material=roof))
cr = cone(0.78, 0.55, loc=(0, 0.5, cz + 0.98), verts=4, rot=(0, 0, math.pi / 4), material=roof)
parts.append(cr)
parts.append(rod((0, 0.5, cz + 1.2), (0, 0.5, cz + 1.75), 0.025, verts=5, material=roof))
for (a, b) in (((-0.25, 0.5), (0.25, 0.5)), ((0, 0.25), (0, 0.75))):
    parts.append(rod((a[0], a[1], cz + 1.55), (b[0], b[1], cz + 1.55), 0.012, verts=4, material=roof))
# haantje (silhouet)
rooster = prism([(-0.22, 0), (0.05, 0), (0.12, 0.1), (0.2, 0.12), (0.22, 0.22), (0.15, 0.27), (0.1, 0.18), (-0.05, 0.12), (-0.22, 0.28), (-0.25, 0.1)], 0.03, material=roof)
xform(rooster, rot=(0, 0, 0), loc=(0, 0.5, cz + 1.68))
parts.append(rooster)

# lampje boven de deur
parts.append(box((0.06, 0.3, 0.06), loc=(1.55, Y0 - 0.2, 3.35), material=roof))
parts.append(cone(0.16, 0.12, loc=(1.55, Y0 - 0.35, 3.25), verts=8, material=roof))
parts.append(sphere(0.07, loc=(1.55, Y0 - 0.35, 3.15), seg=8, rings=5, material=hay))

# silo (achter rechts) met banden en koepel
SX, SY, SR, SH = W2 + 1.05, 1.6, 1.15, 6.6
prof = [(SR, 0)]
for k in range(5):
    z = 0.6 + k * 1.25
    prof += [(SR, z), (SR + 0.07, z + 0.035), (SR + 0.07, z + 0.125), (SR, z + 0.16)]
prof += [(SR, SH)]
silo = lathe(prof, seg=16, material=stone, cap_bottom=False, cap_top=False)
for p in silo.data.polygons:
    rr = Vector((p.center.x, p.center.y)).length
    if rr > SR + 0.03:
        p.material_index = 0
silo.data.materials.append(white)
for p in silo.data.polygons:
    if Vector((p.center.x, p.center.y)).length > SR + 0.025:
        p.material_index = 1
xform(silo, loc=(SX, SY, 0))
smooth(silo, 50)
parts.append(silo)
dome = lathe([(SR + 0.1, SH - 0.05), (SR + 0.1, SH + 0.05), (SR * 0.9, SH + 0.45), (SR * 0.55, SH + 0.82), (0.2, SH + 0.98), (0.2, SH + 1.12), (0, SH + 1.16)], seg=16, material=red)
xform(dome, loc=(SX, SY, 0))
smooth(dome, 40)
parts.append(dome)
# ladder langs de silo
for sx in (-1, 1):
    parts.append(box((0.05, 0.05, SH - 0.5), loc=(SX + sx * 0.2, SY - SR - 0.12, (SH - 0.5) / 2 + 0.4), material=white))
for k in range(12):
    parts.append(box((0.4, 0.04, 0.04), loc=(SX, SY - SR - 0.12, 0.8 + k * 0.48), material=white))
# verbindingsstuk silo-schuur
parts.append(box((0.6, 1.2, 3.0), loc=(W2 + 0.2, SY, 1.5), material=red, bevel=0.03))
parts.append(box((0.8, 1.4, 0.15), loc=(W2 + 0.25, SY, 3.05), rot=(0.0, 0.25, 0), material=roof))

# wat hooi en een baal bij de deur
bale = box((0.9, 0.5, 0.45), material=hay, bevel=0.05)
jitter(bale, 0.015, seed=2)
xform(bale, rot=(0, 0, 18), loc=(-2.1, Y0 - 0.8, 0.225))
parts.append(bale)
for dx in (-0.2, 0.2):
    tw = box((0.03, 0.52, 0.47), material=red)
    xform(tw, loc=(dx, 0, 0.225)); xform(tw, rot=(0, 0, 18), loc=(-2.1, Y0 - 0.8, 0))
    parts.append(tw)
bale2 = box((0.9, 0.5, 0.45), material=hay, bevel=0.05)
jitter(bale2, 0.015, seed=3)
xform(bale2, rot=(0, 0, -5), loc=(-2.0, Y0 - 0.85, 0.675))
parts.append(bale2)

barn = join(parts, 'barn')
smooth(barn, 45)
report()
finish('meadow', 'barn', kind='hero', footprint=4.6, notes='rode schuur met wit lijstwerk, gambreldak met pannenrijen, schuifdeuren met X, open hooizolder, koepeltje met windhaan, silo met ladder')
