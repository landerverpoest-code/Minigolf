import sys, os; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mglib import *
reset()
from b6kit import *

# Small glowing hexagonal rune stone lying flat on the basalt bridge. One part (body), origin centre bottom.
RUNE = mat('glow_rune', '#ff8a2a', rough=0.45, emit='#ff6a10', emit_strength=1.1)
P = []
H = 0.04
# outer hexagonal frame with chamfered top edges (flat corners point along +-X)
P.append(lathe([(0.215, 0.0), (0.3, 0.0), (0.3, 0.028), (0.288, H), (0.227, H), (0.215, 0.028), (0.215, 0.0)],
               seg=6, material=RUNE, smooth=False))
# inner thin hex ring, rotated 30 degrees
P.append(lathe([(0.15, 0.0), (0.172, 0.0), (0.172, 0.026), (0.15, 0.026), (0.15, 0.0)], seg=6, material=RUNE,
               smooth=False, phase=TAU / 12))
# six spokes joining the rings (between the inner ring corners and the outer frame)
for k in range(6):
    a = TAU * k / 6
    o = bx((-0.012, 0.16, 0.0), (0.012, 0.225, 0.022), RUNE)
    place(o, (0, 0, 0), (0, 0, math.degrees(a)))
    P.append(o)
# central flame glyph
FL = [(0.00, -0.50), (0.22, -0.45), (0.36, -0.30), (0.40, -0.10), (0.33, 0.10), (0.30, 0.32), (0.18, 0.15), (0.10, 0.30),
      (0.02, 0.50), (-0.08, 0.30), (-0.16, 0.42), (-0.24, 0.18), (-0.36, 0.05), (-0.40, -0.12), (-0.35, -0.32), (-0.20, -0.46)]
P.append(prism([(x * 0.2, y * 0.22) for x, y in FL], 0.0, 0.034, RUNE))
body = part(P, 'body', (0, 0, 0), angle=30)

report(); print_ext()
std_view()
notes = ('Lava-bridge rune stone, lies flat. Part: body, origin centre bottom (0,0,0). Hexagonal frame r 0.3 (corner radius; '
         'flat-to-flat 0.52) z 0..0.04, inner hex ring r 0.17, six spokes and a central flame glyph; single material glow_rune '
         '(orange emissive; the game may fade it).')
finish('chars', 'lava_bridge_rune', kind='char', footprint=0.3, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('lava_bridge_rune'); montage('lava_bridge_rune', keys=('front', 'top'))
