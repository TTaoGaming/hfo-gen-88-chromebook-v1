// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v17 exists:
// requires an opt-in test plugin that exposes lifecycle counters under window.__hfoUiShellTest

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_TEST_URL_LIGHT}`
    + '&flag-ui-microkernel=true'
    + '&flag-ui-plugins=true'
    + '&flag-ui-test-plugin=true'
    + '&flag-ui-golden-layout=true'
    + '&flag-ui-lil-gui=false';

test('Gen6 v17 (TDD RED): plugin lifecycle is idempotent (mount/dispose counters)', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;

        // RED until v17 exposes deterministic test hooks.
        const t = w.__hfoUiShellTest;
        if (!t) {
            return { ok: false, reason: 'missing __hfoUiShellTest' };
        }

        if (typeof t.enableTestPlugin !== 'function' || typeof t.disableTestPlugin !== 'function') {
            return { ok: false, reason: 'missing enableTestPlugin/disableTestPlugin' };
        }

        t.enableTestPlugin();
        t.enableTestPlugin();
        t.disableTestPlugin();
        t.disableTestPlugin();

        return {
            ok: true,
            mountCount: Number(t.counters?.mountCount || 0),
            disposeCount: Number(t.counters?.disposeCount || 0),
            activeSubscriptions: Number(t.counters?.activeSubscriptions || 0),
            activeIntervals: Number(t.counters?.activeIntervals || 0),
        };
    }, null);

    expect(out.ok, `Expected v17 test hooks; got=${JSON.stringify(out)}`).toBe(true);

    // RED until lifecycle is implemented.
    expect(out.mountCount, 'mountCount should be exactly 1 after repeated enables').toBe(1);
    expect(out.disposeCount, 'disposeCount should be exactly 1 after repeated disables').toBe(1);
    expect(out.activeSubscriptions, 'no leaked subscriptions after dispose').toBe(0);
    expect(out.activeIntervals, 'no leaked intervals after dispose').toBe(0);
});
