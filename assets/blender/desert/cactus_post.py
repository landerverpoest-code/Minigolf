import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _cactus import *

M = cactus_mats()
R = 0.25
pts = [(0, 0, -0.02), (0, 0, 0.4), (0.0, 0, 0.9), (0.01, 0.0, 1.4), (0.0, 0.0, 1.75)]
rads = [R * 1.04, R, R, R * 0.97, R * 0.94]
dome_end(pts, rads, R * 0.94)
trunk = stem(pts, rads, M, verts=10, ribs=0.09)
a1, t1 = arm(0.5, 0.85, out=0.46, up=0.75, r=0.14, trunk_r=R, M=M, elbow=0.18)
a2, t2 = arm(math.pi + 0.7, 1.15, out=0.42, up=0.55, r=0.12, trunk_r=R, M=M, elbow=0.15)
flower(Vector(pts[-1]) + Vector((0, 0, -0.02)), M, s=1.6)
flower(t1 + Vector((0, 0, -0.02)), M, s=1.2)
flower(Vector(pts[-1]) + Vector((-0.12, 0.1, -0.1)), M, s=1.1, n_dir=Vector((-0.6, 0.5, 0.6)))
# kraag van zand en steentjes, binnen r = 0.33
collar = lathe([(0.33, 0.0), (0.3, 0.05), (0.2, 0.09), (0.0, 0.1)], verts=10, material=M['sand'], jitter=0.02, seed=4)
join_all('cactus_post')
o = bpy.context.scene.objects['cactus_post']
lo, hi = bounds()
rmax = max((Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z - lo.z < 0.6))
rall = max((Vector((v.co.x, v.co.y)).length for v in o.data.vertices))
print('FOOT rmax(0-0.6m)=%.3f  rmax(all)=%.3f' % (rmax, rall))
report()
finish('desert', 'cactus_post', kind='post', footprint=0.34,
       notes='Zuilcactus als paal-obstakel: binnen r=0.34 tot 0.6 m, armen hoger op binnen r~0.6')
closeup('cactus_post')
