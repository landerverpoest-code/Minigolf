import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
white = mat('golfball_white', '#f6f6f2', rough=0.45)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#b0213a', rough=0.55)
purple = mat('royal_purple', '#5b2a86', rough=0.55)
grass = mat('grass', '#5fae3a', rough=0.9)
V = Vector
P = []
# gras-sokkel met paarse rand en gouden plaquette
P.append(bev(cyl(1.6, 0.4, loc=(0, 0, 0.2), verts=12, material=purple, r2=1.5), 0.04))
P.append(cyl(1.535, 0.07, loc=(0, 0, 0.405), verts=12, material=gold))
P.append(cyl(1.47, 0.08, loc=(0, 0, 0.43), verts=12, material=grass))
P.append(box((0.8, 0.05, 0.22), loc=(0, -1.52, 0.2), rot=(-0.08, 0, 0), material=gold))
# tee
P.append(lathe([(0.16, 0.42), (0.13, 0.9), (0.18, 1.25), (0.55, 1.48), (0.6, 1.55), (0.0, 1.5)], seg=12, material=crimson, smooth=True))
# golfbal met kuiltjes: ico, hoekpunten afschuinen -> zeshoekige vlakjes, die naar binnen duwen
R = 1.25
ball = ico(R, sub=3, material=white)
bake(ball)
bm = bmesh.new(); bm.from_mesh(ball.data)
orig = set(f.index for f in bm.faces)
res = bmesh.ops.bevel(bm, geom=bm.verts[:], offset=34, offset_type='PERCENT', affect='VERTICES', segments=1)
newf = res['faces']
bmesh.ops.inset_individual(bm, faces=newf, thickness=0.03, depth=-0.05)
bm.to_mesh(ball.data); bm.free()
shade_smooth(ball, 14)
T(ball, loc=(0, 0, 1.52 + R * 0.97))
P.append(ball)
join(P, 'golf_ball_statue')
report()
finish('finale', 'golf_ball_statue', kind='hero', footprint=1.6, notes='reuze golfbal met zeshoekige kuiltjes (geometrie) op een rode tee en grassokkel')
