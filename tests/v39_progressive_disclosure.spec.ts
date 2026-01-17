import { test, expect } from '@playwright/test';
import path from 'path';

test.describe('V39 Progressive Disclosure Audit', () => {

    test('Toggling Essentials Mode should transform the UI', async ({ page }) => {
        page.on('console', msg => console.log('BROWSER:', msg.text()));
        const fileUrl = `http://localhost:8889/active_omega.html`;
        await page.goto(fileUrl);
        await page.waitForSelector('.lil-gui');

        console.log('--- Phase 1: Check Default Essentials Mode ---');

        const folderState = await page.evaluate(() => {
            const folders = Array.from(document.querySelectorAll('.lil-gui'));
            const neural = folders.find(f => {
                const title = f.querySelector(':scope > .title');
                return title && title.textContent.includes('Neural Shards');
            });
            if (!neural) return 'NOT_FOUND';
            const isHidden = window.getComputedStyle(neural).display === 'none';
            return isHidden ? 'HIDDEN' : 'VISIBLE';
        });
        console.log('P0 State:', folderState);
        expect(folderState).toBe('HIDDEN');

        console.log('--- Phase 2: Toggle to Developer Mode ---');
        // More robust locator for lil-gui boolean
        const toggle = page.locator('.lil-gui .name', { hasText: 'ESSENTIALS (KIOSK)' }).first();
        await toggle.click();

        await page.waitForTimeout(5000);

        const devState = await page.evaluate(() => {
            const folders = Array.from(document.querySelectorAll('.lil-gui'));
            const neural = folders.find(f => {
                const title = f.querySelector(':scope > .title');
                return title && title.textContent.includes('Neural Shards');
            });
            if (!neural) return 'NOT_FOUND';
            const isHidden = window.getComputedStyle(neural).display === 'none';
            return isHidden ? 'HIDDEN' : 'VISIBLE';
        });
        console.log('P0 Dev State:', devState);
        expect(devState).toBe('VISIBLE');
    });
});
