// Medallion: Bronze | Mutation: 0% | HIVE: I
import { test, expect } from '@playwright/test';
import { GestureFSMV23 } from '../p3_deliver/gesture_fsm_v23';

test.describe('GestureFSM V23 Transitions', () => {
    test('should start in IDLE', () => {
        const fsm = new GestureFSMV23();
        expect(fsm.getState().currentState).toBe('IDLE');
    });

    test('should transition sequence: IDLE -> ARMING -> ARMED', () => {
        const fsm = new GestureFSMV23();

        // IDLE -> ARMING
        let state = fsm.process('OPEN_PALM', 1000);
        expect(state.currentState).toBe('ARMING');

        // ARMING -> ARMED (Dwell > 1000ms)
        state = fsm.process('OPEN_PALM', 2100);
        expect(state.currentState).toBe('ARMED');
    });

    test('should handle gesture normalization: Open_Palm -> OPEN_PALM', () => {
        const fsm = new GestureFSMV23();
        let state = fsm.process('Open_Palm', 1000);
        expect(state.currentState).toBe('ARMING');

        state = fsm.process('open palm', 2100);
        expect(state.currentState).toBe('ARMED');
    });

    test('ARMING should be sticky to NONE noise', () => {
        const fsm = new GestureFSMV23();
        fsm.process('OPEN_PALM', 1000);

        // 100ms later, NONE flicker
        fsm.process('NONE', 1100);
        expect(fsm.getState().currentState).toBe('ARMING');

        // 1000ms later, OPEN_PALM returns -> should ARMED (if > 1000ms since T=1000)
        let state = fsm.process('OPEN_PALM', 2100);
        expect(state.currentState).toBe('ARMED');
    });

    test('ARMING should reset to IDLE on high-confidence mismatch', () => {
        const fsm = new GestureFSMV23();
        fsm.process('OPEN_PALM', 1000);

        // Sudden Thumb Up
        let state = fsm.process('THUMBS_UP', 1100);
        expect(state.currentState).toBe('IDLE');

        // Start over
        state = fsm.process('OPEN_PALM', 1200);
        expect(state.currentState).toBe('ARMING');
    });

    test('should transition full commit sequence: ARMED -> SEQ_PALM -> SEQ_GAP -> COMMITTED', () => {
        const fsm = new GestureFSMV23();
        fsm.process('OPEN_PALM', 1000); // IDLE -> ARMING
        fsm.process('OPEN_PALM', 1900); // ARMING -> ARMED

        // ARMED -> SEQ_PALM
        let state = fsm.process('OPEN_PALM', 2000);
        expect(state.currentState).toBe('SEQ_PALM');

        // SEQ_PALM -> SEQ_GAP
        state = fsm.process('NONE', 2100);
        expect(state.currentState).toBe('SEQ_GAP');

        // SEQ_GAP -> COMMITTED
        state = fsm.process('POINTING_UP', 2200);
        expect(state.currentState).toBe('COMMITTED');
        expect(state.pointerEvent).toBe('pointerdown');
    });

    test('ARMED should be sticky to NONE and POINTING_UP', () => {
        const fsm = new GestureFSMV23();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 1900); // -> ARMED

        let state = fsm.process('NONE', 2000);
        expect(state.currentState).toBe('ARMED');

        state = fsm.process('POINTING_UP', 2100);
        expect(state.currentState).toBe('ARMED');
    });

    test('ARMED + HIGH_CONFIDENCE other should IDLE (Anti-Midas)', () => {
        const fsm = new GestureFSMV23();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 1900); // -> ARMED

        // Use a gesture that is definitely not NONE/PU/OP
        const state = fsm.process('VICTORY', 2000);
        expect(state.currentState).toBe('IDLE');
        expect(state.pointerEvent).toBe('pointercancel');
    });

    test('COMMITTED should be sticky and survive NONE', () => {
        const fsm = new GestureFSMV23();
        // Setup state to COMMITTED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 1900);
        fsm.process('OPEN_PALM', 2000); fsm.process('NONE', 2100);
        fsm.process('POINTING_UP', 2200);

        // COMMITTED + NONE -> COMMITTED
        const state = fsm.process('NONE', 2300);
        expect(state.currentState).toBe('COMMITTED');
        expect(state.pointerEvent).toBe('pointermove');
    });

    test('COMMITTED + OPEN_PALM should transition to ARMED with pointerup', () => {
        const fsm = new GestureFSMV23();
        // Setup state to COMMITTED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 1900);
        fsm.process('OPEN_PALM', 2000); fsm.process('NONE', 2100);
        fsm.process('POINTING_UP', 2200);

        const state = fsm.process('OPEN_PALM', 2300);
        expect(state.currentState).toBe('ARMED');
        expect(state.pointerEvent).toBe('pointerup');
    });

    test('COMMITTED + OTHER (CLOSE_FIST) should transition to IDLE with pointercancel', () => {
        const fsm = new GestureFSMV23();
        // Setup state to COMMITTED
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 1900);
        fsm.process('OPEN_PALM', 2000); fsm.process('NONE', 2100);
        fsm.process('POINTING_UP', 2200);

        const state = fsm.process('CLOSE_FIST', 2300);
        expect(state.currentState).toBe('IDLE');
        expect(state.pointerEvent).toBe('pointercancel');
    });
});
