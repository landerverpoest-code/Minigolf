import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
V = Vector

# ---------- materialen ----------
shell = mat('shell', '#4a2c18', rough=0.32, metal=0.15)
amber = mat('amber', '#eb951e', rough=0.4)
sting_m = mat('sting', '#ffc21a', rough=0.25, metal=0.6)
white = mat('eye_white', '#ffffff', rough=0.3)
dark = mat('pupil', '#120a06', rough=0.2)


def part(objs, name, pivot):
    """Join objs into one named part with its origin at pivot (rotation stays zero)."""
    o = join(objs if isinstance(objs, list) else [objs], name)
    bake(o); o.data.name = name
    origin_to(o, pivot)
    return o


def ell(c, s, material, seg=12, rings=7, rot=(0, 0, 0)):
    o = sphere(1.0, loc=(0, 0, 0), seg=seg, rings=rings, material=material, scale=s)
    T(o, rot=rot, loc=c)
    return o


def stube(pts, rs, seg=6, material=None, n=2):
    return tube(smooth_path(pts, n), r=interp(rs, n), seg=seg, material=material, smooth=True)


def loft(rings, seg=16, mats=(None, None), name='loft'):
    """Romp langs Y. rings = [(y, w, h_top, h_bot, zc, accent)], w/h = halve breedte/hoogte.
    accent=1 -> vlakken tussen deze ring en de volgende krijgen materiaal 1. Eerste/laatste met w=0 = pool."""
    bm = bmesh.new(); R = []
    for (y, w, ht, hb, zc, acc) in rings:
        if w <= 1e-6:
            R.append([bm.verts.new((0, y, zc))]); continue
        ring = []
        for i in range(seg):
            a = TAU * i / seg
            c, s = math.cos(a), math.sin(a)
            # iets 'superellips' -> vollere, chunky doorsnede
            cx = math.copysign(abs(c) ** 0.8, c); sz = math.copysign(abs(s) ** 0.9, s)
            ring.append(bm.verts.new((w * cx, y, zc + (ht if s > 0 else hb) * sz)))
        R.append(ring)
    for k, (a, b) in enumerate(zip(R, R[1:])):
        acc = rings[k][5]
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                f = bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                f = bm.faces.new((a[j], a[i], b[0]))
            else:
                f = bm.faces.new((a[i], b[i], b[j], a[j]))
            f.material_index = acc
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = link_bm(bm, name)
    o.data.materials.append(mats[0]); o.data.materials.append(mats[1])
    return o


B = []
# ---------- romp: kop + 5 dakpanplaten + staartwortel, 1 doorlopend lichaam ----------
R = [(-0.86, 0, 0, 0, 0.29, 0),
     (-0.83, 0.13, 0.08, 0.06, 0.29, 0),
     (-0.76, 0.25, 0.15, 0.1, 0.31, 0),
     (-0.64, 0.33, 0.2, 0.13, 0.33, 0),
     (-0.48, 0.37, 0.215, 0.14, 0.34, 0),
     (-0.36, 0.37, 0.2, 0.13, 0.34, 0),
     (-0.31, 0.34, 0.17, 0.11, 0.34, 1),      # amber naad
     (-0.28, 0.33, 0.15, 0.1, 0.34, 0)]
plates = [(-0.26, 0.20, 0.42, 0.2), (-0.04, 0.22, 0.43, 0.2), (0.2, 0.22, 0.41, 0.195), (0.44, 0.2, 0.36, 0.18), (0.66, 0.17, 0.29, 0.165)]
for (y0, L, w, h) in plates:
    zc = 0.34 + 0.12 * max(0, (y0 - 0.2) / 0.5)
    R += [(y0 + 0.02, w * 0.93, h * 0.85, h * 0.6, zc, 0),
          (y0 + L * 0.45, w, h, h * 0.68, zc + 0.005, 0),
          (y0 + L * 0.88, w * 0.97, h * 1.08, h * 0.66, zc + 0.02, 0),
          (y0 + L * 1.0, w * 0.8, h * 0.74, h * 0.55, zc + 0.01, 1)]
R += [(0.86, 0.17, 0.15, 0.12, 0.43, 0), (0.93, 0.15, 0.14, 0.12, 0.45, 1), (0.97, 0.13, 0.12, 0.11, 0.45, 1), (0.985, 0, 0, 0, 0.45, 0)]
torso = loft(R, seg=14, mats=(shell, amber), name='torso')
set_mat(torso, amber, lambda c, n: n.z < -0.55)       # amber buik
B.append(torso)

# ---------- ogen (boos-schattig): grote bollen, schuin afgesneden + dikke wenkbrauw ----------
def cut(o, co, no):
    bm = bmesh.new(); bm.from_mesh(o.data)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no, clear_outer=True)
    edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(o.data); bm.free()
    return o


