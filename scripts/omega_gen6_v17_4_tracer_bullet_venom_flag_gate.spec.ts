// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_4_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17.4: tracer_bullet_venom is fail-closed behind OpenFeature flag', async ({ hfoPage }) => {
    const base = `${GEN6_V17_4_TEST_URL_LIGHT}`
        + '&flag-engine-babylon=false'
        + '&flag-engine-canvas=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-p3-injector=false'
        + '&test-run=tracer_flag_gate';

    const runOnce = async (enabled: boolean) => {
        const url = base + `&flag-p3-tracer-bullet-venom=${enabled ? 'true' : 'false'}`;
        await safeGoto(hfoPage, url);
        await hfoPage.waitForTimeout(250);

        return safeEvaluate(
            hfoPage,
            (args) => {
                const w = window as any;
                if (!w.hfoPortsEffects?.clear) throw new Error('missing hfoPortsEffects.clear');
                if (!w.hfoPortsEffects?.getRecent) throw new Error('missing hfoPortsEffects.getRecent');
                if (!w.hfoRegistry?.resolve) throw new Error('missing hfoRegistry.resolve');
                if (!w.hfoTokens?.P3_INJECTOR) throw new Error('missing hfoTokens.P3_INJECTOR');
                if (!w.hfoState?.ui) throw new Error('missing hfoState.ui');

                // Force deterministic queue branch.
                w.hfoState.ui.dinoWrapperIframe = null;
                w.hfoState.ui.dinoPendingNematocystPayloads = [];

                try { w.hfoPortsEffects.clear(); } catch { /* ignore */ }

                const injector = w.hfoRegistry.resolve(w.hfoTokens.P3_INJECTOR);
                const ok = injector.sendNematocystToDino({
                    kind: 'tracer_bullet_venom',
                    traceId: 'tb_v17_4_gate_001',
                    targetId: 'p3.injector',
                    reason: 'spec_tracer_gate',
                    handIndex: 0,
                    pointerId: 10,
                    readiness: 0.95,
                });

                const queued = (w.hfoState.ui.dinoPendingNematocystPayloads || []) as any[];
                const recent = w.hfoPortsEffects.getRecent(250) || [];
                const suppressed = recent.filter((e: any) => e?.port === 'p3' && e?.type === 'tracer_venom_suppressed');

                return {
                    enabled: Boolean(args.enabled),
                    ok: Boolean(ok),
                    queuedLen: queued.length,
                    queuedLast: queued[queued.length - 1] ?? null,
                    suppressedCount: suppressed.length,
                };
            },
            { enabled },
        );
    };

    const disabled = await runOnce(false);
    expect(disabled.suppressedCount).toBeGreaterThanOrEqual(1);
    expect(disabled.queuedLen).toBe(0);

    const enabled = await runOnce(true);
    expect(enabled.suppressedCount).toBe(0);
    expect(enabled.queuedLen).toBeGreaterThanOrEqual(1);
    expect(enabled.queuedLast?.kind).toBe('keyboard');
    expect(enabled.queuedLast?.code).toBe('Space');
    expect(enabled.queuedLast?.traceId).toBe('tb_v17_4_gate_001');
});
