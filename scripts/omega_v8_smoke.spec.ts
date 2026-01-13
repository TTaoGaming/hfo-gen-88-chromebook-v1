// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

test('Omega Gen 4 V8: Monolith Load & Init', async ({ hfoPage }) => {
    const url = getActiveUrl();
    console.log(`Testing URL: ${url}`);
    await hfoPage.goto(url);

    // Check for Status Bar
    const statusBar = hfoPage.locator('#status-bar');
    await expect(statusBar).toContainText('[HFO OMEGA V8.0]');

    // Check for the Ignite button
    const igniteBtn = hfoPage.locator('#btn-ignite');
    await expect(igniteBtn).toBeVisible();

    // Click Ignite
    await igniteBtn.click();

    // Wait for recognizer to be initialized
    const logs = hfoPage.locator('#mission-logs');
    await expect(logs).toContainText('✅ P0: Sensing Cluster Online', { timeout: 30000 });

    console.log("Omega Gen 4 V8: P0 Initialization Successful.");
});

test('Omega Gen 4 V8: Layout Integrity', async ({ hfoPage }) => {
    const url = getActiveUrl();
    await hfoPage.goto(url);

    // Verify Golden Layout initialized
    const glRoot = hfoPage.locator('.lm_root');
    await expect(glRoot).toBeVisible();

    // Verify Hero component
    const hero = hfoPage.locator('.hero-view-container');
    await expect(hero).toBeVisible();

    // Verify Navigator (lil-gui)
    const gui = hfoPage.locator('.lil-gui.root');
    await expect(gui).toBeVisible();
});
