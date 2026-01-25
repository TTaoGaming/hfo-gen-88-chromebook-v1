// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'node:path';
import fs from 'node:fs';
import { safeGoto } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 0 });

test('Gen6 v23.11: solid flamberge variants (4 labeled PNGs)', async ({ hfoPage }) => {
    const cacheBust = Date.now();
    const url =
        'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_11.html'
        + `?__cb=${cacheBust}`
        + '&flag-disable-camera=true'
        + '&flag-p2-sword-meter=true'
        + '&flag-p2-sword-vfx=true'
        + '&flag-ui-golden-layout=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-ui-microkernel=false'
        + '&mode=dev'
        + '&kiosk=0'
        + '&hero=0';

    // Smaller viewport to reduce ReadPixels/GPU stall pressure during screenshots.
    await hfoPage.setViewportSize({ width: 854, height: 480 });
    await safeGoto(hfoPage, url);
    await hfoPage.initHFO();

    // Prep: hide any non-canvas visuals.
    await hfoPage.evaluate(() => {
        const w = window as any;
        try {
            document.documentElement.style.background = '#141414';
            document.body.style.background = '#141414';
            document.querySelectorAll('video').forEach(v => (v as HTMLElement).style.display = 'none');
        } catch {
            // ignore
        }

        if (!w.systemState) throw new Error('missing systemState');
        const jl0 = w.systemState.ui?.juiceLayers?.[0];
        if (!jl0?.canvas) throw new Error('missing babylon canvas');

        // Ensure Babylon canvas is visible and wrapped.
        jl0.canvas.style.display = 'block';
        jl0.canvas.style.background = '#141414';
        jl0.canvas.id = 'hfoBabylonCanvas';

        // Install a fixed overlay badge so screenshots are self-labeled.
        let badge = document.getElementById('hfoVariantBadge') as HTMLElement | null;
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'hfoVariantBadge';
            badge.style.position = 'fixed';
            badge.style.left = '12px';
            badge.style.top = '12px';
            badge.style.padding = '6px 10px';
            badge.style.borderRadius = '10px';
            badge.style.background = 'rgba(0,0,0,0.65)';
            badge.style.color = '#FFD08A';
            badge.style.font = '600 14px system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
            badge.style.letterSpacing = '0.3px';
            badge.style.zIndex = '999999';
            document.body.appendChild(badge);
        }
        badge.textContent = 'v23.11 SOLID — preparing…';

        // Force sword systems.
        w.systemState.parameters = w.systemState.parameters || {};
        w.systemState.parameters.visuals = w.systemState.parameters.visuals || {};
        w.systemState.parameters.visuals.engine = 'BABYLON';

        w.systemState.parameters.p2 = w.systemState.parameters.p2 || {};
        w.systemState.parameters.p2.swordMeter = w.systemState.parameters.p2.swordMeter || {};
        w.systemState.parameters.p2.swordMeter.enabled = true;
        w.systemState.parameters.p2.pyrebladeVfx = w.systemState.parameters.p2.pyrebladeVfx || {};
        w.systemState.parameters.p2.pyrebladeVfx.enabled = true;

        // Core-only: kill particles + glow so silhouette is judged.
        const pvfx = w.systemState.parameters.p2.pyrebladeVfx;
        pvfx.flameIntensity = 0.0;
        pvfx.tipIntensity = 0.0;
        pvfx.emberIntensity = 0.0;
        pvfx.glowIntensity = 0.0;
        pvfx.glowAlpha = 0.0;

        // Make the core readable.
        pvfx.bladeDarkness = 0.0;
        pvfx.bladeAmber = 0.95;
        pvfx.bladeOpacity = 0.80;

        // Marker endpoints centered and fully charged+locked.
        w.__hfoSwordTouch2dMarker = {
            active: true,
            locked: true,
            endpointBUiNorm: { x: 0.44, y: 0.78 },
            endpointAUiNorm: { x: 0.66, y: 0.24 },
        };
        w.systemState.p2 = w.systemState.p2 || {};
        w.systemState.p2.swordMeter = { meter01: 1.0, locked: true };

        // Set opaque clearColor for contrast.
        if (jl0?.scene && w.BABYLON?.Color4) {
            jl0.scene.clearColor = new w.BABYLON.Color4(0.06, 0.06, 0.06, 1.0);
        }
    });

    const repoRoot = process.cwd();
    const outDir = path.join(
        repoRoot,
        'hfo_hot_obsidian',
        'bronze',
        '3_resources',
        'para',
        'omega_gen6_current'
    );
    fs.mkdirSync(outDir, { recursive: true });

    const variants: Array<{ id: 'A' | 'B' | 'C' | 'D'; label: string }> = [
        { id: 'A', label: 'v23.11 SOLID A — base-focused wave' },
        { id: 'B', label: 'v23.11 SOLID B — deep lobes' },
        { id: 'C', label: 'v23.11 SOLID C — gentle many waves' },
        { id: 'D', label: 'v23.11 SOLID D — zweihander forte' },
    ];

    const canvas = hfoPage.locator('#hfoBabylonCanvas');
    await expect(canvas).toHaveCount(1);

    for (const v of variants) {
        await hfoPage.evaluate(async ({ id, label }) => {
            const w = window as any;
            const jl0 = w.systemState?.ui?.juiceLayers?.[0];
            if (!jl0) throw new Error('missing juice layer');

            const raf = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));

            // Ensure label overlay (fixed-position so it's independent of DOM wrappers).
            const badge = document.getElementById('hfoVariantBadge') as HTMLElement | null;
            if (badge) badge.textContent = label;

            // Force-create swordVfx by ticking until updateSwordVfx runs (requires flag-p2-sword-meter/vfx).
            for (let i = 0; i < 18; i++) {
                try { jl0.update([]); } catch { }
                try { jl0.scene?.render?.(); } catch { }
                await raf();
                if (jl0.swordVfx?.setCoreMode) break;
            }

            // Switch to solid core variant.
            const vfx = jl0.swordVfx;
            if (!vfx?.setCoreMode) throw new Error('missing swordVfx.setCoreMode');
            vfx.setCoreMode('solid', id);

            // Force a few ticks after switching.
            for (let i = 0; i < 6; i++) {
                try { jl0.update([]); } catch { }
                try { jl0.scene?.render?.(); } catch { }
                await raf();
            }

            // Frame camera on sword.
            try {
                if (vfx?.root && jl0.camera?.setTarget) {
                    jl0.camera.position = new w.BABYLON.Vector3(0, 0, -6);
                    jl0.camera.setTarget(vfx.root.position);
                }
            } catch {
                // ignore
            }
            for (let i = 0; i < 4; i++) {
                try { jl0.update([]); } catch { }
                try { jl0.scene?.render?.(); } catch { }
                await raf();
            }
        }, v);

        const outPath = path.join(outDir, `omega_gen6_v23_11_solid_flamberge_variant_${v.id}.png`);
        // Canvas-only screenshot to reduce memory pressure vs full-page capture.
        await canvas.screenshot({ path: outPath, timeout: 15_000 });
        expect(fs.existsSync(outPath)).toBe(true);
    }
});
