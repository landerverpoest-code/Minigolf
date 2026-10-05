import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from dkit import *
from dkit import _obj

# Small friendly red dragon flying in circles (LIFE_BRIEF "castle/dragon_flyer").
# Origin = body CENTRE, nose to -Y, up +Z, left = +X. Wings spread along +-X, flapped around Y by the game.

# ---------------------------------------------------------------- materials (5)
RED = mat('dragon_red', '#e5352c', rough=0.5)
BELLY = mat('dragon_belly', '#ffd03c', rough=0.55)
WING = mat('dragon_wing', '#ff7f24', rough=0.6)
WHITE = mat('eye_white', '#ffffff', rough=0.35)
DARK = mat('eye_dark', '#1f1a26', rough=0.3)

B = []
# ---------------------------------------------------------------- torso with yellow belly plates
TC = V(0, 0.0, 0.0)
torso = ell(TC, (0.27, 0.47, 0.26), seg=14, rings=10, material=RED,
            shape=lambda n: Vector((n.x * (1 - 0.18 * n.y), n.y, n.z * (1 - 0.15 * n.y))))
iso_paint(torso, lambda p: p.z + 0.075 + 0.05 * max(0.0, p.y) - 0.1 * max(0.0, -p.y - 0.15), BELLY)
B.append(torso)
# plate seams: thin red arcs across the yellow belly, laid on the surface with ray casts
from mathutils.bvhtree import BVHTree
_bvh = BVHTree.FromObject(torso, bpy.context.evaluated_depsgraph_get())
for y in (-0.22, -0.06, 0.1, 0.25):
    arc = []
    for k in range(7):
        a = -1.15 + 2.3 * k / 6
        o_ = V(0, y, 0.0); d_ = V(math.sin(a), 0, -math.cos(a))
        hit = _bvh.ray_cast(o_ + d_ * 0.6, -d_)
        if hit[0] is not None and hit[0].z < -0.03:
            arc.append(hit[0] + hit[1] * 0.004)
    if len(arc) > 2:
        B.append(tube(arc, 0.011, seg=4, material=RED, cap=False, flat=0.5))
# neck rising to the head
NK = bezier(V(0, -0.32, 0.06), V(0, -0.52, 0.12), V(0, -0.62, 0.24), V(0, -0.7, 0.33), n=5)
neck = tube(NK, [0.18, 0.165, 0.15, 0.14, 0.135, 0.13], seg=10, material=RED, cap=False)
def curve_field(pts, radii, down, frac):
    dense, dr = [], []
    for i in range(len(pts) - 1):
        for k in range(6):
            t = k / 6
            dense.append(pts[i].lerp(pts[i + 1], t)); dr.append(radii[i] * (1 - t) + radii[i + 1] * t)
    dense.append(pts[-1]); dr.append(radii[-1])
    def f(p):
        i = min(range(len(dense)), key=lambda j: (dense[j] - p).length_squared)
        j2 = min(i + 1, len(dense) - 1); j1 = max(i - 1, 0)
        t = (dense[j2] - dense[j1]).normalized()
        return frac * dr[i] - (p - dense[i]).dot(down(t))
    return f
iso_paint(neck, curve_field(NK, [0.18, 0.165, 0.15, 0.14, 0.135, 0.13], lambda t: V(1, 0, 0).cross(t).normalized(), 0.3), BELLY)
B.append(neck)

# ---------------------------------------------------------------- head: round skull, snout, big eyes, horns, smile
HC = V(0, -0.78, 0.4)
B.append(ell(HC, (0.21, 0.21, 0.19), seg=12, rings=8, material=RED))
SN = V(0, -0.97, 0.34)
B.append(ell(SN, (0.15, 0.17, 0.115), seg=10, rings=7, material=RED,
             shape=lambda n: Vector((n.x * (1 + 0.15 * n.y), n.y, n.z * (1 + 0.1 * n.y)))))
