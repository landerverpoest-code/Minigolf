import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
iron = mat('iron', '#2b2733', rough=0.45, metal=0.6)
stone = mat('stone', '#8a958a', rough=0.9)
dark = mat('stone_dark', '#5e6a63', rough=0.95)
moss = mat('moss', '#557f35', rough=1.0)
V = Vector
parts = []
# stenen pilaren
for sx in (-1, 1):
    x = sx * 1.38
    parts.append(box((0.32, 0.32, 1.25), loc=(x, 0, 0.625), material=stone, bevel=0.02))
    parts.append(box((0.4, 0.4, 0.1), loc=(x, 0, 1.3), material=dark, bevel=0.015))
    parts.append(cone(0.24, 0.22, loc=(x, 0, 1.46), rot=(0, 0, math.pi / 4), verts=4, material=dark))
    parts.append(box((0.38, 0.38, 0.12), loc=(x, 0, 0.06), material=dark))
    parts.append(shade_smooth(ico(0.1, loc=(x - sx * 0.08, -0.1, 1.36), material=moss, scale=(1.5, 1.2, 0.45), jitter=0.015, seed=sx + 3)))
# ijzeren hek
xs = [-1.08 + i * 0.24 for i in range(10)]
for i, x in enumerate(xs):
    if i == 6:
        continue   # ontbrekende spijl
    h = 1.32 + 0.05 * math.sin(i * 1.7)
    lean = 0.12 if i == 3 else 0.0
    bar = cyl(0.018, h, loc=(x, 0, h / 2 + 0.05), verts=4, material=iron)
    tip = cone(0.045, 0.14, loc=(x, 0, h + 0.12), verts=4, material=iron)
    b = join([bar, tip], 'bar')
    if lean:
        T(b, rot=(0.0, lean, 0.0), pivot=(x, 0, 0.35))
    parts.append(b)
for z in (0.32, 1.12):
    parts.append(box((2.5, 0.035, 0.06), loc=(0, 0, z), material=iron))
# krullen tussen de spijlen
for i in range(0, 9, 2):
    cx = (xs[i] + xs[i + 1]) / 2
    pts = [V((cx + 0.09 * math.sin(t), 0, 0.95 + 0.11 * math.cos(t))) for t in [k * TAU / 8 for k in range(9)]]
    parts.append(tube(pts, r=0.012, seg=3, material=iron, smooth=False, cap=False))
join(parts, 'iron_fence')
report()
finish('haunted', 'iron_fence', kind='scatter', footprint=1.5, notes='smeedijzeren hekdeel (3 m breed langs X) met puntige spijlen en stenen pilaren')
