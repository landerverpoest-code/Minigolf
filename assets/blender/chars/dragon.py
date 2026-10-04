import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akit import *
from ccp_kit import _obj

# ---------------------------------------------------------------- materials (6)
STONE = mat('stone', '#9a9184', rough=0.9)
BRONZE = mat('bronze', '#c9803d', rough=0.32, metal=0.85)
STEEL = mat('steel', '#7c8796', rough=0.32, metal=0.85)
GOLD = mat('gold', '#ffc93a', rough=0.25, metal=0.9)
GLOW = mat('glow_eyes', '#ffa020', rough=0.4, emit='#ff6a00', emit_strength=3.0)
MEMB = mat('membrane', '#a3322a', rough=0.6, metal=0.2)

B = []
# ---------------------------------------------------------------- stone pedestal (X 2.4, Y 2.6, Z 1.6)
B.append(box((2.62, 2.82, 0.22), loc=(0, 0, 0.11), material=STONE, bevel=0.04))
B.append(box((2.4, 2.6, 1.22), loc=(0, 0, 0.83), material=STONE, bevel=0.025))
B.append(box((2.62, 2.82, 0.18), loc=(0, 0, 1.51), material=STONE, bevel=0.04))
for sx in (-1, 1):            # corner pilasters
    for sy in (-1, 1):
        B.append(box((0.26, 0.26, 1.22), loc=(sx * 1.17, sy * 1.27, 0.83), material=STONE))
# a few big stone blocks on the long sides for texture
rnd = random.Random(3)
# gold gear plaque on the front
gp = gear(R=0.24, teeth=6, depth=0.04, tooth=0.06, material=GOLD)
xf(gp, Matrix.Translation((0, -1.31, 0.86)))
B.append(gp)

TOP = 1.6
# ---------------------------------------------------------------- torso (crouching, chest up)
TC = V(0, 0.2, 2.2)


def torso_shape(n):
    z = n.z
    if z < -0.55:
        z = -0.55 + (z + 0.55) * 0.25            # flat belly resting on the pedestal
    # chest higher at the front
    z += 0.18 * max(0.0, -n.y) * (1 + n.z) * 0.5
    return Vector((n.x * (1 - 0.12 * n.y), n.y, z))


torso = ell(TC, (0.72, 1.12, 0.62), seg=14, rings=9, material=BRONZE, shape=torso_shape)
# steel belly / chest plating in segments
iso_paint(torso, lambda p: max(abs(p.x) - 0.42, p.z - 2.15 + 0.35 * (p.y - 0.2)) + (0.0 if math.sin(p.y * 9.0) > -0.35 else 1.0), STEEL)
B.append(torso)
# spine: gold spikes
for k in range(6):
    t = k / 5
    y = -0.45 + t * 1.45
    z = 2.86 - 0.08 * t - 0.28 * t * t
    B.append(spike((0, y, z - 0.06), (0, 0.45, 1), r=0.11 - 0.025 * t, h=0.34 - 0.1 * t, seg=5, material=GOLD))
# steel back plates under the spikes
B.append(tube([V(0, -0.6, 2.82), V(0, 0.0, 2.88), V(0, 0.6, 2.78), V(0, 1.05, 2.5)], [0.16, 0.18, 0.17, 0.14], seg=6,
              material=STEEL, flat=0.45))
# turning gear on both flanks (static) with gold hub
for sx in (-1, 1):
    g = gear(R=0.36, teeth=6, depth=0.08, tooth=0.08, material=STEEL)
    xf(g, Matrix.Translation((sx * 0.7, 0.3, 2.15)) @ rotm((0, 0, 90)))
    B.append(g)
    B.append(cyl(0.12, 0.12, loc=(sx * 0.75, 0.3, 2.15), rot=(0, math.pi / 2, 0), verts=8, material=GOLD))
