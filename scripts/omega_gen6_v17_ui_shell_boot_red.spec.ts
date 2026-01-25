// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v17 exists:
// - v16 should boot (known-good base)
// - v17 should expose a microkernel UI shell surface when ui-microkernel=true

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_TEST_URL_LIGHT}`
    + '&flag-ui-microkernel=true'
    + '&flag-ui-plugins=false'
    + '&flag-ui-golden-layout=true'
    + '&flag-ui-lil-gui=false'
    + '&flag-ui-test-plugin=false';

test('Gen6 v17 (TDD RED): UI shell boots (microkernel surface exists) even with plugins disabled', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        return {
            hasSystemState: Boolean(w.systemState),
            hasPortsEffects: Boolean(w.hfoPortsEffects?.subscribe && w.hfoPortsEffects?.emit),
            hasUiShell: Boolean(w.hfoUiShell || w.HFOUiShell || w.__hfoUiShell),
        };
    }, null);

    expect(out.hasSystemState, 'Expected v16 baseline to boot (systemState present)').toBe(true);
    expect(out.hasPortsEffects, 'Expected v16 baseline to expose Ports Effects bus').toBe(true);

    // RED until v17 microkernel is implemented.
    expect(out.hasUiShell, 'Expected v17 to expose a UI shell object when ui-microkernel=true').toBe(true);
});
