import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/castle'); from _deco import *

WOOD = mat('wood', '#9a6538', rough=0.8)
WOOD_D = mat('wood_dark', '#6e4528', rough=0.85)
IRON = mat('iron', '#3d3d42', rough=0.5, metal=0.4)
ROPE = mat('rope', '#d9bf8c', rough=0.95)
STONE = mat('stone_warm', '#a69c8f', rough=0.9)

# frame langs Y, werparm slaat naar -Y (voorkant)
L, W, FZ = 1.9, 0.9, 0.42
for sx in (-1, 1):
    plank((sx * W / 2, -L / 2, FZ), (sx * W / 2, L / 2, FZ), w=0.12, t=0.12, material=WOOD_D)
for y in (-L / 2 + 0.12, 0.15, L / 2 - 0.12):
    plank((-W / 2 - 0.06, y, FZ + 0.1), (W / 2 + 0.06, y, FZ + 0.1), w=0.1, t=0.08, material=WOOD)
# A-bok met dwarsbalk (aanslag voor de arm)
for sx in (-1, 1):
    x = sx * W / 2
    plank((x, -0.45, FZ + 0.06), (x, -0.05, 1.45), w=0.1, t=0.1, material=WOOD)
    plank((x, 0.4, FZ + 0.06), (x, -0.05, 1.45), w=0.1, t=0.1, material=WOOD)
plank((-W / 2 - 0.08, -0.07, 1.42), (W / 2 + 0.08, -0.07, 1.42), w=0.13, t=0.13, material=WOOD_D)
# kussentje (stro/touw) tegen de dwarsbalk
cyl(0.08, 0.3, loc=(0, -0.16, 1.42), rot=(0, math.pi / 2, 0), verts=6, material=ROPE)
# draaias + werparm (schuin naar achter, emmer achteraan)
rod((-W / 2 - 0.05, 0.35, FZ + 0.22), (W / 2 + 0.05, 0.35, FZ + 0.22), r=0.05, verts=6, material=IRON)
arm = plank((0, 0.25, FZ + 0.12), (0, 1.25, FZ + 0.6), w=0.11, t=0.09, material=WOOD)
taper(arm, 0.8) if False else None
plank((0, -0.02, FZ + 0.0), (0, 0.32, FZ + 0.2), w=0.13, t=0.1, material=WOOD)
# emmer met steen
cup = lathe([(0.12, 0.0), (0.2, 0.1), (0.22, 0.14), (0.18, 0.14), (0.15, 0.06), (0.0, 0.06)], verts=8, material=WOOD_D, cap0=True, cap1=False)
T(cup, rot=(-25, 0, 0), loc=(0, 1.3, FZ + 0.62))
ball = ico(0.15, sub=1, material=STONE, jitter=0.02, seed=3)
T(ball, loc=(0, 1.32, FZ + 0.8))
# lier met touw achteraan
drum = cyl(0.1, 0.5, verts=8, material=ROPE, rot=(0, math.pi / 2, 0), loc=(0, 0.75, FZ + 0.18))
for sx in (-1, 1):
    cyl(0.13, 0.04, verts=8, material=WOOD_D, rot=(0, math.pi / 2, 0), loc=(sx * 0.27, 0.75, FZ + 0.18))
    # spaken van de lierhendel
    plank((sx * 0.5, 0.75, FZ + 0.18 - 0.22), (sx * 0.5, 0.75, FZ + 0.18 + 0.22), w=0.04, t=0.04, up=(1, 0, 0), material=WOOD)
rod((0, 0.75, FZ + 0.25), (0, 1.0, FZ + 0.47), r=0.022, verts=4, material=ROPE)
# ijzeren beslag op de arm
for t in (0.45, 0.8):
    p = Vector((0, 0.25, FZ + 0.12)).lerp(Vector((0, 1.25, FZ + 0.6)), t)
    box((0.13, 0.04, 0.11), loc=p, rot=(-0.45, 0, 0), material=IRON)
# wielen
R = 0.32
for sx in (-1, 1):
    for y in (-L / 2 + 0.3, L / 2 - 0.3):
        disc = cyl(R, 0.09, verts=10, material=WOOD)
        tire = lathe([(R + 0.012, -0.05), (R + 0.012, 0.05)], verts=10, material=IRON, cap0=False, cap1=False)
        hub = cyl(0.075, 0.16, verts=6, material=WOOD_D)
        brace = box((R * 1.7, 0.07, 0.12), material=WOOD_D)
        sp = [disc, tire, hub, brace]
        w_ = join(sp, 'wheel')
        T(w_, rot=(0, 90, 0), loc=(sx * (W / 2 + 0.12), y, R + 0.015))
# reservestenen naast het frame
for k, (x, y) in enumerate(((0.75, -0.6), (0.8, -0.35), (0.62, -0.47))):
    b = ico(0.12, sub=1, material=STONE, jitter=0.02, seed=10 + k)
    T(b, loc=(x, y, 0.1 + (0.1 if k == 2 else 0)))
o = join_all('catapult')
shade_smooth(o, 40)
report()
done('castle', 'catapult', kind='scatter', footprint=1.2, center=True,
     notes='Houten katapult: frame op vier spaakwielen met ijzeren band, A-bok met dwarsbalk en strokussen, werparm met beslag en emmer met steen, lier met touw, stapeltje reservestenen; werpt naar -Y')
