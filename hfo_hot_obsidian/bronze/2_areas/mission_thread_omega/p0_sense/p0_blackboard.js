// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🎯 PORT-0-SENSE: Blackboard Logger

/**
 * P0 Blackboard Logger
 * Logs all P0 events to the stigmergy blackboard
 * Provides provenance and audit trail
 */

export class P0BlackboardLogger {
    constructor(config = {}) {
        this.config = {
            enableLogging: true,
            logSensingEvents: false,  // High frequency, default off
            logGestureEvents: true,
            logLifecycleEvents: true,
            maxBufferSize: 100,
            ...config
        };

        this.buffer = [];
        this.eventCount = 0;
    }

    /**
     * Log P0 lifecycle event
     */
    logLifecycle(event, details = {}) {
        if (!this.config.enableLogging || !this.config.logLifecycleEvents) {
            return;
        }

        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'P',  // Port phase
            port: 'P0',
            event_type: 'lifecycle',
            event,
            details,
            medallion: 'Bronze',
            mission: 'ThreadOmega_V20'
        };

        this._writeEntry(entry);
    }

    /**
     * Log P0 sensing event
     */
    logSensing(sensingData) {
        if (!this.config.enableLogging || !this.config.logSensingEvents) {
            return;
        }

        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'P',
            port: 'P0',
            event_type: 'sensing',
            data: sensingData,
            medallion: 'Bronze',
            mission: 'ThreadOmega_V20'
        };

        this._writeEntry(entry);
    }

    /**
     * Log P0 gesture event
     */
    logGesture(gesture, confidence) {
        if (!this.config.enableLogging || !this.config.logGestureEvents) {
            return;
        }

        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'P',
            port: 'P0',
            event_type: 'gesture',
            gesture,
            confidence,
            medallion: 'Bronze',
            mission: 'ThreadOmega_V20'
        };

        this._writeEntry(entry);
    }

    /**
     * Log validation error
     */
    logValidationError(input, errors) {
        if (!this.config.enableLogging) {
            return;
        }

        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'P',
            port: 'P0',
            event_type: 'validation_error',
            input,
            errors,
            medallion: 'Bronze',
            mission: 'ThreadOmega_V20'
        };

        this._writeEntry(entry);
    }

    /**
     * Write entry to buffer
     */
    _writeEntry(entry) {
        this.eventCount++;
        this.buffer.push(entry);

        // Maintain buffer size
        if (this.buffer.length > this.config.maxBufferSize) {
            this.buffer.shift();
        }

        // Log to console in development
        console.log('[P0-BLACKBOARD]', JSON.stringify(entry));
    }

    /**
     * Get buffer contents
     */
    getBuffer() {
        return [...this.buffer];
    }

    /**
     * Clear buffer
     */
    clearBuffer() {
        this.buffer = [];
    }

    /**
     * Export buffer as JSONL
     */
    exportJSONL() {
        return this.buffer.map(entry => JSON.stringify(entry)).join('\n');
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            totalEvents: this.eventCount,
            bufferSize: this.buffer.length,
            config: this.config
        };
    }
}

// P0_VALIDATOR_ID: BLACKBOARD_LOGGER_V20
