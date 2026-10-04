import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *
from ship_kit import *

HULL = mat('hull_wood', '#8a4f2a', rough=0.65)
DECK = mat('deck_wood', '#d6a463', rough=0.7)
SAIL = mat('sail', '#fbf3e2', rough=0.8)
RED = mat('ship_red', '#d8342c', rough=0.55)
IRON = mat('iron', '#2a2a33', rough=0.4, metal=0.5)
GOLD = mat('gold', '#f2b632', rough=0.3, metal=0.8)

bp = []
hull = hull_mesh(HULL)
bpy.context.view_layer.update()
iso_paint(hull, lambda p: (p.z - 0.1) * 10, RED)                      # red bottom stripe at the waterline
iso_paint(hull, lambda p: (deck(p.y) - 0.07 - p.z) * 10, DECK)       # deck planks on top
bp.append(hull)
bpy.context.view_layer.update()

# side strakes (plank lines) + portholes
for sx in (-1, 1):
    for z, mm, rr in ((0.3, DECK, 0.03), (0.56, HULL, 0.035)):
        pts = []
        for y in [-2.45, -2.2, -1.8, -1.2, -0.5, 0.3, 1.1, 1.8, 2.36]:
            p, n = ring_on(hull, y, z + 0.05 * ((y + 0.1) / 2.5) ** 2, sx, push=0.005)
            if p is not None:
                pts.append(p)
        bp.append(tube(pts, rr, seg=5, material=DECK, round_end=True))
    for y in (-1.3, -0.4, 0.5):
        p, n = ring_on(hull, y, 0.43, sx, push=0.0)
        M = orient(p, n)
        bp.append(xf(torus(0.13, 0.035, seg=12, ring=5, material=GOLD), M))
        bp.append(xf(ell((0, 0, 0), (0.11, 0.11, 0.025), seg=10, rings=4, material=IRON), M))
        bp.append(xf(ell((0.04, 0.04, 0.03), (0.03, 0.03, 0.006), seg=6, rings=3, material=SAIL), M))
    # cannons poking out above the strake
    for y in (-1.75, 0.95):
        x0 = sx * (beam(y) - 0.35)
        p = V(x0, y, top_at(hull, x0, y).z + 0.13)
        d = V(sx, 0, 0.05).normalized()
        bp.append(tube([p, p + d * 0.45, p + d * 0.55], [0.1, 0.085, 0.1], seg=8, material=IRON, round_end=False))
        bp.append(xf(torus(0.1, 0.03, seg=8, ring=4, material=IRON), Matrix.Translation(p + d * 0.53) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()))

# rounded bulwark around the deck + light cap rail
loop = []
ys_side = [2.3, 1.8, 1.2, 0.5, -0.3, -1.1, -1.7, -2.15, -2.45]
for sx in (-1, 1):
    seq = ys_side if sx == -1 else ys_side[::-1]
    for y in seq:
        x = sx * (beam(y) - 0.07)
        t = top_at(hull, x, y)
        loop.append(V(x, y, t.z + 0.12))
    if sx == -1:
        loop.append(V(0, -2.62, deck(-2.62) + 0.14))
loop.append(loop[0].copy())
bp.append(tube(loop, 0.2, seg=8, material=HULL, flat=0.3, flat_n=False, cap=False))
bp.append(tube([p + V(0, 0, 0.19) for p in loop], 0.055, seg=6, material=DECK, cap=False))

# aft cabin (quarterdeck)
CY0, CY1 = 1.05, 2.3
cab_w = beam(1.6) - 0.22
ctop = deck(CY1) + 0.72
cab = box((cab_w * 2, CY1 - CY0, ctop - 0.5), loc=(0, (CY0 + CY1) / 2, (ctop + 0.5) / 2), material=HULL, bevel=0.06)
bp.append(cab)
roof = box((cab_w * 2 + 0.2, CY1 - CY0 + 0.25, 0.12), loc=(0, (CY0 + CY1) / 2 + 0.05, ctop + 0.06), material=DECK, bevel=0.04)
bp.append(roof)
# door + windows on the cabin front (faces -Y)
fy = CY0 - 0.005
bp.append(box((0.42, 0.06, 0.62), loc=(0, fy, deck(CY0) + 0.33), material=RED, bevel=0.03))
bp.append(ell((0.12, fy - 0.04, deck(CY0) + 0.33), (0.035, 0.03, 0.035), seg=6, rings=4, material=GOLD))
for sx in (-1, 1):
    wc = V(sx * 0.55, fy - 0.01, deck(CY0) + 0.42)
    bp.append(box((0.28, 0.05, 0.28), loc=wc, material=GOLD, bevel=0.02))
    bp.append(box((0.2, 0.05, 0.2), loc=wc + V(0, -0.015, 0), material=IRON))
