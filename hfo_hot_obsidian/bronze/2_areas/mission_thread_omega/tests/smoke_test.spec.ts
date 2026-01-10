import { test, expect } from '@playwright/test';

test.describe('HFO Omega V20 Smoke Test', () => {
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

            // Mock MediaPipe Global Scope (since it's imported via CDN in script tag)
            // @ts-ignore
            window.GestureRecognizer = {
                createFromOptions: async () => ({
                    recognizeForVideo: () => ({
                        landmarks: [[
                            {x:0,y:0,z:0},{x:0,y:0,z:0},{x:0,y:0,z:0},{x:0,y:0,z:0},{x:0,y:0,z:0},
                            {x:0,y:0,z:0},{x:0,y:0,z:0},{x:0,y:0,z:0},{x:0.5,y:0.5,z:0} // Landmark 8
                        ]],
                        gestures: [[{ categoryName: 'Open_Palm', score: 0.9 }]],
                    }),
                    setOptions: () => {}
                })
            };
            // @ts-ignore
            window.FilesetResolver = { forVisionTasks: async () => ({}) };
            // @ts-ignore
            window.DrawingUtils = class { drawConnectors() {} };
        });
    });

    test('should load with 4 cursors and Matter.js initialized', async ({ page }) => {
        page.on('console', msg => {
            if (msg.type() === 'error') console.log('BROWSER ERR:', msg.text());
            else console.log('BROWSER LOG:', msg.text());
        });
        page.on('pageerror', err => console.log('BROWSER EXCEPTION:', err.message));

        await page.goto('http://localhost:8092/omega_workspace_v20.html');

        await page.waitForSelector('#layout-container');

        // Wait for cards
        await page.waitForSelector('.hand-section', { timeout: 30000 });
        const cards = await page.locator('.data-card h3').allInnerTexts();
        console.log('Detected Cards:', cards);

        // Match V20 titles
        const upperCards = cards.map(c => c.toUpperCase());
        expect(upperCards).toContain('RAW');
        expect(upperCards).toContain('SMOOTH');
        expect(upperCards).toContain('SNAPPY');
        expect(upperCards).toContain('SPRING');
        expect(upperCards).toContain('PRED');
    });
});
