// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V21_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { KnuckleTripwireCrossV21Schema } from '../contracts/hfo_tripwire_events.zod';

// v21: confirm the golden master produces begin/end edges in COMMIT for the knuckle tripwire.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V21_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-p3-tripwire-injector-static=false'
    + '&flag-p3-tripwire-injector-knuckle=false'
    + '&flag-ui-knuckle-tripwire-panel=false';

const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v21: golden master drives knuckle tripwire begin/end (COMMIT only)', async ({ hfoPage }) => {
    const lines = fs
        .readFileSync(GOLDEN_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean);
    const frames = lines.map((l) => JSON.parse(l));
    expect(frames.length).toBeGreaterThanOrEqual(4);

    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, (framesIn) => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
        if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

        const captured: Array<{ port: string; type: string; payload: any }> = [];
        const unsubscribe = w.hfoPortsEffects.subscribe((entry: any) => {
            if (entry?.port !== 'p2') return;
            captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
        }, 'p2');

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
            w.hfoP2KnuckleTripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
        }

        if (typeof unsubscribe === 'function') {
            try {
                unsubscribe();
            } catch {
                // ignore
            }
        }

        return { captured };
    }, frames);

    const tripwire = out.captured.filter((e: any) => e?.type === 'tripwire_cross');
    const knuckle = tripwire.filter((e: any) => String(e?.payload?.sensorId || '') === 'knuckle');

    expect(knuckle.length, `Expected >=2 knuckle tripwire_cross events, got=${JSON.stringify(tripwire)}`).toBeGreaterThanOrEqual(2);

    const phases = knuckle.map((e: any) => String(e?.payload?.sensor?.phase || '')).filter(Boolean);
    expect(phases).toContain('begin');
    expect(phases).toContain('end');
    expect(phases.indexOf('begin')).toBeLessThan(phases.indexOf('end'));

    for (const e of knuckle) {
        const parsed = KnuckleTripwireCrossV21Schema.safeParse(e.payload);
        expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
        const p = parsed.success ? parsed.data : e.payload;
        expect(String(p?.fsmState || '')).toBe('COMMIT');
        expect(String(p?.sensorId || '')).toBe('knuckle');
        expect(String(p?.sensor?.engine || '')).toBe('knuckle');

        // v21: distance-based semantics should be present and finite.
        expect(Number.isFinite(p?.sensor?.distance?.featureDistanceUiNorm)).toBe(true);
        expect(Number.isFinite(p?.sensor?.distance?.barLenUiNorm)).toBe(true);
        expect(Number(p.sensor.distance.barLenUiNorm)).toBeGreaterThan(0);

        // v21: velocity/derivative metadata should be present and finite (future use).
        expect(Number.isFinite(p?.vxUiNormPerS)).toBe(true);
        expect(Number.isFinite(p?.vyUiNormPerS)).toBe(true);
        expect(Number.isFinite(p?.speedUiNormPerS)).toBe(true);
        expect(Number.isFinite(p?.sensor?.distance?.rawDistanceVelUiNormPerS)).toBe(true);
        expect(Number.isFinite(p?.sensor?.distance?.orientedDistanceVelUiNormPerS)).toBe(true);
        expect(Number.isFinite(p?.sensor?.distance?.featureDistanceVelUiNormPerS)).toBe(true);
    }
});
