# Medallion: Bronze | Mutation: 0% | HIVE: V
# Medallion: Bronze | Mutation: 0% | HIVE: I
import os

FILE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_10.html"

with open(FILE_PATH, 'r') as f:
    content = f.read()

# 1. Update update(cursors) logic in BabylonJuiceSubstrate
old_logic = """                        // State based visuals (V24.7: PHX CORE SCALING)
                        if (c.fsmState === 'COMMIT' || c.fsmState === 'COAST') {
                            systems.forEach(s => {
                                s.minSize = 0.4; s.maxSize = 1.0; // Larger for Commit
                                if (s.name === "fire") {
                                    s.emitRate = 1500;
                                    s.color1 = new BABYLON.Color4(1, 0.2, 0, 1.0);
                                }
                            });
                        } else {
                            systems.forEach(s => {
                                s.minSize = 0.1; s.maxSize = 0.4; // Smaller for Ready
                                if (s.name === "fire") {
                                    s.emitRate = 500;
                                    s.color1 = new BABYLON.Color4(1, 0.6, 0.2, 1.0);
                                }
                            });
                        }"""

new_logic = """                        // V24.10: Plasma Needle Scion (Fire Lab V3 Aesthetics)
                        const scale = window.hfoState.parameters.physics.fireScale || 1.0;
                        const intensity = window.hfoState.parameters.physics.fireIntensity || 1.0;

                        if (c.fsmState === 'COMMIT' || c.fsmState === 'COAST') {
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

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    print("Babylon update logic patched.")
else:
    print("Could not find Babylon update logic.")

# 2. Update createEffect defaults to match V3
old_defaults = """                fire.color1 = new BABYLON.Color4(1, 0.6, 0.2, 1.0);
                fire.color2 = new BABYLON.Color4(1, 0.2, 0, 1.0);
                fire.colorDead = new BABYLON.Color4(0.2, 0, 0, 0.0);
                fire.minLifeTime = 0.05; fire.maxLifeTime = 0.15;
                fire.emitRate = 1200;
                fire.blendMode = BABYLON.ParticleSystem.BLENDMODE_ONEONE;
                fire.gravity = new BABYLON.Vector3(0, 40, 0);"""

new_defaults = """                fire.color1 = new BABYLON.Color4(1.0, 0.6, 0.1, 1.0);
                fire.color2 = new BABYLON.Color4(1, 0.2, 0, 0.5);
                fire.colorDead = new BABYLON.Color4(0, 0, 0, 0);
                fire.minLifeTime = 0.1; fire.maxLifeTime = 0.3;
                fire.emitRate = 400;
                fire.blendMode = BABYLON.ParticleSystem.BLENDMODE_ONEONE;
                fire.gravity = new BABYLON.Vector3(0, 2, 0);"""

if old_defaults in content:
    content = content.replace(old_defaults, new_defaults)
    print("Babylon defaults patched.")
else:
    print("Could not find Babylon defaults.")

with open(FILE_PATH, 'w') as f:
    f.write(content)