# lower jaw / chin in belly yellow
B.append(ell(SN + V(0, 0.02, -0.07), (0.12, 0.14, 0.055), seg=9, rings=5, material=BELLY))
for sx in (-1, 1):
    B.append(ell(SN + V(sx * 0.055, -0.15, 0.05), (0.022, 0.015, 0.015), seg=6, rings=3, material=DARK))   # nostrils
    B += eye_lo(HC + V(sx * 0.105, -0.15, 0.06), d=(sx * 0.45, -1, 0.15), r=0.085, white=WHITE, black=DARK, depth=0.6,
                tall=1.15, pupil=0.6, look=(-sx * 0.15, 0, 0.1), seg=9)
    # brow ridge
    B.append(ell(HC + V(sx * 0.1, -0.14, 0.15), (0.075, 0.04, 0.025), seg=6, rings=4, material=RED, rot=(0, sx * -15, sx * -25)))
    # horns sweeping back
    hp = bezier(HC + V(sx * 0.1, 0.0, 0.15), HC + V(sx * 0.14, 0.1, 0.27), HC + V(sx * 0.16, 0.24, 0.3), n=4)
    B.append(tube(hp, [0.045, 0.036, 0.026, 0.015, 0.003], seg=6, material=BELLY))
    # ear frills
    B.append(spike(HC + V(sx * 0.18, 0.06, 0.04), (sx * 1, 0.6, 0.25), r=0.05, h=0.15, seg=4, material=WING))
    # cheeks
# smile line + tiny fangs
sm = [SN + V(0.13 * math.sin(t), -0.15 * math.cos(t) + 0.02, -0.035 + 0.02 * abs(math.sin(t))) for t in
      [(-1.1 + 2.2 * k / 6) for k in range(7)]]
B.append(tube(sm, 0.009, seg=4, material=DARK))
for sx in (-1, 1):
    B.append(spike(sm[3] + V(sx * 0.045, 0.005, 0.0), (0, -0.2, -1), r=0.014, h=0.035, seg=4, material=WHITE))
# small crest spikes on the head
for k in range(2):
    B.append(spike(HC + V(0, 0.04 + 0.1 * k, 0.17 - 0.03 * k), (0, 0.5, 1), r=0.04, h=0.09, seg=4, material=BELLY))

# ---------------------------------------------------------------- back spines (head -> tail)
for k in range(5):
    t = k / 4
    y = -0.5 + t * 0.85
    z = 0.21 + 0.1 * (1 - abs(2 * t - 0.6)) - 0.05 * t
    if k == 0:
        z = 0.27
    B.append(spike(V(0, y, z - 0.03), (0, 0.45, 1), r=0.055 - 0.01 * t, h=0.13 - 0.03 * t, seg=4, material=BELLY))

# ---------------------------------------------------------------- tucked legs with little claws
for sx in (-1, 1):
    # front arms
    a0 = V(sx * 0.15, -0.28, -0.08)
    a1 = V(sx * 0.2, -0.35, -0.2)
    a2 = V(sx * 0.15, -0.45, -0.22)
    B.append(tube([a0, a1, a2], [0.07, 0.055, 0.045], seg=7, material=RED))
    for k in (-1, 0, 1):
        B.append(spike(a2 + V(k * 0.025, -0.02, -0.0), (k * 0.3, -1, -0.4), r=0.014, h=0.04, seg=4, material=WHITE))
    # hind legs: thigh + foot trailing back
    B.append(ell(V(sx * 0.19, 0.2, -0.1), (0.11, 0.17, 0.13), seg=8, rings=6, material=RED, rot=(25, 0, 0)))
    f0 = V(sx * 0.2, 0.25, -0.2)
    f1 = V(sx * 0.19, 0.43, -0.27)
    B.append(tube([f0, f1], [0.06, 0.045], seg=7, material=RED))
    B.append(ell(f1 + V(0, 0.05, -0.0), (0.05, 0.08, 0.03), seg=6, rings=4, material=RED))
    for k in (-1, 1):
        B.append(spike(f1 + V(k * 0.025, 0.11, 0.0), (k * 0.2, 1, -0.2), r=0.014, h=0.04, seg=4, material=WHITE))

# ---------------------------------------------------------------- long tail curving behind (S-curve), spade tip
TP = bezier(V(0, 0.36, 0.02), V(0, 0.75, 0.0), V(0.42, 0.85, 0.0), V(0.36, 1.25, 0.1), n=7)
TP += bezier(V(0.36, 1.25, 0.1), V(0.32, 1.4, 0.14), V(0.15, 1.45, 0.2), V(0.08, 1.4, 0.24), n=3)[1:]
nT = len(TP)
rad = [0.17 * (1 - i / nT) ** 0.9 + 0.015 for i in range(nT)]
tail = tube(TP, rad, seg=9, material=RED, cap=False)
iso_paint(tail, curve_field(TP, rad, lambda t: (V(0, 0, -1) - t * t.z).normalized(), 0.35), BELLY)
B.append(tail)
# spade tip (flat diamond, yellow)
tipd = (TP[-1] - TP[-2]).normalized()
sp = prism([(0.0, -0.02), (0.07, 0.06), (0.03, 0.17), (0.0, 0.2), (-0.03, 0.17), (-0.07, 0.06)], -0.018, 0.018, material=BELLY)
xf(sp, Matrix.Translation(TP[-1]) @ Vector((0, 1, 0)).rotation_difference(tipd).to_matrix().to_4x4())
B.append(sp)
# small tail spines
for i in (1, 3, 5):
    p = TP[i]
    B.append(spike(p + V(0, 0, rad[i] * 0.8), (0, 0.4, 1), r=0.04 - 0.005 * i, h=0.09 - 0.008 * i, seg=4, material=BELLY))

