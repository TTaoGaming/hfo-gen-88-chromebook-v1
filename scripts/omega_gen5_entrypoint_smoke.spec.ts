// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Active HFO Omega Entrypoint: forwards to baseline and exposes hex ports', async ({ hfoPage }) => {
    await hfoPage.goto(ENTRYPOINT_URL);

    // Entrypoint uses location.replace; Playwright should follow the navigation.
    await hfoPage.waitForURL(/omega_gen5_v1[12]\.html/i, { timeout: 20000 });
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoPorts) throw new Error('hfoPorts missing');
        // @ts-ignore
        if (!window.hfoPortMeta) throw new Error('hfoPortMeta missing');

        // @ts-ignore
        if (!window.hfoTokens) throw new Error('hfoTokens missing');
        // @ts-ignore
        if (!window.hfoRegistry) throw new Error('hfoRegistry missing');

        // @ts-ignore
        if (!window.hfoPorts?.p7?.navigate?.getMissionVision) throw new Error('Ports.p7.navigate missing');

        return {
            href: window.location.href,
            hasTokens: !!window.hfoTokens,
            hasRegistry: !!window.hfoRegistry,
        };
    });

    expect(out.hasTokens).toBe(true);
    expect(out.hasRegistry).toBe(true);
    expect(out.href).toMatch(/omega_gen5_v1[12]\.html/i);
});
