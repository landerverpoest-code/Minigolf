import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

hay = mat('hay', '#e2bf58', rough=0.95)
hay_d = mat('hay_dark', '#c79a3a', rough=0.95)
twine = mat('twine_red', '#c0442f', rough=0.8)

R, W = 0.46, 0.95
def bale(seed):
    rnd = random.Random(seed)
    h = W / 2
    prof = [(0, -h + 0.035), (0.16, -h + 0.025), (0.3, -h + 0.012), (R - 0.05, -h), (R, -h + 0.06),
            (R, h - 0.06), (R - 0.05, h), (0.3, h - 0.012), (0.16, h - 0.025), (0, h - 0.035)]
    o = lathe(prof, seg=10, material=hay)
    o.data.materials.append(hay_d)
    # spiraal-indruk: afwisselende ringen op de kopse kanten donker
    for p in o.data.polygons:
        rr = Vector((p.center.x, p.center.y)).length
        if abs(p.normal.z) > 0.7 and (0.12 < rr < 0.26 or rr < 0.04):
            p.material_index = 1
    # strooierig: kleine willekeurige verschuivingen aan de buitenkant
    jitter(o, 0.012, seed=seed)
    smooth(o, 40)
    parts = [o]
    for z in (-0.2, 0.2):
        b = lathe([(R + 0.012, z - 0.022), (R + 0.012, z + 0.022)], seg=10, material=twine, cap_bottom=False, cap_top=False)
        parts.append(b)
    # losse strootjes op de rand
    for k in range(2):
        a = rnd.uniform(0, TAU)
        z = rnd.uniform(-h, h)
        p0 = Vector((R * math.cos(a), R * math.sin(a), z))
        p1 = p0 + Vector((math.cos(a + 1.2) * 0.13, math.sin(a + 1.2) * 0.13, rnd.uniform(-0.05, 0.05)))
        parts.append(rod(p0, p1, 0.012, 0.003, verts=3, material=hay))
    return join(parts, 'bale')

b1 = bale(1); xform(b1, rot=(90, 0, 0)); xform(b1, rot=(0, 0, 8), loc=(-R - 0.01, 0, R))
b2 = bale(2); xform(b2, rot=(90, 0, 0)); xform(b2, rot=(0, 0, -6), loc=(R + 0.01, 0.05, R))
b3 = bale(3); xform(b3, rot=(90, 0, 0)); xform(b3, rot=(0, 0, 3), loc=(0.02, 0.02, R + 2 * R * math.sin(math.radians(60)) + 0.01))
# hooi op de grond
parts = [b1, b2, b3]
rnd = random.Random(5)
for i in range(2):
    x, y = rnd.uniform(-0.9, 0.9), rnd.choice((-0.6, 0.6)) + rnd.uniform(-0.1, 0.1)
    t = ico(0.12, sub=1, material=hay_d, scale=(1.4, 1.0, 0.35))
    jitter(t, 0.03, seed=i)
    xform(t, loc=(x, y, 0.02), rot=(0, 0, rnd.uniform(0, 180)))
    parts.append(t)
join(parts, 'hay_bales')
report()
finish('meadow', 'hay_bales', kind='scatter', footprint=0.95, notes='stapel van 3 ronde hooibalen met rood touw, spiraal op de kopse kanten en los hooi')
