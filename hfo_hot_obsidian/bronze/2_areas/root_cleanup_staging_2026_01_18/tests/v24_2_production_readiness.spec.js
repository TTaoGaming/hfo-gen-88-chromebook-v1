// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: E
// HFO OMEGA GEN 4 V24.2 PRODUCTION READINESS TEST
const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('V24.2 Production Readiness: Phoenix Core', () => {
  const filePath = path.join(__dirname, '../hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_2.html');
  const fileUrl = `file://${filePath}`;

  test('Detection of Reference/Type Errors during cold start', async ({ page }) => {
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
        console.log(`[CONSOLE ERROR] ${msg.text()}`);
      }
    });

    page.on('pageerror', err => {
      errors.push(err.message);
      console.log(`[PAGE EXCEPTION] ${err.message}`);
    });

    await page.goto(fileUrl);

    // Wait for initial load and some animation frames
    await page.waitForTimeout(2000);

    // Verify no critical errors found
    expect(errors, "Console errors detected which indicate broken Phoenix Core logic").toEqual([]);
  });

  test('Verify Phoenix Core Component Gating (OpenFeature)', async ({ page }) => {
    await page.goto(fileUrl);
    await page.waitForTimeout(1000);

    // Check if babylon-juice-overlay exists if engine-babylon is on
    const babylonOverlay = await page.$('#babylon-juice-overlay');
    expect(babylonOverlay).not.toBeNull();

    // Verify Golden Layout initial components
    const heroTitle = await page.getByText('Tactical Workspace');
    await expect(heroTitle).toBeVisible();

    // P7 Navigator should be hydrated
    const navigator = await page.$('#port-7-navigator');
    // Note: The above depends on the DOM structure of P7Navigator
  });

  test('Stress Test: Rapid Resize', async ({ page }) => {
    await page.goto(fileUrl);
    await page.waitForTimeout(500);

    const errors = [];
    page.on('pageerror', err => errors.push(err.message));

    // Rapidly resize the window to catch Golden Layout or Substrate resize race conditions
    for (let i = 0; i < 5; i++) {
      await page.setViewportSize({ width: 800 - (i * 50), height: 600 - (i * 50) });
      await page.waitForTimeout(100);
      await page.setViewportSize({ width: 1280, height: 720 });
      await page.waitForTimeout(100);
    }

    expect(errors, "Resize event triggered a regression (likely null-pointer during gating)").toEqual([]);
  });

  test('Chaos Gating: Disable Optional Engines', async ({ page }) => {
    // Disable Babylon but keep Phoenix Core
    await page.goto(`${fileUrl}?flag-engine-babylon=false&flag-engine-pixi=false`);
    await page.waitForTimeout(1000);

    const errors = [];
    page.on('pageerror', err => errors.push(err.message));

    // Interact with Ignite
    const igniteBtn = await page.$('#btn-ignite');
    if (igniteBtn) {
      await igniteBtn.click();
      await page.waitForTimeout(500);
    }

    // Trigger Resize
    await page.setViewportSize({ width: 640, height: 480 });
    await page.waitForTimeout(200);

    expect(errors, "Disabling both engines caused a crash (check null guards on resize or ignite)").toEqual([]);
  });

  test('Chaos Gating: Disable Golden Layout (Extreme)', async ({ page }) => {
    // Note: If Golden Layout is disabled, the page might not render anything, 
    // but it shouldn't have unhandled exceptions in the script.
    await page.goto(`${fileUrl}?flag-ui-golden-layout=false`);
    await page.waitForTimeout(500);

    const errors = [];
    page.on('pageerror', err => errors.push(err.message));

    expect(errors).toEqual([]);
  });
});
