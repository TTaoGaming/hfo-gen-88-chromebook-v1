// Medallion: Bronze | Mutation: 0% | HIVE: V
// 🧪 V24.3 Production Readiness Suite

const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('HFO V24.3 Ballistic Logic (Hardened)', () => {
    let consoleErrors = [];

    test.beforeEach(async ({ page }) => {
        consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
                console.error(`🚨 Browser Error: ${msg.text()}`);
            }
        });

        const filePath = 'file://' + path.resolve(__dirname, '../hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_3.html');
        await page.goto(filePath);

        // Wait for potential async init
        await page.waitForLoadState('networkidle');
        await page.waitForFunction(() => typeof systemState !== 'undefined', { timeout: 10000 });
    });

    test('should have no syntax errors and correct metadata', async ({ page }) => {
        expect(consoleErrors).toHaveLength(0);
        const title = await page.title();
        expect(title.toUpperCase()).toContain('V24.3');
    });

    test('PlanckPhysicsAdapter: Ballistic Interface Verification', async ({ page }) => {
        const result = await page.evaluate(() => {
            const adapter = new PlanckPhysicsAdapter();
            const hasMethod = typeof adapter.setBallistic === 'function';
            const bodyLinearDamping = adapter.cursor.getLinearDamping();
            return { hasMethod, bodyLinearDamping };
        });
        expect(result.hasMethod).toBe(true);
        expect(result.bodyLinearDamping).toBe(2.0);
    });

    test('P1Bridger: Triple Flow FSM Transition Validation', async ({ page }) => {
        const sequence = await page.evaluate(async () => {
            const results = [];
            const dt = 16.6;

            // 1. Reset to IDLE
            systemState.p1.fsmStates[0] = 'IDLE';
            systemState.p1.buckets[0] = 0;
            results.push({ phase: 'IDLE', state: systemState.p1.fsmStates[0] });

            // 2. Charge to READY (Simulate multiple frames)
            const mockLM = Array(21).fill({ x: 0.5, y: 0.5, z: 0.1 });
            for (let i = 0; i < 30; i++) {
                P1Bridger.fuse({ landmarks: [mockLM], gestures: [[{ categoryName: 'None', score: 0.9 }]] }, dt);
            }
            results.push({ phase: 'CHARGE', state: systemState.p1.fsmStates[0], bucket: Math.round(systemState.p1.buckets[0]) });

            // 3. COMMIT (Point)
            P1Bridger.fuse({ landmarks: [mockLM], gestures: [[{ categoryName: 'Pointing_Up', score: 0.95 }]] }, dt);
            results.push({ phase: 'COMMIT', state: systemState.p1.fsmStates[0] });

            // 4. COAST (Drop confidence)
            P1Bridger.fuse({ landmarks: [mockLM], gestures: [[{ categoryName: 'Pointing_Up', score: 0.1 }]] }, dt);
            results.push({ phase: 'COAST', state: systemState.p1.fsmStates[0] });

            return results;
        });

        console.log("FSM Sequence Trace:");
        console.table(sequence);

        expect(sequence.find(s => s.phase === 'CHARGE').state).toBe('READY');
        expect(sequence.find(s => s.phase === 'COMMIT').state).toBe('COMMIT');
        expect(sequence.find(s => s.phase === 'COAST').state).toBe('COAST');
    });
});
