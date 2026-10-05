import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# Castle drawbridge deck. X -0.5..0.5 (width, game scales), Y 0 (hinge) .. -1.0 (far end, game scales), Z -0.18..0.
BEAM = mat('bridge_beam', '#4a3020', rough=0.8)
WOODA = mat('bridge_wood', '#a8743f', rough=0.8)
WOODB = mat('bridge_wood2', '#8f5f33', rough=0.8)
IRON = mat('bridge_iron', '#3a3a42', rough=0.45, metal=0.7)

X0, X1, Y0, Y1, Z0 = -0.5, 0.5, 0.0, -1.0, -0.18
P = []
# dark under-structure (shows in the plank gaps)
P.append(bx((X0 + 0.02, Y1 + 0.02, Z0), (X1 - 0.02, Y0 - 0.02, -0.06), BEAM, 0.015))
# heavy planks running across (along X), repeated along the length
n = 8
pw = (abs(Y1 - Y0) - 0.02) / n
for i in range(n):
    ya = Y0 - 0.01 - i * pw
    top = -0.004 * ((i * 3) % 3) / 2
    o = bx((X0 + 0.004, ya - pw + 0.007, -0.13), (X1 - 0.004, ya - 0.007, top), WOODA if i % 2 == 0 else WOODB, 0.02)
    P.append(o)
# iron edge bands along both long edges, wrapped over the top and down the side
for sx in (-1, 1):
    xa, xb = (X1 - 0.075, X1 + 0.0) if sx > 0 else (X0, X0 + 0.075)
    P.append(bx((xa, Y1 + 0.004, -0.005), (xb, Y0 - 0.004, 0.012), IRON, 0.005))
    xs = (X1 - 0.006, X1 + 0.004) if sx > 0 else (X0 - 0.004, X0 + 0.006)
    P.append(bx((xs[0], Y1 + 0.004, -0.055), (xs[1], Y0 - 0.004, 0.0), IRON, 0.003))
# far-end iron cross strap with big rivets
P.append(bx((X0 + 0.004, Y1, -0.006), (X1 - 0.004, Y1 + 0.085, 0.016), IRON, 0.006))
P.append(bx((X0 + 0.004, Y1 - 0.004, -0.055), (X1 - 0.004, Y1 + 0.006, 0.012), IRON, 0.003))
for x in (-0.44, -0.2, 0.2, 0.44):
    P.append(ell((x, Y1 + 0.043, 0.016), (0.03, 0.03, 0.02), seg=8, rings=4, material=IRON))
# a few rivets on the edge bands near both ends
for sx in (-1, 1):
    for y in (-0.06, -0.86):
        P.append(ell((sx * 0.4625, y, 0.012), (0.018, 0.018, 0.012), seg=6, rings=3, material=IRON))
# hinge rod along X at the hinge line (cylinder along X stretches cleanly), with iron knuckles
P.append(cyl(r=0.045, h=0.98, verts=10, loc=(0, -0.045, -0.09), rot=(0, math.pi / 2, 0), material=BEAM))
for x in (-0.4, 0.0, 0.4):
    P.append(cyl(r=0.055, h=0.12, verts=10, loc=(x, -0.045, -0.09), rot=(0, math.pi / 2, 0), material=IRON))
# chain eye rings on the side faces near the far end (in the YZ plane)
for sx in (-1, 1):
    r = torus(R=0.035, r=0.01, seg=10, ring=5, rot=(0, math.pi / 2, 0), loc=(sx * 0.512, Y1 + 0.12, -0.08), material=IRON)
    P.append(r)
    P.append(bx((sx * 0.5 - 0.004, Y1 + 0.085, -0.13), (sx * 0.5 + 0.008, Y1 + 0.155, -0.03), IRON, 0.003) if sx > 0 else
             bx((sx * 0.5 - 0.008, Y1 + 0.085, -0.13), (sx * 0.5 + 0.004, Y1 + 0.155, -0.03), IRON, 0.003))

body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Castle drawbridge deck. Part: body (origin (0,0,0) = centre of the hinge line, no rotation). Spans X -0.5..0.5 (width, '
         'scale X), Y 0 (hinge) .. -1.0 (far end, scale Y), Z -0.18..0 (top at z=0; iron bands/rivets stand up to ~0.03). '
         '8 heavy planks running across, iron edge bands along both long edges, far-end iron strap with 4 big rivets, '
         'hinge rod with knuckles along the hinge line, chain eye rings on the side faces near the far end.')
finish('chars', 'drawbridge_deck', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('drawbridge_deck'); montage('drawbridge_deck', keys=('front', 'side', 'back', 'top'))
