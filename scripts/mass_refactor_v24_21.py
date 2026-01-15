import os
import re

def refactor_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Bulk string replacements
    replacements = {
        'Math.sin(time / 500)': 'Math.sin(time / cur.bubbleOrbitSpeed)',
        'Date.now() / 1000': 'Date.now() / systemState.parameters.constants.msPerSec',
        'for (let i = 0; i <= 10; i++)': 'for (let i = 0; i <= cur.gridSteps; i++)',
        'rgba(255, 255, 255, 0.05)': '`rgba(255, 255, 255, ${cur.gridAlpha})`',
        "color: 'rgba(255, 255, 255, 0.15)', lineWidth: 1.2": "color: `rgba(255, 255, 255, ${cur.skeletonConnectorAlpha})`, lineWidth: cur.skeletonLineWidth",
        "color: 'rgba(255, 255, 255, 0.2)', radius: 1": "color: `rgba(255, 255, 255, ${cur.skeletonLandmarkAlpha})`, radius: cur.skeletonRadius",
        "ctx.globalAlpha = 0.4;": "ctx.globalAlpha = cur.whiteCoreAlpha;",
        "time / 500": "time / cur.glowTimeDivisor",
        "ctx.globalAlpha = 0.6;": "ctx.globalAlpha = cur.skeletonAlphaReady;",
        "ctx.globalAlpha = 0.3;": "ctx.globalAlpha = cur.depthRingAlpha;",
        "globalAlpha = 0.3": "globalAlpha = cur.depthRingAlpha",
        "split('x')[0]) || 1280": "split('x')[0]) || systemState.parameters.camera.resolutionWidth",
        "split('x')[1]) || 720": "split('x')[1]) || systemState.parameters.camera.resolutionHeight",
        "anchor.set(0.5, 0.85)": "anchor.set(cur.anchorX, cur.anchorY)",
        "Math.random() > 0.7": "Math.random() > cur.randomThreshold",
        "rgba(0, 255, 65, 0.05)": "`rgba(0, 255, 65, ${cur.panelAlpha})`",
        "rgba(255, 65, 54, 0.05)": "`rgba(255, 65, 54, ${cur.panelAlpha})`",
        "Math.random() * 50": "Math.random() * cur.glowColorOffset",
        "arc(sx, sy, 1.5": "arc(sx, sy, cur.skeletonRadius * cur.arcSizeCommitFactor",
        "length > 88": "length > cur.historyLimit",
        "nz > 0.88": "nz > cur.goldilocksThreshold",
        "dotX - 10": "dotX - cur.crosshairSize",
        "setLineDash([2, 4])": "setLineDash([cur.dashLength, cur.dashGap])",
        "globalAlpha = 0.1": "globalAlpha = cur.skeletonAlphaCoast",
        "const gageW = 8": "const gageW = cur.gageWidth",
        "const gageH = 80": "const gageH = cur.gageHeight",
        "radius + 15": "radius + cur.gageOffset",
        "gageX - 5": "gageX - cur.sparklinePadding / 2",
        "gageW + 10": "gageW + cur.sparklinePadding",
        "radius = 40": "radius = cur.radiusBase",
        "shadowBlur = c.isPalmFacing ? 15 : 0": "shadowBlur = c.isPalmFacing ? cur.shadowBlurPalm : 0",
        "const buckW = 12": "const buckW = cur.bucketWidth",
        "const buckH = 80": "const buckH = cur.bucketHeight",
        "radius - 27": "radius - cur.bucketOffset",
        "gageW + 5": "gageW + cur.uiLineOffset",
        "gageX - 8": "gageX - cur.uiIndicatorOffset",
        "gageW + 8": "gageW + cur.uiIndicatorOffset",
        "1 - 0.88": "1 - cur.goldilocksThreshold",
        "buckH / 2": "cur.bucketHeight / 2",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Regex and Logic fixes
    content = re.sub(r"\.addColorStop\(0\.3,", r".addColorStop(cur.gradStopMid,", content)
    content = re.sub(r"\.addColorStop\(0\.4,", r".addColorStop(cur.gradStopAlt,", content)
    content = re.sub(r"\.addColorStop\(0\.5,", r".addColorStop(cur.gradStopB,", content)
    content = re.sub(r"\.addColorStop\(0\.7,", r".addColorStop(cur.gradStopC,", content)
    content = content.replace("fsmState === 'COMMIT' ? 0.9 : 0.6", "fsmState === 'COMMIT' ? cur.skeletonAlphaCommit : cur.skeletonAlphaReady")
    content = content.replace("* 3", "* cur.skeletonRadiusMultiplier")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    target_file = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_21.html'
    refactor_html(target_file)
    print(f'Refactor complete on {target_file}')
