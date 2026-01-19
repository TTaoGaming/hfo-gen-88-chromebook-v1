# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import re

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_10.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add 'engine-canvas' flag to featureConfig (Default: false)
content = content.replace("'engine-babylon': true,", "'engine-babylon': true,\n            'engine-canvas': false,")

# 2. Add tuning parameters to systemState.parameters for Fire Lab V3 integration
old_phys = "planckDamping: z.number().min(0),"
new_phys = "planckDamping: z.number().min(0),\n            fireScale: z.number().min(0.1).default(1.0),\n            fireIntensity: z.number().min(0.1).default(1.0),"
content = content.replace(old_phys, new_phys)

# Also update the actual state object
old_st_phys = "planckDamping: 0.1,"
new_st_phys = "planckDamping: 0.1,\n                fireScale: 1.0, fireIntensity: 1.0,"
content = content.replace(old_st_phys, new_st_phys)

# 3. Use these parameters in the Babylon update loop (if they exist)
# I'll update the logic I just added to use scale/intensity if they are in systemState
new_babylon_update = """       // State based visuals (V24.10: FIRE LAB V3 PLASMA NEEDLE)
       const fireScale = systemState.parameters.physics.fireScale || 1.0;
       const fireInten = systemState.parameters.physics.fireIntensity || 1.0;
       
       if (c.fsmState === 'COMMIT' || (c.fsmState === 'COAST' && c.lastBaseState === 'COMMIT')) {
           const opacity = (c.fsmState === 'COAST') ? 0.6 : 1.0;
           systems.forEach(s => {
               s.minSize = 0.02 * fireScale; s.maxSize = 0.15 * fireScale; 
               if (s.name === "fire") {
                   s.emitRate = 2000 * fireScale;
                   s.color1 = new BABYLON.Color4(0.0, 0.8, 1.0, opacity); // Cyan Plasma
                   s.color2 = new BABYLON.Color4(0, 0.2, 1, 0.5 * opacity);
                   s.minLifeTime = 0.05; s.maxLifeTime = 0.15;
                   s.gravity = new BABYLON.Vector3(0, 30 * fireInten, 0); // Needle force
                   s.minEmitBox = new BABYLON.Vector3(-0.005 * fireScale, 0, -0.005 * fireScale);
                   s.maxEmitBox = new BABYLON.Vector3(0.005 * fireScale, 0.01, 0.005 * fireScale);
               }
           });
       } else {
           // READY state (Amber Fireball)
           const opacity = (c.fsmState === 'COAST') ? 0.4 : 1.0;
           systems.forEach(s => {
               s.minSize = 0.05 * fireScale; s.maxSize = 0.2 * fireScale; 
               if (s.name === "fire") {
                   s.emitRate = 800 * fireScale;
                   s.color1 = new BABYLON.Color4(1.0, 0.6, 0.1, opacity); // Amber
                   s.color2 = new BABYLON.Color4(1, 0.2, 0, 0.5 * opacity);
                   s.minLifeTime = 0.1; s.maxLifeTime = 0.3;
                   s.gravity = new BABYLON.Vector3(0, 4 * fireInten, 0);
                   s.minEmitBox = new BABYLON.Vector3(-0.02 * fireScale, -0.02 * fireScale, -0.02 * fireScale);
                   s.maxEmitBox = new BABYLON.Vector3(0.02 * fireScale, 0.02 * fireScale, 0.02 * fireScale);
               }
           });
       }"""

# Replace the block I added previously
content = re.sub(
    r'// State based visuals \(V24\.10: FIRE LAB V3 PLASMA NEEDLE\).*?maxEmitBox = new BABYLON\.Vector3\(0\.02, 0\.02, 0\.02\);\s+\}\s+\)\s+\;\s+\}',
    new_babylon_update + ' });\n       }',
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("UX Configuration and Scaling Logic complete.")
