// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

test('V20.7 Red Test: Excalidraw UI Button Interaction Failure', async ({ hfoPage, page }) => {
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    // 1. Load the page
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v20_7.html';
    await hfoPage.goto(url);

    // 2. Initialize HFO (Unlock screen)
    await hfoPage.initHFO();

    // 2.5 Mock P1Bridger to return a fixed cursor over the target
    await hfoPage.evaluate(({ x, y }) => {
        // @ts-ignore
        window.P1Bridger.fuse = () => {
            return [{
                screenX: x,
                screenY: y,
                normX: x / 1280,
                normY: y / 720,
                rawX: x,
                rawY: y,
                fsmState: 'COMMIT',
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
        window.hfoState.parameters.p0Active = true;
        // Mock results just to keep predictLoop running
        // @ts-ignore
        window.hfoMockResults = { landmarks: [[]], gestures: [[]] };
    }, { x: viewX, y: viewY });

    // 3. Wait for hand 0 to appear

    // 3. Wait for hand 0 to appear
    await hfoPage.waitForHand(0);

    // 4. Locate the Rectangle tool button in the Excalidraw iframe
    const iframe = hfoPage.frameLocator('#excalidraw-iframe');
    const rectangleBtn = iframe.locator('button[aria-label="Rectangle"]').first();

    await expect(rectangleBtn).toBeVisible({ timeout: 15000 });

    // 5. Get the bounding box of the button
    const box = await rectangleBtn.boundingBox();
    if (!box) throw new Error('Rectangle button bounding box not found');

    const iframeEl = hfoPage.locator('#excalidraw-iframe');
    const iframeBox = await iframeEl.boundingBox();
    if (!iframeBox) throw new Error('Iframe bounding box not found');

    // Calculate viewport coordinates for the button
    const viewX = iframeBox.x + box.x + box.width / 2;
    const viewY = iframeBox.y + box.y + box.height / 2;

    console.log(`Targeting button at Viewport: ${viewX}, ${viewY}`);

    // 6. Inject Hand at those coordinates with COMMIT state
    // We need to map from viewport back to internal sensing buffer (usually 1280x720)
    // In Gen 4, v20.7, screenX/Y are used.
    await hfoPage.injectHand(0, {
        active: true,
        screenX: 1280 * (viewX / 1280), // Assuming viewport matches buffer for now or let the injector handle it
        screenY: 720 * (viewY / 720),
        state: 'COMMIT',
        event: 'pointerdown',
        cursors: {
            snappy: { x: viewX / 1280, y: viewY / 720 }, // Mock cursor position
            predictive: { x: viewX / 1280, y: viewY / 720 }
        }
    });

    // 7. Wait and check for selection. 
    // In Excalidraw, the active tool usually has a background color or a specific class.
    // Or we can check if it's 'checked' if it's an input/checkbox-like button.
    // Current Excalidraw uses data-testid or aria-checked.

    // Wait for the interaction to process
    await hfoPage.waitForTimeout(1000);

    // Verify: The button should be active. 
    // This is the RED part: We expect it to NOT be active because of the bug.
    const isActive = await rectangleBtn.evaluate(el => el.classList.contains('active') || el.getAttribute('aria-checked') === 'true');

    console.log(`Is Rectangle tool active? ${isActive}`);

    // We expect failure here to confirm the bug.
    // But for a TDD red test, we assert what SHOULD happen and see the test fail.
    expect(isActive).toBe(true);
});
