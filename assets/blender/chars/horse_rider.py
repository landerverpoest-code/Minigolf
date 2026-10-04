import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gkit import *
from gkit import _obj

# ---------------------------------------------------------------- materials (6)
HORSE = mat('horse', '#a8683c', rough=0.55)
DARK = mat('horse_dark', '#2a1d1a', rough=0.5)          # mane, tail, hooves, pupils, visor slit
COAT = mat('coat', '#d63238', rough=0.7)                # recoloured red/blue by the game
ARMOR = mat('armor', '#c3ccd8', rough=0.3, metal=0.75)
WHITE = mat('white', '#f7f4ee', rough=0.45)             # eye whites, socks, blaze, lance stripes, emblems
GOLD = mat('gold', '#ffc93a', rough=0.3, metal=0.85)

# ================================================================= BODY (horse torso + caparison + knight)
B = []
KEEP = []          # crisp pieces that must not be decimated (cloth, emblems, shield, eyes)


def dec_part(objs, keep, name, pivot, ratio):
    soft = [o for o in objs if o not in keep]
    for o in soft:
        clean(o)
    t = join(soft, name + '_soft')
    decimate(t, ratio)
    return apart([o for o in objs if o in keep] + [t], name, pivot)


TCZ = 1.0
# horse belly (only the underside shows below the cloth)
B.append(ell(V(0, 0.05, 0.86), (0.27, 0.52, 0.2), seg=8, rings=5, material=HORSE))

# caparison: cloth draped over the horse, scalloped hem
RX, RY, CY, ZT, ZH = 0.335, 0.64, 0.05, 1.33, 0.6
bm = bmesh.new()
NA = 16
zs = [ZT - 0.0001, 1.28, 1.17, 1.02, 0.84, ZH + 0.1, ZH]
rings = []
for z in zs:
    t = min(1.0, max(0.0, (z - TCZ) / (ZT - TCZ)))
    s = math.sqrt(max(0.0, 1 - t * t)) if z > TCZ else 1.0
    s = max(s, 0.05)
    flare = max(0.0, 0.9 - z) * 0.18
    row = []
    for i in range(NA):
        a = TAU * i / NA
        w = 0.0
        if z <= ZH + 0.1:
            w = 0.05 * math.cos(a * 8)          # scallops
        row.append(bm.verts.new((math.cos(a) * (RX * s + flare), CY + math.sin(a) * (RY * s + flare * 1.3), z + w)))
    rings.append(row)
top = bm.verts.new((0, CY, ZT + 0.004))
for i in range(NA):
    bm.faces.new((top, rings[0][(i + 1) % NA], rings[0][i]))
