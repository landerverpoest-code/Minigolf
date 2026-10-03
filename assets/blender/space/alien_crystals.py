import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
rockm = mat('alien_rock', '#343a58', rough=0.9)
mag = mat('glow_crystal', '#b0189e', rough=0.15, emit='#ff2ad8', emit_strength=1.1)
cya = mat('glow_crystal_cyan', '#1590b0', rough=0.15, emit='#22d8f8', emit_strength=1.1)
V = Vector
P = [rock(0.2, loc=(0, 0, 0.0), sub=1, material=rockm, scale=(1.3, 1.1, 0.55), jit=0.15, seed=4)]
def crystal(p, d, L, r, m, rot=0.0):
    c = lathe([(r, -0.05), (r * 1.05, L * 0.7), (0, L)], seg=6, material=m, phase=rot)
    q = V((0, 0, 1)).rotation_difference(V(d).normalized())
    T(c, rot=q.to_euler(), loc=p)
    return c
for (p, d, L, r, m, rt) in [((0, 0, 0.05), (0.05, 0.0, 1), 0.55, 0.075, mag, 0.2), ((0.1, -0.05, 0.03), (0.6, -0.3, 1), 0.36, 0.055, cya, 0.5),
                            ((-0.1, 0.04, 0.03), (-0.7, 0.2, 1), 0.4, 0.06, mag, 0.1), ((0.02, 0.12, 0.03), (0.1, 0.8, 1), 0.3, 0.05, cya, 0.3),
                            ((-0.05, -0.1, 0.03), (-0.3, -0.9, 1), 0.26, 0.045, mag, 0.7), ((0.16, 0.07, 0.0), (0.9, 0.4, 0.6), 0.2, 0.04, mag, 0.0),
                            ((-0.17, -0.02, 0.0), (-0.9, -0.2, 0.5), 0.17, 0.035, cya, 0.4), ((0.06, -0.15, 0.0), (0.3, -1, 0.5), 0.15, 0.03, cya, 0.9)]:
    P.append(crystal(V(p), d, L, r, m, rt))
join(P, 'alien_crystals')
report()
finish('space', 'alien_crystals', kind='edge', footprint=0.28, notes='cluster gloeiende kristallen (glow_crystal magenta + glow_crystal_cyan) op een rotsje')
