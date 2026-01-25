// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'path';
import { readFile } from 'fs/promises';
import { safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { buildStepsFromFrames } from './gen6_v23_red_helpers';

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN6_V23_2_URL =
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_2.html'
    + '?flag-disable-camera=true'
    + '&flag-engine-babylon=true'
    + '&flag-engine-canvas=false'
    + '&flag-ui-excalidraw=false'
    + '&flag-ui-lil-gui=false'
    + '&flag-p3-injector=false'
    + '&flag-p2-sword-meter=true'
    + '&flag-p2-sword-vfx=true'
    + '&mode=dev';

type Golden = {
    golden_id: string;
    artifact: string;
    expect: {
        hasBabylonLayer: boolean;
        locked: { locked: boolean; minMeter01: number };
        drained: { locked: boolean; maxMeter01: number };
    };
};

test('Gen6 v23.2 GOLDEN: COMMIT_THUMBS_DOWN drains/unlocks sword meter after lock', async ({ hfoPage }) => {
    const goldenPath = path.join(__dirname, 'golden', 'omega_gen6_v23_2_sword_thumbs_down_drain_golden.json');
    const golden = JSON.parse(await readFile(goldenPath, 'utf-8')) as Golden;

    await safeGoto(hfoPage, GEN6_V23_2_URL);
    await hfoPage.waitForTimeout(750);
    await hfoPage.initHFO();
    await hfoPage.waitForTimeout(250);

    const frames = [
        // Baseline.
        ...Array.from({ length: 4 }, (_, i) => ({ now: 1000 + i * 50, dt: 50, fsmState: 'READY' as const, gesture: 'None', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
        // Lock.
        ...Array.from({ length: 16 }, (_, i) => ({ now: 1200 + i * 50, dt: 50, fsmState: 'COMMIT' as const, gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
        // Drain.
        ...Array.from({ length: 20 }, (_, i) => ({ now: 2000 + i * 50, dt: 50, fsmState: 'COMMIT' as const, gesture: 'Thumb_Down', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
    ];

    const steps = buildStepsFromFrames(frames);

    const out = await safeEvaluate(hfoPage, (payload: { steps: Array<{ now: number; dt: number; dataFabric: any }> }) => {
        const w = window as any;
        const state = w.systemState;

        const getBabylonLayer = () => {
            const layers = state?.ui?.juiceLayers || [];
            return layers.find((l: any) => l && l.scene && l.engine && l.canvas && typeof l.updateSwordVfx === 'function') || null;
        };

        const snapAt = (label: string) => {
            const sword = state?.p2?.swordMeter || state?.p2?.sword || null;
            const layer = getBabylonLayer();
            return {
                label,
                sword: {
                    meter01: Number(sword?.meter01 ?? 0),
                    locked: !!sword?.locked,
                    lastCommitVariant: String(sword?.lastCommitVariant ?? ''),
                },
                babylon: {
                    hasLayer: !!layer,
                },
            };
        };

        const lockIndex = 4 + 16 - 1;
        const drainIndex = 4 + 16 + 20 - 1;

        let locked: any = null;
        let drained: any = null;

        for (let i = 0; i < payload.steps.length; i++) {
            const s = payload.steps[i];
            try {
                state.dataFabric = s.dataFabric;
                w.hfoP2CommitVariantsThread?.tick?.({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric });
                w.hfoP2SwordMeterThread?.tick?.({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric });

                const layer = getBabylonLayer();
                if (layer?.update) {
                    layer.update(state.dataFabric.cursors || []);
                }
            } catch {
                // ignore
            }

            if (i === lockIndex) locked = snapAt('locked');
            if (i === drainIndex) drained = snapAt('drained');
        }

        return { locked, drained };
    }, { steps });

    expect(out.locked?.babylon?.hasLayer, 'Expected a Babylon layer to exist (engine-babylon=true).').toBe(golden.expect.hasBabylonLayer);
    expect(Boolean(out.locked?.sword?.locked)).toBe(golden.expect.locked.locked);
    expect(Number(out.locked?.sword?.meter01)).toBeGreaterThanOrEqual(golden.expect.locked.minMeter01);

    // Ensure the lock path is being attributed to the correct commit variant.
    expect(String(out.locked?.sword?.lastCommitVariant)).toBe('COMMIT_THUMBS_UP');

    expect(Boolean(out.drained?.sword?.locked)).toBe(golden.expect.drained.locked);
    expect(Number(out.drained?.sword?.meter01)).toBeLessThanOrEqual(golden.expect.drained.maxMeter01);
    expect(String(out.drained?.sword?.lastCommitVariant)).toBe('COMMIT_THUMBS_DOWN');
});
