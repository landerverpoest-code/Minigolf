import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from b6kit import *

# Volcano gong: obsidian frame (body, origin ground centre) + swinging bronze disc (disc, origin = hanging pivot).
OBS = mat('obsidian', '#2b2236', rough=0.22, metal=0.2)
OBS2 = mat('obsidian_trim', '#4b3b5e', rough=0.35, metal=0.2)
LAVA = mat('glow_lava', '#ff7a1c', rough=0.5, emit='#ff5a00', emit_strength=3.0)
BRONZE = mat('gong_bronze', '#f0b040', rough=0.32, metal=0.7)
COPPER = mat('gong_copper', '#a8452a', rough=0.35, metal=0.75)
CORD = mat('gong_cord', '#c22a2e', rough=0.75)

rnd = random.Random(7)
PY = 0.15                     # frame/disc plane (Blender +Y)
H = 0.09                      # half post thickness
P = []

# ------------------------------------------------------------------ posts
for sx in (-1, 1):
    x = sx * 0.75
    P.append(bx((x - H, PY - H, 0.0), (x + H, PY + H, 2.0), OBS, 0.018))                    # square post
    P.append(bx((x - 0.12, PY - 0.12, 0.0), (x + 0.12, PY + 0.12, 0.16), OBS2, 0.022))      # plinth
    P.append(bx((x - 0.105, PY - 0.105, 1.66), (x + 0.105, PY + 0.105, 1.72), OBS2, 0.01))  # collar under the crossbar
    # spiked cap: slab + pyramid spike + four little corner horns
    P.append(bx((x - 0.13, PY - 0.13, 2.0), (x + 0.13, PY + 0.13, 2.075), OBS2, 0.018))
    P.append(lathe([(0.105, 2.07), (0.06, 2.17), (0.0, 2.3)], seg=4, material=OBS, phase=TAU / 8, smooth=False,
                   M=Matrix.Translation((x, PY, 0))))
    for cx in (-1, 1):
        for cy in (-1, 1):
            d = Vector((cx, cy, 0)).normalized()
            base = Vector((x + cx * 0.088, PY + cy * 0.088, 2.07))
            tip = base + d * 0.045 + Vector((0, 0, 0.1))
            P.append(tube([base, base.lerp(tip, 0.5), tip], [0.03, 0.02, 0.002], seg=4, material=OBS, smooth=False))
    # glowing lava cracks on all four faces
    faces = [((x, PY - H, 0), (1, 0, 0), (0, -1, 0)), ((x, PY + H, 0), (-1, 0, 0), (0, 1, 0)),
             ((x + H, PY, 0), (0, 1, 0), (1, 0, 0)), ((x - H, PY, 0), (0, -1, 0), (-1, 0, 0))]
    for fi, (c, u, n) in enumerate(faces):
        c, u, n = Vector(c), Vector(u), Vector(n)
        segs = [(0.2, 1.05), (1.05, 1.64)] if fi > 0 else [(0.2, 0.62), (1.02, 1.64)]   # front leaves room for the glyph
        for (v0, v1) in segs:
            for path in crack_paths(rnd, -0.06, 0.06, v0, v1, n_main=1, steps=6, branch=0.45):
                pts = [c + u * pu + Vector((0, 0, pv)) for (pu, pv) in path]
                P.append(ribbon(pts, 0.022, n, LAVA))
    # fire glyph on the front face: dark diamond plaque, glowing flame, dark inner flame
    gz = 0.82
    plq = relief([(0, -0.14), (0.075, 0), (0, 0.14), (-0.075, 0)], 0, 0.012, OBS2)
    place(plq, (x, PY - H, gz), (90, 0, 0)); P.append(plq)
    FL = [(0.00, -0.50), (0.22, -0.45), (0.36, -0.30), (0.40, -0.10), (0.33, 0.10), (0.30, 0.32), (0.18, 0.15), (0.10, 0.30),
          (0.02, 0.50), (-0.08, 0.30), (-0.16, 0.42), (-0.24, 0.18), (-0.36, 0.05), (-0.40, -0.12), (-0.35, -0.32), (-0.20, -0.46)]
    g = relief([(a * 0.15, b * 0.17) for a, b in FL], 0, 0.02, LAVA); place(g, (x, PY - H, gz), (90, 0, 0)); P.append(g)
    gi = relief([(a * 0.07, b * 0.08 - 0.02) for a, b in FL], 0, 0.026, OBS); place(gi, (x, PY - H, gz), (90, 0, 0)); P.append(gi)

# ------------------------------------------------------------------ crossbar
P.append(bx((-0.88, PY - 0.1, 1.84), (0.88, PY + 0.1, 2.0), OBS, 0.02))
P.append(bx((-0.66, PY - 0.105, 1.86), (0.66, PY + 0.105, 1.875), OBS2))                 # thin trim lines
P.append(bx((-0.66, PY - 0.105, 1.965), (0.66, PY + 0.105, 1.98), OBS2))
# crack along the crossbar front + back
for n in ((0, -1, 0), (0, 1, 0)):
    yy = PY + 0.1 * n[1]
    pts = []
    for i in range(11):
        xx = -0.6 + 1.2 * i / 10
        pts.append((xx, yy, 1.92 + rnd.uniform(-0.022, 0.022)))
    P.append(ribbon(pts, [0.018 * (1 - abs(i - 5) / 7) for i in range(11)], n, LAVA))
