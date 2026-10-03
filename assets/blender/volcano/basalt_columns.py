import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#55473f', rough=0.85)
ash = mat('ash', '#8a827c', rough=1.0)
lava = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff4800', emit_strength=3.0)

rnd = random.Random(7)
R = 0.3
parts = []
# honingraat-raster, hoogte neemt af naar de randen
cells = []
for q in range(-2, 3):
    for r_ in range(-2, 3):
        x = R * 1.75 * (q + r_ * 0.5)
        y = R * 1.75 * 0.866 * r_
        d = math.hypot(x, y)
        if d > 0.95:
            continue
        cells.append((x, y, d))
for i, (x, y, d) in enumerate(cells):
    h = max(0.5, 3.0 - d * 2.0 + rnd.uniform(-0.45, 0.35))
    rr = R * rnd.uniform(0.92, 1.0)
    c = cyl(rr, h, loc=(0, 0, h / 2), verts=6, material=basalt if i % 3 else basalt_l)
    jitter(c, 0.025, seed=i, axes=(1, 1, 0))
    # schuin afgebroken top
    tilt = Vector((rnd.uniform(-0.25, 0.25), rnd.uniform(-0.25, 0.25)))
    for v in c.data.vertices:
        if v.co.z > h / 2 - 1e-3:
            v.co.z += tilt.x * v.co.x + tilt.y * v.co.y
    m = c.modifiers.new('bev', 'BEVEL'); m.width = 0.035; m.segments = 1; m.limit_method = 'ANGLE'; m.angle_limit = math.radians(70)
    bpy.context.view_layer.objects.active = c; bpy.ops.object.modifier_apply(modifier=m.name)
    # onderkant weg (staat in de grond)
    bm = bmesh.new(); bm.from_mesh(c.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.z < -0.9], context='FACES')
    bm.to_mesh(c.data); bm.free()
    xform(c, rot=(0, 0, rnd.uniform(-8, 8)), loc=(x, y, 0))
    dust(c, ash, 0.8)
    smooth(c, 35)
    parts.append(c)
# omgevallen/gebroken zuilstukken
for k, (x, y, a, L) in enumerate(((1.35, -0.5, 25, 0.9), (-1.2, -0.75, -40, 0.7), (0.4, -1.25, 75, 0.55))):
    c = cyl(R * 0.9, L, verts=6, material=basalt_l if k % 2 else basalt)
    jitter(c, 0.02, seed=20 + k)
    bev(c, 0.03)
    xform(c, rot=(90, 0, a), loc=(x, y, R * 0.8))
    dust(c, ash, 0.85)
    smooth(c, 35)
    parts.append(c)
# gloeiende spleet tussen een paar voeten
glow = lathe([(0.32, 0.0), (0.26, 0.03), (0, 0.035)], seg=6, material=lava)
xform(glow, scale=(1.6, 0.6, 1), rot=(0, 0, 20), loc=(0.55, -0.85, 0))
parts.append(glow)
join(parts, 'basalt_columns')
report()
finish('volcano', 'basalt_columns', kind='scatter', footprint=1.4, notes='cluster zeshoekige basaltzuilen van verschillende hoogte met as op de toppen, omgevallen stukken en een gloeiende spleet')