# wind-up key on the back
B.append(cyl_between((0, 0.55, 2.8), (0, 0.6, 3.15), 0.05, seg=6, material=GOLD))
for sx in (-1, 1):
    lp = lathe([(0.12, -0.03), (0.14, 0.0), (0.12, 0.03), (0.1, 0.0)], seg=6, material=GOLD)
    xf(lp, Matrix.Translation((sx * 0.2, 0.6, 3.27)) @ rotm((0, 90, 0)) @ Matrix.Diagonal((1.25, 1.0, 1, 1)))
    B.append(lp)
B.append(ell(V(0, 0.6, 3.22), (0.07, 0.06, 0.06), seg=6, rings=4, material=GOLD))

# ---------------------------------------------------------------- legs (static)
for sx in (-1, 1):
    # front leg: shoulder -> elbow -> paw on the pedestal top near the front edge
    S0, E0, P0 = V(sx * 0.52, -0.55, 2.15), V(sx * 0.66, -0.8, 1.95), V(sx * 0.62, -1.06, 1.7)
    B.append(tube([S0, E0, P0], [0.24, 0.17, 0.13], seg=8, material=BRONZE))
    B.append(ell(E0 + V(sx * 0.04, 0, 0), (0.12, 0.14, 0.14), seg=6, rings=4, material=STEEL))
    B.append(ell(P0 + V(0, -0.06, -0.03), (0.17, 0.2, 0.08), seg=7, rings=4, material=BRONZE))
    for k in (-1, 0, 1):
        base = P0 + V(k * 0.1, -0.22, -0.04)
        B.append(spike(base, (k * 0.2, -1, -0.5), r=0.04, h=0.16, seg=4, material=GOLD))
    # hind leg: big haunch + folded foot
    B.append(ell(V(sx * 0.6, 0.72, 2.02), (0.28, 0.5, 0.4), seg=9, rings=6, material=BRONZE, rot=(-15, 0, 0)))
    H0 = V(sx * 0.66, 0.2, 1.67)
    B.append(ell(H0, (0.15, 0.24, 0.08), seg=6, rings=4, material=BRONZE))
    for k in (-1, 1):
        B.append(spike(H0 + V(k * 0.07, -0.22, -0.02), (k * 0.2, -1, -0.3), r=0.035, h=0.13, seg=4, material=GOLD))

# ---------------------------------------------------------------- static tail root draping down the back of the pedestal
EXIT = V(0, 1.98, 0.7)
tp = bezier(V(0, 1.0, 2.05), V(0, 1.8, 2.0), V(0, 1.75, 0.75), EXIT, n=7)
tail = tube(tp, [0.32 - 0.1 * (i / 7) for i in range(8)], seg=7, material=BRONZE, cap=False)
iso_paint(tail, lambda p: math.sin(((p - V(0, 1.0, 2.05)).length) * 11.0) + 0.2, STEEL)
B.append(tail)
for i in (2, 4, 6):
    a, b = tp[i], tp[i + 1]
    dvec = (b - a).normalized()
    up = V(0, 1, 0).cross(dvec).cross(dvec) * -1 if False else (V(0, 1, 0.3) if i < 4 else V(0, 1, 0)).normalized()
    B.append(spike(a + up * 0.2, up, r=0.08, h=0.22, seg=5, material=GOLD))

body = apart(B, 'body', (0, 0, 0))

# ---------------------------------------------------------------- head (+neck), pivot at the neck base on the torso
NB = V(0, -0.72, 2.6)
HC = V(0, -1.45, 3.22)
H = []
neck_pts = bezier(NB + V(0, 0.15, -0.15), NB + V(0, -0.35, 0.25), HC + V(0, 0.45, -0.35), HC + V(0, 0.15, -0.05), n=6)
neck = tube(neck_pts, [0.32, 0.29, 0.26, 0.24, 0.22, 0.21, 0.21], seg=7, material=BRONZE)
iso_paint(neck, lambda p: math.sin(((p - NB).length) * 12.0) + 0.1, STEEL)
H.append(neck)
for i in (2, 3, 4):
    p = neck_pts[i]
    H.append(spike(p + V(0, 0.15, 0.17), (0, 0.8, 0.6), r=0.06, h=0.18, seg=4, material=GOLD))
