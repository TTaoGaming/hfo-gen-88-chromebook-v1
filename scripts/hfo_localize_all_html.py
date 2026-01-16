import os
import re

# Medallion: Bronze | Mutation: 0% | HIVE: I
# SCRIPTS/HFO_LOCALIZE_SESSION.py
# Purpose: Mass-patch HTML files for 100% offline dependency resolution.

REPLACEMENTS = [
    # GoldenLayout CSS
    (r"https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/dist/css/goldenlayout-base.css", "./lib/css/goldenlayout-base.css"),
    (r"https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/dist/css/themes/goldenlayout-dark-theme.css", "./lib/css/goldenlayout-dark-theme.css"),
    
    # Babylon.js
    (r"https://cdn.babylonjs.com/babylon.js", "./lib/js/babylon.js"),
    (r"https://cdn.babylonjs.com/loaders/babylonjs.loaders.min.js", "./lib/js/babylon.loaders.min.js"),
    
    # OpenFeature
    (r"https://cdn.jsdelivr.net/npm/@openfeature/web-sdk@0.7.0/dist/web-sdk.min.js", "./lib/js/web-sdk.min.js"),
    (r"https://cdn.jsdelivr.net/npm/@openfeature/web-sdk@latest/dist/web-sdk.min.js", "./lib/js/web-sdk.min.js"),
    
    # ImportMap ESM (Standardizing on v30 reference)
    (r"https://cdn.jsdelivr.net/npm/golden-layout@2.6.0/\+esm", "./lib/js/golden-layout.esm.js"),
    (r"https://cdn.jsdelivr.net/npm/lil-gui@0.19.1/\+esm", "./lib/js/lil-gui.esm.js"),
    (r"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js", "./lib/js/vision_bundle.js"),
    (r"https://cdn.jsdelivr.net/npm/zod@3.22.4/\+esm", "./lib/js/zod.esm.js"),
    (r"https://cdn.jsdelivr.net/npm/planck-js@0.10.2/dist/planck.esm.js", "./lib/js/planck.esm.js"),
    (r"https://cdn.jsdelivr.net/npm/planck-js@0.3.1/\+esm", "./lib/js/planck.esm.js"),
    
    # Excalidraw sub-dependencies
    (r"https://unpkg.com/react@18/umd/react.production.min.js", "./lib/js/react.min.js"),
    (r"https://unpkg.com/react-dom@18/umd/react-dom.production.min.js", "./lib/js/react-dom.min.js"),
    (r"https://unpkg.com/@excalidraw/excalidraw/dist/excalidraw.production.min.js", "./lib/js/excalidraw.min.js"),
]

TARGET_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/"

def patch_file(file_path):
    print(f"⚙️ [PATCHING]: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ [PATCHED]: {file_path}")
    else:
        print(f"⏭️ [SKIPPED]: {file_path} (No matches)")

if __name__ == "__main__":
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".html"):
                patch_file(os.path.join(root, file))
