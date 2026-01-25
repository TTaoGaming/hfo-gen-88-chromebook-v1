// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { P3TripwireInjectV1Schema } from '../contracts/hfo_tripwire_events.zod';
import { GEN6_V17_1_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_1_TEST_URL_LIGHT}`
    + '&flag-p3-tripwire-injector=true'
    + '&flag-p3-dino-ready-edge=false'
    + '&flag-p2-tripwire-contact-only=false';

const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_1_tripwire_downcross_8pulse_golden.jsonl';

test('Gen6 v17.1: golden 8 down-cross pulses → 8 p3/tripwire_inject (Space)', async ({ hfoPage }) => {
    const frames = fs
        .readFileSync(GOLDEN_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));

    expect(frames.length).toBe(16);

    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, (framesIn) => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');

        const captured: Array<{ port: string; type: string; payload: any }> = [];
        const unsubscribe = w.hfoPortsEffects?.subscribe
            ? w.hfoPortsEffects.subscribe((entry: any) => {
                if (entry?.port === 'p2' || entry?.port === 'p3') {
                    captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
                }
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

            w.hfoP2TripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
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
            p2Debug: w.hfoP2TripwireThread?.getDebugState?.() || null,
            p3Last: w.hfoP3PlanckSensorInjector?.getLastInject?.() || null,
        };
    }, frames);

    const crosses = out.captured.filter((e: any) => e?.port === 'p2' && e?.type === 'tripwire_cross');
    expect(crosses.length).toBeGreaterThanOrEqual(8);

    const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');
    expect(injects.length, `Expected 8 p3/tripwire_inject; p3Last=${JSON.stringify(out.p3Last)} p2Debug=${JSON.stringify(out.p2Debug)}`).toBe(8);

    for (const ev of injects) {
        const parsed = P3TripwireInjectV1Schema.safeParse(ev.payload);
        expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
        expect(String(ev.payload?.adapterId || '')).toBe('dino-v1');
        expect(String(ev.payload?.direction || '')).toBe('down');
        expect(String(ev.payload?.payload?.code || '')).toBe('Space');
    }
});
