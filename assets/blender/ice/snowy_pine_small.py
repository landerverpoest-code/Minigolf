import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _pine import *

M = pine_mats()
pine(M, height=2.5, radius=0.95, tiers=3, verts=9, seed=5, trunk_h=0.35, snow_start=0.36)
snowbase = lathe([(0.48, 0.0), (0.38, 0.08), (0.15, 0.13), (0.0, 0.14)], verts=8, material=M['snow'], jitter=0.08, seed=4)
join_all('snowy_pine_small')
report()
finish('ice', 'snowy_pine_small', kind='scatter', footprint=0.4, notes='Kleine besneeuwde den met drie lagen')
closeup('snowy_pine_small')
