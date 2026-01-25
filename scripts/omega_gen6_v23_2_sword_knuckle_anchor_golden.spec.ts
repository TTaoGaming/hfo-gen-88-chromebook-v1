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
    + '&flag-engine-babylon=false'
    + '&flag-engine-canvas=false'
    + '&flag-ui-excalidraw=false'
    + '&flag-ui-lil-gui=false'
    + '&flag-p3-injector=false'
    + '&flag-p2-sword-meter=true'
    + '&flag-p2-sword-vfx=false'
    + '&flag-p2-sword-marker-live-landmarks=true'
    + '&mode=dev';

type Golden = {
    golden_id: string;
    artifact: string;
    expect: {
        hasBabylonLayer: boolean;
        marker: {
            endpointPinkyUiNorm: { x: number; y: number };
            endpointIndexUiNorm: { x: number; y: number };
        };
        locked: { locked: boolean };
        babylonMarker: { meshName: string };
    };
};

type Landmark = { x: number; y: number; z?: number };

function makeLandmarks(pairs: Record<number, Landmark>): Array<{ x: number; y: number; z: number }> {
    const maxIdx = Math.max(21, ...Object.keys(pairs).map((k) => Number(k)));
    const lms = Array.from({ length: maxIdx + 1 }, () => ({ x: 0.5, y: 0.5, z: 0 }));
    for (const [k, v] of Object.entries(pairs)) {
        lms[Number(k)] = { x: v.x, y: v.y, z: v.z ?? 0 };
    }
    return lms;
}

test('Gen6 v23.2 GOLDEN: knuckle trip-lane (17→5) anchors sword marker; COMMIT_THUMBS_UP locks sword', async ({ hfoPage }) => {
    const goldenPath = path.join(__dirname, 'golden', 'omega_gen6_v23_2_sword_knuckle_anchor_golden.json');
    const golden = JSON.parse(await readFile(goldenPath, 'utf-8')) as Golden;

    await safeGoto(hfoPage, GEN6_V23_2_URL);
    await hfoPage.waitForTimeout(750);
    await hfoPage.initHFO();
    await hfoPage.waitForTimeout(250);

    const expectedPinky = golden.expect.marker.endpointPinkyUiNorm;
    const expectedIndex = golden.expect.marker.endpointIndexUiNorm;

    const landmarks = makeLandmarks({
        17: { x: expectedPinky.x, y: expectedPinky.y, z: 0 },
        5: { x: expectedIndex.x, y: expectedIndex.y, z: 0 },
    });

    const frames = [
        // Establish baseline.
        ...Array.from({ length: 4 }, (_, i) => ({ now: 1000 + i * 50, dt: 50, fsmState: 'READY' as const, gesture: 'None', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
        // "COMMIT_THUMBS_UP": in real camera flows, Thumb_Up can coincide with COMMIT.
        ...Array.from({ length: 16 }, (_, i) => ({ now: 1200 + i * 50, dt: 50, fsmState: 'COMMIT' as const, gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true, uiNormX: 0.55, uiNormY: 0.55 })),
    ];

    const steps = buildStepsFromFrames(frames);

    const out = await safeEvaluate(hfoPage, (payload: { steps: Array<{ now: number; dt: number; dataFabric: any }>; landmarks: any[] }) => {
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
                    locked: !!sword?.locked,
                    meter01: Number(sword?.meter01 ?? 0),
                },
                markers: {
                    touch2d: marker,
                    babylon: babylonMarker,
                },
                babylon: {
                    hasLayer: !!layer,
                    swordRootEnabled: !!vfx?.root?.isEnabled?.(),
                },
            };
        };

        const lockIndex = 4 + 16 - 1;
        let locked: any = null;

        for (let i = 0; i < payload.steps.length; i++) {
            const s = payload.steps[i];
            try {
                // Add landmarks after contract parse (landmarks are optional and omitted by default in builders).
                const cursors = s.dataFabric?.cursors || [];
                if (cursors[0]) {
                    cursors[0].landmarks = Array.isArray(payload.landmarks) ? payload.landmarks.map((p: any) => ({ ...p })) : [];
                }

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
        }

        return { locked };
    }, { steps, landmarks });

    expect(out.locked?.babylon?.hasLayer, 'Expected a Babylon layer to exist (engine-babylon=true).').toBe(golden.expect.hasBabylonLayer);
    expect(out.locked?.sword?.locked).toBe(golden.expect.locked.locked);
    expect(out.locked?.markers?.babylon?.meshName).toBe(golden.expect.babylonMarker.meshName);

    // v23.2: marker should use knuckle trip-lane endpoints when landmarks are present.
    expect(out.locked?.markers?.touch2d?.endpointPinkyUiNorm?.x).toBeCloseTo(expectedPinky.x, 4);
    expect(out.locked?.markers?.touch2d?.endpointPinkyUiNorm?.y).toBeCloseTo(expectedPinky.y, 4);
    expect(out.locked?.markers?.touch2d?.endpointIndexUiNorm?.x).toBeCloseTo(expectedIndex.x, 4);
    expect(out.locked?.markers?.touch2d?.endpointIndexUiNorm?.y).toBeCloseTo(expectedIndex.y, 4);
});
