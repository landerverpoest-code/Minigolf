import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from okit import *
from okit import _obj

# Mill house of hole 1 (meadow). The ball rolls THROUGH the arched passage x -0.8..0.8, z 0..1.1 (kept fully open);
# the sails (mill_sail, game-placed) turn around the Y axis through (0, -1.6, 2.7) in front of the -Y face, so in front
# of the face (Y < -1.35) nothing but the axle boss lies within 3.2 m of that point.
PLASTER = mat('plaster', '#f6efe2', rough=0.9)
TIMBER = mat('timber', '#7a4a2a', rough=0.75)
TILE = mat('roof_tile', '#c24a2e', rough=0.7)
DARK = mat('roof_dark', '#5a2a1e', rough=0.6)
GLOW = mat('glow_window', '#ffd34d', rough=0.5, emit='#ffc83a', emit_strength=2.2)
LEAF = mat('leaf', '#4f9a3a', rough=0.7)

FY = -1.3           # front face
BY = 1.3            # back face
HUB = V(0, -1.6, 2.7)
P = []


def boolean_diff(o, cutters):
    for c in cutters:
        m = o.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.solver = 'EXACT'; m.object = c
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=m.name)
    for c in cutters:
        bpy.data.objects.remove(c)
    return o


def prism_y(pts_xz, y0, y1, material=None, mat_down=None):
    """Extrude a polygon in the XZ plane (CCW seen from -Y) from y0 to y1."""
    bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in pts_xz]
    b = [bm.verts.new((x, y1, z)) for x, z in pts_xz]
    n = len(pts_xz)
    bm.faces.new(a); bm.faces.new(list(reversed(b)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], b[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj(bm, material, smooth=False)
    if mat_down is not None:
        mi = add_mat(o, mat_down)
        for p in o.data.polygons:
            if abs(p.normal.y) < 0.5 and p.normal.z < 0.5:
                p.material_index = mi
    return o


# ------------------------------------------------------------------ wing blocks (plaster on a brick plinth)
wings = []
for s in (-1, 1):
    x0, x1 = sorted((s * 0.8, s * 3.0))
    w = bx((x0, FY, 0.3), (x1, BY, 2.6), PLASTER)
    cut = []
    xc = s * 1.9
    cut.append(bx((xc - 0.3, FY - 0.2, 1.2), (xc + 0.3, FY + 0.14, 2.05)))      # front niche (depth 0.14)
    cut.append(bx((xc - 0.3, BY - 0.14, 1.2), (xc + 0.3, BY + 0.2, 2.05)))      # back niche
    xa, xb = (2.86, 3.2) if s > 0 else (-3.2, -2.86)
    cut.append(bx((xa, -0.3, 1.2), (xb, 0.3, 2.05)))                             # gable-end niche
    boolean_diff(w, cut)
    mi = add_mat(w, TIMBER)
    for pg in w.data.polygons:
        if abs(abs(pg.center.x) - 0.8) < 1e-3 and abs(pg.normal.x) > 0.9:
            pg.material_index = mi
    wings.append(w)
    P.append(w)
    # brick plinth (flush with the passage side: never sticks into x -0.8..0.8)
    xi0, xi1 = (x0 - 0.03, x1) if s < 0 else (x0, x1 + 0.03)
    P.append(bx((xi0, FY - 0.035, 0.0), (xi1, BY + 0.035, 0.32), TILE, 0.02))
    P.append(bx((xi0 - (0.005 if s < 0 else 0), FY - 0.045, 0.3), (xi1 + (0.005 if s > 0 else 0), BY + 0.045, 0.36), DARK, 0.012))

# ------------------------------------------------------------------ middle section over the arched passage
ARCH_H = 0.36
arch = [(-0.8 + 1.6 * i / 10, 1.1 + ARCH_H * math.sqrt(max(0.0, 1 - ((-0.8 + 1.6 * i / 10) / 0.8) ** 2))) for i in range(11)]
mid_pts = [(0.8, 1.1)] + [p for p in reversed(arch)][1:] + [(-0.8, 2.6), (0.8, 2.6)]
P.append(prism_y(mid_pts, FY, BY, PLASTER, mat_down=TIMBER))

# ------------------------------------------------------------------ arched wooden portals on both ends
def portal(face, s):
    """face = y of the wall face, s = outward sign (-1 front, +1 back). Proud by 0.045 at most."""
    out = []
    y0, y1 = sorted((face, face + s * 0.045))
    for sx in (-1, 1):   # posts on the wing faces (x 0.8..1.0)
        xa, xb = sorted((sx * 0.8, sx * 1.0))
        out.append(bx((xa, y0, 0.0), (xb, y1, 1.16), TIMBER))
        out.append(bx((xa - (0.02 if sx < 0 else 0), y0 - 0.002, 0.0), (xb + (0.02 if sx > 0 else 0), y1 + 0.002, 0.16), DARK))   # post shoe
    # voussoir planks around the arch: inner edge on the arch, outer edge 0.2 further out
    n = 5
    for k in range(n):
        a0 = math.pi * (k + 0.06) / n; a1 = math.pi * (k + 0.94) / n
        pts = []
        for a in (a0, a1):
            pts.append((0.8 * math.cos(a), 1.1 + ARCH_H * math.sin(a)))
        for a in (a1, a0):
            pts.append((1.0 * math.cos(a), 1.1 + (ARCH_H + 0.2) * math.sin(a)))
        pts = [pts[1], pts[0], pts[3], pts[2]]
        o = prism_y([pts[0], pts[1], pts[2], pts[3]], y0, y1, DARK if k == n // 2 else TIMBER)
        out.append(o)
    return out


P += portal(FY, -1)
P += portal(BY, 1)

# ------------------------------------------------------------------ timber frame
for sx in (-1, 1):
    for sy in (-1, 1):
        x = sx * 3.0; y = sy * 1.3
        P.append(bx((x - 0.12 if sx > 0 else x - 0.03, y - 0.12 if sy > 0 else y - 0.035,
                     0.32), (x + 0.03 if sx > 0 else x + 0.12, y + 0.035 if sy > 0 else y + 0.12, 2.6), TIMBER))
# top plate around the whole house
P.append(bx((-3.03, FY - 0.035, 2.46), (3.03, FY + 0.05, 2.6), TIMBER))
P.append(bx((-3.03, BY - 0.05, 2.46), (3.03, BY + 0.035, 2.6), TIMBER))
for sx in (-1, 1):
    P.append(bx((sx * 3.0 - 0.05, FY, 2.46), (sx * 3.0 + 0.05, BY, 2.6), TIMBER))


# ------------------------------------------------------------------ windows
def window(c, n, box=True, shutters=True):
    """c = centre of the niche opening on the wall face, n = outward normal (unit axis vector)."""
    out = []
    c = V(c); n = V(n)
    t = V(-n.y, n.x, 0)   # tangent along the wall
    # helper: box in local (t, n, z) coordinates
    def lb(t0, t1, n0, n1, z0, z1, m, bev=0.0):
        o = bx((t0, n0, z0), (t1, n1, z1), m, bev)
        R = Matrix(((t.x, n.x, 0), (t.y, n.y, 0), (0, 0, 1))).to_4x4()
        return xf(o, Matrix.Translation(V(c.x, c.y, 0)) @ R)
    zc = c.z
    pane = lb(-0.3, 0.3, -0.135, -0.125, 1.2, 2.05, GLOW)                                    # glowing pane (front quad only)
    bmp = bmesh.new(); bmp.from_mesh(pane.data)
    bmesh.ops.delete(bmp, geom=[f for f in bmp.faces if f.normal.dot(n) < 0.9], context='FACES')
    bmp.to_mesh(pane.data); bmp.free()
    out.append(pane)
    out.append(lb(-0.025, 0.025, -0.14, -0.1, 1.2, 2.05, TIMBER))                          # mullion
    out.append(lb(-0.3, 0.3, -0.14, -0.1, 1.68, 1.73, TIMBER))                             # transom
    # frame proud of the wall (max 0.04)
    out.append(lb(-0.38, 0.38, -0.02, 0.035, 2.05, 2.15, TIMBER))                   # lintel
    for sx in (-1, 1):   # jambs
        out.append(lb(*sorted((sx * 0.3, sx * 0.37)), -0.02, 0.03, 1.15, 2.08, TIMBER))
    if box:   # flower box resting in the niche, front at most 0.035 proud
        out.append(lb(-0.29, 0.29, -0.13, 0.035, 1.2, 1.37, TIMBER))
        out.append(lb(-0.31, 0.31, 0.0, 0.04, 1.33, 1.38, DARK))
        rnd = random.Random(int(abs(c.x) * 10 + abs(c.y) * 7))
        for k in range(3):
            tt = -0.18 + 0.18 * k
            g = ell((0, 0, 0), (0.12, 0.07, 0.075), seg=6, rings=3, material=LEAF)
            out.append(xf(g, Matrix.Translation(c + t * tt + n * (-0.06) + V(0, 0, 1.43 - zc))))
        for k in range(5):
            tt = -0.2 + 0.1 * k + rnd.uniform(-0.015, 0.015)
            zf = 1.5 + rnd.uniform(-0.02, 0.04)
            p = c + t * tt + n * (-0.035 - rnd.uniform(0.0, 0.03)) + V(0, 0, zf - zc)
            fl = ell((0, 0, 0), (0.062, 0.055, 0.045), seg=6, rings=3, material=(TILE, GLOW, PLASTER)[k % 3])
            out.append(xf(fl, Matrix.Translation(p)))
    else:
        out.append(lb(-0.36, 0.36, -0.13, 0.04, 1.14, 1.2, TIMBER))                  # sill
    if shutters:
        for sx in (-1, 1):
            a, b = sorted((sx * 0.38, sx * 0.64))
            out.append(lb(a, b, 0.0, 0.03, 1.22, 2.03, LEAF))
            # white diamond cut-out look
            d = ell((0, 0, 0), (0.04, 0.01, 0.06), seg=4, rings=3, material=PLASTER, smooth=False)
            out.append(xf(d, Matrix.Translation(c + t * ((a + b) / 2) + n * 0.03 + V(0, 0, 1.78 - zc))))
    return out


for s in (-1, 1):
    P += window((s * 1.9, FY, 1.6), (0, -1, 0), box=True)
    P += window((s * 1.9, BY, 1.6), (0, 1, 0), box=False)
    P += window((s * 3.0, 0.0, 1.6), (s, 0, 0), box=False)

# a few bare bricks peeking through the plaster
for (x, y, z, n) in ((-2.55, FY, 0.75, (0, -1)), (1.2, FY, 2.22, (0, -1)), (3.0, 0.75, 0.8, (1, 0))):
    for (dx, dz) in ((0, 0), (0.13, 0), (0.065, 0.075)):
        if n[1] != 0:
            P.append(bx((x + dx - 0.055, y - 0.012, z + dz - 0.03), (x + dx + 0.055, y + 0.012, z + dz + 0.03), TILE))
        else:
            P.append(bx((x - 0.012, y + dx - 0.055, z + dz - 0.03), (x + 0.012, y + dx + 0.055, z + dz + 0.03), TILE))

# ------------------------------------------------------------------ front wall gable (dormer) carrying the axle
GX = 0.95
P.append(prism_y([(-GX, 2.55), (GX, 2.55), (GX, 3.0), (0.0, 3.8), (-GX, 3.0)], FY, -0.6, PLASTER))
# its little roof: two tiled slabs from the front face back into the main roof
for sx in (-1, 1):
    a = math.atan2(0.8, GX)
    L = math.hypot(GX + 0.12, 0.88)
    sl = bx((-L / 2, 0.0, 0.0), (L / 2, 0.85, 0.09), TILE, 0.02)
    place(sl, (sx * (GX + 0.12) / 2, FY - 0.045, 3.0 - 0.07 + 0.88 / 2 - 0.02), (0, sx * math.degrees(math.atan2(0.88, GX + 0.12)), 0))
    P.append(sl)
    # barge board
    bb = bx((-L / 2, 0.0, -0.06), (L / 2, 0.04, 0.03), TIMBER, 0.01)
    place(bb, (sx * (GX + 0.12) / 2, FY - 0.046, 3.0 - 0.07 + 0.88 / 2 - 0.05), (0, sx * math.degrees(math.atan2(0.88, GX + 0.12)), 0))
    P.append(bb)
P.append(tube([V(0, FY - 0.04, 3.86), V(0, -0.55, 3.86)], 0.06, seg=6, material=DARK))
# round glowing window in the gable
P.append(xf(ell((0, 0, 0), (0.15, 0.01, 0.15), seg=12, rings=4, material=GLOW), Matrix.Translation((0, FY - 0.005, 3.36))))
P.append(torus(R=0.17, r=0.035, loc=(0, FY - 0.01, 3.36), rot=(math.pi / 2, 0, 0), seg=12, ring=5, material=TIMBER))
P.append(bx((-0.012, FY - 0.03, 3.2), (0.012, FY, 3.52), TIMBER))
P.append(bx((-0.16, FY - 0.03, 3.348), (0.16, FY, 3.372), TIMBER))
# timber posts on the gable corners
for sx in (-1, 1):
    P.append(bx((sx * GX - 0.07, FY - 0.04, 2.55), (sx * GX + 0.07, FY + 0.02, 3.0), TIMBER, 0.01))

# ------------------------------------------------------------------ axle boss
P.append(bx((-0.33, FY - 0.045, 2.38), (0.33, FY + 0.01, 3.04), TIMBER, 0.02))            # bearing plate
for (x, z) in ((-0.26, 2.45), (0.26, 2.45), (-0.26, 2.97), (0.26, 2.97)):
    P.append(xf(ell((0, 0, 0), (0.03, 0.02, 0.03), seg=6, rings=3, material=DARK), Matrix.Translation((x, FY - 0.05, z))))
P.append(lathe([(0.0, 0.0), (0.27, 0.0), (0.27, 0.2), (0.25, 0.26), (0.2, 0.3), (0.0, 0.3)], seg=12, material=TIMBER,
               M=Matrix.Translation((0, FY, HUB.z)) @ rotm((90, 0, 0)), phase=TAU / 24))
for yy, rr in ((FY - 0.06, 0.285), (FY - 0.2, 0.285)):
    P.append(lathe([(rr, -0.025), (rr, 0.025)], seg=12, material=DARK, M=Matrix.Translation((0, yy, HUB.z)) @ rotm((90, 0, 0)),
                   caps=(False, False), phase=TAU / 24))
P.append(lathe([(0.0, 0.0), (0.09, 0.0), (0.09, 0.035)], seg=8, material=DARK, M=Matrix.Translation((0, FY - 0.3, HUB.z)) @ rotm((90, 0, 0))))

# ------------------------------------------------------------------ hip roof with tile courses
EF, EB, EX = -1.35, 1.55, 3.25     # eave outline incl. the tile lip (front kept at -1.35 because of the sails)
LIP = 0.09
CY = (EF + EB) / 2
HY0 = (EB - EF) / 2 - LIP
HX0 = EX - LIP
Z0, Z1 = 2.6, 4.9
N = 7


def ring_at(t, out=0.0, dz=0.0):
    hy = HY0 * (1 - t) + out; hx = HX0 - HY0 * t + out; z = Z0 + (Z1 - Z0) * t + dz
    return [V(hx, CY - hy, z), V(hx, CY + hy, z), V(-hx, CY + hy, z), V(-hx, CY - hy, z)]


bm = bmesh.new()
for k in range(N):
    t0 = k / N; t1 = (k + 1) / N
    lo_out = [bm.verts.new(p) for p in ring_at(t0, LIP, -0.07)]
    lo_in = [bm.verts.new(p) for p in ring_at(t0, 0.0, 0.0)]
    hi = [bm.verts.new(p) for p in ring_at(t1, 0.0, 0.0)]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((lo_out[i], lo_out[j], hi[j], hi[i]))
        bm.faces.new((lo_in[i], lo_in[j], lo_out[j], lo_out[i]))
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
for f in bm.faces:
    if f.normal.z < -0.5:
        f.normal_flip() if False else None
roof = _obj(bm, TILE, smooth=False)
P.append(roof)
# underside / soffit plate to close the roof
P.append(bx((-HX0 + 0.02, EF + LIP, 2.55), (HX0 - 0.02, EB - LIP, 2.62), TIMBER))
# hip + ridge caps
top = ring_at(1.0, 0.0, 0.05)
ridge0, ridge1 = top[3], top[0]
for c0 in ring_at(0.05, 0.0, 0.05):
    end = ridge1 if c0.x > 0 else ridge0
    P.append(tube([c0, end], [0.07, 0.065], seg=6, material=DARK))
P.append(tube([ridge0 + V(-0.08, 0, 0), ridge1 + V(0.08, 0, 0)], 0.085, seg=8, material=DARK))
for e in (ridge0 + V(-0.1, 0, 0.02), ridge1 + V(0.1, 0, 0.02)):
    P.append(ell(e, (0.11, 0.11, 0.11), seg=8, rings=5, material=DARK))
# tiny chimney on the back slope
P.append(bx((1.15, 0.55, 3.6), (1.5, 0.9, 4.75), TILE, 0.02))
P.append(bx((1.1, 0.5, 4.7), (1.55, 0.95, 4.8), DARK, 0.015))

body = part(P, 'body', (0, 0, 0), angle=61)

# ---- remove faces buried inside the walls / under the roof (saves tris and bytes)
EPS = 0.004
SOLIDS = [((0.8, -1.3, 0.0), (3.0, 1.3, 2.6)), ((-3.0, -1.3, 0.0), (-0.8, 1.3, 2.6)), ((-0.8, -1.3, 1.47), (0.8, 1.3, 2.6)),
          ((-GX, -1.3, 2.55), (GX, -0.6, 3.0))]
HOLES = [((1.6, -1.5, 1.2), (2.2, -1.16, 2.05)), ((-2.2, -1.5, 1.2), (-1.6, -1.16, 2.05)),
         ((1.6, 1.16, 1.2), (2.2, 1.5, 2.05)), ((-2.2, 1.16, 1.2), (-1.6, 1.5, 2.05)),
         ((2.86, -0.3, 1.2), (3.3, 0.3, 2.05)), ((-3.3, -0.3, 1.2), (-2.86, 0.3, 2.05))]


def inside_box(p, b, e):
    return all(b[0][i] + e < p[i] < b[1][i] - e for i in range(3))


def buried(p):
    if any(inside_box(p, b, EPS) for b in SOLIDS) and not any(inside_box(p, h, -EPS) for h in HOLES):
        return True
    t = (p.z - Z0) / (Z1 - Z0)
    if 0.0 < t < 1.0 and p.z > 2.63:
        hy = HY0 * (1 - t) - EPS; hx = HX0 - HY0 * t - EPS
        if abs(p.y - CY) < hy and abs(p.x) < hx:
            return True
    return False


bm = bmesh.new(); bm.from_mesh(body.data)
dead = [f for f in bm.faces if buried(f.calc_center_median())]
bmesh.ops.delete(bm, geom=dead, context='FACES')
bm.to_mesh(body.data); bm.free(); body.data.update()
print('CULLED faces', len(dead))
report()
std_view()

# ---- checks: passage box and the sail disc
import numpy as np
viol_p = viol_s = 0
for v in body.data.vertices:
    p = body.matrix_world @ v.co
    if -0.8 + 1e-3 < p.x < 0.8 - 1e-3 and p.z < 1.1 - 1e-3:
        viol_p += 1; print('  PV', tuple(round(k, 3) for k in p))
    if p.y < -1.35 - 1e-3 and (p - HUB).length < 3.2 and not (abs(p.x) < 0.3 and abs(p.z - HUB.z) < 0.3):
        viol_s += 1; print('  SV', tuple(round(k, 3) for k in p))
print('CHECK passage verts inside box:', viol_p, ' sail-disc violations:', viol_s)
lo, hi = bounds([body]); print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))

notes = ('Mill house of hole 1. Part: body (origin (0,0,0) = ground centre of the house, no rotation). Wing blocks x -3.0..-0.8 and '
         '0.8..3.0, y -1.3..1.3, walls z 0..2.6 (white plaster on a brick plinth, timber corners/top plate, glowing windows '
         '"glow_window", flower boxes recessed in the front niches). Middle section x -0.8..0.8, z 1.1..2.6 with a timber-vaulted arch; '
         'passage x -0.8..0.8, z 0..1.1 through the whole depth is completely empty (arched wooden portals on both ends, flush on the '
         'wing faces). Hip roof (red tiles) eaves at z 2.6, overhang 0.25 at back/sides and 0.05 at the front, ridge cap top ~z 5.05. '
         'Front wall gable carries the axle boss: cylinder r 0.27 from y -1.3 to -1.6 at (0, z 2.7); sails turn around Y through '
         '(0,-1.6,2.7) and nothing else lies in front of y -1.35 within 3.2 m of that point.')
finish('chars', 'windmill_house', kind='char', footprint=3.2, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('windmill_house', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.5), 'top': (0.2, -0.4, 1)})
    montage('windmill_house', keys=('front', 'side', 'back', 'top'))
