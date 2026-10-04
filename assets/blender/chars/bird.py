import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

WHITE = mat('bird_white', '#f6f7fa', rough=0.55)
GREY = mat('bird_grey', '#9aa6b8', rough=0.55)
BLACK = mat('bird_black', '#23252c', rough=0.4)
BEAK = mat('beak', '#ffc21a', rough=0.45)
EYEW = mat('eye_white', '#ffffff', rough=0.3)

# ---------------------------------------------------------------- body (origin = body centre)
bp = []


def body_shape(n):
    x, y, z = n
    # plump chest in front, tapering towards the tail
    if y > 0:
        k = 1 - 0.45 * y
        x *= k; z *= k
        z += 0.12 * y * y
    if z < 0:
        z *= 0.92
    return Vector((x, y, z))


torso = ell((0, 0.01, 0), (0.075, 0.14, 0.072), seg=16, rings=10, material=WHITE, shape=body_shape)
iso_paint(torso, lambda p: -min((p.z - 0.035) * 30, (p.y + 0.03) * 20), GREY)
bp.append(torso)
HC = V(0, -0.115, 0.06)
head = ell(HC, (0.066, 0.064, 0.062), seg=14, rings=9, material=WHITE)
bp.append(head)
# beak: upper + lower, hooked tip with little red-free gull look
BK = HC + V(0, -0.058, -0.008)
bp.append(tube([BK, BK + V(0, -0.035, -0.002), BK + V(0, -0.062, -0.012)], [0.02, 0.013, 0.003], seg=7, material=BEAK, flat=0.7))
bp.append(tube([BK + V(0, 0.0, -0.01), BK + V(0, -0.04, -0.016)], [0.014, 0.003], seg=6, material=BEAK, flat=0.6))
# eyes
for sx in (-1, 1):
    ec = HC + V(sx * 0.036, -0.044, 0.016)
    bp += eye(ec, V(sx * 0.55, -1, 0.1), r=0.026, white=EYEW, black=BLACK, depth=0.6, tall=1.15, pupil=0.62,
              look=(-sx * 0.2, 0, 0.1), seg=10, pseg=8)
    # tiny grey brow for an expressive look
    bp.append(tube(bezier(ec + V(-sx * 0.016, 0.004, 0.03), ec + V(0, -0.006, 0.04), ec + V(sx * 0.018, 0.006, 0.032), n=3),
                   0.005, seg=4, material=GREY, round_end=True))
# tail: grey fan with black band
for k, a in enumerate((-0.35, 0.0, 0.35)):
    d = V(math.sin(a) * 0.5, 1, 0.12).normalized()
    s = V(0, 0.13, 0.012)
    bp.append(tube([s, s + d * 0.05, s + d * 0.1], [0.026, 0.032, 0.022], seg=6, material=GREY, flat=0.25, flat_n=True))
    bp.append(ell(s + d * 0.105, (0.022, 0.012, 0.006), seg=6, rings=4, material=BLACK, rot=(0, 0, -math.degrees(a) * 0.5)))
# tucked orange feet
for sx in (-1, 1):
    f0 = V(sx * 0.03, 0.05, -0.06)
    bp.append(tube([f0, f0 + V(0, 0.02, -0.02), f0 + V(0, 0.06, -0.025)], [0.008, 0.007, 0.012], seg=5, material=BEAK, flat=0.4, flat_n=True))
body = part(bp, 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- wings (pivot at shoulder, extended for gliding)
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.055, -0.02, 0.035)
    pts = [SH + V(sx * 0.0, 0.005, 0), SH + V(sx * 0.07, 0.015, 0.022), SH + V(sx * 0.14, 0.035, 0.028), SH + V(sx * 0.2, 0.06, 0.014),
           SH + V(sx * 0.245, 0.085, -0.004)]
    rad = [0.05, 0.068, 0.06, 0.042, 0.014]
    w = tube(pts, rad, seg=10, material=GREY, flat=0.18, flat_n=True, round_end=True)
    # black tip with white dots
    iso_paint(w, lambda p, sx=sx: -(abs(p.x) - 0.215) * 30, BLACK)
    wp = [w]
    # feather fingers at the trailing edge tip
    for k in range(3):
        b = SH + V(sx * (0.18 + 0.028 * k), 0.075 + 0.008 * k, 0.01 - 0.007 * k)
        wp.append(tube([b, b + V(sx * 0.03, 0.045, -0.006)], [0.012, 0.003], seg=5, material=BLACK, flat=0.3, flat_n=True))
    wp.append(ell(SH + V(sx * 0.228, 0.072, 0.009), (0.009, 0.009, 0.004), seg=6, rings=3, material=WHITE))
    part(wp, f'wing_{side}', SH, angle=60)

report()
views('bird')
montage('bird')
finish('chars', 'bird', kind='char', footprint=0.3, grounded=False,
       notes='origin at body centre (0,0,0). parts: body (pivot 0,0,0); wing_l pivot (0.055,-0.02,0.035), wing_r pivot (-0.055,-0.02,0.035) '
             'at the shoulders, wings extended (glide pose), flap = rotate around forward axis (Blender Y / three.js z)')
