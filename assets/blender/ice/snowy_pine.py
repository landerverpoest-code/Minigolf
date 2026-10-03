import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _pine import *

M = pine_mats()
pine(M, height=5.0, radius=1.6, tiers=5, verts=11, seed=2, snow_start=0.36)
# sneeuwhoopje rond de voet
snowbase = lathe([(0.75, 0.0), (0.6, 0.12), (0.25, 0.2), (0.0, 0.21)], verts=9, material=M['snow'], jitter=0.08, seed=3)
join_all('snowy_pine')
report()
finish('ice', 'snowy_pine', kind='scatter', footprint=0.6, notes='Gelaagde den met sneeuwkap en druppelrand op elke laag')
closeup('snowy_pine')
