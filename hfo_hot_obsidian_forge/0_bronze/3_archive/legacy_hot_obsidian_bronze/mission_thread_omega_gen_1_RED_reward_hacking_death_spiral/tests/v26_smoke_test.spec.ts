// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import path from 'path';

test('V26 Tool Onboarding Smoke Test', async ({ page }) => {
    const filePath = `file://${path.resolve('hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v26.html')}`;
    await page.goto(filePath);

    // Check for Golden Layout components
    await expect(page.locator('.lm_title:has-text("OMEGA: EXCALIDRAW")')).toBeVisible();
    await expect(page.locator('.lm_title:has-text("OMEGA: PIANO GENIE")')).toBeVisible();

    // Check iframes
    const excalidraw = page.frameLocator('#excalidraw-iframe');
    const pianoGenie = page.frameLocator('#piano-genie-iframe');

    // Verify iframes exist (even if তারা load slow)
    await expect(page.locator('#excalidraw-iframe')).toBeAttached();
    await expect(page.locator('#piano-genie-iframe')).toBeAttached();

    console.log('V26 Smoke Test: Golden Layout and Iframes verified.');
});
