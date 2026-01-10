// Medallion: Bronze | Mutation: 0% | HIVE: E
// Port 4 (DISRUPT): Core Pointer Suppression
// Blocks native mouse events and establishes virtual cursor dominance

class PointerSuppressor {
    constructor() {
        this.isActive = false;
        this.nativeEventsBlocked = 0;
        this.eventTypes = ['mousemove', 'mousedown', 'mouseup', 'click', 'dblclick', 'contextmenu'];
        this.whitelistedElements = new Set(); // Elements exempt from suppression (e.g., UI controls)
        this.handlers = new Map();
    }

    /**
     * Activates pointer suppression
     * Hides native cursor and blocks mouse events
     */
    activate() {
        if (this.isActive) {
            console.warn('[P4-DISRUPT] Suppressor already active');
            return;
        }

        console.log('[P4-DISRUPT] 🛡️ Activating pointer suppression');

        // Hide native cursor
        document.body.style.cursor = 'none';

        // Install event blockers in capture phase (highest priority)
        this.eventTypes.forEach(eventType => {
            const handler = this._createBlockingHandler(eventType);
            this.handlers.set(eventType, handler);
            document.addEventListener(eventType, handler, { capture: true, passive: false });
        });

        this.isActive = true;
        this._logToBlackboard('suppression_activated');
    }

    /**
     * Deactivates pointer suppression
     * Restores native cursor and removes event blocks
     */
    deactivate() {
        if (!this.isActive) {
            console.warn('[P4-DISRUPT] Suppressor not active');
            return;
        }

        console.log('[P4-DISRUPT] 🔓 Deactivating pointer suppression');

        // Restore native cursor
        document.body.style.cursor = 'default';

        // Remove event blockers
        this.eventTypes.forEach(eventType => {
            const handler = this.handlers.get(eventType);
            if (handler) {
                document.removeEventListener(eventType, handler, { capture: true });
            }
        });
        this.handlers.clear();

        this.isActive = false;
        this._logToBlackboard('suppression_deactivated');
    }

    /**
     * Adds an element to the whitelist (exempt from suppression)
     * Useful for UI controls like settings panels
     */
    whitelistElement(element) {
        this.whitelistedElements.add(element);
        console.log('[P4-DISRUPT] ✅ Whitelisted element:', element);
    }

    /**
     * Removes an element from the whitelist
     */
    unwhitelistElement(element) {
        this.whitelistedElements.delete(element);
        console.log('[P4-DISRUPT] ❌ Removed element from whitelist:', element);
    }

    /**
     * Gets telemetry data for Port 5 (DEFEND)
     */
    getTelemetry() {
        return {
            is_active: this.isActive,
            native_events_blocked: this.nativeEventsBlocked,
            whitelisted_elements_count: this.whitelistedElements.size,
            timestamp: Date.now()
        };
    }

    /**
     * Creates a blocking event handler for a specific event type
     * @private
     */
    _createBlockingHandler(eventType) {
        return (event) => {
            // Check if event originated from whitelisted element
            let target = event.target;
            while (target) {
                if (this.whitelistedElements.has(target)) {
                    // Allow event for whitelisted elements
                    return;
                }
                target = target.parentElement;
            }

            // Block the native event
            event.stopImmediatePropagation();
            event.preventDefault();
            this.nativeEventsBlocked++;

            // Log every 100 blocks to avoid spam
            if (this.nativeEventsBlocked % 100 === 0) {
                console.log(`[P4-DISRUPT] 🚫 Blocked ${this.nativeEventsBlocked} native events`);
            }
        };
    }

    /**
     * Logs suppression events to stigmergy blackboard
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

        console.log('[P4-DISRUPT] 📝 Blackboard entry:', entry);
        // In production, this would write to hot_obsidian_blackboard.jsonl
    }

    /**
     * SCREAM Protocol: Detect and log architectural violations
     */
    detectViolation(reason) {
        const violation = {
            timestamp: new Date().toISOString(),
            port: 'P4',
            severity: 'HIGH',
            reason: reason,
            telemetry: this.getTelemetry()
        };

        console.error('[P4-DISRUPT] 🚨 ARCHITECTURAL VIOLATION:', violation);
        // In production, this would write to BOOK_OF_BLOOD_GRUDGES.jsonl
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PointerSuppressor;
}
