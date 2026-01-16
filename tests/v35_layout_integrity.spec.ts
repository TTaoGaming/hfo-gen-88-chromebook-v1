// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * OMEGA V35: LAYOUT INTEGRITY & SCREENSHOT HARNESS
 * Focus: Verifying Golden Layout stability and Excalidraw overlay parity.
 */

test.describe('Omega V35 Layout Integrity', () => {
    const targetUrl = 'http://localhost:8889/active_omega.html';

    test('Step 1: Verify Initial Layout & Overlay', async ({ page }) => {
        console.log('🔍 Checking V35 Initial Substrate...');
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Ensure canvas and content are present
        await expect(page.locator('#engine-canvas')).toBeVisible();
        await expect(page.locator('.lm_content')).toBeVisible({ timeout: 15000 });

        // Ensure Excalidraw is initialized (look for the iframe)
        const excalidrawIframe = page.frameLocator('iframe[src*="excalidraw"]');
        await expect(page.locator('iframe[src*="excalidraw"]')).toBeVisible();

        console.log('📸 Capturing Initial State Screenshot...');
        await page.screenshot({ path: 'test-results/v35_initial_layout.png' });
    });

    test('Step 2: Verify Maximize Resilience (The V34/V35 Fix)', async ({ page }) => {
        console.log('🔄 Testing Panel Maximization Resilience...');
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Find the "Hero" or main content panel title
        const heroPanel = page.locator('.lm_title', { hasText: 'HERO' }).first();
        await expect(heroPanel).toBeVisible();

        // Find the maximize button relative to the hero panel
        const header = page.locator('.lm_header').filter({ has: page.locator('.lm_title', { hasText: 'HERO' }) });
        const maximizeBtn = header.locator('.lm_maximise');

        console.log('🔼 Maximizing Hero Panel...');
        await maximizeBtn.click();
        
        // Wait for ResizeObserver and layout transition
        await page.waitForTimeout(1000);

        // Capture screenshot of maximized state
        await page.screenshot({ path: 'test-results/v35_maximized_layout.png' });

        // Verify that the canvas still has non-zero dimensions
        const canvasSize = await page.locator('#engine-canvas').boundingBox();
        console.log(`📏 Canvas Dimensions: ${canvasSize.width}x${canvasSize.height}`);
        expect(canvasSize.width).toBeGreaterThan(500);
        expect(canvasSize.height).toBeGreaterThan(500);
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