NH = len(H)
# skull + snout
H.append(ell(HC, (0.3, 0.34, 0.25), seg=10, rings=7, p=0.85, material=BRONZE))
SN = V(0, -1.88, 3.14)
H.append(ell(SN, (0.2, 0.4, 0.145), seg=10, rings=6, p=0.8, material=BRONZE,
             shape=lambda n: Vector((n.x * (1 + 0.25 * n.y), n.y, n.z * (1 + 0.15 * n.y) + 0.0))))
# steel nose plate + nostrils
H.append(ell(SN + V(0, -0.1, 0.12), (0.14, 0.26, 0.05), seg=6, rings=4, material=STEEL, rot=(-6, 0, 0)))
# glowing eyes under steel brows
for sx in (-1, 1):
    ec = V(sx * 0.19, -1.66, 3.3)
    H.append(eye_e := ell(V(0, 0, 0), (0.1, 0.05, 0.09), seg=8, rings=5, material=GLOW))
    frame(eye_e, ec, V(sx * 0.55, -1, 0.05))
    pu = ell(V(0, 0, 0), (0.02, 0.02, 0.065), seg=6, rings=4, material=STEEL)
    H.append(frame(pu, ec + V(sx * 0.55, -1, 0.05).normalized() * 0.045, V(sx * 0.55, -1, 0.05)))
    brow = ell(V(0, 0, 0), (0.14, 0.07, 0.04), seg=6, rings=4, material=STEEL)
    frame(brow, ec + V(sx * 0.0, 0.01, 0.075), V(sx * 0.5, -1, 0.0))
    xf(brow, Matrix.Translation(ec + V(0, 0, 0.075)) @ rotm((0, sx * 18, 0)) @ Matrix.Translation(-(ec + V(0, 0, 0.075))))
    H.append(brow)
    # horns: gold, sweeping back and up
    hp = bezier(V(sx * 0.17, -1.38, 3.4), V(sx * 0.24, -1.25, 3.62), V(sx * 0.3, -1.0, 3.66), V(sx * 0.33, -0.85, 3.58), n=5)
    H.append(tube(hp, [0.075, 0.06, 0.045, 0.03, 0.016, 0.004], seg=5, material=GOLD))
    # upper fangs
    for k in range(3):
        y = -2.1 + k * 0.13
        H.append(spike(V(sx * (0.11 + 0.025 * k), y, 3.02), (0, 0, -1), r=0.03, h=0.09 - 0.015 * k, seg=4, material=GOLD))
# small crest plates on top of the head
for k in range(3):
    H.append(spike(HC + V(0, 0.05 + k * 0.13, 0.22 - 0.03 * k), (0, 0.6, 1), r=0.05, h=0.13, seg=4, material=GOLD))
HS = Matrix.Translation(HC + V(0, 0.2, -0.15)) @ Matrix.Diagonal((1.25, 1.25, 1.25, 1)) @ Matrix.Translation(-(HC + V(0, 0.2, -0.15)))
for o in H[NH:]:
    xf(o, HS)
head = apart(H, 'head', NB)

# ---------------------------------------------------------------- jaw (parented to head), pivot at the hinge
HG = V(0, -1.4, 3.0)
J = [ell(V(0, -1.76, 2.98), (0.17, 0.36, 0.07), seg=8, rings=5, p=0.85, material=STEEL,
         shape=lambda n: Vector((n.x * (1 + 0.2 * n.y), n.y, n.z)))]
J.append(ell(V(0, -1.78, 3.02), (0.14, 0.3, 0.02), seg=6, rings=3, material=GLOW))     # furnace glow inside the mouth
for sx in (-1, 1):
    for k in range(2):
        J.append(spike(V(sx * (0.12 + 0.02 * k), -2.03 + k * 0.16, 3.0), (0, 0, 1), r=0.028, h=0.07, seg=4, material=GOLD))
for sx in (-1, 1):
    J.append(ell(HG + V(sx * 0.17, -0.02, 0), (0.035, 0.06, 0.06), seg=6, rings=4, material=GOLD))   # hinge bolts
for o in J:
    xf(o, HS)
