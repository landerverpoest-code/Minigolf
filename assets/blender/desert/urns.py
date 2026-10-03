import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

TERRA = mat('terracotta', '#c9643a', rough=0.75)
TDARK = mat('terracotta_dark', '#8f3f25', rough=0.8)
TURQ = mat('turquoise', '#27bfb0', rough=0.45)
CREAM = mat('cream', '#f2dfb4', rough=0.7)
M = [TERRA, TDARK, TURQ, CREAM]

# amfoor (hoog)
prof = [(0.07, 0.0), (0.13, 0.08), (0.168, 0.19), (0.17, 0.23), (0.163, 0.28), (0.15, 0.32), (0.1, 0.4), (0.065, 0.45), (0.085, 0.54)]
a = lathe(prof, verts=7, mats=M, band_mats=[0, 0, 2, 0, 1, 0, 0, 3], cap0=True, cap1=False)
shade_smooth(a, 60)
hs = [tube([(s * 0.065, 0, 0.5), (s * 0.15, 0, 0.47), (s * 0.15, 0, 0.36)], [0.015] * 3, verts=3, material=TERRA) for s in (-1, 1)]
a = join([a] + hs, 'amphora')
place(a, loc=(-0.12, 0.08, 0))
# bolle pot
prof = [(0.1, 0.0), (0.17, 0.08), (0.18, 0.13), (0.178, 0.17), (0.12, 0.25), (0.1, 0.28), (0.11, 0.3)]
b = lathe(prof, verts=7, mats=M, band_mats=[0, 3, 1, 0, 2, 0], cap0=True, cap1=False, loc=(0.16, -0.05, 0))
shade_smooth(b, 60)
# klein kruikje, schuin tegen de pot
prof = [(0.06, 0.0), (0.09, 0.07), (0.085, 0.1), (0.07, 0.13), (0.05, 0.16), (0.055, 0.18)]
c = lathe(prof, verts=6, mats=M, band_mats=[0, 2, 0, 0, 3], cap0=True, cap1=False)
shade_smooth(c, 60)
place(c, loc=(0.05, -0.25, 0.06), rot=(1.25, 0, 0.6))
join_all('urns')
o = bpy.context.scene.objects['urns']
for v in o.data.vertices: v.co.z = max(v.co.z, 0.0)
report()
finish('desert', 'urns', kind='edge', footprint=0.3, notes='Drie terracotta potten/kruiken met geschilderde banden (turkoois, crème, donkerrood)')
closeup('urns')
