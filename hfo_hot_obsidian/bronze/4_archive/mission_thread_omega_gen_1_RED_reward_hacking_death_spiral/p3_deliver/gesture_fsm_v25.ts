// Medallion: Bronze | Mutation: 0% | HIVE: I
import { V25GestureFSMState } from '../contracts/v25_gesture.zod';

export class GestureFSMV25 {
    private state: V25GestureFSMState;
    private readonly ARMING_THRESHOLD = 1000; // ms
    private readonly RECOVERY_TIMEOUT = 300; // ms
    private readonly CANCEL_DWELL = 50; // 3 frames approx
    private lastTimestamp: number = 0;

    constructor() {
        this.state = {
            currentState: 'IDLE',
            lastGesture: 'NONE',
            progress: 0,
            pointerEvent: 'none'
        };
    }

    public process(gesture: string, timestamp: number): V25GestureFSMState {
        const currentGesture = gesture.toUpperCase().replace(/[\s_]/g, '_') as any;
        const dt = this.lastTimestamp ? timestamp - this.lastTimestamp : 0;
        this.lastTimestamp = timestamp;
        this.state.pointerEvent = 'none';

        switch (this.state.currentState) {
            case 'IDLE':
                if (currentGesture === 'OPEN_PALM') {
                    this.state.currentState = 'ARMING';
                    this.state.progress = 0;
                }
                break;

            case 'ARMING':
                // Leaking Bucket Logic
                if (currentGesture === 'OPEN_PALM') {
                    this.state.progress += dt;
                } else {
                    this.state.progress -= dt * 2; // Drains twice as fast as it fills
                }

                this.state.progress = Math.max(0, this.state.progress);

                if (this.state.progress >= this.ARMING_THRESHOLD) {
                    this.state.currentState = 'ARMED';
                    this.state.progress = 0;
                } else if (this.state.progress === 0 && currentGesture !== 'OPEN_PALM') {
                    this.state.currentState = 'IDLE';
                }
                break;

            case 'ARMED':
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'POINTING_UP') {
                    // Instant confirm from ARMED (0ms dwell)
                    this.state.currentState = 'COMMITTED';
                    this.state.pointerEvent = 'pointerdown';
                } else if (currentGesture === 'NONE') {
                    // Enter prediction window
                    this.state.currentState = 'COMMITTING';
                    this.state.recoveryStartTime = timestamp;
                } else if (currentGesture === 'OPEN_PALM') {
                    this.state.recoveryStartTime = undefined;
                } else {
                    // Jitter recovery
                    if (!this.state.recoveryStartTime) this.state.recoveryStartTime = timestamp;
                    else if (timestamp - this.state.recoveryStartTime > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                }
                break;

            case 'COMMITTING':
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'POINTING_UP') {
                    // Latency reduction: 1-frame trigger
                    this.state.currentState = 'COMMITTED';
                    this.state.pointerEvent = 'pointerdown';
                    this.state.recoveryStartTime = undefined;
                } else if (currentGesture === 'OPEN_PALM') {
                    // Back to hover
                    this.state.currentState = 'ARMED';
                    this.state.recoveryStartTime = undefined;
                } else if (currentGesture === 'NONE') {
                    if (timestamp - (this.state.recoveryStartTime || 0) > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                } else {
                    // Change in gesture
                    this.state.currentState = 'IDLE';
                    this.state.pointerEvent = 'pointercancel';
                    this.state.recoveryStartTime = undefined;
                }
                break;

            case 'COMMITTED':
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'OPEN_PALM') {
                    // Enter Releasing bridge
                    this.state.currentState = 'RELEASING';
                    this.state.recoveryStartTime = timestamp;
                    this.state.dwellStartTime = timestamp;
                } else if (currentGesture === 'POINTING_UP') {
                    this.state.recoveryStartTime = undefined;
                } else {
                    // Jitter recovery while dragging
                    if (!this.state.recoveryStartTime) this.state.recoveryStartTime = timestamp;
                    else if (timestamp - this.state.recoveryStartTime > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                }
                break;

            case 'RELEASING':
                this.state.pointerEvent = 'pointermove';

                if (currentGesture === 'OPEN_PALM') {
                    // Confirm release (Pointer Up)
                    this.state.currentState = 'ARMED';
                    this.state.pointerEvent = 'pointerup';
                    this.state.recoveryStartTime = undefined;
                } else if (currentGesture === 'POINTING_UP') {
                    // Abort release, back to Drag
                    this.state.currentState = 'COMMITTED';
                    this.state.recoveryStartTime = undefined;
                } else if (currentGesture === 'NONE') {
                    if (timestamp - (this.state.recoveryStartTime || 0) > this.RECOVERY_TIMEOUT) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.recoveryStartTime = undefined;
                    }
                } else {
                    // Complex gesture change - 3 frame dwell before cancel
                    if (!this.state.dwellStartTime) this.state.dwellStartTime = timestamp;
                    else if (timestamp - this.state.dwellStartTime > this.CANCEL_DWELL) {
                        this.state.currentState = 'IDLE';
                        this.state.pointerEvent = 'pointercancel';
                        this.state.dwellStartTime = undefined;
                    }
                }
                break;
        }

        this.state.lastGesture = currentGesture;
        return this.state;
    }

    public getState(): V25GestureFSMState {
        return { ...this.state };
    }
}
