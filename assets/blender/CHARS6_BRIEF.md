# Brief wave 6: obstacle and prop models (Blender → GLB)

Read `assets/blender/BRIEF.md`, `assets/blender/mglib.py` and `assets/blender/CHARS_BRIEF.md` first. ALL rules of
CHARS_BRIEF apply:
- Folder `chars`, `kind='char'`, `grounded=False`.
- Named parts are separate objects with the origin on the pivot and zero rotation.
- Front = Blender −Y, units are metres.
- ≤ 6 materials, ≤ 3500 tris, ≤ 120 KB.
- Check every Cycles preview with the Read tool and iterate.
- `node tools/glb_sheet.js chars` must say NO ERRORS.

Do NOT touch existing models in `chars`. Look at a few previews in `assets/previews/chars/` (e.g. `door_wing`,
`blade_hub`, `knight`, `cow`) and match their chunky, saturated, slightly bevelled cartoon style.

The game positions these models EXACTLY over existing colliders, so the dimensions below are hard requirements. In
the manifest `notes`, list each part, its origin and its extents.

## Agent A
### `windmill_house` (hole 1, meadow): the mill house the ball rolls THROUGH; the sails turn in front of it
One part, `body`. Origin = ground centre of the house.
- **Two wing blocks:** x −3.0..−0.8 and x 0.8..3.0, each Y −1.3..1.3, height 2.6. White-washed plaster/brick with
  timber corners, small lit windows (bright yellow emissive material `glow_window`) and flower boxes on the front
  (−Y) face.
- **Middle section** above the passage: x −0.8..0.8, z 1.1..2.6.
- **The passage under the middle section MUST stay completely open:** x −0.8..0.8, z 0..1.1, through the whole depth.
  Give it an arched wooden portal look on both ends, but nothing may stick into that box.
- **Roof:** a red/brown thatched or tiled hip roof over the whole house, top at about z 5.0, with a small ridge
  cap. Keep the roof overhang ≤ 0.25.
- **Axle boss:** a sturdy wooden axle boss sticks out of the front face around (0, −1.3..−1.6, 2.7). The sails turn
  around the Y axis through (0, −1.6, 2.7), so do not put anything else within 3.2 m of that point in front of
  the face (Y < −1.35).

### `mill_sail`: ONE windmill sail; the game copies and rotates it
One part, `body`. Origin = the axle centre (0,0,0).
- **Spar:** a wooden spar runs from z +0.15 down to z −3.0 (it points DOWN, −Z). About 0.12 thick, at Y −0.12.
- **Lattice:** a lattice frame (side rails plus cross slats) on the +X side of the spar, x 0.06..0.68 from z −0.55
  to z −3.0.
- **Sail cloth:** cream cloth stretched on the lattice, slightly bulged, at Y about −0.14.
- **Hub piece** at the origin: a short cylinder r 0.18 along Y, so four copies form a nice hub.

### `carousel_horse` (castle carousel): a painted wooden carousel horse on a brass pole
One part, `body`. Origin = ground point under the pole.
- **Pole:** brass, r ≈ 0.035, from z 1.05 to z 3.25, with small decorative rings.
- **Horse:** centred around z 1.5, about 0.65 long, nose toward −Y, z 1.22..1.98. Galloping pose with the legs
  stretched, a carved mane and tail, and big friendly eyes.
- **Materials the game recolours (use these names exactly):**
  - `coat` for the body: white in Blender. The game tints it white, brown, black or grey.
  - `saddle` for the saddle and blanket: red in Blender. The game tints it red or blue.
- Gold bridle and trim.

## Agent B
### `gong` (volcano): a big ceremonial gong in an obsidian frame
Parts:
- **`body`**, the frame. Origin = ground centre (0,0,0).
  - Two square obsidian posts, 0.18 thick, at x = ±0.75, y = +0.15, z 0..2.0, each with a glowing-lava crack
    pattern (`glow_lava`) and a spiked cap up to z ≈ 2.3.
  - A crossbar x −0.88..0.88 at z 1.84..2.0, y +0.15.
  - Small carved fire glyphs.
- **`disc`**, the gong plate with its two hanging cords. Origin = the hanging pivot at (0, 0.15, 1.5).
  - A bronze disc with radius 0.55 and thickness 0.06, centred at (0, 0.15, 0.65), standing in the XZ plane so it
    faces −Y.
  - Concentric hammered rings, a raised central boss and a flame/sun emblem.
  - Two thin cords from the disc rim up to the crossbar at x = ±0.25.
  - The disc material must be named exactly **`gong_bronze`**: the game makes it glow.

### `swing_wall` (haunted crypt): a stone wall that pivots around its middle
Parts:
- **`body`**, the wall. Origin = ground centre (0,0,0), which is also the pivot.
  - Spans x −1.0..1.0 (the game scales X to the real length), z −0.05..1.25, thickness 0.28 centred on Y=0.
  - Old crypt stone blocks with moss and a slightly crumbled top edge.
  - A carved rune band on BOTH faces at z ≈ 0.9, using a material named exactly **`rune`** (dark base colour; the
    game drives its emissive green).
  - All repeating detail should run along X, because X is stretched.
- **`pillar`**: the central pivot pillar, static. Origin = ground centre.
  - Radius 0.27, height 1.6, with a stone cap, a carved skull or face on the front and an iron ring.
  - The wall passes through the pillar.

### `lava_bridge_rune` (optional, if time permits): a small glowing hexagonal rune stone that lies flat on the ground
One part, `body`. Origin at its centre bottom, r ≈ 0.3, height 0.04. Material `glow_rune`.
