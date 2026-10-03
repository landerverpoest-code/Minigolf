import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_grey', '#a49a8c', rough=0.9)
wood = mat('wood_boards', '#8a5a34', rough=0.85)
red = mat('cap_red', '#b5332b', rough=0.75)
white = mat('trim_white', '#f4efe2', rough=0.7)
cloth = mat('sail_cloth', '#efe2c4', rough=0.9)

SEG = 8
PH = math.pi / 8   # vlakke kant naar voren (-Y)
parts = []
# --- stenen voet ---
B0, BH = 1.95, 1.6
prof = [(B0, 0)]
for k in range(4):
    z0 = k * 0.4
    r = B0 - 0.06 * (z0 / BH)
    prof += [(r, z0 + 0.03), (r - 0.025, z0 + 0.03), (r - 0.025, z0 + 0.06) if False else (r, z0 + 0.06)]
prof = [(B0, 0)] + [(B0 - 0.04 * k, 0.4 * k + 0.37) for k in range(4)]
base = lathe([(B0, 0), (B0 - 0.02, BH * 0.5), (B0 - 0.06, BH)], seg=SEG, material=stone, phase=PH, cap_bottom=False)
parts.append(base)
# uitstekende stenen (karakter)
rnd = random.Random(2)
for k in range(26):
    a = rnd.uniform(0, TAU); z = rnd.uniform(0.15, BH - 0.15)
    if abs(math.atan2(math.sin(a + math.pi / 2), math.cos(a + math.pi / 2))) < 0.5:   # niet over de deur
        continue
    r = B0 - 0.06 * z / BH - 0.02
    b = box((0.12, rnd.uniform(0.35, 0.6), rnd.uniform(0.2, 0.3)), material=cloth, bevel=0.03)
    xform(b, loc=(r, 0, z)); xform(b, rot=(0, 0, math.degrees(a)))
    parts.append(b)
# --- omloop (stelling) met reling ---
SR = 2.45
stage = lathe([(SR, BH - 0.1), (SR, BH + 0.05), (1.6, BH + 0.05), (1.6, BH - 0.1)], seg=SEG, material=wood, phase=PH, cap_bottom=False, cap_top=False)
parts.append(stage)
for k in range(SEG):
    a = TAU * k / SEG + PH
    # schoren onder de stelling
    parts.append(rod((1.85 * math.cos(a), 1.85 * math.sin(a), BH - 0.7), (2.3 * math.cos(a), 2.3 * math.sin(a), BH - 0.1), 0.05, verts=4, material=wood))
for k in range(16):
    a = TAU * k / 16 + PH
    if 11 <= k <= 13:   # opening aan de voorkant rechts? (trapje) -> geen paal
        pass
    parts.append(box((0.07, 0.07, 0.75), loc=(2.35 * math.cos(a), 2.35 * math.sin(a), BH + 0.42), material=white))
rail = lathe([(2.39, BH + 0.78), (2.39, BH + 0.86), (2.31, BH + 0.86), (2.31, BH + 0.78)], seg=16, material=white, cap_bottom=False, cap_top=False)
parts.append(rail)
rail2 = lathe([(2.37, BH + 0.4), (2.37, BH + 0.45), (2.33, BH + 0.45), (2.33, BH + 0.4)], seg=16, material=white, cap_bottom=False, cap_top=False)
parts.append(rail2)

# --- houten achtkant met overnaadse planken ---
z0, z1, r0, r1 = BH, 5.8, 1.7, 1.08
prof = []
nb = 9
for k in range(nb):
    za = z0 + (z1 - z0) * k / nb
    zb = z0 + (z1 - z0) * (k + 1) / nb
    ra = r0 + (r1 - r0) * k / nb
    rb = r0 + (r1 - r0) * (k + 1) / nb
    prof += [(ra + 0.05, za), (rb, zb - 0.02)]
