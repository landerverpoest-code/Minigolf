import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# Hub post of the tomb blade trap: radius 0.28, height 0.7, red cap ball on top (top ~0.95). Origin base centre.
STEEL = mat('blade_steel', '#98a4b2', rough=0.22, metal=0.95)
DARK = mat('blade_dark', '#3a3d48', rough=0.4, metal=0.8)
RED = mat('blade_red', '#e0262c', rough=0.3, metal=0.2)
BRONZE = mat('blade_bronze', '#c4843a', rough=0.3, metal=0.9)
GOLD = mat('blade_gold', '#ffcc3a', rough=0.25, metal=0.9)

SEG = 20
P = []
# bronze stepped foot
P.append(lathe([(0.0, 0.0), (0.28, 0.0), (0.28, 0.05), (0.265, 0.07), (0.25, 0.08), (0.0, 0.08)], seg=SEG, material=BRONZE))
# steel drum
P.append(lathe([(0.235, 0.08), (0.235, 0.6)], seg=SEG, material=STEEL, caps=(False, False)))
# dark slot ring where the blade arms run (z 0.31..0.53)
P.append(lathe([(0.245, 0.3), (0.255, 0.31), (0.255, 0.53), (0.245, 0.54)], seg=SEG, material=DARK, caps=(False, False)))
# bronze bands with gold rivets
for zc in (0.17, 0.6):
    P.append(lathe([(0.237, zc - 0.04), (0.262, zc - 0.03), (0.268, zc), (0.262, zc + 0.03), (0.237, zc + 0.04)],
                   seg=SEG, material=BRONZE, caps=(False, False)))
    for k in range(8):
        a = TAU * k / 8 + TAU / 16
        P.append(ell((math.cos(a) * 0.266, math.sin(a) * 0.266, zc), (0.017, 0.017, 0.017), seg=6, rings=3, material=GOLD))
# vertical steel ribs on the slot ring
for k in range(12):
    a = TAU * k / 12
    o = bx((-0.012, -0.014, 0.32), (0.012, 0.014, 0.52), STEEL)
    place(o, (math.cos(a) * 0.258, math.sin(a) * 0.258, 0), (0, 0, math.degrees(a)))
    P.append(o)
# bronze dome on top with spikes
P.append(lathe([(0.237, 0.64), (0.22, 0.67), (0.18, 0.7), (0.12, 0.72), (0.08, 0.73), (0.0, 0.73)], seg=SEG, material=BRONZE, caps=(True, False)))
for k in range(6):
    a = TAU * k / 6
    c = V(math.cos(a) * 0.19, math.sin(a) * 0.19, 0.7)
    sp = cone(r=0.03, h=0.08, verts=6, material=GOLD)
    place(sp, (0, 0, 0))
    M = Matrix.Translation(c) @ (V(math.cos(a) * 0.5, math.sin(a) * 0.5, 1).to_track_quat('Z', 'Y').to_matrix().to_4x4()) @ Matrix.Translation((0, 0, 0.03))
    xf(sp, M)
    P.append(sp)
# gold collar + red cap ball (top ~0.95)
P.append(lathe([(0.0, 0.72), (0.09, 0.72), (0.085, 0.75), (0.06, 0.77), (0.0, 0.77)], seg=16, material=GOLD))
P.append(ell((0, 0, 0.84), (0.11, 0.11, 0.11), seg=16, rings=10, material=RED))

body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Blade-trap hub post. Part: body (origin base centre (0,0,0)). Bronze foot r=0.28, steel drum r~0.24 with a dark ribbed slot ring '
         'at z 0.31..0.53 (where blade arms attach), bronze bands with gold rivets, spiked bronze dome, red cap ball (top z 0.95).')
finish('chars', 'blade_hub', kind='char', footprint=0.28, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('blade_hub'); montage('blade_hub', keys=('front', 'side', 'back', 'top'))
