import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
stone = mat('stone', '#8a958a', rough=0.9)
dark = mat('stone_dark', '#5e6a63', rough=0.95)
moss = mat('moss', '#557f35', rough=1.0)
crack = mat('crack', '#262a2c', rough=1.0)

# afgeronde steen (voorkant = -Y)
W, H = 0.48, 0.62
poly = [(-W/2, 0), (W/2, 0)] + [(x, H - W/2 + z) for x, z in arc2d(0, 0, W/2, 0, math.pi, 8)]
slab = prism(poly, 0.12, stone, axis='y', loc=(0, 0, 0.09), bevel=0.016)
inset(slab, lambda c, n: n.y < -0.9, thick=0.05, depth=-0.02)
# kruis-reliëf in het paneel
c1 = box((0.035, 0.02, 0.2), loc=(0, -0.05, 0.47), material=dark)
c2 = box((0.13, 0.02, 0.035), loc=(0, -0.05, 0.51), material=dark)
# barst
ck = tube([(-0.21, -0.067, 0.36), (-0.12, -0.067, 0.31), (-0.07, -0.067, 0.34), (0.0, -0.067, 0.24), (0.07, -0.067, 0.2)],
          r=[0.004, 0.012, 0.011, 0.01, 0.003], seg=3, material=crack, smooth=False, sx=0.6)
chip = ico(0.05, loc=(0.2, 0.0, 0.62), material=dark, scale=(1, 1.4, 0.6), jitter=0.01, seed=3)
m1 = shade_smooth(ico(0.08, loc=(-0.15, -0.0, 0.67), material=moss, scale=(1.5, 1.2, 0.4), jitter=0.012, seed=1))
grave = join([slab, c1, c2, ck, chip, m1], 'slab')
T(grave, rot=(math.radians(-5), math.radians(7), math.radians(3)), pivot=(0, 0, 0.1))
base = box((0.6, 0.22, 0.1), loc=(0, 0, 0.05), material=dark, bevel=0.015)
m2 = shade_smooth(ico(0.07, loc=(-0.27, -0.07, 0.1), material=moss, scale=(1.5, 1.0, 0.55), jitter=0.012, seed=2))
m3 = shade_smooth(ico(0.06, loc=(0.25, 0.07, 0.1), material=moss, scale=(1.4, 1.0, 0.55), jitter=0.01, seed=4))
join([grave, base, m2, m3], 'tombstone_a')
report()
finish('haunted', 'tombstone_a', kind='edge', footprint=0.35, notes='afgeronde grafsteen met kruisreliëf, barst, mos, licht scheef')
