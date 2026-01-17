// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * BDD INTERACTION PARITY TEST: v40.2
 * Purpose: Verifies dynamic isPrimary logic and pointermove gating.
 * Target: omega_gen4_v40_2.html
 */

const TARGET_URL = 'http://127.0.0.1:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v40_2.html?flag-p3-injector=true&flag-p3-move-gate=true';

test.describe('V40.2 Interaction Hardening', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto(TARGET_URL);
        await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

        // Setup Event Logger
        await page.evaluate(() => {
            (window as any).pointerEventsLog = [];
            const handler = (e: any) => {
                (window as any).pointerEventsLog.push({
                    type: e.type,
                    pointerId: e.pointerId,
                    isPrimary: e.isPrimary,
                    button: e.button,
                    buttons: e.buttons
                });
            };
            // Listen on window to catch all synthetic events
            window.addEventListener('pointerdown', handler, true);
            window.addEventListener('pointermove', handler, true);
            window.addEventListener('pointerup', handler, true);
        });
    });

    test('Verify dynamic isPrimary for the second hand', async ({ page }) => {
        console.log('Test: Second hand becomes primary...');

        await page.evaluate(async () => {
            const createHand = (x, y, z) => {
                const landmarks = [];
                for (let i = 0; i < 21; i++) {
                    landmarks.push({ x: x + i * 0.001, y: y + i * 0.001, z: z });
                }
                // Landmarks for palm calculation
                landmarks[0] = { x: x, y: y, z: z };
                landmarks[5] = { x: x + 0.05, y: y, z: z };
                landmarks[17] = { x: x, y: y + 0.05, z: z };
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: z }; // Index tip
                return landmarks;
            };

            // Case: Two hands present
            const hand0 = createHand(0.3, 0.5, -0.1); // Left-ish
            const hand1 = createHand(0.7, 0.5, -0.1); // Right-ish

            // Hand 1 enters COMMIT (Pointing_Up) while Hand 0 is None
            // This should make Hand 1 (index 1) the primary hand
            (window as any).hfoMockResults = {
                landmarks: [hand0, hand1],
                gestures: [
                    [{ categoryName: 'None', score: 0.99 }],
                    [{ categoryName: 'Pointing_Up', score: 0.99 }]
                ],
                handedness: [[{ categoryName: 'Left' }], [{ categoryName: 'Right' }]]
            };

            // Run multiple frames to fill leaky bucket
            for (let i = 0; i < 40; i++) {
                // @ts-ignore
                (window as any).hfoMockNow = (performance.now() || 0) + (i * 50); // Advance 50ms per frame
                predictLoop();
            }
        });

        // Check if Hand 1 (pid 11) is primary
        const events = await page.evaluate(() => (window as any).pointerEventsLog);

        // Find events from hand 1 (pid 11)
        const hand1Events = events.filter((e: any) => e.pointerId === 11);
        const hand0Events = events.filter((e: any) => e.pointerId === 10);

        console.log(`Hand 0 Events: ${hand0Events.length}, Hand 1 Events: ${hand1Events.length}`);

        // Hand 1 should have been primary because it was the one to point first
        const hasPrimaryHand1 = hand1Events.some((e: any) => e.isPrimary === true);
        expect(hasPrimaryHand1).toBe(true);

        // Hand 0 should NOT be primary
        const hasPrimaryHand0 = hand0Events.some((e: any) => e.isPrimary === true);
        expect(hasPrimaryHand0).toBe(false);
    });

    test('Verify pointermove gating: No moves in READY state', async ({ page }) => {
        console.log('Test: READY state move gating...');

        await page.evaluate(() => {
            (window as any).pointerEventsLog = []; // Reset log
        });

        await page.evaluate(async () => {
            const createHand = (x, y, z) => {
                const landmarks = [];
                for (let i = 0; i < 21; i++) {
                    landmarks.push({ x: x + i * 0.001, y: y + i * 0.001, z: z });
                }
                landmarks[0] = { x: x, y: y, z: z };
                landmarks[5] = { x: x + 0.05, y: y, z: z };
                landmarks[17] = { x: x, y: y + 0.05, z: z };
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: z };
                return landmarks;
            };

            const hand0 = createHand(0.5, 0.5, -0.1);

            // Hand 0 is READY (No gesture) but moving
            (window as any).hfoMockResults = {
                landmarks: [hand0],
                gestures: [[{ categoryName: 'None', score: 0.99 }]],
                handedness: [[{ categoryName: 'Right' }]]
            };

            // Run frames to get into READY state (Needs palm facing)
            // Note: landmarks[5/17] were set for palm facing in createHand
            for (let i = 0; i < 20; i++) {
                // Slightly move the hand each frame
                (window as any).hfoMockResults.landmarks[0][8].x += 0.001;
                // @ts-ignore
                predictLoop();
            }
        });

        const events = await page.evaluate(() => (window as any).pointerEventsLog);
        const moves = events.filter((e: any) => e.type === 'pointermove');

        console.log(`Moves in READY state: ${moves.length}`);

        // Should be ZERO moves because isDown is false in READY state
        expect(moves.length).toBe(0);

        // Now enter COMMIT state
        await page.evaluate(async () => {
            (window as any).hfoMockResults.gestures = [[{ categoryName: 'Pointing_Up', score: 0.99 }]];
            for (let i = 0; i < 5; i++) {
                // @ts-ignore
                predictLoop();
            }
        });

        const eventsAfterCommit = await page.evaluate(() => (window as any).pointerEventsLog);
        const movesAfterCommit = eventsAfterCommit.filter((e: any) => e.type === 'pointermove');

        console.log(`Moves after COMMIT: ${movesAfterCommit.length}`);
        expect(movesAfterCommit.length).toBeGreaterThan(0);
    });
});
