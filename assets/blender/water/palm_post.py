import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _palm import *

M = palm_mats()
sand = mat('sand', '#e9cf94', rough=0.95)
# stam blijft binnen r=0.3 op 0-0.6 m (flare 0.17*1.6 = 0.27)
parts, top = palm(M, height=3.55, lean=(0.55, -0.15), r0=0.17, r1=0.11, segs=8, fronds=8, up_fronds=2, flen=2.1,
                  fwidth=0.45, frise=0.75, fdroop=0.9, seed=7)
# klein zandheuveltje rond de voet (r <= 0.29)
mound = lathe([(0.28, 0.0), (0.26, 0.06), (0.2, 0.12), (0.0, 0.13)], verts=9, material=sand, jitter=0.02, seed=2)
join_all('palm_post')
report()
lo, hi = bounds()
# controle footprint
import bmesh
o = bpy.context.scene.objects['palm_post']
rmax = max((Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z - lo.z < 0.6))
print('FOOT rmax(0-0.6m)=%.3f' % rmax)
finish('water', 'palm_post', kind='post', footprint=0.3, notes='Palm als paal-obstakel: stam binnen r=0.3 tot 0.6 m, brede kroon boven 2.5 m')
closeup('palm_post')
