import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

PINK = mat('coral_pink', '#ff4f86', rough=0.6)
ORNG = mat('coral_orange', '#ff8a2a', rough=0.6)
PURP = mat('coral_purple', '#8a46ff', rough=0.6)
YEL = mat('coral_yellow', '#ffd447', rough=0.6)
ROCK = mat('coral_rock', '#c9b48c', rough=0.95)
rnd = random.Random(3)

# basis-steen
base = lathe([(0.22, 0.0), (0.2, 0.04), (0.1, 0.08), (0.0, 0.085)], verts=6, material=ROCK, jitter=0.12, seed=1)
# hertshoornkoraal (vertakt)
def branch(p0, d, L, r, depth):
    p0 = Vector(p0); d = Vector(d).normalized()
    p1 = p0 + d * L * 0.5 + Vector((rnd.uniform(-0.02, 0.02), rnd.uniform(-0.02, 0.02), 0))
    p2 = p0 + d * L
    if depth >= 1:
        tube([p0, p1, p2], [r, r * 0.8, r * 0.55], verts=4, material=PINK, cap0=False)
    else:
        tube([p0, p2], [r, r * 0.6], verts=4, material=PINK, cap0=False)
    if depth > 0:
        for s in ((-1, 1) if depth > 1 else (rnd.choice((-1, 1)),)):
            nd = (d + Vector((s * 0.7, rnd.uniform(-0.5, 0.5), 0.25))).normalized()
            branch(p1, nd, L * 0.55, r * 0.7, depth - 1)
for k in range(3):
    a = k * 2.1 + 0.4
    branch((0.06 * math.cos(a) - 0.05, 0.06 * math.sin(a) + 0.03, 0.05), (math.cos(a) * 0.4, math.sin(a) * 0.4, 1), 0.3, 0.032, 2 if k == 0 else 1)
# hersenkoraal
brain = sphere(0.11, loc=(0.12, -0.07, 0.07), seg=6, rings=4, material=ORNG, scale=(1, 1, 0.7))
for v in brain.data.vertices:
    v.co += Vector((0, 0, 0.012 * math.sin(v.co.x * 90) * math.sin(v.co.y * 90)))
# waaierkoraal (sea fan)
fc = Vector((-0.1, 0.1, 0.06))
def fan(u, v):
    a = math.pi * (0.15 + 0.7 * u)
    r = 0.05 + v * 0.27 * (1 - 0.22 * abs(math.sin(u * math.pi * 3)))
    return fc + Vector((math.cos(a) * r * 0.9, math.sin(u * 3) * 0.03 + 0.02 * v, math.sin(a) * r))
f = grid_sheet(fan, 6, 2, material=PURP, name='fan')
place(f, rot=(0, 0, 0.5), loc=(0, 0, 0))
# stam van de waaier
tube([fc, fc + Vector((0, 0, 0.08))], [0.015, 0.012], verts=4, material=PURP)
# buiskoraaltjes
for i in range(3):
    c = Vector((0.15 + rnd.uniform(-0.03, 0.03), 0.1 + i * 0.05, 0.03))
    h = rnd.uniform(0.07, 0.13)
    lathe([(0.025, c.z), (0.032, c.z + h)], verts=6, material=YEL, loc=(c.x, c.y, 0), cap0=False, cap1=False)
join_all('coral_cluster')
report()
finish('water', 'coral_cluster', kind='edge', footprint=0.28,
       notes='Kleurrijk koraal: roze vertakt koraal, oranje hersenkoraal, paarse waaier en gele buiskoraaltjes op een steen')
closeup('coral_cluster')
