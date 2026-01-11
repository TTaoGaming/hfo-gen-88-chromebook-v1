
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

/**
 * V44 E2E: Verify the new 6-State FSM interaction on Excalidraw.
 */
test('V44 E2E: 6-State FSM Interaction on Excalidraw', async ({ hfoPage }) => {
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v44.html';
    await hfoPage.goto(url);
    await hfoPage.initHFO();
    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoState.active = true;
        // @ts-ignore
        window.hfoSystem.loopActive = true;
    });
    await hfoPage.waitForHand(0);

    // Wait for Excalidraw
    const frame = hfoPage.frameLocator('iframe#excalidraw-iframe');
    const canvas = frame.locator('canvas.interactive');
    await expect(canvas).toBeVisible({ timeout: 20000 });

    // 1. Check if we can enter ARMED state via Palm Face
    await hfoPage.injectHand(0, {
        active: true,
        palm: { facingCamera: true, normal: { x: 0, y: 0, z: -1 } },
        state: 'ARMING'
    });

    // Wait for dwellMs (500ms)
    await hfoPage.waitForTimeout(600);

    // Verify ARMED state
    const hand0 = await hfoPage.getHandState(0);
    console.log(`State after dwell (500ms): ${hand0.state}`);
    expect(hand0.state).toBe('ARMED');

    // 2. Commit with POINTING_UP
    await hfoPage.injectHand(0, {
        state: 'COMMITTED',
        event: 'pointerdown',
        gestures: { active: 'POINTING_UP', score: 0.9 }
    });

    const hand1 = await hfoPage.getHandState(0);
    console.log(`State after POINTING_UP: ${hand1.state}`);
    expect(hand1.state).toBe('COMMITTED');

    // 4. Test RELEASING state (lose gesture but keep palm)
    await hfoPage.injectHand(0, {
        gestures: { active: 'NONE', score: 0.8 }
    });

    const hand2 = await hfoPage.getHandState(0);
    console.log(`State after losing gesture (NONE): ${hand2.state}`);
    expect(hand2.state).toBe('RELEASING');

    // 5. Test IDLE (palm away)
    await hfoPage.injectHand(0, {
        palm: { facingCamera: false, normal: { x: 0, y: 1, z: 0 } }
    });

    await hfoPage.waitForTimeout(600);
    const hand3 = await hfoPage.getHandState(0);
    console.log(`State after palm away: ${hand3.state}`);
    expect(hand3.state).toBe('IDLE');
});
