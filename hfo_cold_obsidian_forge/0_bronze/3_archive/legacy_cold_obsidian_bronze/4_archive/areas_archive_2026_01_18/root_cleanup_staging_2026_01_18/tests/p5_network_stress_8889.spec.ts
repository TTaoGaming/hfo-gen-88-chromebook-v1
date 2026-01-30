// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * Medallion: Bronze | Mutation: 0% | HIVE: V
 * PORT 5: QUALITY GATE (NETWORK STRESS) - AUDIT 8889
 */

test.describe('Port 5 Infrastructure Gate (8889)', () => {
    const targetUrl = 'http://localhost:8889/active_omega.html';

    test('Audit for net::ERR_CONNECTION_RESET and high-concurrency 404s on 8889', async ({ page }) => {
        const failedRequests: string[] = [];

        page.on('requestfailed', (request) => {
            const failure = request.failure();
            failedRequests.push(`${request.url()} [${failure?.errorText || 'Unknown Error'}]`);
        });

        page.on('response', (response) => {
            // Note: 304 is OK in Playwright's response.ok()
            if (!response.ok() && response.status() !== 0) {
                failedRequests.push(`${response.url()} [HTTP ${response.status()}]`);
            }
        });

        console.log(`🚀 [P5-GATE]: Navigating to ${targetUrl}`);
        await page.goto(targetUrl, { waitUntil: 'networkidle' });

        for (let i = 1; i <= 3; i++) {
            console.log(`🔄 [P5-GATE]: Stress Reload ${i}/3...`);
            await page.reload({ waitUntil: 'networkidle' });
        }

        if (failedRequests.length > 0) {
            console.error('❌ [P5-GATE-FAILURE]: Detected network regressions on 8889:');
            failedRequests.forEach(err => console.error(`  - ${err}`));
        }

        expect(failedRequests.length, `Detected ${failedRequests.length} network failures on 8889.`).toBe(0);
        console.log('✅ [P5-GATE-PASS]: Port 8889 stable under stress.');
    });
});
