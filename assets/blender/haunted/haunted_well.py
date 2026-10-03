import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
stone = mat('stone', '#8a958a', rough=0.9)
wood = mat('wood', '#5e4434', rough=0.85)
iron = mat('iron', '#2b2733', rough=0.45, metal=0.6)
glow = mat('glow_well', '#2f9a1c', rough=0.3, emit='#4ad024', emit_strength=1.4)
moss = mat('moss', '#557f35', rough=1.0)
V = Vector
parts = []
rnd = random.Random(5)
R, n = 0.56, 10
for row in range(3):
    for k in range(n):
        if row == 2 and k in (2, 3, 4):
            continue   # afgebrokkeld
        a = (k + 0.5 * (row % 2)) * TAU / n
        h = 0.2 if row < 2 else 0.12
        z = 0.1 + row * 0.205 if row < 2 else 0.47
        w = 0.36 if row < 2 else 0.38
        b = box((w, 0.2 if row < 2 else 0.25, h), loc=(R * math.cos(a), R * math.sin(a), z), rot=(0, 0, a + math.pi / 2), material=stone)
        jitter(b, 0.015, seed=row * 20 + k)
        T(b, rot=(rnd.uniform(-0.04, 0.04), rnd.uniform(-0.04, 0.04), rnd.uniform(-0.05, 0.05)), pivot=(R * math.cos(a), R * math.sin(a), z))
        parts.append(b)
# gevallen stenen
for (x, y, rz, s) in [(0.55, -0.62, 0.4, 7), (0.85, -0.3, 1.2, 8)]:
    b = box((0.3, 0.18, 0.16), loc=(x, y, 0.08), rot=(0.1, 0.05, rz), material=stone); jitter(b, 0.02, s); parts.append(b)
# binnenwand + gloeiend water
parts.append(lathe([(0.47, 0.0), (0.47, 0.5)], seg=10, material=iron, cap_top=False, cap_bot=False))
inner = parts[-1]; flip(inner)
w = lathe([(0.47, 0.3), (0, 0.3)], seg=10, material=glow, cap_bot=False, cap_top=False); parts.append(w)
# palen + balk (licht scheef)
for sx in (-1, 1):
    p = box((0.1, 0.12, 1.45), loc=(sx * 0.66, 0, 0.72), material=wood)
    T(p, rot=(0, sx * 0.04 + 0.03, 0), pivot=(sx * 0.66, 0, 0))
    parts.append(p)
parts.append(cyl(0.065, 1.5, loc=(0.03, 0, 1.3), rot=(0, math.pi / 2, 0), verts=7, material=wood))
crank = tube([V((0.78, 0, 1.3)), V((0.88, 0, 1.3)), V((0.88, 0, 1.12)), V((0.97, 0, 1.12))], r=0.02, seg=4, material=iron, smooth=False)
parts.append(crank)
# dakje (één plank gebroken)
for sy, ln in ((-1, 1.0), (1, 0.62)):
    pl = box((1.75 * ln, 0.5, 0.04), loc=(0.03 - (1 - ln) * 0.6, sy * 0.21, 1.58), rot=(sy * 0.62, 0, 0), material=wood)
    jitter(pl, 0.01, seed=3 if sy < 0 else 4)
    parts.append(pl)
parts.append(box((1.85, 0.06, 0.06), loc=(0.03, 0, 1.73), material=wood))
# ketting met emmer
links = []
for i in range(6):
    z = 1.22 - i * 0.075
    t = torus(0.035, 0.009, loc=(0.0, 0.0, z), rot=(math.pi / 2, 0, (i % 2) * math.pi / 2), seg=4, ring=3, material=iron, smooth=False)
    T(t, scale=(1, 1, 1.4), pivot=(0, 0, z))
    links.append(t)
parts += links
bk = lathe([(0.0, 0.0), (0.1, 0.0), (0.13, 0.2)], seg=8, material=wood, cap_top=False)

T(bk, loc=(0, 0, 0.6))
parts.append(bk)
parts.append(lathe([(0.12, 0.77), (0, 0.77)], seg=8, material=glow, cap_bot=False, cap_top=False))
parts.append(tube([V((-0.13, 0, 0.8)), V((-0.08, 0, 0.92)), V((0, 0, 0.96)), V((0.08, 0, 0.92)), V((0.13, 0, 0.8))], r=0.008, seg=3, material=iron, smooth=False))
for (x, y, s) in [(-0.4, -0.38, 1), (0.45, 0.35, 2)]:
    parts.append(shade_smooth(ico(0.1, loc=(x, y, 0.5 if s != 3 else 0.42), material=moss, scale=(1.4, 1.2, 0.45), jitter=0.015, seed=s)))
join(parts, 'haunted_well')
report()
finish('haunted', 'haunted_well', kind='scatter', footprint=0.75, notes='afgebrokkelde stenen put met ketting, emmer en groen gloeiend water (glow_well)')
