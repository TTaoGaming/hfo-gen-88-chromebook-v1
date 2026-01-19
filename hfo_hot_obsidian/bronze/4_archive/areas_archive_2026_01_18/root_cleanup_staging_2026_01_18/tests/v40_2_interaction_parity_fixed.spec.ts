// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * 🕵️ FORENSIC SPEC: V40.2 INTERACTION PARITY
 * Target: Zero-Slop Interaction (isPrimary, Chirality PointerID, Gated PointerMove)
 * 🦾 Anchored to Sovereign FSM Logic
 */
test.describe('V40.2 Zero-Slop Interaction Parity', () => {

    test.beforeEach(async ({ page }) => {
        // Force the environment into Port 8889 (Production Rebirth)
        await page.goto('http://localhost:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v40_2.html');

        // Wait for system to initialize
        await page.waitForFunction(() => window.hfoLifecycle !== undefined);
    });

    /**
     * Test: isPrimary Hand Promotion
     * Hand 1 (Right) should become primary when it reaches READY/COMMIT state.
     */
    test('Hand 1 should become Primary after Dwell + Pointing_Up', async ({ page }) => {
        // 🛠️ MOCK HAND DATA: Right Hand (Index 1)
        // We need a valid 3D plane for normalZ > 0.7
        const createHand = (index, x, y, z, gesture = 'None') => ({
            index: index,
            score: 0.95,
            label: index === 0 ? 'Left' : 'Right',
            worldLandmarks: Array(21).fill(0).map((_, i) => {
                // Node 0: Wrist
                if (i === 0) return { x: 0, y: 0, z: 0 };
                // Node 5: Index MCP (Horizontal-ish)
                if (i === 5) return { x: 0.05, y: 0.01, z: 0.02 };
                // Node 17: Pinky MCP (Vertical-ish) - Create a tilt away from camera
                if (i === 17) return { x: 0.01, y: 0.05, z: 0.03 };
                return { x: 0, y: 0, z: 0 };
            }),
            landmarks: Array(21).fill(0).map(() => ({ x, y, z })),
            gestures: [{ categoryName: gesture, score: 0.99 }]
        });

        // Step 1: Initialize Hands (Wait for Readiness)
        // Hand 0 is present but IDLE.
        // Hand 1 is "Palm Facing" (isCharging = true)
        await page.evaluate((hand0, hand1) => {
            window.hfoMockNow = 1000;
            window.hfoMockResults = {
                gestures: [hand0.gestures, hand1.gestures],
                landmarks: [hand0.landmarks, hand1.landmarks],
                worldLandmarks: [hand0.worldLandmarks, hand1.worldLandmarks]
            };
            // Note: MediaPipe result structure has 'handedness' array for label
            window.hfoMockResults.handedness = [
                [{ categoryName: hand0.label, score: 0.99 }],
                [{ categoryName: hand1.label, score: 0.99 }]
            ];
            // @ts-ignore
            predictLoop();
        }, createHand(0, 0.2, 0.5, 0), createHand(1, 0.8, 0.5, 0));

        // Step 2: Dwell to fill Leaky Bucket (ChargeTime is 250ms)
        // 50ms steps x 6 = 300ms
        for (let i = 1; i <= 6; i++) {
            await page.evaluate((val) => {
                window.hfoMockNow = 1000 + (val * 50);
                // @ts-ignore
                predictLoop();
            }, i);
        }

        // Step 3: Verify Hand 1 is READY and Primary (since Hand 0 is IDLE)
        let state = await page.evaluate(() => window.hfoState);
        expect(state.hands[1].fsmState).toBe('READY');
        expect(state.fsm.primaryHandIndex).toBe(1);

        // Step 4: Perform "Pointing_Up" to enter COMMIT
        await page.evaluate((hand0, hand1) => {
            window.hfoMockNow = 1400;
            window.hfoMockResults.gestures[1] = [{ categoryName: 'Pointing_Up', score: 0.99 }];
            // @ts-ignore
            predictLoop();
        }, createHand(0, 0.2, 0.5, 0), createHand(1, 0.8, 0.5, 0));

        state = await page.evaluate(() => window.hfoState);
        expect(state.hands[1].fsmState).toBe('COMMIT');
    });

    /**
     * Test: Chirality-Persistence (PointerID)
     * Left Hand should ALWAYS be PointerID 10, Right Hand ALWAYS 11.
     */
    test('Pointer IDs should be deterministic based on Chirality', async ({ page }) => {
        const createHand = (label, x) => ({
            label: label,
            worldLandmarks: Array(21).fill(0).map((_, i) => {
                if (i === 0) return { x: 0, y: 0, z: 0 };
                if (i === 5) return { x: 0.05, y: 0, z: 0.02 };
                if (i === 17) return { x: 0, y: 0.05, z: 0.03 };
                return { x: 0, y: 0, z: 0 };
            }),
            landmarks: Array(21).fill(0).map(() => ({ x, y: 0.5, z: 0 })),
            gestures: [{ categoryName: 'Pointing_Up', score: 0.99 }]
        });

        await page.evaluate((hLeft, hRight) => {
            window.hfoMockResults = {
                gestures: [hLeft.gestures, hRight.gestures],
                landmarks: [hLeft.landmarks, hRight.landmarks],
                worldLandmarks: [hLeft.worldLandmarks, hRight.worldLandmarks],
                handedness: [
                    [{ categoryName: 'Left', score: 0.99 }],
                    [{ categoryName: 'Right', score: 0.99 }]
                ]
            };
            window.hfoMockNow = 2000;
            // Charge them up quickly
            for (let i = 0; i < 10; i++) {
                window.hfoMockNow += 50;
                // @ts-ignore
                predictLoop();
            }
        }, createHand('Left', 0.2), createHand('Right', 0.8));

        const state = await page.evaluate(() => window.hfoState);

        // Find Right hand (Index 1 usually, but let's check label)
        const rightHand = state.hands.find(h => h.label === 'Right');
        const leftHand = state.hands.find(h => h.label === 'Left');

        expect(leftHand.pointerId).toBe(10);
        expect(rightHand.pointerId).toBe(11);
    });

    /**
     * Test: PointerMove Gating (V40.2 Security)
     * Movements should NOT be injected unless the hand is in the COMMIT state.
     */
    test('PointerMove events should be gated by COMMIT state', async ({ page }) => {
        // Create a record of events
        await page.evaluate(() => {
            window.hfoEvents = [];
            window.addEventListener('pointermove', (e) => {
                // @ts-ignore
                window.hfoEvents.push({ type: e.type, pointerId: e.pointerId });
            });
        });

        const createHand = (gesture) => ({
            label: 'Right',
            worldLandmarks: Array(21).fill(0).map((_, i) => {
                if (i === 0) return { x: 0, y: 0, z: 0 };
                if (i === 5) return { x: 0.05, y: 0, z: 0.02 };
                if (i === 17) return { x: 0, y: 0.05, z: 0.03 };
                return { x: 0, y: 0, z: 0 };
            }),
            landmarks: Array(21).fill(0).map(() => ({ x: 0.5, y: 0.5, z: 0 })),
            gestures: [{ categoryName: gesture, score: 0.99 }]
        });

        // 1. Move in IDLE (Should be gated)
        await page.evaluate((hand) => {
            window.hfoMockResults = {
                gestures: [hand.gestures],
                landmarks: [hand.landmarks],
                worldLandmarks: [hand.worldLandmarks],
                handedness: [[{ categoryName: 'Right', score: 0.99 }]]
            };
            window.hfoMockNow = 3000;
            // @ts-ignore
            predictLoop();
        }, createHand('None'));

        let events = await page.evaluate(() => window.hfoEvents);
        expect(events.length).toBe(0);

        // 2. Transition to COMMIT
        await page.evaluate(() => {
            // Charge it up
            for (let i = 0; i < 10; i++) {
                window.hfoMockNow += 50;
                // @ts-ignore
                predictLoop();
            }
        });

        // 3. Pointing_Up -> COMMIT
        await page.evaluate((hand) => {
            window.hfoMockResults.gestures[0] = hand.gestures;
            window.hfoMockNow += 50;
            // @ts-ignore
            predictLoop();
        }, createHand('Pointing_Up'));

        // 4. Move in COMMIT (Should pass gate)
        await page.evaluate(() => {
            window.hfoMockNow += 50;
            // @ts-ignore
            predictLoop();
        });

        events = await page.evaluate(() => window.hfoEvents);
        expect(events.length).toBeGreaterThan(0);
    });
});
