// Medallion: Bronze | Mutation: 0% | HIVE: V
import { V23GestureFSMState } from '../contracts/v23_gesture.zod';

export class GestureFSMV23 {
    private state: V23GestureFSMState;
    private readonly DWELL_TIMEOUT = 1000; // ms for ARMING
    private readonly RECOVERY_TIMEOUT = 300; // ms - Survive none/jitter
    private readonly COMMIT_DWELL = 100; // ms - Short dwell for intent

    constructor() {
        this.state = {
            currentState: 'IDLE',
            lastGesture: 'NONE',
            pointerEvent: 'none'
        };
    }

    public process(gesture: string, timestamp: number): V23GestureFSMState {
        // Normalize gesture string
        const currentGesture = gesture.toUpperCase().replace(/[\s_]/g, '_') as any;
        this.state.pointerEvent = 'none';

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
                } else if (currentGesture === 'NONE' || currentGesture === 'POINTING_UP') {
                    // Arming is slightly sticky to noise
                } else {
                    this.state.currentState = 'IDLE';
                    this.state.dwellStartTime = undefined;
                }
                break;

            case 'ARMED':
                // Hovering mode
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'POINTING_UP' || currentGesture === 'NONE') {
                    // Enter COMMITTING lookahead window
                    this.state.currentState = 'COMMITTING';
                    this.state.recoveryStartTime = timestamp; // Used for lookahead timeout
                    this.state.dwellStartTime = timestamp;    // Used for commit dwell
                } else if (currentGesture === 'OPEN_PALM') {
                    // Stable state
                    this.state.recoveryStartTime = undefined;
                    this.state.dwellStartTime = undefined;
                } else {
                    // Enter recovery on other Jitter
                    this.state.dwellStartTime = undefined;
                    if (!this.state.recoveryStartTime) {
                        this.state.recoveryStartTime = timestamp;
                    } else if (timestamp - this.state.recoveryStartTime > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                }
                break;

            case 'COMMITTING':
                // Hovering mode (lookahead window)
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'POINTING_UP') {
                    // Check if we've dwelled long enough to confirm intent
                    if (timestamp - (this.state.dwellStartTime || 0) > this.COMMIT_DWELL) {
                        this.state.currentState = 'COMMITTED';
                        this.state.pointerEvent = 'pointerdown';
                        this.state.recoveryStartTime = undefined;
                        this.state.dwellStartTime = undefined;
                    }
                } else if (currentGesture === 'OPEN_PALM') {
                    // Intent aborted, back to ARMED
                    this.state.currentState = 'ARMED';
                    this.state.recoveryStartTime = undefined;
                    this.state.dwellStartTime = undefined;
                } else if (currentGesture === 'NONE') {
                    // Still in the window, wait for POINTING_UP
                    if (timestamp - (this.state.recoveryStartTime || 0) > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                        this.state.dwellStartTime = undefined;
                    }
                } else {
                    // Hard reset on other gestures (Victory, etc)
                    this.state.currentState = 'IDLE';
                    this.state.pointerEvent = 'pointercancel';
                    this.state.recoveryStartTime = undefined;
                    this.state.dwellStartTime = undefined;
                }
                break;

            case 'COMMITTED':
                // Dragging mode
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'OPEN_PALM') {
                    // Start transition back to ARMED (Pointer Up)
                    if (!this.state.dwellStartTime) {
                        this.state.dwellStartTime = timestamp;
                    } else if (timestamp - this.state.dwellStartTime > this.COMMIT_DWELL) {
                        this.state.currentState = 'ARMED';
                        this.state.pointerEvent = 'pointerup';
                        this.state.dwellStartTime = undefined;
                        this.state.recoveryStartTime = undefined;
                    }
                } else if (currentGesture === 'POINTING_UP') {
                    // Stable state
                    this.state.recoveryStartTime = undefined;
                    this.state.dwellStartTime = undefined;
                } else {
                    // Enter recovery on NONE or other Jitter
                    this.state.dwellStartTime = undefined;
                    if (!this.state.recoveryStartTime) {
                        this.state.recoveryStartTime = timestamp;
                    } else if (timestamp - this.state.recoveryStartTime > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                }
                break;
        }

        this.state.lastGesture = currentGesture;
        return this.state;
    }

    public getState(): V23GestureFSMState {
        return { ...this.state };
    }
}