# central sun/fire glyph on the crossbar front
sp = relief(poly_pts(0.075, 12), 0, 0.012, OBS2); place(sp, (0, PY - 0.1, 1.92), (90, 0, 0)); P.append(sp)
P.append(place(relief(star_pts(0.07, 0.035, 8), 0, 0.02, LAVA), (0, PY - 0.1, 1.92), (90, 0, 0)))
P.append(place(relief(poly_pts(0.026, 10), 0, 0.028, OBS), (0, PY - 0.1, 1.92), (90, 0, 0)))
# small fire glyphs between the cord hooks and the posts
for sx in (-1, 1):
    g = relief([(a * 0.09, b * 0.1) for a, b in FL], 0, 0.016, LAVA); place(g, (sx * 0.47, PY - 0.1, 1.92), (90, 0, 0)); P.append(g)
# copper hooks under the crossbar where the cords hang
for sx in (-1, 1):
    P.append(lathe([(0.04, 1.835), (0.04, 1.845), (0.0, 1.845)], seg=8, material=COPPER, caps=(True, False)))
    xf(P[-1], Matrix.Translation((sx * 0.25, PY, 0)))
    P.append(torus(R=0.032, r=0.009, loc=(sx * 0.25, PY, 1.81), rot=(0, math.pi / 2, 0), seg=8, ring=4, material=COPPER))

body = part(P, 'body', (0, 0, 0), angle=35)

# ------------------------------------------------------------------ disc (pivot at (0, PY, 1.5))
DC = Vector((0, PY, 0.65))
M = Matrix.Translation(DC) @ rotm((90, 0, 0))        # local +Z -> world -Y (front), local Y -> world Z
D = []
R0 = 0.55
prof = [(0.0, -0.032), (0.5, -0.03), (0.535, -0.028), (0.55, -0.012), (0.55, 0.012), (0.535, 0.028), (0.505, 0.03)]
# front face: concentric hammered ridges (raised rings)
for rc in (0.43, 0.33, 0.235):
    prof += [(rc + 0.013, 0.03), (rc, 0.039), (rc - 0.013, 0.03)]
prof += [(0.13, 0.03), (0.105, 0.052), (0.065, 0.071), (0.0, 0.079)]
plate = lathe(prof, seg=24, material=BRONZE, M=M)
D.append(plate)
# copper flame/sun emblem around the boss: 8 curved flame rays
for k in range(8):
    a = TAU * k / 8 + TAU / 16
    ray = [(0.0, -0.04), (0.08, -0.04), (0.15, -0.012), (0.215, 0.045), (0.13, 0.016), (0.07, 0.03), (0.0, 0.04)]   # curved flame tongue (radial, tangential)
    ray = [(0.155 + p[0], p[1]) for p in ray]
    pts = [(rr * math.cos(a) - tt * math.sin(a), rr * math.sin(a) + tt * math.cos(a)) for rr, tt in ray]
    D.append(xf(relief(pts, 0.03, 0.041, COPPER), M))
# lugs on the rim where the cords attach + cords up to the crossbar + tassels
for sx in (-1, 1):
    xx = sx * 0.25
    zr = DC.z + math.sqrt(R0 ** 2 - xx ** 2)
    D.append(torus(R=0.03, r=0.011, loc=(xx, PY, zr + 0.005), rot=(0, math.pi / 2, 0), seg=8, ring=4, material=COPPER))
    pts = [Vector((xx, PY, zr + 0.03)), Vector((xx, PY, 1.5)), Vector((xx, PY, 1.81))]
    D.append(tube(pts, [0.013, 0.012, 0.012], seg=5, material=CORD))
    D.append(ell((xx, PY, zr + 0.035), (0.022, 0.022, 0.026), seg=8, rings=5, material=CORD))       # knot
    # tassel hanging in front of the lug
    t0 = Vector((xx + sx * 0.03, PY - 0.035, zr + 0.02))
    D.append(tube([t0, t0 + Vector((sx * 0.015, -0.01, -0.06))], [0.006, 0.006], seg=5, material=CORD))
    D.append(lathe([(0.0, -0.17), (0.03, -0.14), (0.022, -0.08), (0.012, -0.07), (0.0, -0.065)], seg=6, material=CORD,
                   M=Matrix.Translation(t0 + Vector((sx * 0.015, -0.01, 0.0)))))
    D.append(ell(t0 + Vector((sx * 0.015, -0.01, -0.068)), (0.016, 0.016, 0.012), seg=8, rings=4, material=COPPER))
disc = part(D, 'disc', (0, PY, 1.5), angle=60)

report(); print_ext()
std_view()
notes = ('Volcano gong. Parts: body = obsidian frame, origin ground centre (0,0,0): two square posts 0.18 thick at x=+-0.75, '
         'y=+0.15, z 0..2.0 with glow_lava cracks, plinths (0.24 sq, z 0..0.2), spiked caps to z 2.3, crossbar x -0.88..0.88, '
         'z 1.84..2.0, y 0.05..0.25, fire glyphs (glow_lava) and copper cord hooks at x=+-0.25 under the crossbar. '
         'disc = gong plate + cords, origin = hanging pivot (0,0.15,1.5) (swing around Blender X = three.js x): bronze disc '
         'r 0.55, plate thickness 0.06 centred at (0,0.15,0.65) in the XZ plane facing -Y, hammered concentric rings, '
         'raised boss (front to y 0.071), copper sun/flame emblem, red cords from the rim lugs up to the hooks at x=+-0.25 '
         '(z 1.81), small tassels. Glow material on the plate: gong_bronze.')
finish('chars', 'gong', kind='char', footprint=0.9, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('gong'); montage('gong', keys=('front', 'side', 'back', 'top'))
