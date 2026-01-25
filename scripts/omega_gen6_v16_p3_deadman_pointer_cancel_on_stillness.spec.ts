// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V16_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// Desired behavior: fail-closed deadman cancels P3 tripwire injection eligibility
// if a COMMIT pointer remains perfectly still longer than the configured timeout.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V16_TEST_URL_LIGHT}&flag-p3-tripwire-injector=true&flag-p3-dino-ready-edge=false`;

const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v16_p3_deadman_commit_still_golden.jsonl';

test('Gen6 v16: COAST deadman forces COAST + emits pointer_cancel on stillness', async ({ hfoPage }) => {
    const frames = fs
        .readFileSync(GOLDEN_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));
    expect(frames.length).toBeGreaterThanOrEqual(3);

    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(
        hfoPage,
        (framesIn) => {
            const w = window as any;
            if (!w.systemState) throw new Error('missing systemState');
            if (!w.hfoP2CoastGovernor?.tick) throw new Error('missing hfoP2CoastGovernor.tick');

            // Make the test fast: use the replay timebase (frame.now) and a short timeout.
            w.systemState.parameters.coasting.deadman = {
                ...(w.systemState.parameters.coasting.deadman || {}),
                enabled: true,
                timeoutMs: 500,
                epsilonUiNorm: 0,
                rearmOnMove: true,
            };

            const captured: Array<{ port: string; type: string; payload: any }> = [];
            const unsubscribe = w.hfoPortsEffects?.subscribe
                ? w.hfoPortsEffects.subscribe((entry: any) => {
                    if (entry?.port === 'p3') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
                })
                : null;

            const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };
            for (const f of framesIn) {
                dataFabric.frameId++;
                dataFabric.systemTime = Number(f?.now || 0);
                dataFabric.cursors = [
                    {
                        ...f.cursor,
                        seq: f?.seq,
                        normX: f.cursor?.uiNormX,
                        normY: f.cursor?.uiNormY,
                    },
                ];
                w.hfoP2CoastGovernor.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
            }

            if (typeof unsubscribe === 'function') {
                try {
                    unsubscribe();
                } catch {
                    // ignore
                }
            }

            return {
                captured,
                deadman: w.hfoP2CoastGovernor?._debug?.() || null,
                finalCursor: dataFabric.cursors?.[0] || null,
            };
        },
        frames,
    );

    const cancels = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'pointer_cancel');
    expect(cancels.length, `Expected pointer_cancel; deadman=${JSON.stringify(out.deadman)}`).toBeGreaterThanOrEqual(1);

    const payload = cancels[0]?.payload || {};
    expect(String(payload.reason || '')).toBe('deadman_stillness');
    expect(Number(payload.pointerId || 0)).toBe(10);
    expect(Number(payload.timeoutMs || 0)).toBe(500);
    expect(String(out.finalCursor?.fsmState || '')).toBe('COAST');
});
