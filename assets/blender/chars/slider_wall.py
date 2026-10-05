import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *

# Haunted-house sliding wall panel. X -0.5..0.5 (game scales X to the wall length), Z -0.075..1.075, Y +-0.12.
BEAM = mat('wall_beam', '#3d2430', rough=0.75)
WOODA = mat('wall_wood', '#8a5a68', rough=0.8)
WOODB = mat('wall_wood2', '#74495c', rough=0.8)
IRON = mat('wall_iron', '#2e2d38', rough=0.45, metal=0.7)
GLOW = mat('glow_runes', '#c77dff', rough=0.4, emit='#b052ff', emit_strength=2.2)

X0, X1, Z0, Z1, T = -0.5, 0.5, -0.075, 1.075, 0.12
P = []
# heavy top and bottom beams
P.append(bx((X0 + 0.004, -T, Z0), (X1 - 0.004, T, 0.06), BEAM, 0.022))
P.append(bx((X0 + 0.004, -T, 0.94), (X1 - 0.004, T, Z1), BEAM, 0.022))
# horizontal planks (repeat nicely when stretched)
zs = [0.06, 0.2, 0.33, 0.44]          # lower panel
zs2 = [0.58, 0.69, 0.82, 0.94]        # upper panel
k = 0
for band in (zs, zs2):
    for za, zb in zip(band, band[1:]):
        d = 0.085 + 0.006 * ((k * 5) % 3)
        P.append(bx((X0 + 0.01, -d, za + 0.004), (X1 - 0.01, d, zb - 0.004), WOODA if k % 2 == 0 else WOODB, 0.016))
        k += 1
# rune channel: dark iron band across the middle
P.append(bx((X0 + 0.004, -0.1, 0.44), (X1 - 0.004, 0.1, 0.58), IRON, 0.012))
# glowing rune strip on both faces: two thin lines + a row of glyphs
for s in (-1, 1):
    y0, y1 = (0.1, 0.108) if s > 0 else (-0.108, -0.1)
    P.append(bx((X0 + 0.06, y0, 0.455), (X1 - 0.06, y1, 0.464), GLOW))
    P.append(bx((X0 + 0.06, y0, 0.556), (X1 - 0.06, y1, 0.565), GLOW))
    n = 7
    w = (X1 - X0 - 0.16) / n
    for i in range(n):
        cx = X0 + 0.08 + w * (i + 0.5)
        kind = i % 3
        P.append(bx((cx - 0.006, y0, 0.478), (cx + 0.006, y1, 0.542), GLOW))       # stem
        if kind == 0:   # arrow rune
            for dz in (0.0, 0.022):
                o = bx((-0.022, 0, -0.005), (0.022, y1 - y0, 0.005), GLOW)
                place(o, (cx + 0.014, y0, 0.53 - dz), (0, 35, 0)); P.append(o)
        elif kind == 1:  # cross-bar rune
            P.append(bx((cx - 0.026, y0, 0.505), (cx + 0.026, y1, 0.515), GLOW))
        else:            # forked rune
            for sg in (-1, 1):
                o = bx((-0.02, 0, -0.005), (0.02, y1 - y0, 0.005), GLOW)
                place(o, (cx + sg * 0.014, y0, 0.53), (0, -sg * 45, 0)); P.append(o)
# iron end straps wrapped round both ends, with corner brackets and rivets (round details only at the ends)
for sx in (-1, 1):
    xa, xb = (X1 - 0.07, X1 + 0.0) if sx > 0 else (X0, X0 + 0.07)
    P.append(bx((xa, -T - 0.008, Z0 + 0.02), (xb, T + 0.008, Z1 - 0.02), IRON, 0.01))
    for s in (-1, 1):
        for z in (0.03, 0.5, 1.0):
            P.append(cyl(r=0.016, h=0.014, verts=6, loc=((xa + xb) / 2, s * (T + 0.012), z), rot=(math.pi / 2, 0, 0), material=IRON))
        # L-bracket arms reaching inward along the beams
        y0, y1 = (T, T + 0.008) if s > 0 else (-T - 0.008, -T)
        for (za, zb) in ((Z0 + 0.03, 0.04), (0.96, Z1 - 0.03)):
            xi = (xa - 0.1, xa) if sx > 0 else (xb, xb + 0.1)
            P.append(bx((xi[0], y0, za), (xi[1], y1, zb), IRON, 0.003))
body = part(P, 'body', (0, 0, 0), angle=40)
report()
std_view()
notes = ('Haunted sliding wall panel. Part: body (origin (0,0,0) at the bottom centre). Spans X -0.5..0.5 (scale X to wall length), '
         'Z -0.075..1.075, thickness 0.24 centred on Y=0. Horizontal purple-brown planks between dark beams, iron rune channel '
         'with a glowing purple rune strip "glow_runes" on both faces (z 0.45..0.57), iron end straps with rivets.')
finish('chars', 'slider_wall', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('slider_wall'); montage('slider_wall', keys=('front', 'side', 'back', 'top'))
