// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🎯 PORT-0-SENSE: Event-Driven Lifecycle Manager

/**
 * P0 Lifecycle Manager
 * Manages initialization sequence with proper event handling
 * Prevents race conditions identified in forensic analysis
 */

export class P0LifecycleManager {
    constructor() {
        this.state = 'uninitialized'; // uninitialized -> initializing -> ready -> running -> stopped
        this.eventTarget = new EventTarget();
        this.components = new Map();
        this.initializationOrder = [];
    }

    /**
     * Register a component with initialization callback
     */
    registerComponent(name, initFn) {
        this.components.set(name, {
            name,
            initFn,
            initialized: false,
            error: null
        });
        this.initializationOrder.push(name);
    }

    /**
     * Initialize all registered components in sequence
     */
    async initialize() {
        if (this.state !== 'uninitialized') {
            console.warn('[P0-LIFECYCLE] Already initialized or initializing');
            return;
        }

        this.state = 'initializing';
        this.eventTarget.dispatchEvent(new CustomEvent('stateChange', {
            detail: { state: this.state, timestamp: Date.now() }
        }));

        try {
            // Initialize components in registered order
            for (const name of this.initializationOrder) {
                const component = this.components.get(name);
                
                console.log(`[P0-LIFECYCLE] Initializing ${name}...`);
                this.eventTarget.dispatchEvent(new CustomEvent('componentInitializing', {
                    detail: { component: name, timestamp: Date.now() }
                }));

                try {
                    await component.initFn();
                    component.initialized = true;
                    
                    console.log(`[P0-LIFECYCLE] ✅ ${name} initialized`);
                    this.eventTarget.dispatchEvent(new CustomEvent('componentInitialized', {
                        detail: { component: name, timestamp: Date.now() }
                    }));
                } catch (error) {
                    component.error = error;
                    console.error(`[P0-LIFECYCLE] ❌ ${name} failed:`, error);
                    
                    this.eventTarget.dispatchEvent(new CustomEvent('componentError', {
                        detail: { component: name, error, timestamp: Date.now() }
                    }));
                    
                    throw new Error(`Component ${name} initialization failed: ${error.message}`);
                }
            }

            this.state = 'ready';
            this.eventTarget.dispatchEvent(new CustomEvent('stateChange', {
                detail: { state: this.state, timestamp: Date.now() }
            }));
            
            this.eventTarget.dispatchEvent(new CustomEvent('ready', {
                detail: { timestamp: Date.now() }
            }));
            
            console.log('[P0-LIFECYCLE] ✅ All components ready');
        } catch (error) {
            this.state = 'error';
            this.eventTarget.dispatchEvent(new CustomEvent('stateChange', {
                detail: { state: this.state, error, timestamp: Date.now() }
            }));
            throw error;
        }
    }

    /**
     * Mark system as running
     */
    start() {
        if (this.state !== 'ready') {
            throw new Error(`[P0-LIFECYCLE] Cannot start from state: ${this.state}`);
        }

        this.state = 'running';
        this.eventTarget.dispatchEvent(new CustomEvent('stateChange', {
            detail: { state: this.state, timestamp: Date.now() }
        }));
        
        console.log('[P0-LIFECYCLE] ✅ System running');
    }

    /**
     * Stop the system
     */
    stop() {
        if (this.state !== 'running') {
            console.warn(`[P0-LIFECYCLE] Cannot stop from state: ${this.state}`);
            return;
        }

        this.state = 'stopped';
        this.eventTarget.dispatchEvent(new CustomEvent('stateChange', {
            detail: { state: this.state, timestamp: Date.now() }
        }));
        
        console.log('[P0-LIFECYCLE] Stopped');
    }

    /**
     * Get current state
     */
    getState() {
        return this.state;
    }

    /**
     * Check if component is initialized
     */
    isComponentInitialized(name) {
        const component = this.components.get(name);
        return component ? component.initialized : false;
    }

    /**
     * Add event listener
     */
    on(event, callback) {
        this.eventTarget.addEventListener(event, callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        this.eventTarget.removeEventListener(event, callback);
    }
}

// P0_VALIDATOR_ID: LIFECYCLE_MANAGER_V20
