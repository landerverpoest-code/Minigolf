import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _palm import *

M = palm_mats()
sand = mat('sand', '#ecd39a', rough=0.95)
# zandheuvel
prof = [(1.45, 0.0), (1.3, 0.12), (0.95, 0.3), (0.5, 0.42), (0.0, 0.46)]
mound = lathe(prof, verts=11, material=sand, jitter=0.08, seed=4, cap0=True)
shade_smooth(mound, 60)
cfg = [  # basis, hoogte, lean, seed, noten
    ((-0.25, 0.15, 0.3), 4.6, (-0.9, 0.5), 11, 3),
    ((0.35, 0.2, 0.25), 3.5, (1.0, 0.45), 12, 0),
    ((0.05, -0.4, 0.25), 2.4, (0.3, -0.9), 13, 0),
]
for b, h, ln, sd, nn in cfg:
    palm(M, base=b, height=h, lean=ln, r0=0.15 + 0.012 * h, r1=0.1, segs=5 if h < 4 else 6, verts=5, fronds=6, up_fronds=0,
         flen=1.2 + 0.25 * h, fwidth=0.36 + 0.03 * h, frise=0.7, fdroop=0.75 + 0.06 * h, fsegs=4, nuts=nn, seed=sd, flare=True, nut_seg=(6, 4))
join_all('palm_cluster')
report()
finish('water', 'palm_cluster', kind='scatter', footprint=1.3, notes='Drie palmen van verschillende hoogte op een zandheuveltje')
closeup('palm_cluster')
