import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

SNOW = mat('snow', '#f4f8ff', rough=0.7)
COAL = mat('coal', '#22252b', rough=0.6)
CARROT = mat('carrot', '#ff7a1c', rough=0.6)
RED = mat('scarf_red', '#d8343c', rough=0.75)
WOOD = mat('stick', '#6e4a2c', rough=0.9)

# drie bollen
b1 = sphere(0.48, loc=(0, 0, 0.42), seg=10, rings=7, material=SNOW, scale=(1, 1, 0.9))
b2 = sphere(0.35, loc=(0, 0, 1.03), seg=10, rings=7, material=SNOW, scale=(1, 1, 0.92))
b3 = sphere(0.26, loc=(0, 0, 1.5), seg=10, rings=7, material=SNOW)
for b in (b1, b2, b3):
    for v in b.data.vertices:
        if v.co.z < (0.02 if b is b1 else -10): v.co.z = 0.02
# sneeuwhoopje
mound = lathe([(0.62, 0.0), (0.5, 0.08), (0.3, 0.12), (0.0, 0.13)], verts=9, material=SNOW, jitter=0.06, seed=3)
shade_smooth(mound, 60)
# gezicht (voor = -Y)
for s in (-1, 1):
    sphere(0.035, loc=(s * 0.09, -0.235, 1.56), seg=5, rings=3, material=COAL)
nose = cone(0.045, 0.24, loc=(0, -0.33, 1.49), rot=(math.pi / 2, 0, 0), verts=6, material=CARROT)
for k in range(3):  # glimlach
    a = math.pi * (1.3 + 0.2 * k)
    sphere(0.018, loc=(math.cos(a) * 0.1 * -1 * -1, -0.245 + 0.0, 1.42 + math.sin(a) * 0.04 + 0.04), seg=4, rings=3, material=COAL, smooth=False)
# knopen
for k, z in enumerate((1.12, 0.98, 0.84)):
    r = 0.35 * math.sqrt(max(0.0, 1 - ((z - 1.03) / (0.35 * 0.92)) ** 2))
    sphere(0.04, loc=(0, -r - 0.005, z), seg=5, rings=3, material=COAL)
# sjaal
torus(0.25, 0.065, loc=(0, 0, 1.28), seg=12, ring=4, material=RED, smooth=False)
tail = tube([(0.12, -0.2, 1.27), (0.17, -0.27, 1.12), (0.2, -0.27, 0.95)], [0.06, 0.055, 0.05], verts=4, material=RED, squash=(1.6, 0.5))
for z in (1.05, 0.98):
    pass
# armen (takken)
for s in (-1, 1):
    p0 = Vector((s * 0.3, 0, 1.12)); p1 = Vector((s * 0.62, 0.02, 1.32)); p2 = Vector((s * 0.85, 0.0, 1.5))
    tube([p0, p1, p2], [0.025, 0.02, 0.012], verts=4, material=WOOD)
    tube([p1 + (p2 - p1) * 0.4, p1 + (p2 - p1) * 0.4 + Vector((s * 0.05, -0.02, 0.17))], [0.013, 0.006], verts=3, material=WOOD)
    tube([p2 - (p2 - p1) * 0.1, p2 + Vector((s * 0.15, 0.0, -0.02))], [0.011, 0.005], verts=3, material=WOOD)
# hoge hoed
brim = cyl(0.27, 0.035, loc=(0, 0, 1.72), verts=12, material=COAL)
crown = cyl(0.17, 0.32, loc=(0, 0, 1.88), verts=12, material=COAL, r2=0.18)
band = cyl(0.178, 0.07, loc=(0, 0, 1.775), verts=12, material=RED)
hat = join([brim, crown, band], 'hat')
place(hat, rot=(0.08, -0.12, 0))
join_all('snowman')
report()
finish('ice', 'snowman', kind='scatter', footprint=0.55,
       notes='Sneeuwpop: drie bollen, wortelneus, kolen-ogen en knopen, rode sjaal, takken-armen en hoge hoed (kijkt naar -Y)')
closeup('snowman')
