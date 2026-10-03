import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
purple = mat('royal_purple', '#5b2a86', rough=0.6)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#b0213a', rough=0.6)
stone = mat('stone_dark', '#3d3648', rough=0.9)
V = Vector
P = []
P.append(box((0.32, 0.32, 0.14), loc=(0, 0, 0.07), material=stone, bevel=0.02))
P.append(cyl(0.035, 2.35, loc=(0, 0, 1.25), verts=6, material=gold))
P.append(ico(0.07, loc=(0, 0, 2.47), sub=1, material=gold, smooth=True))
P.append(cyl(0.025, 0.9, loc=(0.42, 0, 2.25), rot=(0, math.pi / 2, 0), verts=4, material=gold))
def pennant(x0, z0, w, h, m, ph):
    bm = bmesh.new()
    n = 3
    top = [bm.verts.new((x0 + w * i / n, 0, z0)) for i in range(n + 1)]
    tip = bm.verts.new((x0 + w / 2, 0, z0 - h))
    for i in range(n):
        bm.faces.new((top[i], top[i + 1], tip))
    o = link_bm(bm, 'pennant', m)
    deform(o, lambda v: V((v.x, v.y + 0.05 * math.sin(v.x * 9 + ph) + 0.06 * (z0 - v.z), v.z)))
    return o
for k, (m, ph) in enumerate([(purple, 0.0), (crimson, 1.3), (purple, 2.4)]):
    P.append(pennant(0.04 + k * 0.29, 2.24, 0.27, 0.5 - 0.04 * k, m, ph))
# langwerpige banier aan de paal
ban = prism([(0, 0), (0.5, 0), (0.5, -0.9), (0.25, -0.75), (0, -0.9)], 0.015, crimson, axis='y', loc=(-0.54, 0, 1.95))
deform(ban, lambda v: V((v.x, v.y + 0.04 * math.sin(v.x * 8), v.z)))
P.append(ban)
P.append(cyl(0.02, 0.6, loc=(-0.29, 0, 1.96), rot=(0, math.pi / 2, 0), verts=4, material=gold))
em = prism([(0.12 * math.sin(i * math.pi / 5) * (1 if i % 2 == 0 else 0.45), 0.12 * math.cos(i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)], 0.02, gold, axis='y', loc=(-0.29, -0.02, 1.58))
P.append(em)
join(P, 'banner_flags')
report()
finish('finale', 'banner_flags', kind='edge', footprint=0.3, notes='gouden vlaggenmast met drie driehoekige wimpels en een rode banier met ster')
