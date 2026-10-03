import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

leaf_d = mat('leaf_bush', '#337a2a', rough=0.85)
leaf_l = mat('leaf_bush_light', '#5aa834', rough=0.85)
pink = mat('petal_pink', '#f27aa6', rough=0.6)
white = mat('petal_white', '#fbf6ee', rough=0.6)
yellow = mat('flower_heart', '#ffcf33', rough=0.5)

# bos: overlappende knobbels, donker onder, licht boven
blob_def = [(0.0, 0.08, 0.45, 0.58, 0), (0.4, -0.12, 0.36, 0.42, 0), (-0.38, -0.1, 0.38, 0.42, 0),
            (0.0, -0.12, 0.75, 0.45, 1)]
blobs = []
for i, (x, y, z, r, l) in enumerate(blob_def):
    b = ico(r, sub=2, material=leaf_l if l else leaf_d, scale=(1, 1, 0.88))
    lumpy(b, r * 0.2, 1.5 / r, seed=i * 7 + 2)
    xform(b, loc=(x, y, z), rot=(0, 0, i * 50))
    bend(b, lambda c: (c.x, c.y, max(c.z, 0.03)))
    smooth(b, 55)
    blobs.append(b)
bush = join(blobs, 'bush_flowering')

# bloemetjes: vijfhoekige kussentjes (roze/wit) met geel hart, gelijkmatig verspreid
cand = surface_points(bush, 600, seed=11, center=(0, 0, 0.4), zmin=0.22, up_bias=0.25)
pts = []
for p, n in cand:
    if all((p - q).length > 0.15 for q, _ in pts):
        pts.append((p, n))
    if len(pts) >= 38:
        break
flowers = []
for i, (p, n) in enumerate(pts):
    m = white if i % 3 == 0 else pink
    s = 0.055 + 0.012 * ((i * 7) % 3)
    f = cyl(s, 0.03, verts=5, r2=s * 0.42, material=m)
    f.data.materials.append(yellow)
    bm = bmesh.new(); bm.from_mesh(f.data)
    for face in list(bm.faces):
        if face.normal.z < -0.9:
            bm.faces.remove(face)
        elif face.normal.z > 0.9:
            face.material_index = 1
    bm.to_mesh(f.data); bm.free()
    xform(f, rot=(0, 0, i * 23))
    orient(f, n, p + n * 0.006)
    flowers.append(f)
join([bush] + flowers, 'bush_flowering')
report()
finish('meadow', 'bush_flowering', kind='scatter', footprint=0.6, notes='ronde bloeiende struik met roze/witte bloemetjes')
