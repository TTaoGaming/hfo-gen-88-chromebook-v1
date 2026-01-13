// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

test('Omega Gen 4: Monolith Load & Init', async ({ hfoPage }) => {
  const url = getActiveUrl();
  console.log(`Testing URL: ${url}`);
  await hfoPage.goto(url);

  // Check for M3 Status Bar
  const statusBar = hfoPage.locator('#status-bar');
  await expect(statusBar).toContainText('[HFO OMEGA GEN 4]');

  // Check for the Initialize button
  const startBtn = hfoPage.locator('#btn-start-p0');
  await expect(startBtn).toBeVisible();

  // Click Initialize
  await startBtn.click();

  // Wait for recognizer to be initialized (logged in mission logs)
  const logs = hfoPage.locator('#mission-logs-content');
  await expect(logs).toContainText('✅ P0: MediaPipe Shard Online', { timeout: 15000 });

  console.log("Omega Gen 4: P0 Initialization Successful.");
});

test('Omega Gen 4: Layout Integrity', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  // Verify Golden Layout initialized
  const glRoot = hfoPage.locator('.lm_root');
  await expect(glRoot).toBeVisible();

  // Verify Hero component
  const hero = hfoPage.locator('.hero-view-container');
  await expect(hero).toBeVisible();

  // Verify Command Manifold (lil-gui)
  const gui = hfoPage.locator('.lil-gui');
  await expect(gui).toBeVisible();
});
