// Medallion: Bronze | Mutation: 0% | HIVE: V
import path from 'node:path';
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_4_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17.4: P3 diagnostic battery probe (real adapter surfaces)', async ({ hfoPage }) => {
  const batteryPath = path.resolve(
    process.cwd(),
    'hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/lib/js/hfo_p3_diagnostic_battery_v1.js',
  );

  const runOnce = async (tag: string, extraParams: string) => {
    const url = `${GEN6_V17_4_TEST_URL_LIGHT}`
      + '&flag-p3-diagnostic-battery=true'
      + `&probe-tag=${encodeURIComponent(tag)}`
      + '&test-run=p3_diagnostic_battery_probe_v17_4'
      + (extraParams || '');

    await safeGoto(hfoPage, url);
    await hfoPage.addScriptTag({ path: batteryPath });

    return safeEvaluate(hfoPage, async () => {
      const w = window as any;
      if (!w.HFOP3DiagnosticBatteryV1?.create) throw new Error('missing HFOP3DiagnosticBatteryV1.create');

      const effects = w.hfoPortsEffects;
      const canGetRecent = !!effects?.getRecent;
      const canClear = !!effects?.clear;

      try { if (canClear) effects.clear(); } catch { /* ignore */ }

      const ui = w.hfoState?.ui;
      const before = {
        dinoWrapperIframePresent: !!ui?.dinoWrapperIframe,
        pendingQueueLen: Array.isArray(ui?.dinoPendingNematocystPayloads) ? ui.dinoPendingNematocystPayloads.length : null,
        hasAdapterHost: !!w.hfoAdapterHost,
        hasRegistryHost: !!(w.hfoRegistry?.resolve && w.hfoTokens?.P7_ADAPTER_HOST),
        hasPortsEffects: !!effects,
        canGetRecent,
      };

      const battery = w.HFOP3DiagnosticBatteryV1.create();

      const keyboard = await battery.runShot({ variant: 'keyboard_packet', params: { repeat: 1, code: 'Space', key: ' ' } });
      const spans = await battery.runShot({ variant: 'trace_span_chain' });
      const ultrasound = await battery.runShot({ variant: 'queue_ultrasound', params: { sampleEveryMs: 150, sampleWindowMs: 900 } });
      const canary = await battery.runShot({ variant: 'synthetic_canary', params: { windowMs: 800, pollEveryMs: 100 } });

      const after = {
        dinoWrapperIframePresent: !!ui?.dinoWrapperIframe,
        pendingQueueLen: Array.isArray(ui?.dinoPendingNematocystPayloads) ? ui.dinoPendingNematocystPayloads.length : null,
        lastPending: Array.isArray(ui?.dinoPendingNematocystPayloads) && ui.dinoPendingNematocystPayloads.length
          ? ui.dinoPendingNematocystPayloads[ui.dinoPendingNematocystPayloads.length - 1]
          : null,
      };

      const recent = canGetRecent ? (effects.getRecent(250) || []) : [];

      const flush = recent.filter((e: any) => e?.port === 'p7' && e?.type === 'dino_flush_queue');
      const p3diag = recent.filter((e: any) => e?.port === 'p3' && String(e?.type || '').startsWith('diagnostic_'));

      return {
        before,
        after,
        keyboard,
        spans,
        ultrasound,
        canary,
        recentCounts: {
          total: recent.length,
          flush: flush.length,
          p3diagnostic: p3diag.length,
        },
      };
    }, undefined as any);
  };

  const light = await runOnce('light', '');
  const injectorOn = await runOnce('injector_on', '&flag-p3-injector=true');

  // Emit a compact, human-readable summary into the test output.
  // Keep this intentionally small to avoid log spam.
  const compact = (r: any) => ({
    before: r.before,
    after: {
      dinoWrapperIframePresent: r.after?.dinoWrapperIframePresent,
      pendingQueueLen: r.after?.pendingQueueLen,
      lastPendingKind: r.after?.lastPending?.kind ?? null,
      lastPendingReason: r.after?.lastPending?.reason ?? null,
      lastPendingTraceId: r.after?.lastPending?.traceId ?? null,
    },
    keyboard: { ok: r.keyboard?.ok ?? null, okCount: r.keyboard?.okCount ?? null, failCount: r.keyboard?.failCount ?? null },
    spans: { ok: r.spans?.ok ?? null },
    ultrasound: { sampleCount: r.ultrasound?.sampleCount ?? null, maxFlush: r.ultrasound?.maxFlush ?? null },
    canary: {
      ok: r.canary?.ok ?? null,
      verdict: r.canary?.verdict ?? null,
      primarySignal: r.canary?.primarySignal ?? null,
      attempts: r.canary?.attempts ?? null,
      okCount: r.canary?.okCount ?? null,
      failCount: r.canary?.failCount ?? null,
      baselineFlush: r.canary?.baselineFlush ?? null,
      finalFlush: r.canary?.finalFlush ?? null,
      baselinePending: r.canary?.baselinePending ?? null,
      finalPending: r.canary?.finalPending ?? null,
    },
    recentCounts: r.recentCounts,
  });

  console.log('[p3_diagnostic_battery_probe_v17_4:light]', JSON.stringify(compact(light)));
  console.log('[p3_diagnostic_battery_probe_v17_4:injector_on]', JSON.stringify(compact(injectorOn)));

  // Only assert that the probe returns structure; ok-ness depends on runtime readiness.
  expect(light.before.hasPortsEffects).toBe(true);
  expect(light.before.canGetRecent).toBe(true);
  expect(light.recentCounts.p3diagnostic).toBeGreaterThan(0);

  expect(injectorOn.before.hasPortsEffects).toBe(true);
  expect(injectorOn.before.canGetRecent).toBe(true);
  expect(injectorOn.recentCounts.p3diagnostic).toBeGreaterThan(0);
});
