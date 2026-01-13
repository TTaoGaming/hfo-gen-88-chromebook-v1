// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import config from './hfo_config.json';

test.describe('HFO Omega Gen 4 V8: Rigid Rod E2E', () => {

    test('V8: System Ignition and State Transparency', async ({ page }) => {
        const url = `${config.baseUrl}${config.activeVersion}${config.suffix}`;
        await page.goto(url);

        // 1. Initial State
        await expect(page.locator('#state-indicator')).toContainText('IDLE');

        // 2. Ignite Cluster
        const igniteBtn = page.locator('#btn-ignite');
        await expect(igniteBtn).toBeVisible();
        await igniteBtn.click();
        await expect(igniteBtn).not.toBeVisible();

        // 3. Check State Transparency (window.hfoState)
        const hfoState = await page.evaluate(() => (window as any).hfoState);
        expect(hfoState).toBeDefined();
        expect(hfoState.parameters).toBeDefined();
        expect(hfoState.fsm.currentState).toBe('IDLE');
    });

    test('V8: Navigator Configuration Sync', async ({ page }) => {
        const url = `${config.baseUrl}${config.activeVersion}${config.suffix}`;
        await page.goto(url);
        await page.locator('#btn-ignite').click();

        // Open Navigator
        const navTitle = page.getByRole('button', { name: /NAVIGATOR CONFIG/ });
        await expect(navTitle).toBeVisible();

        // Toggle Laser Beam Path
        const beamCheckbox = page.getByLabel('Show Beam Path');
        await expect(beamCheckbox).toBeVisible();
        await beamCheckbox.check();

        // Verify parameter sync in window.hfoState
        const showBeam = await page.evaluate(() => (window as any).hfoState.parameters.physics.showLaserBeam);
        expect(showBeam).toBe(true);
    });

    test('V8: FSM Panel Integrity', async ({ page }) => {
        const url = `${config.baseUrl}${config.activeVersion}${config.suffix}`;
        await page.goto(url);
        await page.locator('#btn-ignite').click();

        const fsmCanvas = page.locator('#fsm-visualizer');
        await expect(fsmCanvas).toBeVisible();

        // Check if canvas has dimensions
        const box = await fsmCanvas.boundingBox();
        expect(box?.width).toBeGreaterThan(0);
        expect(box?.height).toBeGreaterThan(0);
    });
});
