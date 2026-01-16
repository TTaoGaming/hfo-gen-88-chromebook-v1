import { test, expect } from '@playwright/test';

test.describe('HFO Forensic Audit', () => {
    const targets = [
        'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v29_1.html',
        'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v30.html'
    ];

    for (const target of targets) {
        test(`Audit ${target}`, async ({ page }) => {
            const errors: string[] = [];
            const failedResources: string[] = [];

            page.on('requestfailed', request => {
                failedResources.push(`${request.url()} [${request.failure()?.errorText}]`);
            });

            page.on('response', response => {
                if (!response.ok() && response.status() !== 404) {
                    failedResources.push(`${response.url()} [HTTP ${response.status()}]`);
                }
            });

            page.on('console', msg => {
                if (msg.type() === 'error') {
                    errors.push(msg.text());
                }
            });

            page.on('pageerror', err => {
                errors.push(err.message);
            });

            console.log(`🚀 Auditing: http://localhost:8888/${target}`);
            await page.goto(`http://localhost:8888/${target}`);

            // Allow settle time
            await page.waitForTimeout(5000);

            if (errors.length > 0) {
                console.error(`🔴 Errors in ${target}:`, errors);
            }
            if (failedResources.length > 0) {
                console.error(`❌ Failed Resources in ${target}:`, failedResources);
            }

            expect(errors, `No runtime errors permitted in ${target}`).toHaveLength(0);
            expect(failedResources, `All resources must load in ${target}`).toHaveLength(0);
        });
    }
});
