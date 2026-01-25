// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V19_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// TDD (was RED): lock in FSM→color mapping for the knuckle tripwire panel.

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V19_TEST_URL_LIGHT}`
    + '&flag-ui-knuckle-tripwire-panel=true'
    + '&flag-ui-multiview=false'
    + '&flag-ui-multiapp=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-p3-tripwire-injector-static=false'
    + '&flag-p3-tripwire-injector-knuckle=false';

const rgb = (hex: string): string => {
    const h = hex.replace('#', '').trim();
    const r = parseInt(h.slice(0, 2), 16);
    const g = parseInt(h.slice(2, 4), 16);
    const b = parseInt(h.slice(4, 6), 16);
    return `rgb(${r}, ${g}, ${b})`;
};

test('Gen6 v19 (TDD): knuckle tripwire panel renders and maps FSM→color', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, async () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');

        const panel = document.querySelector('[data-testid="knuckle-tripwire-panel"]');
        const bar = document.querySelector('[data-testid="knuckle-tripwire-bar"]') as HTMLElement | null;
        if (!panel) throw new Error('missing knuckle-tripwire-panel');
        if (!bar) throw new Error('missing knuckle-tripwire-bar');
        if (!w.hfoUiKnuckleTripwirePanel?.renderOnce) throw new Error('missing window.hfoUiKnuckleTripwirePanel.renderOnce');

        const setFsm = (fsmState: string) => {
            w.systemState.dataFabric = {
                cursors: [
                    {
                        handIndex: 0,
                        pointerId: 1,
                        fsmState,
                        readinessScore: 0.9,
                        uiNormX: 0.5,
                        uiNormY: 0.5,
                    },
                ],
                systemTime: 1000,
                frameId: 1,
            };
            w.hfoUiKnuckleTripwirePanel.renderOnce();
        };

        const getBarColor = () => {
            const cs = window.getComputedStyle(bar);
            return String(cs.backgroundColor || '');
        };

        setFsm('IDLE');
        const idle = getBarColor();
        setFsm('READY');
        const ready = getBarColor();
        setFsm('COMMIT');
        const commit = getBarColor();
        setFsm('COAST');
        const coast = getBarColor();

        return { idle, ready, commit, coast };
    }, null);

    expect(out.idle).toBe(rgb('#9E9E9E'));
    expect(out.ready).toBe(rgb('#FFB300'));
    expect(out.commit).toBe(rgb('#00BCD4'));
    expect(out.coast).toBe(rgb('#FFEB3B'));
});
