import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
marble = mat('marble', '#efe9f2', rough=0.35)
purple = mat('royal_purple', '#5b2a86', rough=0.55)
crimson = mat('crimson', '#b0213a', rough=0.6)
white = mat('golfball_white', '#f6f6f2', rough=0.5)
V = Vector
P = []
# marmeren sokkel met paarse randen en gouden plaquette
P.append(box((2.5, 2.5, 0.35), loc=(0, 0, 0.175), material=purple, bevel=0.05))
P.append(box((2.1, 2.1, 0.95), loc=(0, 0, 0.82), material=marble, bevel=0.04))
P.append(box((2.3, 2.3, 0.18), loc=(0, 0, 1.38), material=purple, bevel=0.04))
P.append(box((2.15, 2.15, 0.06), loc=(0, 0, 0.4), material=gold))
P.append(box((1.1, 0.06, 0.45), loc=(0, -1.06, 0.84), material=gold, bevel=0.015))
P.append(box((0.8, 0.02, 0.06), loc=(0, -1.095, 0.92), material=purple))
P.append(box((0.6, 0.02, 0.05), loc=(0, -1.095, 0.78), material=purple))
# beker (gedraaid profiel)
z0 = 1.47
cup = lathe([(0.0, 0.0), (0.75, 0.0), (0.78, 0.1), (0.55, 0.18), (0.3, 0.3), (0.2, 0.55), (0.34, 0.72), (0.34, 0.8), (0.2, 0.95), (0.22, 1.1),
             (0.6, 1.3), (0.95, 1.65), (1.12, 2.15), (1.15, 2.6), (1.25, 2.72), (1.2, 2.78), (1.05, 2.7), (1.0, 2.45), (0.0, 2.3)],
            seg=20, material=gold, smooth=True, loc=(0, 0, z0), cap_top=False, cap_bot=False)
shade_smooth(cup, 40)
P.append(cup)
# grote gekrulde handvatten
for sx in (-1, 1):
    pts = [V((sx * 1.05, 0, z0 + 2.35)), V((sx * 1.55, 0, z0 + 2.5)), V((sx * 1.85, 0, z0 + 2.2)), V((sx * 1.75, 0, z0 + 1.75)), V((sx * 1.4, 0, z0 + 1.45)),
           V((sx * 1.05, 0, z0 + 1.4)), V((sx * 0.9, 0, z0 + 1.55)), V((sx * 1.05, 0, z0 + 1.68)), V((sx * 1.2, 0, z0 + 1.6))]
    P.append(tube(smooth_path(pts, 3), r=interp([0.09, 0.1, 0.1, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05], 3), seg=6, material=gold, smooth=True))
# golfbal in de beker
ball = ico(0.62, sub=3, material=white, smooth=True)
T(ball, loc=(0.1, -0.05, z0 + 2.75))
P.append(ball)
# rode strik rond de voet
P.append(torus(0.24, 0.06, loc=(0, 0, z0 + 0.88), seg=12, ring=4, material=crimson, smooth=True))
for sx in (-1, 1):
    bow = prism([(0, 0), (sx * 0.32, 0.16), (sx * 0.32, -0.16)], 0.06, crimson, axis='y', loc=(0, -0.26, z0 + 0.88))
    P.append(bow)
    tail = prism([(0, 0), (sx * 0.12, -0.5), (sx * 0.05, -0.42), (sx * -0.02, -0.5)], 0.04, crimson, axis='y', loc=(sx * 0.03, -0.27, z0 + 0.86))
    P.append(tail)
P.append(ico(0.08, loc=(0, -0.29, z0 + 0.88), sub=1, material=crimson))
# gouden ster op de voorkant van de beker
star = [(0.25 * (1 if i % 2 == 0 else 0.45) * math.sin(i * math.pi / 5), 0.25 * (1 if i % 2 == 0 else 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
st = prism(star, 0.05, purple, axis='z')
place_on(st, cup, (0, -1, 0), center=(0, 0, z0 + 1.95), sink=0.0)
P.append(st)
join(P, 'trophy')
report()
finish('finale', 'trophy', kind='hero', footprint=1.3, notes='reuze gouden golftrofee met golfbal, gekrulde handvatten en rode strik op marmeren sokkel')
