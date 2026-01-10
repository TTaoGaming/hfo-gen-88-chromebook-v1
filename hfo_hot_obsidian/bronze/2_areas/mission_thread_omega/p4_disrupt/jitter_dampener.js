// Medallion: Bronze | Mutation: 0% | HIVE: E
// Port 4 (DISRUPT): Jitter Dampener
// Applies deadzone and rate limiting to reduce cursor shake

class JitterDampener {
    constructor(options = {}) {
        // Configuration
        this.deadzone = options.deadzone || 2.0; // pixels
        this.maxUpdateRate = options.maxUpdateRate || 60; // Hz
        this.minUpdateInterval = 1000 / this.maxUpdateRate; // ms
        this.hysteresisThreshold = options.hysteresisThreshold || 0.1; // For on/off transitions

        // State
        this.lastPosition = { x: 0, y: 0 };
        this.lastUpdateTime = 0;
        this.dampedPosition = { x: 0, y: 0 };
        this.correctionsApplied = 0;
        this.updatesBlocked = 0;
    }

    /**
     * Apply jitter dampening to incoming cursor position
     * @param {Object} position - { x, y } coordinates (normalized 0-1)
     * @param {number} timestamp - Current timestamp in ms
     * @returns {Object} - { shouldUpdate, dampedPosition, reason }
     */
    dampen(position, timestamp = Date.now()) {
        // Rate limiting check
        const timeSinceLastUpdate = timestamp - this.lastUpdateTime;
        if (timeSinceLastUpdate < this.minUpdateInterval) {
            this.updatesBlocked++;
            return {
                shouldUpdate: false,
                dampedPosition: this.dampedPosition,
                reason: 'rate_limited',
                timeSinceLastUpdate
            };
        }

        // Calculate movement delta
        const dx = position.x - this.lastPosition.x;
        const dy = position.y - this.lastPosition.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Deadzone check
        if (distance < this.deadzone / 1000) { // Convert px to normalized
            this.correctionsApplied++;
            return {
                shouldUpdate: false,
                dampedPosition: this.dampedPosition,
                reason: 'deadzone',
                distance
            };
        }

        // Update passed all checks
        this.lastPosition = { x: position.x, y: position.y };
        this.dampedPosition = { x: position.x, y: position.y };
        this.lastUpdateTime = timestamp;

        return {
            shouldUpdate: true,
            dampedPosition: this.dampedPosition,
            reason: 'passed',
            distance
        };
    }

    /**
     * Apply hysteresis to binary state transitions (e.g., gesture on/off)
     * Prevents rapid flickering between states
     * @param {number} value - Current value (0-1)
     * @param {boolean} currentState - Current binary state
     * @returns {boolean} - New state after hysteresis
     */
    applyHysteresis(value, currentState) {
        if (currentState) {
            // Currently ON - need to drop below threshold to turn OFF
            return value >= (0.5 - this.hysteresisThreshold);
        } else {
            // Currently OFF - need to rise above threshold to turn ON
            return value >= (0.5 + this.hysteresisThreshold);
        }
    }

    /**
     * Configure dampener parameters
     */
    configure(options) {
        if (options.deadzone !== undefined) this.deadzone = options.deadzone;
        if (options.maxUpdateRate !== undefined) {
            this.maxUpdateRate = options.maxUpdateRate;
            this.minUpdateInterval = 1000 / this.maxUpdateRate;
        }
        if (options.hysteresisThreshold !== undefined) {
            this.hysteresisThreshold = options.hysteresisThreshold;
        }

        console.log('[P4-DAMPENER] 🎛️ Reconfigured:', {
            deadzone: this.deadzone,
            maxUpdateRate: this.maxUpdateRate,
            hysteresisThreshold: this.hysteresisThreshold
        });
    }

    /**
     * Get jitter dampening telemetry
     */
    getTelemetry() {
        const totalAttempts = this.correctionsApplied + this.updatesBlocked;
        const dampeningRate = totalAttempts > 0 ? (this.correctionsApplied + this.updatesBlocked) / totalAttempts : 0;

        return {
            deadzone_px: this.deadzone,
            max_update_rate_hz: this.maxUpdateRate,
            corrections_applied: this.correctionsApplied,
            updates_blocked: this.updatesBlocked,
            dampening_rate: dampeningRate.toFixed(2),
            last_position: this.lastPosition,
            timestamp: Date.now()
        };
    }

    /**
     * Reset dampener state
     */
    reset() {
        this.lastPosition = { x: 0, y: 0 };
        this.dampedPosition = { x: 0, y: 0 };
        this.lastUpdateTime = 0;
        this.correctionsApplied = 0;
        this.updatesBlocked = 0;

        console.log('[P4-DAMPENER] 🔄 Reset');
    }

    /**
     * Log dampening statistics
     */
    logStats() {
        const telemetry = this.getTelemetry();
        console.log('[P4-DAMPENER] 📊 Stats:', telemetry);
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JitterDampener;
}
