// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

const URL =
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/app/omega_gen7_v1_excalidraw_kiosk_pointerup.html'
    + '?kiosk=1&hero=1'
    + '&flag-disable-camera=true' // keep tests stable in CI/low-RAM; launcher defaults to false for real use
    + '&flag-engine-canvas=true'
    + '&flag-engine-babylon=true'
    + '&flag-ui-excalidraw=true'
    + '&flag-p3-adapter-standard=false'
    + '&flag-p3-legacy-click=true'
    + '&mode=dev';

test('Gen7 v1 variant: Excalidraw kiosk launcher loads + iframe visible', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'domcontentloaded' });

    // Excalidraw iframe should be present when enabled.
    await expect(page.locator('#excalidraw-iframe')).toBeVisible({ timeout: 20_000 });

    // Touch2D hero canvas is a strong signal the video+touch2d stack mounted.
    await expect(page.locator('#touch2d-hero-canvas')).toBeVisible({ timeout: 20_000 });
});
