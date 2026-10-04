import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

WOOD = mat('torch_wood', '#8a5530', rough=0.85)
IRON = mat('torch_iron', '#3b3a40', rough=0.45, metal=0.75)
STONE = mat('torch_stone', '#8d8a86', rough=0.95)
FLAME = mat('glow_flame', '#ff5a00', rough=0.6, emit='#ff6a10', emit_strength=0.9)
CORE = mat('glow_flame_core', '#ffc400', rough=0.6, emit='#ffd23a', emit_strength=0.9)

body = []
# --- stone footing: bevelled block with a chunky cap stone
body.append(box((0.42, 0.42, 0.14), loc=(0, 0, 0.07), material=STONE, bevel=0.025))
body.append(box((0.32, 0.32, 0.08), loc=(0, 0, 0.175), material=STONE, bevel=0.02))
# --- tapered octagonal wooden pole with slight facets
pole = lathe([(0.085, 0.2), (0.083, 0.6), (0.078, 1.1), (0.072, 1.5), (0.07, 1.62)], seg=8, material=WOOD, caps=(False, True),
             phase=math.pi / 8)
body.append(pole)
# iron collar at the foot + bands along the pole
body.append(lathe([(0.12, 0.21), (0.12, 0.26), (0.1, 0.29), (0.088, 0.3)], seg=12, material=IRON, caps=(True, False)))
for z, r in ((0.75, 0.09), (1.2, 0.084)):
    body.append(cyl(r=r, h=0.05, verts=10, loc=(0, 0, z), material=IRON))
    for k in range(4):   # rivets
        a = TAU * k / 4 + math.pi / 4
        body.append(ell((math.cos(a) * r, math.sin(a) * r, z), (0.012, 0.012, 0.012), seg=6, rings=3, material=IRON))
# rope wrap (grip) between the bands
pts = [V(math.cos(t * 0.9) * 0.086, math.sin(t * 0.9) * 0.086, 0.88 + t * 0.012) for t in range(0, 22)]
body.append(tube(pts, 0.014, seg=5, material=WOOD))
# --- iron bracket: top collar + four curved straps holding the bowl
body.append(lathe([(0.088, 1.56), (0.1, 1.58), (0.1, 1.66), (0.06, 1.7)], seg=10, material=IRON, caps=(False, True)))
for k in range(4):
    a = TAU * k / 4 + math.pi / 4
    d = V(math.cos(a), math.sin(a), 0)
    p = bezier(V(0, 0, 1.6) + d * 0.08, V(0, 0, 1.62) + d * 0.2, V(0, 0, 1.72) + d * 0.22, V(0, 0, 1.86) + d * 0.2, n=6)
    body.append(tube(p, [0.022, 0.02, 0.019, 0.018, 0.018, 0.019, 0.022], seg=5, flat=0.55, material=IRON))
    # curl at the end of each strap
    o = torus(R=0.03, r=0.011, seg=8, ring=4, material=IRON)
    xf(o, Matrix.Translation(V(0, 0, 1.9) + d * 0.225) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(math.pi / 2, 4, 'X'))
    body.append(o)
# bowl (brazier cup) with rolled rim and little spikes
body.append(lathe([(0.0, 1.66), (0.06, 1.665), (0.12, 1.7), (0.17, 1.76), (0.2, 1.83), (0.205, 1.86), (0.18, 1.85),
                   (0.0, 1.84)], seg=14, material=IRON))
rim = torus(R=0.205, r=0.022, seg=14, ring=5, material=IRON); place(rim, (0, 0, 1.865)); body.append(rim)
for k in range(7):
    a = TAU * k / 7
    body.append(cone(r=0.022, h=0.08, verts=5, loc=(math.cos(a) * 0.205, math.sin(a) * 0.205, 1.92), material=IRON))
# finial under the bowl
body.append(cone(r=0.05, h=0.1, verts=8, loc=(0, 0, 1.63), rot=(math.pi, 0, 0), material=IRON))
# coals / embers in the bowl
import random as _r
rr = _r.Random(3)
for k in range(9):
    a = TAU * k / 9 + rr.uniform(-0.2, 0.2); d = 0.11 if k % 2 else 0.06
    body.append(ico(r=0.05, sub=1, loc=(math.cos(a) * d, math.sin(a) * d, 1.865), material=IRON if k % 3 else CORE,
                    scale=(1, 1, 0.75), jitter=0.01, seed=k))
bodyo = part(body, 'body', (0, 0, 0), angle=45)

# ---------------------------------------------------------------- flame (origin at its base)
FB = V(0, 0, 1.86)
fl = []
# big central tongue, curling slightly
fl.append(tongue(FB + V(0, 0, -0.02), FB + V(0.05, 0, 0.18), FB + V(-0.07, 0.01, 0.34), FB + V(0.04, -0.01, 0.52), 0.17,
                 seg=10, n=7, material=FLAME, prof=[0.75, 1.0, 0.95, 0.78, 0.55, 0.33, 0.15, 0.05]))
# side tongues
for k, (a, h, r) in enumerate(((0.3, 0.36, 0.1), (1.6, 0.27, 0.085), (2.6, 0.32, 0.095), (4.0, 0.34, 0.095), (5.2, 0.28, 0.085))):
    d = V(math.cos(a), math.sin(a), 0)
    fl.append(tongue(FB + d * 0.06, FB + d * 0.11 + V(0, 0, h * 0.35), FB + d * 0.09 + V(0, 0, h * 0.7),
                     FB + d * 0.16 + V(0, 0, h), r, seg=7, n=5, material=FLAME))
# yellow core
fl.append(tongue(FB + V(0, -0.05, 0.0), FB + V(0.02, -0.1, 0.1), FB + V(-0.03, -0.1, 0.22), FB + V(0.0, -0.09, 0.36), 0.1,
                 seg=8, n=5, material=CORE, prof=[0.8, 1.0, 0.9, 0.65, 0.35, 0.1]))
for a in (-1.0, -2.3, 0.9, 2.5):
    d = V(math.cos(a), math.sin(a), 0) * 1.6
    fl.append(tongue(FB + d * 0.05 + V(0, 0, 0.0), FB + d * 0.08 + V(0, 0, 0.07), FB + d * 0.06 + V(0, 0, 0.13),
                     FB + d * 0.09 + V(0, 0, 0.19), 0.05, seg=6, n=4, material=CORE))
flame = part(fl, 'flame', FB, angle=80)

report()
notes = ('Parts/pivots (Blender coords, front -Y): body (origin 0,0,0; stone footing, tapered wooden pole with iron bands and '
         'rope grip, iron bracket straps, brazier bowl with spikes and coals, rim at z~1.87); '
         f'flame (origin at its base ({FB.x:.2f},{FB.y:.2f},{FB.z:.2f}); layered stylised flame, top at z~2.4, outer material '
         '"glow_flame" (orange), inner core "glow_flame_core" (yellow); flicker its scale). '
         'Materials: torch_wood, torch_iron, torch_stone, glow_flame, glow_flame_core.')
std_view()
finish('chars', 'torch', kind='char', footprint=0.3, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['flame'].scale = (0.9, 0.9, 1.25)
    views('torch', pose); montage('torch')
