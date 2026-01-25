// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'node:path';
import fs from 'node:fs';
import { safeGoto } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 0 });

test('Gen6 v23.11: pyreblade real flamberge core (core-only + analysis PNG)', async ({ hfoPage }) => {
    const url =
        'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_11.html'
        + '?flag-disable-camera=true'
        + '&flag-ui-golden-layout=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-ui-microkernel=false'
        + '&mode=dev'
        + '&kiosk=0'
        + '&hero=0';

    await hfoPage.setViewportSize({ width: 1280, height: 720 });

    // Init script runs before any page JS executes.
    await hfoPage.addInitScript(() => {
        try {
            (window as any).__hfoInitScriptInstalled = true;
            window.addEventListener('error', (e: any) => {
                // eslint-disable-next-line no-console
                console.error('HFO_WINDOW_ERROR', e?.message, e?.filename, e?.lineno, e?.colno);
            });
            window.addEventListener('unhandledrejection', (e: any) => {
                const reason = e?.reason;
                // eslint-disable-next-line no-console
                console.error('HFO_UNHANDLED_REJECTION', reason?.message || String(reason));
            });
        } catch {
            // ignore
        }
    });

    // Diagnostics: capture the root cause of "Unexpected token <" (usually JSON parsing HTML/404).
    const recentResponses: Array<{ url: string; status: number; contentType: string }> = [];
    hfoPage.on('console', (msg) => {
        const type = msg.type();
        if (type === 'error' || type === 'warning') {
            const loc = msg.location();
            const where = loc?.url ? ` ${loc.url}:${loc.lineNumber}:${loc.columnNumber}` : '';
            // eslint-disable-next-line no-console
            console.log(`[page:${type}]${where} ${msg.text()}`);
        }
    });
    hfoPage.on('pageerror', (err) => {
        // eslint-disable-next-line no-console
        console.log(`[pageerror] ${err?.stack || err?.message || String(err)}`);
        // eslint-disable-next-line no-console
        console.log('[pageerror] recentResponses', JSON.stringify(recentResponses.slice(-25), null, 2));
    });
    hfoPage.on('requestfailed', (req) => {
        // eslint-disable-next-line no-console
        console.log(`[requestfailed] ${req.failure()?.errorText || 'unknown'} ${req.method()} ${req.url()}`);
    });
    hfoPage.on('response', async (res) => {
        const url = res.url();
        const status = res.status();
        const headers = res.headers();
        const contentType = headers['content-type'] || '';
        recentResponses.push({ url, status, contentType });
        if (recentResponses.length > 200) recentResponses.shift();

        const isMaybeMisroutedJson = url.endsWith('.json') || url.includes('manifest') || url.includes('entrypoint');
        const isHtml = contentType.includes('text/html');
        const isBad = status >= 400 || (isHtml && (isMaybeMisroutedJson || url.endsWith('.js')));
        if (!isBad) return;

        let head = '';
        try {
            head = (await res.text()).slice(0, 180).replace(/\s+/g, ' ');
        } catch {
            // ignore
        }
        // eslint-disable-next-line no-console
        console.log(`[response] ${status} ${contentType} ${url} :: ${head}`);
    });
    await safeGoto(hfoPage, url);
    await hfoPage.initHFO();

    await hfoPage.waitForTimeout(250);

    await hfoPage.evaluate(async () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');

        try {
            document.documentElement.style.background = '#141414';
            document.body.style.background = '#141414';
            document.querySelectorAll('video').forEach(v => (v as HTMLElement).style.display = 'none');
        } catch {
            // ignore
        }

        // Ensure Babylon canvas is visible.
        const jl0 = w.systemState.ui?.juiceLayers?.[0];
        if (!jl0?.canvas) throw new Error('missing babylon canvas');
        jl0.canvas.style.display = 'block';
        jl0.canvas.style.background = '#141414';
        jl0.canvas.id = 'hfoBabylonCanvas';
        if (jl0?.scene && w.BABYLON?.Color4) {
            jl0.scene.clearColor = new w.BABYLON.Color4(0.08, 0.08, 0.08, 1.0);
        }
        try { jl0?.engine?.resize?.(); } catch { }

        // Force sword systems.
        w.systemState.parameters = w.systemState.parameters || {};
        w.systemState.parameters.visuals = w.systemState.parameters.visuals || {};
        w.systemState.parameters.visuals.engine = 'BABYLON';

        w.systemState.parameters.p2 = w.systemState.parameters.p2 || {};
        w.systemState.parameters.p2.swordMeter = w.systemState.parameters.p2.swordMeter || {};
        w.systemState.parameters.p2.swordMeter.enabled = true;
        w.systemState.parameters.p2.pyrebladeVfx = w.systemState.parameters.p2.pyrebladeVfx || {};
        w.systemState.parameters.p2.pyrebladeVfx.enabled = true;

        // Core-only: kill particles + glow.
        const pvfx = w.systemState.parameters.p2.pyrebladeVfx;
        pvfx.flameIntensity = 0.0;
        pvfx.tipIntensity = 0.0;
        pvfx.emberIntensity = 0.0;
        pvfx.glowIntensity = 0.0;
        pvfx.glowAlpha = 0.0;

        // Make the core readable.
        pvfx.bladeDarkness = 0.0;
        pvfx.bladeAmber = 0.95;
        pvfx.bladeOpacity = 0.55;

        // Flamberge wave settings.
        pvfx.waveAmp = 0.038;
        pvfx.waveCycles = 3.4;
        pvfx.waveSpeedHz = 0.0;
        pvfx.waveTaperIn = 0.10;
        pvfx.waveTaperOut = 0.12;

        // Marker endpoints centered and fully charged+locked.
        w.__hfoSwordTouch2dMarker = {
            active: true,
            locked: true,
            // EndpointB is guard/hilt side (anchor). EndpointA is blade tip.
            endpointBUiNorm: { x: 0.44, y: 0.78 },
            endpointAUiNorm: { x: 0.66, y: 0.24 },
        };
        w.systemState.p2 = w.systemState.p2 || {};
        w.systemState.p2.swordMeter = { meter01: 1.0, locked: true };

        // Force a few Babylon ticks so updateSwordVfx actually runs.
        const raf = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
        for (let i = 0; i < 10; i++) {
            try { jl0.update([]); } catch { }
            try { jl0.scene?.render?.(); } catch { }
            await raf();
        }

        // Frame camera on sword if available.
        try {
            const vfx = jl0.swordVfx;
            if (vfx?.root && jl0.camera?.setTarget) {
                jl0.camera.position = new w.BABYLON.Vector3(0, 0, -6);
                jl0.camera.setTarget(vfx.root.position);
                for (let i = 0; i < 6; i++) {
                    try { jl0.update([]); } catch { }
                    try { jl0.scene?.render?.(); } catch { }
                    await raf();
                }
            }
        } catch {
            // ignore
        }
    });

    const repoRoot = process.cwd();
    const outCore = path.join(
        repoRoot,
        'hfo_hot_obsidian',
        'bronze',
        '3_resources',
        'para',
        'omega_gen6_current',
        'omega_gen6_v23_11_pyreblade_real_flamberge_core_only.png'
    );
    const outAnalysis = path.join(
        repoRoot,
        'hfo_hot_obsidian',
        'bronze',
        '3_resources',
        'para',
        'omega_gen6_current',
        'omega_gen6_v23_11_pyreblade_real_flamberge_core_analysis.png'
    );

    fs.mkdirSync(path.dirname(outCore), { recursive: true });

    const canvas = hfoPage.locator('#hfoBabylonCanvas');
    await expect(canvas).toHaveCount(1);
    await canvas.screenshot({ path: outCore });

    // High-contrast silhouette for shape judgment.
    await hfoPage.evaluate(async () => {
        const w = window as any;
        const jl0 = w.systemState?.ui?.juiceLayers?.[0];
        const raf = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
        try {
            if (jl0?.swordVfx?.coreMat) {
                jl0.swordVfx.coreMat.alpha = 0.96;
                jl0.swordVfx.coreMat.emissiveColor = new w.BABYLON.Color3(1.9, 1.0, 0.30);
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

    await canvas.screenshot({ path: outAnalysis });

    expect(fs.existsSync(outCore)).toBe(true);
    expect(fs.existsSync(outAnalysis)).toBe(true);
});
