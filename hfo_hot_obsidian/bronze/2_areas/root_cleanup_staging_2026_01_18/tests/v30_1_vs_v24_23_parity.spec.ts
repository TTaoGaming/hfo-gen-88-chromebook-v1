// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * GOLDEN MASTER PARITY TEST: v24.23 vs v30.1
 * Purpose: Replays v24.23 telemetry against v30.1
 * to verify coordinate parity and FSM state alignment on PORT 8889.
 */

const V23_URL = 'http://127.0.0.1:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_23.html';
const V30_URL = 'http://127.0.0.1:8889/active_omega.html';
const TELEMETRY_PATH = path.join(__dirname, '../test-results/golden_telemetry_v24_23.jsonl');

test.describe.configure({ mode: 'serial' });

test.describe('HFO Parity: Golden Master (v24.23) vs Candidate (v30.1)', () => {

    test('Step 1: Record Golden Telemetry from v24.23', async ({ page }) => {
        console.log('⏺️ Recording Baseline from v24.23...');
        await page.goto(V23_URL);

        // Wait for P1Bridger to be ready
        await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

        const telemetry = await page.evaluate(async () => {
            const results = [];
            const createHand = (x, y) => {
                const landmarks = [];
                for (let i = 0; i < 21; i++) {
                    landmarks.push({ x: x + i * 0.001, y: y + i * 0.001, z: 0 });
                }
                // Landmarks 0, 5, 17 are used for palm calculation
                landmarks[0] = { x: x, y: y, z: 0 };
                landmarks[5] = { x: x + 0.05, y: y, z: 0 };
                landmarks[17] = { x: x, y: y + 0.05, z: 0 };
                // Landmark 8 is the index tip
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: 0 };
                return landmarks;
            };

            for (let i = 0; i < 50; i++) {
                const x = 0.5 + Math.sin(i * 0.1) * 0.2;
                const y = 0.5 + Math.cos(i * 0.1) * 0.2;

                const landmarks = createHand(x, y);
                // Frame 25-50: BACK OF HAND (Flip palm vector)
                if (i >= 25) {
                    const temp = landmarks[5];
                    landmarks[5] = landmarks[17];
                    landmarks[17] = temp;
                }

                const mockResults = {
                    landmarks: [landmarks],
                    gestures: [[{ categoryName: 'Pointing_Up', score: 0.99 }]],
                    handedness: [[{ categoryName: 'Right' }]]
                };

                // @ts-ignore
                const cursors = P1Bridger.fuse(mockResults, 16.6);
                results.push({ frame: i, cursors });
            }
            return results;
        });

        fs.mkdirSync(path.dirname(TELEMETRY_PATH), { recursive: true });
        fs.writeFileSync(TELEMETRY_PATH, telemetry.map(t => JSON.stringify(t)).join('\n'));
        console.log(`✅ Recorded ${telemetry.length} frames.`);
    });

    test('Step 2: Compare Parity with v30.1', async ({ page }) => {
        const telemetry = fs.readFileSync(TELEMETRY_PATH, 'utf-8')
            .split('\n')
            .filter(l => l)
            .map(l => JSON.parse(l));

        console.log('▶️ Comparing against v30.1...');
        await page.goto(V30_URL);
        await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

        for (const frame of telemetry) {
            const x = 0.5 + Math.sin(frame.frame * 0.1) * 0.2;
            const y = 0.5 + Math.cos(frame.frame * 0.1) * 0.2;

            const createHand = (x, y) => {
                const landmarks = [];
                for (let i = 0; i < 21; i++) {
                    landmarks.push({ x: x + i * 0.001, y: y + i * 0.001, z: 0 });
                }
                landmarks[0] = { x: x, y: y, z: 0 };
                landmarks[5] = { x: x + 0.05, y: y, z: 0 };
                landmarks[17] = { x: x, y: y + 0.05, z: 0 };
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: 0 };
                return landmarks;
            };

            const landmarks = createHand(x, y);
            if (frame.frame >= 25) {
                const temp = landmarks[5];
                landmarks[5] = landmarks[17];
                landmarks[17] = temp;
            }

            const mockResults = {
                landmarks: [landmarks],
                gestures: [[{ categoryName: 'Pointing_Up', score: 0.99 }]],
                handedness: [[{ categoryName: 'Right' }]]
            };

            const candidateCursors = await page.evaluate((res) => {
                // @ts-ignore
                return P1Bridger.fuse(res, 16.6);
            }, mockResults);

            const golden = frame.cursors[0];
            const candidate = candidateCursors[0];

            if (golden && candidate) {
                if (frame.frame === 0) {
                    console.log(`Frame 0 State - Golden: ${golden.fsmState}, Candidate: ${candidate.fsmState}`);
                }
                // We expect coordinate parity (within epsilon)
                // Note: v30 might have different screen scaling, but unit coords (0-1) should match
                expect(candidate.screenX).toBeCloseTo(golden.screenX, 2);
                expect(candidate.screenY).toBeCloseTo(golden.screenY, 2);

                // FSM parity is critical
                expect(candidate.fsmState).toBe(golden.fsmState);
            }
        }
        console.log('🏁 Parity Audit PASS.');
    });
});
