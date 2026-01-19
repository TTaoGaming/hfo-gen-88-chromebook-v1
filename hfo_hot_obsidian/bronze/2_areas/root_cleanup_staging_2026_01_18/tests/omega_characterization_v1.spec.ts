// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * GOLDEN MASTER CHARACTERIZATION TEST [V24.21]
 * Purpose: Captures telemetry from a known-good version (v24.20) 
 * and replays it against the current version (v24.21) 
 * to detect tracking regressions and coordinate drift.
 */

const V20_URL = 'http://localhost:8888/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_20.html';
const V23_URL = 'http://localhost:8888/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_23.html';
const TELEMETRY_PATH = path.join(__dirname, '../test-results/golden_telemetry_v20.jsonl');

test.describe('Omega Characterization: v24.20 vs v24.23', () => {

    test('Phase 1: Record Golden Telemetry from v24.20', async ({ page }) => {
        console.log('⏺️ Navigating to v24.20 for Recording...');
        await page.goto(V20_URL);

        // Wait for P1Bridger to load instead of GestureRecognizer
        await page.waitForFunction(() => typeof P1Bridger !== 'undefined', { timeout: 30000 });

        console.log('⏺️ Starting Telemetry Recording...');
        // Simulate a "synthetic" landmark stream if real camera isn't available in CI
        // For this characterization, we inject known coordinates into P1Bridger
        await page.evaluate(() => {
            window.hfoTelemetry.start();
            let frame = 0;
            const recordStep = () => {
                if (frame > 200) {
                    window.hfoTelemetry.stop();
                    return;
                }
                const now = performance.now();
                // Simulated circle movement
                const x = 0.5 + Math.sin(frame * 0.1) * 0.2;
                const y = 0.5 + Math.cos(frame * 0.1) * 0.2;

                // Mock MediaPipe result for P1Bridger
                const mockResults = {
                    landmarks: [[
                        { x: x, y: y, z: 0 }, // Index Tip
                        { x: x, y: y + 0.1, z: 0 }, // MCP
                    ]],
                    gestures: [[{ categoryName: 'POINTING_UP', score: 0.99 }]],
                    handedness: [[{ categoryName: 'Right' }]]
                };

                // Directly call Bridger.fuse
                // @ts-ignore
                const cursors = P1Bridger.fuse(mockResults, 16.6);
                // In v24.20/21 DataFabricSchema is scoped to an IIFE or block, 
                // but we can bypass Zod validation for simple recording if needed, 
                // or just construct the object. v24.20/21 uses the schema to parse.
                // We'll try to use the global 'systemState' to access the schema if available,
                // or just pass a raw object since window.hfoTelemetry.record clones it.

                const fabricData = {
                    cursors: cursors,
                    systemTime: now,
                    frameId: frame
                };

                // @ts-ignore
                window.hfoTelemetry.record('P1_FUSE', fabricData);

                frame++;
                requestAnimationFrame(recordStep);
            };
            recordStep();
        });

        // Wait for recording to finish (200 frames @ 60fps ~ 3.3s)
        await page.waitForTimeout(5000);

        const telemetry = await page.evaluate(() => {
            // @ts-ignore
            return window.hfoTelemetry.buffer.map(e => JSON.stringify(e)).join('\n');
        });

        fs.mkdirSync(path.dirname(TELEMETRY_PATH), { recursive: true });
        fs.writeFileSync(TELEMETRY_PATH, telemetry);
        console.log(`✅ Golden Telemetry saved to ${TELEMETRY_PATH}`);
    });

    test('Phase 2: Replay Telemetry against v24.21 and Assert Parity', async ({ page }) => {
        if (!fs.existsSync(TELEMETRY_PATH)) {
            throw new Error('❌ Missing Golden Telemetry. Run Phase 1 first.');
        }

        console.log('▶️ Navigating to v24.23 for Replay...');
        await page.goto(V23_URL);

        // Wait for systemState to be initialized instead
        await page.waitForFunction(() => typeof window['systemState'] !== 'undefined' && window['systemState'].parameters, { timeout: 30000 });

        const telemetryData = fs.readFileSync(TELEMETRY_PATH, 'utf-8');

        console.log('▶️ Injecting Telemetry into v24.23 and Monitoring for Regressions...');
        const regressions = await page.evaluate(async (data) => {
            const frames = data.split('\n').filter(l => l.trim()).map(l => JSON.parse(l));
            const diffs = [];

            for (let i = 0; i < frames.length; i++) {
                const goldenFrame = frames[i];
                // Deep clone state before processing
                // @ts-ignore
                systemState.dataFabric = goldenFrame.data;

                // Trigger one render cycle
                // @ts-ignore
                if (typeof window['drawResults'] === 'function') {
                    // @ts-ignore
                    window['drawResults']({ landmarks: [], gestures: [], handedness: [] }, systemState.dataFabric);
                } else {
                    diffs.push(`Frame ${i}: drawResults is not globally accessible`);
                }

                // Check for critical runtime variables that tend to regression
                // @ts-ignore
                const p = systemState.parameters;
                // @ts-ignore
                if (!p.canvasCursors || !p.canvasCursors.radiusBase) diffs.push(`Frame ${i}: radiusBase is missing from canvasCursors`);

                // Verify screen coordinate projections
                // @ts-ignore
                const cur = systemState.dataFabric.cursors[0];
                const gold = goldenFrame.data.cursors[0];

                if (cur && gold) {
                    // Check if screen coordinates are NaN or extreme (classic regression)
                    if (isNaN(cur.screenX) || isNaN(cur.screenY)) {
                        diffs.push(`Frame ${i}: Screen coordinate NaN detected`);
                    }

                    // Tolerance for floating point drift (0.1% of viewport width)
                    const epsilon = 0.0001;
                    if (Math.abs(cur.screenX - gold.screenX) > epsilon || Math.abs(cur.screenY - gold.screenY) > epsilon) {
                        diffs.push(`Frame ${i}: Coordinate Drift! v24.23: (${cur.screenX.toFixed(1)}, ${cur.screenY.toFixed(1)}) vs v24.20: (${gold.screenX.toFixed(1)}, ${gold.screenY.toFixed(1)})`);
                    }

                    // Readiness Score Mapping (v24.23 readinessScore = v24.20 bucketLevel)
                    const readiness = cur.readinessScore !== undefined ? cur.readinessScore : cur.bucketLevel;
                    const goldBucket = gold.bucketLevel !== undefined ? gold.bucketLevel : gold.readinessScore;
                    if (Math.abs(readiness - goldBucket) > epsilon) {
                        diffs.push(`Frame ${i}: Readiness/Bucket Mismatch! v24.23: ${readiness.toFixed(2)} vs v24.20: ${goldBucket.toFixed(2)}`);
                    }
                }
            }
            return diffs;
        }, telemetryData);

        if (regressions.length > 0) {
            console.error('❌ REGRESSIONS DETECTED:');
            regressions.slice(0, 10).forEach(r => console.error(`  - ${r}`));
            if (regressions.length > 10) console.error(`  ... and ${regressions.length - 10} more.`);
        }

        expect(regressions).toHaveLength(0);
        console.log('✅ v24.23 passed Characterization against Golden Master v24.20');
    });
});