for sx in (-1, 1):
    ec = V((sx * 0.15, -0.6, 0.54))
    w = sphere(1.0, seg=12, rings=8, material=white, scale=(0.15, 0.13, 0.168))
    no = V((-sx * 0.5, -0.25, 1.0)).normalized()               # snijvlak: binnenkant laag (boze blik)
    cut(w, no * 0.08, no)
    T(w, loc=ec); B.append(w)
    B.append(ell(ec + V((-sx * 0.028, -0.095, -0.035)), (0.085, 0.05, 0.095), dark, seg=8, rings=6))
    B.append(ell(ec + V((-sx * 0.0, -0.14, 0.0)), (0.027, 0.012, 0.029), white, seg=6, rings=4))
    br = box((0.22, 0.09, 0.055), material=shell, bevel=0.02)
    q = V((0, 0, 1)).rotation_difference(no)
    T(br, rot=q.to_euler(), loc=ec + no * 0.095)
    B.append(br)
# kaakjes (chelicerae)
for sx in (-1, 1):
    B.append(stube([(sx * 0.07, -0.78, 0.25), (sx * 0.065, -0.88, 0.21), (sx * 0.035, -0.91, 0.15)], [0.045, 0.035, 0.0], seg=5, material=amber, n=1))
body = part(B, 'body', (0, 0, 0))
shade_smooth(body, 50)

# ---------- poten ----------
leg_y = [-0.3, -0.06, 0.18, 0.42]
splay = [-0.6, -0.2, 0.2, 0.55]
for side, sx in (('l', 1), ('r', -1)):          # links van het dier = +X (voorkant -Y)
    for k in range(4):
        piv = V((sx * 0.3, leg_y[k], 0.3))
        a = splay[k]
        d = V((sx * math.cos(a), math.sin(a), 0))
        pts = [piv - d * 0.08, piv + d * 0.14 + V((0, 0, 0.13)), piv + d * 0.3 + V((0, 0, 0.2)),
               piv + d * 0.5 + V((0, 0, 0.08)), piv + d * 0.62 + V((0, 0, -0.18))]
        L = [tube(pts, r=[0.065, 0.062, 0.055, 0.044, 0.036], seg=5, material=shell, smooth=True)]
        L.append(sphere(0.062, loc=pts[2], seg=6, rings=4, material=amber))
        foot = piv + d * 0.66 + V((0, 0, -0.3))
        L.append(tube([pts[4], foot], r=[0.036, 0.0], seg=5, material=amber, cap=False))
        o = part(L, f'leg_{side}{k + 1}', piv)
        shade_smooth(o, 55)

# ---------- armen met scharen ----------
for side, sx in (('l', 1), ('r', -1)):
    sh = V((sx * 0.25, -0.66, 0.28))                 # schouder
    el = V((sx * 0.56, -0.84, 0.31))                 # elleboog
    wr = V((sx * 0.52, -1.1, 0.32))                  # pols
    A = []
    A.append(tube([sh - V((sx * 0.05, -0.03, 0)), sh.lerp(el, 0.5) + V((0, 0, 0.03)), el], r=[0.075, 0.075, 0.068], seg=6, material=shell, smooth=True))
    A.append(sphere(0.08, loc=el, seg=7, rings=5, material=amber))
    A.append(tube([el, el.lerp(wr, 0.5), wr], r=[0.068, 0.074, 0.08], seg=6, material=shell, smooth=True))
    # dikke schaarhand
    hc = V((sx * 0.5, -1.27, 0.32))
    A.append(ell(hc, (0.165, 0.2, 0.135), shell, seg=11, rings=7))
    A.append(ell(hc + V((sx * 0.06, -0.01, 0.105)), (0.055, 0.1, 0.03), amber, seg=6, rings=4))   # amber vlek
    # vaste (onderste) vinger
    f0 = V((sx * 0.47, -1.4, 0.28))
    A.append(stube([f0, f0 + V((-sx * 0.02, -0.12, -0.02)), f0 + V((-sx * 0.06, -0.24, 0.01)), f0 + V((-sx * 0.085, -0.31, 0.065))],
                   [0.078, 0.06, 0.04, 0.0], seg=6, material=shell, n=1))
    for t in range(3):   # tandjes (amber)
        A.append(cone(0.022, 0.055, loc=f0 + V((-sx * 0.022 * t, -0.07 - t * 0.065, 0.045)), verts=5, material=amber))
    arm = part(A, f'arm_{side}', sh)
    shade_smooth(arm, 55)
    # beweegbare bovenste vinger (scharnier bovenaan de hand)
    hg = V((sx * 0.48, -1.37, 0.37))
    J = [sphere(0.062, loc=hg, seg=6, rings=4, material=shell)]
    J.append(stube([hg, hg + V((-sx * 0.02, -0.12, 0.035)), hg + V((-sx * 0.06, -0.23, 0.005)), hg + V((-sx * 0.085, -0.3, -0.06))],
                   [0.066, 0.055, 0.036, 0.0], seg=6, material=shell, n=1))
    for t in range(2):
        J.append(cone(0.02, 0.05, loc=hg + V((-sx * 0.02 * t, -0.09 - t * 0.07, -0.035)), rot=(math.pi, 0, 0), verts=5, material=amber))
    jaw = part(J, f'jaw_{side}', hg)
    shade_smooth(jaw, 55)
    jaw.parent = arm
    jaw.matrix_parent_inverse = Matrix.Identity(4)
    jaw.location = hg - sh

