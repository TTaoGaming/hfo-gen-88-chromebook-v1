# Medallion: Bronze | Mutation: 0% | HIVE: V
# Medallion: Bronze | Mutation: 0% | HIVE: I
import os

FILE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_11.html"

with open(FILE_PATH, 'r') as f:
    content = f.read()

# 1. Update title and version header
content = content.replace("<title>HFO OMEGA GEN 4 | V24.10</title>", "<title>HFO OMEGA GEN 4 | V24.11</title>")
content = content.replace("<!-- OMEGA GEN 4 V24.10 (Babylon Substrate Integration) -->", "<!-- OMEGA GEN 4 V24.11 (Enhanced Visual Scion) -->")
content = content.replace("<!-- Restoration of v24.7 Interaction Baseline -->", "<!-- Default Scale 2.0 | Enhanced Trails -->")

# 2. Add defaults to systemState.parameters.physics
old_physics = """                physics: {
                    mode: 'PLANCK_SPRING',
                    useDirectProjection: true, // V20.6 Feature Flag (Default ON)
                    directProjectionOffset: 0.04, // V20.6 Custom Offset for Direct projection
                    cursorTheme: 'LI', // V20.5 stable evolution
                    oneEuroMinCutoff: 0.85,
                    oneEuroBeta: 0.02,
                    oneEuroRodMinCutoff: 0.8,
                    planckStiffness: 4.5,
                    planckDamping: 1.2,
                    palmRodMultiplier: 0.64,
                    showLaserBeam: true,
                    predictiveLookahead: 0.5
                },"""

new_physics = """                physics: {
                    mode: 'PLANCK_SPRING',
                    useDirectProjection: true, // V20.6 Feature Flag (Default ON)
                    directProjectionOffset: 0.04, // V20.6 Custom Offset for Direct projection
                    fireScale: 2.0, // V24.11: Default increased for visibility
                    fireIntensity: 2.0, // V24.11: Default increased for visibility
                    cursorTheme: 'LI', // V20.5 stable evolution
                    oneEuroMinCutoff: 0.85,
                    oneEuroBeta: 0.02,
                    oneEuroRodMinCutoff: 0.8,
                    planckStiffness: 4.5,
                    planckDamping: 1.2,
                    palmRodMultiplier: 0.64,
                    showLaserBeam: true,
                    predictiveLookahead: 0.5
                },"""

content = content.replace(old_physics, new_physics)

# 3. Enhance Trails in update logic
old_update_logic = """                        if (c.fsmState === 'COMMIT' || c.fsmState === 'COAST') {
                            systems.forEach(s => {
                                s.color1 = new BABYLON.Color4(0.0, 0.8, 1.0, 1.0); // Cyan Plasma
                                s.color2 = new BABYLON.Color4(0, 0.2, 1, 0.5);
                                s.emitRate = 1200 * scale;
                                s.minSize = 0.02 * scale;
                                s.maxSize = 0.15 * scale;
                                s.minLifeTime = 0.05;
                                s.maxLifeTime = 0.15;
                                s.gravity = new BABYLON.Vector3(0, 15 * intensity, 0);
                            });
                        } else {
                            systems.forEach(s => {
                                s.color1 = new BABYLON.Color4(1.0, 0.6, 0.1, 1.0); // Amber Fire 
                                s.color2 = new BABYLON.Color4(1, 0.2, 0, 0.5);
                                s.emitRate = 400 * scale;
                                s.minSize = 0.05 * scale;
                                s.maxSize = 0.2 * scale;
                                s.minLifeTime = 0.1;
                                s.maxLifeTime = 0.3;
                                s.gravity = new BABYLON.Vector3(0, 2 * intensity, 0);
                            });
                        }"""

new_update_logic = """                        if (c.fsmState === 'COMMIT' || c.fsmState === 'COAST') {
                            systems.forEach(s => {
                                s.color1 = new BABYLON.Color4(0.0, 0.8, 1.0, 1.0); // Cyan Plasma
                                s.color2 = new BABYLON.Color4(0, 0.2, 1, 0.5);
                                s.emitRate = 1200 * scale;
                                s.minSize = 0.02 * scale;
                                s.maxSize = 0.15 * scale;
                                s.minLifeTime = 0.15; // V24.11: Increased trails
                                s.maxLifeTime = 0.45; // V24.11: Increased trails
                                s.gravity = new BABYLON.Vector3(0, 15 * intensity, 0);
                            });
                        } else {
                            systems.forEach(s => {
                                s.color1 = new BABYLON.Color4(1.0, 0.6, 0.1, 1.0); // Amber Fire 
                                s.color2 = new BABYLON.Color4(1, 0.2, 0, 0.5);
                                s.emitRate = 400 * scale;
                                s.minSize = 0.05 * scale;
                                s.maxSize = 0.2 * scale;
                                s.minLifeTime = 0.25; // V24.11: Increased trails
                                s.maxLifeTime = 0.75; // V24.11: Increased trails
                                s.gravity = new BABYLON.Vector3(0, 2 * intensity, 0);
                            });
                        }"""

content = content.replace(old_update_logic, new_update_logic)

with open(FILE_PATH, 'w') as f:
    f.write(content)

print("v24.11 patched successfully with enhanced visuals and defaults.")