prof += [(r1, z1)]
body = lathe(prof, seg=SEG, material=wood, phase=PH, cap_bottom=False)
parts.append(body)
# witte hoekribben
for k in range(SEG):
    a = TAU * k / SEG + PH + math.pi / SEG
    rc = 1 / math.cos(math.pi / SEG)
    parts.append(plank((r0 * rc * math.cos(a) * 1.01, r0 * rc * math.sin(a) * 1.01, z0), (r1 * rc * math.cos(a) * 1.01, r1 * rc * math.sin(a) * 1.01, z1), w=0.12, t=0.08, up=(math.cos(a), math.sin(a), 0), material=white))
# kraag onder de kap
parts.append(lathe([(r1 + 0.12, z1 - 0.05), (r1 + 0.12, z1 + 0.12), (r1 - 0.2, z1 + 0.12)], seg=SEG, material=white, phase=PH, cap_bottom=True, cap_top=False))

def window(a, z, r, w=0.42, h=0.55):
    """Venster op de achtkant (hoek a), raam donker met wit kader."""
    out = []
    n = Vector((math.cos(a), math.sin(a), 0))
    t = Vector((-n.y, n.x, 0))
    c = n * r + Vector((0, 0, z))
    g = box((w, 0.05, h), material=red)
    out.append(g)
    for (dx, dz, ww, hh) in ((0, h / 2 + 0.04, w + 0.16, 0.08), (0, -h / 2 - 0.04, w + 0.2, 0.08), (-w / 2 - 0.04, 0, 0.08, h), (w / 2 + 0.04, 0, 0.08, h), (0, 0, 0.04, h), (0, 0, w, 0.04)):
        out.append(box((ww, 0.07, hh), loc=(dx, -0.02, dz), material=white))
    for o in out:
        xform(o, rot=(0, 0, math.degrees(a) + 90), loc=c)
    return out
# r op hoogte z (vlak midden)
def body_r(z):
    return r0 + (r1 - r0) * (z - z0) / (z1 - z0) + 0.04
parts += window(-math.pi / 2, 3.1, body_r(3.1))
parts += window(-math.pi / 2 + math.pi / 4 * 2, 4.4, body_r(4.4))
parts += window(math.pi, 2.6, body_r(2.6))
# deur in de stenen voet (voorkant) met boog
dz = 0.0
door = box((0.85, 0.12, 1.15), loc=(0, -B0 + 0.04, 0.6), material=wood, bevel=0.02)
parts.append(door)
arch = cyl(0.425, 0.12, loc=(0, -B0 + 0.04, 1.17), rot=(math.pi / 2, 0, 0), verts=10, material=wood)
parts.append(arch)
for (dx, z) in ((-0.5, 0.6), (0.5, 0.6)):
    parts.append(box((0.14, 0.14, 1.25), loc=(dx, -B0 + 0.0, z + 0.02), material=white, bevel=0.02))
arch2 = lathe([(0.57, -0.07), (0.57, 0.07), (0.43, 0.07), (0.43, -0.07)], seg=12, material=white, cap_bottom=False, cap_top=False)
bm = bmesh.new(); bm.from_mesh(arch2.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.01], context='VERTS')
bm.to_mesh(arch2.data); bm.free()
xform(arch2, rot=(90, 0, 0), loc=(0, -B0 + 0.0, 1.2))
parts.append(arch2)
parts.append(box((1.3, 0.5, 0.12), loc=(0, -B0 - 0.2, 0.06), material=stone, bevel=0.03))   # stoep
parts.append(sphere(0.04, loc=(0.28, -B0 - 0.05, 0.6), seg=6, rings=4, material=white))

