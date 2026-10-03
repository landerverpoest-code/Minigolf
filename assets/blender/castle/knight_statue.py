import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

st = mat('statue_stone', '#b3a895', rough=0.8)
pl = mat('stone_dark', '#877c70', rough=0.9)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)
moss = mat('moss', '#5c8a35', rough=0.95)
dark = mat('slit_dark', '#3a332d', rough=0.9)

parts = []
# --- sokkel ---
parts.append(box((1.9, 1.9, 0.28), loc=(0, 0, 0.14), material=pl, bevel=0.05))
parts.append(box((1.6, 1.6, 0.16), loc=(0, 0, 0.36), material=pl, bevel=0.04))
ped = box((1.25, 1.25, 1.0), loc=(0, 0, 0.94), material=pl, bevel=0.04)
parts.append(ped)
parts.append(box((1.45, 1.45, 0.16), loc=(0, 0, 1.5), material=pl, bevel=0.04))
# hoekpilasters
for sx in (-1, 1):
    for sy in (-1, 1):
        parts.append(box((0.16, 0.16, 1.0), loc=(sx * 0.62, sy * 0.62, 0.94), material=pl, bevel=0.03))
# gouden plaquette met rand
parts.append(box((0.62, 0.05, 0.34), loc=(0, -0.64, 0.98), material=gold, bevel=0.015))
for k in range(3):
    parts.append(box((0.42 - k * 0.08, 0.02, 0.025), loc=(0, -0.67, 1.06 - k * 0.07), material=dark))
# mos op de sokkel
for p_ in [o for o in parts]:
    pass
P = 1.58
# --- ridder ---
def S(o):
    parts.append(o); return o
for sx in (-1, 1):
    x = sx * 0.17
    S(box((0.17, 0.3, 0.12), loc=(x, -0.05, P + 0.06), material=st, bevel=0.03))                 # voet
    S(rod((x, 0, P + 0.1), (x, 0, P + 0.66), 0.105, 0.125, verts=8, material=st))                 # scheen
    S(sphere(0.125, loc=(x, -0.02, P + 0.69), seg=8, rings=6, material=st))                        # knie
    S(rod((x, 0, P + 0.7), (x * 1.05, 0, P + 1.12), 0.14, 0.165, verts=8, material=st))            # dij
# lendenstuk (rok van platen)
S(lathe([(0.37, P + 0.98), (0.34, P + 1.12), (0.31, P + 1.24), (0.29, P + 1.36)], seg=10, material=st, cap_bottom=True, cap_top=False))
S(lathe([(0.3, P + 1.33), (0.3, P + 1.41)], seg=10, material=gold, cap_bottom=False, cap_top=False))   # riem
S(box((0.1, 0.04, 0.09), loc=(0, -0.3, P + 1.37), material=gold))                                    # gesp
# borstkuras
torso = lathe([(0.29, P + 1.38), (0.32, P + 1.6), (0.35, P + 1.8), (0.32, P + 1.98), (0.18, P + 2.06)], seg=10, material=st, cap_bottom=False, cap_top=True)
xform(torso, scale=(1.0, 0.72, 1.0))
S(torso)
S(box((0.05, 0.05, 0.4), loc=(0, -0.24, P + 1.75), material=st, bevel=0.015))   # middenrib
# halsberg + helm
S(rod((0, 0, P + 2.0), (0, 0, P + 2.12), 0.15, verts=8, material=st))
helm = lathe([(0.19, P + 2.08), (0.2, P + 2.38), (0.18, P + 2.48), (0.1, P + 2.55), (0, P + 2.57)], seg=10, material=st)
S(helm)
S(box((0.3, 0.06, 0.035), loc=(0, -0.19, P + 2.33), material=dark))   # vizierspleet
S(box((0.035, 0.06, 0.16), loc=(0, -0.195, P + 2.22), material=dark))
for k in range(3):
    S(box((0.025, 0.05, 0.025), loc=(0.09, -0.18, P + 2.22 - k * 0.05), material=dark))
crest = prism([(-0.17, 0), (0.15, 0), (0.08, 0.2), (-0.05, 0.26), (-0.2, 0.12)], 0.05, axis='X', material=gold)
xform(crest, loc=(0, 0.0, P + 2.52))
S(crest)
# schouderstukken (2 lagen)
for sx in (-1, 1):
    for k, (r, dz) in enumerate(((0.19, 0.0), (0.16, -0.1))):
        pd = sphere(r, seg=8, rings=5, material=st, scale=(1.1, 1.0, 0.7))
        xform(pd, rot=(0, sx * -18, 0), loc=(sx * (0.36 + k * 0.03), 0, P + 1.95 + dz))
        S(pd)
