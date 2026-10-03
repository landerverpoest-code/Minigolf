import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_warm', '#a69c8f', rough=0.9)
stone_d = mat('stone_dark', '#877c70', rough=0.9)
moss = mat('moss', '#5c8a35', rough=0.95)
grass = mat('grass', '#4f8f30', rough=0.9)

rnd = random.Random(9)
parts = []
L, T, CH = 3.0, 0.62, 0.36
NC = 6
def top_at(x):
    if x < -0.25:
        return NC * CH
    return NC * CH - (x + 0.25) * 1.05 + 0.25 * noise.noise(Vector((x * 3, 0.5, 0.2)))
for k in range(NC):
    z0 = k * CH
    bw = 0.5
    off = (bw / 2 if k % 2 else 0)
    x = -L / 2 - off
    i = 0
    while x < L / 2 - 0.01:
        x0, x1 = max(x, -L / 2), min(x + bw, L / 2)
        cx = (x0 + x1) / 2
        i += 1
        x += bw
        if z0 + CH * 0.5 > top_at(cx):
            continue
        if (k, i) in ((3, 2),):   # gat in de muur
            continue
        broken = z0 + CH * 1.5 > top_at(cx) and cx > -0.25
        w = x1 - x0 - 0.03
        b = box((w, T + rnd.uniform(-0.03, 0.03), CH - 0.03), material=stone_d if rnd.random() < 0.3 else stone)
        jitter(b, 0.012, seed=k * 50 + i)
        rot = (rnd.uniform(-6, 6), rnd.uniform(-8, 8), rnd.uniform(-6, 6)) if broken else (0, 0, rnd.uniform(-1.5, 1.5))
        xform(b, rot=rot, loc=(cx + (rnd.uniform(-0.03, 0.03) if broken else 0), rnd.uniform(-0.02, 0.02), z0 + CH / 2))
        parts.append(b)
# kantelen op het intacte deel
for x in (-1.25, -0.6):
    m = box((0.48, T, 0.42), material=stone, bevel=0.025)
    jitter(m, 0.01, seed=int(x * 10))
    xform(m, loc=(x, 0, NC * CH + 0.21))
    parts.append(m)
# gevallen stenen voor de muur
for k, (x, y, a) in enumerate(((0.9, -0.75, 25), (1.35, -0.45, -40), (0.45, -0.95, 60), (1.7, 0.2, 10), (0.2, -0.6, -15))):
    b = box((0.46, 0.3, 0.32), material=stone if k % 2 else stone_d, bevel=0.03)
    jitter(b, 0.02, seed=200 + k)
    xform(b, rot=(rnd.uniform(-10, 10), rnd.uniform(-15, 15), a), loc=(x, y, 0.15))
    parts.append(b)
# mos op de bovenkanten en graspollen aan de voet
for k, (x, z) in enumerate(((-1.0, NC * CH + 0.43), (0.15, top_at(0.15) - 0.05), (0.75, top_at(0.75) - 0.12))):
    mb = ico(0.3, sub=1, material=moss, scale=(1.4, 1.2, 0.35))
    jitter(mb, 0.04, seed=k)
    xform(mb, loc=(x, 0.0, z))
    smooth(mb, 70)
    parts.append(mb)
for k in range(8):
    x = rnd.uniform(-1.5, 1.5); y = rnd.choice((-1, 1)) * (T / 2 + 0.05)
    g = leaf(rnd.uniform(0.2, 0.32), 0.07, 0.015, material=grass)
    xform(g, rot=(55, 0, rnd.uniform(0, 360)), loc=(x, y, 0))
    parts.append(g)
o = join(parts, 'wall_ruin')
# mos op een deel van de bovenvlakken
mi = [m.name for m in o.data.materials].index('moss')
for p_ in o.data.polygons:
    if p_.normal.z > 0.85 and noise.noise(p_.center * 2.2 + Vector((3, 1, 0))) > 0.0 and p_.material_index != [m.name for m in o.data.materials].index('grass'):
        p_.material_index = mi
smooth(o, 40)
report()
finish('castle', 'wall_ruin', kind='scatter', footprint=1.8, notes='afgebrokkeld stuk kantelenmuur uit losse blokken (2 steentinten), gat in de muur, gevallen stenen, mos en graspollen')
