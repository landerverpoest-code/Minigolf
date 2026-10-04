import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/water'); from _deco import *

WHITE = mat('boat_white', '#f6f4ee', rough=0.5)
TURQ = mat('boat_turq', '#27b8c4', rough=0.5)
WOOD = mat('boat_wood', '#b98450', rough=0.75)
CORAL = mat('boat_coral', '#ef6a4c', rough=0.5)
SAND = mat('sand', '#ead7a8', rough=0.95)

L = 2.2
NS = 9; NP = 9


def section(t, shrink=0.0):
    """Doorsnede op station t (0 = boeg -Y, 1 = spiegel +Y)."""
    y = -L / 2 + t * L
    w = 0.47 * (math.sin(min(1, t * 1.25 + 0.03) * math.pi / 2) ** 0.8) * (1 - 0.12 * max(0, t - 0.8) / 0.2) - shrink
    sheer = 0.55 + 0.18 * (1 - t) ** 3 + 0.03 * t      # boeg omhoog
    d = 0.4 * (0.35 + 0.65 * math.sin(min(1, t * 1.6 + 0.05) * math.pi / 2)) - shrink
    pts = []
    for j in range(NP):
        phi = math.pi * j / (NP - 1)
        x = w * math.cos(phi)
        z = sheer - d * math.sin(phi) ** 0.7 - (0.04 * (1 - t) ** 2 if 0 < j < NP - 1 else 0)
        pts.append(Vector((x, y, z)))
    return pts


# kleurbanden op de romp: turquoise boord, wit, koraalrode onderkant
outer = loft([section(i / (NS - 1)) for i in range(NS)], mats=[WHITE, TURQ, CORAL], band_mats=[1, 0, 0, 2, 2, 0, 0, 1], closed=False, cap0=False, cap1=True)
inner = loft([section(i / (NS - 1), 0.03) for i in range(NS)], material=WOOD, closed=False, cap0=False, cap1=False)
# boordrand (gunwale) en kiel
for s in (-1, 1):
    pts = [Vector((s * p[0].x if s > 0 else p[-1].x, p[0].y, p[0].z)) for p in [section(i / (NS - 1)) for i in range(NS)]]
    tube(pts, 0.03, verts=4, material=TURQ, smooth=True)
keel = [section(i / (NS - 1))[NP // 2] - Vector((0, 0, 0.02)) for i in range(NS)]
tube(keel, 0.025, verts=4, material=WOOD)
# doften (zitbanken)
for t in (0.4, 0.75):
    sec = section(t, 0.03)
    z = sec[0].z - 0.12
    plank((sec[0].x - 0.02, sec[0].y, z), (sec[-1].x + 0.02, sec[0].y, z), w=0.2, t=0.035, material=WOOD)
# roeiriemen: één in de boot, één tegen de romp in het zand
def oar(p0, p1):
    p0, p1 = Vector(p0), Vector(p1)
    rod(p0, p1, r=0.022, verts=5, material=WOOD)
    d = (p1 - p0).normalized()
    blade = box((0.16, 0.025, 0.42), material=CORAL)
    q = d.to_track_quat('Z', 'X')
    blade.data.transform(Matrix.Translation(p1 + d * 0.18) @ q.to_matrix().to_4x4())
oar((-0.22, -0.6, 0.48), (0.18, 0.75, 0.55))
oar((0.7, -0.75, 0.04), (0.62, 0.55, 0.12))
# zandhoop waarin de boot een beetje wegzakt + touw naar een paaltje
sand = lathe([(1.0, 0.0), (0.85, 0.08), (0.5, 0.14), (0.0, 0.16)], verts=12, material=SAND, sx=0.85, sy=1.45, jitter=0.08, seed=3)
lumpy(sand, 0.04, 2.0, seed=2, axes=(1, 1, 0.5))
rope = tube([(0.0, -1.12, 0.62), (0.08, -1.4, 0.3), (0.12, -1.6, 0.14), (0.15, -1.75, 0.2)], 0.015, verts=3, material=WOOD)
rod((0.15, -1.75, 0.0), (0.15, -1.78, 0.35), r=0.04, verts=5, material=WOOD)
# boot een beetje gekanteld in het zand (rollen om de lengteas)
for o in [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and ob is not sand]:
    if o.name.startswith('Cylinder') and o.location.length > 0:
        pass
boat_objs = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and ob not in (sand,)]
for ob in boat_objs:
    T(ob, rot=(0, 9, 0), pivot=(0, 0, 0.3))
    T(ob, loc=(0, 0, -0.12))
o = join_all('rowboat')
clip_below(o, 0.0)
report()
done('water', 'rowboat', kind='scatter', footprint=1.3, center=True,
     notes='Op het strand getrokken roeiboot: witte romp met turquoise boord en koraalrode waterlijn, houten binnenkant met twee doften, kiel, roeiriemen met koraalrode bladen, touw naar een meerpaaltje, zandhoop')
