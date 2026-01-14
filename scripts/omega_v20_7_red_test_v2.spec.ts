// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

test('V20.7 Red Test: Excalidraw UI Button Interaction Failure', async ({ hfoPage, page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    // 1. Load the page
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v20_7.html';
    await hfoPage.goto(url);

    // 2. Initialize HFO (Unlock screen)
    await hfoPage.initHFO();

    // 3. Wait for the Excalidraw iframe and the button
    const iframe = page.frameLocator('#excalidraw-iframe');

    // Log available buttons with more attributes
    await page.waitForTimeout(5000);
    const buttons = await iframe.locator('button').all();
    console.log(`Found ${buttons.length} buttons in iframe`);
    for (const btn of buttons) {
        const label = await btn.getAttribute('aria-label');
        const title = await btn.getAttribute('title');
        const testid = await btn.getAttribute('data-testid');
        console.log(`Button: label=${label}, title=${title}, testid=${testid}`);
    }

    const rectangleBtn = iframe.locator('button[aria-label*="Rectangle"], button[title*="Rectangle"], [data-testid*="rectangle"]').first();

    await expect(rectangleBtn).toBeVisible({ timeout: 20000 });

    // 4. Get the bounding box of the button
    const box = await rectangleBtn.boundingBox();
    if (!box) throw new Error('Rectangle button bounding box not found');

    const iframeEl = page.locator('#excalidraw-iframe');
    const iframeBox = await iframeEl.boundingBox();
    if (!iframeBox) throw new Error('Iframe bounding box not found');

    // Calculate viewport coordinates for the button
    const viewX = iframeBox.x + box.x + box.width / 2;
    const viewY = iframeBox.y + box.y + box.height / 2;

    console.log(`Targeting button at Viewport: ${viewX}, ${viewY}`);

    // 5. Mock P1Bridger to return a fixed cursor over the target in COMMIT state
    await page.evaluate(({ x, y }) => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state) return;

        // @ts-ignore
        window.P1Bridger.fuse = () => {
            return [{
                screenX: x,
                screenY: y,
                normX: x / 1280,
                normY: y / 720,
                rawX: x,
                rawY: y,
                fsmState: 'COMMIT', // Force COMMIT to trigger pointerdown
                gesture: 'SELECT',
                confidence: 1.0,
                isPalmFacing: true,
                normalZ: 1.0,
                palmConeAngle: 0,
                palmNormal: { x: 0, y: 0, z: 1 },
                bucketLevel: 1.0,
                handIndex: 0,
                curls: { index: 1, middle: 1, ring: 1, pinky: 1 },
                timestamp: performance.now()
            }];
        };
        // @ts-ignore
        state.parameters.p0Active = true;
        // @ts-ignore
        window.hfoMockResults = { landmarks: [Array(21).fill({ x: 0, y: 0, z: 0 })], gestures: [[{ categoryName: 'select', score: 1 }]], handedness: [[{ categoryName: 'Right' }]] };
    }, { x: viewX, y: viewY });

    // 6. Wait for the interaction to process 
    await page.waitForTimeout(3000);

    // 7. Verify: The button should be active. 
    const isActive = await rectangleBtn.evaluate(el => {
        return el.classList.contains('active') ||
            el.getAttribute('aria-checked') === 'true' ||
            el.classList.contains('is-active');
    });

    console.log(`Is Rectangle tool active? ${isActive}`);

    // This is expected to FAIL until we implement the fix in v20.7
    expect(isActive).toBe(true);
});
