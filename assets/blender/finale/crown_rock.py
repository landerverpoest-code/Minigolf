import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
basalt = mat('basalt', '#3d3648', rough=0.9)
basalt2 = mat('basalt_dark', '#2c2636', rough=0.95)
glow = mat('glow_gold', '#e8a820', rough=0.25, emit='#ffb012', emit_strength=1.2)
V = Vector
P = []
r = rock(0.85, sub=2, material=basalt, scale=(1.15, 1.0, 0.9), jit=0.1, seed=31)
chop(r, 7, seed=4, depth=(0.78, 0.92), minz=-0.1)
P.append(r)
r2 = rock(0.4, loc=(0.8, 0.5, 0), sub=2, material=basalt2, scale=(1.2, 1, 0.8), jit=0.08, seed=32)
chop(r2, 3, seed=5)
P.append(r2)
top = surface_hit(r, (0, 0, 1), center=(0, 0, 0.3))[0].z
# kroon van gouden kristallen bovenop
def crystal(L, rad, m):
    return lathe([(rad, -0.08), (rad * 1.05, L * 0.7), (0, L)], seg=5, material=m)
for k in range(7):
    a = k * TAU / 7
    c = crystal(0.45 + 0.2 * (k % 2), 0.09, glow)
    place_on(c, r, (0.45 * math.cos(a), 0.45 * math.sin(a), 1), center=(0, 0, 0.3), sink=0.04, spin=a)
    T(c, rot=(0, 0, 0))
    P.append(c)
c = crystal(0.8, 0.12, glow); place_on(c, r, (0, 0, 1), center=(0, 0, 0.3), sink=0.05); P.append(c)
for (d, L) in [((0.9, -0.6, 0.3), 0.3), ((-0.8, -0.5, 0.2), 0.25), ((0.2, 0.9, 0.2), 0.22)]:
    c = crystal(L, 0.06, glow); place_on(c, r, d, center=(0, 0, 0.3), sink=0.03); P.append(c)
# gouden aders over de rots
for k, (a, z0, z1) in enumerate([(-1.4, 0.15, 0.75), (-0.5, 0.1, 0.65), (2.0, 0.15, 0.8)]):
    pts = []
    for j in range(4):
        z = z0 + (z1 - z0) * j / 3
        aa = a + 0.15 * math.sin(j * 2.3 + k)
        loc, nor = surface_hit(r, (math.cos(aa), math.sin(aa), 0), center=(0, 0, z))
        if loc is not None:
            pts.append(loc + nor * 0.008)
    P.append(tube(pts, r=[0.0] + [0.03] * (len(pts) - 2) + [0.0], seg=3, material=glow, smooth=False))
join(P, 'crown_rock')
report()
finish('finale', 'crown_rock', kind='scatter', footprint=0.95, notes='donkere rots met een kroon van gouden kristallen en gouden aders (glow_gold)')
