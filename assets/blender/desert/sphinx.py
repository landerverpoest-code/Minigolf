import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

SAND = mat('sandstone', '#e3bb7c', rough=0.85)
SAND2 = mat('sandstone_dark', '#b88a57', rough=0.9)
GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.55)
TURQ = mat('turquoise', '#27bfb0', rough=0.45)
DARK = mat('eye_dark', '#3b2a20', rough=0.7)
rnd = random.Random(3)

# --- sokkel ---
ZP = 0.6
plinth = box((3.0, 6.9, ZP - 0.12), loc=(0, -0.2, (ZP - 0.12) / 2), material=SAND2, bevel=0.04)
lip = box((3.2, 7.1, 0.12), loc=(0, -0.2, ZP - 0.06), material=SAND, bevel=0.03)
for s in (-1, 1):
    box((0.04, 6.2, 0.12), loc=(s * 1.5, -0.2, ZP * 0.45), material=TURQ)
    box((2.6, 0.04, 0.12), loc=(0, -0.2 + s * 3.45, ZP * 0.45), material=TURQ)
# --- lijf (loft van achter naar voor, -Y = voorkant) ---
def sec(y, w, h, z0=ZP, rr=0.3):
    pts = []
    for (u, v) in [(-1, 0), (-1, 0.7), (-0.75, 1), (0, 1.08), (0.75, 1), (1, 0.7), (1, 0), (0, -0.02)]:
        pts.append((u * w / 2, y, z0 + v * h))
    return pts
secs = [sec(2.55, 0.7, 0.6), sec(2.2, 1.15, 1.0), sec(1.5, 1.35, 1.2), sec(0.6, 1.1, 1.0), sec(-0.2, 1.2, 1.35), sec(-0.75, 1.15, 1.55), sec(-1.05, 0.95, 1.45)]
body = loft(secs, material=SAND, closed=True, cap0=True, cap1=True)
shade_smooth(body, 45)
# heupen (achterpoten opgevouwen)
for s in (-1, 1):
    sphere(1.0, loc=(s * 0.62, 1.45, ZP + 0.55), seg=10, rings=6, material=SAND, scale=(0.32, 0.85, 0.55))
    box((0.4, 0.75, 0.28), loc=(s * 0.7, 0.55, ZP + 0.14), material=SAND, bevel=0.1)   # achterpoot
# voorpoten
for s in (-1, 1):
    leg = box((0.46, 2.3, 0.46), loc=(s * 0.52, -1.95, ZP + 0.23), material=SAND, bevel=0.12)
    paw = box((0.54, 0.42, 0.36), loc=(s * 0.52, -3.0, ZP + 0.18), material=SAND, bevel=0.12)
    for k in (-1, 0, 1):
        box((0.025, 0.12, 0.2), loc=(s * 0.52 + k * 0.13, -3.2, ZP + 0.17), material=SAND2)
# staart langs de rechterzijde
tube([(0.4, 2.5, ZP + 0.15), (0.75, 2.4, ZP + 0.06), (0.85, 1.6, ZP + 0.06), (0.88, 0.8, ZP + 0.06), (0.75, 0.3, ZP + 0.12)],
     [0.08, 0.08, 0.075, 0.07, 0.09], verts=5, material=SAND)
# --- hoofd ---
_before = set(bpy.context.scene.objects)
HY, HZ = -0.95, ZP + 2.15
face = box((0.66, 0.5, 0.8), loc=(0, HY - 0.05, HZ), material=SAND, bevel=0.12)
nose = loft([[(-0.07, HY - 0.3, HZ + 0.12), (0.07, HY - 0.3, HZ + 0.12), (0.0, HY - 0.3, HZ + 0.14)],
             [(-0.09, HY - 0.36, HZ - 0.08), (0.09, HY - 0.36, HZ - 0.08), (0.0, HY - 0.44, HZ - 0.08)]], material=SAND, closed=True)
