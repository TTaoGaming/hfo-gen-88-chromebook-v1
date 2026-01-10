// Medallion: Bronze | Mutation: 0% | HIVE: E
// Port 4 (DISRUPT): Native Event Rejector
// Hijacks and blocks native pointer events to ensure virtual cursor dominance

class NativeRejector {
    constructor() {
        this.isActive = false;
        this.rejectionCount = 0;
        this.eventLog = []; // Recent rejections for debugging
        this.maxLogSize = 100;
        this.rejectedEventTypes = [
            'mousemove',
            'mousedown',
            'mouseup',
            'click',
            'dblclick',
            'contextmenu',
            'wheel',
            'pointerdown',
            'pointerup',
            'pointermove'
        ];
        this.handlers = new Map();
    }

    /**
     * Activates native event rejection
     * Installs high-priority event blockers
     */
    activate() {
        if (this.isActive) {
            console.warn('[P4-REJECTOR] Already active');
            return;
        }

        console.log('[P4-REJECTOR] 🚫 Activating native event rejection');

        // Install rejectors for each event type
        this.rejectedEventTypes.forEach(eventType => {
            const handler = this._createRejectionHandler(eventType);
            this.handlers.set(eventType, handler);

            // Use capture phase (true) and non-passive to ensure we can preventDefault
            window.addEventListener(eventType, handler, {
                capture: true,
                passive: false
            });
        });

        this.isActive = true;
        this._logToBlackboard('rejection_activated');
    }

    /**
     * Deactivates native event rejection
     * Removes all event blockers
     */
    deactivate() {
        if (!this.isActive) {
            console.warn('[P4-REJECTOR] Not active');
            return;
        }

        console.log('[P4-REJECTOR] ✅ Deactivating native event rejection');

        // Remove all handlers
        this.rejectedEventTypes.forEach(eventType => {
            const handler = this.handlers.get(eventType);
            if (handler) {
                window.removeEventListener(eventType, handler, {
                    capture: true
                });
            }
        });

        this.handlers.clear();
        this.isActive = false;
        this._logToBlackboard('rejection_deactivated');
    }

    /**
     * Creates a rejection handler for a specific event type
     * @private
     */
    _createRejectionHandler(eventType) {
        return (event) => {
            // Check if event should be allowed (e.g., synthetic events from Port 3)
            if (event.isTrusted === false && event.pointerType === 'virtual-physics') {
                // This is a synthetic event from our virtual cursor - allow it
                return;
            }

            // Reject native event
            event.stopImmediatePropagation();
            event.preventDefault();

            this.rejectionCount++;

            // Log to event log (for debugging)
            this._logRejection(eventType, event);

            // Periodic logging
            if (this.rejectionCount % 100 === 0) {
                console.log(`[P4-REJECTOR] 🚫 Rejected ${this.rejectionCount} native events`);
            }
        };
    }

    /**
     * Logs rejected event to circular buffer
     * @private
     */
    _logRejection(eventType, event) {
        const rejection = {
            type: eventType,
            timestamp: Date.now(),
            clientX: event.clientX,
            clientY: event.clientY,
            target: event.target?.tagName,
            isTrusted: event.isTrusted
        };

        this.eventLog.push(rejection);

        // Maintain circular buffer
        if (this.eventLog.length > this.maxLogSize) {
            this.eventLog.shift();
        }
    }

    /**
     * Gets recent rejection log for debugging
     */
    getRecentRejections(count = 10) {
        return this.eventLog.slice(-count);
    }

    /**
     * Gets telemetry data
     */
    getTelemetry() {
        return {
            is_active: this.isActive,
            rejection_count: this.rejectionCount,
            rejection_rate_per_sec: this._calculateRejectionRate(),
            rejected_event_types: this.rejectedEventTypes,
            recent_rejections: this.getRecentRejections(5),
            timestamp: Date.now()
        };
    }

    /**
     * Calculates rejection rate per second
     * @private
     */
    _calculateRejectionRate() {
        if (this.eventLog.length < 2) return 0;

        const oldest = this.eventLog[0].timestamp;
        const newest = this.eventLog[this.eventLog.length - 1].timestamp;
        const durationSec = (newest - oldest) / 1000;

        return durationSec > 0 ? (this.eventLog.length / durationSec).toFixed(2) : 0;
    }

    /**
     * Logs rejection events to stigmergy blackboard
     * @private
     */
    _logToBlackboard(event) {
        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'E',
            port: 'P4',
            module: 'native_rejector',
            event: event,
            payload: this.getTelemetry()
        };

        console.log('[P4-REJECTOR] 📝 Blackboard entry:', entry);
        // In production, this would write to hot_obsidian_blackboard.jsonl
    }

    /**
     * Resets rejection counters and log
     */
    reset() {
        this.rejectionCount = 0;
        this.eventLog = [];
        console.log('[P4-REJECTOR] 🔄 Reset');
    }

    /**
     * Logs current statistics
     */
    logStats() {
        const telemetry = this.getTelemetry();
        console.log('[P4-REJECTOR] 📊 Stats:', telemetry);
        console.table(this.getRecentRejections(10));
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NativeRejector;
}
