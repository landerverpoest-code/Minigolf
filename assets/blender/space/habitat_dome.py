import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#eef1f5', rough=0.4)
navy = mat('navy', '#1e2a48', rough=0.5)
glass = mat('glass', '#4a86b8', rough=0.08, metal=0.35)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
glow = mat('glow_window', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)
V = Vector
P = []
R0 = 2.3
# voetring + ringmuur
P.append(bev(cyl(R0 + 0.25, 0.25, loc=(0, 0, 0.125), verts=16, material=navy), 0.03))
wall = lathe([(R0, 0.25), (R0, 1.45), (R0 - 0.1, 1.55)], seg=16, material=white, cap_bot=False, cap_top=True)
P.append(wall)
P.append(cyl(R0 + 0.06, 0.12, loc=(0, 0, 0.42), verts=16, material=navy))
# verlichte raamstroken rondom (behalve bij de luchtsluis)
for k in range(16):
    a = (k + 0.5) * TAU / 16
    if abs(math.atan2(math.sin(a + math.pi / 2), math.cos(a + math.pi / 2))) < 0.45:
        continue
    P.append(box((0.62, 0.06, 0.32), loc=((R0 + 0.01) * math.cos(a), (R0 + 0.01) * math.sin(a), 0.98), rot=(0, 0, a + math.pi / 2), material=glow))
    P.append(box((0.08, 0.08, 0.5), loc=((R0 + 0.02) * math.cos(a - TAU / 32), (R0 + 0.02) * math.sin(a - TAU / 32), 0.98), rot=(0, 0, a + math.pi / 2), material=navy))
# geodetische koepel: ico, bovenste helft, panelen ingezet
dome = ico(R0 - 0.08, sub=3, material=glass)
bake(dome)
bm = bmesh.new(); bm.from_mesh(dome.data)
bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, -0.01), plane_no=(0, 0, 1), clear_inner=True)
bm.to_mesh(dome.data); bm.free()
T(dome, scale=(1, 1, 0.82), loc=(0, 0, 1.52))
inset(dome, lambda c, n: True, thick=0.07, depth=-0.02)
# randen (niet de ingezette panelen) wit maken: ingezette vlakken zijn de originele; nieuwe zijvlakken krijgen wit
dome.data.materials.append(white)
bm = bmesh.new(); bm.from_mesh(dome.data)
for f in bm.faces:
    f.material_index = 1
bm.to_mesh(dome.data); bm.free()
# originele panelen (de kleinste driehoeken met 3 verts en normale ~radiaal) terug naar glas
for p in dome.data.polygons:
    if p.loop_total == 3:
        p.material_index = 0
P.append(dome)
# top: ring + antenne
P.append(cyl(0.35, 0.12, loc=(0, 0, 1.52 + (R0 - 0.08) * 0.82 + 0.0), verts=8, material=white))
P.append(cyl(0.03, 0.9, loc=(0.0, 0, 1.52 + (R0 - 0.08) * 0.82 + 0.5), verts=4, material=white))
P.append(ico(0.07, loc=(0.0, 0, 1.52 + (R0 - 0.08) * 0.82 + 0.98), sub=1, material=glow))
# luchtsluis naar -Y
ay = -R0 - 0.55
P.append(cyl(0.68, 1.4, loc=(0, ay + 0.1, 0.95), rot=(math.pi / 2, 0, 0), verts=10, material=white))
for y in (ay - 0.45, ay + 0.35):
    P.append(cyl(0.73, 0.14, loc=(0, y, 0.95), rot=(math.pi / 2, 0, 0), verts=10, material=navy))
P.append(cyl(0.6, 0.06, loc=(0, ay - 0.62, 0.95), rot=(math.pi / 2, 0, 0), verts=10, material=navy))
door = box((0.56, 0.06, 0.95), loc=(0, ay - 0.66, 0.88), material=white, bevel=0.03)
P.append(door)
P.append(box((0.66, 0.04, 0.06), loc=(0, ay - 0.68, 1.38), material=glow))
P.append(box((0.16, 0.04, 0.06), loc=(0.17, ay - 0.7, 0.95), material=glow))
P.append(box((0.9, 0.7, 0.12), loc=(0, ay - 0.95, 0.3), material=navy, bevel=0.02))
P.append(box((0.9, 0.5, 0.12), loc=(0, ay - 1.2, 0.12), material=navy, bevel=0.02))
# goudfolie tanks + kleine zonnepanelen aan de zijkant
for sx in (-1, 1):
    a = math.pi / 2 + sx * 1.9
    P.append(cyl(0.32, 1.0, loc=((R0 + 0.45) * math.cos(a), (R0 + 0.45) * math.sin(a), 0.6), verts=8, material=gold))
    P.append(lathe([(0.32, 1.1), (0.2, 1.25), (0, 1.3)], seg=8, material=white))
    T(P[-1], loc=((R0 + 0.45) * math.cos(a), (R0 + 0.45) * math.sin(a), 0))
    P.append(cyl(0.33, 0.1, loc=((R0 + 0.45) * math.cos(a), (R0 + 0.45) * math.sin(a), 0.35), verts=8, material=navy))
join(P, 'habitat_dome')
report()
finish('space', 'habitat_dome', kind='hero', footprint=2.7, notes='geodetische glazen koepel op ringvoet met verlichte raamstroken (glow_window), luchtsluis en goudfolie tanks')
