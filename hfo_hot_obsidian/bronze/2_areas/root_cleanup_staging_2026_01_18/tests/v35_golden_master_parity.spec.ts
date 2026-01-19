// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * GOLDEN MASTER PARITY TEST: v24.23 vs v35
 * Purpose: Replays v24.23 telemetry against v35
 * to verify coordinate parity and FSM state alignment on PORT 8889.
 */

const V23_URL = 'http://127.0.0.1:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_23.html?flag-chargeTimeMs=200';
const V30_URL = 'http://127.0.0.1:8889/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v40_1.html';
const TELEMETRY_PATH = path.resolve(process.cwd(), 'tests/data/golden_telemetry_v24_23.jsonl');

test.describe.configure({ mode: 'serial' });

test.describe('HFO Parity: Golden Master (v24.23) vs Candidate (v35)', () => {

    test('Step 1: Record Golden Telemetry from v24.23', async ({ page }) => {
        console.log('⏺️ Recording Baseline from v24.23...');
        await page.goto(V23_URL);

        // Wait for P1Bridger to be ready
        await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

        // 🛡️ Force Parity Parameters
        await page.evaluate(() => {
            const fsm = (window as any).systemState.parameters.fsm;
            fsm.chargeTimeMs = 200;
            fsm.hysteresisHigh = 88;
            (window as any).systemState.parameters.p0Active = false;
        });

        const telemetry = await page.evaluate(async () => {
            const results = [];
            const createHand = (x, y, z, palmScale) => {
                const landmarks = [];
                for (let i = 0; i < 21; i++) {
                    landmarks.push({ x: x + i * 0.001, y: y + i * 0.001, z: z });
                }
                // Landmarks 0, 5, 17 are used for palm calculation
                landmarks[0] = { x: x, y: y, z: z };
                landmarks[5] = { x: x + 0.05 * palmScale, y: y, z: z };
                landmarks[17] = { x: x, y: y + 0.05 * palmScale, z: z };
                // Landmark 8 is the index tip
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: z };
                return landmarks;
            };

            for (let i = 0; i < 100; i++) {
                const x = 0.5 + Math.sin(i * 0.1) * 0.2;
                const y = 0.5 + Math.cos(i * 0.1) * 0.2;
                const z = Math.sin(i * 0.05) * 0.2; // Variable Z
                const palmScale = 1.0 + Math.sin(i * 0.2) * 0.1; // Variable Palm Size

                const landmarks = createHand(x, y, z, palmScale);

                // Varied palm orientation
                if (i % 10 === 0) {
                    // Temporary flip
                    const temp = landmarks[5];
                    landmarks[5] = landmarks[17];
                    landmarks[17] = temp;
                }

                // Variable confidence to trigger FSM paths (READY -> COAST -> IDLE)
                let confidence = 0.99;
                if (i > 70 && i < 85) confidence = 0.1; // Trigger COAST

                const mockResults = {
                    landmarks: [landmarks],
                    gestures: [[{ categoryName: i < 50 ? 'Pointing_Up' : 'None', score: confidence }]],
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

    test('Step 2: Compare Parity with v35', async ({ page }) => {
        const telemetry = fs.readFileSync(TELEMETRY_PATH, 'utf-8')
            .split('\n')
            .filter(l => l)
            .map(l => JSON.parse(l));

        console.log('▶️ Comparing against v35...');
        await page.goto(V30_URL);
        await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

        // �️ Force Parity Parameters
        await page.evaluate(() => {
            const fsm = (window as any).systemState.parameters.fsm;
            fsm.chargeTimeMs = 200;
            fsm.hysteresisHigh = 88;
            (window as any).systemState.parameters.p0Active = false;
        });

        for (const frame of telemetry) {
            const i = frame.frame;
            const x = 0.5 + Math.sin(i * 0.1) * 0.2;
            const y = 0.5 + Math.cos(i * 0.1) * 0.2;
            const z = Math.sin(i * 0.05) * 0.2;
            const palmScale = 1.0 + Math.sin(i * 0.2) * 0.1;

            const createHand = (x, y, z, palmScale) => {
                const landmarks = [];
                for (let k = 0; k < 21; k++) {
                    landmarks.push({ x: x + k * 0.001, y: y + k * 0.001, z: z });
                }
                landmarks[0] = { x: x, y: y, z: z };
                landmarks[5] = { x: x + 0.05 * palmScale, y: y, z: z };
                landmarks[17] = { x: x, y: y + 0.05 * palmScale, z: z };
                landmarks[8] = { x: x + 0.02, y: y - 0.1, z: z };
                return landmarks;
            };

            const landmarks = createHand(x, y, z, palmScale);
            if (i % 10 === 0) {
                const temp = landmarks[5];
                landmarks[5] = landmarks[17];
                landmarks[17] = temp;
            }

            let confidence = 0.99;
            if (i > 70 && i < 85) confidence = 0.1;

            const mockResults = {
                landmarks: [landmarks],
                gestures: [[{ categoryName: i < 50 ? 'Pointing_Up' : 'None', score: confidence }]],
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

                try {
                    // FSM parity is critical
                    expect(candidate.fsmState).toBe(golden.fsmState);
                } catch (e) {
                    console.error(`❌ FSM mismatch at Frame ${frame.frame}: Golden=${golden.fsmState}, Candidate=${candidate.fsmState}`);
                    throw e;
                }

                // We expect coordinate parity (within epsilon)
                expect(candidate.screenX).toBeCloseTo(golden.screenX, 2);
            }
        }
        console.log('🏁 Parity Audit PASS.');
    });
});