HG = HS @ HG
jaw = apart(J, 'jaw', HG)
jaw.parent = head
jaw.matrix_parent_inverse = Matrix.Identity(4)
jaw.location = HG - NB

# ---------------------------------------------------------------- folded mechanical bat wings, pivot at the shoulder
WINGS = {}
for side, sx in (('l', 1), ('r', -1)):
    SHW = V(sx * 0.5, -0.15, 2.7)
    WR = V(sx * 0.78, 0.3, 3.45)                         # wrist (folded high)
    tips = [V(sx * 0.82, 1.45, 2.95), V(sx * 0.88, 1.25, 2.35), V(sx * 0.8, 0.75, 2.15)]
    Wp = [tube([SHW, SHW + V(sx * 0.12, 0.2, 0.4), WR], [0.09, 0.08, 0.06], seg=6, material=STEEL)]
    Wp.append(ell(WR, (0.08, 0.08, 0.08), seg=6, rings=4, material=GOLD))
    Wp.append(spike(WR + V(0, -0.02, 0.05), (sx * 0.2, -0.6, 1), r=0.04, h=0.18, seg=4, material=GOLD))
    for t in tips:
        mid = WR.lerp(t, 0.5) + V(sx * 0.05, 0, 0)
        Wp.append(tube([WR, mid, t], [0.045, 0.035, 0.015], seg=4, material=STEEL))
    # membrane: fan from shoulder / wrist to the finger tips with scalloped trailing edge
    bm = bmesh.new()
    pts = [SHW + V(sx * 0.03, 0.1, 0.05), WR]
    for i, t in enumerate(tips):
        pts.append(t)
        if i < len(tips) - 1:
            n2 = tips[i + 1]
            mid = t.lerp(n2, 0.5)
            pts.append(mid.lerp(WR, 0.22))          # scallop inward
    pts.append(SHW + V(sx * 0.1, 0.45, -0.12))
    vs = [bm.verts.new(p + V(sx * 0.01, 0, 0)) for p in pts]
    c = bm.verts.new(sum(pts, Vector()) / len(pts) + V(sx * 0.04, 0, 0))
    for i in range(len(vs) - 1):
        bm.faces.new((c, vs[i], vs[i + 1]))
    bm.faces.new((c, vs[-1], vs[0]))
    Wp.append(_obj(bm, MEMB, smooth=False))
    w = apart(Wp, f'wing_{side}', SHW)
    WINGS[side] = SHW

# ---------------------------------------------------------------- tail segment (centred, 0.45 long along Y, gold spike on top)
seg = lathe([(0.0, -0.225), (0.17, -0.225), (0.225, -0.13), (0.225, 0.1), (0.17, 0.225), (0.0, 0.225)],
            seg=9, material=BRONZE)
iso_paint(seg, lambda p: -(p.z + 0.13) if p.z < 0 else 1, STEEL)           # steel collar toward the body (-Y after rotation)
xf(seg, rotm((-90, 0, 0)))          # local +Z -> -Y? (rotate so lathe axis runs along Y; collar at -Y)
TS = [seg, spike(V(0, 0.02, 0.2), (0, 0.35, 1), r=0.085, h=0.25, seg=5, material=GOLD)]
for sx in (-1, 1):
    TS.append(ell(V(sx * 0.215, 0.0, 0.0), (0.03, 0.06, 0.06), seg=6, rings=4, material=GOLD))
TSEG = V(1.75, 0.55, 0.23)
tail_seg = apart(TS, 'tail_seg', (0, 0, 0))
tail_seg.location = TSEG

# ---------------------------------------------------------------- tail tip (spade, origin at its base, points -Y)
spade = [(0.0, 0.0), (0.07, -0.08), (0.27, -0.22), (0.22, -0.36), (0.1, -0.46), (0.0, -0.64), (-0.1, -0.46), (-0.22, -0.36),
         (-0.27, -0.22), (-0.07, -0.08)]
