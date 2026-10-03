import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood', '#9a6538', rough=0.8)
wood_d = mat('wood_dark', '#6e4528', rough=0.85)
hay = mat('hay', '#e2bf58', rough=0.95)
hay_d = mat('hay_dark', '#c99d3c', rough=0.95)
iron = mat('iron', '#3d3d42', rough=0.5, metal=0.4)

parts = []
BZ = 0.62    # hoogte laadbak
L, Wd = 1.5, 0.95
# laadbak: bodem + zijplanken met staanders
parts.append(box((L, Wd, 0.07), loc=(0, 0, BZ), material=wood_d))
for sy in (-1, 1):
    for k, z in enumerate((BZ + 0.12, BZ + 0.3)):
        parts.append(box((L + 0.06, 0.05, 0.13), loc=(0, sy * (Wd / 2 + 0.02), z), material=wood if k else wood_d))
    for x in (-L / 2 + 0.05, 0, L / 2 - 0.05):
        parts.append(box((0.07, 0.07, 0.48), loc=(x, sy * (Wd / 2 + 0.05), BZ + 0.18), material=wood_d))
for sx in (-1, 1):
    for k, z in enumerate((BZ + 0.12, BZ + 0.3)):
        parts.append(box((0.05, Wd, 0.13), loc=(sx * (L / 2 + 0.02), 0, z), material=wood if k else wood_d))
# disselbomen naar voren (-Y is voorkant -> wagen staat langs X, dissel naar -X)
for sy in (-1, 1):
    parts.append(plank((-L / 2 + 0.2, sy * 0.3, BZ - 0.05), (-L / 2 - 1.0, sy * 0.25, 0.32), w=0.07, t=0.07, material=wood))
parts.append(box((0.06, 0.62, 0.06), loc=(-L / 2 - 0.9, 0, 0.37), material=wood))
# as + wielen met spaken
parts.append(rod((0.15, -Wd / 2 - 0.2, 0.45), (0.15, Wd / 2 + 0.2, 0.45), 0.04, verts=6, material=wood_d))
R = 0.45
for sy in (-1, 1):
    y = sy * (Wd / 2 + 0.17)
    rim = lathe([(R, -0.05), (R, 0.05), (R - 0.07, 0.05), (R - 0.07, -0.05)], seg=12, material=wood, cap_bottom=False, cap_top=False)
    tire = lathe([(R + 0.02, -0.035), (R + 0.02, 0.035)], seg=12, material=iron, cap_bottom=False, cap_top=False)
    hub = cyl(0.09, 0.16, verts=8, material=wood_d)
    sp = [rim, tire, hub]
    for k in range(6):
        a = k * TAU / 6 + 0.2
        sp.append(plank((0.07 * math.cos(a), 0.07 * math.sin(a), 0), ((R - 0.05) * math.cos(a), (R - 0.05) * math.sin(a), 0), w=0.05, t=0.04, up=(0, 0, 1), material=wood))
    w_ = join(sp, 'wheel')
    xform(w_, rot=(90, 0, 0), loc=(0.15, y, 0.45))
    parts.append(w_)
# steunpoot achter
parts.append(plank((L / 2 - 0.15, 0, BZ), (L / 2 - 0.05, 0, 0.0), w=0.07, t=0.07, material=wood_d))
# hooi: bolle berg met sprieten
heap = ico(0.62, sub=2, material=hay, scale=(1.35, 0.85, 0.75))
lumpy(heap, 0.1, 2.0, seed=5)
heap.data.materials.append(hay_d)
for p in heap.data.polygons:
    if noise.noise(p.center * 3.0) > 0.25:
        p.material_index = 1
xform(heap, loc=(0.05, 0, BZ + 0.38))
bend(heap, lambda c: (c.x, c.y, max(c.z, BZ + 0.05)))
smooth(heap, 60)
parts.append(heap)
rnd = random.Random(4)
for k in range(10):
    a = rnd.uniform(0, TAU)
    p0 = Vector((0.75 * math.cos(a) + 0.05, 0.48 * math.sin(a), BZ + 0.38 + rnd.uniform(0.0, 0.25)))
    d = Vector((math.cos(a), math.sin(a) * 0.7, rnd.uniform(-0.2, 0.5))).normalized()
    parts.append(rod(p0, p0 + d * rnd.uniform(0.15, 0.25), 0.025, 0.0, verts=3, material=hay))
# hooivork in het hooi
parts.append(rod((0.5, 0.15, BZ + 0.2), (0.85, 0.3, BZ + 1.25), 0.025, verts=5, material=wood))
fz = Vector((0.5, 0.15, BZ + 0.2)); fd = (fz - Vector((0.85, 0.3, BZ + 1.25))).normalized()
for k in (-1, 0, 1):
    p0 = fz + Vector((0.05 * k, -0.05 * k * 0.3, 0))
    parts.append(rod(p0, p0 + fd * 0.25, 0.012, 0.004, verts=3, material=iron))
o = join(parts, 'hay_cart')
smooth(o, 40)
report()
finish('castle', 'hay_cart', kind='scatter', footprint=1.2, notes='houten boerenkar met 2 spaakwielen (ijzeren banden), dissel, steunpoot, berg hooi in 2 tinten en een hooivork')
