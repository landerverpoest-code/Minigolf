import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
purple = mat('royal_purple', '#4a2270', rough=0.5)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
marble = mat('marble', '#efe9f2', rough=0.35)
glow = mat('glow_lantern', '#ffb040', rough=0.4, emit='#ff9a1a', emit_strength=2.2)
V = Vector
P = []
P.append(box((0.5, 0.5, 0.2), loc=(0, 0, 0.1), material=marble, bevel=0.03))
P.append(lathe([(0.17, 0.2), (0.14, 0.35), (0.08, 0.5), (0.065, 2.3), (0.09, 2.36), (0.09, 2.42)], seg=8, material=purple, smooth=False))
for z in (0.42, 1.2, 2.0):
    P.append(cyl(0.09, 0.05, loc=(0, 0, z), verts=8, material=gold))
P.append(lathe([(0.09, 2.42), (0.06, 2.55), (0.0, 2.62)], seg=8, material=gold))
P.append(ico(0.05, loc=(0, 0, 2.66), sub=1, material=gold, smooth=True))
# sierlijke arm met krul
arm = smooth_path([V((0, 0, 2.15)), V((0.25, 0, 2.3)), V((0.5, 0, 2.32)), V((0.62, 0, 2.24))], 2)
P.append(tube(arm, r=0.025, seg=5, material=gold, smooth=True))
cur = [V((0.05, 0, 2.0))] + [V((0.22 + 0.1 * math.cos(t) * (1 - t / 11), 0, 2.13 + 0.1 * math.sin(t) * (1 - t / 11))) for t in [3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 9.6]]
P.append(tube(cur, r=0.016, seg=4, material=gold, smooth=True))
# hangende lantaarn (zeshoekig)
top = V((0.62, 0, 2.22))
P.append(cyl(0.012, 0.12, loc=top + V((0, 0, -0.06)), verts=4, material=gold))
P.append(cone(0.16, 0.14, loc=top + V((0, 0, -0.19)), verts=6, material=purple))
P.append(ico(0.03, loc=top + V((0, 0, -0.1)), sub=1, material=gold))
P.append(cyl(0.17, 0.03, loc=top + V((0, 0, -0.27)), verts=6, material=gold))
P.append(cyl(0.12, 0.3, loc=top + V((0, 0, -0.43)), verts=6, r2=0.14, material=glow))
for k in range(6):
    a = k * TAU / 6
    P.append(box((0.022, 0.022, 0.3), loc=top + V((0.14 * math.cos(a), 0.14 * math.sin(a), -0.43)), material=gold))
P.append(cyl(0.13, 0.04, loc=top + V((0, 0, -0.6)), verts=6, material=gold))
P.append(cone(0.08, 0.1, loc=top + V((0, 0, -0.67)), rot=(math.pi, 0, 0), verts=6, material=purple))
join(P, 'lantern_post')
report()
finish('finale', 'lantern_post', kind='scatter', footprint=0.3, notes='sierlijke paars/gouden lantaarnpaal met hangende glow_lantern')
