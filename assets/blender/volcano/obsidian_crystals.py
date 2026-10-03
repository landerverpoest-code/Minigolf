import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

obs = mat('obsidian', '#17121c', rough=0.06, metal=0.1)
obs_p = mat('obsidian_purple', '#4b2c74', rough=0.1, metal=0.1)
basalt = mat('basalt', '#3a322e', rough=0.9)

rnd = random.Random(5)
parts = []
base = chunk(0.2, (1.4, 1.2, 0.6), cuts=6, seed=3, material=basalt, flat_bottom=0.3, base_sub=1)
xform(base, loc=(0, 0, 0.03))
parts.append(base)
spec = [(0.0, 0.0, 0.5, 0.075, (0, 0), 1), (0.09, -0.05, 0.34, 0.06, (14, 22), 0), (-0.1, 0.02, 0.38, 0.06, (-8, -24), 0),
        (0.03, 0.1, 0.3, 0.05, (-24, 8), 1), (-0.04, -0.11, 0.24, 0.045, (26, -10), 1), (0.15, 0.07, 0.2, 0.04, (-10, 38), 0),
        (-0.16, -0.08, 0.18, 0.04, (20, -40), 1)]
for k, (x, y, h, r, (rx, ry), purple) in enumerate(spec):
    seg = 5 if k % 2 else 6
    c = lathe([(r, -0.05), (r * 1.05, h * 0.68), (0, h)], seg=seg, material=obs_p if purple else obs, cap_bottom=False, phase=rnd.uniform(0, 1))
    # schuine, scherpe punt
    for v in c.data.vertices:
        if v.co.z > h * 0.95:
            v.co.x += r * 0.4; v.co.y += r * 0.2
    jitter(c, r * 0.12, seed=k)
    xform(c, rot=(rx, ry, rnd.uniform(0, 360)), loc=(x, y, 0.05))
    parts.append(c)
# losse scherfjes
for k in range(2):
    a = k * 2.6 + 0.5
    c = chunk(0.035, (1.6, 0.8, 0.6), cuts=3, seed=70 + k, material=obs_p if k % 2 else obs, base_sub=1)
    xform(c, rot=(0, 20, rnd.uniform(0, 180)), loc=(0.25 * math.cos(a), 0.22 * math.sin(a), 0.02))
    parts.append(c)
join(parts, 'obsidian_crystals')
report()
finish('volcano', 'obsidian_crystals', kind='edge', footprint=0.25, notes='glanzende zwarte en paarse obsidiaanscherven op een basaltvoetje (lage roughness)')
