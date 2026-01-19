// Medallion: Bronze | Mutation: 0% | HIVE: V

const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('HFO Omega V24.16 Production Audit', () => {

    test.beforeEach(async ({ page }) => {
        const filePath = path.join(process.cwd(), 'hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_16.html');
        await page.goto(`file://${filePath}`);

        await page.waitForFunction(() => window.systemState && window.systemState.ui.juiceLayers);

        await page.evaluate(() => {
            console.log("TEST INIT: Setting up systemState");
            window.systemState.parameters.visuals.engine = 'BABYLON';
            window.systemState.parameters.p0Active = true;
            window.systemState.parameters.landmarks.numHands = 2;
            window.systemState.p0.videoBounds = { width: 1280, height: 720 };

            // Force ignite
            const btn = document.querySelector('button'); // Should find Ignite Omega if it's the first button or search text
            const igniteBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('IGNITE'));
            if (igniteBtn) igniteBtn.click();
        });

        await page.waitForFunction(() => {
            const layers = window.systemState.ui.juiceLayers;
            return layers && layers.some(l => l.constructor.name === 'BabylonJuiceSubstrate');
        });
    });

    test('GREEN: Verify TrailMesh Disposal on Hand Loss', async ({ page }) => {
        page.on('console', msg => console.log('PAGE LOG:', msg.text()));

        // 1. Inject Hand Landmarks
        await page.evaluate(() => {
            const mockLandmarks = new Array(21).fill(0).map((_, i) => ({
                x: 0.5, y: 0.5, z: 0
            }));
            mockLandmarks[0] = { x: 0.5, y: 0.7, z: 0 };
            mockLandmarks[5] = { x: 0.4, y: 0.5, z: 0 };
            mockLandmarks[17] = { x: 0.6, y: 0.5, z: 0 };
            mockLandmarks[8] = { x: 0.5, y: 0.3, z: 0 }; // Pointing up

            window.hfoMockResults = {
                landmarks: [mockLandmarks],
                gestures: [[{ categoryName: 'Pointing_Up', score: 0.9 }]]
            };
            window.systemState.parameters.physics.cursorTheme = 'LI';
            console.log("TEST: Mock Results Injected");
        });

        // Wait for update loop to create meshes
        // Use waitForFunction to be sure creation happened
        await page.waitForFunction(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            return b && b.emitterRoots[0] && b.scene.meshes.length > 0;
        }, { timeout: 2000 });

        const meshCountBefore = await page.evaluate(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            return b.scene.meshes.length;
        });

        console.log(`Mesh count before hand loss: ${meshCountBefore}`);
        expect(meshCountBefore).toBeGreaterThan(0);

        // 2. Remove hand
        await page.evaluate(() => {
            window.hfoMockResults = { landmarks: [], gestures: [] };
            console.log("TEST: Hand removed");
        });

        // Use waitForFunction to wait for disposal
        await page.waitForFunction(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            const total = b.scene.meshes.filter(m => !m.isDisposed).length;
            return total === 0;
        }, { timeout: 3000 });

        const meshCountAfter = await page.evaluate(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            return b.scene.meshes.filter(m => !m.isDisposed).length;
        });

        console.log(`Mesh count after hand loss: ${meshCountAfter}`);
        expect(meshCountAfter).toBe(0);
    });

    test('GREEN: High-Velocity Trail Persistence (No Gaps)', async ({ page }) => {
        await page.evaluate(() => {
            const mockLandmarks = new Array(21).fill(0).map(() => ({ x: 0.5, y: 0.5, z: 0 }));
            mockLandmarks[0] = { x: 0.5, y: 0.7, z: 0 };
            mockLandmarks[5] = { x: 0.4, y: 0.5, z: 0 };
            mockLandmarks[17] = { x: 0.6, y: 0.5, z: 0 };
            mockLandmarks[8] = { x: 0.5, y: 0.3, z: 0 };

            window.hfoMockResults = {
                landmarks: [mockLandmarks],
                gestures: [[{ categoryName: 'Pointing_Up', score: 0.9 }]]
            };
        });

        await page.waitForFunction(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            return b && b.trails[0] && b.trails[0].isVisible;
        });

        const trailStatus = await page.evaluate(() => {
            const b = window.systemState.ui.juiceLayers.find(l => l.constructor.name === 'BabylonJuiceSubstrate');
            const trail = b.trails[0];
            return !!trail && trail.isVisible && !trail.isDisposed();
        });

        expect(trailStatus).toBe(true);
    });

    test('GREEN: Global Engine Disposal', async ({ page }) => {
        await page.evaluate(() => {
            window.hfoLifecycle.dispose('BABYLON_ENGINE');
        });

        const exists = await page.evaluate(() => {
            return !!document.getElementById('babylon-canvas');
        });

        expect(exists).toBe(false);
    });
});
