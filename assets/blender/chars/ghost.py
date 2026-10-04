import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
V = Vector

# ---------- materialen ----------
ghost = mat('ghost', '#eef6ff', rough=0.45, emit='#a8dcff', emit_strength=0.25)
eye_m = mat('eye', '#1d1433', rough=0.2)
shine = mat('shine', '#ffffff', rough=0.2, emit='#ffffff', emit_strength=0.6)
blush = mat('blush', '#ff8fb8', rough=0.6)
mouth_m = mat('mouth', '#3d0f2c', rough=0.4)


def part(objs, name, pivot):
    o = join(objs if isinstance(objs, list) else [objs], name)
    bake(o); o.data.name = name
    origin_to(o, pivot)
    return o


# ---------- laken (lathe met golvende zoom, plooien en dikke omgeslagen rand) ----------
SEG = 30
WAVES = 5
HEM = 0.15


def hem_z(a):
    return HEM + 0.2 * (0.5 - 0.5 * math.cos(WAVES * a + math.pi / 2))       # punten (laagst) bij cos=1


prof = [(0.555 * math.cos(math.radians(t)), 1.35 + 0.55 * math.sin(math.radians(t))) for t in (90, 72, 54, 36, 18)]
prof += [(0.56, 1.35), (0.565, 1.17), (0.578, 0.98), (0.6, 0.78), (0.635, 0.58), (0.665, 0.42), (0.69, None)]
prof[0] = (0.0, 1.9)
bm = bmesh.new(); rings = []
for (r, z) in prof:
    if r == 0:
        rings.append([bm.verts.new((0, 0, z))]); continue
    ring = []
    for i in range(SEG):
        a = TAU * i / SEG - math.pi / 2          # een punt recht vooraan (-Y)
        if z is None:
            zz = hem_z(a); t = 1.0
        else:
            t = max(0.0, (1.0 - z) / (1.0 - 0.4)) if z < 1.0 else 0.0
            zz = z
        f = 1 + 0.07 * math.cos(WAVES * a + math.pi / 2) * t ** 1.5           # plooien die naar de punten uitwaaieren
        ring.append(bm.verts.new((r * f * math.cos(a), r * f * math.sin(a), zz)))
    rings.append(ring)
# omgeslagen rand: binnenring net boven de zoom, dan binnenkant omhoog naar een koepeltje
inner = []
for i, v in enumerate(rings[-1]):
    a = TAU * i / SEG - math.pi / 2
    inner.append(bm.verts.new((v.co.x * 0.93, v.co.y * 0.93, v.co.z + 0.03)))
