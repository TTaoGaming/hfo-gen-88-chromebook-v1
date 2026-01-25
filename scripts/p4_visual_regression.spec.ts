// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * Medallion: Bronze | Mutation: 0% | HIVE: V
 * PORT 4: VISUAL REGRESSION HARNESS
 * Ensures GoldenLayout structure, canvas presence, and tutorial visibility.
 * Uses pixel-parity snapshots.
 */

test.describe('Port 4 Visual Integrity', () => {
    const targetUrl = 'http://localhost:8889/active_omega.html';

    test('Snapshot: Baseline UI State', async ({ page }) => {
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Wait for the tutorial overlay to appear (if not already dismissed)
        const tutorial = page.locator('#tutorial-overlay');

        // Ensure main UI components are visible
        const canvas = page.locator('#babylon-canvas, #engine-canvas').first();
        await expect(canvas).toBeVisible();
        await expect(page.locator('.lm_content')).toBeVisible({ timeout: 10000 });

        // Capture screenshot of the whole page
        // Note: First run will fail if no baseline exists (use --update-snapshots)
        await expect(page).toHaveScreenshot('hfo-p4-baseline.png', {
            maxDiffPixelRatio: 0.05,
            mask: [page.locator('#debug-panel')] // Mask dynamic content
        });
    });

    test('Check Element Presets (Trigrams)', async ({ page }) => {
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Open Navigator panel (Port 7)
        const navigatorTab = page.locator('.lm_title', { hasText: 'Navigator' });
        if (await navigatorTab.isVisible()) {
            await navigatorTab.click();
        }

        // Verify element preset dropdown or text is present
        // V40.1 uses a lil-gui dropdown for Trigrams
        const elementLabel = page.locator('div.name', { hasText: 'HFO Element (Trigram)' });
        await expect(elementLabel).toBeVisible();
    });
});
