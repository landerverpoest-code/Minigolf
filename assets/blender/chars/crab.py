import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ccp_kit import *

# ---------------------------------------------------------------- materials
RED = mat('crab_red', '#ea3a22', rough=0.42)
LIGHT = mat('crab_light', '#ffb46b', rough=0.55)      # underside, shell dots, joints
DARK = mat('crab_dark', '#9c1f17', rough=0.45)        # pincer tips, leg tips
WHITE = mat('eye_white', '#ffffff', rough=0.35)
PUPIL = mat('pupil', '#1d1414', rough=0.3)
BLUSH = mat('blush', '#ff7f9a', rough=0.6)

# ---------------------------------------------------------------- body
SC = V(0, 0.0, 0.36)
SR = (0.55, 0.39, 0.25)


def shell_shape(n):
    x, y, z = n
    if z < 0:
        z *= 0.55                     # flat underside
    else:
        z *= 1.0 - 0.18 * abs(x) ** 2  # sides slope down: dome
    y *= 1.0 - 0.12 * max(0, -y) * (1 - abs(x))  # front a little flatter
    return Vector((x, y, z))


shell = ell(SC, SR, seg=18, rings=12, p=0.8, material=RED, shape=shell_shape)
# light underside
iso_paint(shell, lambda p: (p.z - SC.z + 0.02) * 6 + 0.0, LIGHT)
# dots on the shell
DOTS = [V(0.0, 0.08, 0.62), V(0.24, 0.14, 0.58), V(-0.24, 0.14, 0.58), V(0.38, -0.08, 0.52), V(-0.38, -0.08, 0.52)]
body_parts = [shell]
bpy.context.view_layer.update()
for i, c in enumerate(DOTS):   # little raised dots on the shell
    dirn = (c - SC).normalized()
    ok, loc, nrm, _ = shell.ray_cast(SC, dirn)
    rr = 0.085 if i == 0 else 0.065
    q = nrm.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    body_parts.append(xf(ell((0, 0, 0), (rr, rr * 0.85, 0.022), seg=7, rings=3, material=LIGHT), Matrix.Translation(loc) @ q))
# little spikes on the shell rim (front corners)
for sx in (-1, 1):
    for k, (a, s) in enumerate(((-0.62, 0.06), (-0.85, 0.05))):
        ang = a
        base = V(sx * 0.5 * math.cos(ang * 0.9), -0.35 * math.sin(-ang * 0.9) * 0.9, 0.42)
        base = V(sx * (0.47 - 0.07 * k), -0.2 + 0.12 * k, 0.43)
        tip = base + V(sx * 0.11, -0.02, 0.03)
        body_parts.append(tube([base - V(sx * 0.03, 0, 0), tip], [s, 0.004], seg=6, material=RED))
# eye stalks + big eyes
EYES = []
for sx in (-1, 1):
    b = V(sx * 0.13, -0.2, 0.5)
    t = V(sx * 0.17, -0.25, 0.6)
    body_parts.append(tube(bezier(b, b + V(0, 0, 0.08), t, n=3), [0.045, 0.04, 0.036, 0.034], seg=6, material=RED))
    ec = t + V(sx * 0.005, -0.005, 0.075)
    body_parts += eye(ec, V(sx * 0.3, -1, 0.1), r=0.105, white=WHITE, black=PUPIL, depth=0.95, tall=1.1, pupil=0.6,
                      look=(-sx * 0.25, 0, 0.0), seg=10, pseg=8)
    # eyelid-ish brow: tiny red cap on the back-top of the eye ball
# mouth: happy smile + blush
MZ = V(0, -0.385, 0.37)
body_parts.append(tube(bezier(MZ + V(-0.1, 0.0, 0.03), MZ + V(0, -0.04, -0.06), MZ + V(0.1, 0.0, 0.03), n=6), 0.016, seg=5,
                       material=PUPIL, round_end=True))
for sx in (-1, 1):
    body_parts.append(ell(MZ + V(sx * 0.2, 0.035, 0.06), (0.06, 0.02, 0.035), seg=6, rings=4, material=BLUSH,
                          rot=(0, 0, sx * -28)))
body = part(body_parts, 'body', (0, 0, 0))

