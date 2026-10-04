import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

POLE = mat('flag_pole', '#f7f7f4', rough=0.35, metal=0.15)
GOLD = mat('gold', '#f5bd22', rough=0.25, metal=0.85)
STEEL = mat('flag_steel', '#9aa3ae', rough=0.3, metal=0.85)

b = []
# steel ferrule at the foot, white pole, gold collar under the ball
b.append(lathe([(0.0, 0.0), (0.02, 0.0), (0.031, 0.015), (0.031, 0.075), (0.026, 0.09)], seg=10, material=STEEL, caps=(False, False)))
b.append(lathe([(0.025, 0.085), (0.025, 1.2), (0.024, 2.3)], seg=10, material=POLE, caps=(False, False)))
b.append(lathe([(0.024, 2.29), (0.032, 2.3), (0.032, 2.322), (0.022, 2.335)], seg=10, material=GOLD, caps=(False, True)))
b.append(sphere(r=0.048, loc=(0, 0, 2.352), seg=12, rings=8, material=GOLD))
# little cup-rim ring at the bottom (sits on the cup insert)
b.append(torus(R=0.075, r=0.013, seg=16, ring=5, material=POLE, loc=(0, 0, 0.013)))
for k in range(4):   # spokes to the ferrule
    a = TAU * k / 4
    b.append(tube([V(math.cos(a) * 0.028, math.sin(a) * 0.028, 0.012), V(math.cos(a) * 0.066, math.sin(a) * 0.066, 0.012)],
                  0.007, seg=4, material=STEEL))
body = part(b, 'body', (0, 0, 0), angle=50)

report()
notes = ('Parts: body only (origin 0,0,0 = bottom centre of the pole). White pole r=0.025 up to z=2.3, gold collar + gold ball '
         '(centre z=2.352, r=0.048, top at 2.4), steel ferrule at the foot and a small white cup-rim ring (R=0.075) at z~0.013. '
         'Cloth is added by the game (attach along the pole, e.g. z 1.75-2.28). Materials: flag_pole, gold, flag_steel.')
std_view()
finish('chars', 'golf_flag', kind='char', footprint=0.09, grounded=False, notes=notes)
