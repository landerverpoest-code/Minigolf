import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

red = mat('cap_red', '#e0302a', rough=0.45)
cream = mat('mush_cream', '#f6ecd6', rough=0.7)
green = mat('grass', '#4a9a32', rough=0.8)

parts = []
def toadstool(x, y, h, R, tilt, seg, nspots, seed):
    rnd = random.Random(seed)
    st = lathe([(R * 0.34, 0), (R * 0.33, h * 0.35), (R * 0.22, h * 0.95)], seg=5, material=cream, cap_bottom=False, cap_top=False)
    smooth(st, 80)
    # hoed: koepel + vlakke onderkant (lamellen) in crème
    cap = lathe([(R * 0.25, h * 0.92), (R, h * 0.9), (R * 0.88, h * 1.14), (R * 0.5, h * 1.34), (0, h * 1.4)], seg=seg, material=red, cap_bottom=True)
    cap.data.materials.append(cream)
    for p in cap.data.polygons:
        if p.normal.z < -0.5:
            p.material_index = 1
    smooth(cap, 50)
    objs = [st, cap]
    # stippen op de hoed
    for k in range(nspots):
        a = TAU * k / nspots + rnd.uniform(-0.3, 0.3)
        el = rnd.uniform(0.35, 0.95) if k else 1.5
        # punt op de koepel (benadering)
        rr = R * 0.9 * math.cos(el) if k else 0.0
        zz = h * 1.0 + (h * 0.38) * math.sin(el) if k else h * 1.4
        nrm = Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el) * 1.6)).normalized() if k else Vector((0, 0, 1))
        sp = cyl(R * rnd.uniform(0.14, 0.2), 0.006, verts=5, material=cream)
        bm = bmesh.new(); bm.from_mesh(sp.data)
        for f in list(bm.faces):
            if abs(f.normal.z) < 0.5 or f.normal.z < 0:
                bm.faces.remove(f)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
        bm.to_mesh(sp.data); bm.free()
        orient(sp, nrm, Vector((rr * math.cos(a), rr * math.sin(a), zz)))
        objs.append(sp)
    for o in objs:
        xform(o, rot=(tilt[0], tilt[1], 0), loc=(x, y, 0))
    return objs

parts += toadstool(0.0, 0.0, 0.2, 0.11, (0, 6), 8, 6, 1)
parts += toadstool(0.12, -0.07, 0.13, 0.075, (-8, 14), 7, 4, 2)
parts += toadstool(-0.1, -0.08, 0.09, 0.055, (10, -12), 6, 3, 3)
# grassprietjes
rnd = random.Random(9)
for i in range(4):
    a = i * 90 + rnd.uniform(-20, 20)
    g = leaf(rnd.uniform(0.08, 0.12), 0.03, 0.004, material=green)
    xform(g, rot=(65, 0, 0))
    xform(g, rot=(0, 0, a), loc=(0.09 * math.cos(math.radians(a)), 0.07 * math.sin(math.radians(a)), 0))
    parts.append(g)
join(parts, 'mushroom_cluster')
report()
finish('meadow', 'mushroom_cluster', kind='edge', footprint=0.17, notes='3 rode vliegenzwammen met witte stippen en grassprietjes')
