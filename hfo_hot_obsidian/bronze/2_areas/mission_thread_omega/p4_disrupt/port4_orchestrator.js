// Medallion: Bronze | Mutation: 0% | HIVE: E
// Port 4 (DISRUPT): Main Orchestrator
// Coordinates all disruption modules to establish virtual cursor dominance

class Port4Disrupt {
    constructor() {
        // Module instances (lazy-loaded when needed)
        this.suppressor = null;
        this.dampener = null;
        this.locker = null;
        this.rejector = null;

        // State
        this.isActive = false;
        this.violationsDetected = 0;
        this.lastViolationReason = null;

        console.log('[P4-DISRUPT] 🎯 Port 4 orchestrator initialized');
    }

    /**
     * Initializes all Port 4 modules
     */
    async initialize() {
        console.log('[P4-DISRUPT] ⚙️ Initializing disruption modules...');

        // Dynamically import modules (assuming they're loaded)
        try {
            this.suppressor = new PointerSuppressor();
            this.dampener = new JitterDampener({
                deadzone: 2.0,
                maxUpdateRate: 60,
                hysteresisThreshold: 0.1
            });
            this.locker = new HardwareLocker();
            this.rejector = new NativeRejector();

            console.log('[P4-DISRUPT] ✅ All modules initialized');
            return { success: true };
        } catch (error) {
            console.error('[P4-DISRUPT] ❌ Initialization failed:', error);
            this._triggerScream('module_initialization_failed', error.message);
            return { success: false, error };
        }
    }

    /**
     * Activates full disruption suite
     * Call this when virtual cursor becomes active
     */
    async activate() {
        if (this.isActive) {
            console.warn('[P4-DISRUPT] Already active');
            return { success: false, reason: 'already_active' };
        }

        console.log('[P4-DISRUPT] 🚀 Activating full disruption suite...');

        try {
            // Step 1: Activate pointer suppression
            this.suppressor.activate();

            // Step 2: Request hardware lock
            const lockResult = await this.locker.requestLock();
            if (!lockResult.success) {
                console.warn('[P4-DISRUPT] ⚠️ Hardware lock failed, continuing anyway');
            }

            // Step 3: Activate native event rejection
            this.rejector.activate();

            // Step 4: Reset dampener state
            this.dampener.reset();

            this.isActive = true;
            this._logToBlackboard('port_4_activated');

            console.log('[P4-DISRUPT] ✅ Full disruption suite active');
            return { success: true };
        } catch (error) {
            console.error('[P4-DISRUPT] ❌ Activation failed:', error);
            this._triggerScream('activation_failed', error.message);
            return { success: false, error };
        }
    }

    /**
     * Deactivates full disruption suite
     * Call this when virtual cursor is no longer active
     */
    deactivate() {
        if (!this.isActive) {
            console.warn('[P4-DISRUPT] Not active');
            return { success: false, reason: 'not_active' };
        }

        console.log('[P4-DISRUPT] 🛑 Deactivating disruption suite...');

        try {
            // Deactivate in reverse order
            this.rejector.deactivate();
            this.locker.exitLock();
            this.suppressor.deactivate();

            this.isActive = false;
            this._logToBlackboard('port_4_deactivated');

            console.log('[P4-DISRUPT] ✅ Disruption suite deactivated');
            return { success: true };
        } catch (error) {
            console.error('[P4-DISRUPT] ❌ Deactivation failed:', error);
            this._triggerScream('deactivation_failed', error.message);
            return { success: false, error };
        }
    }

    /**
     * Processes incoming data from Port 3 (DELIVER)
     * Applies jitter dampening and determines if updates should propagate
     * @param {Object} p3Data - Data from Port 3 FSM
     * @returns {Object} - Processed data for Port 5
     */
    process(p3Data) {
        if (!this.isActive) {
            return {
                success: false,
                reason: 'port_4_not_active',
                data: null
            };
        }

        // Apply jitter dampening to cursor position
        const dampenResult = this.dampener.dampen(
            p3Data.cursor_position,
            p3Data.timestamp
        );

        // Build P4 to P5 contract data
        const p4ToP5Data = {
            port_status: this._determinePortStatus(),
            suppressor: this.suppressor.getTelemetry(),
            dampener: this.dampener.getTelemetry(),
            locker: this.locker.getTelemetry(),
            rejector: this.rejector.getTelemetry(),
            total_disruptions: this._calculateTotalDisruptions(),
            disruption_effectiveness: this._calculateEffectiveness(),
            virtual_cursor_active: this.isActive,
            native_cursor_suppressed: this.suppressor.isActive,
            violations_detected: this.violationsDetected,
            last_violation_reason: this.lastViolationReason,
            timestamp: Date.now(),
            medallion: 'bronze'
        };

        return {
            success: true,
            shouldUpdate: dampenResult.shouldUpdate,
            dampedPosition: dampenResult.dampedPosition,
            dampenReason: dampenResult.reason,
            p3Data: p3Data,
            p4Telemetry: p4ToP5Data
        };
    }

