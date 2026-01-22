// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    // NOTE: disable-camera must be false here; we stub getUserMedia in-page.
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=false';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

function withTarget(urlStr: string, targetPath: string) {
    const url = new URL(urlStr);
    url.searchParams.set('target', targetPath);
    return url.toString();
}

test('Gen5 v11.3: multiview uses single getUserMedia stream across multiple views', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11_3.html';

    // Stub camera APIs before any page script runs.
    await hfoPage.addInitScript(() => {
        // @ts-ignore
        window.__gumCalls = 0;
        // @ts-ignore
        window.__gumStreams = [];

        // Ensure mediaDevices exists.
        // @ts-ignore
        if (!navigator.mediaDevices) {
            // @ts-ignore
            navigator.mediaDevices = {};
        }

        // @ts-ignore
        navigator.mediaDevices.getUserMedia = async () => {
            // @ts-ignore
            window.__gumCalls += 1;
            const stream = new MediaStream();
            // @ts-ignore
            window.__gumStreams.push(stream);
            return stream;
        };
    });

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(withFlag(url, 'ui-multiview', 'true'));
    await hfoPage.waitForURL(/omega_gen5_v11_3\.html/i, { timeout: 20000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry && window.hfoPorts);
    }, null, { timeout: 20000 });
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        const ports = window.hfoPorts;
        // @ts-ignore
        const gumCalls = window.__gumCalls || 0;

        const videos = Array.from(document.querySelectorAll('video')) as HTMLVideoElement[];
        const withStream = videos.filter(v => !!v.srcObject).length;

        const stream = videos.find(v => v.srcObject)?.srcObject || null;
        const allSame = stream ? videos.filter(v => !!v.srcObject).every(v => v.srcObject === stream) : false;

        return {
            hasPorts: !!ports,
            hasCameraFacade: !!ports?.p0?.camera,
            gumCalls,
            totalVideos: videos.length,
            videosWithStream: withStream,
            allSame
        };
    });

    expect(out.hasPorts).toBe(true);
    expect(out.hasCameraFacade).toBe(true);

    expect(out.totalVideos).toBeGreaterThanOrEqual(2);
    expect(out.videosWithStream).toBeGreaterThanOrEqual(2);

    expect(out.gumCalls).toBe(1);
    expect(out.allSame).toBe(true);
});
