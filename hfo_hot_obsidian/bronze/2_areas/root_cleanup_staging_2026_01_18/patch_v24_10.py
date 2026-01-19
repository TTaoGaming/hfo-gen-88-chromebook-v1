# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import re

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_10.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix 1: Update createEffect for "Beautiful" fire
# Search for fire.minLifeTime = 0.2; fire.maxLifeTime = 0.5; and the surrounding lines
content = re.sub(
    r'fire\.minLifeTime = 0\.2; fire\.maxLifeTime = 0\.5;.*?fire\.emitRate = 400;.*?fire\.gravity = new BABYLON\.Vector3\(0, 15, 0\);',
    'fire.minLifeTime = 0.05; fire.maxLifeTime = 0.15;\n                fire.emitRate = 1200;\n                fire.blendMode = BABYLON.ParticleSystem.BLENDMODE_ONEONE;\n                fire.gravity = new BABYLON.Vector3(0, 40, 0);',
    content,
    flags=re.DOTALL
)

# Fix 2: Update update() for Coast Fading and Red/Amber Purity
new_visuals = """// State based visuals (V24.10: PHX CORE SCALING with COAST Fading)
       if (c.fsmState === 'COMMIT' || c.fsmState === 'COAST') {
           const isCoast = c.fsmState === 'COAST';
           const opacity = isCoast ? 0.6 : 1.0;
           systems.forEach(s => {
               s.minSize = 0.4; s.maxSize = 1.0; 
               if (s.name === "fire") {
                   s.emitRate = isCoast ? 800 : 2500;
                   s.color1 = new BABYLON.Color4(1, 0.2, 0, opacity); // HFO Red-Orange
               }
           });
       } else {
           systems.forEach(s => {
               s.minSize = 0.1; s.maxSize = 0.4; 
               if (s.name === "fire") {
                   s.emitRate = 800;
                   s.color1 = new BABYLON.Color4(1, 0.7, 0.1, 1.0); // Amber Ready
               }
           });
       }"""

content = re.sub(
    r'// State based visuals \(V24.7: PHX CORE SCALING\).*?if \(s\.name === "fire"\) \{.*?s\.color1 = new BABYLON\.Color4\(1, 0\.6, 0\.2, 1\.0\);.*?\}\s+ \}\s+ \);',
    new_visuals + ' } });',
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Patch complete.")
