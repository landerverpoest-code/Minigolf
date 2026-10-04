import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

CAP = mat('cap', '#e8262b', rough=0.3, emit='#ff1a1a', emit_strength=0.15)   # the game turns this green when pressed
METAL = mat('button_metal', '#8a93a0', rough=0.35, metal=0.8)
YEL = mat('button_yellow', '#ffc61a', rough=0.5)
WHITE = mat('eye_white', '#ffffff', rough=0.3)
DARK = mat('eye_dark', '#1c1a26', rough=0.35)
BLUSH = mat('blush', '#ff8fa8', rough=0.6)

CZ = 0.2      # cap origin (base centre of the cap)
base = []
# --- metal housing: foot flange + body
base.append(lathe([(0.45, 0.0), (0.45, 0.035), (0.44, 0.05), (0.415, 0.062), (0.385, 0.068), (0.375, 0.08), (0.37, 0.15),
                   (0.365, 0.165)], seg=36, material=METAL, caps=(True, False)))
# --- yellow/black hazard collar
col = lathe([(0.365, 0.16), (0.37, 0.175), (0.36, 0.195), (0.33, 0.212), (0.305, 0.214), (0.298, 0.2)], seg=48,
            material=YEL, caps=(False, False))
iso_paint(col, lambda p: math.sin(9 * math.atan2(p.y, p.x) + p.z * 18), DARK)
base.append(col)
base.append(cyl(r=0.3, h=0.03, verts=36, loc=(0, 0, 0.19), material=DARK))   # dark gap/well under the cap
# --- hex bolts on the flange
for k in range(8):
    a = TAU * k / 8 + TAU / 16
    base.append(cyl(r=0.022, h=0.02, verts=6, loc=(math.cos(a) * 0.412, math.sin(a) * 0.412, 0.068), material=METAL))
    base.append(ell((math.cos(a) * 0.412, math.sin(a) * 0.412, 0.078), (0.012, 0.012, 0.006), seg=6, rings=3, material=METAL))
basep = part(base, 'base', (0, 0, 0), angle=40)

# ---------------------------------------------------------------- cap: red gumdrop with a face
cp = []
dome = lathe([(0.285, -0.01), (0.292, 0.04), (0.29, 0.1), (0.275, 0.15), (0.24, 0.195), (0.18, 0.228), (0.1, 0.246),
              (0.0, 0.252)], seg=32, material=CAP, caps=(True, False))
cp.append(dome)
# cartoon shine on the dome (upper left)
sh = ell((0, 0, 0), (0.07, 0.02, 0.03), seg=8, rings=4, material=WHITE)
xf(sh, Matrix.Translation((0.12, -0.12, 0.215)) @ rotm((40, 0, 35)))
cp.append(sh)
cp.append(ell((0.175, -0.07, 0.205), (0.022, 0.02, 0.016), seg=6, rings=3, material=WHITE))


def surf(x, z):
    """point on the dome front at height z (approx, radius profile)."""
    rr = 0.29 if z < 0.1 else 0.29 - (z - 0.1) * 0.5
    return V(x, -math.sqrt(max(rr * rr - x * x, 0.0001)), z)


for sx in (-1, 1):
    p = surf(sx * 0.11, 0.15)
    cp += eye(p + V(0, 0.02, 0), V(sx * 0.32, -1, 0.25), r=0.082, white=WHITE, black=DARK, depth=0.55, tall=1.25,
              pupil=0.68, look=(-sx * 0.1, 0, 0.1), seg=12, pseg=9)
    # brows
    bp = [surf(sx * 0.065, 0.236) + V(0, -0.004, 0), surf(sx * 0.11, 0.246) + V(0, -0.006, 0), surf(sx * 0.155, 0.236) + V(0, -0.004, 0)]
    cp.append(tube(bp, [0.008, 0.011, 0.007], seg=5, material=DARK))
    # blush
    b = surf(sx * 0.19, 0.085)
    cp.append(ell(b + V(0, 0.012, 0), (0.042, 0.016, 0.025), seg=8, rings=4, material=BLUSH, rot=(0, 0, sx * -38)))
# smile
sm = [surf(x, 0.075 - 0.45 * (0.075 ** 2 - x * x) ** 0.5) + V(0, -0.004, 0) for x in (-0.075, -0.05, -0.025, 0.0, 0.025, 0.05, 0.075)]
cp.append(tube(sm, [0.008, 0.011, 0.013, 0.013, 0.013, 0.011, 0.008], seg=5, material=DARK))
capo = part(cp, 'cap', (0, 0, 0))
capo.location = (0, 0, CZ)
bpy.context.view_layer.update()

report()
notes = ('Parts/pivots (Blender coords, front -Y): base (origin 0,0,0; steel housing r=0.45 with bolts, yellow/black hazard '
         f'collar, dark well); cap (origin = its base centre (0,0,{CZ}); red dome with eyes, brows, blush and smile, top at z~0.45, '
         'dome material "cap" (turn it green when pressed); press it down along Z). '
         'Materials: cap, button_metal, button_yellow, eye_white, eye_dark, blush.')
std_view()
finish('chars', 'button', kind='char', footprint=0.45, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['cap'].location.z = CZ - 0.12
    views('button', pose); montage('button')
