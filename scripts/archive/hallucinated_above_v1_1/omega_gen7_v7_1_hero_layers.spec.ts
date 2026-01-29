// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

function withTarget(urlStr: string, targetPath: string) {
    const url = new URL(urlStr);
    url.searchParams.set('target', targetPath);
    return url.toString();
}

test('Gen7 v7.1: GoldenLayout hero exposes 4-layer stack (P0–P3) and toggles apply visually', async ({ hfoPage }) => {
    const target =
      "/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/app/omega_gen7_v7_1.html";

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(withFlag(url, 'p3-target-active-app', 'true'));
    await hfoPage.waitForURL(/omega_gen7_v7_1\.html/i, { timeout: 20000 });

    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 20000 });

    await hfoPage.initHFO();

    // GoldenLayout root exists.
    await expect(hfoPage.locator('.lm_root').first()).toBeVisible();

    // Ensure hero is mounted (kiosk/essentials default in file).
    const out = await hfoPage.evaluate(() => {
        const q = (sel: string) => document.querySelector(sel) as HTMLElement | null;

        const video = q('[data-hfo-layer="video"]');
        const touch2d = q('[data-hfo-layer="touch2d-cursor"]');
        const babylon = q('[data-hfo-layer="babylon"]');
        const excalOverlay = q('[data-hfo-layer="excalidraw-overlay"]');

        if (!video || !touch2d || !babylon || !excalOverlay) {
            return {
                ok: false,
                found: {
                    video: !!video,
                    touch2d: !!touch2d,
                    babylon: !!babylon,
                    excalOverlay: !!excalOverlay,
                },
            };
        }

        // @ts-ignore
        const ports = window.hfoPorts;
        if (!ports?.p7?.navigate?.patchParameters) throw new Error('Missing p7.navigate.patchParameters');

        // Hide P3 excalidraw layer.
        ports.p7.navigate.patchParameters({ ui: { heroLayers: { p3ExcalidrawVisible: false } } });
        // @ts-ignore
        window.hfoHeroApplyLayers?.();

        const afterHide = {
            p3Display: excalOverlay.style.display,
            p3PointerEvents: excalOverlay.style.pointerEvents,
        };

        // Show again.
        ports.p7.navigate.patchParameters({ ui: { heroLayers: { p3ExcalidrawVisible: true } } });
        // @ts-ignore
        window.hfoHeroApplyLayers?.();

        const afterShow = {
            p3Display: excalOverlay.style.display,
            p3PointerEvents: excalOverlay.style.pointerEvents,
        };

        return {
            ok: true,
            found: {
                video: !!video,
                touch2d: !!touch2d,
                babylon: !!babylon,
                excalOverlay: !!excalOverlay,
            },
            afterHide,
            afterShow,
        };
    });

    if (!out.ok) {
        throw new Error(`Missing hero layers: ${JSON.stringify(out.found)}`);
    }

    expect(out.found.video).toBe(true);
    expect(out.found.touch2d).toBe(true);
    expect(out.found.babylon).toBe(true);
    expect(out.found.excalOverlay).toBe(true);

    expect(out.afterHide.p3Display).toBe('none');
    expect(out.afterHide.p3PointerEvents).toBe('none');

    expect(out.afterShow.p3Display).toBe('block');
    expect(out.afterShow.p3PointerEvents).toBe('auto');
});
