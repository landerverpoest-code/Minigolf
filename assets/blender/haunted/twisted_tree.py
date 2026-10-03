import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
bark = mat('bark', '#4a3d4c', rough=0.95)
bark2 = mat('bark_light', '#62546a', rough=0.95)
hole = mat('hollow', '#140d18', rough=1.0)
eyes = mat('glow_eyes', '#d8ff5a', rough=0.5, emit='#c6ff3a', emit_strength=3.0)

V = Vector
# stam: kronkelend, onderaan breed
tp = [V((0, 0, -0.1)), V((0.05, 0, 0.5)), V((-0.1, 0.05, 1.1)), V((0.0, -0.02, 1.7)), V((0.22, 0.05, 2.3)), V((0.18, 0.1, 2.8)), V((0.05, 0.05, 3.25))]
trunk = tube(tp, r=[0.46, 0.36, 0.3, 0.26, 0.23, 0.19, 0.14], seg=7, material=bark, smooth=True)
parts = [trunk]
# wortels
for k, a in enumerate([0.3, 1.9, 3.4, 4.8]):
    d = V((math.cos(a), math.sin(a), 0))
    pts = [V((0, 0, 0.45)) + d * 0.1, V((0, 0, 0.18)) + d * 0.45, d * 0.85 + V((0, 0, -0.02)), d * 1.15 + V((0, 0, -0.08))]
    parts.append(tube(pts, r=[0.2, 0.15, 0.08, 0.0], seg=5, material=bark, smooth=True))
# hoofdtakken met krul aan het eind (naar beneden-binnen of omhoog-spiraal)
up = V((0, 0, 1))
br = [  # start, richting, lengte, krul omlaag?, krul, seed
    (V((0.15, 0.05, 2.4)), V((1, -0.25, 0.3)), 2.6, False, 1.25, 1),
    (V((0.05, 0.05, 3.0)), V((-1, 0.35, 0.45)), 2.6, True, 1.2, 2),
    (V((0.1, 0.1, 3.0)), V((0.25, 1, 0.5)), 2.1, False, 1.3, 3),
    (V((0.0, 0.0, 1.8)), V((-1, -0.7, 0.2)), 1.7, False, 1.3, 4),
    (V((0.12, 0.0, 3.0)), V((0.4, -0.8, 0.9)), 2.0, True, 1.2, 5),
]
tips = []
for (p, d, L, down, curl, sd) in br:
    ax = up.cross(d) if down else d.cross(up)
    pts = grow(p, d, L, 7, ax, -0.12, curl, seed=sd, wob=0.04, shrink=0.55)
    parts.append(tube(pts, r=taper(len(pts), 0.15, 0.035), seg=5, material=bark2 if sd % 2 else bark, smooth=True))
    tips.append(pts)
# zijtwijgjes
rnd = random.Random(7)
for k, pts in enumerate(tips):
    for j in ((2,) if k % 2 else (1, 3)):
        p = pts[j]; d = (pts[j + 1] - pts[j]).normalized()
        side = d.cross(V((0, 0, 1))).normalized() * (1 if (k + j) % 2 else -1)
        dd = (d * 0.6 + side + V((0, 0, 0.5))).normalized()
        tw = grow(p, dd, 0.7, 3, d.cross(dd), 0.3, 1.1, seed=k * 10 + j, wob=0.05)
        parts.append(tube(tw, r=[0.045, 0.03, 0.018, 0.0], seg=4, material=bark2, smooth=False))
# holte met gloeiende oogjes (vlak, net voor de stam)
from mathutils.bvhtree import BVHTree
tree = BVHTree.FromObject(trunk, bpy.context.evaluated_depsgraph_get())
hz = 1.12
hit = tree.ray_cast(V((0.0, -2, hz)), V((0, 1, 0)))[0]
yf = hit.y
hl = poly_face([(0.16 * math.cos(a), hz + 0.26 * math.sin(a)) for a in [i * TAU / 8 for i in range(8)]], hole, y=yf - 0.0)
# rand van de holte iets dieper in de stam laten zakken zodat het geen los plaatje lijkt
for v in hl.data.vertices:
    h2 = tree.ray_cast(V((v.co.x, -2, v.co.z)), V((0, 1, 0)))[0]
    v.co.y = min(yf, h2.y) - 0.012 if h2 else yf - 0.012
e1 = poly_face([(-0.09, hz + 0.04), (-0.02, hz + 0.02), (-0.05, hz + 0.1)], eyes, y=yf - 0.03)
e2 = poly_face([(0.02, hz + 0.02), (0.09, hz + 0.04), (0.05, hz + 0.1)], eyes, y=yf - 0.03)
parts += [hl, e1, e2]
T(join(parts, 'twisted_tree'), scale=1.2)
report()
finish('haunted', 'twisted_tree', kind='scatter', footprint=1.0, notes='kronkelige kale boom met krullende takken en holte met gloeiende oogjes (glow_eyes)')
