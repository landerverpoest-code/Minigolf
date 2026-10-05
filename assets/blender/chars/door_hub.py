import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# Central post of the haunted revolving door: radius 0.12, height 1.3, finial on top. Origin base centre.
WOOD = mat('hub_wood', '#4a2a38', rough=0.7)
IRON = mat('door_iron', '#34333d', rough=0.45, metal=0.7)
GOLD = mat('door_gold', '#ffc23a', rough=0.25, metal=0.9)
GLOW = mat('glow_hub', '#c070ff', rough=0.4, emit='#b25cff', emit_strength=1.6)

SEG = 16
R = 0.12
P = []
# iron foot ring + wooden pole with slight entasis
P.append(lathe([(0.0, 0.0), (0.165, 0.0), (0.165, 0.03), (0.15, 0.05), (0.13, 0.06), (0.0, 0.06)], seg=SEG, material=IRON))
P.append(lathe([(R, 0.05), (R, 1.25)], seg=SEG, material=WOOD, caps=(False, False)))
# iron bands along the pole (where the wings attach)
for zc in (0.1, 0.28, 0.83, 1.2):
    P.append(lathe([(R + 0.003, zc - 0.035), (R + 0.016, zc - 0.022), (R + 0.016, zc + 0.022), (R + 0.003, zc + 0.035)],
                   seg=SEG, material=IRON, caps=(False, False)))
    for k in range(4):
        a = TAU * k / 4 + TAU / 8
        P.append(ell((math.cos(a) * (R + 0.018), math.sin(a) * (R + 0.018), zc), (0.013, 0.013, 0.013), seg=6, rings=4, material=GOLD))
# vertical grooves suggested by thin dark wooden strips
for k in range(8):
    a = TAU * k / 8
    o = bx((-0.008, -0.006, 0.36), (0.008, 0.006, 0.75), IRON)
    place(o, (math.cos(a) * (R - 0.001), math.sin(a) * (R - 0.001), 0), (0, 0, math.degrees(a) + 90))
    P.append(o)
# top cap + finial (gold ball, glowing purple orb, spike)
P.append(lathe([(0.0, 1.25), (R + 0.03, 1.25), (R + 0.035, 1.28), (R + 0.01, 1.3), (0.07, 1.31), (0.0, 1.31)], seg=SEG, material=IRON))
P.append(lathe([(0.0, 1.31), (0.05, 1.32), (0.03, 1.35), (0.0, 1.35)], seg=12, material=GOLD))
P.append(ell((0, 0, 1.4), (0.055, 0.055, 0.055), seg=12, rings=8, material=GLOW))
P.append(lathe([(0.025, 1.445), (0.0, 1.53)], seg=8, material=GOLD, caps=(True, False)))
for k in range(4):
    a = TAU * k / 4
    t = tube([V(math.cos(a) * 0.04, math.sin(a) * 0.04, 1.34), V(math.cos(a) * 0.07, math.sin(a) * 0.07, 1.4),
              V(math.cos(a) * 0.03, math.sin(a) * 0.03, 1.46)], [0.008, 0.008, 0.006], seg=5, material=GOLD)
    P.append(t)

body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Revolving-door hub post. Part: body (origin base centre (0,0,0)). Dark wood pole r=0.12, height 1.3 with iron bands '
         '(gold rivets), iron foot ring r=0.165, top cap and a finial (gold cage around a glowing purple orb "glow_hub", spike) up to z~1.53.')
finish('chars', 'door_hub', kind='char', footprint=0.165, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('door_hub'); montage('door_hub', keys=('front', 'side', 'back', 'top'))
