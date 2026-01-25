// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

test('Gen5 v11 strict hex: entrypoint forwards flag + boots fail-closed surfaces', async ({ hfoPage }) => {
    await hfoPage.goto(withFlag(ENTRYPOINT_URL, 'p5-defend-strict-v11', 'true'));

    await hfoPage.waitForURL(/omega_gen5_v11\.html/i, { timeout: 20000 });
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoPorts) throw new Error('hfoPorts missing');
        // @ts-ignore
        if (!window.hfoTokens) throw new Error('hfoTokens missing');
        // @ts-ignore
        if (!window.hfoRegistry) throw new Error('hfoRegistry missing');

        // @ts-ignore
        if (!window.hfoPorts?.p0?.sense?.readForVideo) throw new Error('P0 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p1?.weave) throw new Error('P1 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p2?.physics?.getTelemetry) throw new Error('P2.physics facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p2?.render?.listJuiceLayers) throw new Error('P2.render facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p3?.deliver) throw new Error('P3 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p4?.disrupt?.noOp) throw new Error('P4 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p5?.eval) throw new Error('P5 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p6?.store) throw new Error('P6 facade missing');
        // @ts-ignore
        if (!window.hfoPorts?.p7?.navigate?.getMissionVision) throw new Error('P7 facade missing');

        const url = new URL(window.location.href);
        return {
            href: window.location.href,
            strictFlag: url.searchParams.get('flag-p5-defend-strict-v11'),
        };
    });

    expect(out.href).toMatch(/omega_gen5_v11\.html/i);
    expect(out.strictFlag).toBe('true');
});
