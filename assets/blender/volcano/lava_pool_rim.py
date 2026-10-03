import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
ash = mat('ash', '#7d7570', rough=1.0)
lava = mat('glow_lava', '#ff7010', rough=0.4, emit='#ff4c00', emit_strength=3.0)
lava_h = mat('glow_lava_hot', '#ffb020', rough=0.4, emit='#ff9000', emit_strength=3.0)

rnd = random.Random(3)
parts = []
# lavaplas: onregelmatige schijf met hete kern
seg = 14
outline = [0.95 + 0.12 * noise.noise(Vector((math.cos(TAU * i / seg) * 1.5, math.sin(TAU * i / seg) * 1.5, 0.3))) for i in range(seg)]
vs = [(0, 0, 0.07)]
for i in range(seg):
    a = TAU * i / seg
    vs.append((outline[i] * 0.5 * math.cos(a), outline[i] * 0.5 * math.sin(a), 0.065))
for i in range(seg):
    a = TAU * i / seg
    vs.append((outline[i] * math.cos(a), outline[i] * math.sin(a), 0.05))
fs = [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)] + [(1 + i, 1 + seg + i, 1 + seg + (i + 1) % seg, 1 + (i + 1) % seg) for i in range(seg)]
pool = mesh_obj(vs, fs, lava_h)
pool.data.materials.append(lava)
for p in pool.data.polygons:
    if len(p.vertices) == 4:
        p.material_index = 1
smooth(pool, 60)
parts.append(pool)
# drijvende korstplaten
for k, (x, y, r) in enumerate(((0.35, 0.2, 0.17), (-0.3, -0.25, 0.13), (-0.2, 0.42, 0.1), (0.15, -0.45, 0.09))):
    c = chunk(r, (1.4, 1.1, 0.25), cuts=3, seed=90 + k, material=basalt, base_sub=1)
    xform(c, rot=(0, 0, rnd.uniform(0, 180)), loc=(x, y, 0.075))
    parts.append(c)
# ring van rotsen
n = 9
for k in range(n):
    a = TAU * k / n + rnd.uniform(-0.12, 0.12)
    d = rnd.uniform(1.0, 1.12)
    r = rnd.uniform(0.22, 0.34)
    c = chunk(r, (1.4, 1.0, rnd.uniform(0.7, 1.0)), cuts=5, seed=100 + k, material=basalt if k % 3 else basalt_l, flat_bottom=0.4, base_sub=1)
    zs = [v.co.z for v in c.data.vertices]
    xform(c, loc=(0, 0, -min(zs) - 0.04))
    xform(c, rot=(0, 0, math.degrees(a) + rnd.uniform(-30, 30)), loc=(d * math.cos(a), d * math.sin(a), 0))
    dust(c, ash, 0.75)
    parts.append(c)
# grond-rand (donkere lage ring onder de rotsen)
rim = lathe([(1.3, 0.0), (1.15, 0.06), (0.9, 0.07), (0.85, 0.0)], seg=seg, material=basalt, cap_bottom=False, cap_top=False)
jitter(rim, 0.03, seed=4, axes=(1, 1, 0.3))
smooth(rim, 60)
parts.append(rim)
join(parts, 'lava_pool_rim')
report()
finish('volcano', 'lava_pool_rim', kind='scatter', footprint=1.3, notes='vlakke gloeiende lavaplas (hete gele kern + oranje rand) met drijvende korstplaten in een ring van basaltrotsen')
