// Medallion: Bronze | Mutation: 0% | HIVE: I
import { test, expect } from '@playwright/test';
import { GestureFSM } from '../p3_deliver/gesture_fsm';

test.describe('GestureFSM Transitions', () => {
    test('should start in IDLE', () => {
        const fsm = new GestureFSM();
        expect(fsm.getState().currentState).toBe('IDLE');
    });

    test('should transition to PENDING on OPEN_PALM', () => {
        const fsm = new GestureFSM();
        const state = fsm.process('OPEN_PALM', 1000);
        expect(state.currentState).toBe('PENDING');
        expect(state.dwellStartTime).toBe(1000);
    });

    test('should transition to ARMING after dwell timeout', () => {
        const fsm = new GestureFSM();
        fsm.process('OPEN_PALM', 1000);
        const state = fsm.process('OPEN_PALM', 1600); // 1600 - 1000 > 500
        expect(state.currentState).toBe('ARMING');
    });

    test('should return to IDLE if gesture lost during PENDING', () => {
        const fsm = new GestureFSM();
        fsm.process('OPEN_PALM', 1000);
        const state2 = fsm.process('CLOSE_FIST', 1200);
        expect(state2.currentState).toBe('IDLE');
    });

    test('should transition to COMMITTING on POINTING_UP when ARMING', () => {
        const fsm = new GestureFSM();
        fsm.process('OPEN_PALM', 1000);
        fsm.process('OPEN_PALM', 1600);
        const state = fsm.process('POINTING_UP', 1700);
        expect(state.currentState).toBe('COMMITTING');
        expect(state.pointerEvent).toBe('pointerdown');
    });

    test('should trigger pointerup and return to ARMING on OPEN_PALM in COMMITTING', () => {
        const fsm = new GestureFSM();
        fsm.process('OPEN_PALM', 1000);
        fsm.process('OPEN_PALM', 1600);
        fsm.process('POINTING_UP', 1700);
        const state = fsm.process('OPEN_PALM', 1800);
        expect(state.currentState).toBe('ARMING');
        expect(state.pointerEvent).toBe('pointerup');
    });

    test('should timeout to IDLE if gesture lost in COMMITTING', () => {
        const fsm = new GestureFSM();
        fsm.process('OPEN_PALM', 1000);
        fsm.process('OPEN_PALM', 1600);
        fsm.process('POINTING_UP', 1700);
        fsm.process('NONE', 1800);
        const state = fsm.process('NONE', 3000);
        expect(state.currentState).toBe('IDLE');
        expect(state.pointerEvent).toBe('pointercancel');
    });
});