    /**
     * Whitelist UI elements that should remain interactive
     * (e.g., settings panels, debug controls)
     */
    whitelistUIElement(element) {
        if (this.suppressor) {
            this.suppressor.whitelistElement(element);
        }
    }

    /**
     * Configure jitter dampener parameters
     */
    configureDampener(options) {
        if (this.dampener) {
            this.dampener.configure(options);
        }
    }

    /**
     * Gets comprehensive Port 4 telemetry
     */
    getTelemetry() {
        if (!this.suppressor || !this.dampener || !this.locker || !this.rejector) {
            return { error: 'Modules not initialized' };
        }

        return {
            port_status: this._determinePortStatus(),
            is_active: this.isActive,
            modules: {
                suppressor: this.suppressor.getTelemetry(),
                dampener: this.dampener.getTelemetry(),
                locker: this.locker.getTelemetry(),
                rejector: this.rejector.getTelemetry()
            },
            total_disruptions: this._calculateTotalDisruptions(),
            disruption_effectiveness: this._calculateEffectiveness(),
            violations_detected: this.violationsDetected,
            last_violation_reason: this.lastViolationReason
        };
    }

    /**
     * Determines overall port status
     * @private
     */
    _determinePortStatus() {
        if (!this.isActive) return 'offline';
        if (!this.locker.isLocked) return 'degraded';
        return 'online';
    }

    /**
     * Calculates total disruptions across all modules
     * @private
     */
    _calculateTotalDisruptions() {
        return (
            this.suppressor.nativeEventsBlocked +
            this.dampener.correctionsApplied +
            this.dampener.updatesBlocked +
            this.rejector.rejectionCount
        );
    }

    /**
     * Calculates disruption effectiveness (0-1)
     * @private
     */
    _calculateEffectiveness() {
        if (!this.isActive) return 0;

        const metrics = [
            this.suppressor.isActive ? 1 : 0,
            this.locker.isLocked ? 1 : 0,
            this.rejector.isActive ? 1 : 0,
            this.dampener.correctionsApplied > 0 ? 1 : 0
        ];

        return metrics.reduce((sum, val) => sum + val, 0) / metrics.length;
    }

    /**
     * Logs to stigmergy blackboard
     * @private
     */
    _logToBlackboard(event) {
        const entry = {
            timestamp: new Date().toISOString(),
            phase: 'E',
            port: 'P4',
            event: event,
            payload: this.getTelemetry()
        };

        console.log('[P4-DISRUPT] 📝 Blackboard:', entry);
        // In production, write to hot_obsidian_blackboard.jsonl
    }

    /**
     * SCREAM Protocol: Trigger architectural violation
     * @private
     */
    _triggerScream(reason, details = null) {
        this.violationsDetected++;
        this.lastViolationReason = reason;

        const violation = {
            timestamp: new Date().toISOString(),
            port: 'P4',
            severity: 'HIGH',
            reason: reason,
            details: details,
            telemetry: this.getTelemetry()
        };

        console.error('[P4-DISRUPT] 🚨 SCREAM:', violation);
        // In production, write to BOOK_OF_BLOOD_GRUDGES.jsonl
    }

    /**
     * Logs comprehensive statistics
     */
    logStats() {
        console.log('[P4-DISRUPT] 📊 Port 4 Statistics');
        console.log('========================================');
        
        const telemetry = this.getTelemetry();
        console.log('Port Status:', telemetry.port_status);
        console.log('Active:', telemetry.is_active);
        console.log('Total Disruptions:', telemetry.total_disruptions);
        console.log('Effectiveness:', (telemetry.disruption_effectiveness * 100).toFixed(1) + '%');
        console.log('Violations:', telemetry.violations_detected);
        
        console.log('\n--- Modules ---');
        console.log('Suppressor:', telemetry.modules.suppressor);
        console.log('Dampener:', telemetry.modules.dampener);
        console.log('Locker:', telemetry.modules.locker);
        console.log('Rejector:', telemetry.modules.rejector);
        
        console.log('========================================');
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Port4Disrupt;
}
