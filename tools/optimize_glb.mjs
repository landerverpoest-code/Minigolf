// Verkleint GLB-bestanden voor de game: dubbele data samenvoegen, vertices lassen en quantiseren
// (KHR_mesh_quantization, wordt ondersteund door de GLTFLoader van three r128).
// Gebruik: node tools/optimize_glb.mjs <in.glb> <uit.glb>   (GT_DIR = map met node_modules van @gltf-transform)
import { createRequire } from 'module';
const GT = process.env.GT_DIR || '/tmp/claude-0/-home-user-Minigolf/4c79ae41-7166-567d-9db0-3f5c6b08d719/scratchpad/gt';
const require = createRequire(GT + '/package.json');
const { NodeIO } = require('@gltf-transform/core');
const { ALL_EXTENSIONS } = require('@gltf-transform/extensions');
const { dedup, weld, quantize, prune } = require('@gltf-transform/functions');
const [, , src, dst] = process.argv;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(src);
await doc.transform(dedup(), weld(), prune(), quantize({ quantizePosition: 14, quantizeNormal: 8, quantizeTexcoord: 12, quantizeColor: 8 }));
await io.write(dst, doc);
