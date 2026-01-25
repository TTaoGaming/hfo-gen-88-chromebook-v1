// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import path from 'path';
import { readFile } from 'fs/promises';
import { safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { buildStepsFromFrames } from './gen6_v23_red_helpers';

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN6_V23_1_URL =
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_1.html'
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
        charge: { meter01: number; locked: boolean; swordRootEnabled: boolean };
        locked: { meter01: number; locked: boolean; swordRootEnabled: boolean };
        postMove: { locked: boolean; swordRootEnabled: boolean };
        babylonMarker: { meshName: string };
    };
};

function round3(n: unknown): number {
    const x = Number(n);
    if (!Number.isFinite(x)) return NaN;
    return Math.round(x * 1000) / 1000;
}

test('Gen6 v23.1 GOLDEN: COMMIT_THUMBS_UP charges + locks Babylon sword; remains locked across IDLE/READY moves', async ({ hfoPage }) => {
    const goldenPath = path.join(__dirname, 'golden', 'omega_gen6_v23_1_sword_babylon_golden.json');
    const golden = JSON.parse(await readFile(goldenPath, 'utf-8')) as Golden;

    await safeGoto(hfoPage, GEN6_V23_1_URL);
    await hfoPage.waitForTimeout(750);

    const frames = [
        // Establish baseline.
        ...Array.from({ length: 4 }, (_, i) => ({ now: 1000 + i * 50, dt: 50, fsmState: 'READY' as const, gesture: 'None', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
        // "COMMIT_THUMBS_UP": in real camera flows, Thumb_Up can coincide with COMMIT.
        ...Array.from({ length: 16 }, (_, i) => ({ now: 1200 + i * 50, dt: 50, fsmState: 'COMMIT' as const, gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
        // Move cursor while IDLE: sword should remain locked and follow marker updates.
        ...Array.from({ length: 6 }, (_, i) => ({ now: 2000 + i * 50, dt: 50, fsmState: 'IDLE' as const, gesture: 'None', confidence: 0.99, isPalmFacing: true, uiNormX: 0.25 + i * 0.08, uiNormY: 0.45 })),
        // Move cursor while READY.
        ...Array.from({ length: 6 }, (_, i) => ({ now: 2400 + i * 50, dt: 50, fsmState: 'READY' as const, gesture: 'None', confidence: 0.99, isPalmFacing: true, uiNormX: 0.75 - i * 0.06, uiNormY: 0.6 })),
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
            const marker = w.__hfoSwordTouch2dMarker ?? null;
            const babylonMarker = w.__hfoSwordBabylonMarker ?? null;
            const sword = state?.p2?.swordMeter || state?.p2?.sword || null;
            const layer = getBabylonLayer();
            const vfx = layer?.swordVfx ?? null;

            return {
                label,
                sword: {
                    meter01: Number(sword?.meter01 ?? 0),
                    locked: !!sword?.locked,
                    active: !!sword?.active,
                },
                markers: {
                    touch2d: marker,
                    babylon: babylonMarker,
                },
                babylon: {
                    hasLayer: !!layer,
                    canvasDisplay: String(layer?.canvas?.style?.display ?? ''),
                    swordVfxCreated: !!vfx,
                    swordRootEnabled: !!vfx?.root?.isEnabled?.(),
                    sheathStarted: !!vfx?.sheath?.isStarted?.(),
                    sheathEmitRate: Number(vfx?.sheath?.emitRate ?? 0),
                },
            };
        };

        const chargeIndex = 4 + 6 - 1; // after 6 Thumb_Up ticks
        const lockIndex = 4 + 16 - 1; // after full dwell

        let charge: any = null;
        let locked: any = null;

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

            if (i === chargeIndex) charge = snapAt('charge');
            if (i === lockIndex) locked = snapAt('locked');
        }

        const postMove = snapAt('postMove');

        return { charge, locked, postMove };
    }, { steps });

    expect(out.charge?.babylon?.hasLayer, 'Expected a Babylon layer to exist (engine-babylon=true).').toBe(true);
    expect(out.locked?.babylon?.hasLayer, 'Expected a Babylon layer to exist (engine-babylon=true).').toBe(true);

    // Charge phase: sword should be visible (meter > 0) even before lock.
    expect(round3(out.charge?.sword?.meter01)).toBeCloseTo(golden.expect.charge.meter01, 3);
    expect(out.charge?.sword?.locked).toBe(golden.expect.charge.locked);
    expect(out.charge?.babylon?.swordRootEnabled).toBe(golden.expect.charge.swordRootEnabled);

    // Locked phase: sword locks at (or clamped to) 1.0 and should remain visible.
    expect(round3(out.locked?.sword?.meter01)).toBeCloseTo(golden.expect.locked.meter01, 3);
    expect(out.locked?.sword?.locked).toBe(golden.expect.locked.locked);
    expect(out.locked?.babylon?.swordRootEnabled).toBe(golden.expect.locked.swordRootEnabled);

    // Persistence phase: after movement across IDLE/READY, lock remains.
    expect(out.postMove?.sword?.locked).toBe(golden.expect.postMove.locked);
    expect(out.postMove?.babylon?.swordRootEnabled).toBe(golden.expect.postMove.swordRootEnabled);

    // Marker contract stays stable.
    expect(out.postMove?.markers?.babylon?.meshName).toBe(golden.expect.babylonMarker.meshName);
});
