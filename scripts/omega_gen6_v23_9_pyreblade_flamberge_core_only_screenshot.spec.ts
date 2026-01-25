// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'node:path';
import fs from 'node:fs';
import { safeGoto } from './omega_gen6_test_guards';

// Core-only visual sanity check (not a pixel-golden): render v23.9 with synthetic sword marker,
// disable fire/sheath particles + glow shell, and capture a canvas-only screenshot of the amber flamberge core.

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v23.9: pyreblade flamberge core-only (no fire/sheath) screenshot', async ({ hfoPage }) => {
    const url =
        'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_9.html'
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

    await hfoPage.evaluate(() => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');

        // Remove background noise so the blade silhouette is easy to read.
        try {
            document.documentElement.style.background = '#000';
            document.body.style.background = '#000';
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
                jl0.canvas.style.background = '#000';
                jl0.canvas.id = 'hfoBabylonCanvas';
            }
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
        pvfx.bladeAmber = 0.85;
        pvfx.bladeOpacity = 0.32;

        // Strong, unmistakable flamberge (safe-clamped per segment in v23.9 code).
        pvfx.waveAmp = 0.03;
        pvfx.waveCycles = 4.8;
        pvfx.waveSpeedHz = 0.0;
        pvfx.waveTaperIn = 0.08;
        pvfx.waveTaperOut = 0.08;

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
    });

    await hfoPage.waitForTimeout(500);

    const outDir = path.join(process.cwd(), 'test-results');
    fs.mkdirSync(outDir, { recursive: true });
    const outPath = path.join(outDir, 'omega_gen6_v23_9_pyreblade_flamberge_core_only.png');

    const canvas = hfoPage.locator('#hfoBabylonCanvas');
    await expect(canvas).toHaveCount(1);
    await canvas.screenshot({ path: outPath });

    expect(fs.existsSync(outPath)).toBe(true);
});
