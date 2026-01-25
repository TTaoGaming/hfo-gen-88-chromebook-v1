// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v10_2.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

test('Gen5 v10.2 P4 disrupt: opt-in adapter + other ports remain reachable', async ({ hfoPage }) => {
    await hfoPage.goto(withFlag(GEN5_URL, 'p4-disrupt', 'true'));
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoTokens?.P4_DISRUPT) throw new Error('hfoTokens.P4_DISRUPT missing');
        // @ts-ignore
        if (!window.hfoPorts?.p4?.disrupt) throw new Error('Ports.p4.disrupt not available');

        // Ensure other port surfaces still exist.
        // @ts-ignore
        if (!window.hfoPorts?.p0?.sense?.readForVideo) throw new Error('Ports.p0.sense missing');
        // @ts-ignore
        if (!window.hfoPorts?.p1?.weave) throw new Error('Ports.p1.weave missing');
        // @ts-ignore
        if (!window.hfoPorts?.p3?.deliver) throw new Error('Ports.p3.deliver missing');
        // @ts-ignore
        if (!window.hfoPorts?.p6?.store) throw new Error('Ports.p6.store missing');
        // @ts-ignore
        if (!window.hfoPorts?.p7?.navigate?.getMissionVision) throw new Error('Ports.p7.navigate missing');

        // @ts-ignore
        const enabled = window.hfoPorts.p4.disrupt.isEnabled();
        // @ts-ignore
        const noOp = window.hfoPorts.p4.disrupt.noOp();
        // @ts-ignore
        const probe = window.hfoPorts.p4.disrupt.probeAdapters();

        return { enabled, noOp, probe };
    });

    expect(out?.enabled).toBe(true);
    expect(out?.noOp?.ok).toBe(true);
    expect(out?.noOp?.enabled).toBe(true);
    expect(out?.noOp?.ts).toBeTruthy();

    // Minimum expected adapters for the v10.2 modular monolith scaffold.
    expect(out?.probe?.p0).toBe(true);
    expect(out?.probe?.p1).toBe(true);
    expect(out?.probe?.p2_physics).toBe(true);
    expect(out?.probe?.p2_render).toBe(true);
    expect(out?.probe?.p5_eval).toBe(true);
    expect(out?.probe?.p6).toBe(true);
    expect(out?.probe?.p7).toBe(true);
});
