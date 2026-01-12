// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import { GestureFSMV22 } from '../p3_deliver/gesture_fsm_v22';

test.describe('Exhaustive GestureFSM V22 Stability', () => {

    test('Normalization: Different formats of Open Palm', () => {
        const fsm = new GestureFSMV22();
        expect(fsm.process('Open_Palm', 1000).currentState).toBe('ARMING');

        const fsm2 = new GestureFSMV22();
        expect(fsm2.process('open palm', 1000).currentState).toBe('ARMING');

        const fsm3 = new GestureFSMV22();
        expect(fsm3.process('OPEN PALM', 1000).currentState).toBe('ARMING');
    });

    test('ARMING: Should not transition before 1000ms', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000);

        // At 999ms after start
        let state = fsm.process('OPEN_PALM', 1999);
        expect(state.currentState).toBe('ARMING');

        // At 1001ms after start
        state = fsm.process('OPEN_PALM', 2001);
        expect(state.currentState).toBe('ARMED');
    });

    test('ARMING: Sticky to NONE noise', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000);

        // Flicker NONE
        fsm.process('NONE', 1500);
        expect(fsm.getState().currentState).toBe('ARMING');

        // Still ARMING even if NONE continues
        fsm.process('NONE', 2000);
        expect(fsm.getState().currentState).toBe('ARMING');

        // Back to OPEN_PALM -> Should ARMED immediately if total time passed
        let state = fsm.process('OPEN_PALM', 2100);
        expect(state.currentState).toBe('ARMED');
    });

    test('ARMED: Entering COMMITTING window on NONE', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2101); // -> ARMED

        // Transition from ARMED to NONE should enter COMMITTING
        expect(fsm.process('NONE', 2200).currentState).toBe('COMMITTING');
        expect(fsm.getState().pointerEvent).toBe('pointermove'); // Still hovering

        // After 100ms of NONE, still in COMMITTING
        expect(fsm.process('NONE', 2300).currentState).toBe('COMMITTING');

        // After 301ms (total from 2200), should timeout to IDLE
        expect(fsm.process('NONE', 2501).currentState).toBe('IDLE');
        expect(fsm.getState().pointerEvent).toBe('pointercancel');
    });

    test('Full Lookahead: ARMED -> COMMITTING -> COMMITTED', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2101); // -> ARMED

        // Enter window via NONE
        fsm.process('NONE', 2200);
        expect(fsm.getState().currentState).toBe('COMMITTING');

        // POINTING_UP for 50ms (not enough)
        fsm.process('POINTING_UP', 2250);
        expect(fsm.getState().currentState).toBe('COMMITTING');

        // POINTING_UP for 101ms (total since 2200 start of window)
        const state = fsm.process('POINTING_UP', 2301);
        expect(state.currentState).toBe('COMMITTED');
        expect(state.pointerEvent).toBe('pointerdown');
    });

    test('COMMITTING Abort: ARMED -> COMMITTING -> ARMED', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2101); // -> ARMED

        fsm.process('NONE', 2200);
        expect(fsm.getState().currentState).toBe('COMMITTING');

        // Abort by going back to Palm
        const state = fsm.process('OPEN_PALM', 2300);
        expect(state.currentState).toBe('ARMED');
        expect(state.pointerEvent).toBe('pointermove');
    });

    test('COMMITTED: Resistant to temporary NONE', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2101); // -> ARMED
        fsm.process('POINTING_UP', 2200); // -> COMMITTING
        fsm.process('POINTING_UP', 2301); // -> COMMITTED
        expect(fsm.getState().currentState).toBe('COMMITTED');

        expect(fsm.process('NONE', 2400).currentState).toBe('COMMITTED');
        expect(fsm.process('NONE', 2600).currentState).toBe('COMMITTED');

        // After 300ms of NONE (started at 2400), should go to IDLE
        expect(fsm.process('NONE', 2701).currentState).toBe('IDLE');
    });
});
