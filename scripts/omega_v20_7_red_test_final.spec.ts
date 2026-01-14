// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

test('V20.7 Red Test: Excalidraw UI Button Interaction Failure', async ({ hfoPage, page }) => {
    test.setTimeout(120000); // 2 minutes for very slow Chromebook/Network
    await page.setViewportSize({ width: 1920, height: 1080 });
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
    
    // 1. Load the page
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v20_7.html';
    await hfoPage.goto(url);

    // 2. Initialize HFO (Unlock screen and disable mirror for test parity)
    await hfoPage.initHFO();
    await page.evaluate(() => {
        window.hfoState.parameters.camera.mirror = false;
        window.hfoState.parameters.devMode = true;
    });
    
    // 3. Wait for Excalidraw to be fully ready
    console.log("Waiting for Excalidraw to be ready...");
    const iframeEl = page.locator('#excalidraw-iframe');
    const iframe = page.frameLocator('#excalidraw-iframe');
    
    // 3. Wait for the Help button (known to be present)
    const targetBtn = iframe.locator('button[aria-label="Help"]').first();
    await targetBtn.waitFor({ state: 'visible', timeout: 60000 });
    console.log("Target button found.");

    // 4. Get the bounding box
    const box = await targetBtn.boundingBox();
    if (!box) throw new Error('Target button bounding box not found');

    const iframeBox = await iframeEl.boundingBox();
    if (!iframeBox) throw new Error('Iframe bounding box not found');

    // Calculate viewport coordinates for the button
    const viewX = iframeBox.x + box.x + box.width / 2;
    const viewY = iframeBox.y + box.y + box.height / 2;

    console.log(`Targeting button at Viewport: ${viewX}, ${viewY}`);

    // 5. Mock hand interaction at those coordinates
    await page.evaluate(({x, y}) => {
        const state = window.hfoState;
        if (!state) return;

        state.parameters.p0Active = true;
        
        const mockLandmarks = Array(21).fill(0).map((_, i) => ({
            x: x / 1920, 
            y: y / 1080,
            z: 0
        }));
        mockLandmarks[5] = { x: x / 1920, y: (y + 10) / 1080, z: 0 };
        mockLandmarks[8] = { x: x / 1920, y: y / 1080, z: 0 };

        window.hfoMockResults = {
            landmarks: [mockLandmarks],
            gestures: [[{categoryName: 'pointing_up', score: 1.0}]],
            handedness: [[{categoryName: 'Right', score: 1.0}]]
        };
    }, { x: viewX, y: viewY });

    // 6. Wait for the interaction to process.
    await page.waitForTimeout(3000);

    // 7. Verify: The button should be active/focused.
    // Clicking 'Help' in Excalidraw usually opens a modal or highlights the button.
    const hasFocusOrModal = await targetBtn.evaluate(el => {
        return document.activeElement === el || document.querySelector('.HelpDialog') !== null;
    });
    
    console.log(`Is Help dialog open? ${hasFocusOrModal}`);
    
    expect(hasFocusOrModal).toBe(true); 
});
