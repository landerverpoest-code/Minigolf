import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *
from okit import _obj

# ONE windmill sail (the game makes 4 copies rotated around the Y axis). Origin = axle centre (0,0,0), sail hangs DOWN (-Z),
# lattice on the +X side of the spar, faces -Y (front).
SPAR = mat('sail_wood', '#6b4226', rough=0.75)
FRAME = mat('sail_frame', '#a8743f', rough=0.7)
CLOTH = mat('sail_cloth', '#f7e7c6', rough=0.95)
IRON = mat('sail_iron', '#3b3532', rough=0.45, metal=0.6)
RED = mat('sail_red', '#c23b2b', rough=0.55)

P = []
SY = -0.12                        # spar centre plane
# ---- spar: z +0.15 .. -3.0, 0.12 thick, slightly tapered toward the tip
bm = bmesh.new()
prof = [(0.15, 0.06), (-3.0, 0.045)]
rings = []
for z, h in prof:
    rings.append([bm.verts.new((sx * h, SY + sy * 0.06, z)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i]))
bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[1])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
spar = _obj(bm, SPAR, smooth=False)
bevel_obj(spar, 0.015, 1, 40)
P.append(spar)
# painted red tip cap
P.append(bx((-0.052, SY - 0.068, -3.0), (0.052, SY + 0.068, -2.82), RED, 0.012))

# ---- lattice: side rails + cross slats, x 0.06..0.68, z -0.55..-3.0
LY0, LY1 = -0.19, -0.095
P.append(bx((0.06, LY0, -3.0), (0.11, LY1, -0.55), FRAME, 0.01))       # inner rail (against the spar)
P.append(bx((0.63, LY0, -3.0), (0.68, LY1, -0.55), FRAME, 0.01))       # outer rail
NS = 10
for k in range(NS):
    z = -0.57 - (3.0 - 0.6) * k / (NS - 1)
    z = max(min(z, -0.57), -2.98)
    P.append(bx((0.06, LY0 + 0.004, z - 0.025), (0.68, -0.152, z + 0.025), FRAME))
P.append(bx((0.355, -0.2, -2.98), (0.385, -0.165, -0.57), FRAME))   # middle lath in front of the slats
# diagonal-free brace from the spar to the top of the outer rail
br = tube([V(0.03, -0.14, -0.2), V(0.655, -0.14, -0.56)], 0.022, seg=6, material=FRAME, smooth=False)
P.append(br)

# ---- cloth: cream sheet in front of the lattice (Y ~ -0.14), bulged forward, with a hem and reef lines
CX0, CX1, CZ0, CZ1 = 0.1, 0.64, -2.95, -0.6
NX, NZ = 4, 12
bm = bmesh.new()
grid = []
for iz in range(NZ + 1):
    row = []
    for ix in range(NX + 1):
        u = ix / NX; v = iz / NZ
        x = CX0 + (CX1 - CX0) * u
        z = CZ0 + (CZ1 - CZ0) * v
        bulge = math.sin(math.pi * u) * (0.6 + 0.4 * math.sin(math.pi * v)) * 0.04
        row.append(bm.verts.new((x, -0.142 + bulge, z)))
    grid.append(row)
for iz in range(NZ):
    for ix in range(NX):
        bm.faces.new((grid[iz][ix], grid[iz][ix + 1], grid[iz + 1][ix + 1], grid[iz + 1][ix]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
for f in bm.faces:
    if f.normal.y > 0:
        f.normal_flip()
front = list(bm.faces)
# give it a back side (copy, offset backward, flipped) so it is visible from behind without double-sided material
geom = bmesh.ops.duplicate(bm, geom=front)
newf = [g for g in geom['geom'] if isinstance(g, bmesh.types.BMFace)]
newv = [g for g in geom['geom'] if isinstance(g, bmesh.types.BMVert)]
for v in newv:
    v.co.y += 0.008
for f in newf:
    f.normal_flip()
cloth = _obj(bm, CLOTH, smooth=True)
P.append(cloth)
# hem around the cloth + vertical seam lines
# rope ties holding the cloth to the inner and outer rail
for k in range(6):
    z = -0.75 - k * 0.42
    for x in (0.085, 0.655):
        P.append(xf(ell((0, 0, 0), (0.024, 0.022, 0.016), seg=6, rings=3, material=RED), Matrix.Translation((x, -0.192, z))))

# ---- hub piece at the origin: short cylinder r 0.18 along Y (16 verts -> four copies coincide nicely)
P.append(lathe([(0.0, -0.06), (0.17, -0.06), (0.18, -0.04), (0.18, 0.22), (0.165, 0.25), (0.0, 0.25)], seg=16, material=SPAR,
               M=rotm((90, 0, 0)), phase=TAU / 32))
P.append(lathe([(0.188, 0.02), (0.188, 0.07)], seg=16, material=IRON, M=rotm((90, 0, 0)), caps=(False, False), phase=TAU / 32))
P.append(lathe([(0.188, 0.17), (0.188, 0.22)], seg=16, material=IRON, M=rotm((90, 0, 0)), caps=(False, False), phase=TAU / 32))
P.append(lathe([(0.0, 0.245), (0.09, 0.245), (0.085, 0.29), (0.05, 0.315), (0.0, 0.32)], seg=8, material=RED, M=rotm((90, 0, 0)),
               phase=TAU / 16))
# iron strap clamping the spar to the hub
P.append(bx((-0.075, SY - 0.075, -0.32), (0.075, SY + 0.075, -0.24), IRON, 0.01))
for z in (-0.28,):
    for sx in (-1, 1):
        P.append(xf(ell((0, 0, 0), (0.016, 0.016, 0.016), seg=6, rings=3, material=IRON), Matrix.Translation((sx * 0.04, SY - 0.078, z))))

body = part(P, 'body', (0, 0, 0), angle=50)
report()
std_view()
lo, hi = bounds([body]); print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('One windmill sail; the game copies and rotates it around the Y axis. Part: body (origin (0,0,0) = axle centre, no rotation). '
         'Spar 0.12 thick centred on y -0.12 from z +0.15 down to z -3.0 (red tip); lattice (rails + 10 slats) on the +X side, '
         'x 0.06..0.68, z -0.55..-3.0, y -0.19..-0.095 (slats in front); cream cloth x 0.1..0.64, z -2.95..-0.6 at y -0.142 bulging back to ~-0.1; '
         'hub piece: cylinder r 0.18 along Y (y -0.25..0.06) with iron bands and a red nose cap to y -0.32 (16-gon, so 4 copies coincide).')
finish('chars', 'mill_sail', kind='char', footprint=0.7, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('mill_sail', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.5), 'top': (0.2, -0.4, 1)})
    montage('mill_sail', keys=('front', 'side', 'back', 'top'))
