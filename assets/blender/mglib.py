"""Gedeelde Blender-helpers voor de minigolf-decoratie.

Gebruik (headless, Blender als Python-module 'bpy' 4.2):
    import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
    from mglib import *
    reset()
    ... modelleren ...
    finish('meadow', 'oak_tree', kind='scatter', footprint=0.6)

Afspraken:
- Eenheden in meter. Blender is Z-omhoog; de glTF-export zet dat om naar Y-omhoog voor three.js.
- Oorsprong = midden van de voet (grond op z=0).
- Alleen materiaalkleuren (Principled BSDF), geen beeldtextures. Max ~4 materialen per model.
- Renderen ALLEEN met Cycles (CPU). Eevee/Workbench crashen hier (geen EGL).
"""
import bpy, bmesh, math, os, json, random
from mathutils import Vector, Matrix, Euler

ROOT = '/home/user/Minigolf/assets'
_MATS = {}


def reset():
    """Lege scène."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _MATS.clear()


def mat(name, color, rough=0.8, metal=0.0, emit=None, emit_strength=1.0, alpha=1.0):
    """Materiaal (hergebruikt per naam). color = '#rrggbb' of (r,g,b) in 0..1 (sRGB)."""
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*_lin(color), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit is not None:
        b.inputs['Emission Color'].default_value = (*_lin(emit), 1)
        b.inputs['Emission Strength'].default_value = emit_strength
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
        m.blend_method = 'BLEND'
    _MATS[name] = m
    return m


def _lin(c):
    if isinstance(c, str):
        c = c.lstrip('#'); c = tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def _new(op, material=None, smooth=False, **kw):
    op(**kw)
    o = bpy.context.active_object
    if material is not None:
        o.data.materials.append(material)
    if smooth:
        shade_smooth(o)
    return o


def box(size=(1, 1, 1), loc=(0, 0, 0), rot=(0, 0, 0), material=None, bevel=0.0):
    o = _new(bpy.ops.mesh.primitive_cube_add, material, size=1, location=loc, rotation=rot)
    o.scale = size
    apply(o)
    if bevel > 0:
        bev(o, bevel)
    return o


def cyl(r=0.5, h=1, loc=(0, 0, 0), rot=(0, 0, 0), verts=12, material=None, r2=None, smooth=False):
    """Cilinder of afgeknotte kegel (r2 = bovenstraal). loc = midden."""
    if r2 is None:
        o = _new(bpy.ops.mesh.primitive_cylinder_add, material, smooth, vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    else:
        o = _new(bpy.ops.mesh.primitive_cone_add, material, smooth, vertices=verts, radius1=r, radius2=r2, depth=h, location=loc, rotation=rot)
    return o


def cone(r=0.5, h=1, loc=(0, 0, 0), rot=(0, 0, 0), verts=10, material=None, smooth=False):
    return _new(bpy.ops.mesh.primitive_cone_add, material, smooth, vertices=verts, radius1=r, radius2=0, depth=h, location=loc, rotation=rot)


def sphere(r=0.5, loc=(0, 0, 0), seg=12, rings=8, material=None, smooth=True, scale=(1, 1, 1)):
    o = _new(bpy.ops.mesh.primitive_uv_sphere_add, material, smooth, segments=seg, ring_count=rings, radius=r, location=loc)
    o.scale = scale; apply(o)
    return o


def ico(r=0.5, loc=(0, 0, 0), sub=1, material=None, smooth=False, scale=(1, 1, 1), jitter=0.0, seed=0):
    """Icosfeer, optioneel met willekeurige vervorming (rotsen, boomkruinen)."""
    o = _new(bpy.ops.mesh.primitive_ico_sphere_add, material, smooth, subdivisions=sub, radius=r, location=loc)
    o.scale = scale; apply(o)
    if jitter:
        rnd = random.Random(seed)
        for v in o.data.vertices:
            v.co += Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * jitter
    return o


def torus(R=1, r=0.2, loc=(0, 0, 0), rot=(0, 0, 0), seg=16, ring=8, material=None, smooth=True):
    return _new(bpy.ops.mesh.primitive_torus_add, material, smooth, major_radius=R, minor_radius=r, major_segments=seg, minor_segments=ring, location=loc, rotation=rot)


def apply(o):
    """Transformaties toepassen."""
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return o


def bev(o, w=0.03, seg=1):
    m = o.modifiers.new('bev', 'BEVEL'); m.width = w; m.segments = seg; m.limit_method = 'ANGLE'
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
    return o


def shade_smooth(o, angle=50):
    bpy.context.view_layer.objects.active = o
    for p in o.data.polygons:
        p.use_smooth = True
    try:
        o.data.set_sharp_from_angle(angle=math.radians(angle))
    except Exception:
        pass
    return o


def join(objs, name='model'):
    objs = [o for o in objs if o is not None]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    o = bpy.context.active_object; o.name = name
    return o


def tris(objs=None):
    objs = objs or [o for o in bpy.context.scene.objects if o.type == 'MESH']
    n = 0
    for o in objs:
        dg = bpy.context.evaluated_depsgraph_get(); me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles(); n += len(me.loop_triangles); o.evaluated_get(dg).to_mesh_clear()
    return n


def bounds(objs=None):
    objs = objs or [o for o in bpy.context.scene.objects if o.type == 'MESH']
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def ground():
    """Model zo verschuiven dat de laagste punt op z=0 staat (x/y blijven, oorsprong = voetmidden)."""
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs)
    for o in objs:
        o.location.z -= lo.z
    bpy.context.view_layer.update()


def render_preview(path, size=384, samples=24, bg='#8fb8de'):
    """Snelle Cycles-render in 3/4-aanzicht, automatisch ingekaderd."""
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs); c = (lo + hi) / 2; ext = max((hi - lo).length, 0.5)
    cam = bpy.data.objects.new('pvcam', bpy.data.cameras.new('pvcam')); scene.collection.objects.link(cam)
    cam.data.lens = 50
    d = Vector((1.0, -1.25, 0.8)).normalized() * ext * 1.55
    cam.location = c + d
    cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler(); scene.camera = cam
    sun = bpy.data.objects.new('pvsun', bpy.data.lights.new('pvsun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.5; sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    if scene.world is None:
        scene.world = bpy.data.worlds.new('w')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (*_lin(bg), 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = samples
    scene.render.resolution_x = scene.render.resolution_y = size
    scene.render.filepath = path; scene.render.image_settings.file_format = 'PNG'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam); bpy.data.objects.remove(sun)


def export_glb(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                              export_texcoords=False, export_normals=True, export_materials='EXPORT', export_cameras=False,
                              export_lights=False, export_animations=False, export_extras=False)


def finish(theme, name, kind='scatter', footprint=0.5, notes='', preview=True, grounded=True, **extra):
    """Model op de grond zetten, exporteren, preview renderen en manifest bijwerken.
    kind: 'scatter' (veel kopieën in de omgeving), 'hero' (groot opvallend stuk, 1-3 keer),
          'edge' (klein detail vlak naast de baan), 'post' (vervangt een paal-obstakel op de baan, footprint = botsstraal!)
    footprint: straal in meter van de voet (voor plaatsing zonder overlap met de baan)."""
    if grounded:
        ground()
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    lo, hi = bounds(objs)
    n = tris(objs)
    glb = f'{ROOT}/models/{theme}/{name}.glb'
    export_glb(glb)
    if preview:
        render_preview(f'{ROOT}/previews/{theme}/{name}.png')
    entry = dict(name=name, theme=theme, file=f'models/{theme}/{name}.glb', kind=kind, footprint=round(footprint, 3),
                 height=round(hi.z - lo.z, 3), size=[round(hi.x - lo.x, 3), round(hi.y - lo.y, 3)], tris=n,
                 bytes=os.path.getsize(glb), notes=notes, **extra)
    mf = f'{ROOT}/models/{theme}/manifest.json'
    data = json.load(open(mf)) if os.path.exists(mf) else []
    data = [e for e in data if e['name'] != name] + [entry]
    json.dump(sorted(data, key=lambda e: e['name']), open(mf, 'w'), indent=1)
    print('MODEL', json.dumps(entry))
    return entry
