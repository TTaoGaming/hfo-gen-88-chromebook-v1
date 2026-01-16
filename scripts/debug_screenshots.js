
import { chromium } from '@playwright/test';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v29_1.html');
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'v29_1_debug.png', fullPage: true });
  
  await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v30_1.html');
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'v30_1_debug.png', fullPage: true });
  
  await browser.close();
})();
