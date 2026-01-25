// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V17_4_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17.4: palm-cone READY gate (anti-midas) drops READY/COMMIT to IDLE when gate closes', async ({ hfoPage }) => {
    const url = `${GEN6_V17_4_TEST_URL_LIGHT}`
        + '&flag-engine-babylon=false'
        + '&flag-engine-canvas=false'
        + '&flag-ui-excalidraw=false'
        + '&flag-ui-lil-gui=false'
        + '&flag-p3-injector=false'
        + '&flag-p2-ready-gate-palm-cone=true'
        + '&test-run=p2_ready_gate_palm_cone';

    await safeGoto(hfoPage, url);
    await hfoPage.waitForTimeout(100);

    const res = await safeEvaluate(
        hfoPage,
        () => {
            const w = window as any;
            if (!w.hfoP2MirrorMagus?.computeSovereignFsmNext) throw new Error('missing hfoP2MirrorMagus.computeSovereignFsmNext');

            const base = {
                readiness: 0.95,
                isFacingCamera: true,
                isCharging: false,
                hasConfidence: true,
                isPointing: false,
                handIndex: 0,
                primaryHandIndex: null as number | null,
                hysteresisHigh: 0.7,
                hysteresisLow: 0.3,
            };

            const idleGateClosed = w.hfoP2MirrorMagus.computeSovereignFsmNext({
                ...base,
                fsmState: 'IDLE',
                isFacingCamera: false,
            });

            const readyGateClosed = w.hfoP2MirrorMagus.computeSovereignFsmNext({
                ...base,
                fsmState: 'READY',
                isFacingCamera: false,
            });

            const commitGateClosed = w.hfoP2MirrorMagus.computeSovereignFsmNext({
                ...base,
                fsmState: 'COMMIT',
                isFacingCamera: false,
                primaryHandIndex: 0,
            });

            const readyToCommit = w.hfoP2MirrorMagus.computeSovereignFsmNext({
                ...base,
                fsmState: 'READY',
                isFacingCamera: true,
                isPointing: true,
                primaryHandIndex: null,
            });

            return {
                idleGateClosed,
                readyGateClosed,
                commitGateClosed,
                readyToCommit,
            };
        },
        undefined as any,
    );

    expect(res.idleGateClosed?.nextState).toBe('IDLE');

    expect(res.readyGateClosed?.nextState).toBe('IDLE');
    expect(res.readyGateClosed?.reason).toBe('p2_ready_gate_closed_to_idle');

    expect(res.commitGateClosed?.nextState).toBe('IDLE');
    expect(res.commitGateClosed?.reason).toBe('p2_commit_gate_closed_to_idle');
    expect(res.commitGateClosed?.nextPrimary).toBeNull();

    expect(res.readyToCommit?.nextState).toBe('COMMIT');
    expect(res.readyToCommit?.reason).toBe('p2_ready_to_commit');
    expect(res.readyToCommit?.nextPrimary).toBe(0);
});
