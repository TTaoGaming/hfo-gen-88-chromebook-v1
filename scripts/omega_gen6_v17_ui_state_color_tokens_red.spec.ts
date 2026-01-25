// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v17 exists:
// v17 must expose consolidated global state color tokens via theming service.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_TEST_URL_LIGHT}`
    + '&flag-ui-microkernel=true'
    + '&flag-ui-theme-tokens=true'
    + '&flag-ui-test-plugin=false'
    + '&flag-ui-lil-gui=false';

const EXPECTED = {
    IDLE: { name: 'gray', hex: '#8E8E93' },
    READY: { name: 'amber', hex: '#FFB300' },
    COMMIT: { name: 'cyan', hex: '#00BCD4' },
    COAST: { name: 'yellow', hex: '#FFEB3B' },
};

test('Gen6 v17 (TDD RED): theming exposes global state color tokens', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        const shell = w.hfoUiShell || w.HFOUiShell || w.__hfoUiShell;
        const tokens = shell?.services?.theming?.tokens?.state_colors?.mapping;
        return { hasShell: Boolean(shell), tokens: tokens || null };
    }, null);

    // RED until v17 implements shell+theming.
    expect(out.hasShell, 'Expected v17 UI shell to exist').toBe(true);
    expect(out.tokens, 'Expected v17 theming tokens at shell.services.theming.tokens.state_colors.mapping').toBeTruthy();

    // Once shell exists, enforce exact mapping.
    expect(out.tokens).toEqual(EXPECTED);
});
