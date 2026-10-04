import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/water'); from _deco import *

WOOD = mat('wood_dark', '#77502c', rough=0.85)
ROPE = mat('rope', '#e8d6a8', rough=0.9)
WHITE = mat('gull_white', '#f6f4ee', rough=0.6)
GREY = mat('gull_grey', '#9aa6b2', rough=0.6)
BEAK = mat('beak_yellow', '#ffc23a', rough=0.5)

# verweerde meerpaal: licht schuin, afgeschuinde kop
post = lathe([(0.13, 0.0), (0.14, 0.5), (0.13, 0.85), (0.1, 0.9), (0.0, 0.92)], verts=7, material=WOOD, jitter=0.06, seed=2)
T(post, rot=(3, -2, 0))
# touwlussen om de paal
for z in (0.42, 0.5):
    torus(0.145, 0.025, loc=(0, 0.0, z), rot=(0.05, 0, 0), seg=7, ring=3, material=ROPE, smooth=True)
rope_end = tube([(0.14, -0.02, 0.44), (0.24, -0.1, 0.28), (0.28, -0.14, 0.02), (0.38, -0.08, 0.01)], [0.022] * 4, verts=3, material=ROPE)
# meeuw bovenop, kijkt schuin naar -Y
G = []
body = sphere(1.0, seg=6, rings=4, material=WHITE, scale=(0.07, 0.13, 0.07))
deform(body, lambda c: Vector((c.x, c.y, c.z + 0.04 * max(0, c.y / 0.13))))
T(body, rot=(-10, 0, 0), loc=(0, 0.01, 1.04))
G.append(body)
for s in (-1, 1):
    w = mesh_obj([(s * 0.06, -0.06, 1.08), (s * 0.075, 0.05, 1.09), (s * 0.05, 0.2, 1.1), (s * 0.03, 0.05, 1.12)], [(0, 1, 2, 3)], GREY, 'wing')
    G.append(w)
    G.append(rod((s * 0.03, 0.0, 0.92), (s * 0.03, 0.0, 0.99), r=0.008, verts=3, material=BEAK))
G.append(sphere(0.05, loc=(0, -0.11, 1.15), seg=6, rings=4, material=WHITE))
G.append(cone(0.016, 0.07, loc=(0, -0.18, 1.14), rot=(math.pi / 2 + 0.15, 0, 0), verts=4, material=BEAK))
for s in (-1, 1):
    G.append(sphere(0.009, loc=(s * 0.035, -0.14, 1.17), seg=3, rings=2, material=WOOD))
g = join(G, 'gull')
T(g, rot=(0, 0, 25), scale=1.45, pivot=(0, 0, 0.92))
o = join_all('seagull_post')
report()
done('water', 'seagull_post', kind='edge', footprint=0.25,
     notes='Verweerde houten meerpaal met touwlussen en losse touweinde, met een meeuw (wit lijf, grijze vleugels, gele snavel) bovenop')
