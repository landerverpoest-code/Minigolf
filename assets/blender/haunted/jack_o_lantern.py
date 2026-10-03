import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
orange = mat('pumpkin', '#d95d0e', rough=0.5)
stem = mat('stem', '#5a6328', rough=0.9)
glow = mat('glow_pumpkin', '#ffd040', rough=0.5, emit='#ffc21a', emit_strength=3.0)

seg = 14
ribs = lambda a, z: 1.0 - 0.12 * (round((a + math.pi / 2) / (TAU / seg)) % 2)
body = lathe([(0, 0.035), (0.15, 0.0), (0.225, 0.075), (0.238, 0.165), (0.205, 0.265), (0.125, 0.322), (0.05, 0.338), (0, 0.315)],
             seg=seg, material=orange, smooth=True, phase=-math.pi / 2, rfn=ribs)
T(body, scale=(1.08, 0.98, 0.92))
flat(body); shade_smooth(body, 25)
# gesneden gezicht (gloeit)
eyeL = [(-0.15, 0.165), (-0.035, 0.17), (-0.08, 0.245)]
eyeR = [(0.035, 0.17), (0.15, 0.165), (0.08, 0.245)]
nose = [(-0.025, 0.125), (0.025, 0.125), (0.0, 0.16)]
mouth = [(-0.16, 0.115), (-0.1, 0.075), (-0.07, 0.09), (-0.04, 0.06), (0.0, 0.08), (0.04, 0.06), (0.07, 0.09), (0.1, 0.075), (0.16, 0.115),
         (0.11, 0.1), (0.075, 0.115), (0.04, 0.095), (0.0, 0.11), (-0.04, 0.095), (-0.075, 0.115), (-0.11, 0.1)]
face = join([poly_face(p, glow) for p in (eyeL, eyeR, nose, mouth)], 'face')
project(face, body, (0, 1, 0), offset=0.004)
# steel + krul
st = tube([(0, 0, 0.3), (0.0, 0.0, 0.36), (0.02, 0.005, 0.41), (0.05, 0.01, 0.43)], r=[0.03, 0.026, 0.02, 0.016], seg=5, material=stem, smooth=False)
curl = tube([(0.0, 0.01, 0.335)] + [(0.04 + 0.05 * math.cos(t) * (1 - t / 9), -0.02 + 0.05 * math.sin(t) * (1 - t / 9), 0.345 + 0.007 * t) for t in [0.5, 1.6, 2.7, 3.8, 4.9, 6.0]],
            r=0.007, seg=3, material=stem, smooth=True)
leaf = prism([(0, 0), (0.06, 0.035), (0.12, 0.0), (0.06, -0.03)], 0.008, stem, axis='z', loc=(-0.13, -0.05, 0.31))
T(leaf, rot=(0.2, -0.4, -0.5), pivot=(-0.01, -0.05, 0.31))
join([body, face, st, curl, leaf], 'jack_o_lantern')
T(bpy.data.objects['jack_o_lantern'], rot=(0, math.radians(-4), math.radians(18)))
report()
finish('haunted', 'jack_o_lantern', kind='edge', footprint=0.25, notes='uitgesneden pompoen; gezicht = glow_pumpkin')
