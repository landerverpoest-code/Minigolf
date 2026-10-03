import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

bone = mat('bone', '#ecdfc0', rough=0.6)
dark = mat('socket_dark', '#2a1d19', rough=0.9)

parts = []
# --- schedel (cartoony): ronde hersenpan + snuit, grote oogkassen ---
cr = sphere(0.1, seg=8, rings=6, material=bone, scale=(1.0, 1.1, 0.95))
xform(cr, loc=(0, 0.01, 0.1))
smooth(cr, 70)
parts.append(cr)
mz = box((0.13, 0.08, 0.075), material=bone)
xform(mz, loc=(0, -0.075, 0.045))
bend(mz, lambda c: (c.x * (0.82 if c.z < 0.03 else 1.0), c.y, c.z))
smooth(mz, 50)
parts.append(mz)
# oogkassen: platte zeshoekjes net voor het oppervlak
for sx in (-1, 1):
    e = mesh_obj([(0.032 * math.cos(a), 0.0, 0.036 * math.sin(a)) for a in [k * TAU / 6 for k in range(6)]], [list(range(6))[::-1]], dark)
    xform(e, rot=(0, 0, sx * 22), loc=(sx * 0.042, -0.092, 0.1))
    parts.append(e)
nose = mesh_obj([(-0.017, 0, 0.076), (0.017, 0, 0.076), (0, 0, 0.05)], [(0, 2, 1)], dark)
xform(nose, loc=(0, -0.1155, 0.0))
parts.append(nose)
# tanden: donkere streepjes op de snuit
for x in (-0.027, 0.0, 0.027):
    t = mesh_obj([(-0.004, 0, 0.012), (0.004, 0, 0.012), (0.004, 0, 0.038), (-0.004, 0, 0.038)], [(0, 1, 2, 3)], dark)
    xform(t, loc=(x, -0.1162, 0.0))
    parts.append(t)
mouth = mesh_obj([(-0.045, 0, 0.024), (0.045, 0, 0.024), (0.045, 0, 0.029), (-0.045, 0, 0.029)], [(0, 1, 2, 3)], dark)
xform(mouth, loc=(0, -0.1163, 0))
parts.append(mouth)
skull = join(parts, 'skull')
xform(skull, rot=(-8, 0, 28), loc=(-0.06, -0.0, 0.0))

# --- botten: schacht + twee bolletjes aan elk uiteinde (cartoon) ---
def bone_piece(L, r):
    h = L / 2
    ps = [cyl(r, L - 2 * r, verts=5, material=bone)]
    bm = bmesh.new(); bm.from_mesh(ps[0].data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if abs(f.normal.z) > 0.9], context='FACES')
    bm.to_mesh(ps[0].data); bm.free()
    for sz in (-1, 1):
        for sx in (-1, 1):
            k = sphere(r * 1.45, seg=5, rings=3, material=bone)
            xform(k, loc=(sx * r * 1.05, 0, sz * (h - r * 0.9)))
            ps.append(k)
    o = join(ps, 'bone')
    smooth(o, 70)
    return o
b1 = bone_piece(0.3, 0.02)
xform(b1, rot=(90, 0, 70), loc=(0.12, 0.08, 0.03))
b2 = bone_piece(0.24, 0.018)
xform(b2, rot=(84, 0, -35), loc=(0.1, -0.12, 0.027))
o = join([skull, b1, b2], 'bones')
report()
finish('volcano', 'bones', kind='edge', footprint=0.22, notes='cartoony schedel met grote oogkassen en twee knokige botten')