# stern windows on the transom (faces +Y)
for sx in (-1, 0, 1):
    wc = V(sx * 0.42, CY1 + 0.02, ctop - 0.32)
    bp.append(box((0.26, 0.05, 0.3), loc=wc, material=GOLD, bevel=0.02))
    bp.append(box((0.18, 0.05, 0.22), loc=wc + V(0, 0.015, 0), material=IRON))
# little railing on the quarterdeck: posts + rail
rail = [V(-cab_w - 0.05, CY0 - 0.02, ctop + 0.4), V(-cab_w - 0.05, CY1 + 0.12, ctop + 0.4), V(cab_w + 0.05, CY1 + 0.12, ctop + 0.4),
        V(cab_w + 0.05, CY0 - 0.02, ctop + 0.4)]
bp.append(tube(rail, 0.045, seg=6, material=DECK, round_end=True))
for a, b in zip(rail, rail[1:]):
    n = max(2, int((b - a).length / 0.32))
    for k in range(n + 1):
        q = a.lerp(b, k / n)
        bp.append(cyl(0.03, 0.34, loc=(q.x, q.y, ctop + 0.23), verts=6, material=DECK))
# stern lantern
lp = V(0, CY1 + 0.12, ctop + 0.45)
bp.append(cyl(0.035, 0.35, loc=lp + V(0, 0, 0.17), verts=6, material=IRON))
bp.append(box((0.18, 0.18, 0.22), loc=lp + V(0, 0, 0.42), material=GOLD, bevel=0.03))
bp.append(cone(0.15, 0.12, loc=lp + V(0, 0, 0.59), verts=4, rot=(0, 0, math.pi / 4), material=RED))
# steering wheel on a post, facing -Y
wc = V(0, CY0 + 0.25, ctop + 0.52)
bp.append(cyl(0.06, 0.4, loc=(0, wc.y + 0.06, ctop + 0.25), verts=6, material=HULL))
WM = Matrix.Translation(wc) @ rotm((90, 0, 0))
bp.append(xf(torus(0.22, 0.03, seg=14, ring=5, material=DECK), WM))
for k in range(6):
    a = TAU * k / 6
    d = V(math.cos(a), 0, math.sin(a))
    bp.append(tube([wc, wc + d * 0.31], [0.022, 0.02], seg=5, material=DECK, round_end=True))
bp.append(ell(wc, (0.05, 0.05, 0.05), seg=6, rings=4, material=GOLD))

# bowsprit + gold figurehead star + anchor
b0 = V(0, -2.45, deck(-2.45) + 0.12)
b1 = V(0, -3.45, deck(-2.45) + 0.62)
bp.append(tube([b0, b1], [0.1, 0.055], seg=8, material=DECK, round_end=True))
bp.append(tube([b1 + V(0, 0.15, -0.07), b1 + V(0, 0.15, -0.3), b0 + V(0, -0.2, -0.55)], [0.012, 0.012, 0.012], seg=4, material=IRON))
st = V(0, -2.72, deck(-2.6) - 0.1)
bp.append(xf(prism(star_pts(0.17, 0.08, 5), -0.04, 0.04, material=GOLD), Matrix.Translation(st) @ rotm((90, 0, 0))))
ap = V(-0.72, -1.95, 0.55)
p, n = ring_on(hull, -1.95, 0.5, -1, push=0.05)
bp.append(tube([p + V(0, 0, 0.18), p + V(0, 0, -0.24)], 0.03, seg=5, material=IRON))
bp.append(tube(bezier(p + V(0, -0.17, -0.12), p + V(0, -0.1, -0.3), p + V(0, 0.1, -0.3), p + V(0, 0.17, -0.12), n=5), 0.025, seg=5, material=IRON, round_end=True))
bp.append(xf(torus(0.06, 0.018, seg=8, ring=4, material=IRON), Matrix.Translation(p + V(0, 0, 0.24)) @ rotm((0, 90, 0))))
# barrels on deck
for (x, y) in ((0.55, -1.0), (0.32, -1.25)):
    z = deck(y) - 0.02
    bp.append(lathe([(0.0, z), (0.15, z), (0.19, z + 0.17), (0.15, z + 0.34), (0, z + 0.34)], seg=10, material=HULL))
    bp.append(xf(torus(0.18, 0.018, seg=10, ring=4, material=IRON), Matrix.Translation(V(x, y, z + 0.09))))
    bp.append(xf(torus(0.18, 0.018, seg=10, ring=4, material=IRON), Matrix.Translation(V(x, y, z + 0.25))))
    bp[-5].data.transform(Matrix.Translation(V(x, y, 0))); bp[-5].data.update()