# --- kap: langgerekte koepel, rood ---
CZ = z1 + 0.1
cap = lathe([(1.3, CZ), (1.32, CZ + 0.2), (1.12, CZ + 0.65), (0.75, CZ + 1.0), (0.3, CZ + 1.18), (0, CZ + 1.22)], seg=12, material=red)
xform(cap, scale=(1.0, 1.3, 1.0))
smooth(cap, 40)
parts.append(cap)
# nokbalk
parts.append(box((0.14, 2.4, 0.14), loc=(0, 0.2, CZ + 1.2), material=white, bevel=0.03))
# staart (kruiwerk) aan de achterkant naar de stelling
parts.append(plank((0, 1.4, CZ + 0.3), (0, SR + 0.25, BH + 0.95), w=0.16, t=0.16, material=wood))
parts.append(plank((-0.5, 1.5, CZ + 0.1), (0, SR + 0.2, BH + 1.2), w=0.09, t=0.09, material=wood))
parts.append(plank((0.5, 1.5, CZ + 0.1), (0, SR + 0.2, BH + 1.2), w=0.09, t=0.09, material=wood))
wheel = torus(0.35, 0.04, loc=(0, SR + 0.3, BH + 1.05), rot=(0, math.pi / 2, 0), seg=10, ring=4, material=white)
parts.append(wheel)
for k in range(3):
    a = k * math.pi / 3
    parts.append(rod((0, SR + 0.3 + 0.35 * math.cos(a), BH + 1.05 + 0.35 * math.sin(a)), (0, SR + 0.3 - 0.35 * math.cos(a), BH + 1.05 - 0.35 * math.sin(a)), 0.02, verts=4, material=white))

# as (windas) en naaf
HUB = Vector((0, -1.75, CZ + 0.45))
parts.append(rod((0, -0.6, HUB.z), (0, HUB.y + 0.15, HUB.z), 0.17, verts=8, material=wood))
mill = join(parts, 'windmill')
smooth(mill, 40)

# --- wieken (apart object, draaien rond de as) ---
sp = []
sp.append(rod((0, HUB.y + 0.2, HUB.z), (0, HUB.y - 0.25, HUB.z), 0.28, 0.22, verts=10, material=wood))
sp.append(cone(0.22, 0.25, loc=(0, HUB.y - 0.37, HUB.z), rot=(math.pi / 2, 0, 0), verts=10, material=red))
L = 3.75
for k in range(4):
    ang = TAU * k / 4 + math.radians(20)
    arm = []
    # roede (hoofdbalk)
    arm.append(box((0.16, 0.16, L), loc=(0, 0, L / 2 - 0.1), material=white))
    # hekwerk aan één kant
    w0, w1 = 0.12, 0.95
    zr0, zr1 = 0.75, L - 0.05
    arm.append(box((0.07, 0.07, zr1 - zr0), loc=(w1, 0, (zr0 + zr1) / 2), material=white))
    arm.append(box((0.05, 0.05, zr1 - zr0), loc=(-0.25, 0, (zr0 + zr1) / 2), material=white))
    nbars = 9
    for b in range(nbars + 1):
        z = zr0 + (zr1 - zr0) * b / nbars
        arm.append(box((w1 + 0.25 + 0.04, 0.05, 0.05), loc=((w1 - 0.25) / 2, 0.02, z), material=white))
    # zeildoek op twee wieken, deels opgerold
    if k % 2 == 0:
        c = box((w1 - 0.1, 0.03, (zr1 - zr0) * 0.62), loc=((w1 + 0.08) / 2 + 0.02, 0.07, zr1 - (zr1 - zr0) * 0.31), material=cloth)
        bend(c, lambda v: (v.x, v.y - 0.06 * math.sin(max(0, min(1, (v.x - 0.1) / (w1 - 0.1))) * math.pi), v.z))
        arm.append(c)
        roll = rod((0.1, 0.06, zr1 - (zr1 - zr0) * 0.62), (w1, 0.06, zr1 - (zr1 - zr0) * 0.62), 0.06, verts=6, material=cloth)
        arm.append(roll)
    else:
        # opgerold doek langs de roede
        arm.append(rod((0.2, 0.05, zr0), (0.2, 0.05, zr1), 0.07, verts=6, material=cloth))
    a_o = join(arm, 'arm')
    xform(a_o, rot=(0, math.degrees(ang), 0), loc=HUB)
    sp.append(a_o)
sails = join(sp, 'spin_sails')
smooth(sails, 40)
set_origin(sails, HUB)
report()
finish('meadow', 'windmill', kind='hero', footprint=2.6, notes='molen: stenen voet, houten achtkant met overnaadse planken, omloop met reling, rode kap met staart; 4 hekwerkwieken (deels met zeil) als spin_sails',
       spin=[{'node': 'spin_sails', 'axis': 'z', 'speed': 0.9}])
