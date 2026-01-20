// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true&flag-ui-excalidraw=true';

test('Gen5 excalidraw wrapper: ready signal + canvas present', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    await hfoPage.evaluate(() => {
        // @ts-ignore
        if (window.hfoState?.parameters?.excalidraw) {
            // @ts-ignore
            window.hfoState.parameters.excalidraw.enabled = true;
        }
        // @ts-ignore
        if (window.hfoState?.ui?.excalidrawOverlay) {
            // @ts-ignore
            window.hfoState.ui.excalidrawOverlay.style.display = 'block';
        }
    });

    await expect(hfoPage.locator('#excalidraw-iframe')).toBeVisible({ timeout: 20000 });


    const frame = hfoPage.frameLocator('#excalidraw-iframe');
    const canvases = frame.locator('canvas.excalidraw__canvas');
    await expect(canvases).toHaveCount(2, { timeout: 20000 });
    await expect(canvases.nth(1)).toBeVisible({ timeout: 20000 });

    const apiReady = await frame.locator('body').evaluate(() => {
        // @ts-ignore
        return !!window.excalidrawAPI;
    });
    expect(apiReady).toBe(true);
});
