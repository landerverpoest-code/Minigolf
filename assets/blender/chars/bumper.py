import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

# ---------------------------------------------------------------- materials
METAL = mat('bumper_metal', '#2b3040', rough=0.32, metal=0.75)
CHROME = mat('chrome', '#dfe5ee', rough=0.16, metal=1.0)
GLOW = mat('bumper_glow', '#ff1fc8', rough=0.3, emit='#ff1fc8', emit_strength=0.9)
CAPM = mat('bumper_cap', '#fbf7ff', rough=0.22)
TOP = mat('cap_top', '#3b2a9c', rough=0.2, metal=0.1)
STAR = mat('bumper_star', '#ffc42e', rough=0.3, metal=0.4, emit='#ffa000', emit_strength=0.25)
LAMP = GLOW

SEG = 32
R = 0.55          # base radius (collision)
CAPZ = 0.43       # cap origin (base centre of the cap)

base_parts = []
# --- foot plate: dark metal disc with a bevelled rim
base_parts.append(lathe([(R, 0), (R, 0.03), (R - 0.012, 0.05), (R - 0.04, 0.062), (0.46, 0.066)],
                        seg=SEG, material=METAL, caps=(False, False)))
# --- chrome kicker skirt (the ring that 'kicks' the ball)
base_parts.append(lathe([(0.475, 0.06), (0.478, 0.085), (0.465, 0.105), (0.43, 0.15), (0.405, 0.168),
                         (0.34, 0.172)], seg=SEG, material=CHROME, caps=(False, False)))
# --- body column: dark metal with a groove for the neon ring and a flared top
base_parts.append(lathe([(0.345, 0.17), (0.345, 0.235), (0.315, 0.25), (0.315, 0.33), (0.345, 0.345),
                         (0.35, 0.385)], seg=SEG, material=METAL, caps=(False, False)))
# --- neon ring (magenta, the game pulses it)
ring = torus(R=0.338, r=0.042, seg=SEG, ring=7, material=GLOW)
place(ring, (0, 0, 0.29))
base_parts.append(ring)
# --- vertical chrome ribs on the lower column
for k in range(10):
    a = TAU * k / 10 + TAU / 20
    c = V(math.cos(a) * 0.35, math.sin(a) * 0.35, 0.205)
    rib = box((0.026, 0.03, 0.07), loc=(0, 0, 0), material=CHROME)
    place(rib, c, (0, 0, math.degrees(a)))
    base_parts.append(rib)
# --- chrome top lip under the cap
base_parts.append(lathe([(0.33, 0.38), (0.405, 0.398), (0.418, 0.412), (0.41, 0.426), (0.36, CAPZ)],
                         seg=SEG, material=CHROME, caps=(False, False)))
# --- bolts and cyan lamps on the foot plate
for k in range(8):
    a = TAU * k / 8
    b = cyl(r=0.024, h=0.022, verts=6, loc=(math.cos(a) * 0.508, math.sin(a) * 0.508, 0.073), material=CHROME)
    base_parts.append(b)
    a2 = a + TAU / 16
    lp = ell((math.cos(a2) * 0.508, math.sin(a2) * 0.508, 0.066), (0.022, 0.022, 0.016), seg=6, rings=3, material=LAMP)
    base_parts.append(lp)
base = part(base_parts, 'base', (0, 0, 0), angle=40)

# ---------------------------------------------------------------- cap (origin = its base centre)
cap_parts = []
cap_parts.append(lathe([(0.37, 0.0), (0.385, 0.012), (0.389, 0.024)], seg=SEG, material=CAPM, caps=(True, False)))
cap_parts.append(lathe([(0.389, 0.024), (0.3905, 0.042)], seg=SEG, material=GLOW, caps=(False, False)))
cap_parts.append(lathe([(0.3905, 0.042), (0.388, 0.054), (0.38, 0.068), (0.355, 0.086), (0.3, 0.103), (0.27, 0.107)],
                       seg=SEG, material=CAPM, caps=(False, False)))
cap_parts.append(lathe([(0.27, 0.107), (0.2, 0.114), (0.1, 0.119), (0.0, 0.12)], seg=SEG, material=TOP, caps=(False, False)))
# magenta stripe around the cap band
# raised golden star on top, plus a ring of small stars
star = prism(star_pts(0.165, 0.072, 5), 0.105, 0.132, material=STAR)
cap_parts.append(bevel_obj(star, 0.006, 1, 40))
for k in range(5):
    a = math.pi / 2 + TAU * k / 5 + TAU / 10
    c = V(math.cos(a) * 0.225, math.sin(a) * 0.225, 0)
    s = prism(star_pts(0.03, 0.013, 5, phase=a), 0.1, 0.119, material=STAR)
    place(s, c)
    cap_parts.append(s)
cap = part(cap_parts, 'cap', (0, 0, 0), angle=40)
cap.location = (0, 0, CAPZ)
bpy.context.view_layer.update()

report()
notes = ('Parts/pivots (Blender coords, front -Y): base (origin 0,0,0; dark metal foot plate r=0.55 with bolts and small magenta lamps, '
         'chrome kicker skirt, column with the magenta neon ring of material "bumper_glow" at z=0.29, chrome lip); '
         f'cap (origin = its base centre (0,0,{CAPZ}); white domed cap with a gold star, top at z~0.56; squash/scale it). '
         'Materials: bumper_metal, chrome, bumper_glow, bumper_cap, cap_top, bumper_star.')
std_view()
finish('chars', 'bumper', kind='char', footprint=0.55, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['cap'].scale = (1.1, 1.1, 0.6)
    views('bumper', pose); montage('bumper')
