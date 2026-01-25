// Medallion: Bronze | Mutation: 0% | HIVE: V
import path from 'node:path';
import { test, expect } from './hfo_fixtures';
import { GEN6_V16_1_TEST_URL_LIGHT, GEN6_V17_4_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6: P3 diagnostic battery runs across v16.1 + v17.4 (thin adapter, version-independent)', async ({ hfoPage }) => {
    const batteryPath = path.resolve(
        process.cwd(),
        'hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/lib/js/hfo_p3_diagnostic_battery_v1.js',
    );

    const runOn = async (url: string) => {
        await safeGoto(hfoPage, `${url}&test-run=p3_diagnostic_battery_cross_version`);
        await hfoPage.addScriptTag({ path: batteryPath });

        return safeEvaluate(
            hfoPage,
            async () => {
                const w = window as any;
                if (!w.HFOP3DiagnosticBatteryV1?.create) throw new Error('missing HFOP3DiagnosticBatteryV1.create');

                const emits: any[] = [];
                let recentCalls = 0;

                const battery = w.HFOP3DiagnosticBatteryV1.create({
                    isEnabled: () => true,
                    emit: (port: string, type: string, payload: any) => {
                        emits.push({ port, type, payload });
                    },
                    deliverEffect: () => true,
                    getRecent: () => {
                        // Synthetic canary expects to observe at least one p7/dino_flush_queue.
                        recentCalls++;
                        if (recentCalls >= 3) return [{ port: 'p7', type: 'dino_flush_queue' }];
                        return [];
                    },
                });

                const biopsy = await battery.runShot({ variant: 'dom_target_biopsy', params: { selector: 'body' } });
                const keyboard = await battery.runShot({ variant: 'keyboard_packet', params: { repeat: 1, code: 'Space', key: ' ' } });
                const canary = await battery.runShot({ variant: 'synthetic_canary', params: { windowMs: 400, pollEveryMs: 50 } });
                const w3c = await battery.runShot({ variant: 'w3c_pointer_packet', params: {} });
                const echo = await battery.runShot({ variant: 'adapter_echo', params: { echo: 'ping' } });

                return {
                    biopsy,
                    keyboard,
                    canary,
                    w3c,
                    echo,
                    emitsLen: emits.length,
                };
            },
            undefined as any,
        );
    };

    const v16 = await runOn(GEN6_V16_1_TEST_URL_LIGHT);
    expect(v16.emitsLen).toBeGreaterThan(0);
    expect(v16.biopsy.ok).toBe(true);
    expect(v16.canary.ok).toBe(true);
    expect(typeof v16.w3c.traceparent).toBe('string');
    expect(v16.w3c.traceparent.startsWith('00-')).toBe(true);
    expect(v16.echo.ok).toBe(true);

    const v17_4 = await runOn(GEN6_V17_4_TEST_URL_LIGHT);
    expect(v17_4.emitsLen).toBeGreaterThan(0);
    expect(v17_4.biopsy.ok).toBe(true);
    expect(v17_4.canary.ok).toBe(true);
    expect(typeof v17_4.w3c.traceparent).toBe('string');
    expect(v17_4.w3c.traceparent.startsWith('00-')).toBe(true);
    expect(v17_4.echo.ok).toBe(true);
});
