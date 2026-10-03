import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

ICE = mat('ice', '#5fd2f2', rough=0.12, emit='#1aa8e0', emit_strength=0.3)
ICE2 = mat('ice_pale', '#b8ecff', rough=0.12, emit='#6fd0ff', emit_strength=0.2)
GLOW = mat('glow_ice', '#7ff4ff', rough=0.1, emit='#22d8ff', emit_strength=1.6)
SNOW = mat('snow', '#eef6ff', rough=0.7)
rnd = random.Random(12)


def spike(base, h, r, tilt=(0, 0), twist=1.2, material=ICE, verts=6, seed=0):
    prof = [(r, 0.0), (r * 0.86, h * 0.22), (r * 0.62, h * 0.5), (r * 0.34, h * 0.78), (0.0, h)]
    o = lathe(prof, verts=verts, material=material, jitter=0.08, seed=seed, cap0=True)
    for v in o.data.vertices:
        a = twist * v.co.z / h
        x, y = v.co.x, v.co.y
        v.co.x = x * math.cos(a) - y * math.sin(a); v.co.y = x * math.sin(a) + y * math.cos(a)
    place(o, loc=base, rot=(tilt[0], tilt[1], 0))
    return o

# hoofdpiek + kleinere pieken, allemaal met voet binnen r=0.3
spike((0, 0, 0.0), 1.85, 0.235, tilt=(0.02, 0.03), material=ICE, verts=7, seed=1)
spike((0.1, 0.08, 0.0), 1.2, 0.15, tilt=(-0.1, 0.12), material=ICE2, seed=2)
spike((-0.12, 0.06, 0.0), 0.95, 0.14, tilt=(-0.08, -0.14), material=ICE, seed=3)
spike((0.02, -0.13, 0.0), 0.8, 0.13, tilt=(0.14, 0.02), material=ICE2, seed=4)
spike((-0.08, -0.1, 0.0), 0.55, 0.08, tilt=(0.1, -0.12), material=GLOW, seed=5)
spike((0.15, -0.07, 0.0), 0.45, 0.07, tilt=(0.08, 0.2), material=GLOW, seed=6)
# sneeuwkraag aan de voet (r <= 0.31)
collar = lathe([(0.31, 0.0), (0.27, 0.07), (0.17, 0.12), (0.0, 0.13)], verts=10, material=SNOW, jitter=0.03, seed=2)
shade_smooth(collar, 60)
join_all('icicle_post')
o = bpy.context.scene.objects['icicle_post']
lo, hi = bounds()
rmax = max((Vector((v.co.x, v.co.y)).length for v in o.data.vertices if v.co.z - lo.z < 0.6))
print('FOOT rmax(0-0.6m)=%.3f' % rmax)
report()
finish('ice', 'icicle_post', kind='post', footprint=0.32,
       notes='Cluster ijspieken (stalagmieten) als paal-obstakel, binnen r=0.32 tot 0.6 m; kleine pieken gloeien (glow_ice)')
closeup('icicle_post')
