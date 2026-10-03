import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _cactus import *

M = cactus_mats()
R = 0.28
pts = [(0, 0, -0.02), (0, 0, 0.5), (0.01, 0, 1.2), (0.02, 0.01, 2.0), (0.02, 0.0, 2.7), (0.0, 0.0, 3.2)]
rads = [R * 1.08, R, R * 0.99, R * 0.97, R * 0.95, R * 0.92]
dome_end(pts, rads, R * 0.92)
trunk = stem(pts, rads, M, verts=10, ribs=0.09)
a1, t1 = arm(0.2, 1.25, out=0.62, up=1.15, r=0.18, trunk_r=R, M=M)
a2, t2 = arm(math.pi + 0.35, 1.7, out=0.55, up=0.85, r=0.16, trunk_r=R, M=M)
a3, t3 = arm(-1.9, 2.25, out=0.42, up=0.5, r=0.12, trunk_r=R, M=M, verts=8, elbow=0.15)
flower(Vector(pts[-1]) + Vector((0.0, 0.0, -0.02)), M, s=1.7)
flower(Vector(pts[-1]) + Vector((0.12, -0.1, -0.12)), M, s=1.4, n_dir=Vector((0.6, -0.5, 0.6)))
flower(t1 + Vector((0, 0, -0.03)), M, s=1.4)
# zandhoopje + steentjes
mound = lathe([(0.75, 0.0), (0.6, 0.06), (0.35, 0.1), (0.0, 0.11)], verts=10, material=M['sand'], jitter=0.08, seed=2)
for k, (x, y) in enumerate([(0.5, -0.35), (-0.45, 0.4)]):
    rock(0.09 + 0.03 * k, loc=(x, y, 0.03), scale=(1.3, 1.0, 0.7), seed=k, jitter=0.2, material=M['dark'])
join_all('saguaro_cactus')
report()
finish('desert', 'saguaro_cactus', kind='scatter', footprint=0.5,
       notes='Hoge geribde saguaro met drie armen en witte bloemetjes op een zandhoopje')
closeup('saguaro_cactus')