rings.append(inner)
inner2 = [bm.verts.new((v.co.x * 0.86, v.co.y * 0.86, v.co.z + 0.12)) for v in inner]
rings.append(inner2)
rings.append([bm.verts.new((0, 0, 0.62))])
for A, Bv in zip(rings, rings[1:]):
    for i in range(SEG):
        j = (i + 1) % SEG
        if len(A) == 1:
            bm.faces.new((A[0], Bv[i], Bv[j]))
        elif len(Bv) == 1:
            bm.faces.new((A[j], A[i], Bv[0]))
        else:
            bm.faces.new((A[i], Bv[i], Bv[j], A[j]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
sheet = link_bm(bm, 'body', ghost)
# heel licht naar voren leunende kop (vriendelijker silhouet)
deform(sheet, lambda v: V((v.x, v.y - 0.06 * max(0, v.z - 1.0) ** 2, v.z)))
body = part([sheet], 'body', (0, 0, 0))
shade_smooth(body, 70)

# ---------- armpjes (ronde laken-wantjes), oorsprong in de schouder ----------
for side, sx in (('l', 1), ('r', -1)):      # links van het spook = +X (voorkant -Y)
    sh = V((sx * 0.51, -0.02, 1.12))
    pts = [sh - V((sx * 0.1, 0, 0.0)), sh + V((sx * 0.08, -0.03, 0.02)), sh + V((sx * 0.2, -0.08, 0.0)),
           sh + V((sx * 0.29, -0.13, -0.06)), sh + V((sx * 0.34, -0.16, -0.13)), sh + V((sx * 0.355, -0.17, -0.17))]
    arm = tube(smooth_path(pts, 2), r=interp([0.12, 0.125, 0.12, 0.11, 0.08, 0.0], 2), seg=10, material=ghost, smooth=True)
    o = part([arm], f'arm_{side}', sh)
    shade_smooth(o, 70)

# ---------- gezicht: grote donkere ovale ogen met glimlichtjes + blosjes ----------
F = []
def on_body(build, d, z, sink, spin=0.0):
    o = build()
    loc, nor = surface_hit(body_ref, d, center=(0, 0, z))
    q = V((0, 0, 1)).rotation_difference(nor)
    T(o, rot=(0, 0, spin))
    T(o, rot=q.to_euler(), loc=loc - nor * sink)
    return o, loc, nor

body_ref = dup(body); bake(body_ref)
for sx in (-1, 1):
    d = V((sx * 0.4, -1, 0))
    e, loc, nor = on_body(lambda: sphere(1.0, seg=12, rings=9, material=eye_m, scale=(0.11, 0.16, 0.035)), d, 1.44, 0.012)
    F.append(e)
    up = V((0, 0, 1)); tx = nor.cross(up).normalized()     # raaklijn (naar -sx kant)
    F.append(on_body(lambda: sphere(1.0, seg=8, rings=6, material=shine, scale=(0.04, 0.05, 0.02)), d, 1.44, 0)[0])
    # glimlicht linksboven in het oog, klein tweede lichtje rechtsonder
    hl = F.pop(); bake(hl)
    T(hl, loc=nor * 0.024 + V((0, 0, 0.058)) + tx * 0.034)
    F.append(hl)
    hl2 = on_body(lambda: sphere(1.0, seg=6, rings=4, material=shine, scale=(0.02, 0.02, 0.012)), d, 1.44, 0)[0]
    T(hl2, loc=nor * 0.02 + V((0, 0, -0.055)) - tx * 0.035)
    F.append(hl2)
    # blosje
    F.append(on_body(lambda: sphere(1.0, seg=10, rings=6, material=blush, scale=(0.095, 0.055, 0.02)), V((sx * 0.68, -1, 0)), 1.25, 0.008)[0])
fc = surface_hit(body_ref, (0, -1, 0), center=(0, 0, 1.38))[0]
face = part(F, 'face', fc)
shade_smooth(face, 70)

# ---------- open "O"-mondje, oorsprong in het midden ----------
M = []
mo, mloc, mnor = on_body(lambda: sphere(1.0, seg=12, rings=8, material=mouth_m, scale=(0.075, 0.095, 0.03)), V((0, -1, 0)), 1.21, 0.01)
M.append(mo)
tg, _, _ = on_body(lambda: sphere(1.0, seg=8, rings=5, material=blush, scale=(0.045, 0.028, 0.02)), V((0, -1, 0)), 1.21, 0.0)
T(tg, loc=mnor * 0.018 + V((0, 0, -0.055)))
M.append(tg)
mouth = part(M, 'mouth', mloc)
shade_smooth(mouth, 70)
bpy.data.objects.remove(body_ref)

report()
notes = ('parts (pivot, Blender coords, front -Y, l = ghost own left = +X): '
         'body (sheet, origin 0,0,0 on the ground under its centre; hem tips at z=0.15, top z=1.9, material ghost, closed mesh with turned-in hem); '
         'arm_l / arm_r (round sheet mittens, shoulder x=+/-0.51 y=-0.02 z=1.12, reach out/forward and droop; material ghost); '
         f'face (eyes + highlights + blush, origin on the body surface at the face centre {tuple(round(c, 3) for c in fc)}, sits ~0.015 in front of the sheet); '
         f'mouth (open dark O + tiny tongue, origin at its centre {tuple(round(c, 3) for c in mloc)}; scale it to open/close). '
         'Materials: ghost, eye, shine, blush, mouth.')
finish('chars', 'ghost', kind='char', footprint=0.55, grounded=False, notes=notes)
if os.environ.get('VIEWS'):
    sys.path.insert(0, '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad')
    from views import views
    views('ghost', dirs=((0, -1, 0.15), (1, 0.1, 0.1), (0.4, -1, -0.6)))
