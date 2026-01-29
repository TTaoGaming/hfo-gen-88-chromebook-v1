// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import { GEN7_V1_PORTABLE_V23_10_URL_BASE, buildLightUrl, safeGoto } from './_support';

test.describe.configure({ mode: 'serial', retries: 0 });

test('Gen7 portable: v23.10 loads from 1_projects and exports core globals', async ({ page }) => {
  const url = buildLightUrl(
    GEN7_V1_PORTABLE_V23_10_URL_BASE,
    'test-run=smoke',
  );

  await safeGoto(page, url);
  await page.waitForTimeout(250);

  const ok = await page.evaluate(() => {
    const w = window as any;
    return {
      hasSystemState: Boolean(w.systemState),
      hasHfoStateAlias: Boolean(w.hfoState),
      hasPortsEffects: Boolean(w.hfoPortsEffects?.emit && w.hfoPortsEffects?.getRecent),
      hasP2Tripwire: Boolean(w.hfoP2TripwireThread?.tick),
      hasP3Injector: Boolean(w.hfoP3PlanckSensorInjector?.tick),
    };
  });

  expect(ok.hasSystemState).toBe(true);
  expect(ok.hasHfoStateAlias).toBe(true);
  expect(ok.hasPortsEffects).toBe(true);
  expect(ok.hasP2Tripwire).toBe(true);
  expect(ok.hasP3Injector).toBe(true);
});
