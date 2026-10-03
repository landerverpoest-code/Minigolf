import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
marble = mat('marble', '#efe9f2', rough=0.35)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
purple = mat('royal_purple', '#5b2a86', rough=0.55)
fire = mat('glow_fire', '#ff8a20', rough=0.4, emit='#ff6a10', emit_strength=2.5)
V = Vector
P = []
P.append(box((0.95, 0.95, 0.25), loc=(0, 0, 0.125), material=purple, bevel=0.03))
P.append(box((0.8, 0.8, 0.15), loc=(0, 0, 0.32), material=marble, bevel=0.02))
P.append(lathe([(0.36, 0.4), (0.38, 0.47), (0.33, 0.55), (0.3, 0.6)], seg=16, material=gold, smooth=True))
# gecanneleerde schacht
seg = 24
flute = lambda a, z: 1.0 - 0.09 * (round(a / (TAU / seg)) % 2)
P.append(lathe([(0.3, 0.6), (0.29, 1.8), (0.26, 3.05)], seg=seg, material=marble, rfn=flute, cap_bot=False, cap_top=False))
# gouden kapiteel (Korinthisch-achtig: uitlopend met blaadjes)
P.append(lathe([(0.28, 3.05), (0.3, 3.12), (0.32, 3.18), (0.45, 3.42), (0.48, 3.48)], seg=12, material=gold, smooth=False))
for k in range(8):
    a = k * TAU / 8
    lf = prism([(-0.07, 0), (0.07, 0), (0.0, 0.3)], 0.03, gold, axis='y')
    T(lf, rot=(-0.45, 0, a + math.pi / 2), loc=(0.3 * math.cos(a), 0.3 * math.sin(a), 3.13))
    P.append(lf)
P.append(box((0.98, 0.98, 0.14), loc=(0, 0, 3.55), material=gold, bevel=0.025))
# vuurschaal
P.append(cyl(0.12, 0.2, loc=(0, 0, 3.72), verts=8, material=purple))
P.append(lathe([(0.1, 3.8), (0.32, 3.88), (0.44, 4.05), (0.4, 4.08), (0.0, 3.98)], seg=10, material=gold, smooth=False))
flames = [(0.0, 0.0, 0.55, 0.22), (0.12, 0.08, 0.38, 0.14), (-0.13, 0.05, 0.4, 0.15), (0.03, -0.14, 0.34, 0.13)]
for k, (x, y, h, r) in enumerate(flames):
    pts = [V((x, y, 3.98)), V((x * 1.1 + 0.02, y, 3.98 + h * 0.4)), V((x * 0.8 - 0.03, y + 0.02, 3.98 + h * 0.75)), V((x * 0.6 + 0.02, y, 3.98 + h))]
    P.append(tube(pts, r=[r, r * 0.8, r * 0.4, 0.0], seg=5, material=fire, smooth=False))
join(P, 'gold_column')
report()
finish('finale', 'gold_column', kind='scatter', footprint=0.5, notes='gecanneleerde marmeren zuil met gouden kapiteel en vuurschaal (glow_fire)')