# ---------- staartsegment (1x, game kopieert het 7x) ----------
# lathe langs Z: amber kraagje (smal) onderaan, bolle schaal, afgerond eind; daarna lange as -> Blender Y
seg_o = lathe([(0.0, -0.16), (0.075, -0.158), (0.1, -0.13), (0.112, -0.105), (0.15, -0.07), (0.158, 0.0), (0.148, 0.07),
               (0.12, 0.12), (0.07, 0.152), (0.0, 0.16)], seg=10, material=shell, smooth=True)
set_mat(seg_o, amber, lambda c, n: c.z < -0.1)
crest = ell((0, 0.135, 0.0), (0.03, 0.04, 0.1), amber, seg=6, rings=5)     # rugkammetje
seg_o = join([seg_o, crest], 'tail_seg')
T(seg_o, rot=(math.pi / 2, 0, 0))          # lange as langs Blender Y (three.js Z); kraag naar -Y, kam naar +Z
seg_pos = V((0, 1.12, 0.62))
T(seg_o, loc=seg_pos)
tail_seg = part([seg_o], 'tail_seg', seg_pos)
shade_smooth(tail_seg, 55)

# ---------- angel (oorsprong aan de basis, wijst naar -Z) ----------
S = [sphere(0.135, loc=(0, 0, -0.12), seg=9, rings=6, material=sting_m, scale=(1, 1, 1.1))]
hook = smooth_path([(0, 0, -0.16), (0, -0.015, -0.27), (0, -0.06, -0.35), (0, -0.13, -0.41)], 2)
S.append(tube(hook, r=interp([0.085, 0.055, 0.03, 0.0], 2), seg=6, material=sting_m, smooth=True))
S.append(lathe([(0.075, 0.0), (0.105, -0.015), (0.105, -0.045), (0.08, -0.06)], seg=9, material=shell, cap_top=True, cap_bot=False, smooth=True))
sting = part(S, 'sting', (0, 0, 0))
shade_smooth(sting, 55)
b0, b1, b2 = V((0, 0.95, 0.45)), V((0, 1.62, 2.05)), V((0, 0.45, 1.8))     # staartcurve (preview)
sting.location = b2


def bez(u):
    return b0 * (1 - u) ** 2 + b1 * 2 * (1 - u) * u + b2 * u * u


report()
notes = ('parts (pivot, Blender coords, front -Y, l = animal own left = +X): '
         'body (origin 0,0,0 = body centre on ground; head front y=-0.86, tail root ends at y=+0.98 z=0.45); '
         'leg_l1..leg_l4 / leg_r1..leg_r4 (body side x=+/-0.30 z=0.30, y=-0.30,-0.06,0.18,0.42; feet on z=0); '
         'arm_l / arm_r (shoulder x=+/-0.25 y=-0.66 z=0.28, pincer forward -Y to y=-1.7); '
         'jaw_l / jaw_r (movable upper pincer finger, parented to its arm, hinge at x=+/-0.48 y=-1.37 z=0.37; three.js rotation.x<0 opens it upward); '
         'tail_seg (centred on its origin, 0.32 long along its local three.js Z with the narrow amber collar toward three.js +Z (Blender -Y) and a small crest on top (+Y), 0.31 thick; placed behind the tail root); '
         'sting (origin at its base, points down -Y in three.js, 0.42 long, hook curls forward; material sting; placed at the resting tail tip). '
         'Materials: shell, amber, sting, eye_white, pupil.')
finish('chars', 'scorpion', kind='char', footprint=0.9, grounded=False, notes=notes, preview=False)

# ---------- preview: volledige staart zoals de game hem opbouwt (alleen voor de render) ----------
for i in range(7):
    u = (i + 1) / 8
    p = bez(u); t = (bez(u + 0.01) - bez(u - 0.01)).normalized()
    c = dup(tail_seg); bake(c)
    c.data.transform(Matrix.Translation(-tail_seg.location))
    s = 1.0 - i * 0.035
    q = V((0, -1, 0)).rotation_difference(-t)      # kraag (lokaal -Y) naar het lichaam toe
    c.data.transform(Matrix.Translation(p) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
tail_seg.hide_render = True
st = dup(sting); bake(st)
d = (b2 - b1 + V((0, 0, -0.6))).normalized()
q = V((0, 0, -1)).rotation_difference(d)
st.data.transform(Matrix.Translation(-b2)); st.data.transform(Matrix.Translation(b2) @ q.to_matrix().to_4x4())
sting.hide_render = True
render_preview(f'{ROOT}/previews/chars/scorpion.png')
if os.environ.get('VIEWS'):
    sys.path.insert(0, '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad')
    from views import views
    views('scorpion')
