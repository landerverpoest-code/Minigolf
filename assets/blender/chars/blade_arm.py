import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# Spinning tomb-trap blade arm. X 0..1 (game scales X), Z 0.31..0.53 (centre 0.42), thickness 0.1.
STEEL = mat('blade_steel', '#98a4b2', rough=0.22, metal=0.95)
EDGE = mat('blade_edge', '#e4eaf0', rough=0.28, metal=0.45)
DARK = mat('blade_dark', '#3a3d48', rough=0.4, metal=0.8)
RED = mat('blade_red', '#e0262c', rough=0.3, metal=0.2)
BRONZE = mat('blade_bronze', '#c4843a', rough=0.3, metal=0.9)

P = []
ZB, ZT = 0.31, 0.53
# main bar (steel) with a dark fuller groove on both faces
P.append(bx((0.01, -0.045, 0.385), (0.98, 0.045, ZT), STEEL, 0.014))
for s in (-1, 1):
    y0, y1 = (0.04, 0.05) if s > 0 else (-0.05, -0.04)
    P.append(bx((0.13, y0, 0.44), (0.95, y1, 0.465), DARK, 0.004))
    # bright bevelled top edge strip
P.append(bx((0.11, -0.03, ZT - 0.004), (0.985, 0.03, ZT + 0.006), EDGE, 0.004))
# dark seam between bar and teeth
P.append(bx((0.11, -0.042, 0.38), (0.975, 0.042, 0.395), DARK, 0.004))
# serrated cutting edge underneath (repeating sawteeth)
P.append(wedge_teeth(0.115, 0.975, 9, 0.39, ZB, 0.038, 0.005, EDGE))
# root clamp (bronze) at the hub end with bolts
P.append(bx((0.0, -0.05, ZB + 0.01), (0.115, 0.05, ZT + 0.01), BRONZE, 0.014))
for s in (-1, 1):
    for z in (0.37, 0.48):
        P.append(cyl(r=0.016, h=0.02, verts=6, loc=(0.058, s * 0.055, z), rot=(math.pi / 2, 0, 0), material=DARK))
# tip cap
P.append(bx((0.975, -0.05, 0.36), (1.0, 0.05, ZT + 0.005), DARK, 0.008))
# 4 red spikes on top, each on a dark collar
for x in (0.26, 0.46, 0.66, 0.86):
    P.append(cyl(r=0.032, h=0.02, verts=8, loc=(x, 0, ZT + 0.01), material=DARK))
    P.append(cyl(r=0.028, r2=0.0, h=0.1, verts=8, loc=(x, 0, ZT + 0.07), material=RED))

body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Spinning blade arm. Part: body (origin (0,0,0) = spin axis, no rotation). Polished steel bar spanning X 0..1 '
         '(scale X to arm length), Z 0.31..0.53 (centre 0.42), thickness 0.1 centred on Y=0; serrated edge (sawteeth) along '
         'the bottom, bronze root clamp at x 0..0.115, 4 red spikes on top (to z~0.65).')
finish('chars', 'blade_arm', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('blade_arm'); montage('blade_arm', keys=('front', 'side', 'back', 'top'))
