import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

RED = mat('buoy_red', '#e0362f', rough=0.5)
WHITE = mat('buoy_white', '#f6f3ec', rough=0.5)
DARK = mat('buoy_dark', '#34404a', rough=0.5, metal=0.2)
GLOW = mat('glow_buoy', '#fff1c8', rough=0.3, emit='#ffcf4a', emit_strength=6.0)

# drijflichaam (onderkant = waterlijn)
prof = [(0.0, 0.0), (0.42, 0.0), (0.5, 0.08), (0.52, 0.18), (0.5, 0.3), (0.42, 0.4), (0.3, 0.46), (0.0, 0.47)]
body = lathe(prof, verts=14, mats=[RED, WHITE], band_mats=[0, 0, 1, 1, 0, 0, 0, 0], name='body')
shade_smooth(body, 35)
# stootrand
torus(0.52, 0.05, loc=(0, 0, 0.13), seg=14, ring=5, material=DARK)
# vakwerktorentje
top_r, bot_r, z0, z1 = 0.09, 0.27, 0.44, 1.0
for k in range(4):
    a = math.pi / 4 + k * math.pi / 2
    p0 = Vector((math.cos(a) * bot_r, math.sin(a) * bot_r, z0)); p1 = Vector((math.cos(a) * top_r, math.sin(a) * top_r, z1))
    tube([p0, p1], [0.028, 0.024], verts=4, material=RED)
    a2 = a + math.pi / 2
    q0 = Vector((math.cos(a2) * bot_r, math.sin(a2) * bot_r, z0))
    q1 = Vector((math.cos(a) * (bot_r + top_r) / 2, math.sin(a) * (bot_r + top_r) / 2, (z0 + z1) / 2))
    tube([q0, q1], [0.016, 0.016], verts=4, material=WHITE)
# dagmerk (rood-wit plaatje) en ringen
ring1 = lathe([(0.2, 0.69), (0.19, 0.75), (0, 0.75)], verts=8, material=WHITE, name='ring')
plate = lathe([(0.15, 0.98), (0.15, 1.03), (0, 1.03)], verts=8, material=DARK)
# lamp
lamp = cyl(0.075, 0.13, loc=(0, 0, 1.03 + 0.065), verts=8, material=GLOW)
for k in range(4):
    a = k * math.pi / 2
    box((0.018, 0.018, 0.14), loc=(math.cos(a) * 0.08, math.sin(a) * 0.08, 1.1), material=DARK)
cap = cone(0.11, 0.09, loc=(0, 0, 1.03 + 0.13 + 0.045), verts=8, material=RED)
tip = sphere(0.025, loc=(0, 0, 1.28), seg=6, rings=4, material=DARK)
join_all('buoy')
report()
finish('water', 'buoy', kind='scatter', footprint=0.55,
       notes='Rood-witte drijvende boei met vakwerktorentje en lampje (glow_buoy); onderkant = waterlijn')
closeup('buoy')
