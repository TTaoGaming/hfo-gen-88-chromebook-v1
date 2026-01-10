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

    test('ARMED: Resistant to NONE and POINTING_UP flickers', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2100); // -> ARMED
        
        expect(fsm.process('NONE', 2200).currentState).toBe('ARMED');
        expect(fsm.process('POINTING_UP', 2300).currentState).toBe('ARMED');
        expect(fsm.process('NONE', 2400).currentState).toBe('ARMED');
    });

    test('Full Sequence: OP -> NONE -> PU', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2100); // -> ARMED
        
        expect(fsm.process('OPEN_PALM', 3000).currentState).toBe('SEQ_PALM');
        expect(fsm.process('NONE', 3100).currentState).toBe('SEQ_GAP');
        expect(fsm.process('POINTING_UP', 3200).currentState).toBe('COMMITTED');
        expect(fsm.getState().pointerEvent).toBe('pointerdown');
    });

    test('Sequence Timeout: Should revert to ARMED if too slow', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2100); // -> ARMED
        
        fsm.process('OPEN_PALM', 3000); // -> SEQ_PALM
        
        // Wait > 1500ms
        let state = fsm.process('NONE', 4600);
        expect(state.currentState).toBe('ARMED');
    });

    test('Anti-Midas: Rejection during Sequence', () => {
        const fsm = new GestureFSMV22();
        fsm.process('OPEN_PALM', 1000); fsm.process('OPEN_PALM', 2100); // -> ARMED
        
        fsm.process('OPEN_PALM', 3000); // -> SEQ_PALM
        
        // Sudden THUMBS_UP
        let state = fsm.process('THUMBS_UP', 3100);
        expect(state.currentState).toBe('ARMED'); // Reverts to ARMED, not IDLE, because it's a sequence failure
    });
});
