import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space'); from _deco import *

WHITE = mat('panel_white', '#eef1f5', rough=0.4)
GREY = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
NAVY = mat('navy', '#1e2a48', rough=0.5)
GLOW = mat('glow', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)
ORANGE = mat('fuel_orange', '#f08a24', rough=0.45)

# lijf: afgeronde capsule (kop naar -Y)
body = box((0.26, 0.42, 0.2), loc=(0, 0.03, 0.3), material=WHITE, bevel=0.06)
box((0.2, 0.12, 0.02), loc=(0, 0.03, 0.405), material=ORANGE)
# kop: groot en rond (schattig), met vizier
head = box((0.26, 0.22, 0.2), loc=(0, -0.24, 0.47), material=WHITE, bevel=0.06)
visor = box((0.2, 0.02, 0.09), loc=(0, -0.355, 0.48), material=NAVY)
for s in (-1, 1):
    box((0.05, 0.02, 0.04), loc=(s * 0.05, -0.367, 0.485), material=GLOW)
    # oortjes (driehoekige panelen)
    e = prism([(-0.04, 0), (0.04, 0), (0.0, 0.1)], 0.02, material=NAVY, axis='Y')
    T(e, rot=(0, s * -20, 0), loc=(s * 0.09, -0.22, 0.56))
# snuitje
box((0.1, 0.06, 0.06), loc=(0, -0.37, 0.42), material=GREY)
# antenne-staart met gloeibol
rod((0, 0.24, 0.36), (0, 0.36, 0.55), r=0.012, verts=3, material=GREY)
sphere(0.035, loc=(0, 0.37, 0.57), seg=4, rings=3, material=GLOW)
# poten met gewrichten
for x, y in ((0.1, -0.12), (-0.1, -0.12), (0.1, 0.17), (-0.1, 0.17)):
    tube([(x, y, 0.25), (x * 1.1, y + 0.03, 0.12), (x * 1.1, y - 0.02, 0.03)], [0.028, 0.03, 0.022], verts=4, material=GREY, cap0=False, cap1=False)
    box((0.06, 0.09, 0.035), loc=(x * 1.1, y - 0.04, 0.0175), material=NAVY)
# halsband met lampje
o = join_all('robot_dog')
report()
done('space', 'robot_dog', kind='edge', footprint=0.3,
     notes='Schattig robothondje: wit afgerond lijf met oranje streep, grote kop met donker vizier en gloeiende oogjes, driehoekige oortjes, antennestaartje met gloeibol (glow), poten met gewrichten; kijkt naar -Y')
