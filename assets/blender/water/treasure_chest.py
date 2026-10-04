import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/water'); from _deco import *

WOOD = mat('wood', '#a8743e', rough=0.85)
WOOD_D = mat('wood_dark', '#77502c', rough=0.85)
GOLD = mat('gold', '#f5c542', rough=0.3, metal=0.6)
GEM = mat('gem_red', '#e8304a', rough=0.15, metal=0.1)
SAND = mat('sand', '#ead7a8', rough=0.95)

W, D, H = 0.62, 0.4, 0.3
# zandhoopje
sand = lathe([(0.48, 0.0), (0.4, 0.04), (0.0, 0.05)], verts=8, material=SAND, sx=1.25, sy=1.0, jitter=0.1, seed=4)
# kist
box((W, D, H), loc=(0, 0, 0.05 + H / 2), material=WOOD)
for x in (-W / 2 + 0.06, W / 2 - 0.06):
    box((0.045, D + 0.02, H + 0.01), loc=(x, 0, 0.05 + H / 2), material=GOLD)
box((W + 0.02, D + 0.02, 0.04), loc=(0, 0, 0.07), material=WOOD_D)
box((0.07, 0.03, 0.09), loc=(0, -D / 2 - 0.01, 0.05 + H - 0.04), material=GOLD)
# open deksel (halve ton) naar achteren gekanteld
lid = lathe([(D / 2, -W / 2), (D / 2, W / 2)], verts=8, material=WOOD, cap0=True, cap1=True)
deform(lid, lambda c: Vector((c.x, c.y, max(c.z, 0.0))) if False else c)
lid_bm = lid
clip = clip_below
T(lid, rot=(0, 90, 0))
deform(lid, lambda c: Vector((c.x, c.y, max(c.z, 0.0))))
T(lid, rot=(-105, 0, 0), pivot=(0, 0, 0))
T(lid, loc=(0, D / 2, 0.05 + H))
for x in (-W / 2 + 0.06, W / 2 - 0.06):
    band = lathe([(D / 2 + 0.008, -0.022), (D / 2 + 0.008, 0.022)], verts=8, material=GOLD, cap0=False, cap1=False)
    T(band, rot=(0, 90, 0))
    deform(band, lambda c: Vector((c.x, c.y, max(c.z, 0.0))))
    T(band, rot=(-105, 0, 0))
    T(band, loc=(x, D / 2, 0.05 + H))
# goudberg met munten en juweel
heap = blob([((0, 0, 0.3), 0.2), ((0.15, 0.02, 0.29), 0.15), ((-0.15, -0.02, 0.29), 0.15)], center=(0, 0, 0.27), sub=2, material=GOLD, smooth=False)
jitter(heap, 0.02, seed=3)
deform(heap, lambda c: Vector((max(-W / 2 + 0.02, min(W / 2 - 0.02, c.x)), max(-D / 2 + 0.02, min(D / 2 - 0.02, c.y)), max(c.z, 0.25))))
ico(0.045, loc=(0.05, -0.06, 0.48), sub=1, material=GEM)
for k, (x, y, a) in enumerate(((0.38, -0.25, 20), (-0.36, -0.3, 70), (0.25, -0.38, 50))):
    c = cyl(0.035, 0.012, verts=5, material=GOLD, rot=(math.radians(a * 0.3), 0, 0))
    T(c, loc=(x, y, 0.055))
o = join_all('treasure_chest')
report()
done('water', 'treasure_chest', kind='edge', footprint=0.4, center=True,
     notes='Open schatkist op een zandhoopje: houten kist met gouden banden en slot, deksel naar achteren open, berg goud met rood juweel, losse munten')
