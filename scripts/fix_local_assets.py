import os
import requests

ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
LIB_DIR = os.path.join(ROOT, "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/lib")
ESM_DIR = os.path.join(LIB_DIR, "esm")
MP_DIR = os.path.join(LIB_DIR, "mediapipe")

# Ensure base directories exist
os.makedirs(LIB_DIR, exist_ok=True)
os.makedirs(ESM_DIR, exist_ok=True)
os.makedirs(MP_DIR, exist_ok=True)

ASSETS = {
    # Standalone Bundles (ESM for importmap)
    os.path.join(ESM_DIR, "zod.js"): "https://cdn.jsdelivr.net/npm/zod@3.23.8/+esm",
    os.path.join(ESM_DIR, "lil-gui.js"): "https://cdn.jsdelivr.net/npm/lil-gui@0.19.2/+esm",
    os.path.join(ESM_DIR, "planck.js"): "https://cdn.jsdelivr.net/npm/planck-js@0.3.31/+esm",
    os.path.join(ESM_DIR, "pixi.js"): "https://cdn.jsdelivr.net/npm/pixi.js@7.4.2/+esm",
    os.path.join(ESM_DIR, "golden-layout.js"): "https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/+esm",
    os.path.join(ESM_DIR, "vision_bundle.js"): "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/vision_bundle.js",
    os.path.join(ESM_DIR, "openfeature.js"): "https://cdn.jsdelivr.net/npm/@openfeature/web-sdk@1.7.2/+esm",
    
    # Core Libs (Global/UMD)
    os.path.join(LIB_DIR, "babylon.js"): "https://cdn.babylonjs.com/babylon.js",
    os.path.join(LIB_DIR, "babylonjs.loaders.min.js"): "https://cdn.babylonjs.com/loaders/babylonjs.loaders.min.js",
    
    # CSS
    os.path.join(LIB_DIR, "goldenlayout-base.css"): "https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/dist/css/goldenlayout-base.css",
    os.path.join(LIB_DIR, "goldenlayout-dark-theme.css"): "https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/dist/css/themes/goldenlayout-dark-theme.css",
    
    # MediaPipe WASM & Models
    os.path.join(MP_DIR, "gesture_recognizer.task"): "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
    os.path.join(MP_DIR, "vision_wasm_internal.wasm"): "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm/vision_wasm_internal.wasm",
    os.path.join(MP_DIR, "vision_wasm_nosimd_internal.wasm"): "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm/vision_wasm_nosimd_internal.wasm",
    os.path.join(MP_DIR, "vision_wasm_internal.js"): "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm/vision_wasm_internal.js",
    os.path.join(MP_DIR, "vision_wasm_nosimd_internal.js"): "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm/vision_wasm_nosimd_internal.js",
    
    # Assets
    os.path.join(ESM_DIR, "flare.png"): "https://playground.babylonjs.com/textures/flare.png"
}

def download_file(url, path):
    print(f"Downloading {url} to {path}...")
    try:
        response = requests.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Success: {path} ({len(response.content)} bytes)")
    except Exception as e:
        print(f"❌ Failed: {url} -> {e}")

if __name__ == "__main__":
    for path, url in ASSETS.items():
        download_file(url, path)
