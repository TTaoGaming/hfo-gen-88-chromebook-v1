import sys
import os
import re

filepath = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_10.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Fix Babylon Constructor (Correct ID, Z-Index, and Pointer-Events)
# This prevents the "Glass Barrier" UI bug.
pattern_constructor = r"this\.canvas = document\.createElement\('canvas'\);\s+this\.canvas\.style\.width = '100%';\s+this\.canvas\.style\.height = '100%';\s+this\.canvas\.style\.display = 'none'; // Hidden by default\s+container\.appendChild\(this\.canvas\);"
replacement_constructor = """this.canvas = document.createElement('canvas');
                this.canvas.id = 'babylon-canvas';
                this.canvas.style.position = 'absolute';
                this.canvas.style.left = '0';
                this.canvas.style.top = '0';
                this.canvas.style.width = '100%';
                this.canvas.style.height = '100%';
                this.canvas.style.pointerEvents = 'none';
                this.canvas.style.zIndex = '9';
                this.canvas.style.display = 'none'; // Hidden by default
                container.appendChild(this.canvas);"""
content = re.sub(pattern_constructor, replacement_constructor, content, flags=re.MULTILINE)

# 2. Fix updateVisuals/update(cursors) with v24.8 Fire Lab V3 logic
# We'll use Pareto Optimal hardcoded defaults: Scale 1.0, Intensity 1.0
new_visual_logic = """       // State based visuals (V24.10: FIRE LAB V3 PLASMA NEEDLE)
       if (c.fsmState === 'COMMIT' || (c.fsmState === 'COAST' && c.lastBaseState === 'COMMIT')) {
           const opacity = (c.fsmState === 'COAST') ? 0.6 : 1.0;
           systems.forEach(s => {
               s.minSize = 0.02; s.maxSize = 0.15; 
               if (s.name === "fire") {
                   s.emitRate = 2000;
                   s.color1 = new BABYLON.Color4(0.0, 0.8, 1.0, opacity); // Cyan Plasma
                   s.color2 = new BABYLON.Color4(0, 0.2, 1, 0.5 * opacity);
                   s.minLifeTime = 0.05; s.maxLifeTime = 0.15;
                   s.gravity = new BABYLON.Vector3(0, 30, 0); // Needle force
                   s.minEmitBox = new BABYLON.Vector3(-0.005, 0, -0.005);
                   s.maxEmitBox = new BABYLON.Vector3(0.005, 0.01, 0.005);
               }
           });
       } else {
           // READY state (Amber Fireball)
           const opacity = (c.fsmState === 'COAST') ? 0.4 : 1.0;
           systems.forEach(s => {
               s.minSize = 0.05; s.maxSize = 0.2; 
               if (s.name === "fire") {
                   s.emitRate = 800;
                   s.color1 = new BABYLON.Color4(1.0, 0.6, 0.1, opacity); // Amber
                   s.color2 = new BABYLON.Color4(1, 0.2, 0, 0.5 * opacity);
                   s.minLifeTime = 0.1; s.maxLifeTime = 0.3;
                   s.gravity = new BABYLON.Vector3(0, 4, 0);
                   s.minEmitBox = new BABYLON.Vector3(-0.02, -0.02, -0.02);
                   s.maxEmitBox = new BABYLON.Vector3(0.02, 0.02, 0.02);
               }
           });
       }"""

# Use re.DOTALL to match across lines
content = re.sub(
    r'// State based visuals \(V24.7: PHX CORE SCALING\).*?if \(s\.name === "fire"\) \{.*?s\.color1 = new BABYLON\.Color4\(1, 0\.6, 0\.2, 1\.0\);.*?\}\s+ \}\s+ \);',
    new_visual_logic + ' } });',
    content,
    flags=re.DOTALL
)

# 3. Gate legacy canvas results to prevent "muddiness"
old_draw = """            // V19.5: Unified Draw Call (Only skeleton receives raw results for ISR overlay)
            drawResults(results, systemState.dataFabric);"""
new_draw = """            // V24.10: Substrate Gating (Prevent visual muddiness when Babylon is active)
            if (isFlagEnabled('engine-canvas')) {
                drawResults(results, systemState.dataFabric);
            }"""
content = content.replace(old_draw, new_draw)

# 4. Fix createEffect parameters for fast precision particles (V24.10)
pattern_create_effect = r'fire\.minLifeTime = 0\.2; fire\.maxLifeTime = 0\.5;'
replacement_create_effect = 'fire.minLifeTime = 0.05; fire.maxLifeTime = 0.15;'
content = content.replace(pattern_create_effect, replacement_create_effect)

# 5. Fix emission rate in createEffect
content = re.sub(r'fire\.emitRate = 400;', 'fire.emitRate = 1200;', content)
content = re.sub(r'fire\.gravity = new BABYLON\.Vector3\(0, 15, 0\);', 'fire.gravity = new BABYLON.Vector3(0, 40, 0);', content)

with open(filepath, 'w') as f:
    f.write(content)

print("Restoration and Fire Lab V3 integration complete.")