for s in (-1, 1):
    box((0.17, 0.04, 0.06), loc=(s * 0.16, HY - 0.31, HZ + 0.12), material=DARK)            # ogen
    box((0.2, 0.04, 0.04), loc=(s * 0.16, HY - 0.31, HZ + 0.22), rot=(0, s * 0.12, 0), material=SAND2)   # wenkbrauw
    box((0.12, 0.03, 0.03), loc=(s * 0.27, HY - 0.31, HZ + 0.1), rot=(0, -s * 0.3, 0), material=DARK)  # oogstreep
box((0.18, 0.04, 0.035), loc=(0, HY - 0.31, HZ - 0.2), material=SAND2)   # mond
# baard
beard = loft([[(-0.08, HY - 0.2, HZ - 0.38), (0.08, HY - 0.2, HZ - 0.38), (0.08, HY - 0.08, HZ - 0.38), (-0.08, HY - 0.08, HZ - 0.38)],
              [(-0.06, HY - 0.26, HZ - 0.85), (0.06, HY - 0.26, HZ - 0.85), (0.06, HY - 0.12, HZ - 0.85), (-0.06, HY - 0.12, HZ - 0.85)]],
             material=GOLD, closed=True)
for k in range(3):
    box((0.15, 0.17, 0.04), loc=(0, HY - 0.17 - k * 0.018, HZ - 0.5 - k * 0.12), material=TURQ)
# nemes-hoofddoek: kap boven en achter het gezicht, gestreept
def nsec(z, w, d, yoff=0.0):
    return [(-w / 2, HY + 0.05 + yoff, z), (-w / 2 * 0.9, HY + 0.05 + yoff + d, z), (w / 2 * 0.9, HY + 0.05 + yoff + d, z), (w / 2, HY + 0.05 + yoff, z),
            (w / 2 * 0.8, HY - 0.28 + yoff, z), (-w / 2 * 0.8, HY - 0.28 + yoff, z)]
nz = [(HZ - 0.65, 1.3, 0.55, 0.05), (HZ - 0.3, 1.1, 0.5, 0.04), (HZ + 0.05, 0.9, 0.48, 0.02), (HZ + 0.32, 0.84, 0.46, 0.0), (HZ + 0.52, 0.72, 0.4, 0.02), (HZ + 0.62, 0.5, 0.3, 0.05), (HZ + 0.66, 0.2, 0.15, 0.1)]
nz2 = []
for i in range(len(nz) - 1):
    a, b = nz[i], nz[i + 1]
    nsub = 3 if i < 4 else 1
    for j in range(nsub):
        t = j / nsub
        nz2.append(tuple(a[k] + (b[k] - a[k]) * t for k in range(4)))
nz2.append(nz[-1])
nemes = loft([nsec(z, w, d, yo) for z, w, d, yo in nz2], mats=[GOLD, TURQ], closed=True, cap0=False, cap1=True)
# strepen: per doorsnede-band om en om
nsecs = len(nz2)
for i, p in enumerate(nemes.data.polygons):
    band = i // 6
    p.material_index = band % 2 if band < 12 else 0
# voorste kapdeel (hoofdband boven het voorhoofd)
box((0.72, 0.12, 0.12), loc=(0, HY - 0.27, HZ + 0.38), material=GOLD, bevel=0.03)
# lappen voor de schouders
for s in (-1, 1):
    for k in range(5):
        z = HZ - 0.2 - k * 0.16
        box((0.26, 0.1, 0.15), loc=(s * 0.48, HY - 0.12, z), material=GOLD if k % 2 == 0 else TURQ)
# uraeus (cobra)
cone(0.06, 0.18, loc=(0, HY - 0.36, HZ + 0.5), verts=5, material=GOLD)
head = [o for o in bpy.context.scene.objects if o not in _before and o.type == 'MESH']
hd = join(head, 'head')
bpy.context.scene.cursor.location = (0, HY, HZ - 0.75)
bpy.ops.object.select_all(action='DESELECT'); hd.select_set(True); bpy.context.view_layer.objects.active = hd
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
hd.scale = (1.25, 1.25, 1.25); hd.location.z += 0.05
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
join_all('sphinx')
report()
finish('desert', 'sphinx', kind='hero', footprint=2.4,
       notes='Gestileerde sfinx op sokkel, kijkt naar -Y; gestreepte goud/turkoois nemes, gouden baard, staart langs de zijkant')
closeup('sphinx')
