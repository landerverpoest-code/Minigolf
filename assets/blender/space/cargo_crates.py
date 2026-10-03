import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#e9edf2', rough=0.45)
navy = mat('navy', '#1e2a48', rough=0.55)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
cy = mat('glow', '#30d8f0', rough=0.3, emit='#22d8f8', emit_strength=1.4)
mg = mat('glow_magenta', '#c81aa8', rough=0.3, emit='#ff2ad8', emit_strength=1.4)
P = []
# grote krat
P.append(box((0.62, 0.55, 0.48), loc=(0, 0, 0.24), material=white, bevel=0.035))
P.append(box((0.66, 0.59, 0.08), loc=(0, 0, 0.24), material=navy))
P.append(box((0.3, 0.02, 0.05), loc=(-0.1, -0.3, 0.38), material=cy))
P.append(box((0.08, 0.02, 0.05), loc=(0.2, -0.3, 0.38), material=mg))
# kleine krat erop, gedraaid
k2 = [box((0.42, 0.36, 0.3), loc=(0, 0, 0.63), material=white, bevel=0.03),
      box((0.08, 0.4, 0.34), loc=(-0.12, 0, 0.63), material=navy),
      box((0.08, 0.4, 0.34), loc=(0.12, 0, 0.63), material=navy),
      box((0.02, 0.2, 0.04), loc=(0.215, 0.0, 0.7), material=mg)]
k2 = join(k2, 'k2'); T(k2, rot=(0, 0, 0.35), loc=(0.03, 0.02, 0)); P.append(k2)
# goudfolie bus ernaast
P.append(cyl(0.15, 0.42, loc=(0.48, -0.12, 0.21), verts=8, material=gold))
P.append(cyl(0.16, 0.06, loc=(0.48, -0.12, 0.42), verts=8, material=navy))
P.append(cyl(0.16, 0.06, loc=(0.48, -0.12, 0.03), verts=8, material=navy))
P.append(box((0.02, 0.1, 0.06), loc=(0.48, -0.27, 0.27), rot=(0, 0, math.pi / 2), material=cy))
join(P, 'cargo_crates')
report()
finish('space', 'cargo_crates', kind='edge', footprint=0.42, notes='stapel sci-fi kratten met strepen (glow cyaan + glow_magenta) en goudfolie bus')
