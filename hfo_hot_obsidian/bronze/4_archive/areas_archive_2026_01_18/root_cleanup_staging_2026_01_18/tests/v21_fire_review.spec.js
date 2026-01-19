// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import path from 'path';

test('Fire Review Lab Rendering Health', async ({ page }) => {
  const filePath = path.join(process.cwd(), 'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v21_fire_review.html');
  const fileUrl = `file://${filePath}`;

  const logs = [];
  page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));
  page.on('pageerror', err => logs.push(`[error] ${err.message}`));

  await page.goto(fileUrl);

  // Wait for Pixi initiation
  await page.waitForTimeout(2000);

  console.log('--- BROWSER LOGS ---');
  logs.forEach(log => console.log(log));
  console.log('--- END BROWSER LOGS ---');

  // Check for critical failures
  const errors = logs.filter(l => l.includes('[error]') || l.includes('PixiJS Error'));
  expect(errors).toHaveLength(0);

  // Check all 4 quadrants exist
  await expect(page.locator('#q1')).toBeVisible();
  await expect(page.locator('#q2')).toBeVisible();
  await expect(page.locator('#q3')).toBeVisible();
  await expect(page.locator('#q4')).toBeVisible();

  // Verify labels
  await expect(page.locator('text=GILDED SHIMMER')).toBeVisible();
  await expect(page.locator('text=CRIMSON TURBULENCE')).toBeVisible();
  await expect(page.locator('text=PLASMA TONGUES')).toBeVisible();
  await expect(page.locator('text=SOLAR CORONA')).toBeVisible();
});
