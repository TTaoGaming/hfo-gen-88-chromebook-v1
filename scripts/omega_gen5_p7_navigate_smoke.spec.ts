// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v10_1.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Gen5 v10.1 P7 navigate: mission vision + safe parameter patch', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoPorts?.p7?.navigate) throw new Error('Ports.p7.navigate not available');

        // @ts-ignore
        const vision = window.hfoPorts.p7.navigate.getMissionVision();

        // Patch a couple parameters (should be safe even headless)
        // @ts-ignore
        const params = window.hfoPorts.p7.navigate.patchParameters({
            gestures: { minGestureConfidence: 0.55 },
            excalidraw: { activeTool: 'freedraw' }
        });

        // @ts-ignore
        const tool = window.hfoPorts.p7.navigate.setExcalidrawTool('freedraw');

        // @ts-ignore
        const intent = window.hfoPorts.p7.navigate.setIntent({
            mode: 'tool_virtualization',
            request: 'phoenix_core_fireball_fingertip'
        });

        return {
            vision,
            tool,
            minGestureConfidence: params?.gestures?.minGestureConfidence,
            intent
        };
    });

    expect(out?.vision?.mission_thread).toBe('OMEGA');
    expect(out?.vision?.title).toBeTruthy();
    expect(out?.vision?.north_star).toBeTruthy();

    expect(out?.minGestureConfidence).toBe(0.55);
    expect(out?.tool).toBe('freedraw');

    expect(out?.intent?.ts).toBeTruthy();
    expect(out?.intent?.intent?.mode).toBe('tool_virtualization');
});
