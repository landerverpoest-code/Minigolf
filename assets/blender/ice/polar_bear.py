import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice'); from _deco import *

FUR = mat('bear_fur', '#f4f0e6', rough=0.8)
FUR_S = mat('bear_fur_shade', '#dcd6c8', rough=0.85)
BLACK = mat('coal', '#22252b', rough=0.5)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
ICE = mat('ice_pale', '#b8ecff', rough=0.12, emit='#6fd0ff', emit_strength=0.2)

# mollige ijsbeer op vier poten, kop naar -Y, iets naar de camera gedraaid
body = blob([((0, 0.05, 0.62), 0.38), ((0, 0.38, 0.6), 0.36), ((0, -0.22, 0.66), 0.33), ((0, 0.05, 0.8), 0.3)],
            center=(0, 0.08, 0.64), sub=3, material=FUR, angle=50)
recolor(body, [FUR, FUR_S], lambda f: 1 if f.center.z < 0.42 else 0)
# poten: dikke zuilen met platte voeten
for x, y in ((0.2, -0.3), (-0.2, -0.3), (0.21, 0.45), (-0.21, 0.45)):
    tube([(x, y, 0.1), (x * 1.02, y, 0.35), (x * 0.95, y + 0.02, 0.6)], [0.13, 0.13, 0.15], verts=6, material=FUR, smooth=True, cap1=False)
    sphere(1.0, loc=(x * 1.03, y - 0.04, 0.08), seg=6, rings=3, material=FUR_S, scale=(0.15, 0.19, 0.09))
    if y < 0:
        for k in (-1, 0, 1):
            cone(0.022, 0.05, loc=(x * 1.03 + k * 0.06, y - 0.22, 0.04), rot=(math.pi / 2, 0, 0), verts=3, material=BLACK)
# kop met snuit, oortjes, ogen, neus
H = Vector((0.06, -0.62, 0.88))
head = sphere(1.0, seg=8, rings=5, material=FUR, scale=(0.21, 0.22, 0.19))
T(head, loc=H)
snout = sphere(1.0, seg=6, rings=4, material=FUR, scale=(0.11, 0.13, 0.09))
T(snout, loc=H + Vector((0.0, -0.17, -0.05)))
sphere(1.0, seg=5, rings=3, material=BLACK, scale=(0.05, 0.035, 0.032), loc=H + Vector((0.0, -0.3, -0.02)))
for s in (-1, 1):
    sphere(0.028, loc=H + Vector((s * 0.09, -0.18, 0.06)), seg=5, rings=3, material=BLACK)
    sphere(0.009, loc=H + Vector((s * 0.09 + 0.008, -0.205, 0.072)), seg=4, rings=3, material=SNOW)
    e = sphere(1.0, seg=6, rings=4, material=FUR_S, scale=(0.065, 0.04, 0.06))
    T(e, loc=H + Vector((s * 0.15, 0.04, 0.15)))
# staartje
sphere(0.08, loc=(0, 0.75, 0.72), seg=5, rings=3, material=FUR)
# kop iets naar de camera draaien
# ijsschots onder de beer
floe = lathe([(0.75, 0.0), (0.72, 0.06), (0.65, 0.08), (0.0, 0.085)], verts=8, material=SNOW, sx=0.9, sy=1.3, jitter=0.1, seed=2)
recolor(floe, [SNOW, ICE], lambda f: 1 if f.normal.z < 0.5 else 0)
for o in [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and ob is not floe]:
    T(o, loc=(0, 0, 0.06))
o = join_all('polar_bear')
report()
done('ice', 'polar_bear', kind='scatter', footprint=0.9, center=True,
     notes='Schattige mollige ijsbeer op vier poten (lijf als unie van bollen), ronde oortjes, zwarte neus en kraaloogjes met glimlichtje, nageltjes, op een ijsschots; kijkt naar -Y')
