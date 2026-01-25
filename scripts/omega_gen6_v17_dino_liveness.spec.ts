// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto } from './omega_gen6_test_guards';

test('Gen6 v17: Dino runner liveness (Space starts + distance increases)', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_V17_TEST_URL_LIGHT);

    await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
    await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

    // Ensure wrapper document is ready (inner runner may still be loading).
    await hfoPage.waitForFunction(() => {
        const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
        if (!wrapper) return false;
        try {
            return wrapper.contentDocument?.readyState === 'complete';
        } catch {
            return false;
        }
    }, null, { timeout: 20_000 });

    // Ensure the inner vendor frame exists and Runner is present.
    await hfoPage.waitForFunction(() => {
        const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
        if (!wrapper) return false;
        const inner = wrapper.contentDocument?.getElementById('frame') as HTMLIFrameElement | null;
        if (!inner) return false;
        const w = inner.contentWindow as any;
        return !!w?.Runner;
    }, null, { timeout: 20_000 });

    const snap0 = await hfoPage.evaluate(() => {
        const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
        const inner = wrapper?.contentDocument?.getElementById('frame') as HTMLIFrameElement | null;
        const w = inner?.contentWindow as any;
        const inst = w?.Runner?.instance_ || null;

        return {
            hasWrapper: !!wrapper,
            hasInner: !!inner,
            hasRunner: !!w?.Runner,
            hasInstance: !!inst,
            playing: Boolean(inst?.playing),
            paused: Boolean(inst?.paused),
            crashed: Boolean(inst?.crashed),
            distanceRan: typeof inst?.distanceRan === 'number' ? inst.distanceRan : null,
        };
    });

    expect(snap0.hasWrapper).toBe(true);
    expect(snap0.hasInner).toBe(true);
    expect(snap0.hasRunner).toBe(true);

    // Start the game using the wrapper adapter, since that's the production control path.
    await hfoPage.evaluate(() => {
        const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
        const cw = wrapper?.contentWindow;
        if (!cw) throw new Error('Missing dino wrapper contentWindow');

        cw.postMessage(
            {
                type: 'hfo:nematocyst',
                payload: { kind: 'keyboard', action: 'keypress', key: ' ', code: 'Space' },
            },
            window.location.origin,
        );
    });

    // Wait for game to enter playing state.
    await hfoPage.waitForFunction(() => {
        const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
        const inner = wrapper?.contentDocument?.getElementById('frame') as HTMLIFrameElement | null;
        const w = inner?.contentWindow as any;
        const inst = w?.Runner?.instance_ || null;
        return Boolean(inst?.playing) && !Boolean(inst?.paused) && !Boolean(inst?.crashed);
    }, null, { timeout: 10_000 });

    const snap1 = await hfoPage.evaluate(async () => {
        const getDistance = () => {
            const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
            const inner = wrapper?.contentDocument?.getElementById('frame') as HTMLIFrameElement | null;
            const w = inner?.contentWindow as any;
            const inst = w?.Runner?.instance_ || null;
            return typeof inst?.distanceRan === 'number' ? inst.distanceRan : null;
        };

        const d0 = getDistance();
        await new Promise((r) => setTimeout(r, 1200));
        const d1 = getDistance();

        return { d0, d1 };
    });

    expect(typeof snap1.d0).toBe('number');
    expect(typeof snap1.d1).toBe('number');

    // Liveness assertion: distance increases (i.e., the runner loop is advancing).
    expect((snap1.d1 as number) - (snap1.d0 as number)).toBeGreaterThan(0);
});
