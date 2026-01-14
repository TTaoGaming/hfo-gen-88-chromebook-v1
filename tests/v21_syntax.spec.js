// Medallion: Bronze | Mutation: 0% | HIVE: E
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

test.describe('HFO Omega Gen 4 V21 Syntax & Runtime Check', () => {
  test('should load without console errors and log pixi status', async ({ page }) => {
    const errors = [];
    const logs = [];
    page.on('console', msg => {
      const text = msg.text();
      logs.push(`[${msg.type()}] ${text}`);
      if (msg.type() === 'error') {
        errors.push(text);
        console.log(`PAGE ERROR: ${text}`);
      }
    });

    page.on('pageerror', err => {
      errors.push(err.message);
      console.log(`PAGE EXCEPTION: ${err.message}`);
    });

    const filePath = path.join(__dirname, '../hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v21.html');
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl);

    // Give it more time to run modules and initialize shaders
    await page.waitForTimeout(3000);

    console.log("--- BROWSER LOGS ---");
    logs.forEach(l => console.log(l));
    console.log("--- END BROWSER LOGS ---");

    expect(errors).toEqual([]);
  });
});
