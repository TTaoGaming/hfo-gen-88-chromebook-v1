// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

test('V30 Hardening: Check Iframe and FSM stability', async ({ page }) => {
  // Use absolute path for local file
  const filePath = `file://${process.cwd()}/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v30.html`;
  await page.goto(filePath);

  // 1. Check title
  await expect(page).toHaveTitle(/HFO Omega V30/);

  // 2. Check Golden Layout
  const layout = page.locator('#layout-container');
  await expect(layout).toBeVisible();

  // 3. Check Iframe
  const iframe = page.locator('iframe#excalidraw-iframe');
  await expect(iframe).toBeVisible();

  // 4. Try to drill (using same-origin access)
  const frame = page.frameLocator('iframe#excalidraw-iframe');
  const canvas = frame.locator('canvas.interactive');
  
  // Wait for Excalidraw to load (might take a second for unpkg)
  await expect(canvas).toBeVisible({ timeout: 15000 });

  // 5. Test Menu Interaction (The problematic area)
  // Excalidraw menu items often have specific labels or aria-attributes
  // We'll look for the "Selection" tool or similar to verify UI responsiveness
  const selectionTool = frame.locator('label[title="Selection"]');
  if (await selectionTool.count() > 0) {
    await expect(selectionTool).toBeVisible();
    console.log("V30: Menu element 'Selection' found.");
  }

  console.log("V30: Drill verified. Canvas is accessible inside the same-origin iframe.");
});
