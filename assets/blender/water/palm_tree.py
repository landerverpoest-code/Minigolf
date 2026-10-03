import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _palm import *

M = palm_mats()
parts, top = palm(M, height=4.2, lean=(1.2, 0.3), fronds=8, up_fronds=2, flen=2.5, fwidth=0.5, frise=0.8, fdroop=1.0, seed=3)
join_all('palm_tree')
report()
finish('water', 'palm_tree', kind='scatter', footprint=0.5, notes='Gebogen gesegmenteerde palm met hangende bladeren en kokosnoten')
closeup('palm_tree')