sp = flat_shape([(x, z) for x, z in spade], 0.08, GOLD)       # outline in XZ, thickness along Y
xf(sp, rotm((90, 0, 0)))                                       # -> outline in XY, thickness along Z
TT = [sp, lathe([(0.0, 0.0), (0.12, 0.0), (0.13, -0.08), (0.08, -0.14), (0.0, -0.15)], seg=8, material=STEEL)]
xf(TT[1], rotm((90, 0, 0)) @ Matrix.Translation((0, 0, 0)))
TT.append(ell(V(0, -0.3, 0.035), (0.05, 0.16, 0.03), seg=6, rings=4, material=BRONZE))
TTIP = V(1.75, 0.15, 0.08)
tail_tip = apart(TT, 'tail_tip', (0, 0, 0))
tail_tip.location = TTIP

report()
notes = ('Parts/pivots (Blender coords, front -Y, left=+X): body (origin 0,0,0 = pedestal centre on the ground; stone pedestal '
         'X2.4 x Y2.6 x Z1.6 (top z=1.6), crouching bronze torso with steel belly plates, gold spine spikes, static gears on both '
         'flanks, gold wind-up key on the back, legs, and a static tail root that drapes down the back of the pedestal); '
         'TAIL EXIT POINT (where the game should start the animated tail, heading +Y, radius ~0.22) = %s; '
         'head (neck + head, pivot at the neck base on the torso %s; face looks -Y; gold horns, glowing eyes glow_eyes); '
         'jaw (lower jaw, PARENTED to head, hinge %s (world), hinge axis = X; rotation.x>0 in Blender (= three.js x>0) opens it '
         'downward; glow_eyes furnace inside); wing_l / wing_r (folded bat wings, pivot shoulder %s / %s); '
         'tail_seg (ONE segment, centred on its origin, 0.45 long along Blender Y (three.js Z), 0.45 thick, steel collar toward '
         '-Y (the body), gold spike on top +Z; parked at %s); tail_tip (gold spade, origin at its base, points -Y, 0.64 long, '
         '0.54 wide; parked at %s). Materials: stone, bronze, steel, gold, glow_eyes, membrane.'
         % (fmt(EXIT), fmt(NB), fmt(HG), fmt(WINGS['l']), fmt(WINGS['r']), fmt(TSEG), fmt(TTIP)))
finish('chars', 'dragon', kind='char', footprint=1.9, grounded=False, notes=notes, preview=False)

# ---------------------------------------------------------------- preview: assemble a full tail like the game would
def tail_curve(u):
    return bezier(EXIT, EXIT + V(0, 0.9, 0.0), EXIT + V(1.6, 1.7, -0.1), EXIT + V(2.6, 0.9, -0.2), n=40)[int(round(u * 40))]


bpy.context.view_layer.update()
PREV = []
nseg = 8
for i in range(nseg):
    u0 = (i + 0.5) / (nseg + 1.2)
    p = tail_curve(u0); p2 = tail_curve(min(1, u0 + 0.025)); p1 = tail_curve(max(0, u0 - 0.025))
    t = (p2 - p1).normalized()
    s = 1.0 - 0.06 * i
    c = dup_baked(tail_seg, 'pv'); c.data.transform(Matrix.Translation(-TSEG))
    q = V(0, 1, 0).rotation_difference(t)
    c.data.transform(Matrix.Translation(p) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    PREV.append(c)
u = (nseg + 0.1) / (nseg + 1.2)
p = tail_curve(u); t = (tail_curve(1.0) - tail_curve(u - 0.03)).normalized()
c = dup_baked(tail_tip, 'pvt'); c.data.transform(Matrix.Translation(-TTIP))
q = V(0, -1, 0).rotation_difference(t)
c.data.transform(Matrix.Translation(p) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((0.6, 0.6, 0.6, 1)))
PREV.append(c)
tail_seg.hide_render = True; tail_tip.hide_render = True
render_preview(f'{ROOT}/previews/chars/dragon.png')
if '--views' in sys.argv:
    views('dragon', dirs={'front': (0, -1, 0.2), 'side': (1, 0, 0.15), 'back': (-0.7, 1, 0.5), 'left': (-1, -0.3, 0.3)})
