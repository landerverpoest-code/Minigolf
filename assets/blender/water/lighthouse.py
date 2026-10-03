import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

RED = mat('lh_red', '#d8342c', rough=0.55)
WHITE = mat('lh_white', '#f3efe6', rough=0.6)
DARK = mat('lh_metal', '#2f3a44', rough=0.45, metal=0.3)
ROCK = mat('rock', '#8c867b', rough=0.95)
GLOW = mat('glow_lamp', '#fff3c4', rough=0.3, emit='#ffd860', emit_strength=6.0)

rnd = random.Random(5)
# --- rotsen ---
for i in range(11):
    a = 2 * math.pi * i / 11 + rnd.uniform(-0.2, 0.2)
    d = rnd.uniform(1.5, 2.4)
    s = rnd.uniform(0.7, 1.15)
    rock(r=s, loc=(math.cos(a) * d, math.sin(a) * d, 0.15 * s), scale=(rnd.uniform(1.0, 1.5), 1.0, rnd.uniform(0.6, 1.0)),
         seed=i + 3, jitter=0.22, material=ROCK, rot_z=a)
rock(r=1.6, loc=(0, 0, 0.35), scale=(1.4, 1.4, 0.7), seed=40, jitter=0.18, material=ROCK)
# --- sokkel ---
Z0 = 1.15
plinth = lathe([(1.55, Z0 - 0.5), (1.55, Z0 + 0.15), (1.4, Z0 + 0.3), (0, Z0 + 0.3)], verts=10, material=WHITE)
bev(plinth, 0.04)
Zt = Z0 + 0.3
# --- toren met strepen ---
H = 8.6
rb, rt = 1.12, 0.78
nb = 6
prof, bm = [], []
for i in range(nb + 1):
    z = Zt + H * i / nb
    r = rb + (rt - rb) * i / nb
    prof.append((r, z))
    if i < nb: bm.append(i % 2)
prof.append((0, Zt + H))
bm.append(0)
tower = lathe(prof, verts=16, mats=[WHITE, RED], band_mats=bm, cap0=False)
shade_smooth(tower, 30)
# kleine richels tussen de banden
for i in range(1, nb):
    z = Zt + H * i / nb; r = rb + (rt - rb) * i / nb
    ring = cyl(r + 0.03, 0.06, loc=(0, 0, z), verts=16, material=WHITE if i % 2 else RED)
# deur (voorkant -Y)
door = box((0.62, 0.3, 1.15), loc=(0, -rb + 0.06, Zt + 0.58), material=DARK, bevel=0.03)
arch = cyl(0.31, 0.3, loc=(0, -rb + 0.06, Zt + 1.15), rot=(math.pi / 2, 0, 0), verts=10, material=DARK)
frame = box((0.82, 0.26, 0.12), loc=(0, -rb + 0.02, Zt + 1.52), material=WHITE, bevel=0.03)
step = box((1.0, 0.6, 0.18), loc=(0, -rb - 0.25, Zt - 0.06), material=WHITE, bevel=0.04)
# ramen in een spiraal
for k, (z, ang) in enumerate([(3.0, 0.3), (5.0, -2.0), (6.9, 2.4), (8.2, -0.7)]):
    zz = Zt + z; r = rb + (rt - rb) * (z / H)
    c = Vector((math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2), 0))
    w = box((0.3, 0.16, 0.48), loc=c * (r - 0.02) + Vector((0, 0, zz)), rot=(0, 0, ang), material=DARK, bevel=0.02)
    sill = box((0.42, 0.2, 0.07), loc=c * (r + 0.02) + Vector((0, 0, zz - 0.27)), rot=(0, 0, ang), material=WHITE)
# --- galerij ---
Zg = Zt + H
gal = lathe([(rt - 0.05, Zg - 0.25), (1.38, Zg - 0.02), (1.38, Zg + 0.12), (0, Zg + 0.12)], verts=16, material=DARK)
bev(gal, 0.02)
for k in range(12):
    a = 2 * math.pi * k / 12
    c = Vector((math.cos(a), math.sin(a), 0))
    cb = box((0.32, 0.12, 0.3), loc=c * (rt + 0.12) + Vector((0, 0, Zg - 0.28)), rot=(0, 0, a), material=DARK)
for k in range(16):
    a = 2 * math.pi * k / 16
    box((0.05, 0.05, 0.62), loc=(math.cos(a) * 1.3, math.sin(a) * 1.3, Zg + 0.43), rot=(0, 0, a), material=DARK)
torus(1.3, 0.035, loc=(0, 0, Zg + 0.74), seg=24, ring=4, material=DARK, smooth=True)
torus(1.3, 0.025, loc=(0, 0, Zg + 0.42), seg=24, ring=4, material=DARK, smooth=True)
# --- lantaarnkamer (open frame, draaiend licht zichtbaar) ---
Zl = Zg + 0.12
base = lathe([(0.72, Zl), (0.72, Zl + 0.38), (0.66, Zl + 0.42), (0, Zl + 0.42)], verts=12, material=RED)
for k in range(8):
    a = 2 * math.pi * k / 8 + math.pi / 8
    box((0.07, 0.07, 1.15), loc=(math.cos(a) * 0.64, math.sin(a) * 0.64, Zl + 0.42 + 0.57), rot=(0, 0, a), material=DARK)
Zr = Zl + 0.42 + 1.15
topring = cyl(0.78, 0.14, loc=(0, 0, Zr + 0.07), verts=16, material=DARK)
roof = cone(0.86, 0.85, loc=(0, 0, Zr + 0.14 + 0.42), verts=16, material=RED)
shade_smooth(roof, 40)
ball = sphere(0.13, loc=(0, 0, Zr + 0.14 + 0.88), seg=8, rings=6, material=DARK)
rod = cyl(0.025, 0.55, loc=(0, 0, Zr + 0.14 + 1.2), verts=5, material=DARK)
ped = cyl(0.16, 0.36, loc=(0, 0, Zl + 0.42 + 0.18), verts=8, material=DARK)
join_all('lighthouse')
# --- draaiend lichthuis ---
Zc = Zl + 0.42 + 0.36 + 0.33
sp = []
sp.append(cyl(0.17, 0.5, loc=(0, 0, Zc), verts=10, material=GLOW))
for s in (-1, 1):
    sp.append(box((0.42, 0.1, 0.52), loc=(s * 0.24, 0, Zc), rot=(0, 0, math.pi / 2), material=GLOW))
    sp.append(box((0.08, 0.5, 0.6), loc=(s * 0.33, 0, Zc), material=DARK, bevel=0.015))
sp.append(cyl(0.22, 0.07, loc=(0, 0, Zc + 0.31), verts=10, material=DARK))
sp.append(cyl(0.22, 0.07, loc=(0, 0, Zc - 0.31), verts=10, material=DARK))
spin = join(sp, 'spin_light')
bpy.context.scene.cursor.location = (0, 0, Zc)
bpy.ops.object.select_all(action='DESELECT'); spin.select_set(True); bpy.context.view_layer.objects.active = spin
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
report()
finish('water', 'lighthouse', kind='hero', footprint=2.6,
       notes='Rood-wit gestreepte vuurtoren op rotsen met galerij; open lantaarnkamer met draaiend lichthuis',
       spin=[{'node': 'spin_light', 'axis': 'y', 'speed': 1.0}])
closeup('lighthouse')
