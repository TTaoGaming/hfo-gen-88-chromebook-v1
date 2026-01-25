// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'node:path';
import fs from 'node:fs';
import { safeGoto } from './omega_gen6_test_guards';

// Core-only visual sanity check (not a pixel-golden): render v23.10 with synthetic sword marker,
// disable fire/sheath particles + glow shell, and capture a canvas-only screenshot of the amber flamberge core.
// Output is written into the Gen6 folder next to the HTML artifact.

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v23.10: pyreblade historical flamberge core-only PNG (Gen6 folder)', async ({ hfoPage }) => {
    const url =
        'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_10.html'
        + '?flag-disable-camera=true'
        + '&flag-ui-golden-layout=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-ui-microkernel=false'
        + '&mode=dev'
        + '&kiosk=0'
        + '&hero=0';

    await hfoPage.setViewportSize({ width: 1280, height: 720 });
    await safeGoto(hfoPage, url);
    await hfoPage.initHFO();

    await hfoPage.waitForTimeout(250);

    await hfoPage.evaluate(async () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');

        // Remove background noise so the blade silhouette is easy to read.
        try {
            document.documentElement.style.background = '#141414';
            document.body.style.background = '#141414';
            document.querySelectorAll('video').forEach(v => (v as HTMLElement).style.display = 'none');
        } catch {
            // ignore
        }

        // Ensure Babylon canvas is visible and tag it for a locator screenshot.
        try {
            w.systemState.parameters = w.systemState.parameters || {};
            w.systemState.parameters.visuals = w.systemState.parameters.visuals || {};
            w.systemState.parameters.visuals.engine = 'BABYLON';
            const jl0 = w.systemState.ui?.juiceLayers?.[0];
            if (jl0?.canvas) {
                jl0.canvas.style.display = 'block';
                jl0.canvas.style.background = '#141414';
                jl0.canvas.id = 'hfoBabylonCanvas';
            }
            if (jl0?.scene && w.BABYLON?.Color4) {
                jl0.scene.clearColor = new w.BABYLON.Color4(0.08, 0.08, 0.08, 1.0);
            }
            try { jl0?.engine?.resize?.(); } catch { }
        } catch {
            // ignore
        }

        // Force-enable sword systems.
        w.systemState.parameters.p2 = w.systemState.parameters.p2 || {};
        w.systemState.parameters.p2.swordMeter = w.systemState.parameters.p2.swordMeter || {};
        w.systemState.parameters.p2.swordMeter.enabled = true;
        w.systemState.parameters.p2.pyrebladeVfx = w.systemState.parameters.p2.pyrebladeVfx || {};
        w.systemState.parameters.p2.pyrebladeVfx.enabled = true;

        // Core-only: disable particle sheath/tip/embers and disable glow shell.
        const pvfx = w.systemState.parameters.p2.pyrebladeVfx;
        pvfx.flameIntensity = 0.0;
        pvfx.tipIntensity = 0.0;
        pvfx.emberIntensity = 0.0;
        pvfx.glowIntensity = 0.0;
        pvfx.glowAlpha = 0.0;

        // Keep the core readable but still transparent amber.
        pvfx.bladeDarkness = 0.0;
        pvfx.bladeAmber = 0.95;
        pvfx.bladeOpacity = 0.46;

        // Historical flamberge: thicker profile is in v23.10 geometry; keep waviness static.
        pvfx.waveAmp = 0.034;
        pvfx.waveCycles = 3.2;
        pvfx.waveSpeedHz = 0.0;
        pvfx.waveTaperIn = 0.10;
        pvfx.waveTaperOut = 0.10;

        // Synthetic marker endpoints in uiNorm.
        w.__hfoSwordTouch2dMarker = {
            active: true,
            locked: true,
            endpointAUiNorm: { x: 0.64, y: 0.30 },
            endpointBUiNorm: { x: 0.38, y: 0.76 },
        };

        // Synthetic meter snapshot.
        w.systemState.p2 = w.systemState.p2 || {};
        w.systemState.p2.swordMeter = { meter01: 1.0, locked: true };

        // IMPORTANT: the sword VFX is updated from BabylonJuiceSubstrate.update(cursors).
        // In disable-camera mode we may never get a cursor update tick, so we force a few ticks here.
        const jl0 = w.systemState.ui?.juiceLayers?.[0];
        if (!jl0?.update) throw new Error('missing BabylonJuiceSubstrate.update');
        if (!w.systemState.p1) w.systemState.p1 = {};
        if (!w.systemState.p1.readinessScores) w.systemState.p1.readinessScores = [1, 1];

        const raf = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
        for (let i = 0; i < 8; i++) {
            try { jl0.update([]); } catch { }
            try { jl0.scene?.render?.(); } catch { }
            await raf();
        }

        // Frame camera on the sword root if available.
        try {
            const vfx = jl0.swordVfx;
            if (vfx?.root && jl0.camera?.setTarget) {
                jl0.camera.position = new w.BABYLON.Vector3(0, 0, -6);
                jl0.camera.setTarget(vfx.root.position);
                for (let i = 0; i < 4; i++) {
                    try { jl0.update([]); } catch { }
                    try { jl0.scene?.render?.(); } catch { }
                    await raf();
                }
            }
        } catch {
            // ignore
        }
    });

    await hfoPage.waitForTimeout(500);

    const repoRoot = process.cwd();
    const outPath = path.join(
        repoRoot,
        'hfo_hot_obsidian',
        'bronze',
        '3_resources',
        'para',
        'omega_gen6_current',
        'omega_gen6_v23_10_pyreblade_flamberge_core_only.png'
    );

    const outPathAnalysis = path.join(
        repoRoot,
        'hfo_hot_obsidian',
        'bronze',
        '3_resources',
        'para',
        'omega_gen6_current',
        'omega_gen6_v23_10_pyreblade_flamberge_core_analysis.png'
    );

    fs.mkdirSync(path.dirname(outPath), { recursive: true });

    const canvas = hfoPage.locator('#hfoBabylonCanvas');
    await expect(canvas).toHaveCount(1);
    await canvas.screenshot({ path: outPath });

    // Emit a high-contrast analysis shot to judge whether the silhouette is truly flamberge.
    await hfoPage.evaluate(async () => {
        const w = window as any;
        const jl0 = w.systemState?.ui?.juiceLayers?.[0];
        const raf = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
        try {
            if (jl0?.swordVfx?.coreMat) {
                jl0.swordVfx.coreMat.wireframe = false;
                jl0.swordVfx.coreMat.alpha = 0.92;
                jl0.swordVfx.coreMat.emissiveColor = new w.BABYLON.Color3(1.8, 0.9, 0.25);
                jl0.swordVfx.coreMat.disableLighting = true;
            }
            if (jl0?.scene && w.BABYLON?.Color4) {
                jl0.scene.clearColor = new w.BABYLON.Color4(0.02, 0.02, 0.02, 1.0);
            }
            for (let i = 0; i < 6; i++) {
                try { jl0.update([]); } catch { }
                try { jl0.scene?.render?.(); } catch { }
                await raf();
            }
        } catch {
            // ignore
        }
    });
    await canvas.screenshot({ path: outPathAnalysis });

    expect(fs.existsSync(outPath)).toBe(true);
    expect(fs.existsSync(outPathAnalysis)).toBe(true);
});
