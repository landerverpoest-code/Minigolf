import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/volcano'); from _deco import *

BASALT = mat('basalt', '#3a322e', rough=0.9)
ROCK = mat('rock_brown', '#5e4a3c', rough=0.9)
ASH = mat('ash', '#8a827c', rough=1.0)
GLOW = mat('glow_lava', '#ff5a00', rough=0.45, emit='#ff3c00', emit_strength=2.4)
HOT = mat('glow_lava_hot', '#ffb020', rough=0.4, emit='#ff9000', emit_strength=3.0)

rnd = random.Random(9)
# kegel: gelaagd draaiprofiel met krater, ruw vervormd
prof = [(0.95, 0.0), (0.9, 0.12), (0.72, 0.3), (0.55, 0.52), (0.42, 0.72), (0.36, 0.8), (0.27, 0.78), (0.2, 0.66), (0.0, 0.62)]
cone_ = lathe(prof, verts=10, material=ROCK, band_mats=[0, 0, 0, 0, 0, 2, 2, 2], mats=[ROCK, BASALT, GLOW], jitter=0.08, seed=4)
lumpy(cone_, amp=0.06, freq=3.0, seed=2, axes=(1, 1, 0.6))
flat(cone_)
# asrand bovenaan + donkere basaltvlekken
recolor(cone_, [ROCK, BASALT, GLOW, ASH], lambda f: None if f.material_index == 2 else (3 if f.center.z > 0.68 and f.normal.z > 0.3 else (1 if noise.noise(f.center * 3) > 0.15 else 0)))
# lavapoel in de krater
pool = lathe([(0.24, 0.66), (0.0, 0.67)], verts=10, material=HOT, cap0=False)
# lavastroompjes langs de flank
tree = None
for k, a in enumerate((0.3, 2.4, 4.3)):
    pts = []
    for i in range(6):
        t = i / 5
        r = 0.36 + t * 0.55
        z = 0.8 - t * 0.78
        aa = a + math.sin(t * 5 + k) * 0.12
        pts.append(Vector((r * math.cos(aa), r * math.sin(aa), z + 0.045)))
    tube(pts, [0.07, 0.065, 0.06, 0.05, 0.045, 0.03], verts=4, material=GLOW, squash=(1.0, 0.35), cap0=False)
# geiser: straal + spetterkroon + druppels
jet = tube([(0, 0, 0.62), (0.0, 0.0, 0.9), (0.02, 0.0, 1.15), (0.0, 0.02, 1.32)], [0.16, 0.12, 0.1, 0.12], verts=7, material=HOT, smooth=True, cap1=False)
crown = blob([((0, 0, 1.38), 0.16), ((0.14, 0.05, 1.3), 0.1), ((-0.12, 0.09, 1.3), 0.1), ((0.02, -0.14, 1.28), 0.1),
              ((-0.08, -0.08, 1.45), 0.08), ((0.08, 0.1, 1.47), 0.08)], center=(0, 0, 1.34), sub=2, material=GLOW, angle=40)
for k in range(7):
    a = k * TAU / 7 + 0.3; r = 0.28 + 0.1 * (k % 3); z = 1.0 + 0.2 * ((k * 5) % 3)
    ico(0.035 + 0.012 * (k % 2), loc=(r * math.cos(a), r * math.sin(a), z), sub=0, material=GLOW if k % 2 else HOT)
# brokken lavasteen aan de voet
for k, (x, y, s) in enumerate(((0.95, 0.3, 0.14), (-0.85, -0.45, 0.12), (0.2, -1.0, 0.1))):
    c = chunk(s, (1.3, 1.0, 0.8), cuts=5, seed=40 + k, material=BASALT, flat_bottom=0.3, base_sub=1)
    T(c, loc=(x, y, s * 0.25))
join_all('lava_geyser_cone')
report()
done('volcano', 'lava_geyser_cone', kind='scatter', footprint=1.05,
     notes='Kleine lavagaiser: ruwe kegel met askraag en heetgele lavapoel, drie gloeiende lavastroompjes langs de flank, spuitende straal met spetterkroon en druppels (glow_lava, glow_lava_hot)')
