import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
wood = mat('wood', '#5e4434', rough=0.85)
cloth = mat('cloth', '#43385a', rough=0.95)
straw = mat('straw', '#d6b04a', rough=0.9)
orange = mat('pumpkin', '#d95d0e', rough=0.5)
glow = mat('glow_pumpkin', '#ffd040', rough=0.5, emit='#ffc21a', emit_strength=2.0)
V = Vector
parts = []
parts.append(box((0.1, 0.1, 2.0), loc=(0, 0.02, 1.0), material=wood))
parts.append(box((1.5, 0.08, 0.08), loc=(0, 0.02, 1.45), material=wood))
# jas met gerafelde zoom
seg = 10
coat = lathe([(0.29, 0.72), (0.25, 1.05), (0.22, 1.35), (0.2, 1.5), (0.08, 1.56)], seg=seg, material=cloth, cap_bot=False, cap_top=False)
def hem(v):
    if v.z < 0.73:
        a = math.atan2(v.y, v.x)
        k = round(a / (TAU / seg))
        v.z += 0.12 * (k % 2) + 0.03 * math.sin(k * 2.3)
    return v
deform(coat, hem)
T(coat, scale=(1.0, 0.75, 1.0))
inner = dup(coat); flip(inner); T(inner, scale=0.97, pivot=(0, 0, 1.2))
parts += [coat, inner]
# mouwen
for sx in (-1, 1):
    sl = tube([V((sx * 0.12, 0.02, 1.45)), V((sx * 0.4, 0.02, 1.44)), V((sx * 0.62, 0.02, 1.42))], r=[0.1, 0.1, 0.13], seg=6, material=cloth, smooth=False, cap=False)
    parts.append(sl)
    for j, (dy, dz) in enumerate([(0.04, 0.03), (-0.05, -0.02), (0.0, -0.08)]):
        parts.append(cone(0.035, 0.22, loc=(sx * 0.7, 0.02 + dy, 1.42 + dz), rot=(0, sx * (math.pi / 2 + dz * 3), 0), verts=4, material=straw))
# stro onder de jas en aan de nek
for k in range(6):
    a = k * TAU / 6 + 0.3
    parts.append(cone(0.04, 0.25, loc=(0.2 * math.cos(a), 0.15 * math.sin(a), 0.68), rot=(math.pi + 0.3 * math.sin(a), 0.3 * math.cos(a), 0), verts=4, material=straw))
parts.append(cyl(0.1, 0.08, loc=(0, 0.02, 1.58), verts=8, r2=0.13, material=straw))
# touw-riem + lappen
parts.append(cyl(0.25, 0.05, loc=(0, 0, 1.0), verts=10, material=straw))
T(parts[-1], scale=(1.0, 0.76, 1.0))
parts.append(box((0.12, 0.02, 0.12), loc=(0.1, -0.21, 1.2), rot=(0, 0.2, 0.15), material=straw))
parts.append(box((0.1, 0.02, 0.1), loc=(-0.12, -0.215, 0.88), rot=(0, -0.3, 0.1), material=wood))
parts.append(box((0.1, 0.1, 0.02), loc=(-0.45, 0.02, 1.535), rot=(0, 0.1, 0.3), material=straw))
# pompoenhoofd
hseg = 10
ribs = lambda a, z: 1.0 - 0.1 * (round((a + math.pi / 2) / (TAU / hseg)) % 2)
head = lathe([(0, 0.02), (0.15, 0.0), (0.22, 0.1), (0.21, 0.21), (0.13, 0.29), (0, 0.27)], seg=hseg, material=orange, smooth=True, phase=-math.pi / 2, rfn=ribs)
shade_smooth(head, 25)
T(head, scale=(1.05, 0.95, 0.95), loc=(0, 0.0, 1.6))
face = join([poly_face(p, glow) for p in (
    [(-0.13, 1.75), (-0.03, 1.74), (-0.09, 1.81)], [(0.03, 1.74), (0.13, 1.75), (0.09, 1.81)],
    [(-0.13, 1.68), (-0.08, 1.64), (-0.04, 1.665), (0.0, 1.635), (0.04, 1.665), (0.08, 1.64), (0.13, 1.68), (0.06, 1.665), (0.0, 1.68), (-0.06, 1.665)])], 'face')
project(face, head, (0, 1, 0), offset=0.004)
parts += [head, face]
# heksenhoed met geknikte punt
parts.append(cyl(0.32, 0.025, loc=(0, 0, 1.86), verts=12, material=cloth))
hat = tube([V((0, 0, 1.86)), V((0.0, 0.0, 2.02)), V((0.03, 0.02, 2.15)), V((0.1, 0.05, 2.24)), V((0.2, 0.06, 2.24))], r=[0.18, 0.13, 0.08, 0.04, 0.0], seg=8, material=cloth, smooth=False)
parts.append(hat)
parts.append(cyl(0.17, 0.05, loc=(0, 0, 1.9), verts=8, r2=0.15, material=straw))
T(parts[-1], rot=(0, 0, 0))
# kraai op de arm
cx = 0.48
crow = [ico(0.07, loc=(cx, 0.02, 1.55), material=cloth, scale=(1.5, 0.8, 0.85), smooth=True),
        ico(0.045, loc=(cx - 0.09, 0.02, 1.62), material=cloth, smooth=True),
        cone(0.018, 0.07, loc=(cx - 0.15, 0.02, 1.615), rot=(0, -math.pi / 2, 0), verts=4, material=orange),
        prism([(0, 0), (0.14, 0.03), (0.14, -0.03)], 0.012, cloth, axis='z', loc=(cx + 0.08, 0.02, 1.56))]
T(crow[3], rot=(0, -0.4, 0), pivot=(cx + 0.08, 0.02, 1.56))
for sy in (-1, 1):
    crow.append(prism([(0, 0), (0.12, 0.03), (0.1, -0.02)], 0.01, cloth, axis='z', loc=(cx - 0.03, 0.02 + sy * 0.055, 1.56)))
    T(crow[-1], rot=(sy * 0.4, -0.2, 0), pivot=(cx - 0.03, 0.02 + sy * 0.055, 1.56))
c = join(crow, 'crow'); T(c, scale=1.35, pivot=(cx, 0.02, 1.5), loc=(0, 0, 0.06)); parts.append(c)
join(parts, 'scarecrow_spooky')
report()
finish('haunted', 'scarecrow_spooky', kind='scatter', footprint=0.4, notes='gerafelde vogelverschrikker met pompoenhoofd (glow_pumpkin), heksenhoed en kraai')
