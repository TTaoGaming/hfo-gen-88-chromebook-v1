// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v17 exists:
// v17 should provide deterministic resize/activation hooks for panels (tested via test plugin counters).

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_TEST_URL_LIGHT}`
    + '&flag-ui-microkernel=true'
    + '&flag-ui-plugins=true'
    + '&flag-ui-test-plugin=true'
    + '&flag-ui-golden-layout=true'
    + '&flag-ui-lil-gui=false';

test('Gen6 v17 (TDD RED): panels receive resize/show/hide hooks', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, async () => {
        const w = window as any;
        const t = w.__hfoUiShellTest;
        if (!t) return { ok: false, reason: 'missing __hfoUiShellTest' };

        if (typeof t.enableTestPanel !== 'function' || typeof t.simulateTabSwitch !== 'function' || typeof t.simulateResize !== 'function') {
            return { ok: false, reason: 'missing test panel hooks' };
        }

        t.enableTestPanel();
        t.simulateTabSwitch();
        t.simulateResize();

        return {
            ok: true,
            onShowCount: Number(t.counters?.onShowCount || 0),
            onHideCount: Number(t.counters?.onHideCount || 0),
            onResizeCount: Number(t.counters?.onResizeCount || 0),
        };
    }, null);

    expect(out.ok, `Expected v17 panel test hooks; got=${JSON.stringify(out)}`).toBe(true);

    // RED until v17 panel lifecycle exists.
    expect(out.onShowCount, 'Expected at least 1 onShow').toBeGreaterThanOrEqual(1);
    expect(out.onHideCount, 'Expected at least 1 onHide').toBeGreaterThanOrEqual(1);
    expect(out.onResizeCount, 'Expected at least 1 onResize').toBeGreaterThanOrEqual(1);
});
