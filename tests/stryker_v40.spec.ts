// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * STRYKER FAST AUDIT: V40.1
 * Purpose: Pre-loaded parity test for high-speed mutation scoring.
 */

const V40_1_PATH = path.resolve(process.cwd(), 'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v40_1.html');
const TELEMETRY_PATH = path.resolve(process.cwd(), 'tests/data/golden_telemetry_v24_23.jsonl');

test('Stryker Fast Parity Audit', async ({ page }) => {
    // Load pre-recorded telemetry
    if (!fs.existsSync(TELEMETRY_PATH)) {
        throw new Error('Telemetry baseline missing! Run parity test recording first.');
    }
    const telemetry = fs.readFileSync(TELEMETRY_PATH, 'utf-8')
        .split('\n')
        .filter(l => l)
        .map(l => JSON.parse(l));

    await page.goto(`file://${V40_1_PATH}`);
    await page.waitForFunction(() => typeof (window as any).P1Bridger !== 'undefined', { timeout: 10000 });

    for (const frame of telemetry) {
        // Reconstruct mock results matching the recorded frame
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
            expect(candidate.fsmState).toBe(golden.fsmState);
            expect(candidate.screenX).toBeCloseTo(golden.screenX, 2);
        }
    }
});
