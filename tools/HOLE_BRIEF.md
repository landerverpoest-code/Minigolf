# Brief: new holes for Minigolf Avontuur 3D

The whole game is `index.html` (three.js r128, ~3500 lines, Dutch comments). There are 9 themed holes
(one per theme). The goal is **3 holes per theme → 2 new holes per theme**. You design the new holes for
the themes assigned to you.

## Read first
- `index.html` section `HOLE-DATA` (search `const HOLES = []`): the 9 existing holes. Every key is
  shown in use there: `floor` (polygons; `surf`, `h`, `ramp`, `bridge`, `over`, `id`), `walls` (`LINE`/`LOOP`
  polylines, `style`, `h`, `t`), `zones` (sand, mud, snow, slope with `acc`, lava, water, quicksand, lowg,
  rock, `id`, `hidden`), `posts` (round obstacles with `kind`), `blocks`, `bumpers`, `movers`, `specials`,
  `torches`, `set`, `deco`, `theme`.
- Helpers: `RECT(x0,z0,x1,z1)`, `CIRC(cx,cz,r,n,rot)`, `ARC(cx,cz,r,a0,a1,n)`, `PLANK(p0,p1,w)`, `LINE`, `LOOP`,
  `islandWalls(...)`, `offsetLine(...)`.
- `MOVERS` (rotbar, slider, ring, windmill, drawbridge) and `SPECIALS` (cow, boulder, knight, crab, penguin,
  scorpion, ghost, drone, dragon, switchGate, shield, eruption, tide, floes, tornado, lanterns, swingwall,
  planet): read the code of the ones you use to learn their parameters.
- `ENV` (search `const ENV = {`): theme environments. Fixed set-pieces are only built when the hole asks for
  them through `set` (volcano `set.cone`; castle `set.moat`, `set.arches`, `set.keep`; ice `set.channels`,
  `set.igloo`; desert `set.gorge`, `set.gorgeArches`, `set.pyramid`, `set.sphinx`; haunted `set.pit`,
  `set.facade`, `set.housePosts`, `set.candles`, `set.mansion`, `set.pumpkins`; space `set.strips`; finale
  `set.arch`, `set.gatehouse`, `set.flags`; water `deco.islands` = `[[[x,z],r],...]`, `deco.wheel`, `deco.falls`).
  Example: a floes channel needs `set.channels`, a tornado-over-a-gorge needs `set.gorge`.
- Coordinates: `[x, z]` in metres. The ball has radius 0.22, walls are ~0.5 high and `WALL_T` thick. Courses so
  far run from the start toward negative z, are 40–65 m long, fairways 4–7 m wide, pars 3–6.

## What makes a good new hole
- A **clearly different layout** from the theme's existing hole (different route shape: S-bend, loop, split
  paths, islands, plateaus with ramps, a big open arena, a risky shortcut vs. a safe detour …).
- At least one **course-changing element** (something that opens/closes/creates a route over time or when hit)
  and at least one **moving character/obstacle**, using the theme's flavour. Re-using the theme's existing
  specials in a new configuration is good; combining with other elements is good; a NEW special/mover type is
  allowed if it is well made (see rules).
- Visual identity per hole: give each new hole its own `name`, `icon` and a variation of the theme's `theme`
  block (same `env`, `wall`, `surf` family, but e.g. a different time of day: other `sky`/`sun`/`hemi`/`fog`
  colours, other flag colour, music `seed` and maybe `root`/`tempo`). `themeName` must be EXACTLY the theme's
  existing `themeName` (Weide, Vulkaan, Kasteel, Eilanden, IJs, Woestijn, Spookhuis, Ruimte, Finale).
- Every special needs Dutch `name` and `desc` (shown in the instructions screen). Dutch comments in code.
- Fair: the bot must be able to solve it, nothing may trap the ball, no unwinnable timing.

## Rules
1. Add your holes as `HOLES.push({...})` blocks in ONE marked block placed right after the last existing hole
   (after the `HOLE 9` block, before the `RENDERER / SCENE` banner):
   `// ===== NIEUWE HOLES (<your themes>) =====`. Each block starts with a comment line
   `// ---------- <Theme> 2: <Name> ----------` (or 3) plus 1–2 lines describing the route.
2. Only add NEW specials/movers in a marked block at the end of `SPECIALS`/`MOVERS`:
   `// ----- nieuw (<your themes>) -----`. Use names that cannot clash (e.g. prefix with the theme).
   They must implement the kinematic interface used by the others (`group`, `prims`, `update(t,h,ball)`,
   `visual(t,dt)`, optional `onHit`, optional `reset()` for button-like things that must reset at a new turn)
   and run on the game clock `t` (never wall time), so they keep moving forever.
3. Do not change engine/physics/UI code. If you truly need an engine fix, make it minimal, backwards
   compatible, and list it in your report. Small additive `set.*` options in `ENV` are OK (list them).
4. Buttons/triggers stay open for the rest of the turn (the user explicitly wants that).
5. Commit your work in your worktree when done (`git add -A && git commit -m "..."`); do NOT push.

## Testing (all must pass for every new hole; new holes get indices 9, 10, … in your copy)
Run from your worktree root (the tools use `../index.html` relative to `tools/`):
- `node tools/smoke.js 9,10,11,12,13,14 <shotdir>` → `NO ERRORS`; look at the screenshots
  (`h10_overview.png`, `h10_start.png`, …) with the Read tool: course readable, decor not on the course,
  start camera sensible (`aim`).
- `node tools/solve.js 9` (one index at a time; a beam-search bot) → `solvedIn` ≤ `par` (≤ par+1 only if the
  hole is deliberately hard; then raise par). Takes 1–5 min per hole.
- `node tools/phys.js 9,10` → `tunnel: 0`, `pen: 0`, `notStopped: 0` (random shots incl. very hard ones).
- `node tools/kin.js 9,10` → `worstOverlapSteps` < 60 and no `stk` entries (ball never stuck in a mover).
- `node tools/motion.js` style check if you add movers: every moving element still moves after 60 s.
- Debug hook in the page: `window.__mg = { G, H: () => H, ball, HOLES, loadHole, shoot, physicsStep, startGame, … }`.

## Report
End with: per hole name, theme, par, solver result, phys/kin results, the elements used, any new
special/mover types, any `set` options or engine changes, and the worktree branch name with your commit.
