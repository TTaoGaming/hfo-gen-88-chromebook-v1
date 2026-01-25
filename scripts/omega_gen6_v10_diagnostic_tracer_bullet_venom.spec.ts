// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_URL =
    process.env.HFO_GEN6_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v10.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

test('Gen6 v10: diagnosticTracerBulletVenom traces e2e (P1→P3→P7→ACK)', async ({ hfoPage }) => {
    await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });

    // Ensure the runtime has booted enough for replay + adapters.
    await hfoPage.waitForTimeout(250);

    const out = await hfoPage.evaluate(async () => {
        const anyWindow = window as any;
        if (!anyWindow.diagnosticTracerBulletVenom?.fire) {
            throw new Error('missing diagnosticTracerBulletVenom.fire');
        }

        // Use seq01 because it should produce exactly one IDLE→READY edge.
        return await anyWindow.diagnosticTracerBulletVenom.fire({
            sequenceId: 'seq01_basic_fill_then_drain',
        });
    });

    expect(out?.traceId, 'Expected traceId returned').toBeTruthy();

    const counts = out?.counts || {};
    expect(counts.p1FsmEdge, 'Expected at least one P1 fsm_edge with traceId').toBeGreaterThanOrEqual(1);
    expect(counts.p3Nematocyst, 'Expected at least one P3 nematocyst_deliver with traceId').toBeGreaterThanOrEqual(1);
    expect(counts.p7PostMessageOk, 'Expected at least one P7 dino_postMessage ok with traceId').toBeGreaterThanOrEqual(1);
    expect(counts.ackOk, 'Expected at least one wrapper hfo:nematocyst:ack ok with traceId').toBeGreaterThanOrEqual(1);
});
