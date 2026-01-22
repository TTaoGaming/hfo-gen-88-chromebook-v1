// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs/promises';
import path from 'node:path';

const GEN6_URL =
    process.env.HFO_GEN6_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v12.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

const GOLDEN_PATH = path.resolve(
    __dirname,
    '..',
    'hfo_hot_obsidian',
    'bronze',
    '3_resources',
    'fixtures',
    'golden',
    'gen6_v12_touch2d_split_top_bottom_commit_crossing_golden.json'
);

test('Gen6 v12: Touch2D top/bottom split zones emit P2 events and map bottom-enter to Dino Space', async ({ hfoPage }) => {
    const goldenRaw = await fs.readFile(GOLDEN_PATH, 'utf-8');
    const golden = JSON.parse(goldenRaw);

    await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
    await hfoPage.waitForTimeout(250);

    const result = await hfoPage.evaluate((g) => {
        const w = window as any;
        // Ensure we can drive the module deterministically.
        if (!w.hfoP2GestureLanguage?.tick) throw new Error('missing hfoP2GestureLanguage.tick');

        // Capture Port2 telemetry emissions.
        const p2Calls: Array<{ port: string; type: string; payload: any }> = [];
        const p3Telem: Array<{ port: string; type: string; payload: any }> = [];
        const dinoSent: any[] = [];

        // Stub emit bus if present (preserve other behavior if any).
        const origEmit = w.hfoPortsEffects?.emit;
        if (!w.hfoPortsEffects) w.hfoPortsEffects = {};
        w.hfoPortsEffects.emit = (port: string, type: string, payload: any) => {
            if (port === 'p2') p2Calls.push({ port, type, payload });
            if (port === 'p3') p3Telem.push({ port, type, payload });
            try { return origEmit?.call?.(w.hfoPortsEffects, port, type, payload); } catch (_) { return undefined; }
        };

        // Stub Dino injector so P3 dispatch is observable.
        w.P3InjectorPort = w.P3InjectorPort || {};
        w.P3InjectorPort.sendNematocystToDino = (payload: any) => {
            dinoSent.push(payload);
            return true;
        };

        // Enable P2 and P3 dispatch.
        // NOTE: systemState is a top-level const in the runtime; it is accessible in-page (not as window.systemState).
        // @ts-ignore
        systemState.parameters.p2.gestureLanguage.enabled = true;
        // @ts-ignore
        systemState.parameters.p2.gestureLanguage.emitP3 = true;
        // @ts-ignore
        systemState.parameters.p2.gestureLanguage.emitTelemetry = true;
        // @ts-ignore
        systemState.parameters.p2.gestureLanguage.minReadiness = 0.2;

        const frames = Array.isArray(g?.frames) ? g.frames : [];
        const tpl = g?.cursorTemplate || {};

        for (const f of frames) {
            const cursor = {
                ...tpl,
                uiNormY: f.uiNormY,
                normX: tpl.uiNormX,
                normY: f.uiNormY,
            };
            w.hfoP2GestureLanguage.tick({
                now: Number(f.now || 0),
                dt: Number(f.dt || 16),
                dataFabric: { cursors: [cursor] },
            });
        }

        return {
            p2Calls,
            p3Telem,
            dinoSent,
        };
    }, golden);

    const p2Types = new Set((result?.p2Calls || []).map((c: any) => c.type));
    expect(p2Types.has('zone_enter'), 'Expected P2 zone_enter').toBeTruthy();
    expect(p2Types.has('zone_exit'), 'Expected P2 zone_exit').toBeTruthy();

    const p2ZoneIds = new Set((result?.p2Calls || []).map((c: any) => c?.payload?.zoneId).filter(Boolean));
    expect(p2ZoneIds.has('top'), 'Expected to enter/exit top zone').toBeTruthy();
    expect(p2ZoneIds.has('bottom'), 'Expected to enter bottom zone').toBeTruthy();

    const dino = result?.dinoSent || [];
    expect(dino.length, 'Expected at least one Dino injection payload').toBeGreaterThan(0);

    const hasSpace = dino.some((p: any) => p?.kind === 'keyboard' && (p?.key === ' ' || p?.code === 'Space'));
    expect(hasSpace, 'Expected bottom-enter to map to Space keypress').toBeTruthy();
});
