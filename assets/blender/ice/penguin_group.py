import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

BLACK = mat('penguin_black', '#222a38', rough=0.5)
WHITE = mat('penguin_white', '#f6f8fb', rough=0.6)
ORANGE = mat('penguin_orange', '#ff9a1f', rough=0.5)
GRAY = mat('penguin_chick', '#9da7b3', rough=0.8)
SNOW = mat('snow', '#eef5ff', rough=0.7)


def penguin(pos, yaw, H=0.6, body=BLACK, tilt=0.0, chick=False):
    s = H / 0.6
    prof = [(0.0, 0.0), (0.12, 0.015), (0.165, 0.1), (0.165, 0.22), (0.135, 0.33), (0.115, 0.42), (0.11, 0.5), (0.08, 0.57), (0.0, 0.6)]
    prof = [(r * s * (1.12 if chick else 1), z * s) for r, z in prof]
    b = lathe(prof, verts=10, mats=[body, WHITE], name='peng')
    for p in b.data.polygons:
        c = p.center
        # buik (voorkant -Y) en witte oogvlekjes / gezichtje
        if not chick and p.normal.y < -0.45 and c.z < 0.4 * s:
            p.material_index = 1
        if chick and p.normal.y < -0.3 and 0.4 * s < c.z < 0.56 * s:
            p.material_index = 1
    shade_smooth(b, 70)
    parts = [b]
    # ogen
    for sx in (-1, 1):
        parts.append(sphere(0.022 * s, loc=(sx * 0.045 * s, -0.098 * s, 0.48 * s), seg=4, rings=3, material=BLACK))
    if not chick:
        for sx in (-1, 1):
            parts.append(sphere(0.03 * s, loc=(sx * 0.045 * s, -0.088 * s, 0.48 * s), seg=4, rings=3, material=WHITE, scale=(1, 0.5, 1.1)))
    # snavel
    parts.append(cone(0.03 * s, 0.09 * s, loc=(0, -0.14 * s, 0.43 * s), rot=(math.pi / 2 + 0.2, 0, 0), verts=5, material=ORANGE))
    # vleugels
    for sx in (-1, 1):
        f = sphere(1.0, loc=(sx * 0.16 * s, 0.0, 0.25 * s), seg=5, rings=3, material=body, scale=(0.03 * s, 0.07 * s, 0.15 * s))
        place(f, rot=(0, sx * 0.35, 0))
        parts.append(f)
    # voetjes
    for sx in (-1, 1):
        ft = sphere(1.0, loc=(sx * 0.06 * s, -0.08 * s, 0.012), seg=4, rings=3, material=ORANGE, scale=(0.045 * s, 0.07 * s, 0.015), smooth=False)
        parts.append(ft)
    o = join(parts, 'peng')
    place(o, loc=pos, rot=(tilt, 0, yaw))
    return o

# ijsschots als ondergrond
floe = lathe([(0.62, 0.0), (0.6, 0.05), (0.55, 0.07), (0.0, 0.075)], verts=8, material=SNOW, jitter=0.12, seed=3)
penguin((-0.12, 0.05, 0.07), -0.25, H=0.72)
penguin((0.24, 0.12, 0.07), 0.45, H=0.6, tilt=-0.12)
penguin((0.05, -0.25, 0.07), 0.1, H=0.36, body=GRAY, chick=True)
join_all('penguin_group')
report()
finish('ice', 'penguin_group', kind='scatter', footprint=0.6,
       notes='Drie schattige pinguins (twee volwassen, een grijs kuiken) op een ijsschotsje; kijken naar -Y')
closeup('penguin_group')
