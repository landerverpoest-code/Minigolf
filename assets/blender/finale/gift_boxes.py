import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale'); from _deco import *

PURPLE = mat('royal_purple', '#5b2a86', rough=0.55)
CRIMSON = mat('crimson', '#b0213a', rough=0.55)
GOLD = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
WHITE = mat('marble', '#efe9f2', rough=0.35)


def gift(size, loc, yaw, body, ribbon, bow=True):
    w, d, h = size
    P = [box((w, d, h), loc=(0, 0, h / 2), material=body)]
    P.append(box((w + 0.01, 0.05, h + 0.01), loc=(0, 0, h / 2), material=ribbon))
    P.append(box((0.05, d + 0.01, h + 0.01), loc=(0, 0, h / 2), material=ribbon))
    if bow:
        for s in (-1, 1):
            l = sphere(1.0, seg=4, rings=2, material=ribbon, scale=(0.07, 0.035, 0.05), smooth=False)
            T(l, rot=(0, s * -30, 0), loc=(s * 0.06, 0, h + 0.035))
            P.append(l)
    o = join(P, 'gift')
    return T(o, rot=(0, 0, yaw), loc=loc)


gift((0.42, 0.42, 0.34), (0, 0, 0), 10, PURPLE, GOLD)
gift((0.28, 0.28, 0.22), (0.02, 0.0, 0.34), -15, CRIMSON, WHITE)
gift((0.3, 0.24, 0.2), (0.38, -0.12, 0), 35, WHITE, CRIMSON)
gift((0.2, 0.2, 0.16), (-0.33, -0.2, 0), -20, GOLD, PURPLE)
o = join_all('gift_boxes')
report()
done('finale', 'gift_boxes', kind='edge', footprint=0.4, center=True,
     notes='Stapeltje cadeaus: paars met gouden lint, rood met wit lint erbovenop, wit met rood en klein goud met paars, elk met strik')
