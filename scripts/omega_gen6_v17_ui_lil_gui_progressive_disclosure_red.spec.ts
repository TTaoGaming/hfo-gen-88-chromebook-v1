// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v17 exists:
// v17 must own lil-gui creation and expose a registry so tests can assert progressive disclosure
// without brittle DOM scraping.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_TEST_URL_LIGHT}`
    + '&flag-ui-microkernel=true'
    + '&flag-ui-lil-gui=true'
    + '&flag-ui-test-plugin=true';

test('Gen6 v17 (TDD RED): lil-gui progressive disclosure (Advanced folder gated)', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        const shell = w.hfoUiShell || w.HFOUiShell || w.__hfoUiShell;
        const t = w.__hfoUiShellTest;

        if (!shell || !t) {
            return { ok: false, reason: 'missing shell or test hooks' };
        }

        // Registry API is a v17 requirement.
        const listFolders = shell?.services?.gui?.listFolders;
        if (typeof listFolders !== 'function') {
            return { ok: false, reason: 'missing shell.services.gui.listFolders' };
        }

        const baseline = listFolders();
        t.enableAdvancedGui?.(false);
        const afterDisable = listFolders();
        t.enableAdvancedGui?.(true);
        const afterEnable = listFolders();

        return { ok: true, baseline, afterDisable, afterEnable };
    }, null);

    expect(out.ok, `Expected v17 gui registry/test hooks; got=${JSON.stringify(out)}`).toBe(true);

    // RED until v17 implements progressive disclosure.
    expect(out.afterDisable?.includes?.('Advanced') || false, 'Advanced folder should be absent by default').toBe(false);
    expect(out.afterEnable?.includes?.('Advanced') || false, 'Advanced folder should appear only when explicitly enabled').toBe(true);
});
