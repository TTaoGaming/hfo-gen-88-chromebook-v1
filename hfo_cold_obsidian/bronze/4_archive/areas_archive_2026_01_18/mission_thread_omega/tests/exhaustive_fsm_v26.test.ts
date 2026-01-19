// Medallion: Bronze | Mutation: 0% | HIVE: I
import { test, expect } from '@playwright/test';
import { GestureFSMV25 } from '../p3_deliver/gesture_fsm_active';

test.describe('V25 Prefire FSM Stability', () => {

    test('ARMING: Leaking Bucket Logic', () => {
        const fsm = new GestureFSMV25();
        fsm.process('OPEN_PALM', 1000); // Start
        fsm.process('OPEN_PALM', 1500); // Progress = 500

        // Flicker to NONE for 100ms
        fsm.process('NONE', 1600); // Progress = 500 - 200 = 300
        expect(fsm.getState().progress).toBe(300);

        // Resume PALM
        fsm.process('OPEN_PALM', 1700); // Progress = 300 + 100 = 400
        expect(fsm.getState().progress).toBe(400);

        // Reach threshold
        fsm.process('OPEN_PALM', 2300); // 400 + 600 = 1000
        expect(fsm.getState().currentState).toBe('ARMED');
    });

    test('COMMITTING: Prefire Latency (0ms dwell on PU)', () => {
        const fsm = new GestureFSMV25();
        // Skip to ARMED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2000);

        // Palm -> NONE (COMMITTING)
        fsm.process('NONE', 2100);
        expect(fsm.getState().currentState).toBe('COMMITTING');

        // Instant PU confirm
        const state = fsm.process('POINTING_UP', 2110); // 10ms later
        expect(state.currentState).toBe('COMMITTED');
        expect(state.pointerEvent).toBe('pointerdown');
    });

    test('RELEASING: Prefire Symmetry', () => {
        const fsm = new GestureFSMV25();
        // Skip to COMMITTED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2000);
        fsm.process('POINTING_UP', 2100);

        // Drag -> PALM (RELEASING)
        fsm.process('OPEN_PALM', 2200);
        expect(fsm.getState().currentState).toBe('RELEASING');

        // Confirm UP
        const state = fsm.process('OPEN_PALM', 2210);
        expect(state.currentState).toBe('ARMED');
        expect(state.pointerEvent).toBe('pointerup');
    });

    test('RELEASING: 3-frame dwell confirm for cancel', () => {
        const fsm = new GestureFSMV25();
        // Skip to COMMITTED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2000);
        fsm.process('POINTING_UP', 2100);

        fsm.process('OPEN_PALM', 2200); // RELEASING

        // Switch to VICTORY (Anomalous)
        fsm.process('VICTORY', 2210); // Start cancel dwell
        expect(fsm.getState().currentState).toBe('RELEASING');

        // After 50ms (CANCEL_DWELL)
        const state = fsm.process('VICTORY', 2261);
        expect(state.currentState).toBe('IDLE');
        expect(state.pointerEvent).toBe('pointercancel');
    });
});
