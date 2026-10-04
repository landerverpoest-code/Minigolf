import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from bkit import *

IRON = mat('lantern_iron', '#34333f', rough=0.45, metal=0.7)
GLASS = mat('lantern_glass', '#8fe8b0', rough=0.1, emit='#5dff8a', emit_strength=0.18, alpha=0.32)
FLAME = mat('glow_flame', '#7dff9a', rough=0.5, emit='#9dffb0', emit_strength=1.0)
WAX = mat('wax', '#efe6d2', rough=0.6)
STONE = mat('lantern_stone', '#6f6a74', rough=0.95)

# ---------------------------------------------------------------- body: post + crook arm
b = []
b.append(box((0.46, 0.46, 0.1), loc=(0, 0, 0.05), material=STONE, bevel=0.03))
b.append(lathe([(0.2, 0.1), (0.2, 0.15), (0.17, 0.18), (0.155, 0.25), (0.12, 0.29), (0.095, 0.38), (0.07, 0.42)],
               seg=12, material=IRON, caps=(True, False)))
b.append(lathe([(0.062, 0.4), (0.058, 1.0), (0.054, 1.6), (0.052, 1.84)], seg=8, material=IRON, caps=(False, False),
               phase=math.pi / 8))
for z in (0.95, 1.55):
    b.append(lathe([(0.06, z - 0.04), (0.08, z - 0.02), (0.08, z + 0.02), (0.06, z + 0.04)], seg=10, material=IRON,
                   caps=(False, False)))
b.append(lathe([(0.052, 1.83), (0.08, 1.86), (0.085, 1.9), (0.06, 1.93), (0.04, 1.95)], seg=10, material=IRON, caps=(False, True)))
b.append(sphere(r=0.045, loc=(0, 0, 1.99), seg=10, rings=6, material=IRON))
b.append(cone(r=0.022, h=0.1, verts=6, loc=(0, 0, 2.07), material=IRON))
HX = 0.52
H = V(HX, 0, 1.83)   # hanging point (cage pivot)
arm = bezier(V(0.02, 0, 1.8), V(0.2, 0, 1.99), V(0.44, 0, 2.0), V(HX, 0, 1.92), n=8)
b.append(tube(arm, [0.03, 0.028, 0.026, 0.024, 0.023, 0.022, 0.022, 0.022, 0.022], seg=6, material=IRON))
b.append(sphere(r=0.03, loc=(HX + 0.01, 0, 1.935), seg=8, rings=5, material=IRON))
# hook
b.append(tube([V(HX, 0, 1.92), V(HX, 0, 1.87), V(HX, 0, 1.845)], 0.011, seg=5, material=IRON))
# decorative scroll under the arm (spiral)
sp = []
c = V(0.2, 0, 1.8)
for i in range(18):
    t = i / 17
    a = math.pi * 1.0 + t * TAU * 1.2
    r = 0.14 * (1 - t * 0.8)
    sp.append(c + V(math.cos(a) * r, 0, math.sin(a) * r))
sp = [V(0.05, 0, 1.62), V(0.058, 0, 1.75)] + sp
b.append(tube(sp, [0.017] * len(sp), seg=5, material=IRON))
body = part(b, 'body', (0, 0, 0), angle=45)

# ---------------------------------------------------------------- cage (pivot = hanging point H)
cg = []
top_ring = torus(R=0.03, r=0.009, seg=10, ring=4, material=IRON)
xf(top_ring, Matrix.Translation(H + V(0, 0, -0.025)) @ Matrix.Rotation(math.pi / 2, 4, 'X'))
cg.append(top_ring)
CW = 0.17                 # half width of the cage
ZT, ZB = 1.65, 1.29       # top frame / bottom tray
# roof: flared 4-sided pyramid with a lip
roof = lathe([(CW + 0.05, ZT + 0.02), (CW + 0.055, ZT + 0.04), (CW - 0.01, ZT + 0.08), (0.05, ZT + 0.13), (0.025, ZT + 0.15),
              (0.0, ZT + 0.16)], seg=4, material=IRON, caps=(True, False), phase=math.pi / 4)
