import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
stone = mat('stone', '#8a958a', rough=0.9)
dark = mat('stone_dark', '#5e6a63', rough=0.95)
moss = mat('moss', '#557f35', rough=1.0)
crack = mat('crack', '#262a2c', rough=1.0)

# kruisvormige steen
a, b = 0.07, 0.22   # halve breedte stam / arm
z0, z1, z2, z3 = 0.0, 0.36, 0.49, 0.64
poly = [(-a, z0), (a, z0), (a, z1), (b, z1), (b, z2), (a, z2), (a, z3), (-a, z3),
        (-a, z2), (-b, z2), (-b, z1), (-a, z1)]
cross = prism(poly, 0.1, stone, axis='y', loc=(0, 0, 0.12), bevel=0.014)
ck = tube([(0.03, -0.058, 0.76), (0.0, -0.058, 0.7), (0.03, -0.058, 0.64), (-0.01, -0.058, 0.53), (-0.06,-0.058,0.5)],
          r=[0.003, 0.01, 0.009, 0.008, 0.003], seg=3, material=crack, smooth=False, sx=0.6)
m1 = shade_smooth(ico(0.06, loc=(-0.17, 0.0, 0.615), material=moss, scale=(1.5, 1.1, 0.45), jitter=0.01, seed=5))
c = join([cross, ck, m1], 'cross')
T(c, rot=(math.radians(-4), math.radians(-10), math.radians(-6)), pivot=(0, 0, 0.12))
# getrapte voet
b1 = box((0.42, 0.26, 0.07), loc=(0, 0, 0.035), material=dark)
b2 = box((0.28, 0.18, 0.06), loc=(0, 0, 0.1), material=stone, bevel=0.012)
# afgebroken stuk in het gras
piece = box((0.09, 0.07, 0.06), loc=(0.27, -0.12, 0.03), rot=(0.2, 0.1, 0.6), material=stone)
jitter(piece, 0.008, 2)
m2 = shade_smooth(ico(0.07, loc=(0.18, 0.1, 0.07), material=moss, scale=(1.5, 1.0, 0.5), jitter=0.01, seed=6))
m3 = shade_smooth(ico(0.05, loc=(-0.19, -0.11, 0.07), material=moss, scale=(1.4, 1.0, 0.5), jitter=0.01, seed=7))
join([c, b1, b2, piece, m2, m3], 'tombstone_b')
report()
finish('haunted', 'tombstone_b', kind='edge', footprint=0.35, notes='kruisvormige grafsteen, scheef, barst, afgebroken stuk, mos')
