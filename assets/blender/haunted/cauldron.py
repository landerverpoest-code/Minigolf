import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted'); from _deco import *

IRON = mat('iron', '#2b2733', rough=0.45, metal=0.6)
STONE = mat('stone', '#8a958a', rough=0.9)
WOOD = mat('wood_dark', '#3b2820', rough=0.9)
BREW = mat('glow_brew', '#3fbf22', rough=0.3, emit='#5ae02a', emit_strength=1.8)
FIRE = mat('glow_fire', '#ffb040', rough=0.4, emit='#ff7a1a', emit_strength=2.5)

rnd = random.Random(5)
# kring van stenen
for k in range(7):
    a = k * TAU / 7 + rnd.uniform(-0.1, 0.1)
    c = ico(0.14, sub=0, material=STONE, scale=(1.3, 1.0, 0.7), jitter=0.025, seed=10 + k)
    T(c, rot=(0, 0, math.degrees(a)), loc=(0.62 * math.cos(a), 0.62 * math.sin(a), 0.05))
# houtblokken + vlammetjes
for k in range(4):
    a = k * TAU / 4 + 0.3
    rod((0.38 * math.cos(a), 0.38 * math.sin(a), 0.05), (0.05 * math.cos(a + 0.3), 0.05 * math.sin(a + 0.3), 0.15), r=0.05, verts=5, material=WOOD)
for k in range(5):
    a = k * TAU / 5
    h = rnd.uniform(0.22, 0.34)
    f = lathe([(0.07, 0.0), (0.06, h * 0.5), (0.0, h)], verts=4, material=FIRE)
    T(f, rot=(rnd.uniform(-10, 10), rnd.uniform(-10, 10), 0), loc=(0.2 * math.cos(a), 0.2 * math.sin(a), 0.08))
# ketel op drie pootjes
pot = lathe([(0.12, 0.25), (0.34, 0.33), (0.47, 0.5), (0.48, 0.66), (0.4, 0.82), (0.36, 0.86), (0.4, 0.9), (0.36, 0.92), (0.33, 0.86), (0.3, 0.8)],
            verts=12, material=IRON, cap0=True, cap1=False)
shade_smooth(pot, 50)
for k in range(3):
    a = k * TAU / 3 + 0.5
    rod((0.33 * math.cos(a), 0.33 * math.sin(a), 0.35), (0.42 * math.cos(a), 0.42 * math.sin(a), 0.0), r=0.035, verts=4, material=IRON)
# oortjes
for s in (-1, 1):
    torus(0.07, 0.018, loc=(s * 0.47, 0, 0.78), rot=(math.pi / 2, 0, 0), seg=6, ring=3, material=IRON)
# bubbelend groen brouwsel met bubbels erboven
brew = lathe([(0.36, 0.84), (0.2, 0.87), (0.0, 0.88)], verts=12, material=BREW, cap0=False)
for k, (x, y, z, r) in enumerate(((0.1, 0.05, 0.93, 0.06), (-0.12, -0.08, 0.92, 0.05), (0.02, -0.15, 0.96, 0.035), (-0.05, 0.1, 1.08, 0.04), (0.08, -0.04, 1.2, 0.03), (-0.02, 0.0, 1.32, 0.022))):
    sphere(r, loc=(x, y, z), seg=5, rings=3, material=BREW)
# pollepel die erin steekt
rod((0.05, 0.15, 0.85), (0.32, 0.4, 1.35), r=0.022, verts=4, material=WOOD)
o = join_all('cauldron')
report()
done('haunted', 'cauldron', kind='scatter', footprint=0.8,
     notes='Heksenketel: ijzeren buikige ketel op drie pootjes met oortjes, bubbelend gloeiend groen brouwsel en opstijgende bellen (glow_brew), houtvuurtje met vlammetjes (glow_fire), kring van stenen, pollepel')
