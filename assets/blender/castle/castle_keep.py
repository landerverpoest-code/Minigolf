import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

# ---------------------------------------------------------------- materials (6)
stone = mat('stone', '#cbc7c0', rough=0.9)
roof = mat('roof_red', '#c23b2c', rough=0.6)
wood = mat('wood', '#8a5530', rough=0.85)
gold = mat('gold', '#f0bf3a', rough=0.3, metal=0.5)
glow = mat('glow_window', '#ffd27a', rough=0.4, emit='#ffb547', emit_strength=2.2)
blue = mat('banner_blue', '#2459d6', rough=0.75)

rnd = random.Random(7)
P = []          # -> body
FY = -3.0       # front wall plane


def arch_pts(w, h, n=7, x0=0.0, z0=0.0):
    """Closed outline (x,z) of an arched opening: width w, total height h (semicircular top)."""
    r = w / 2
    pts = [(x0 - r, z0), (x0 + r, z0)]
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((x0 + r * math.cos(a), z0 + h - r + r * math.sin(a)))
    return pts


DIRS = {'+x': (1, 0, 0), '-x': (-1, 0, 0), '+y': (0, 1, 0), '-y': (0, -1, 0), '+z': (0, 0, 1), '-z': (0, 0, -1)}


def drop(o, dirs):
    """Delete faces whose normal points along one of dirs (hidden faces against walls/floors)."""
    if not dirs:
        return o
    bm = bmesh.new(); bm.from_mesh(o.data)
    bm.normal_update()
    kill = [f for f in bm.faces if any(f.normal.dot(Vector(DIRS[d])) > 0.99 for d in dirs)]
    bmesh.ops.delete(bm, geom=kill, context='FACES_ONLY')
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o


def bx(size, loc=(0, 0, 0), material=None, dirs=(), bevel=0.0):
    o = box(size, loc=loc, material=material, bevel=bevel)
    return drop(o, dirs)


def face(pts, y, material):
    """Single front-facing polygon (x,z) at depth y, normal -Y."""
    o = mesh_obj([(x, y, z) for x, z in pts], [list(range(len(pts)))], material, 'face')
    bm = bmesh.new(); bm.from_mesh(o.data); bm.normal_update()
    if bm.faces[0].normal.y > 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(o.data); bm.free()
    return o


def window(x, z, w=0.9, h=1.55):
    out = []
    sur = prism(arch_pts(w + 0.36, h + 0.2, 5, x, z - 0.02), 0.14, stone)
    xform(sur, loc=(0, FY - 0.07, 0)); drop(sur, ('+y', '-z'))
    out.append(sur)
    out.append(face(arch_pts(w, h, 5, x, z), FY - 0.145, glow))
    out.append(bx((0.07, 0.05, h - 0.12), (x, FY - 0.17, z + h / 2 - 0.06), wood, ('+y', '-z', '+z')))
    out.append(bx((w + 0.5, 0.3, 0.16), (x, FY - 0.15, z - 0.08), stone, ('+y',)))
    return out


# ---------------------------------------------------------------- main hall
hall = box((12.0, 6.0, 9.0), loc=(0, 0, 4.5), material=stone)
P.append(hall)
# battered plinth
pl = prism([(-3.32, 0), (3.32, 0), (3.32, 0.35), (3.0, 0.85), (-3.0, 0.85), (-3.32, 0.35)], 12.0, stone, axis='X')
P.append(pl)
# string course between the floors
P.append(box((12.0, 6.3, 0.26), loc=(0, 0, 4.62), material=stone, bevel=0.04))
# corbel band + projecting parapet with crenellations
for k in range(24):
    x = -5.75 + k * 0.5
    c = box((0.3, 0.3, 0.42), loc=(x, FY - 0.14, 7.95), material=stone)
    bend(c, lambda v: (v.x, v.y + (0.13 if v.z < 7.95 and v.y < FY - 0.14 else 0), v.z))
    P.append(c)
P.append(box((12.0, 6.6, 0.25), loc=(0, 0, 8.28), material=stone, bevel=0.04))
P.append(box((12.0, 0.4, 0.62), loc=(0, FY - 0.1, 8.71), material=stone))
P.append(box((12.0, 0.4, 0.62), loc=(0, -FY + 0.1, 8.71), material=stone))
for x in [-5.1 + i * 1.02 for i in range(11)]:
    for sy in (-1, 1):
        m = box((0.62, 0.42, 0.62), loc=(x, sy * (3.1), 9.33), material=stone, bevel=0.035)
        P.append(m)
