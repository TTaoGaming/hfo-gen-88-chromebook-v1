// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 88% | HIVE: V
import { test, expect } from '@playwright/test';

test.describe('PORT 5: Production Infrastructure Readiness', () => {
    const targetUrl = 'http://localhost:8889/active_omega.html';

    test('Critical Asset Loading and Console Audit', async ({ page }) => {
        const errors: string[] = [];
        const failedRequests: string[] = [];

        // 🛡️ [HFO SENTRY] Intercept failed requests
        page.on('requestfailed', request => {
            const entry = `${request.url()} [${request.failure()?.errorText}]`;
            failedRequests.push(entry);
            console.log(`❌ [REQUEST FAILED]: ${entry}`);
        });

        // 🛡️ [HFO SENTRY] Catch runtime and console errors
        page.on('console', msg => {
            if (msg.type() === 'error') {
                const text = msg.text();
                errors.push(text);
                console.log(`🔴 [CONSOLE ERROR]: ${text}`);
            }
        });

        page.on('pageerror', err => {
            errors.push(err.message);
        });

        page.on('response', response => {
            if (!response.ok()) {
                const entry = `${response.url()} [HTTP ${response.status()}]`;
                failedRequests.push(entry);
                console.log(`❌ [HTTP ERROR]: ${entry}`);
            }
        });

        // 🚀 [HFO SENTRY] Navigate to the active abstraction
        console.log(`Navigating to: ${targetUrl}`);
        const response = await page.goto(targetUrl);
        expect(response?.ok()).toBeTruthy();

        // Allow time for MediaPipe and Babylon to initialize
        await page.waitForTimeout(5000);

        // 🔍 Audit Infrastructure
        console.log('--- AUDIT REPORT ---');
        console.log('Failed Requests:', failedRequests.length);
        failedRequests.forEach(url => console.error(`  - FAILED: ${url}`));

        console.log('Console Errors:', errors.length);
        errors.forEach(err => console.error(`  - ERROR: ${err}`));

        // 🛡️ [HFO ASSERTIONS]
        expect(failedRequests, `Detected ${failedRequests.length} failed assets.`).toHaveLength(0);
        expect(errors, `Detected ${errors.length} console/runtime errors.`).toHaveLength(0);

        // Verify TutorialSystem state
        const tutorialStatus = await page.evaluate(() => {
            return {
                exists: !!window.hfoTutorial,
                isCompleted: window.hfoTutorial?.isCompleted,
                step: window.hfoTutorial?.currentStepIdx
            };
        });

        console.log('Tutorial Status:', tutorialStatus);
        expect(tutorialStatus.exists).toBe(true);
    });
});
