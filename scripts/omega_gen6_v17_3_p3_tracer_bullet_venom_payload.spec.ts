// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_3_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17.3: P3 accepts tracer_bullet_venom payload and maps to keyboard + traceId', async ({ hfoPage }) => {
    const url = `${GEN6_V17_3_TEST_URL_LIGHT}`
        + '&flag-engine-babylon=false'
        + '&flag-engine-canvas=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-p3-injector=false'
        + '&test-run=tracer_bullet_venom';

    await safeGoto(hfoPage, url);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(
        hfoPage,
        () => {
            const w = window as any;
            if (!w.hfoRegistry?.resolve) throw new Error('missing hfoRegistry.resolve');
            if (!w.hfoTokens?.P3_INJECTOR) throw new Error('missing hfoTokens.P3_INJECTOR');
            if (!w.hfoState?.ui) throw new Error('missing hfoState.ui');

            // Force the deterministic queue path: pretend the dino iframe is missing.
            w.hfoState.ui.dinoWrapperIframe = null;
            w.hfoState.ui.dinoPendingNematocystPayloads = [];

            const injector = w.hfoRegistry.resolve(w.hfoTokens.P3_INJECTOR);
            injector.sendNematocystToDino({
                kind: 'tracer_bullet_venom',
                traceId: 'tb_spec_v17_3_001',
                targetId: 'p3.injector',
                reason: 'spec_tracer_payload',
            });

            const queued = (w.hfoState.ui.dinoPendingNematocystPayloads || []) as any[];
            return { queuedLast: queued[queued.length - 1] ?? null };
        },
        undefined,
    );

    const payload = out.queuedLast;
    expect(payload, 'expected queued payload').toBeTruthy();
    expect(payload?.kind).toBe('keyboard');
    expect(payload?.code).toBe('Space');
    expect(payload?.traceId).toBe('tb_spec_v17_3_001');
});