for y in (-1.6, 0.0, 1.6):
    for sx in (-1, 1):
        P.append(box((0.42, 0.62, 0.62), loc=(sx * 5.75, y, 9.33), material=stone))
# low red roof inside the parapet (seen above the battlements)
rf = prism([(-2.75, 0), (2.75, 0), (0, 1.9)], 10.6, roof, axis='X', loc=(0, 0, 8.95))
bm = bmesh.new(); bm.from_mesh(rf.data)
for v in bm.verts:          # hip the ends a little
    if v.co.z > 1.0:
        v.co.x *= 0.82
bm.to_mesh(rf.data); bm.free()
P.append(rf)

# ---------------------------------------------------------------- gate
GW, GR, GH = 2.5, 1.25, 3.6           # width, arch radius, total height
P.append(box((GW + 0.1, 0.2, GH), loc=(0, FY + 0.02, GH / 2), material=wood))   # recess back
for i in range(6):
    x = -GW / 2 + (i + 0.5) * GW / 6
    top = GH - GR + math.sqrt(max(0.0, GR * GR - x * x)) - 0.03
    pk = box((GW / 6 - 0.03, 0.12, top), loc=(x, FY - 0.08, top / 2), material=wood, bevel=0.025)
    jitter(pk, 0.008, i)
    P.append(pk)
for z in (0.8, 2.3):
    hw = GW / 2 - 0.03 if z < GH - GR else math.sqrt(GR * GR - (z - (GH - GR)) ** 2)
    P.append(box((2 * hw, 0.05, 0.14), loc=(0, FY - 0.16, z), material=gold))
for x in (-0.95, -0.35, 0.35, 0.95):
    for z in (0.8, 2.3):
        P.append(box((0.08, 0.06, 0.08), loc=(x, FY - 0.2, z), material=gold))
for sx in (-1, 1):
    P.append(torus(0.14, 0.03, loc=(sx * 0.3, FY - 0.2, 1.55), rot=(math.pi / 2, 0, 0), seg=8, ring=4, material=gold, smooth=False))
