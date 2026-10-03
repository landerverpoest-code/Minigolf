import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
stalk = mat('alien_stalk', '#5b3fa0', rough=0.6)
leaf = mat('alien_leaf', '#22a69a', rough=0.6)
bulb = mat('glow_bulb', '#d020b8', rough=0.3, emit='#ff3ae0', emit_strength=1.2)
rockm = mat('alien_rock', '#343a58', rough=0.9)
V = Vector
P = [rock(0.13, loc=(0, 0, 0), sub=1, material=rockm, scale=(1.3, 1.2, 0.5), jit=0.15, seed=2)]
for k, (a, el, L, curl, s) in enumerate([(0.3, 1.42, 0.85, 1.25, 0.06), (2.4, 1.2, 0.62, 1.4, 0.05), (4.3, 1.15, 0.7, 1.3, 0.055)]):
    d = V((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el)))
    ax = d.cross(V((0, 0, 1))) * (1 if k % 2 else -1)
    pts = grow(V((0, 0, 0.03)), d, L, 5, ax, 0.0, curl, seed=k, wob=0.03, shrink=0.25)
    P.append(tube(pts, r=taper(len(pts), 0.024, 0.011, 0.007), seg=4, material=stalk, smooth=True))
    P.append(ico(s, loc=pts[-1], sub=1, material=bulb, smooth=True))
    if k == 0:
        P.append(ico(s * 0.55, loc=pts[2] + V((0.02, 0, 0.0)), sub=1, material=bulb, smooth=True))
for k, a in enumerate([0.9, 3.0, 5.0]):
    d = V((math.cos(a), math.sin(a), 0.7))
    pts = grow(V((0, 0, 0.04)), d, 0.3, 2, d.cross(V((0, 0, 1))), 0.4, 0.6, seed=k + 9, wob=0.02)
    P.append(tube(pts, r=[0.03, 0.06, 0.0], seg=3, material=leaf, smooth=False, sx=0.3, phase=math.pi / 2))
T(join(P, 'alien_plant'), scale=1.35)
report()
finish('space', 'alien_plant', kind='edge', footprint=0.38, notes='krullende buitenaardse plant met gloeiende bolletjes (glow_bulb)')