# armen: handen samen op de pareerstang van het zwaard
SY = -0.42
for sx in (-1, 1):
    sh = Vector((sx * 0.38, 0.0, P + 1.86))
    el = Vector((sx * 0.37, -0.13, P + 1.52))
    hd = Vector((sx * 0.07, SY, P + 1.42))
    S(rod(sh, el, 0.09, 0.085, verts=7, material=st))
    S(sphere(0.09, loc=el, seg=7, rings=5, material=st))
    S(rod(el, hd, 0.085, 0.075, verts=7, material=st))
    S(box((0.12, 0.13, 0.11), loc=hd + Vector((sx * 0.01, 0, 0.02)), material=st, bevel=0.03))
# zwaard, punt op de sokkel
S(box((0.5, 0.07, 0.06), loc=(0, SY, P + 1.33), material=gold, bevel=0.015))          # pareerstang
S(rod((0, SY, P + 1.36), (0, SY, P + 1.6), 0.035, verts=6, material=st))               # greep
S(sphere(0.06, loc=(0, SY, P + 1.64), seg=8, rings=5, material=gold))                  # knop
blade = prism([(-0.055, 0), (0.055, 0), (0.045, -1.2), (0, -1.3), (-0.045, -1.2)], 0.035, material=st)
xform(blade, loc=(0, SY, P + 1.3))
S(blade)
S(box((0.015, 0.04, 0.9), loc=(0, SY - 0.01, P + 0.75), material=st))                  # bloedgroef-rib
# schild (heater) tegen het linkerbeen, met gouden kruis en rand
sh = prism([(-0.32, 0.25), (0.32, 0.25), (0.3, -0.2), (0.12, -0.5), (0, -0.58), (-0.12, -0.5), (-0.3, -0.2)], 0.06, axis='X', material=st)
rim = prism([(-0.36, 0.29), (0.36, 0.29), (0.34, -0.22), (0.14, -0.55), (0, -0.64), (-0.14, -0.55), (-0.34, -0.22)], 0.04, axis='X', material=pl)
cr1 = box((0.03, 0.09, 0.62), loc=(0.04, 0, -0.12), material=gold)
cr2 = box((0.03, 0.5, 0.09), loc=(0.04, 0, 0.05), material=gold)
for o in (sh, rim, cr1, cr2):
    xform(o, loc=(0.0 if o in (sh, rim) else 0.0, 0, 0))
xform(rim, loc=(-0.03, 0, 0))
shield = join([rim, sh, cr1, cr2], 'shield')
xform(shield, rot=(0, -12, -25), loc=(0.5, -0.12, P + 0.62))
S(shield)
# cape achter de rug
cv, cf = [], []
rows, cols = 4, 6
for j in range(rows + 1):
    t = j / rows
    z = P + 1.95 - t * 1.4
    w = 0.3 + 0.22 * t
    for i in range(cols + 1):
        u = i / cols - 0.5
        a = u * math.pi * 0.9
        cv.append((w * math.sin(a) * 1.35, 0.12 + 0.12 * t + w * math.cos(a) * 0.55 + 0.03 * math.sin(i * 2.1 + j), z))
for j in range(rows):
    for i in range(cols):
        a = j * (cols + 1) + i
        cf.append((a, a + 1, a + cols + 2, a + cols + 1))
n = len(cv)
cv2 = [(x * 0.97, y - 0.03, z) for (x, y, z) in cv]
cf2 = [tuple(reversed([k + n for k in f])) for f in cf]
cape = mesh_obj(cv + cv2, cf + cf2, st)
S(cape)
# mos op enkele bovenvlakken van de sokkel
o = join(parts, 'knight_statue')
mi = len(o.data.materials)
o.data.materials.append(moss)
pli = [m.name for m in o.data.materials].index('stone_dark')
sti = [m.name for m in o.data.materials].index('statue_stone')
for p_ in o.data.polygons:
    nz = noise.noise(p_.center * 3.0 + Vector((1, 2, 3)))
    if p_.material_index == pli and p_.normal.z > 0.8 and nz > 0.15:
        p_.material_index = mi
    elif p_.material_index == sti and p_.normal.z > 0.55 and nz > 0.25:
        p_.material_index = mi
smooth(o, 40)
report()
finish('castle', 'knight_statue', kind='hero', footprint=1.0, notes='stenen ridderbeeld (helm met vizier en gouden kam, schouderstukken, cape, schild met gouden kruis) leunend op zwaard met gouden pareerstang, op gelaagde sokkel met gouden plaquette en mos')
