// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

/**
 * V41 Standard E2E: Verify that modern tools (Excalidraw) work with PURE PointerEvents.
 */
test('V41 Standard E2E: PointerEvent-only Interaction on Excalidraw', async ({ hfoPage }) => {
    // 1. Load the V41 workspace
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v40.html';
    await hfoPage.goto(url);
    await hfoPage.initHFO();
    await hfoPage.waitForHand(0);

    // Wait for Excalidraw
    const frame = hfoPage.frameLocator('iframe#excalidraw-iframe');
    const canvas = frame.locator('canvas.interactive');
    await expect(canvas).toBeVisible({ timeout: 20000 });

    // 2. Locate the Rectangle tool
    const rectTool = frame.locator('label[title*="Rectangle"]');
    await expect(rectTool).toBeVisible();

    // Get positions
    const iframeEl = hfoPage.locator('iframe#excalidraw-iframe');
    const iframeBox = await iframeEl.boundingBox();
    const box = await rectTool.boundingBox();
    if (!box || !iframeBox) throw new Error("Could not find box for Rectangle tool or iframe");

    const targetX = (box.x + box.width / 2 - iframeBox.x) / iframeBox.width;
    const targetY = (box.y + box.height / 2 - iframeBox.y) / iframeBox.height;

    // 3. Inject State using Hand 0 (Primary)
    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoState.physics.p3Mirror = false;
    });

    await hfoPage.injectHand(0, {
        active: true,
        state: 'COMMITTED',
        event: 'pointerdown',
        cursors: { predictive: { x: targetX, y: targetY } }
    });

    // Release
    await hfoPage.injectHand(0, {
        state: 'IDLE',
        event: 'pointerup'
    });

    // 4. Verification: Wait for state change
    await hfoPage.waitForTimeout(500);
    const isSelected = await rectTool.evaluate((el) => {
        const input = el.querySelector('input');
        return input ? input.checked : el.classList.contains('active');
    });

    console.log(`V41 E2E: Rectangle tool selected with Pure PointerEvents? ${isSelected}`);
    expect(isSelected).toBe(true);
});