for k, (a, b) in enumerate(zip(rings, rings[1:])):
    for i in range(NA):
        f = bm.faces.new((a[i], a[(i + 1) % NA], b[(i + 1) % NA], b[i]))
        f.material_index = 1 if k == len(rings) - 2 else 0          # gold hem band
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
cloth = _obj(bm, COAT)
cloth.data.materials.append(GOLD)
# make sure normals point outwards (open mesh -> check one face)
if cloth.data.polygons[len(cloth.data.polygons) // 2].normal.dot(Vector((*cloth.data.polygons[len(cloth.data.polygons) // 2].center.xy, 0)) - Vector((0, CY, 0))) < 0:
    for p in cloth.data.polygons:
        p.flip()
B.append(cloth); KEEP.append(cloth)
# white emblem (cross) on both flanks
for sx in (-1, 1):
    a, b = 0.045, 0.14
    crs = [(-a, b), (a, b), (a, a), (b, a), (b, -a), (a, -a), (a, -b), (-a, -b), (-a, -a), (-b, -a), (-b, a), (-a, a)]
    e = flat_shape(list(reversed(crs)), 0.02, WHITE)
    frame(e, V(sx * (RX + 0.0), 0.05, 0.95), V(sx, 0, 0))
    B.append(e); KEEP.append(e)
# saddle
B.append(ell(V(0, 0.12, 1.33), (0.25, 0.26, 0.06), seg=8, rings=4, material=DARK))

# ---- knight
KC = V(0, 0.12, 1.6)
kt = ell(KC, (0.21, 0.165, 0.25), seg=8, rings=6, p=0.9, material=ARMOR,
         shape=lambda n: Vector((n.x * (1 + 0.08 * n.z), n.y * (1 + 0.08 * max(0, -n.y)), n.z)))
iso_paint(kt, lambda p: p.z - 1.56 - 0.05 * abs(p.x) * 0, COAT)      # surcoat lower half
B.append(kt)
B.append(lathe([(0.215, 1.48), (0.225, 1.5), (0.225, 1.53), (0.215, 1.55)], seg=8, material=GOLD,
               M=Matrix.Translation((0, 0.12, 0)) @ Matrix.Diagonal((1.0, 0.82, 1, 1))))      # belt
B.append(ell(V(0, -0.04, 1.515), (0.05, 0.02, 0.04), seg=6, rings=4, material=GOLD))
# surcoat skirt flaps over the thighs
for sx in (-1, 1):
    B.append(ell(V(sx * 0.12, 0.02, 1.4), (0.13, 0.17, 0.09), seg=7, rings=4, material=COAT, rot=(0, sx * 25, 0)))
# pauldrons
for sx in (-1, 1):
    c = V(sx * 0.24, 0.12, 1.77)
    B.append(ell(c, (0.13, 0.14, 0.1), seg=8, rings=5, material=ARMOR, rot=(0, sx * 25, 0)))
# knight legs (outside the cloth, feet in gold stirrups)
for sx in (-1, 1):
    hp, kn, an = V(sx * 0.15, 0.12, 1.4), V(sx * 0.37, -0.06, 1.26), V(sx * 0.38, -0.01, 0.98)
    B.append(tube([hp, kn], [0.09, 0.075], seg=6, material=ARMOR))
    B.append(ell(kn, (0.075, 0.075, 0.075), seg=6, rings=4, material=ARMOR))
    B.append(tube([kn, an], [0.07, 0.06], seg=6, material=ARMOR))
    B.append(ell(an + V(0, -0.07, -0.02), (0.065, 0.12, 0.055), seg=6, rings=4, material=ARMOR))
# right arm (holding the lance, hand at H)
H = V(-0.3, -0.1, 1.44)
SR, ER = V(-0.25, 0.12, 1.72), V(-0.36, 0.12, 1.5)
B += [tube([SR, ER], [0.075, 0.068], seg=6, material=ARMOR), ell(ER, (0.07, 0.07, 0.07), seg=6, rings=4, material=ARMOR),
      tube([ER, H + V(0, 0.07, 0)], [0.066, 0.06], seg=6, material=ARMOR),
      tube([H + V(0, 0.09, 0), H + V(0, 0.04, 0)], [0.06, 0.078], seg=6, material=GOLD),
      ell(H, (0.07, 0.075, 0.07), seg=6, rings=4, material=ARMOR)]
# left arm (holding the reins) + shield in coat
SL, EL, HL = V(0.25, 0.12, 1.72), V(0.36, 0.1, 1.5), V(0.2, -0.12, 1.42)
B += [tube([SL, EL], [0.075, 0.068], seg=6, material=ARMOR), ell(EL, (0.07, 0.07, 0.07), seg=6, rings=4, material=ARMOR),
      tube([EL, HL], [0.066, 0.06], seg=6, material=ARMOR), ell(HL, (0.065, 0.07, 0.065), seg=6, rings=4, material=ARMOR)]
outline = []
W, Ht = 0.22, 0.54
for i in range(3):
    x = W - 2 * W * i / 2
    outline.append((x, 0.24 + 0.02 * (1 - (x / W) ** 2)))
for i in range(1, 6):
    t = i / 6; a = t * math.pi / 2
    outline.append((-W * math.cos(a) ** 0.8, 0.24 - Ht * math.sin(a) ** 1.6))
outline.append((0.0, 0.24 - Ht))
for i in range(5, 0, -1):
    t = i / 6; a = t * math.pi / 2
    outline.append((W * math.cos(a) ** 0.8, 0.24 - Ht * math.sin(a) ** 1.6))
SC, SD = V(0.47, -0.02, 1.58), V(1, -0.45, 0.05)
sh = flat_shape(outline, 0.04, COAT, curve=0.6)
B.append(frame(sh, SC, SD)); KEEP.append(sh)
rim = flat_shape([(x * 1.12, z * 1.07 + 0.01) for x, z in outline], 0.025, GOLD, curve=0.6)
xf(rim, Matrix.Translation((0, 0.018, 0)))
B.append(frame(rim, SC, SD)); KEEP.append(rim)
# white chevron + gold boss on the shield
chev = [(-0.17, 0.0), (0.0, 0.12), (0.17, 0.0), (0.17, -0.08), (0.0, 0.04), (-0.17, -0.08)]
ch = flat_shape(chev, 0.012, WHITE, curve=0.6)
xf(ch, Matrix.Translation((0, -0.024, 0)))
B.append(frame(ch, SC, SD)); KEEP.append(ch)
B.append(frame(ell(V(0, -0.03, 0.12), (0.04, 0.025, 0.04), seg=6, rings=4, material=GOLD), SC, SD))
# helmet (great helm) with visor slit, gold cross band and team-coloured plume
HC = V(0, 0.1, 1.97)
helm = ell(HC, (0.165, 0.165, 0.175), seg=10, rings=7, p=0.78, material=ARMOR,
           shape=lambda n: Vector((n.x, n.y, n.z if n.z < 0.5 else 0.5 + (n.z - 0.5) * 0.7)))
B.append(helm)
B.append(lathe([(0.152, 1.785), (0.165, 1.81), (0.15, 1.83)], seg=10, material=ARMOR, M=Matrix.Translation((0, 0.1, 0))))
slit = []
for i in range(7):
    a = math.radians(-60 + 120 * i / 6)
    slit.append(HC + V(math.sin(a) * 0.168, -math.cos(a) * 0.168, 0.02))
B.append(tube(slit, 0.02, seg=4, flat=0.7, material=DARK))
for sx in (-1, 1):  # bright eyes peeking out of the visor
    B.append(ell(HC + V(sx * 0.06, -0.172, 0.022), (0.022, 0.012, 0.016), seg=6, rings=4, material=WHITE))
B.append(tube([HC + V(0, -0.173, -0.15), HC + V(0, -0.176, -0.0)], 0.018, seg=5, material=GOLD))
B.append(tube([HC + V(0, -0.175, 0.045), HC + V(0, -0.15, 0.13), HC + V(0, -0.05, 0.17), HC + V(0, 0.05, 0.17)],
              0.018, seg=5, material=GOLD))
B.append(lathe([(0.035, 2.11), (0.045, 2.14), (0.035, 2.17)], seg=8, material=GOLD, M=Matrix.Translation((0, 0.1, 0))))
for (dx, L, rr) in ((0.0, 1.0, 0.075), (0.06, 0.8, 0.06), (-0.06, 0.8, 0.06)):
    p0 = V(dx * 0.3, 0.1, 2.15)
    pts = bezier(p0, p0 + V(dx * 0.4, -0.12 * L, 0.16 * L), p0 + V(dx * 1.4, 0.3 * L, 0.2 * L), p0 + V(dx * 1.8, 0.5 * L, -0.06 * L), n=5)
    radii = [rr * (0.7 + 0.6 * math.sin(math.pi * min(1, (i / 5) * 1.1))) * (1 - (i / 5) ** 3 * 0.75) for i in range(6)]
    B.append(tube(pts, radii, seg=4, material=COAT, flat=0.6, round_end=True))
body = dec_part(B, KEEP, 'body', (0, 0, 0), 0.62)

# ================================================================= NECK + HEAD (pivot at the neck base)
NECK = V(0, -0.42, 1.15)
N = [tube(bezier(V(0, -0.36, 1.02), V(0, -0.6, 1.25), V(0, -0.72, 1.5), V(0, -0.8, 1.66), n=3),
          [0.21, 0.175, 0.14, 0.13], seg=9, material=HORSE)]
HD = V(0, -0.88, 1.66)
head = ell(V(0, 0, 0), (0.145, 0.27, 0.15), seg=10, rings=7, material=HORSE,
           shape=lambda n: Vector((n.x * (1 - 0.15 * max(0, -n.y)), n.y, n.z * (1 - 0.1 * max(0, -n.y)))))
xf(head, Matrix.Translation(HD + V(0, -0.06, 0)) @ rotm((32, 0, 0)))
N.append(head)
MZ = V(0, -1.08, 1.52)
muzzle = ell(MZ, (0.13, 0.13, 0.115), seg=9, rings=6, material=HORSE)
N.append(muzzle)
iso_paint(muzzle, lambda p: p.y + 1.13, WHITE)
# blaze (white stripe down the face)
TAN = math.tan(math.radians(32))
iso_paint(head, lambda p: abs(p.x) - 0.035 - max(0.0, -(p.y + 0.9)) * 0.25 + max(0.0, p.y + 0.86) * 9
          + max(0.0, -(p.z - (HD.z + (p.y - HD.y) * TAN))) * 9, WHITE)
for sx in (-1, 1):
    N.append(ell(MZ + V(sx * 0.055, -0.1, 0.03), (0.022, 0.015, 0.03), seg=5, rings=3, material=DARK, rot=(0, sx * 20, 0)))   # nostrils
# smile
sm = [MZ + V(math.sin(a) * 0.115, -math.cos(a) * 0.118, -0.05 + 0.03 * (a / 1.0) ** 2) for a in [(-1 + 2 * i / 6) * 0.95 for i in range(7)]]
N.append(tube(sm, 0.009, seg=4, material=DARK, round_end=True))
# big eyes
for sx in (-1, 1):
    ec = HD + V(sx * 0.11, -0.07, 0.08)
    EY = eye(ec, V(sx * 0.75, -1, 0.15), r=0.062, white=WHITE, black=DARK, depth=0.6, tall=1.2, pupil=0.66,
             look=(-sx * 0.3, 0, 0.0), seg=7, pseg=6)
    N += EY; KEEP += EY
    # lash/brow
    N.append(tube([ec + V(sx * 0.055, 0.02, 0.08), ec + V(sx * 0.01, -0.03, 0.09), ec + V(-sx * 0.035, -0.06, 0.075)],
                  0.012, seg=4, material=DARK, round_end=True))
    # ears
    eb = HD + V(sx * 0.085, 0.07, 0.17)
    N.append(tube([eb, eb + V(sx * 0.04, 0.01, 0.1), eb + V(sx * 0.05, 0.03, 0.18)], [0.05, 0.04, 0.006], seg=5,
                  flat=0.6, material=HORSE))
# bridle (gold)
for sx in (-1, 1):
    N.append(tube([HD + V(sx * 0.13, 0.08, 0.12), HD + V(sx * 0.14, -0.05, -0.04), MZ + V(sx * 0.12, 0.05, 0.0)], 0.014,
                  seg=4, material=GOLD))
N.append(tube([MZ + V(-0.12, 0.03, 0.06), MZ + V(0, -0.11, 0.08), MZ + V(0.12, 0.03, 0.06)], 0.014, seg=4, material=GOLD))
# mane: dark tufts along the top of the neck + forelock
mpts = bezier(V(0, -0.3, 1.27), V(0, -0.5, 1.45), V(0, -0.64, 1.72), V(0, -0.8, 1.85), n=4)
for i, p in enumerate(mpts):
    side = 1 if i % 2 else -1
    N.append(ell(p + V(side * 0.02, 0.04, 0.0), (0.065, 0.12, 0.075), seg=5, rings=4, material=DARK,
                 rot=(-35 - i * 6, 0, side * 10)))
N.append(tube(bezier(HD + V(0, 0.04, 0.17), HD + V(0, -0.08, 0.2), HD + V(0.03, -0.17, 0.12), n=3), [0.05, 0.045, 0.03, 0.008],
              seg=6, material=DARK, round_end=True))
neck = dec_part(N, KEEP, 'neck', NECK, 0.6)

# ================================================================= LEGS (pivot at shoulder / hip, hooves on z=0)
LEGS = {}
for name, sx, y0 in (('fl', 1, -0.33), ('fr', -1, -0.33), ('bl', 1, 0.4), ('br', -1, 0.4)):
    x = sx * 0.155
    P = V(x, y0, 0.92)
    back = name[0] == 'b'
    knee = V(x, y0 + (0.07 if back else -0.02), 0.46)
    fet = V(x, y0 + (0.0 if back else -0.02), 0.15)
    L = [tube([P + V(0, 0, -0.1), knee], [0.11, 0.085], seg=7, material=HORSE),
         ell(knee, (0.08, 0.085, 0.08), seg=6, rings=4, material=HORSE),
         tube([knee, fet], [0.07, 0.065], seg=7, material=HORSE)]
    iso_paint(L[2], lambda p: p.z - 0.27, WHITE)       # white socks
    L.append(ell(fet + V(0, 0.0, 0.0), (0.085, 0.09, 0.07), seg=7, rings=4, material=WHITE))   # fluffy fetlock
    L.append(lathe([(0.1, 0.0), (0.105, 0.02), (0.088, 0.115), (0.0, 0.118)], seg=7, material=DARK,
                   M=Matrix.Translation((x, fet.y - 0.02, 0))))                                   # hoof
    apart(L, f'leg_{name}', P)
    LEGS[name] = P

# ================================================================= TAIL (pivot at the root)
TR = V(0, 0.62, 1.17)
tp = bezier(TR, V(0, 0.82, 1.18), V(0, 0.9, 0.85), V(0, 0.86, 0.55), n=6)
Tl = [tube(tp, [0.07, 0.09, 0.11, 0.12, 0.11, 0.08, 0.02], seg=7, material=DARK, round_end=True)]
for k, (dx, dy) in enumerate(((0.05, 0.0), (-0.05, 0.02))):
    tp2 = bezier(TR + V(0, 0.05, 0), V(dx, 0.84 + dy, 1.12), V(dx * 2, 0.9 + dy, 0.8), V(dx * 2.2, 0.85 + dy, 0.6), n=5)
    Tl.append(tube(tp2, [0.05, 0.07, 0.08, 0.07, 0.04, 0.01], seg=5, material=DARK, round_end=True))
apart(Tl, 'tail', TR)

# ================================================================= LANCE (pivot at the knight's right hand, pointing -Y)
LA = []
Lb, Lf = 0.45, 2.55
# shaft: tapered pole along local +Z with slanted rings -> diagonal barber-pole stripes (coat / white)
SEG = 6
bm = bmesh.new()
zr = [(-Lb - 0.03, 0.0), (-Lb, 0.05), (0.3, 0.058)]
nb = 9
for k in range(nb + 1):
    z = 0.42 + (Lf - 0.12 - 0.42) * k / nb
    zr.append((z, 0.056 - 0.03 * (z - 0.42) / (Lf - 0.54)))
zr += [(Lf - 0.04, 0.03), (Lf + 0.02, 0.0)]
rws = []
for j, (z, r) in enumerate(zr):
    if r == 0:
        rws.append([bm.verts.new((0, 0, z))]); continue
    slant = 0.07 if 3 <= j <= 3 + nb else 0.0
    rws.append([bm.verts.new((r * math.cos(TAU * i / SEG), r * math.sin(TAU * i / SEG), z + slant * math.cos(TAU * i / SEG)))
                for i in range(SEG)])
for j, (a, b) in enumerate(zip(rws, rws[1:])):
    mi = 1 if (3 <= j < 3 + nb and j % 2 == 0) else 0
    if len(a) == 1:
        fs = [bm.faces.new((a[0], b[(i + 1) % SEG], b[i])) for i in range(SEG)]
    elif len(b) == 1:
        fs = [bm.faces.new((a[i], a[(i + 1) % SEG], b[0])) for i in range(SEG)]
    else:
        fs = [bm.faces.new((a[i], a[(i + 1) % SEG], b[(i + 1) % SEG], b[i])) for i in range(SEG)]
    for f in fs:
        f.material_index = mi
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
shaft = _obj(bm, COAT)
shaft.data.materials.append(WHITE)
xf(shaft, rotm((90, 0, 0)))    # local +Z -> -Y
LA.append(shaft)
vamp = lathe([(0.03, 0.12), (0.16, 0.14), (0.17, 0.17), (0.11, 0.3), (0.06, 0.45)], seg=8, material=ARMOR)
xf(vamp, rotm((90, 0, 0)))
LA.append(vamp)
LA.append(xf(lathe([(0.058, -0.05), (0.068, 0.0), (0.058, 0.05)], seg=8, material=GOLD), Matrix.Translation((0, Lb - 0.05, 0)) @ rotm((90, 0, 0))))
LA.append(xf(ell(V(0, 0, 0), (0.05, 0.05, 0.05), seg=7, rings=4, material=GOLD), Matrix.Translation((0, -Lf - 0.0, 0))))   # blunt coronel
lance = apart(LA, 'lance', (0, 0, 0))
lance.location = H

report()
lo, hi = bounds()
print('BOUNDS', tuple(lo), tuple(hi))
notes = ('De ruiters. Parts/pivots (Blender coords, front -Y, left=+X; ~2.2 m tall incl. plume, horse nose to tail ~2 m): '
         'body (origin 0,0,0; horse torso with caparison cloth in material "coat" (gold hem, white cross emblems), saddle, '
         'knight with armour + surcoat (coat), great helm with visor and coat plume, coat shield with white chevron on the left arm); '
         f'neck (pivot neck base {fmt(NECK)}; neck, head with big eyes, blaze, bridle, dark mane); '
         f'leg_fl {fmt(LEGS["fl"])}, leg_fr {fmt(LEGS["fr"])}, leg_bl {fmt(LEGS["bl"])}, leg_br {fmt(LEGS["br"])} (pivot shoulder/hip, '
         f'white socks, hooves on z=0); tail (pivot root {fmt(TR)}); lance (pivot at the right hand {fmt(H)}, ~3.0 m: 0.45 m behind '
         f'the hand, tip 2.57 m in front along -Y; spiral stripes coat + white, steel vamplate). '
         'Materials: horse, horse_dark, coat, armor, white, gold.')
finish('chars', 'horse_rider', kind='char', footprint=0.45, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        bpy.data.objects['neck'].rotation_euler = (0.25, 0, 0)
        bpy.data.objects['leg_fl'].rotation_euler = (0.5, 0, 0)
        bpy.data.objects['leg_br'].rotation_euler = (-0.5, 0, 0)
        bpy.data.objects['lance'].rotation_euler = (0.2, 0, 0)
    views2('horse', dirs={'front': (0, -1, 0.15), 'side': (-1, 0, 0.1), 'back': (0.7, 1, 0.5), 'face': (0.5, -1, 0.3)}, dist=1.1)
    views2('horse_pose', dirs={'p': (1, -1.25, 0.8)}, pose=pose, dist=1.2)
