// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * OMEGA V35: LAYOUT INTEGRITY & SCREENSHOT HARNESS
 * Focus: Verifying Golden Layout stability and Excalidraw overlay parity.
 */

test.describe('Omega V35 Layout Integrity', () => {
    const targetUrl = 'http://127.0.0.1:8889/active_omega.html';

    test('Step 1: Verify Initial Layout & Overlay', async ({ page }) => {
        console.log('🔍 Checking V35 Initial Substrate...');
        await page.goto(targetUrl, { waitUntil: 'load' });

        // Ensure canvas and content are present
        await expect(page.locator('#overlay-canvas')).toBeVisible({ timeout: 15000 });

        console.log('🔥 Igniting Omega Substrate...');
        const igniteBtn = page.locator('#btn-ignite');
        await expect(igniteBtn).toBeVisible();
        await igniteBtn.click();

        // Ensure Excalidraw becomes visible
        const excalidrawOverlay = page.locator('#excalidraw-hero-overlay');
        await expect(excalidrawOverlay).toBeVisible({ timeout: 10000 });

        // Ensure Excalidraw is initialized (look for the iframe)
        const excalidrawIframe = page.frameLocator('#excalidraw-iframe');
        await expect(page.locator('#excalidraw-iframe')).toBeVisible();

        console.log('📸 Capturing Initial State Screenshot...');
        await page.screenshot({ path: 'test-results/v35_initial_layout.png' });
    });

    test('Step 2: Verify Maximize Resilience (The V34/V35 Fix)', async ({ page }) => {
        console.log('🔄 Testing Panel Maximization Resilience...');
        await page.goto(targetUrl, { waitUntil: 'load' });

        console.log('🔥 Igniting Omega Substrate for Maximize Test...');
        await page.locator('#btn-ignite').click();

        // Find the "Tactical Workspace" or main content panel title
        const heroPanel = page.locator('.lm_title', { hasText: 'Tactical Workspace' }).first();
        await expect(heroPanel).toBeVisible({ timeout: 15000 });

        // Find the maximize button relative to the Tactical Workspace panel
        const header = page.locator('.lm_header').filter({ has: page.locator('.lm_title', { hasText: 'Tactical Workspace' }) });
        const maximizeBtn = header.locator('.lm_maximise');

        console.log('🔼 Maximizing Tactical Workspace Panel...');
        await maximizeBtn.click();

        // Wait for ResizeObserver and layout transition settlement
        await page.waitForTimeout(2000);

        // Capture screenshot of maximized state
        await page.screenshot({ path: 'test-results/v35_maximized_layout.png', fullPage: true });

        // Verify that the canvas and iframe have non-zero dimensions
        const canvas = page.locator('#overlay-canvas');
        const iframe = page.locator('#excalidraw-iframe');

        const canvasSize = await canvas.boundingBox();
        const iframeSize = await iframe.boundingBox();
        const containerSize = await page.locator('.lm_content').first().boundingBox();

        if (canvasSize && iframeSize && containerSize) {
            console.log(`📏 Canvas Dimensions: ${canvasSize.width}x${canvasSize.height}`);
            console.log(`📏 Iframe Dimensions: ${iframeSize.width}x${iframeSize.height}`);
            console.log(`📏 Container Dimensions: ${containerSize.width}x${containerSize.height}`);

            // Forensic Discovery: Check for Clipping (Overflow)
            if (iframeSize.width > containerSize.width || iframeSize.height > containerSize.height) {
                console.log('🚨 DETECTED CLIPPING: Iframe is larger than its Golden Layout container!');
            }

            expect(canvasSize.width).toBeGreaterThan(100);
            expect(iframeSize.width).toBeGreaterThan(100);
        }
    });

    test('Step 3: Screenshot Golden Master Parity (Manual Comparison)', async ({ page }) => {
        // This test captures a screenshot for manual confirmation vs Golden Master
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Trigger a specific state (e.g. SENSE/🖐️) via evaluating window state if possible
        // or just capture the idle state.
        await page.screenshot({ path: 'test-results/v35_golden_parity_check.png' });
        console.log('✅ Screenshot captured for manual Golden Master audit.');
    });
});
