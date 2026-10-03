import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
iron = mat('iron', '#2b2733', rough=0.45, metal=0.6)
stone = mat('stone', '#8a958a', rough=0.9)
glow = mat('glow_lamp', '#ffd36a', rough=0.4, emit='#ffb53a', emit_strength=3.0)
moss = mat('moss', '#557f35', rough=1.0)
V = Vector
parts = []
# voet
parts.append(bev(cyl(0.26, 0.22, loc=(0, 0, 0.11), verts=8, material=stone), 0.02))
parts.append(cyl(0.15, 0.32, loc=(0, 0, 0.38), verts=8, r2=0.075, material=iron))
parts.append(cyl(0.1, 0.05, loc=(0, 0, 0.55), verts=8, material=iron))
# kromme paal met herdersstaf-boog
post = [V((0, 0, 0.5)), V((0.02, 0, 1.1)), V((0.09, 0, 1.7)), V((0.2, 0.02, 2.2)), V((0.22, 0.03, 2.55)), V((0.15, 0.03, 2.8)),
        V((0.0, 0.02, 2.93)), V((-0.2, 0.0, 2.95)), V((-0.36, 0.0, 2.88)), V((-0.42, 0.0, 2.8))]
parts.append(tube(post, r=[0.055, 0.05, 0.047, 0.044, 0.042, 0.04, 0.038, 0.036, 0.034, 0.03], seg=6, material=iron, smooth=True))
for z, p in [(1.1, V((0.02, 0, 1.1))), (1.95, V((0.15, 0.01, 1.95)))]:
    parts.append(cyl(0.07, 0.06, loc=p, verts=8, material=iron))
# krul onder de boog
sc = [V((0.2, 0.025, 2.35))] + [V((0.0 + 0.12 * math.cos(t) * (1 - t / 10), 0.025, 2.66 + 0.12 * math.sin(t) * (1 - t / 10))) for t in [-0.3, 0.6, 1.5, 2.4, 3.3, 4.2, 5.1, 6.0]]
parts.append(tube(sc, r=0.014, seg=4, material=iron, smooth=True))
# lantaarn (hangt, licht schuin)
top = V((-0.42, 0.0, 2.8))
lan = []
lan.append(cyl(0.012, 0.12, loc=top + V((0, 0, -0.06)), verts=4, material=iron))
lan.append(cyl(0.035, 0.03, loc=top + V((0, 0, -0.12)), verts=6, material=iron))
lan.append(cone(0.17, 0.13, loc=top + V((0, 0, -0.2)), verts=4, material=iron))
lan.append(box((0.2, 0.2, 0.03), loc=top + V((0, 0, -0.275)), rot=(0, 0, math.pi / 4), material=iron))
lan.append(cyl(0.11, 0.26, loc=top + V((0, 0, -0.42)), verts=4, r2=0.13, material=glow))
for k in range(4):
    a = math.pi / 4 + k * math.pi / 2 + math.pi / 4
    lan.append(box((0.025, 0.025, 0.28), loc=top + V((0.12 * math.cos(a), 0.12 * math.sin(a), -0.42)), rot=(0, 0, a), material=iron))
lan.append(cyl(0.12, 0.06, loc=top + V((0, 0, -0.58)), verts=4, r2=0.14, material=iron))
lan.append(cone(0.06, 0.08, loc=top + V((0, 0, -0.65)), rot=(math.pi, 0, 0), verts=4, material=iron))
L = join(lan, 'lantern')
T(L, rot=(math.radians(6), math.radians(-9), math.radians(45)), pivot=top)
parts.append(L)
parts.append(shade_smooth(ico(0.09, loc=(0.18, -0.12, 0.22), material=moss, scale=(1.4, 1.1, 0.5), jitter=0.015, seed=1)))
join(parts, 'crooked_lamp')
report()
finish('haunted', 'crooked_lamp', kind='scatter', footprint=0.3, notes='kromme ijzeren straatlantaarn met hangende lantaarn (glow_lamp)')
