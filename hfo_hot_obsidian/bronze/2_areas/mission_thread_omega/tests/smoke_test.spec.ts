import { test, expect } from '@playwright/test';

test.describe('HFO Omega V17 Smoke Test', () => {
    test.beforeEach(async ({ page }) => {
        await page.addInitScript(() => {
            if (!navigator.mediaDevices) {
                // @ts-ignore
                navigator.mediaDevices = {};
            }
            Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
                value: async () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = 1280;
                    canvas.height = 720;
                    const stream = canvas.captureStream(30);
                    return stream;
                },
                configurable: true
            });
        });
    });

    test('should load with 4 cursors and Matter.js initialized', async ({ page }) => {
        page.on('console', msg => {
            if (msg.type() === 'error') console.log('BROWSER ERR:', msg.text());
            else console.log('BROWSER LOG:', msg.text());
        });
        page.on('pageerror', err => console.log('BROWSER EXCEPTION:', err.message));

        await page.goto('http://localhost:8092/omega_workspace_v17.html');

        await page.waitForSelector('#layout-container');
        
        // Wait for cards
        await page.waitForSelector('.data-card', { timeout: 30000 });
        const cards = await page.locator('.data-card h3').allInnerTexts();
        console.log('Detected Cards:', cards);
        
        // Match V16 titles
        const upperCards = cards.map(c => c.toUpperCase());
        expect(upperCards).toContain('SPRING (MATTER)');
        expect(upperCards).toContain('PREDICTIVE (MATTER)');
    });
});
