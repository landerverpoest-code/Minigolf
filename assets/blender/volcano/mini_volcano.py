import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

basalt = mat('basalt', '#3a322e', rough=0.9)
rockb = mat('rock_brown', '#5e4a3c', rough=0.9)
ash = mat('ash', '#8a827c', rough=1.0)
lava = mat('glow_lava', '#ff6a00', rough=0.45, emit='#ff4800', emit_strength=3.0)
smoke = mat('smoke', '#5f5a57', rough=1.0)

H, RB, RT = 11.0, 10.5, 2.9     # hoogte, voetstraal, kraterstraal
SEG = 32
# kegelprofiel (r, z): concaaf, met kraterrand en kom
prof = [(RT + (RB - RT) * (1 - z / H) ** 1.45, z) for z in (0.0, 0.7, 1.7, 3.0, 4.4, 5.9, 7.4, 8.8, 10.0)] + [(RT + 0.12, H - 0.25), (RT - 0.1, H), (RT - 0.6, H - 0.15), (RT - 1.2, H - 0.9)]
cone_ = lathe(prof, seg=SEG, material=rockb, cap_bottom=False, cap_top=True)
cone_.data.materials.append(basalt); cone_.data.materials.append(ash)
# ribbels en geulen: radiale ruis afhankelijk van hoek; kraterrand gekarteld
for v in cone_.data.vertices:
    r = Vector((v.co.x, v.co.y)).length
    if r < 1e-4:
        continue
    a = math.atan2(v.co.y, v.co.x)
    t = v.co.z / H
    ridge = 0.5 + 0.5 * math.sin(a * 7 + 1.3 * noise.noise(Vector((math.cos(a), math.sin(a), t * 2))))
    k = 1 + (0.09 * ridge + 0.06 * noise.noise(Vector((v.co.x * 0.35, v.co.y * 0.35, v.co.z * 0.3)))) * (1 - 0.6 * t)
    v.co.x *= k; v.co.y *= k
    if v.co.z > H - 0.3:
        v.co.z += 0.5 * noise.noise(Vector((math.cos(a) * 2, math.sin(a) * 2, 5)))
# kleuren: donker basalt onderaan in banden, as bovenaan
for p in cone_.data.polygons:
    a = math.atan2(p.center.y, p.center.x)
    z = p.center.z + 1.6 * noise.noise(p.center * 0.45) + 1.2 * math.sin(a * 7)
    if z > 8.6:
        p.material_index = 2
    elif z < 1.8:
        p.material_index = 1
flat(cone_)
parts = [cone_]
# lava in de krater (licht bol, met korstjes)
pool = lathe([(RT - 0.9, H - 1.0), (RT * 0.5, H - 0.8), (0, H - 0.7)], seg=SEG // 2, material=lava, cap_bottom=False)
parts.append(pool)
# lavastromen vanaf de rand naar beneden
tree = surf_tree(cone_)
for k, (a, L, w) in enumerate(((-1.6, 12.0, 1.3), (-0.75, 8.5, 1.0), (-2.5, 7.5, 0.9), (1.9, 10.0, 1.0))):
    start = Vector((math.cos(a) * (RT + 0.15), math.sin(a) * (RT + 0.15), H - 0.1))
    dvec = Vector((math.cos(a), math.sin(a), -2.5))
    rib = crack_ribbon(tree, start, dvec, length=L, width=w, steps=12, seed=k * 5 + 1, material=lava, lift=0.08, wiggle=0.3, branch=1 if k == 0 else 0, flow=True, down=0.6)
    parts += rib
    if k in (0, 3):
        me = rib[0].data
        e = (me.vertices[-1].co + me.vertices[-2].co) / 2
        pl = lathe([(w * 1.1, 0.0), (w * 0.8, 0.12), (0, 0.15)], seg=8, material=lava, cap_bottom=False)
        jitter(pl, 0.15, seed=k, axes=(1, 1, 0))
        xform(pl, scale=(1.4, 1.0, 1.0), rot=(0, 0, math.degrees(a)), loc=(e.x, e.y, max(0.0, e.z - 0.2)))
        parts.append(pl)
# lavapoeltjes waar de stromen eindigen + wat rotsblokken aan de voet
rnd = random.Random(8)
for k in range(10):
    a = rnd.uniform(0, TAU)
    d = RB * rnd.uniform(0.95, 1.12)
    r = rnd.uniform(0.7, 1.4)
    c = chunk(r, (1.3, 1.0, 0.8), cuts=6, seed=200 + k, material=basalt, flat_bottom=0.4, base_sub=1)
    xform(c, loc=(d * math.cos(a), d * math.sin(a), r * 0.2))
    dust(c, ash, 0.8)
    parts.append(c)
# rookpluim (cartoon-wolkjes boven de krater)
for k, (x, y, z, r) in enumerate(((0.0, 0.3, H + 0.6, 1.3), (0.7, 0.5, H + 1.7, 1.45), (-0.5, 0.6, H + 1.5, 1.0), (1.5, 0.8, H + 2.6, 1.25))):
    s_ = ico(r, sub=2, material=smoke)
    lumpy(s_, r * 0.18, 1.2 / r, seed=k)
    xform(s_, loc=(x, y, z))
    smooth(s_, 70)
    parts.append(s_)
v = join(parts, 'mini_volcano')
report()
finish('volcano', 'mini_volcano', kind='hero', footprint=11.5, notes='achtergrondvulkaan: geribde kegel (basalt/bruin/as), gloeiende lava in de krater, 4 lavastromen (glow_lava), rotsblokken en cartoon-rookpluim')