body = part(bp, 'body', (0, 0, 0), angle=50)

# ---------------------------------------------------------------- sail part (mast + yards + sail + crow's nest)
MB = V(0, MAST_Y, deck(MAST_Y) - 0.02)
TOP = 4.55
sp = []
sp.append(tube([MB, V(0, MAST_Y, TOP)], [0.13, 0.085], seg=10, material=HULL))
YT, YB = 3.85, 1.85
for z, w in ((YT, 1.45), (YB, 1.62)):
    sp.append(tube([V(-w, MAST_Y - 0.12, z), V(w, MAST_Y - 0.12, z)], [0.055, 0.055], seg=6, material=HULL, round_end=True))
    for sx in (-1, 1):
        sp.append(ell((sx * w, MAST_Y - 0.12, z), (0.06, 0.06, 0.06), seg=6, rings=4, material=GOLD))
sail, border, left, right = sail_grid(2.7, 3.05, YB + 0.05, YT - 0.03, MAST_Y - 0.18, 0.5, nu=10, nv=7, material=SAIL)
iso_paint(sail, lambda p: math.sin(p.x * math.pi / 0.62) * 3, RED)
sp.append(sail)
# red circle emblem with a little white anchor feel: simple roundel
em_c = V(0, MAST_Y - 0.18 - 0.5 * (1 - 0.0) * (1 - 0.0) - 0.03, (YB + YT) / 2 + 0.05)
sp.append(xf(ell((0, 0, 0), (0.42, 0.42, 0.02), seg=16, rings=4, material=SAIL), Matrix.Translation(em_c) @ rotm((90, 0, 0))))
sp.append(xf(torus(0.42, 0.04, seg=16, ring=4, material=RED), Matrix.Translation(em_c + V(0, -0.01, 0)) @ rotm((90, 0, 0))))
sp.append(xf(prism(star_pts(0.3, 0.13, 5), -0.02, 0.02, material=RED), Matrix.Translation(em_c + V(0, -0.02, 0)) @ rotm((90, 0, 0))))
# crow's nest
cz = 4.08
sp.append(lathe([(0.0, cz), (0.3, cz), (0.36, cz + 0.28), (0.3, cz + 0.28), (0.26, cz + 0.06), (0, cz + 0.06)], seg=12, material=HULL,
                M=Matrix.Translation(V(0, MAST_Y, 0))))
sp.append(xf(torus(0.35, 0.03, seg=12, ring=4, material=GOLD), Matrix.Translation(V(0, MAST_Y, cz + 0.28))))
sp.append(ell((0, MAST_Y, TOP + 0.05), (0.08, 0.08, 0.08), seg=8, rings=5, material=GOLD))
# lift ropes from the mast top to the yard tips
for z, w in ((YT, 1.45), (YB, 1.62)):
    for sx in (-1, 1):
        sp.append(tube([V(0, MAST_Y, TOP - 0.1), V(sx * w * 0.97, MAST_Y - 0.12, z + 0.03)], 0.012, seg=4, material=IRON, cap=False))
sail_o = part(sp, 'sail', MB, angle=50)

# ---------------------------------------------------------------- flag (pivot at the pole attachment)
FP = V(0, MAST_Y + 0.08, TOP - 0.12)
fl = flag_mesh(0.8, 0.45, 0, MAST_Y + 0.08, TOP - 0.55, RED, notch=True)
flag_o = part([fl], 'flag', FP, angle=50)

report()
views('ship_water')
montage('ship_water')
finish('chars', 'ship_water', kind='char', footprint=1.6, grounded=False,
       notes=f'origin at waterline centre (0,0,0), bow -Y, keel to z=-0.55. parts: body (pivot 0,0,0); sail = mast+yards+sail+crow nest, '
             f'pivot at mast base ({MB.x:.2f},{MB.y:.2f},{MB.z:.2f}); flag pivot at its pole attachment ({FP.x:.2f},{FP.y:.2f},{FP.z:.2f}) '
             f'(top level, flies toward +Y)')
