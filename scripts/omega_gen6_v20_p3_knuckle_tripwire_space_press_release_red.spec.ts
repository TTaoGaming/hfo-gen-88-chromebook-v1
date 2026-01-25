// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V20_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV2Schema } from '../contracts/hfo_tripwire_events.zod';

// TDD (intentionally RED): v20 requires Space keydown on begin and Space keyup on end for knuckle tripwire.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V20_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector-knuckle=true'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-p3-tripwire-injector-static=false'
    + '&flag-ui-knuckle-tripwire-panel=false';

const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v20 (TDD RED): P3 maps knuckle begin/end → Space keydown/keyup', async ({ hfoPage }) => {
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

        try {
            w.hfoP3PlanckSensorInjector?.start?.();
        } catch {
            // ignore
        }

        const captured: Array<{ port: string; type: string; payload: any }> = [];
        const unsubscribe = w.hfoPortsEffects.subscribe((entry: any) => {
            if (entry?.port !== 'p3') return;
            captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
        }, 'p3');

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

            // Keep deadman state in sync (defense-in-depth). Injector subscription is event-driven.
            try {
                w.hfoP3PlanckSensorInjector?.tick?.({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
            } catch {
                // ignore
            }
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

    const injects = out.captured.filter((e: any) => e?.type === 'tripwire_inject');

    expect(injects.length, `Expected >=1 tripwire_inject; got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);

    // Validate payload shape (V2 supports keydown/keyup). This should stay GREEN even while action semantics are RED.
    for (const e of injects) {
        const parsed = P3TripwireInjectV2Schema.safeParse(e.payload);
        expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
    }

    // RED until P3 supports phase=end and action=keydown/keyup for knuckle.
    const actions = injects.map((e: any) => String(e?.payload?.payload?.action || '')).filter(Boolean);
    expect(actions, `Expected keydown+keyup; got=${JSON.stringify(injects)}`).toEqual(['keydown', 'keyup']);
});
