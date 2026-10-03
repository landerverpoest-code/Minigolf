import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

C1 = mat('ice_crystal', '#18b8e8', rough=0.1, emit='#0aa8e8', emit_strength=0.5)
C2 = mat('ice_crystal_pale', '#8fe6ff', rough=0.1, emit='#4fd0ff', emit_strength=0.35)
GLOW = mat('glow_crystal', '#30e0ff', rough=0.1, emit='#00d0ff', emit_strength=1.8)
ROCK = mat('ice_rock', '#4f6077', rough=0.85)
SNOW = mat('snow', '#eef6ff', rough=0.7)
rnd = random.Random(9)


def crystal(base, direction, h, r, material, phase=0.0):
    c = lathe([(r * 0.8, 0.0), (r, h * 0.7), (0.0, h)], verts=6, material=material, phase=phase)
    d = Vector(direction).normalized()
    q = Vector((0, 0, 1)).rotation_difference(d)
    c.rotation_mode = 'QUATERNION'; c.rotation_quaternion = q; c.location = base
    bpy.ops.object.select_all(action='DESELECT'); c.select_set(True); bpy.context.view_layer.objects.active = c
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return c

base = rock(0.24, loc=(0, 0, 0.04), scale=(1.3, 1.1, 0.6), seed=2, jitter=0.2, material=ROCK)
cfg = [((0, 0, 0.05), (0.05, 0.0, 1), 0.62, 0.075, GLOW),
       ((0.1, 0.05, 0.04), (0.6, 0.25, 1), 0.42, 0.06, C1),
       ((-0.09, 0.06, 0.04), (-0.6, 0.35, 1), 0.47, 0.065, C2),
       ((0.04, -0.1, 0.04), (0.2, -0.7, 1), 0.36, 0.055, C1),
       ((-0.08, -0.08, 0.03), (-0.55, -0.5, 1), 0.3, 0.05, C1),
       ((0.16, -0.06, 0.02), (1.0, -0.3, 0.8), 0.22, 0.04, C2),
       ((-0.17, 0.0, 0.02), (-1.0, 0.1, 0.7), 0.2, 0.04, GLOW),
       ((0.02, 0.15, 0.03), (0.1, 0.9, 0.9), 0.27, 0.045, C1)]
for b, d, h, r, m in cfg:
    crystal(Vector(b), d, h, r, m, phase=rnd.uniform(0, 1))
# sneeuwplukjes op de steen
s = rock(0.12, loc=(0.18, 0.12, 0.08), scale=(1.4, 1.0, 0.45), seed=5, jitter=0.15, material=SNOW)
s = rock(0.1, loc=(-0.2, -0.1, 0.07), scale=(1.3, 1.1, 0.45), seed=6, jitter=0.15, material=SNOW)
join_all('ice_crystals')
report()
finish('ice', 'ice_crystals', kind='edge', footprint=0.3,
       notes='Cluster cyaan ijskristallen (lage roughness, lichte emissie); middelste kristallen gloeien (glow_crystal)')
closeup('ice_crystals')
