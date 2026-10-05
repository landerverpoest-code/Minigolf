# Brief wave 7: ambient creatures and vehicles (Blender → GLB)

Read `assets/blender/BRIEF.md`, `assets/blender/mglib.py` and `assets/blender/CHARS_BRIEF.md` first. The CHARS_BRIEF
rules apply, with ONE difference: these models go into their **theme folder** (not `chars`), each still with
`kind='char'` and `grounded=False`.

The game animates them in the background around the course, seen from 10–60 m away, so the following matter most:
- clear silhouettes, saturated colours and charm;
- the named parts below, each a separate object with its origin on the pivot and zero rotation;
- front = Blender −Y, units in metres.

Limits and checks:
- ≤ 6 materials, ≤ 3000 tris, ≤ 100 KB per model.
- Check every Cycles preview with the Read tool and iterate.
- Run `node tools/glb_sheet.js <theme>` for each theme you touch (NO ERRORS).

Do not modify existing models.

Emissive materials must have a name that starts with `glow` (the game handles those). In the manifest `notes`,
list each part and its pivot.

## Agent C
### `meadow/hot_air_balloon`: a big colourful hot-air balloon, total height ~9 m
- **`body`**: the envelope (vertical gores in bright alternating colours, e.g. red/yellow/blue, with a pattern
  band) plus ropes and a wicker basket at the bottom (basket ~1.4 m wide, bottom at z = 0) holding a tiny waving
  passenger. Origin at the basket bottom centre.
- **`flame`**: the burner flame just above the basket, origin at its base, material `glow_flame`. The game
  flickers it.

### `meadow/sheep`: a fluffy cartoon sheep, ~1.0 m long, ~0.8 m high
- **`body`**: cloud-like wool built from lumpy spheres, plus a black face.
- **`head`**: black face, white wool tuft, ears and big eyes. Pivot at the neck; the game makes it graze (nod down).
- **Legs:** `leg_fl`, `leg_fr`, `leg_bl`, `leg_br`, black, pivot at the hip, hooves at z = 0.

### `water/dolphin`: a friendly bottlenose dolphin, ~2.2 m long
- **`body`**: grey-blue top, pale belly, smiling beak and big eye. Origin at its body CENTRE, pointing nose to −Y.
- **`tail`**: the flukes, pivot at the tail stock; the game beats it up and down.

The game makes it leap out of the water in arcs.

### `desert/tumbleweed`: a ball of dry, tangled twigs, radius exactly 0.6, origin at its CENTRE
- **`body`**: many thin curved branch tubes in light tan and brown, airy (you can see through it), ≤ 2500 tris.

The game rolls it across the sand.

### `ice/polar_bear`: a chunky cute polar bear, ~1.8 m long, ~1.1 m high
- **`body`**: creamy white body.
- **`head`**: pivot at the neck, with a black nose, small round ears and big eyes.
- **Legs:** `leg_fl`, `leg_fr`, `leg_bl`, `leg_br`, pivot at the hip/shoulder, paws at z = 0.

## Agent D
### `space/ufo`: a classic flying saucer, ~3.2 m wide, origin at its CENTRE
- **`body`**: metallic saucer with a ring of coloured lights (material `glow_ufo_lights`) and a glass dome with a
  tiny green alien waving inside.
- **`beam`**: a translucent cone of light pointing down under it, 2.5 m long, origin at the top of the cone (the
  saucer's underside), material `glow_beam`. The game fades it.

### `space/astronaut`: a cute chunky astronaut, ~1.7 m tall, floating, origin at the body CENTRE
- **`body`**: white suit with orange patches and a backpack.
- **`head`**: the helmet with a gold reflective visor (material `visor`), pivot at the neck.
- **`arm_l`**, **`arm_r`**: pivot at the shoulder; the game waves them.

The game slowly tumbles it through space.

### `haunted/witch`: a witch riding a broomstick, ~1.8 m long broom, origin at the broom CENTRE
The broom lies along Y with its bristles at +Y (the back) and the handle pointing to −Y.
- **`body`**: broom plus witch (pointy purple hat, green face with a big grin, black dress, purple-striped
  stockings).
- **`cape`**: pivot at the shoulders, flowing backwards; the game flaps it.
- **`cat`**: a tiny black cat sitting on the bristles, pivot at its feet.

### `castle/dragon_flyer`: a small friendly red dragon flying in circles over the castle, ~2.5 m long
Origin at the body CENTRE, nose to −Y.
- **`body`**: red body, yellow belly plates, horns, big eyes, and a long tail curving behind.
- **`wing_l`**, **`wing_r`**: membranous bat wings, pivot at the shoulder; the game flaps them around Y.
