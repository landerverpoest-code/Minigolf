import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
basalt_l = mat('basalt_light', '#5a4b43', rough=0.85)
ash = mat('ash', '#7d7570', rough=1.0)
lava = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff4800', emit_strength=3.0)

# brede, platte kei die in tweeën gespleten is; lava gloeit in de spleet
big = chunk(0.75, (1.4, 1.1, 1.05), cuts=16, seed=31, material=basalt, flat_bottom=0.55, depth=(0.5, 0.85), base_sub=2)
xform(big, loc=(0, 0, 0.55))
# splitsen langs een schuin vlak
def split(o, co, n):
    a = o.copy(); a.data = o.data.copy(); bpy.context.scene.collection.objects.link(a)
    for ob, clear_outer in ((o, True), (a, False)):
        bm = bmesh.new(); bm.from_mesh(ob.data)
        res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-5, plane_co=co, plane_no=n, clear_outer=clear_outer, clear_inner=not clear_outer)
        ce = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
        bmesh.ops.holes_fill(bm, edges=ce, sides=0)
        bm.to_mesh(ob.data); bm.free()
        flat(ob)
    return o, a
core = big.copy(); core.data = big.data.copy(); bpy.context.scene.collection.objects.link(core)
set_mat(core, lava)
xform(core, loc=(0, 0, -0.55)); xform(core, scale=(0.9, 0.86, 0.9)); xform(core, loc=(0, 0, 0.52))
n = Vector((1, 0.35, 0.1)).normalized()
h1, h2 = split(big, Vector((0.05, 0, 0)), n)
xform(h1, loc=-n * 0.11 + Vector((0, 0, -0.01)), rot=(0, 0, 0))
xform(h2, loc=n * 0.11)
xform(h2, rot=(0, -4, 0))
h2.data.materials.clear(); h2.data.materials.append(basalt_l)
# gloeiende kern in de spleet
parts = [h1, h2, core]
# scheuren op de bovenkant
for o, s0, d, sd in ((h1, (-0.6, -0.6, 0.9), (-1, -0.2, 0.3), 4), (h2, (0.6, -0.5, 0.9), (1, -0.3, 0.3), 6), (h1, (-0.3, -0.7, 0.4), (-0.5, 0, 1), 9)):
    parts += crack_ribbon(surf_tree(o), s0, d, length=0.8, width=0.05, steps=8, seed=sd, material=lava, branch=1)
# kleine brokjes rondom
rnd = random.Random(4)
for k, (x, y, r) in enumerate(((-1.05, -0.3, 0.2), (1.05, -0.4, 0.16), (0.25, -0.75, 0.13), (-0.5, 0.65, 0.15))):
    c = chunk(r, (1.2, 1, 0.8), cuts=7, seed=40 + k, material=basalt if k % 2 else basalt_l, flat_bottom=0.4, base_sub=1)
    xform(c, loc=(x, y, r * 0.35), rot=(0, 0, rnd.uniform(0, 180)))
    parts.append(c)
for o in parts:
    if o.data.materials[0].name != 'glow_lava':
        dust(o, ash, 0.72)
join(parts, 'lava_rock_b')
report()
finish('volcano', 'lava_rock_b', kind='scatter', footprint=1.2, notes='brede gespleten basaltkei met gloeiende lavakern in de spleet, scheuren en brokjes')
