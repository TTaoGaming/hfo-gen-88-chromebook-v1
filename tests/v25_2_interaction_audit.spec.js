
import { test, expect } from '@playwright/test';
import path from 'path';

test('Audit V25.2 Interaction: Excalidraw Interaction', async ({ page }) => {
    const filePath = 'file://' + path.join(process.cwd(), 'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v25_2.html');

    page.on('console', msg => {
        if (msg.text().includes('EXCALIDRAW')) console.log('EXCALIDRAW LOG:', msg.text());
        else if (msg.type() === 'error') console.error('BROWSER ERROR:', msg.text());
        else console.log('BROWSER:', msg.text());
    });

    await page.goto(filePath);
    await page.waitForTimeout(5000);

    const iframe = page.frameLocator('#excalidraw-iframe');

    // Check for help button
    const helpBtn = iframe.locator('button[aria-label="Help"]');
    if (await helpBtn.count() > 0) {
        console.log('Help button found. Attempting to click...');
        await helpBtn.first().click({ force: true });
        console.log('Help button clicked.');

        // Check if dialog appears
        await page.waitForTimeout(2000);
        const dialog = iframe.locator('.excalidraw-dialog');
        if (await dialog.count() > 0) {
            console.log('Excalidraw Dialog (Help) is VISIBLE. Interaction confirmed.');
        } else {
            console.log('Excalidraw Dialog NOT visible after click.');
        }
    } else {
        console.log('Help button NOT found in Excalidraw iframe.');
        // List all buttons in iframe
        const buttons = await iframe.locator('button').all();
        console.log('Total buttons in iframe:', buttons.length);
        for (let i = 0; i < Math.min(buttons.length, 5); i++) {
            console.log('Button ' + i + ' aria-label: ' + await buttons[i].getAttribute('aria-label'));
        }
    }
});
