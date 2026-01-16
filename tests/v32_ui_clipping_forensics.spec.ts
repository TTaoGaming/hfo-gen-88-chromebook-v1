
import { test, expect } from '@playwright/test';

/**
 * MISSION: OMEGA V32 UI CLIPPING FORENSICS
 * GOAL: Detect if Excalidraw UI elements are clipped by the parent container due to overscan.
 */

test('Detect UI Clipping in V32', async ({ page }) => {
    await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v32.html');
    await page.waitForSelector('#layout-container');

    // 1. Ignite Omega to show Excalidraw
    await page.click('#btn-ignite');
    await page.waitForSelector('#excalidraw-iframe');

    // 2. Set Max Viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(1000); // Wait for resizes

    // 3. Check for Clipping
    const clippingForensics = await page.evaluate(() => {
        const iframe = document.getElementById('excalidraw-iframe');
        const overlay = document.getElementById('excalidraw-hero-overlay');
        const container = overlay.parentElement;

        const iRect = iframe.getBoundingClientRect();
        const cRect = container.getBoundingClientRect();

        // Coordinates of the 4 corners of the UI
        return {
            iframe: { top: iRect.top, bottom: iRect.bottom, left: iRect.left, right: iRect.right },
            container: { top: cRect.top, bottom: cRect.bottom, left: cRect.left, right: cRect.right },
            clipping: {
                top: iRect.top < cRect.top,
                bottom: iRect.bottom > cRect.bottom,
                left: iRect.left < cRect.left,
                right: iRect.right > cRect.right
            },
            delta: {
                top: cRect.top - iRect.top,
                bottom: iRect.bottom - cRect.bottom
            }
        };
    });

    console.log('Clipping Forensics:', JSON.stringify(clippingForensics, null, 2));

    expect(clippingForensics.clipping.top).toBe(true);
    expect(clippingForensics.clipping.bottom).toBe(true);

    console.log(`❌ FORENSIC CONFIRMED: Excalidraw UI is clipped by ${clippingForensics.delta.top}px at the top.`);
});
