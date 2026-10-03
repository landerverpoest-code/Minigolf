import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _palm import *

RL = mat('arch_rock', '#cfae80', rough=0.95)
RD = mat('arch_rock_dark', '#a07d58', rough=0.95)
GR = mat('arch_grass', '#4fae3c', rough=0.8)
GR2 = mat('arch_grass_light', '#86cc4a', rough=0.8)
BARK = mat('arch_bark', '#a27b4c', rough=0.9)
rnd = random.Random(8)

# --- boog langs een halve ellips ---
N = 24
pts, rad, sq = [], [], []
for i in range(N + 1):
    t = i / N
    th = math.pi * t
    x = -3.6 * math.cos(th)
    z = 6.6 * math.sin(th) - 0.4
    pts.append((x + 0.12 * math.sin(th * 3), 0.3 * math.sin(th * 2), z))
    edge = min(t, 1 - t)
    r = 0.62 + 0.75 * (max(0, 0.32 - edge) / 0.32) ** 1.5
    rad.append(r * (1.0 if i not in (0, N) else 1.25))
    sq.append((1.7 + 0.3 * max(0, 0.25 - edge) / 0.25, 0.95))
arch = tube(pts, rad, verts=10, mats=[RL, RD, GR], squash=sq, jitter=0.12, seed=4, name='arch')
me = arch.data
# lagen: banden in z afwisselend licht/donker, gras op naar boven gerichte vlakken bovenin
for p in me.polygons:
    c = p.center
    band = int((c.z + 0.25 * math.sin(c.x * 0.9)) / 0.95)
    p.material_index = band % 2
    if p.normal.z > 0.5 and c.z > 5.3:
        p.material_index = 2
# willekeurige vervorming van de punten (rotsachtig)
for v in me.vertices:
    v.co += Vector((rnd.uniform(-0.12, 0.12), rnd.uniform(-0.12, 0.12), rnd.uniform(-0.1, 0.1)))
    v.co.z = max(v.co.z, 0.0)
# --- rotsblokken rond de voeten ---
for i in range(12):
    side = -1 if i % 2 == 0 else 1
    a = rnd.uniform(0, 2 * math.pi)
    d = rnd.uniform(1.2, 2.3)
    s = rnd.uniform(0.6, 1.2)
    r = rock(r=s, loc=(side * 3.6 + math.cos(a) * d, math.sin(a) * d * 1.2, 0.25 * s), scale=(1.3, 1.0, rnd.uniform(0.6, 1.0)),
             seed=20 + i, jitter=0.25, material=RL if i % 3 else RD, rot_z=a)
# --- groene kuif bovenop: struikjes ---
for i in range(5):
    x = rnd.uniform(-1.4, 1.4)
    th = math.acos(max(-1, min(1, -x / 3.6)))
    z = 6.6 * math.sin(th) - 0.4 + 0.5
    b = ico(rnd.uniform(0.3, 0.42), loc=(x, rnd.uniform(-0.7, 0.7), z), sub=1, material=GR if i % 2 else GR2,
            scale=(1.2, 1.0, 0.75), jitter=0.06, seed=i)
# hangende ranken langs de boog
for i in range(4):
    x = rnd.uniform(-1.8, 1.8); y = rnd.choice([-1.05, 1.05])
    th = math.acos(max(-1, min(1, -x / 3.6))); z = 6.6 * math.sin(th) - 0.2
    tube([(x, y, z), (x + 0.05, y * 1.08, z - 0.6), (x - 0.05, y * 1.1, z - 1.2 - rnd.uniform(0, 0.6))], [0.12, 0.08, 0.0], verts=4, material=GR)
# --- palmpje bovenop ---
M = dict(bark=BARK, bark2=RD, leaf=GR, leaf2=GR2, nut=RD)
palm(M, base=(0.9, 0.1, 6.6 * math.sin(math.acos(-0.25)) - 0.4 + 0.45), height=2.0, lean=(0.6, -0.3), r0=0.12, r1=0.08,
     segs=5, verts=5, fronds=7, flen=1.3, fwidth=0.3, frise=0.6, fdroop=0.8, fsegs=5, nuts=2, seed=5, flare=False, nut_seg=(6, 4))
join_all('rock_arch')
report()
finish('water', 'rock_arch', kind='hero', footprint=3.2,
       notes='Natuurlijke rotsboog uit zee met gelaagd gesteente, groene kuif, ranken en een palmpje bovenop')
closeup('rock_arch')
