// Medallion: Bronze | Mutation: 0% | HIVE: V

import { test, expect } from '@playwright/test';

/**
 * MISSION: OMEGA V32 SUBSTRATE EMPIRICISM
 * GOAL: Verify the "Shared Data Substrate" is real and reactive to layout changes.
 * Medallion: Bronze | Mutation: 0% | HIVE: V
 */

test('Verify V32 Shared Data Substrate Reactivity', async ({ page }) => {
    // 1. Load V32
    await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v32.html');

    // 2. Wait for GL to initialize
    await page.waitForSelector('#layout-container');

    // 3. Capture Initial Substrate State
    const initialBounds = await page.evaluate(() => {
        return JSON.parse(JSON.stringify(window.hfoState.ui.viewBounds));
    });

    console.log('Initial Bounds:', initialBounds);

    // 4. Trigger Fullscreen Logic (Simulate GL Maximization)
    // We'll manually resize the window or resize the layout container to trigger ResizeObserver
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Wait for ResizeObserver + setTimeout (150ms in code)
    await page.waitForTimeout(500);

    const maximizedBounds = await page.evaluate(() => {
        return JSON.parse(JSON.stringify(window.hfoState.ui.viewBounds));
    });

    console.log('Maximized Bounds:', maximizedBounds);

    // 5. Verification 1: Substrate Reactivity
    // Checking if bounds changed after viewport resize
    expect(maximizedBounds.width).not.toBe(initialBounds.width);
    expect(maximizedBounds.height).not.toBe(initialBounds.height);

    // 6. Verification 2: Projection Parity
    // Test if a normalized center (0.5, 0.5) projects to the absolute center of the video element
    const projectionCheck = await page.evaluate(() => {
        const video = document.getElementById('video-feed');
        if (!video) return { error: 'No video element' };

        const vRect = video.getBoundingClientRect();
        const absoluteCenterX = vRect.left + vRect.width / 2;
        const absoluteCenterY = vRect.top + vRect.height / 2;

        const substrateCenterX = window.hfoState.p1.toViewportX(0.5);
        const substrateCenterY = window.hfoState.p1.toViewportY(0.5);

        return {
            absolute: { x: absoluteCenterX, y: absoluteCenterY },
            substrate: { x: substrateCenterX, y: substrateCenterY },
            delta: {
                x: Math.abs(absoluteCenterX - substrateCenterX),
                y: Math.abs(absoluteCenterY - substrateCenterY)
            }
        };
    });

    console.log('Projection Check:', projectionCheck);

    // Threshold: 1px drift is acceptable for rounding, but significant delta means theater/failure.
    expect(projectionCheck.delta.x).toBeLessThan(1.5);
    expect(projectionCheck.delta.y).toBeLessThan(1.5);

    console.log('✅ SUBSTRATE EMPIRICISM VERIFIED: Substrate matches Physical Reality.');
});
