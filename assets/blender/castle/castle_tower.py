import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_warm', '#a69c8f', rough=0.9)
roof = mat('roof_blue', '#3c62b5', rough=0.6)
dark = mat('wood_dark', '#4a3220', rough=0.85)
red = mat('banner_red', '#c0392f', rough=0.8)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)

rnd = random.Random(21)
SEG = 16
R0, R1, HB = 2.3, 2.05, 7.2   # voet-, topstraal, hoogte romp
parts = []
# romp met beschoeide voet en twee lijsten
body = lathe([(R0 + 0.35, 0.0), (R0 + 0.12, 0.7), (R0, 1.0), (R0 - 0.05, 3.5), (R1, HB)], seg=SEG, material=stone, cap_bottom=False)
smooth(body, 30)
parts.append(body)
def r_at(z):
    return R0 + (R1 - R0) * max(0, z - 1.0) / (HB - 1.0) if z >= 1.0 else R0 + 0.35 * (1 - z)
for z in (1.0, 4.2):
    parts.append(lathe([(r_at(z) + 0.1, z - 0.08), (r_at(z) + 0.1, z + 0.08), (r_at(z) - 0.02, z + 0.12)], seg=SEG, material=stone, cap_bottom=True, cap_top=False))
# uitstekende stenen voor metselwerk-karakter
for k in range(46):
    a = rnd.uniform(0, TAU); z = rnd.uniform(1.2, HB - 0.4)
    if abs(math.atan2(math.sin(a + math.pi / 2), math.cos(a + math.pi / 2))) < 0.45 and z < 3.2:
        continue
    b = box((0.12, rnd.uniform(0.4, 0.7), rnd.uniform(0.22, 0.32)), material=stone)
    xform(b, loc=(r_at(z) - 0.02, 0, z)); xform(b, rot=(0, 0, math.degrees(a)))
    parts.append(b)
# schietgaten (donker) met stenen omlijsting
def slit(a, z, h=0.75):
    out = []
    r = r_at(z)
    s = box((0.13, 0.12, h), material=dark)
    xform(s, loc=(r + 0.0, 0, z)); out.append(s)
    for dz in (h / 2 + 0.06, -h / 2 - 0.06):
        f = box((0.16, 0.36, 0.12), material=stone)
        xform(f, loc=(r + 0.02, 0, z + dz)); out.append(f)
    for dy in (-0.13, 0.13):
        f = box((0.16, 0.1, h), material=stone)
        xform(f, loc=(r + 0.02, dy, z)); out.append(f)
    # slit staat als blok tangentieel -> draaien rond z
    for o in out:
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(r, 0, z), matrix=Matrix.Rotation(math.pi / 2, 3, 'Z'))
        bm.to_mesh(o.data); bm.free()
        xform(o, rot=(0, 0, math.degrees(a)))
    return out
# NB: de rotatie hierboven zet het gat 'plat' tegen de muur: x=dikte, y=breedte
def slit2(a, z, h=0.75):
    out = []
    r = r_at(z)
    for (w, d, hh, dy, dz, m) in ((0.14, 0.14, h, 0, 0, dark), (0.38, 0.16, 0.12, 0, h / 2 + 0.06, stone), (0.38, 0.16, 0.12, 0, -h / 2 - 0.06, stone), (0.1, 0.16, h, -0.14, 0, stone), (0.1, 0.16, h, 0.14, 0, stone)):
        b = box((d, w, hh), material=m)
        xform(b, loc=(r + 0.02, dy, z + dz))
        xform(b, rot=(0, 0, math.degrees(a)))
        out.append(b)
    return out
for (a, z) in ((-90, 3.2), (-90, 5.6), (-20, 4.8), (-160, 4.4), (30, 2.6), (90, 5.4), (150, 3.2), (-45, 6.4)):
    parts += slit2(math.radians(a), z)
# deur met boog, ijzerbeslag (donker hout) en gouden ring
DY = -r_at(0.9) - 0.05
parts.append(box((1.1, 0.3, 1.5), loc=(0, DY + 0.1, 0.75), material=dark, bevel=0.03))
parts.append(cyl(0.55, 0.3, loc=(0, DY + 0.1, 1.5), rot=(math.pi / 2, 0, 0), verts=12, material=dark))
for k in range(5):
    parts.append(box((0.04, 0.05, 1.9), loc=(-0.44 + k * 0.22, DY - 0.07, 1.0), material=dark))
