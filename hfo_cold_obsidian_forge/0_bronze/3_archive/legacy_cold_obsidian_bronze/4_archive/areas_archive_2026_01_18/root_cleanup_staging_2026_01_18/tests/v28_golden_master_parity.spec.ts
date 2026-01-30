// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import path from 'path';

test('V28.0 Universal Projection Engine (UPE) Parity Verification', async ({ page }) => {
    const filePath = 'file://' + path.resolve('hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v28.html');
    await page.goto(filePath);

    // Give it time to initialize
    await page.waitForFunction(() => typeof systemState !== 'undefined');

    const result = await page.evaluate(() => {
        // 1. Set a controlled zoom level
        systemState.parameters.excalidraw.zoomFactor = 1.15;
        
        // 2. Force a resize to calculate viewBounds
        window.dispatchEvent(new Event('resize'));
        
        const b = systemState.ui.viewBounds;
        const normX = 0.5; // Center point
        
        // 3. Get projected coordinates from UPE
        const screenX = systemState.p1.toScreenX(normX);
        const viewportX = systemState.p1.toViewportX(normX);
        
        // 4. Calculate expected math (Manual Verification)
        const vw = systemState.p0.videoBounds.width;
        const pRect = document.getElementById('video-feed').parentElement.getBoundingClientRect();
        const expectedScreenX = (normX * b.width) + b.offsetX;
        const expectedViewportX = pRect.left + b.offsetX + (normX * b.width);
        
        return {
            zoom: systemState.parameters.excalidraw.zoomFactor,
            bounds: b,
            normX,
            screenX,
            viewportX,
            expectedScreenX,
            expectedViewportX,
            parity: {
                screen: Math.abs(screenX - expectedScreenX) < 0.1,
                viewport: Math.abs(viewportX - expectedViewportX) < 0.1
            }
        };
    });

    console.log('GOLDEN MASTER RESULTS:', JSON.stringify(result, null, 2));
    expect(result.parity.screen).toBe(true);
    expect(result.parity.viewport).toBe(true);
});
