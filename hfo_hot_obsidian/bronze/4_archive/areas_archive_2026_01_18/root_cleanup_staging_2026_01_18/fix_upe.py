# Medallion: Bronze | Mutation: 0% | HIVE: V

import os

filepath = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v28_1.html"

with open(filepath, 'r') as f:
    lines = f.readlines()

# We want to replace the p1 block with a clean one.
# p1 starts around line 603 and ends at 644 in the messed up version.

start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if "p1: {" in line and i > 500:
        start_line = i
    if "ui: {" in line and i > 600:
        end_line = i
        break

if start_line != -1 and end_line != -1:
    new_p1_block = [
        "            p1: {\n",
        "                cursors: [],\n",
        "                readinessScores: [0, 0, 0, 0], // Per-hand leaky buckets\n",
        "                fsmStates: ['IDLE', 'IDLE', 'IDLE', 'IDLE'], // Per-hand FSM states [V15]\n",
        "                palmFacingStates: [false, false, false, false], // Hysteresis state\n",
        "                lastPalmFacingTimes: [0, 0, 0, 0], // Tension/Coyote timers\n",
        "                lastData: [null, null, null, null], // Per-hand coasting data\n",
        "                lastTrackingTimes: [0, 0, 0, 0], // V26: Tracking heartbeats\n",
        "                lastMovementTimes: [0, 0, 0, 0], // V26: Inactivity detection\n",
        "                lastLandmarks: [null, null, null, null], // V26: Ghost landmarks for fading\n",
        "                coastStartTimes: [0, 0, 0, 0], // Per-hand coast timers\n",
        "                filters: [null, null, null, null], // OneEuroFilters\n",
        "                rodFilters: [null, null, null, null], // V19.2: Stabilize rod length\n",
        "                anchorFilters: [null, null, null, null], // V19.2: Stabilize anchor point\n",
        "                directionFilters: [null, null, null, null], // V19.2: Stabilize rod direction\n",
        "                physicsState: [null, null, null, null], // Mass-Spring state\n",
        "\n",
        "                // 🎯 V28.1 UNIVERSAL PROJECTION ENGINE (UPE)\n",
        "                // Centralized parity logic for all coordinate substrates\n",
        "                toBufferX: (nx) => nx * (systemState.p0.canvas?.width || 1280),\n",
        "                toBufferY: (ny) => ny * (systemState.p0.canvas?.height || 720),\n",
        "                \n",
        "                toScreenX: (nx) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    return (nx * b.drawW) + b.offsetX;\n",
        "                },\n",
        "                toScreenY: (ny) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    return (ny * b.drawH) + b.offsetY;\n",
        "                },\n",
        "\n",
        "                toViewportX: (nx) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    const r = systemState.p0.video?.parentElement?.getBoundingClientRect() || { left: 0 };\n",
        "                    const zoom = b.zoom || 1.15;\n",
        "                    const margin = (1.0 - (1.0 / zoom)) / 2;\n",
        "                    const ui_nx = (nx - margin) / (1.0 - 2 * margin);\n",
        "                    return r.left + b.uiOffsetX + (ui_nx * b.uiW);\n",
        "                },\n",
        "                toViewportY: (ny) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    const r = systemState.p0.video?.parentElement?.getBoundingClientRect() || { top: 0 };\n",
        "                    const zoom = b.zoom || 1.15;\n",
        "                    const margin = (1.0 - (1.0 / zoom)) / 2;\n",
        "                    const ui_ny = (ny - margin) / (1.0 - 2 * margin);\n",
        "                    return r.top + b.uiOffsetY + (ui_ny * b.uiH);\n",
        "                },\n",
        "                toUiNormX: (nx) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    const zoom = b.zoom || 1.15;\n",
        "                    const margin = (1.0 - (1.0 / zoom)) / 2;\n",
        "                    return (nx - margin) / (1.0 - 2 * margin);\n",
        "                },\n",
        "                toUiNormY: (ny) => {\n",
        "                    const b = systemState.ui.viewBounds;\n",
        "                    const zoom = b.zoom || 1.15;\n",
        "                    const margin = (1.0 - (1.0 / zoom)) / 2;\n",
        "                    return (ny - margin) / (1.0 - 2 * margin);\n",
        "                }\n",
        "            },\n"
    ]
    
    # Check if there is a '};' between the last toViewportY and ui:
    # In the cat -e output:
    #                 return r.top + b.uiOffsetY + (ui_
    # ny * b.uiH);$                                                }$
    #         };$
    #             ui: {$
    
    # So the closing brace for p1 is there, then a '};' which closes systemState?
    # No, systemState starts with 'const systemState = {'.
    # p1 is a property of systemState.
    # The '};' is probably closing p1 or something else.
    
    # Let's adjust end_line to include that '};' if it's there.
    
    lines[start_line:end_line] = new_p1_block

    with open(filepath, 'w') as f:
        f.writelines(lines)
    print("Cleaned p1 block.")
else:
    print(f"Could not find start ({start_line}) or end ({end_line})")
