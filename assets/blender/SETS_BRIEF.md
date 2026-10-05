# Brief wave 8: large set pieces (Blender → GLB)

Read `assets/blender/BRIEF.md`, `assets/blender/mglib.py` and `assets/blender/CHARS_BRIEF.md` first. The CHARS_BRIEF
rules apply, with these differences:
- Models go into their **theme folder**, with `kind='char'` and `grounded=False`. The game places them itself.
- These are large background buildings, so ≤ 6 materials, ≤ 4500 tris, ≤ 150 KB.

The game replaces blocky procedural buildings with these models at EXACTLY the same place and size, so the dimensions
are hard requirements. Units are metres, front = Blender −Y (it faces the golf course), and the origin is the
ground centre unless stated otherwise.

Check every Cycles preview with the Read tool and iterate until it looks genuinely good: chunky, charming,
saturated cartoon style matching the existing previews in that theme folder. Emissive window materials must be
named starting with `glow`. Run `node tools/glb_sheet.js <theme>` (NO ERRORS). List parts and extents in the manifest
`notes`.

Do NOT modify existing models. If a name already exists in the folder, append `_set` to yours and report it.

## `castle/castle_keep`: the big castle behind the castle holes
- **Main hall:** x −6..6, y −3..3, walls up to z 9 with crenellations on top, in light grey stone (blocks/bevels).
  A big arched wooden gate in the middle of the front (−Y) face, warm glowing windows (`glow_window`) in two rows,
  and stone trim.
- **Corner towers:** two round towers at x = ±6, y = 0, radius 1.8–2.0, height 13, each with a crenellated walkway
  ring and a red conical roof (base radius 2.3) up to z ≈ 17 with a small gold finial.
- **Optional:** a small third tower on the back roof.
- **Parts:**
  - `body`: everything above.
  - `banner`: a long blue banner with a gold emblem hanging on the front face above the gate, around (0, −3.05, 6).
    Pivot at its top centre; the game sways it.

## `haunted/haunted_mansion`: the spooky mansion on the haunted horizon
- **Main block:** x −8..8, y −3.5..3.5, walls to z 8, in crooked purple-grey wooden planks. Steep dark hip roof to
  z ≈ 13 with dormers, a crooked chimney and broken shingles.
- **Tower:** at x = 9, y = 0, radius 2, walls to z 14, with a pointed dark roof to z ≈ 19, a weather vane and a
  round attic window.
- **Windows:** 8 or more glowing windows (`glow_window`, warm orange) on the front, some boarded up, shutters
  hanging askew.
- **Front:** a porch with steps and two jack-o-lanterns.
- **Parts:** `body` only.

## `haunted/haunted_facade`: the spooky gable gateway the golf course passes UNDER
The opening below z 1.2 must stay completely free between x −1.4 and x 1.4, and beside it everywhere at
y −0.2..0.2 for x in −7..7. The ball rolls under the wall segments.
- **Wall segments:** two crooked wooden wall segments at x −7.0..−1.4 and x 1.4..7.0, z 1.2..2.6, thickness 0.3
  (y −0.15..0.15). They hang from:
- **Beam:** a heavy beam across x −7.15..7.15 at z 2.6..3.4.
- **Gable:** a triangular gable (base 13 wide at z 3.4, apex at z 6.6) above the beam, with planks, a glowing round
  window (`glow_window`) at z ≈ 4.4, bats/cobwebs carved in, and a small crooked sign "SPOOKHUIS".
- **No supports:** NO posts down to the ground (the course and its walls are below). It hangs like the original.
- **Parts:** `body` only.
