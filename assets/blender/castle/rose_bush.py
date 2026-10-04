import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/castle'); from _deco import *

LEAF = mat('cypress_light', '#3a7438', rough=0.85)
LEAF_D = mat('cypress_dark', '#24502a', rough=0.85)
ROSE = mat('rose_red', '#e01e3c', rough=0.5)
ROSE_P = mat('rose_pink', '#f07a9a', rough=0.55)
STONE = mat('stone_warm', '#a69c8f', rough=0.9)

# bolle struik uit twee gefacetteerde lobben
b1 = ico(0.3, sub=2, material=LEAF, scale=(1.1, 1.0, 0.95), jitter=0.035, seed=3)
T(b1, loc=(0.04, 0.03, 0.3))
b2 = ico(0.22, sub=2, material=LEAF_D, scale=(1.1, 1.0, 0.9), jitter=0.03, seed=5)
T(b2, rot=(0, 0, 30), loc=(-0.2, -0.08, 0.2))
for b in (b1, b2):
    deform(b, lambda c: Vector((c.x, c.y, max(c.z, 0.0))))
    recolor(b, [LEAF, LEAF_D], lambda f: 1 if f.center.z < 0.14 or noise.noise(f.center * 5) > 0.35 else None)
    flat(b)
# rozen: bolletjes in twee kleuren, op het oppervlak
dirs = [((0.04, 0.03, 0.3), 0.31, (0.1, -1, 0.5)), ((0.04, 0.03, 0.3), 0.31, (0.8, -0.6, 0.3)), ((0.04, 0.03, 0.3), 0.31, (0.2, 0.1, 1)),
        ((0.04, 0.03, 0.3), 0.31, (0.9, 0.5, 0.4)), ((0.04, 0.03, 0.3), 0.31, (-0.3, 0.9, 0.5)),
        ((-0.2, -0.08, 0.2), 0.23, (-0.6, -0.8, 0.4)), ((-0.2, -0.08, 0.2), 0.23, (-0.8, 0.1, 0.7))]
for k, (c, r, d) in enumerate(dirs):
    d = Vector(d).normalized()
    p = Vector(c) + d * (r + 0.015)
    ro = ico(0.068, sub=1, material=ROSE if k % 3 else ROSE_P, scale=(1, 1, 0.7), smooth=True)
    orient(ro, d, p)
o = join_all('rose_bush')
report()
done('castle', 'rose_bush', kind='edge', footprint=0.38,
     notes='Rozenstruik: bolle gefacetteerde struik in twee groentinten met rode en roze rozen')
