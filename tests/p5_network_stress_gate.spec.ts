import { test, expect } from '@playwright/test';

/**
 * Medallion: Bronze | Mutation: 0% | HIVE: V
 * PORT 5: QUALITY GATE (NETWORK STRESS)
 * Detects net::ERR_CONNECTION_RESET and asset failures under concurrent load.
 */

test.describe('Port 5 Infrastructure Gate', () => {
    // Audit Port 5500 (Live Server) to catch regressions as requested
    const targetUrl = 'http://localhost:5500/active_omega.html';

    test('Audit for net::ERR_CONNECTION_RESET and high-concurrency 404s', async ({ page }) => {
        const failedRequests: string[] = [];

        // Listen for failed requests
        page.on('requestfailed', (request) => {
            const failure = request.failure();
            failedRequests.push(`${request.url()} [${failure?.errorText || 'Unknown Error'}]`);
        });

        // Listen for non-200 responses (But allow 304 Not Modified)
        page.on('response', (response) => {
            const status = response.status();
            if (!response.ok() && status !== 304 && status !== 0) {
                failedRequests.push(`${response.url()} [HTTP ${status}]`);
            }
        });

        console.log(`🚀 [P5-GATE]: Navigating to ${targetUrl}`);
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        // Stress: Force a few reloads to see if the server chokes
        for (let i = 1; i <= 3; i++) {
            console.log(`🔄 [P5-GATE]: Stress Reload ${i}/3...`);
            await page.reload({ waitUntil: 'networkidle' });
        }

        if (failedRequests.length > 0) {
            console.error('❌ [P5-GATE-FAILURE]: Detected network regressions:');
            failedRequests.forEach(err => console.error(`  - ${err}`));
        }

        expect(failedRequests.length, `Detected ${failedRequests.length} network failures. Check logs for net::ERR_CONNECTION_RESET.`).toBe(0);
        console.log('✅ [P5-GATE-PASS]: Infrastructure stable under stress.');
    });
});
