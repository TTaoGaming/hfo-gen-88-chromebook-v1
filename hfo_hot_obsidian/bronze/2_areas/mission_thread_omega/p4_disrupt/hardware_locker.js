// Medallion: Bronze | Mutation: 0% | HIVE: E
// Port 4 (DISRUPT): Hardware Cursor Locker
// Uses Pointer Lock API to capture and center physical mouse

class HardwareLocker {
    constructor() {
        this.isLocked = false;
        this.lockTarget = null;
        this.lockAttempts = 0;
        this.maxLockAttempts = 3;
        this.onLockChange = null;
        this.onLockError = null;

        // Bind pointer lock event listeners
        this._initListeners();
    }

    /**
     * Requests pointer lock on specified element
     * @param {HTMLElement} element - Element to lock pointer to (usually document.body)
     */
    async requestLock(element = document.body) {
        if (this.isLocked) {
            console.warn('[P4-LOCKER] Already locked');
            return { success: true, status: 'already_locked' };
        }

        this.lockTarget = element;
        this.lockAttempts++;

        try {
            console.log(`[P4-LOCKER] 🔒 Requesting pointer lock (attempt ${this.lockAttempts})`);
            await element.requestPointerLock();
            return { success: true, status: 'requested' };
        } catch (error) {
            console.error('[P4-LOCKER] ❌ Lock request failed:', error);
            
            if (this.lockAttempts >= this.maxLockAttempts) {
                this._triggerScream('pointer_lock_failed_max_attempts');
                return { success: false, status: 'max_attempts_exceeded', error };
            }

            return { success: false, status: 'request_failed', error };
        }
    }

    /**
     * Exits pointer lock
     */
    exitLock() {
        if (!this.isLocked) {
            console.warn('[P4-LOCKER] Not currently locked');
            return { success: false, status: 'not_locked' };
        }

        console.log('[P4-LOCKER] 🔓 Exiting pointer lock');
        document.exitPointerLock();
        return { success: true, status: 'exit_requested' };
    }

    /**
     * Gets hardware lock telemetry
     */
    getTelemetry() {
        return {
            is_locked: this.isLocked,
            lock_target: this.lockTarget ? this.lockTarget.tagName : null,
            lock_attempts: this.lockAttempts,
            pointer_lock_element: document.pointerLockElement ? document.pointerLockElement.tagName : null,
            timestamp: Date.now()
        };
    }

    /**
     * Initializes pointer lock event listeners
     * @private
     */
    _initListeners() {
        // Listen for pointer lock change
        document.addEventListener('pointerlockchange', () => {
            this.isLocked = document.pointerLockElement === this.lockTarget;
            
            if (this.isLocked) {
                console.log('[P4-LOCKER] ✅ Pointer lock acquired');
                this._logToBlackboard('lock_acquired');
            } else {
                console.log('[P4-LOCKER] 🔓 Pointer lock released');
                this._logToBlackboard('lock_released');
            }

            if (this.onLockChange) {
                this.onLockChange(this.isLocked);
            }
        });

        // Listen for pointer lock errors
        document.addEventListener('pointerlockerror', () => {
            console.error('[P4-LOCKER] ❌ Pointer lock error');
            this._triggerScream('pointer_lock_error');

            if (this.onLockError) {
                this.onLockError();
            }
        });
    }

    /**
     * Logs hardware lock events to stigmergy blackboard
     * @private
     */
    _logToBlackboard(event) {
        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'E',
            port: 'P4',
            module: 'hardware_locker',
            event: event,
            payload: this.getTelemetry()
        };

        console.log('[P4-LOCKER] 📝 Blackboard entry:', entry);
        // In production, this would write to hot_obsidian_blackboard.jsonl
    }

    /**
     * SCREAM Protocol: Trigger architectural violation
     * @private
     */
    _triggerScream(reason) {
        const violation = {
            timestamp: new Date().toISOString(),
            port: 'P4',
            module: 'hardware_locker',
            severity: 'HIGH',
            reason: reason,
            telemetry: this.getTelemetry()
        };

        console.error('[P4-LOCKER] 🚨 SCREAM:', violation);
        // In production, this would write to BOOK_OF_BLOOD_GRUDGES.jsonl
    }

    /**
     * Sets callback for lock state changes
     */
    setOnLockChange(callback) {
        this.onLockChange = callback;
    }

    /**
     * Sets callback for lock errors
     */
    setOnLockError(callback) {
        this.onLockError = callback;
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HardwareLocker;
}
