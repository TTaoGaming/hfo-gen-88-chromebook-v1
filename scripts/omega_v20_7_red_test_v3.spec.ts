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

    // 3. Wait for Excalidraw to be fully ready
    console.log("Waiting for Excalidraw to be ready...");
    const iframeEl = page.locator('#excalidraw-iframe');
    const src = await iframeEl.getAttribute('src');
    console.log(`Iframe src: ${src}`);

    const iframe = page.frameLocator('#excalidraw-iframe');

    // Wait for ANY button
    await iframe.locator('button').first().waitFor({ state: 'visible', timeout: 30000 });
    console.log("Found at least one button in iframe.");

    // 4. Get the bounding box of the button
    const box = await rectangleBtn.boundingBox();
    if (!box) throw new Error('Rectangle button bounding box not found');

    const iframeBox = await iframeEl.boundingBox();
    if (!iframeBox) throw new Error('Iframe bounding box not found');

    // Calculate viewport coordinates for the button
    const viewX = iframeBox.x + box.x + box.width / 2;
    const viewY = iframeBox.y + box.y + box.height / 2;

    console.log(`Targeting button at Viewport: ${viewX}, ${viewY}`);

    // 5. Mock hand interaction at those coordinates
    await page.evaluate(({ x, y }) => {
        const state = window.hfoState;
        if (!state) return;

        // Force P0 Active and set mock results
        state.parameters.p0Active = true;

        // We need 21 landmarks to satisfy Port 1 Fusion contract
        const mockLandmarks = Array(21).fill(0).map((_, i) => ({
            x: x / 1920, // Match viewport scale
            y: y / 1080,
            z: 0
        }));
        // Offset tip (8) and mcp (5) slightly to provide a valid direction for the "rod"
        mockLandmarks[5] = { x: x / 1920, y: (y + 10) / 1080, z: 0 };
        mockLandmarks[8] = { x: x / 1920, y: y / 1080, z: 0 };

        window.hfoMockResults = {
            landmarks: [mockLandmarks],
            gestures: [[{ categoryName: 'pointing_up', score: 1.0 }]],
            handedness: [[{ categoryName: 'Right', score: 1.0 }]]
        };

        // Force a specific FSM state in the fabric
        // This is a bit of a bypass but ensures the injector sees a COMMIT state
        window.hfoMockFSMState = 'COMMIT';
    }, { x: viewX, y: viewY });

    // 6. Wait for the interaction to process. We expect the system to stay in COMMIT state.
    // We need to ensure the injector actually runs. v20.7 calls it every frame in predictLoop.
    await page.waitForTimeout(3000);

    // 7. Verify: The button should be active. 
    // In current Excalidraw, active tools may have 'aria-checked="true"' or specific styles.
    const isActive = await rectangleBtn.evaluate(el => {
        return el.classList.contains('active') ||
            el.getAttribute('aria-checked') === 'true' ||
            getComputedStyle(el).backgroundColor !== 'transparent';
    });

    console.log(`Is Rectangle tool active? ${isActive}`);

    // We expect this to fail (isActive === false) in the currently bugged v20.7
    expect(isActive).toBe(true);
});