body = part(B, 'body', (0, 0, 0), angle=55)

# ---------------------------------------------------------------- wings: bat wings, pivot at the shoulder, spread along +-X
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.17, -0.14, 0.17)
    EL = V(sx * 0.5, -0.2, 0.33)
    WR = V(sx * 0.82, -0.1, 0.4)
    tips = [V(sx * 1.38, 0.08, 0.36), V(sx * 1.22, 0.42, 0.26), V(sx * 0.9, 0.6, 0.2), V(sx * 0.5, 0.5, 0.16)]
    W = [tube([SH, EL, WR], [0.06, 0.045, 0.04], seg=6, material=RED)]
    W.append(ell(WR, (0.045, 0.045, 0.045), seg=6, rings=4, material=RED))
    W.append(spike(WR + V(0, -0.02, 0.02), (sx * 0.4, -1, 0.4), r=0.025, h=0.08, seg=4, material=WHITE))   # thumb claw
    for t in tips[:3]:
        mid = WR.lerp(t, 0.5) + V(0, 0, 0.03)
        W.append(tube([WR, mid, t], [0.028, 0.022, 0.008], seg=5, material=RED))
    # membrane: fan from the wrist with a scalloped trailing edge, slightly arched
    pts = [SH + V(sx * 0.02, 0.02, 0.0), EL, WR]
    for i, t in enumerate(tips):
        pts.append(t)
        if i < len(tips) - 1:
            pts.append(t.lerp(tips[i + 1], 0.5).lerp(WR, 0.2) + V(0, 0, 0.02))
    pts.append(SH + V(sx * 0.12, 0.3, -0.02))
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in pts]
    cen = sum(pts, Vector()) / len(pts) + V(0, 0, 0.05)
    c = bm.verts.new(cen)
    for i in range(len(vs) - 1):
        bm.faces.new((c, vs[i], vs[i + 1]))
    bm.faces.new((c, vs[-1], vs[0]))
    # subdivide once for a smooth arch
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    for v in bm.verts:
        d = abs(v.co.x - SH.x)
        v.co.z += 0.05 * math.sin(min(d / 1.2, 1.0) * math.pi)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mem = _obj(bm, WING, smooth=True)
    m = mem.modifiers.new('sol', 'SOLIDIFY'); m.thickness = 0.016; m.offset = 0.0
    bpy.context.view_layer.objects.active = mem; bpy.ops.object.select_all(action='DESELECT'); mem.select_set(True)
    bpy.ops.object.modifier_apply(modifier=m.name)
    W.append(mem)
    for o in W:
        xf(o, Matrix.Translation(SH) @ Matrix.Diagonal((1.2, 1.15, 1.2, 1)) @ Matrix.Translation(-SH))
    part(W, f'wing_{side}', SH, angle=70)

std_view()
print_ext()
if '--close' in sys.argv:
    closeup('dragon_flyer', (0, -0.1, 0.0), 3.2, d=(0.8, -0.6, -0.5))
    sys.exit()
notes = ('Small friendly red dragon ~2.5 m long (nose y=-1.14 .. tail tip y=+1.6), wingspan ~2.8 m, origin (0,0,0) = body '
         'CENTRE, nose to -Y, left = +X. Parts/pivots: body (origin 0,0,0: red body with yellow belly plates, neck, head with big '
         'eyes, horns, crest, smile, tucked legs, back spines, long S-curved tail with a yellow spade); wing_l (+X) / wing_r (-X) '
         '(bat wings spread horizontally, slight arch; pivot at the shoulder (+-0.17,-0.14,0.17); the game flaps them around Y). '
         'Materials: dragon_red, dragon_belly, dragon_wing, eye_white, eye_dark.')
finish('castle', 'dragon_flyer', kind='char', footprint=1.3, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('dragon_flyer', dirs={'front': (0, -1, 0.2), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.5), 'top': (0.2, -0.2, 1)})
    montage('dragon_flyer', keys=('front', 'side', 'back', 'top'))
