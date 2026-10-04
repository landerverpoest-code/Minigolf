import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice'); from _deco import *

STONE = mat('ice_rock', '#7f8c9c', rough=0.85)
STONE_D = mat('ice_rock_dark', '#5a6a7e', rough=0.85)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
GLOW = mat('glow_window', '#ffd27a', rough=0.4, emit='#ffa640', emit_strength=5.0)

# sneeuwlantaarn (yukimi-doro): drie poten, lichtkamer, breed dak met sneeuwkap
for k in range(3):
    a = k * TAU / 3 + 0.5
    rod((0.22 * math.cos(a), 0.22 * math.sin(a), 0.0), (0.1 * math.cos(a), 0.1 * math.sin(a), 0.3), r=0.04, verts=4, material=STONE_D)
cyl(0.2, 0.06, loc=(0, 0, 0.33), verts=6, material=STONE)
# lichtkamer: zeshoekig met gloeiende ramen
ch = lathe([(0.13, 0.36), (0.13, 0.56)], verts=6, material=STONE, cap0=False, cap1=False)
recolor(ch, [STONE, GLOW], lambda f: 1)
for k in range(3):
    a = k * TAU / 3 + math.pi / 6
    box((0.035, 0.035, 0.22), loc=(0.135 * math.cos(a), 0.135 * math.sin(a), 0.46), rot=(0, 0, a), material=STONE)
# dak: breed, licht gebogen, zes hoeken met opgewipte puntjes
roof = lathe([(0.34, 0.58), (0.33, 0.62), (0.2, 0.7), (0.06, 0.76), (0.0, 0.77)], verts=6, material=STONE_D, phase=math.pi / 6)
deform(roof, lambda c: Vector((c.x, c.y, c.z + (0.03 if math.hypot(c.x, c.y) > 0.32 else 0))))
# sneeuwkap op het dak en knop
cap = lathe([(0.3, 0.635), (0.27, 0.68), (0.18, 0.75), (0.06, 0.81), (0.0, 0.82)], verts=8, material=SNOW, jitter=0.06, seed=3)
cap2 = sphere(0.06, loc=(0, 0, 0.85), seg=5, rings=3, material=STONE_D)
sphere(0.07, loc=(0, 0, 0.9), seg=5, rings=3, material=SNOW, scale=(1, 1, 0.6))
# sneeuwhoopje aan de voet
mound = lathe([(0.38, 0.0), (0.3, 0.05), (0.0, 0.07)], verts=7, material=SNOW, jitter=0.12, seed=5)
o = join_all('snow_lantern')
shade_smooth(o, 35)
report()
done('ice', 'snow_lantern', kind='edge', footprint=0.3,
     notes='Stenen sneeuwlantaarn (yukimi-doro) op drie poten met gloeiende lichtkamer (glow_window), zeshoekig dak met sneeuwkap en knop, sneeuwhoopje aan de voet')
