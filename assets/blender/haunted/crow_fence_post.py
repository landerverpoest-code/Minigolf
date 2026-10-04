import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted'); from _deco import *

WOOD = mat('wood', '#6b5040', rough=0.85)
WOOD_D = mat('wood_dark', '#3d2e2c', rough=0.9)
CROW = mat('crow_black', '#1d1a24', rough=0.5)
BEAK = mat('crow_beak', '#5a5560', rough=0.5)
EYES = mat('glow_eyes', '#d8ff5a', rough=0.5, emit='#c6ff3a', emit_strength=3.0)

# scheve paal met puntje en een stuk gebroken hek-lat
post = prism([(-0.07, 0), (0.07, 0), (0.07, 0.95), (0.0, 1.03), (-0.07, 0.95)], 0.12, material=WOOD, axis='Y')
T(post, rot=(0, 5, 0))
jitter(post, 0.01, seed=2)
plank((0.02, -0.07, 0.62), (0.55, -0.07, 0.48), w=0.11, t=0.025, up=(0, -1, 0), material=WOOD_D)
plank((0.02, -0.07, 0.3), (0.42, -0.07, 0.12), w=0.1, t=0.025, up=(0, -1, 0), material=WOOD_D)
for p in ((0.04, -0.09, 0.62), (0.04, -0.09, 0.3)):
    box((0.025, 0.02, 0.025), loc=p, material=BEAK)
# kraai bovenop (kijkt naar -Y, kopje schuin)
C = Vector((0.06, 0.0, 1.06))
body = sphere(1.0, seg=6, rings=4, material=CROW, scale=(0.075, 0.12, 0.085))
T(body, rot=(-25, 0, 0), loc=C + Vector((0, 0.01, 0.08)))
tail = mesh_obj([C + Vector((-0.035, 0.08, 0.08)), C + Vector((0.035, 0.08, 0.08)), C + Vector((0.05, 0.24, 0.02)), C + Vector((-0.05, 0.24, 0.02))], [(0, 1, 2, 3)], CROW, 'tail')
for s in (-1, 1):
    mesh_obj([C + Vector((s * 0.07, -0.06, 0.12)), C + Vector((s * 0.085, 0.04, 0.13)), C + Vector((s * 0.06, 0.17, 0.08))], [(0, 1, 2)], CROW, 'wing')
    rod(C + Vector((s * 0.03, 0.0, -0.03)), C + Vector((s * 0.03, 0.0, 0.03)), r=0.008, verts=3, material=BEAK)
head = sphere(0.055, loc=C + Vector((0, -0.09, 0.19)), seg=6, rings=4, material=CROW)
beak = cone(0.022, 0.08, loc=C + Vector((0, -0.165, 0.18)), rot=(math.pi / 2 + 0.15, 0, 0), verts=4, material=BEAK)
for s in (-1, 1):
    sphere(0.012, loc=C + Vector((s * 0.032, -0.125, 0.205)), seg=4, rings=3, material=EYES)
# veertjes op de kop
cone(0.015, 0.05, loc=C + Vector((0, -0.08, 0.25)), rot=(-0.4, 0, 0), verts=3, material=CROW)
for ob in [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and ob.data.materials and ob.data.materials[0].name in ('crow_black', 'glow_eyes')]:
    T(ob, scale=1.3, pivot=C - Vector((0, 0, 0.03)))
for ob in [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and ob.data.materials and ob.data.materials[0].name == 'crow_beak' and bounds([ob])[0].z > 1.0]:
    T(ob, scale=1.3, pivot=C - Vector((0, 0, 0.03)))
o = join_all('crow_fence_post')
report()
done('haunted', 'crow_fence_post', kind='edge', footprint=0.3,
     notes='Scheve houten hekpaal met afgebroken latten en spijkers, met een zwarte kraai (gloeiende gele oogjes, glow_eyes) bovenop')
