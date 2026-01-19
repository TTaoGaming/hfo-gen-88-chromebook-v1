// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

test.describe('P5 Runtime Sentry', () => {
  const errors: string[] = [];
  const warnings: string[] = [];

  test('V30.0 Production Readiness Audit', async ({ page }) => {
    // 🛡️ [HFO SENTRY] Initialize Listeners

    const failedResources: string[] = [];
    page.on('requestfailed', request => {
      failedResources.push(`${request.url()} [${request.failure()?.errorText}]`);
      console.error('❌ [RESOURCE FAILED]:', request.url(), request.failure()?.errorText);
    });

    page.on('response', response => {
      if (!response.ok() && response.status() !== 404) {
        failedResources.push(`${response.url()} [HTTP ${response.status()}]`);
        console.error('❌ [HTTP ERROR]:', response.url(), response.status());
      }
    });

    page.on('console', msg => {
      const text = msg.text();
      if (msg.type() === 'error') {
        errors.push(text);
        console.error('🔴 [CONSOLE ERROR]:', text);
      } else if (msg.type() === 'warning') {
        warnings.push(text);
        console.warn('🟡 [CONSOLE WARN]:', text);
      }
    });

    page.on('pageerror', err => {
      errors.push(err.message);
      console.error('🛑 [RUNTIME ERROR]:', err.message);
    });

    // 🚀 [HFO SENTRY] Execute Boot (via HTTP to avoid CORS)
    await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v30_1.html');

    // Allow settle time
    await page.waitForTimeout(3000);

    // 🔍 [HFO SENTRY] Diagnostic: Deep Probe
    const ofProbe = await page.evaluate(() => {
      const root = window.OpenFeature;
      if (!root) return { status: 'MISSING' };

      const results = {
        rootKeys: Object.keys(root),
        ofKeys: root.OpenFeature ? Object.keys(root.OpenFeature) : [],
        ofHasSetProvider: root.OpenFeature && typeof root.OpenFeature.setProvider === 'function',
        ofApiKeys: root.OpenFeatureAPI ? Object.keys(root.OpenFeatureAPI) : [],
        ofApiInstanceKeys: (root.OpenFeatureAPI && root.OpenFeatureAPI.getInstance) ? Object.keys(root.OpenFeatureAPI.getInstance()) : [],
      };

      let match = null;
      if (typeof root.setProvider === 'function') match = 'root';
      else if (root.OpenFeature && typeof root.OpenFeature.setProvider === 'function') match = 'root.OpenFeature';
      else if (root.OpenFeatureAPI && root.OpenFeatureAPI.getInstance && typeof root.OpenFeatureAPI.getInstance().setProvider === 'function') match = 'root.OpenFeatureAPI.getInstance()';

      return { ...results, match };
    });
    console.log('🧪 [HFO DEBUG] OpenFeature Probe:', JSON.stringify(ofProbe, null, 2));

    // 🔍 [HFO SENTRY] Assertions
    expect(errors, 'No runtime TypeErrors permitted in production baseline').toHaveLength(0);
    expect(failedResources, 'Critical resources must load successfully').toHaveLength(0);

    const globals = await page.evaluate(() => {
      return {
        openFeature: typeof window.OpenFeature !== 'undefined',
        babylon: typeof window.BABYLON !== 'undefined',
        goldenLayout: typeof window.GoldenLayout !== 'undefined'
      };
    });

    expect(globals.openFeature, 'OpenFeature Global must be defined').toBe(true);
    expect(globals.babylon, 'Babylon.js Global must be defined').toBe(true);

    // 🔍 [HFO SENTRY] ImportMap Integrity Check
    const importValidation = await page.evaluate(async () => {
      const results = { planck: false, zod: false, gui: false };
      try {
        const planck = await import('planck');
        results.planck = !!planck;
        const zod = await import('zod');
        results.zod = !!zod;
        const gui = await import('lil-gui');
        results.gui = !!gui;
      } catch (e) {
        console.error('🛑 [IMPORT FAILURE]:', e);
      }
      return results;
    });

    expect(importValidation.planck, 'ESM Import: planck must be resolvable').toBe(true);
    expect(importValidation.zod, 'ESM Import: zod must be resolvable').toBe(true);
    expect(importValidation.gui, 'ESM Import: lil-gui must be resolvable').toBe(true);
  });

  test('V29.1 Standard Baseline Audit', async ({ page }) => {
    // 🛡️ [HFO SENTRY] Initialize Listeners
    const failedResources: string[] = [];
    const localErrors: string[] = [];

    page.on('requestfailed', request => failedResources.push(`${request.url()} [${request.failure()?.errorText}]`));
    page.on('console', msg => { if (msg.type() === 'error') localErrors.push(msg.text()); });
    page.on('pageerror', err => localErrors.push(err.message));

    await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v29_1.html');
    await page.waitForTimeout(3000);

    expect(localErrors, 'V29.1 Regression Detected').toHaveLength(0);
    expect(failedResources, 'V29.1 Resources Missing').toHaveLength(0);
  });
});
