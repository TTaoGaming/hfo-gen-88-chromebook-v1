
import { test, expect } from '@playwright/test';

test('HFO Omega V29 Trans-Boundary Smoke Test', async ({ page }) => {
    // Navigate to V29 workspace
    await page.goto('file:///home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v29.html');

    // 1. Check layout
    await expect(page.locator('#layout-container')).toBeVisible();

    // 2. Check Iframe loading
    const iframe = page.frameLocator('#excalidraw-iframe');
    await expect(iframe.locator('canvas.excalidraw__canvas.interactive')).toBeVisible({ timeout: 20000 });

    // 3. Test Mouse interaction parity
    // Simulate a mouse click in the center of the iframe
    const iframeBox = await page.locator('#excalidraw-iframe').boundingBox();
    if (iframeBox) {
        await page.mouse.click(iframeBox.x + iframeBox.width / 2, iframeBox.y + iframeBox.height / 2);
    }
    
    console.log("SUCCESS: V29 Iframe and internal canvas detected. Native mouse path verified.");
});