# stone voussoirs around the arch + jamb blocks
NV = 9
for i in range(NV):
    a0 = math.pi * i / NV + 0.012; a1 = math.pi * (i + 1) / NV - 0.012
    ri, ro = GR + 0.02, GR + (0.6 if i == NV // 2 else 0.48)
    pts = [(ri * math.cos(a0), ri * math.sin(a0)), (ro * math.cos(a0), ro * math.sin(a0)),
           (ro * math.cos(a1), ro * math.sin(a1)), (ri * math.cos(a1), ri * math.sin(a1))]
    v = prism([(px, pz + GH - GR) for px, pz in pts], 0.32 if i == NV // 2 else 0.26, stone)
    xform(v, loc=(0, FY - 0.12, 0))
    P.append(v)
for sx in (-1, 1):
    for k in range(4):
        h = (GH - GR) / 4
        wj = 0.5 if k % 2 == 0 else 0.38
        P.append(box((wj, 0.26, h - 0.04), loc=(sx * (GW / 2 + wj / 2 + 0.02), FY - 0.12, h * k + h / 2), material=stone))
# two little steps in front of the gate
P.append(box((3.4, 0.6, 0.18), loc=(0, FY - 0.3, 0.09), material=stone, bevel=0.03))

# ---------------------------------------------------------------- windows (two rows)
for x in (-4.7, -2.6, 2.6, 4.7):
    P += window(x, 2.05)
    P += window(x, 5.6)

# ---------------------------------------------------------------- loose stone blocks on the front
avoid = [(-1.8, 1.8, 0, 4.2), (-0.85, 0.85, 4.0, 8.0)] + [(x - 0.75, x + 0.75, z - 0.3, z + 1.95) for x in (-4.7, -2.6, 2.6, 4.7) for z in (2.05, 5.6)]
placed = 0; tries_ = 0
while placed < 34 and tries_ < 600:
    tries_ += 1
    x = rnd.uniform(-5.6, 5.6); z = rnd.uniform(1.1, 7.6)
    w = rnd.uniform(0.5, 0.85); h = rnd.uniform(0.28, 0.36)
    if any(a - w / 2 < x < b + w / 2 and c - h < z < d + h for a, b, c, d in avoid):
        continue
    if 4.3 < z < 5.0:
        continue
    avoid.append((x - w / 2 - 0.08, x + w / 2 + 0.08, z - 0.1, z + 0.1))
    P.append(box((w, 0.1, h), loc=(x, FY - 0.03, z), material=stone))
    placed += 1

# ---------------------------------------------------------------- corner towers
SEG = 16


def tower(cx):
    out = []
    prof = [(2.3, 0.0), (2.3, 0.45), (2.02, 0.95), (1.83, 10.6), (2.36, 11.25), (2.36, 12.1), (2.06, 12.1), (2.06, 11.6), (1.72, 11.6), (1.72, 13.05)]
    t = lathe(prof, seg=SEG, material=stone, cap_bottom=False, cap_top=True, phase=math.pi / SEG)
    smooth(t, 30)
    xform(t, loc=(cx, 0, 0))
    out.append(t)
    # band halfway
    def r_at(z):
        return 2.02 + (1.83 - 2.02) * (z - 0.95) / (10.6 - 0.95)
    band = lathe([(r_at(4.5) + 0.12, 4.5), (r_at(4.5) + 0.12, 4.75), (r_at(4.75) - 0.02, 4.8)], seg=SEG, material=stone, cap_bottom=True, cap_top=False, phase=math.pi / SEG)
    xform(band, loc=(cx, 0, 0)); out.append(band)
    # merlons on the walkway ring
    for k in range(10):
        a = TAU * (k + 0.5) / 10
        m = box((0.32, 0.62, 0.6), material=stone, bevel=0.03)
        xform(m, loc=(2.21, 0, 12.4))
        xform(m, rot=(0, 0, math.degrees(a)))
        xform(m, loc=(cx, 0, 0))
        out.append(m)
    # conical red roof with tile rings and flared eave
    RZ = 13.0
    rp = [(2.3, RZ), (2.05, RZ + 0.42)]
    rows = 5
    for k in range(1, rows + 1):
        tt = k / (rows + 1)
        z = RZ + 0.42 + tt * 3.58
        r = 2.05 * (1 - tt) ** 1.12
        rp += [(r + 0.09, z - 0.03), (r, z)]
    rp += [(0, RZ + 4.0)]
    rr = lathe(rp, seg=SEG, material=roof, cap_bottom=True, phase=math.pi / SEG)
    smooth(rr, 35)
    xform(rr, loc=(cx, 0, 0)); out.append(rr)
    # gold finial
    out.append(sphere(0.17, loc=(cx, 0, RZ + 4.08), seg=8, rings=6, material=gold))
    out.append(cone(0.07, 0.5, loc=(cx, 0, RZ + 4.45), verts=6, material=gold))
    # glowing tower windows (facing front / outward)
    s = 1 if cx > 0 else -1
    for (ang, z, w, h) in ((-90 + s * 35, 6.5, 0.6, 1.2), (-90 + s * 75, 9.0, 0.55, 1.1), (-90 + s * 10, 2.2, 0.55, 1.0)):
        r = r_at(z + h / 2)
        pane = prism(arch_pts(w, h, 5, 0, 0), 0.08, glow)
        fr = arch_frame(w, h, 0.14, 0.12, 0.0, 0, 0, stone, 5)
        sill = box((w + 0.3, 0.26, 0.12), loc=(0, -0.1, -0.06), material=stone)
        for o in (pane, fr, sill):
            xform(o, loc=(0, -r + 0.03, z))
            xform(o, rot=(0, 0, ang + 90))
            xform(o, loc=(cx, 0, 0))
            out.append(o)
    # tiny dormer window on the roof drum
    for ang in (-90 + s * 20,):
        pane = prism(arch_pts(0.34, 0.55, 4, 0, 0), 0.06, glow)
        xform(pane, loc=(0, -1.72, 12.25)); xform(pane, rot=(0, 0, ang + 90)); xform(pane, loc=(cx, 0, 0))
        out.append(pane)
    # scattered blocks on the shaft
    for k in range(10):
        a = math.radians(rnd.uniform(-180, 20) if cx < 0 else rnd.uniform(160, 360))
        z = rnd.uniform(1.4, 10.0)
        if 4.2 < z < 5.1:
            continue
        b = box((0.1, rnd.uniform(0.45, 0.7), rnd.uniform(0.26, 0.34)), material=stone)
        xform(b, loc=(r_at(z) - 0.01, 0, z)); xform(b, rot=(0, 0, math.degrees(a))); xform(b, loc=(cx, 0, 0))
        out.append(b)
    return out


P += tower(-6.0)
P += tower(6.0)

# ---------------------------------------------------------------- small third tower on the back roof
bt = lathe([(1.05, 8.9), (1.0, 11.6), (1.25, 11.95), (1.25, 12.35), (1.0, 12.35), (1.0, 12.5)], seg=12, material=stone, cap_bottom=False, cap_top=True)
xform(bt, loc=(0, 1.6, 0)); P.append(bt)
for k in range(8):
    a = TAU * (k + 0.5) / 8
    m = box((0.22, 0.38, 0.36), material=stone)
    xform(m, loc=(1.14, 0, 12.53)); xform(m, rot=(0, 0, math.degrees(a))); xform(m, loc=(0, 1.6, 0))
    P.append(m)
btr = lathe([(1.3, 12.55), (1.15, 12.8), (0.75, 13.7), (0.38, 14.55), (0, 15.3)], seg=12, material=roof)
smooth(btr, 35)
xform(btr, loc=(0, 1.6, 0)); P.append(btr)
P.append(sphere(0.12, loc=(0, 1.6, 15.35), seg=8, rings=5, material=gold))
pane = prism(arch_pts(0.4, 0.75, 4, 0, 0), 0.06, glow)
xform(pane, loc=(0, 1.6 - 1.02, 10.5)); P.append(pane)

# banner rod + brackets (fixed, part of the body)
BY, BZ = FY - 0.22, 7.9
P.append(rod((-0.85, BY, BZ), (0.85, BY, BZ), 0.045, verts=6, material=gold))
for sx in (-0.75, 0.75):
    P.append(box((0.06, 0.24, 0.06), loc=(sx, FY - 0.11, BZ), material=gold))
for sx in (-1, 1):
    P.append(sphere(0.07, loc=(sx * 0.88, BY, BZ), seg=6, rings=4, material=gold, smooth=False))

body = join(P, 'body')
smooth(body, 30)

# ---------------------------------------------------------------- banner (separate, pivot at its top centre)
BW, BL = 1.4, 3.6
outline = [(-BW / 2, 0), (BW / 2, 0), (BW / 2, -BL + 0.55), (0, -BL), (-BW / 2, -BL + 0.55)]
cloth = prism(outline, 0.04, blue)
# gold border behind the cloth
bord = prism([(x * 1.09, z * 1.03 + 0.0) for x, z in outline], 0.02, gold)
xform(bord, loc=(0, 0.025, 0.02))
# loops over the rod
loops = [box((0.18, 0.1, 0.16), loc=(x, 0, 0.02), material=blue) for x in (-0.5, 0.0, 0.5)]
# emblem: golden crown + diamond
crown = prism([(-0.36, -0.28), (0.36, -0.28), (0.4, 0.12), (0.2, -0.06), (0.0, 0.2), (-0.2, -0.06), (-0.4, 0.12)], 0.03, gold)
xform(crown, loc=(0, -0.03, -1.15))
gems = [sphere(0.06, loc=(x, -0.04, z), seg=6, rings=4, material=gold, smooth=False) for x, z in ((-0.4, -1.0), (0.0, -0.92), (0.4, -1.0))]
dia = prism([(0, 0.32), (0.22, 0), (0, -0.32), (-0.22, 0)], 0.03, gold)
xform(dia, loc=(0, -0.03, -2.05))
stripe = box((BW * 0.92, 0.03, 0.08), loc=(0, -0.03, -0.42), material=gold)
ban = join([cloth, bord, crown, dia, stripe] + loops + gems, 'banner')
bend(ban, lambda v: (v.x, v.y + 0.035 * math.sin(v.x * 5.0) * min(1, -v.z / 0.6 if v.z < 0 else 0), v.z))
xform(ban, loc=(0, BY, BZ))
set_origin(ban, (0, BY, BZ))
flat(ban)

report()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
finish('castle', 'castle_keep', kind='char', footprint=8.3, grounded=False,
       notes='Big castle keep behind the castle holes. Parts: body (main hall x -6..6, y -3..3, walls to z 9 + crenellations to 9.64, '
             'arched wooden gate, 8 glowing windows in two rows (glow_window), stone trim/corbels, low red roof, round towers at x=+-6 '
             '(r 2.0->1.83, walls to 13, crenellated walkway ring, red cone roof base r 2.3 to z 17, gold finial), small back-roof tower); '
             'banner (blue banner with gold crown, pivot at its top centre (0,-3.22,7.9), sways). Origin = ground centre.')
