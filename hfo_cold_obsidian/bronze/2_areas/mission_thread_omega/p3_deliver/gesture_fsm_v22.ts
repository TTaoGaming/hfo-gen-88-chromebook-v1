// Medallion: Bronze | Mutation: 0% | HIVE: I
import { V22GestureFSMState, HandGestureSchema, GestureStateSchema } from '../contracts/v22_gesture.zod';

export class GestureFSMV22 {
    private state: V22GestureFSMState;
    private readonly DWELL_TIMEOUT = 1000; // ms - bit more stable
    private readonly SEQ_WINDOW = 1500; // ms

    constructor() {
        this.state = {
            currentState: 'IDLE',
            lastGesture: 'NONE',
            pointerEvent: 'none'
        };
    }

    public process(gesture: string, timestamp: number): V22GestureFSMState {
        // Normalize gesture string (e.g., "Open_Palm" or "open palm" -> "OPEN_PALM")
        const currentGesture = gesture.toUpperCase().replace(/[\s_]/g, '_') as any;
        this.state.pointerEvent = 'none';

        // 🛡️ Sequence Timeouts
        if (['SEQ_PALM', 'SEQ_GAP'].includes(this.state.currentState)) {
            if (this.state.commitSequenceStartTime && (timestamp - this.state.commitSequenceStartTime > this.SEQ_WINDOW)) {
                this.state.currentState = 'ARMED';
                this.state.commitSequenceStartTime = undefined;
            }
        }

        switch (this.state.currentState) {
            case 'IDLE':
                if (currentGesture === 'OPEN_PALM') {
                    this.state.currentState = 'ARMING';
                    this.state.dwellStartTime = timestamp;
                }
                break;

            case 'ARMING':
                if (currentGesture === 'OPEN_PALM') {
                    if (timestamp - (this.state.dwellStartTime || 0) > this.DWELL_TIMEOUT) {
                        this.state.currentState = 'ARMED';
                        this.state.dwellStartTime = undefined;
                    }
                } else if (currentGesture === 'NONE') {
                    // Let ARMING be slightly sticky to NONE
                } else {
                    this.state.currentState = 'IDLE';
                    this.state.dwellStartTime = undefined;
                }
                break;

            case 'ARMED':
                if (currentGesture === 'OPEN_PALM') {
                    this.state.currentState = 'SEQ_PALM';
                    this.state.commitSequenceStartTime = timestamp;
                } else if (currentGesture === 'NONE' || currentGesture === 'POINTING_UP') {
                    // Sticky ARMED resistant to NONE/PU
                } else if (currentGesture !== 'NONE') {
                    // High confidence other gesture -> pointercancel + IDLE
                    this.state.currentState = 'IDLE';
                    this.state.pointerEvent = 'pointercancel';
                }
                break;

            case 'SEQ_PALM':
                if (currentGesture === 'NONE') {
                    this.state.currentState = 'SEQ_GAP';
                } else if (currentGesture === 'OPEN_PALM') {
                    // Stay in SEQ_PALM
                } else {
                    this.state.currentState = 'ARMED';
                    this.state.commitSequenceStartTime = undefined;
                }
                break;

            case 'SEQ_GAP':
                if (currentGesture === 'POINTING_UP') {
                    this.state.currentState = 'COMMITTED';
                    this.state.pointerEvent = 'pointerdown';
                    this.state.commitSequenceStartTime = timestamp; // Reset for stickiness tracking
                } else if (currentGesture === 'NONE') {
                    // Stay in SEQ_GAP
                } else {
                    this.state.currentState = 'ARMED';
                    this.state.commitSequenceStartTime = undefined;
                }
                break;

            case 'COMMITTED':
                if (currentGesture === 'NONE' || currentGesture === 'POINTING_UP') {
                    // Stickiness: Survives NONE and PU flickers
                    this.state.pointerEvent = 'pointermove';
                } else if (currentGesture === 'OPEN_PALM') {
                    // Controlled Exit: Pointer Up -> back to ARMED
                    this.state.currentState = 'ARMED';
                    this.state.pointerEvent = 'pointerup';
                    this.state.commitSequenceStartTime = undefined;
                } else {
                    // High confidence Other -> pointercancel + IDLE
                    this.state.currentState = 'IDLE';
                    this.state.pointerEvent = 'pointercancel';
                    this.state.commitSequenceStartTime = undefined;
                }
                break;
        }

        this.state.lastGesture = currentGesture;
        return this.state;
    }

    public getState(): V22GestureFSMState {
        return { ...this.state };
    }
}
