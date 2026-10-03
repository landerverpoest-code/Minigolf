import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
capm = mat('glow_shroom', '#0b6e50', rough=0.4, emit='#12c084', emit_strength=1.0)
stemm = mat('shroom_stem', '#d9d2e6', rough=0.7)
gill = mat('shroom_gill', '#6a4a8a', rough=0.8)
moss = mat('moss', '#4a6e30', rough=1.0)
V = Vector
parts = []
# (x, y, hoogte, hoedstraal, helling)
for (x, y, h, r, lx, ly, sg) in [(0.0, 0.02, 0.22, 0.11, 0.1, 0.05, 7), (0.1, -0.06, 0.13, 0.075, -0.15, 0.25, 7), (-0.1, -0.05, 0.1, 0.06, 0.25, -0.15, 7),
                             (0.05, 0.1, 0.06, 0.04, -0.2, -0.4, 6)]:
    top = V((x + lx * h, y + ly * h, h))
    parts.append(tube([V((x, y, 0)), V((x + lx * h * 0.3, y + ly * h * 0.3, h * 0.5)), top], r=[r * 0.3, r * 0.24, r * 0.2], seg=4, material=stemm, smooth=True))
    cap = lathe([(r, 0.0), (r * 0.85, r * 0.45), (r * 0.42, r * 0.78), (0, r * 0.84)], seg=sg, material=capm, smooth=True)
    set_mat(cap, gill, lambda c, n: n.z < -0.5)
    T(cap, rot=(-ly * 1.2, lx * 1.2, 0), loc=top)
    parts.append(cap)
parts.append(shade_smooth(ico(0.1, loc=(0.0, 0.0, 0.0), material=moss, scale=(1.5, 1.3, 0.25), jitter=0.012, seed=3)))
join(parts, 'glow_mushrooms')
report()
finish('haunted', 'glow_mushrooms', kind='edge', footprint=0.18, notes='cluster lichtgevende paddenstoelen (hoedjes = glow_shroom)')