xf(roof, Matrix.Translation((HX, 0, 0)) @ Matrix.Diagonal((1.41, 1.41, 1, 1)))
cg.append(roof)
cg.append(tube([H + V(0, 0, -0.05), V(HX, 0, ZT + 0.15)], 0.012, seg=5, material=IRON))
# frames
for z, hgt in ((ZT, 0.03), (ZB, 0.04)):
    cg.append(box((2 * CW + 0.03, 2 * CW + 0.03, hgt), loc=(HX, 0, z), material=IRON, bevel=0.006))
for sx in (-1, 1):
    for sy in (-1, 1):
        cg.append(box((0.03, 0.03, ZT - ZB), loc=(HX + sx * CW, sy * CW, (ZT + ZB) / 2), material=IRON))
# glass panes + a thin cross bar on each
for k in range(4):
    a = TAU * k / 4
    d = V(math.cos(a), math.sin(a), 0); t = V(-math.sin(a), math.cos(a), 0)
    pane = box((0.012, 2 * CW - 0.02, ZT - ZB - 0.03), loc=(0, 0, 0), material=GLASS)
    place(pane, V(HX, 0, (ZT + ZB) / 2) + d * (CW - 0.004), (0, 0, math.degrees(a)))
    cg.append(pane)
    bar = box((0.016, 0.016, ZT - ZB), loc=(0, 0, 0), material=IRON)
    place(bar, V(HX, 0, (ZT + ZB) / 2) + d * (CW + 0.004), (0, 0, math.degrees(a)))
    cg.append(bar)
# bottom finial
cg.append(lathe([(0.07, ZB - 0.02), (0.05, ZB - 0.05), (0.02, ZB - 0.09), (0.0, ZB - 0.13)], seg=8, material=IRON,
                caps=(True, False), M=Matrix.Translation((HX, 0, 0))))
# candle with drips on the tray
cg.append(cyl(r=0.042, h=0.11, verts=10, loc=(HX, 0, ZB + 0.075), material=WAX))
for k in range(3):
    a = TAU * k / 3 + 0.4
    cg.append(ell((HX + math.cos(a) * 0.04, math.sin(a) * 0.04, ZB + 0.1), (0.014, 0.014, 0.03), seg=6, rings=4, material=WAX))
cg.append(tube([V(HX, 0, ZB + 0.13), V(HX, 0, ZB + 0.15)], 0.004, seg=4, material=IRON))   # wick
cage = part(cg, 'cage', H, angle=45)

# ---------------------------------------------------------------- flame (inside the cage, parented to it)
FB = V(HX, 0, ZB + 0.135)
fl = [tongue(FB, FB + V(0.0, 0, 0.04), FB + V(0.012, 0, 0.09), FB + V(-0.005, 0, 0.15), 0.04, seg=8, n=5, material=FLAME,
             prof=[0.7, 1.0, 0.9, 0.6, 0.3, 0.08])]
flame = part(fl, 'flame', FB, angle=80)
parent_keep(flame, cage)

report()
notes = ('Parts/pivots (Blender coords, front -Y): body (origin 0,0,0; stone foot, iron post ~2.1 m with collars and finial, '
         f'crook arm to +X with a scroll, hook at x={HX}); cage (pivot = hanging point ({H.x:.2f},{H.y:.2f},{H.z:.2f}); '
         'square iron lantern with roof, 4 glass panes of material "lantern_glass", candle; swing it about its local axes); '
         f'flame (origin at its base ({FB.x:.2f},{FB.y:.2f},{FB.z:.3f}) world, PARENTED to cage (local offset '
         f'({FB.x - H.x:.2f},0,{FB.z - H.z:.3f})); material "glow_flame", ghostly green). '
         'Materials: lantern_iron, lantern_glass, glow_flame, wax, lantern_stone.')
std_view()
finish('chars', 'lantern', kind='char', footprint=0.3, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['cage'].rotation_euler = (0, 0.35, 0)
    views('lantern', pose); montage('lantern')
