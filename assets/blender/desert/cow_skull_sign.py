import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert'); from _deco import *

WOOD = mat('tent_wood', '#6e4a2c', rough=0.85)
PLANK = mat('date_bark', '#9a7550', rough=0.9)
BONE = mat('cream', '#f2dfb4', rough=0.7)
DARK = mat('eye_dark', '#3b2a20', rough=0.7)
RED = mat('terracotta', '#c9573c', rough=0.7)

# paal licht scheef
post = rod((0, 0, 0), (0.03, 0.02, 1.25), r=0.05, r2=0.045, verts=5, material=WOOD)
# pijlvormig bord naar links en een kleiner naar rechts
def arrow(z, length, dirn, yaw):
    L = length
    prof = [(0, -0.09), (L - 0.12, -0.09), (L, 0.0), (L - 0.12, 0.09), (0, 0.09)]
    o = prism([(x * dirn, y) for x, y in prof], 0.035, material=PLANK, axis='Y')
    # rood randje (geschilderde streep)
    s = prism([(x * dirn, y * 0.25) for x, y in prof[:1] + [(L - 0.2, -0.09), (L - 0.2, 0.09)] + prof[4:]], 0.04, material=RED, axis='Y')
    return [T(o, rot=(0, 0, yaw), loc=(0.02 - dirn * 0.06, 0, z)), T(s, rot=(0, 0, yaw), loc=(0.02 - dirn * 0.06, 0, z))]
arrow(0.95, 0.62, -1, 8)
arrow(0.7, 0.48, 1, -12)
for z in (0.95, 0.7):
    box((0.03, 0.06, 0.03), loc=(0.02, -0.03, z), material=DARK)
# koeienschedel op de top
S = Vector((0.03, -0.04, 1.32))
skull = sphere(1.0, seg=6, rings=4, material=BONE, scale=(0.11, 0.08, 0.1), smooth=False)
T(skull, loc=S)
snout = lathe([(0.075, 0.0), (0.06, 0.14), (0.04, 0.2)], verts=5, material=BONE, cap0=False)
T(snout, rot=(160, 0, 0), loc=S + Vector((0, -0.02, -0.02)))
for s in (-1, 1):
    sphere(0.028, loc=S + Vector((s * 0.05, -0.075, 0.02)), seg=4, rings=3, material=DARK)
    horn = tube([S + Vector((s * 0.09, 0.0, 0.05)), S + Vector((s * 0.2, -0.01, 0.06)), S + Vector((s * 0.28, -0.03, 0.14)), S + Vector((s * 0.3, -0.05, 0.22))],
                [0.03, 0.025, 0.018, 0.0], verts=4, material=BONE, smooth=True)
# zandhoopje + steentjes aan de voet
lathe([(0.25, 0.0), (0.18, 0.04), (0.0, 0.05)], verts=6, material=PLANK, jitter=0.15, seed=2)
o = join_all('cow_skull_sign')
report()
done('desert', 'cow_skull_sign', kind='edge', footprint=0.35,
     notes='Woestijnwegwijzer: scheve houten paal met twee pijlborden met rode streep, koeienschedel met lange hoorns op de top')