# ---------------------------------------------------------------- arms with big claws
arms = {}
for side, sx in (('l', 1), ('r', -1)):
    SH = V(sx * 0.36, -0.27, 0.34)          # shoulder pivot on the body front side
    EL = V(sx * 0.56, -0.47, 0.36)
    WR = V(sx * 0.5, -0.66, 0.42)
    PC = V(sx * 0.47, -0.79, 0.43)           # palm centre
    ap = []
    ap.append(tube([SH + V(-sx * 0.04, 0.04, 0), SH.lerp(EL, 0.5) + V(0, 0, 0.02), EL], [0.07, 0.065, 0.06], seg=8, material=RED))
    ap.append(ell(EL, (0.075, 0.075, 0.075), seg=6, rings=4, material=LIGHT))
    ap.append(tube([EL, EL.lerp(WR, 0.5), WR], [0.06, 0.066, 0.075], seg=8, material=RED))
    # palm: big swollen claw
    palm = ell(PC, (0.16, 0.19, 0.15), seg=12, rings=8, p=0.95, material=RED,
               shape=lambda n: Vector((n.x, n.y, n.z * (1 + 0.12 * n.y))))
    ap.append(palm)
    # fixed lower pincer
    lb = PC + V(-sx * 0.01, -0.13, -0.045)
    lpts = bezier(lb, lb + V(0, -0.12, -0.02), lb + V(-sx * 0.02, -0.22, 0.03), lb + V(-sx * 0.03, -0.27, 0.07), n=5)
    low = tube(lpts, [0.095, 0.085, 0.07, 0.052, 0.032, 0.008], seg=8, flat=0.7, material=RED)
    iso_paint(low, lambda p, b=lb: (p - b).length * -1 + 0.2, DARK)
    ap.append(low)
    for k in range(2):  # teeth (inner side, pointing up)
        tp = lpts[1 + k * 2] + V(0, 0, 0.035)
        ap.append(tube([tp - V(0, 0, 0.02), tp + V(0, 0, 0.03)], [0.022, 0.003], seg=5, material=LIGHT))
    arm = part(ap, f'arm_{side}', SH)
    # movable upper pincer half (jaw): hinge at the palm front top
    HG = PC + V(-sx * 0.01, -0.13, 0.065)
    upts = bezier(HG, HG + V(0, -0.11, 0.05), HG + V(-sx * 0.02, -0.23, 0.02), HG + V(-sx * 0.03, -0.28, -0.05), n=5)
    jp = [tube(upts, [0.09, 0.08, 0.066, 0.05, 0.03, 0.008], seg=8, flat=0.7, material=RED)]
    iso_paint(jp[0], lambda p, b=HG: (p - b).length * -1 + 0.2, DARK)
    jp.append(ell(HG, (0.07, 0.07, 0.07), seg=6, rings=4, material=RED))
    for k in range(2):
        tp = upts[1 + k * 2] + V(0, 0, -0.035)
        jp.append(tube([tp + V(0, 0, 0.02), tp - V(0, 0, 0.03)], [0.02, 0.003], seg=5, material=LIGHT))
    jaw = part(jp, f'jaw_{side}', HG)
    parent_keep(jaw, arm)
    arms[side] = (SH, HG)

# ---------------------------------------------------------------- legs (pivot at the body side)
LEGP = {}
for side, sx in (('l', 1), ('r', -1)):
    for k, y in enumerate((-0.08, 0.1, 0.26)):
        piv = V(sx * 0.45, y, 0.3)
        spread = (k - 1) * 0.08
        knee = V(sx * 0.68, y + spread, 0.42)
        tip = V(sx * 0.8, y + spread * 1.7, 0.001)
        lp = [tube([piv - V(sx * 0.05, 0, 0), knee], [0.065, 0.056], seg=6, material=RED),
              ell(knee, (0.06, 0.06, 0.06), seg=6, rings=4, material=LIGHT)]
        seg2 = bezier(knee, knee + V(sx * 0.07, 0, 0.0), tip + V(0, 0, 0.14), tip, n=3)
        lo = tube(seg2, [0.056, 0.05, 0.034, 0.006], seg=6, material=RED)
        iso_paint(lo, lambda p: p.z - 0.1, DARK)
        lp.append(lo)
        part(lp, f'leg_{side}{k + 1}', piv)
        LEGP[f'leg_{side}{k + 1}'] = piv

report()
fmt = lambda v: '(%.3g,%.3g,%.3g)' % tuple(v)
notes = ('Parts/pivots (Blender coords, front -Y, left=+X): body (origin 0,0,0; shell, eye stalks+eyes, smile); '
         f'arm_l shoulder {fmt(arms["l"][0])}, arm_r shoulder {fmt(arms["r"][0])} (arm + big claw pointing -Y); '
         f'jaw_l hinge {fmt(arms["l"][1])} / jaw_r hinge {fmt(arms["r"][1])} = movable upper pincer, PARENTED to its arm, '
         'hinge axis = local X (negative X rotation opens: tip goes up); '
         + ', '.join(f'{k} {fmt(v)}' for k, v in LEGP.items()) + ' (body side). '
         'Materials: crab_red, crab_light, crab_dark, eye_white, pupil, blush.')
finish('chars', 'crab', kind='char', footprint=0.6, grounded=False, notes=notes)
if '--views' in sys.argv:
    def pose():
        for s in 'lr':
            bpy.data.objects[f'jaw_{s}'].rotation_euler = (-0.6, 0, 0)
        bpy.data.objects['arm_l'].rotation_euler = (0.4, 0, 0.3)
        bpy.data.objects['leg_l1'].rotation_euler = (0, 0, 0.4)
        bpy.data.objects['leg_r2'].rotation_euler = (0, 0.4, 0)
    views('crab', pose)
