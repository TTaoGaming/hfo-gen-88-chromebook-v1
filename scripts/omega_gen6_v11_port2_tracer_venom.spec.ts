// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_URL =
    process.env.HFO_GEN6_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v11.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

test('Gen6 v11: tracer venom disperse reveals P2 + P3 coverage', async ({ hfoPage }) => {
    await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
    await hfoPage.waitForTimeout(300);

    const out = await hfoPage.evaluate(async () => {
        const anyWindow = window as any;
        if (!anyWindow.diagnosticTracerBulletVenom?.disperse) {
            throw new Error('missing diagnosticTracerBulletVenom.disperse');
        }

        return await anyWindow.diagnosticTracerBulletVenom.disperse({
            sequenceId: 'seq01_basic_fill_then_drain',
        });
    });

    expect(out?.traceId, 'Expected base traceId').toBeTruthy();
    expect(out?.summary?.total, 'Expected 3 shots').toBe(3);

    const shots: any[] = out?.shots || [];
    const byTarget: Record<string, any> = Object.fromEntries(shots.map((s) => [s.targetId, s]));

    expect(byTarget['p2.fsm']?.counts?.p2FsmTransition, 'Expected P2 fsm_transition via replay').toBeGreaterThanOrEqual(1);

    expect(byTarget['p2.dino']?.counts?.p2DinoReadyEdge, 'Expected P2 dino_ready_edge via replay').toBeGreaterThanOrEqual(1);
    expect(byTarget['p2.dino']?.counts?.ackOk, 'Expected wrapper ack ok for P2 dino shot').toBeGreaterThanOrEqual(1);

    expect(byTarget['p3.direct']?.counts?.ackOk, 'Expected wrapper ack ok for direct P3 strike').toBeGreaterThanOrEqual(1);
});
