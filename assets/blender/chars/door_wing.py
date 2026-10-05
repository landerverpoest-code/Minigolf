import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# One wing of a haunted revolving door. X 0..1 (game scales X to arm length), Z 0..1.1, Y +-0.06.
FRAME = mat('door_frame', '#44222f', rough=0.75)
WOODA = mat('door_wood', '#8e5662', rough=0.8)
WOODB = mat('door_wood2', '#784a5e', rough=0.8)
IRON = mat('door_iron', '#34333d', rough=0.45, metal=0.7)
GOLD = mat('door_gold', '#ffc23a', rough=0.25, metal=0.9)

T = 0.06          # half thickness
P = []
# --- frame: rails (stretch fine along X) and short end stiles
P.append(bx((0.0, -T, 0.0), (1.0, T, 0.11), FRAME, 0.018))          # bottom rail
P.append(bx((0.0, -T, 0.99), (1.0, T, 1.1), FRAME, 0.018))          # top rail
P.append(bx((0.004, -T, 0.09), (0.075, T, 1.01), FRAME, 0.014))       # hinge stile
P.append(bx((0.925, -T, 0.09), (0.995, T, 1.01), FRAME, 0.014))       # outer stile
P.append(bx((0.06, -0.05, 0.515), (0.94, 0.05, 0.6), FRAME, 0.014))  # middle rail
# --- horizontal planks in the two panels (recessed)
k = 0
for (z0, z1, n) in ((0.11, 0.515, 3), (0.6, 0.99, 3)):
    h = (z1 - z0) / n
    for i in range(n):
        za, zb = z0 + i * h + 0.004, z0 + (i + 1) * h - 0.004
        d = 0.034 + 0.004 * ((k * 7) % 3) / 2
        P.append(bx((0.07, -d, za), (0.93, d, zb), WOODA if k % 2 == 0 else WOODB, 0.014))
        k += 1
# --- iron bands across both faces, wrapped around the outer stile
for zc in (0.28, 0.83):
    for s in (-1, 1):
        y0, y1 = (s * 0.036, s * 0.05) if s > 0 else (-0.05, -0.036)
        P.append(bx((0.075, y0, zc - 0.035), (0.925, y1, zc + 0.035), IRON, 0.006))
    P.append(bx((0.0, -0.068, zc - 0.04), (0.06, 0.068, zc + 0.04), IRON, 0.008))   # hinge strap
    P.append(bx((0.95, -0.068, zc - 0.04), (1.0, 0.068, zc + 0.04), IRON, 0.008))  # end cap strap
    # rivets only near the ends
    for x in (0.03, 0.115, 0.885, 0.98):
        for s in (-1, 1):
            yy = s * (0.068 if x in (0.03, 0.98) else 0.05)
            r = cyl(r=0.014, h=0.016, verts=6, loc=(x, yy + s * 0.006, zc), rot=(math.pi / 2, 0, 0), material=IRON)
            P.append(r)
# --- iron corner brackets on the outer end (top and bottom, both faces)
for s in (-1, 1):
    y0, y1 = (0.06, 0.068) if s > 0 else (-0.068, -0.06)
    for (za, zb, zh0, zh1) in ((0.02, 0.2, 0.02, 0.09), (0.9, 1.08, 1.01, 1.08)):
        P.append(bx((0.935, y0, za), (0.985, y1, zb), IRON, 0.003))
        P.append(bx((0.8, y0, zh0), (0.985, y1, zh1), IRON, 0.003))
        P.append(cyl(r=0.012, h=0.012, verts=6, loc=(0.83, s * 0.072, (zh0 + zh1) / 2), rot=(math.pi / 2, 0, 0), material=IRON))
# --- gold knob near the outer end on both faces (on the middle rail)
for s in (-1, 1):
    P.append(bx((0.835, s * 0.05 - 0.008, 0.505), (0.885, s * 0.05 + 0.008, 0.61), GOLD, 0.006))
    P.append(cyl(r=0.012, h=0.04, verts=8, loc=(0.86, s * 0.075, 0.56), rot=(math.pi / 2, 0, 0), material=GOLD))
    P.append(sphere(r=0.038, loc=(0.86, s * 0.1, 0.56), seg=10, rings=6, material=GOLD))
    # tiny keyhole plate below the knob
    P.append(bx((0.853, s * 0.058 - 0.003, 0.525), (0.867, s * 0.058 + 0.003, 0.54), IRON))

body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Revolving-door wing. Part: body (origin (0,0,0) = revolving axis, no rotation). Spans X 0..1 (scale X to arm length), '
         'Z 0..1.1, thickness 0.12 centred on Y=0. Purple-brown horizontal planks in a dark frame, two iron bands with rivets '
         'near the ends, gold knob near the outer end (x~0.86, z 0.56) on both faces.')
finish('chars', 'door_wing', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('door_wing'); montage('door_wing', keys=('front', 'side', 'back', 'top'))
