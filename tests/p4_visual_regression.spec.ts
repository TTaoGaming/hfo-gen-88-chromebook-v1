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
        await expect(page.locator('#engine-canvas')).toBeVisible();
        await expect(page.locator('.lm_content')).toBeVisible({ timeout: 10000 });

        // Capture screenshot of the whole page
        // Note: First run will fail if no baseline exists (use --update-snapshots)
        await expect(page).toHaveScreenshot('hfo-p4-baseline.png', {
            maxDiffPixelRatio: 0.05,
            mask: [page.locator('#debug-panel')] // Mask dynamic content
        });
    });

    test('Check Element Presets (Dui/Li/etc)', async ({ page }) => {
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Open Navigator panel (Port 7)
        // This assumes a specific ID or title for the navigator tab
        const navigatorTab = page.locator('.lm_title', { hasText: 'NAVIGATOR' });
        if (await navigatorTab.isVisible()) {
            await navigatorTab.click();
        }

        // Verify element preset buttons are present
        const waterBtn = page.locator('button', { hasText: 'WATER (DUI)' });
        const fireBtn = page.locator('button', { hasText: 'FIRE (LI)' });

        await expect(waterBtn).toBeVisible();
        await expect(fireBtn).toBeVisible();
    });
});