arch = lathe([(0.78, -0.12), (0.78, 0.12), (0.58, 0.12), (0.58, -0.12)], seg=14, material=stone, cap_bottom=False, cap_top=False)
bm = bmesh.new(); bm.from_mesh(arch.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.01], context='VERTS')
bm.to_mesh(arch.data); bm.free()
xform(arch, rot=(90, 0, 0), loc=(0, DY - 0.02, 1.5))
parts.append(arch)
for sx in (-1, 1):
    parts.append(box((0.22, 0.26, 1.55), loc=(sx * 0.68, DY - 0.02, 0.78), material=stone, bevel=0.02))
parts.append(torus(0.09, 0.022, loc=(0.25, DY - 0.1, 0.95), rot=(math.pi / 2, 0, 0), seg=8, ring=4, material=gold))

# --- weergang: kraagstenen, borstwering met kantelen ---
RP = R1 + 0.4
for k in range(SEG):
    a = TAU * (k + 0.5) / SEG
    c = box((0.5, 0.26, 0.5), material=stone)
    bend(c, lambda v: (v.x, v.y, v.z + (0.25 * (v.x + 0.25) / 0.5 if v.z < 0 else 0)))
    xform(c, loc=(R1 + 0.15, 0, HB - 0.1))
    xform(c, rot=(0, 0, math.degrees(a)))
    parts.append(c)
parapet = lathe([(RP, HB + 0.1), (RP, HB + 0.85), (RP - 0.3, HB + 0.85), (RP - 0.3, HB + 0.2)], seg=SEG, material=stone, cap_bottom=False, cap_top=False)
parts.append(parapet)
parts.append(lathe([(RP + 0.05, HB + 0.05), (RP + 0.05, HB + 0.18), (R1 - 0.1, HB + 0.18)], seg=SEG, material=stone, cap_bottom=True, cap_top=False))
for k in range(12):
    a = TAU * k / 12
    m = box((0.3, 0.62, 0.55), material=stone, bevel=0.03)
    xform(m, loc=(RP - 0.15, 0, HB + 0.85 + 0.27))
    xform(m, rot=(0, 0, math.degrees(a)))
    parts.append(m)

# --- kegeldak (licht uitlopend) met pannenringen, goud topje en vlag ---
RZ = HB + 0.55
rprof = [(R1 + 0.35, RZ), (R1 + 0.05, RZ + 0.45)]
for k in range(1, 8):
    t = k / 8
    z = RZ + 0.45 + t * 3.95
    r = (R1 + 0.05) * (1 - t) ** 1.15
    rprof += [(r + 0.06, z - 0.02), (r, z)]
rprof += [(0, RZ + 4.6)]
rf = lathe(rprof, seg=SEG, material=roof, cap_bottom=True)
smooth(rf, 35)
parts.append(rf)
# dakkapel (klein venstertje) op het dak
dk = box((0.55, 0.6, 0.55), loc=(0, -1.6, RZ + 1.1), material=stone, bevel=0.02)
parts.append(dk)
parts.append(box((0.24, 0.06, 0.32), loc=(0, -1.86, RZ + 1.1), material=dark))
dkr = prism([(-0.4, 0), (0.4, 0), (0, 0.38)], 0.75, material=roof)
xform(dkr, loc=(0, -1.6, RZ + 1.37))
parts.append(dkr)
TOPZ = RZ + 4.6
parts.append(sphere(0.16, loc=(0, 0, TOPZ + 0.05), seg=8, rings=6, material=gold))
parts.append(rod((0, 0, TOPZ), (0, 0, TOPZ + 1.3), 0.04, verts=6, material=gold))
flag = prism([(0, 0), (0.95, 0.12), (0.75, 0.25), (0.95, 0.4), (0, 0.5)], 0.03, material=red)
bend(flag, lambda c: (c.x, c.y + 0.08 * math.sin(c.x * 5), c.z))
xform(flag, loc=(0.04, 0, TOPZ + 0.75))
parts.append(flag)
# hangend wapenschild-vaandel aan de borstwering (voorkant)
ban = prism([(-0.5, 0), (0.5, 0), (0.5, -1.6), (0, -1.95), (-0.5, -1.6)], 0.05, material=red)
xform(ban, loc=(0, -RP - 0.05, HB + 0.75))
parts.append(ban)
parts.append(box((1.15, 0.1, 0.1), loc=(0, -RP - 0.1, HB + 0.75), material=gold))
emb = prism([(0, 0.32), (0.25, 0), (0, -0.32), (-0.25, 0)], 0.04, material=gold)
xform(emb, loc=(0, -RP - 0.1, HB - 0.35))
parts.append(emb)
t = join(parts, 'castle_tower')
smooth(t, 30)
report()
finish('castle', 'castle_tower', kind='hero', footprint=2.7, notes='ronde stenen toren: beschoeide voet, schietgaten, boogdeur, kraagstenen + kantelen, blauw kegeldak met pannenringen en dakkapel, gouden topje, rode vlag en vaandel (statisch)')
