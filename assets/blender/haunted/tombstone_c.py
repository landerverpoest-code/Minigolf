import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
stone = mat('stone', '#8a958a', rough=0.9)
dark = mat('stone_dark', '#5e6a63', rough=0.95)
moss = mat('moss', '#557f35', rough=1.0)
crack = mat('crack', '#262a2c', rough=1.0)

# obelisk
b1 = box((0.36, 0.36, 0.08), loc=(0, 0, 0.04), material=dark, bevel=0.012)
b2 = box((0.27, 0.27, 0.12), loc=(0, 0, 0.14), material=stone, bevel=0.012)
plate = box((0.17, 0.02, 0.07), loc=(0, -0.138, 0.14), material=dark)
shaft = cyl(0.13, 0.62, loc=(0, 0, 0.51), rot=(0, 0, math.pi / 4), verts=4, r2=0.08, material=stone)
bev(shaft, 0.01)
tip = cone(0.085, 0.12, loc=(0, 0, 0.88), rot=(0, 0, math.pi / 4), verts=4, material=stone)
band = box((0.2, 0.2, 0.03), loc=(0, 0, 0.215), material=dark)
ck = tube([(-0.06, -0.083, 0.68), (-0.02, -0.08, 0.6), (-0.045, -0.076, 0.52), (0.02, -0.07, 0.44)],
          r=[0.003, 0.009, 0.009, 0.003], seg=3, material=crack, smooth=False, sx=0.6)
m3 = shade_smooth(ico(0.045, loc=(-0.05, -0.05, 0.76), material=moss, scale=(1.2, 0.8, 0.7), jitter=0.006, seed=10))
ob = join([b2, plate, shaft, tip, band, ck, m3], 'ob')
T(ob, rot=(math.radians(4), math.radians(5), math.radians(8)), pivot=(0, 0, 0.08))
m1 = shade_smooth(ico(0.07, loc=(0.15, -0.1, 0.09), material=moss, scale=(1.4, 1.2, 0.55), jitter=0.01, seed=8))
m2 = shade_smooth(ico(0.06, loc=(-0.13, 0.14, 0.09), material=moss, scale=(1.4, 1.0, 0.5), jitter=0.01, seed=9))
join([ob, b1, m1, m2], 'tombstone_c')
report()
finish('haunted', 'tombstone_c', kind='edge', footprint=0.3, notes='obelisk-grafsteen op getrapte voet, barst, mos')
