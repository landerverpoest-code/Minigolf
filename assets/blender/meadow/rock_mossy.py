import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

stone = mat('stone_grey', '#9a968f', rough=0.9)
stone_d = mat('stone_dark', '#77736d', rough=0.95)
moss = mat('moss', '#5a9a2c', rough=0.95)
moss_l = mat('moss_light', '#86bd3c', rough=0.95)

def rock(r, scale, seed, sub=3, dec=0.7, matrock=stone):
    o = ico(r, sub=sub, material=matrock, scale=scale)
    off = Vector((seed * 1.7, seed * 2.9, seed * 0.3))
    for v in o.data.vertices:
        d = v.co.normalized()
        v.co *= 1 + 0.16 * noise.noise(d * 1.6 + off) + 0.05 * noise.noise(d * 4.5 + off)
        if v.co.z < -r * 0.3:
            v.co.z = -r * 0.3 + (v.co.z + r * 0.3) * 0.3   # platte onderkant
    decimate(o, dec)
    flat(o)
    return o

def moss_cap(o, lvl, seed, thick):
    """Mos als aparte laag: bovenste vlakken kopiëren, dikte geven, rand overhangend."""
    off = Vector((seed * 3.1, seed * 0.7, 2.0))
    cap = o.copy(); cap.data = o.data.copy(); bpy.context.scene.collection.objects.link(cap)
    set_mat(cap, moss)
    cap.data.materials.append(moss_l)
    bm = bmesh.new(); bm.from_mesh(cap.data)
    lo_z = min(v.co.z for v in bm.verts); hi_z = max(v.co.z for v in bm.verts)
    kill = []
    for f in bm.faces:
        c = f.calc_center_median()
        h = (c.z - lo_z) / (hi_z - lo_z)
        if f.normal.z + 0.25 * noise.noise(c * 3 + off) + 0.4 * h < lvl:
            kill.append(f)
    bmesh.ops.delete(bm, geom=kill, context='FACES')
    for v in bm.verts:
        v.co += v.normal * thick
    # rand iets naar buiten/omlaag laten hangen
    for e in bm.edges:
        if e.is_boundary:
            for v in e.verts:
                v.tag = True
    for v in bm.verts:
        if v.tag:
            v.co += Vector((v.normal.x, v.normal.y, 0)) * thick * 0.6 - Vector((0, 0, thick * 0.5))
    for f in bm.faces:
        if noise.noise(f.calc_center_median() * 4 + off) > 0.15:
            f.material_index = 1
    # rand: grensranden naar binnen/onder extruderen (dikte zichtbaar, geen verborgen binnenkant)
    bnd = [e for e in bm.edges if e.is_boundary]
    res = bmesh.ops.extrude_edge_only(bm, edges=bnd)
    for v in [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co += Vector((-v.co.x, -v.co.y, 0)).normalized() * thick * 1.2 - Vector((0, 0, thick * 1.2))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(cap.data); bm.free()
    flat(cap)
    return cap

big = rock(0.55, (1.25, 1.0, 0.85), 3)
xform(big, loc=(0, 0, 0.42))
cap = moss_cap(big, 0.95, 3, 0.035)
s2 = rock(0.28, (1.1, 1.0, 0.8), 8, sub=2, dec=1.0, matrock=stone_d)
xform(s2, loc=(0.62, -0.38, 0.17))
cap2 = moss_cap(s2, 1.05, 5, 0.025)
parts = [big, cap, s2, cap2]
for i, (x, y, r) in enumerate(((-0.62, -0.3, 0.1), (0.25, -0.62, 0.08), (-0.4, 0.5, 0.09))):
    p = ico(r, sub=1, material=stone_d, scale=(1.2, 1, 0.6))
    jitter(p, r * 0.15, seed=i)
    xform(p, loc=(x, y, r * 0.3), rot=(0, 0, i * 40))
    parts.append(p)
join(parts, 'rock_mossy')
report()
finish('meadow', 'rock_mossy', kind='scatter', footprint=0.8, notes='ronde grijze kei met overhangende moskap in 2 tinten, kleine steen en kiezels')
