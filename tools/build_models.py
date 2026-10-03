#!/usr/bin/env python3
"""Bundelt de Blender-modellen (assets/models/<thema>/*.glb + manifest.json) per thema in models/<thema>.js.

Elk bestand doet: MG_MODELS['<thema>'] = { manifest: [...], data: { naam: '<base64 glb>' } }.
De game laadt die pakketjes op de achtergrond (eerst het thema dat ze nodig heeft). Ontbreekt een
pakket (bv. alleen index.html gedownload), dan valt ze terug op de procedurele decoratie.
Gebruik: python3 tools/build_models.py
"""
import base64, json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, 'models'), exist_ok=True)
grand = 0
for mf in sorted(glob.glob(os.path.join(ROOT, 'assets/models/*/manifest.json'))):
    theme = os.path.basename(os.path.dirname(mf))
    if theme.startswith('_'):
        continue
    manifest, data, total = [], {}, 0
    for e in json.load(open(mf)):
        glb = os.path.join(ROOT, 'assets', e['file'])
        if not os.path.exists(glb):
            continue
        raw = open(glb, 'rb').read(); total += len(raw)
        data[e['name']] = base64.b64encode(raw).decode()
        manifest.append({k: e[k] for k in ('name', 'kind', 'footprint', 'height', 'size', 'spin') if k in e})
    out = os.path.join(ROOT, 'models', theme + '.js')
    with open(out, 'w') as f:
        f.write(f'// Automatisch gegenereerd door tools/build_models.py uit assets/models/{theme} (Blender). Niet met de hand aanpassen.\n')
        f.write(f"(window.MG_MODELS = window.MG_MODELS || {{}})['{theme}'] = " + json.dumps({'manifest': manifest, 'data': data}, separators=(',', ':')) + ';\n')
    grand += os.path.getsize(out)
    print(f'{theme:8s} {len(manifest):3d} modellen  {total / 1024:6.0f} KB glb -> {os.path.getsize(out) / 1024:6.0f} KB')
print(f'totaal {grand / 1024:.0f} KB')
