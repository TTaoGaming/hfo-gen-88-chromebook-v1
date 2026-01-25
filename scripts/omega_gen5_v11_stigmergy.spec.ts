// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Gen5 v11 stigmergy: emitter exists + event dispatch + bounded buffer', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    const out = (await hfoPage.evaluate(async () => {
        // @ts-ignore
        if (!window.hfoStigmergy) throw new Error('hfoStigmergy missing');
        // @ts-ignore
        if (typeof window.hfoStigmergy.emit !== 'function') throw new Error('hfoStigmergy.emit missing');
        // @ts-ignore
        if (typeof window.hfoStigmergy.getRecent !== 'function') throw new Error('hfoStigmergy.getRecent missing');

        // @ts-ignore
        const unsub = window.hfoStigmergy.subscribe((detail) => {
            // no-op; capture below
        });
        unsub();

        return await new Promise((resolve, reject) => {
            const payload = { intent: 'omega_gate_probe', n: 1 };
            const timeout = setTimeout(() => reject(new Error('stigmergy event timeout')), 1500);

            function onAny(e: any) {
                clearTimeout(timeout);
                try {
                    // @ts-ignore
                    const recent = window.hfoStigmergy.getRecent(10);
                    resolve({
                        gotType: e?.detail?.type,
                        gotPayloadIntent: e?.detail?.payload?.intent,
                        recentCount: recent.length,
                        recentLastType: recent[recent.length - 1]?.type,
                    });
                } catch (err) {
                    reject(err);
                } finally {
                    window.removeEventListener('hfo:stigmergy', onAny);
                }
            }

            window.addEventListener('hfo:stigmergy', onAny);

            // @ts-ignore
            window.hfoStigmergy.emit('omega_gate_probe', payload);
        });
    })) as {
        gotType: string;
        gotPayloadIntent: string;
        recentCount: number;
        recentLastType: string;
    };

    expect(out.gotType).toBe('omega_gate_probe');
    expect(out.gotPayloadIntent).toBe('omega_gate_probe');
    expect(out.recentCount).toBeGreaterThan(0);
    expect(out.recentLastType).toBe('omega_gate_probe');
});
