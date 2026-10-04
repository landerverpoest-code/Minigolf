import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

WOOD = mat('shield_wood', '#8a5a36', rough=0.85)
RED = mat('shield_red', '#d42a2a', rough=0.45)
WHITE = mat('shield_white', '#f6f2ea', rough=0.45)
GOLD = mat('gold', '#f2b61e', rough=0.3, metal=0.75)
BLUE = mat('shield_blue', '#1f63c8', rough=0.35, metal=0.3)
IRON = mat('shield_iron', '#3d3d45', rough=0.45, metal=0.7)

SC = V(0, -0.02, 0.78)          # shield centre (pivot)
RS = 0.46
ROT = Matrix.Translation(SC) @ Matrix.Rotation(math.pi / 2, 4, 'X')    # local +Z (front) -> world -Y


def hfront(r):
    return 0.032 + 0.04 * (1 - (r / RS) ** 2)


SEG = 36
sh = []
bands = [(0.085, 0.19, RED), (0.19, 0.27, WHITE), (0.27, 0.345, RED), (0.345, 0.375, GOLD)]
for r0, r1, m in bands:
    rr = [r0 + (r1 - r0) * t for t in (0, 0.5, 1)]
    sh.append(lathe([(r, hfront(r)) for r in rr], seg=SEG, material=m, caps=(False, False), M=ROT))
sh.append(lathe([(0.0, hfront(0) - 0.004), (0.085, hfront(0.085))], seg=SEG, material=GOLD, caps=(False, False), M=ROT))
# raised blue rim with a rolled edge, and the flat back
rim = [(0.375, hfront(0.375)), (0.385, hfront(0.385) + 0.018), (0.42, hfront(0.42) + 0.022), (0.452, 0.04), (0.462, 0.02),
       (0.458, 0.0), (0.44, -0.008), (0.0, -0.008)]
sh.append(lathe(rim, seg=SEG, material=BLUE, caps=(False, False), M=ROT))
# central gold boss (dome) with a ring
boss = lathe([(0.09, hfront(0.09) - 0.005), (0.088, hfront(0.09) + 0.02), (0.07, hfront(0.07) + 0.05), (0.04, hfront(0.04) + 0.07),
              (0.0, hfront(0) + 0.077)], seg=20, material=GOLD, caps=(True, False), M=ROT)
sh.append(boss)
sh.append(xf(torus(R=0.095, r=0.012, seg=24, ring=5, material=GOLD), ROT @ Matrix.Translation((0, 0, hfront(0.095)))))
# gold rivets on the rim
for k in range(12):
    a = TAU * k / 12
    p = ROT @ V(math.cos(a) * 0.418, math.sin(a) * 0.418, hfront(0.418) + 0.022)
    sh.append(ell(p, (0.017, 0.012, 0.017), seg=8, rings=4, material=GOLD))
# little gold star points between the red/white rings (heraldic accent)
for k in range(4):
    a = math.pi / 4 + TAU * k / 4
    s_ = prism(star_pts(0.03, 0.013, 4, phase=a), 0, 0.012, material=GOLD)
    xf(s_, ROT @ Matrix.Translation((math.cos(a) * 0.23, math.sin(a) * 0.23, hfront(0.23) - 0.002)))
    sh.append(s_)
shield = part(sh, 'shield', SC, angle=50)

# ---------------------------------------------------------------- body: wooden post behind the shield
b = []
PY = 0.13
b.append(box((0.13, 0.13, 1.08), loc=(0, PY, 0.54), material=WOOD, bevel=0.015))
b.append(cone(r=0.105, h=0.12, verts=4, loc=(0, PY, 1.14), rot=(0, 0, math.pi / 4), material=WOOD))
b.append(box((0.145, 0.145, 0.04), loc=(0, PY, 1.06), material=IRON, bevel=0.006))
b.append(box((0.145, 0.145, 0.04), loc=(0, PY, 0.2), material=IRON, bevel=0.006))
# axle from post to the shield back + iron bracket plate
b.append(cyl(r=0.035, h=0.13, verts=10, loc=(0, 0.04, SC.z), rot=(math.pi / 2, 0, 0), material=IRON))
b.append(box((0.16, 0.03, 0.16), loc=(0, PY - 0.075, SC.z), material=IRON, bevel=0.008))
for sx in (-1, 1):
    for sz in (-1, 1):
        b.append(ell((sx * 0.055, PY - 0.092, SC.z + sz * 0.055), (0.012, 0.008, 0.012), seg=6, rings=3, material=IRON))
# wood grain grooves on the front face of the post
for k, z in enumerate((0.35, 0.5, 0.95)):
    b.append(box((0.006, 0.01, 0.12 + 0.04 * k), loc=(0.03 * (k - 1), PY - 0.066, z), material=IRON))
# little stone/earth mound at the foot
for k, (x, y, r) in enumerate(((0.12, 0.05, 0.08), (-0.11, 0.08, 0.07), (0.06, 0.25, 0.075), (-0.08, 0.22, 0.065), (0.0, -0.02, 0.06))):
    b.append(ico(r=r, sub=1, loc=(x, y, r * 0.72), material=IRON if k % 2 else WOOD, scale=(1, 1, 0.6), jitter=0.008, seed=k))
body = part(b, 'body', (0, 0, 0), angle=45)

report()
notes = ('Parts/pivots (Blender coords, front -Y): body (origin 0,0,0; wooden post 1.2 m behind the shield at y=0.13 with iron '
         f'bands, axle and stones); shield (pivot at its centre ({SC.x:.2f},{SC.y:.2f},{SC.z:.2f}); round heraldic shield r=0.46 '
         'facing -Y: gold boss, red/white/red rings, gold ring, raised blue rim with gold rivets; spin/wobble it about Blender Y '
         '(three.js z)). Materials: shield_wood, shield_red, shield_white, gold, shield_blue, shield_iron.')
std_view()
finish('chars', 'shield_sign', kind='char', footprint=0.46, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['shield'].rotation_euler = (0, 0.6, 0)
    views('shield_sign', pose); montage('shield_sign')
