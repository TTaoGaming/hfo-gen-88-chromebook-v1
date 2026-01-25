// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V18_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v18 exists:
// When flag-p2-knuckle-keybar=true, runtime should expose a deterministic P2 thread.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V18_TEST_URL_LIGHT}`
    + '&flag-p2-knuckle-keybar=true'
    + '&flag-p2-knuckle-keybar-orientation-knob=false'
    + '&flag-p3-knuckle-key-injector=false'
    + '&flag-ui-knuckle-keybar-overlay=false';

test('Gen6 v18 (TDD RED): P2 KnuckleKeybarThread exists when enabled', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        return {
            hasSystemState: Boolean(w.systemState),
            hasPortsEffects: Boolean(w.hfoPortsEffects?.subscribe && w.hfoPortsEffects?.emit),
            hasThread: Boolean(w.hfoP2KnuckleKeybarThread),
            hasTick: Boolean(w.hfoP2KnuckleKeybarThread?.tick),
        };
    }, null);

    expect(out.hasSystemState, 'Expected v18 entrypoint to boot (systemState present)').toBe(true);
    expect(out.hasPortsEffects, 'Expected Ports Effects bus to exist').toBe(true);

    // RED until v18 implemented.
    expect(out.hasThread, 'Expected v18 to expose window.hfoP2KnuckleKeybarThread when flag enabled').toBe(true);
    expect(out.hasTick, 'Expected v18 thread to expose tick({now,dt,dataFabric})').toBe(true);
});
