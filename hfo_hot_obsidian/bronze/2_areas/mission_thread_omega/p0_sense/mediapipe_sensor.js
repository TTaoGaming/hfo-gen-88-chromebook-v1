// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🎯 PORT-0-SENSE: MediaPipe Sensor Core

/**
 * MediaPipe Hand Tracking Sensor
 * Manages camera initialization, hand detection, and landmark extraction
 * Outputs P0SensingSchema-compliant data
 */

export class MediaPipeSensor {
    constructor(config = {}) {
        this.videoElement = config.videoElement || null;
        this.canvasElement = config.canvasElement || null;
        this.canvasCtx = null;
        this.handLandmarker = null;
        this.gestureRecognizer = null;
        this.isInitialized = false;
        this.isRunning = false;
        this.eventTarget = new EventTarget();
        
        // MediaPipe configuration
        this.config = {
            runningMode: 'VIDEO',
            numHands: 1,
            minHandDetectionConfidence: 0.5,
            minHandPresenceConfidence: 0.5,
            minTrackingConfidence: 0.5,
            ...config
        };
    }

    /**
     * Initialize MediaPipe with event-driven approach
     * Emits 'initialized' event when ready
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('[P0-SENSE] Already initialized');
            return;
        }

        try {
            // Wait for vision bundle to load
            if (typeof vision === 'undefined') {
                throw new Error('[P0-SENSE] MediaPipe vision bundle not loaded');
            }

            // Initialize FilesetResolver
            const visionFileset = await vision.FilesetResolver.forVisionTasks(
                'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm'
            );

            // Create HandLandmarker
            this.handLandmarker = await vision.HandLandmarker.createFromOptions(visionFileset, {
                baseOptions: {
                    modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
                    delegate: 'GPU'
                },
                runningMode: this.config.runningMode,
                numHands: this.config.numHands,
                minHandDetectionConfidence: this.config.minHandDetectionConfidence,
                minHandPresenceConfidence: this.config.minHandPresenceConfidence,
                minTrackingConfidence: this.config.minTrackingConfidence
            });

            // Create GestureRecognizer
            this.gestureRecognizer = await vision.GestureRecognizer.createFromOptions(visionFileset, {
                baseOptions: {
                    modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task',
                    delegate: 'GPU'
                },
                runningMode: this.config.runningMode,
                numHands: this.config.numHands
            });

            // Setup canvas context if canvas provided
            if (this.canvasElement) {
                this.canvasCtx = this.canvasElement.getContext('2d');
            }

            this.isInitialized = true;
            this.eventTarget.dispatchEvent(new CustomEvent('initialized', { 
                detail: { timestamp: Date.now() } 
            }));
            
            console.log('[P0-SENSE] ✅ Initialized');
        } catch (error) {
            console.error('[P0-SENSE] ❌ Initialization failed:', error);
            this.eventTarget.dispatchEvent(new CustomEvent('error', { 
                detail: { error, timestamp: Date.now() } 
            }));
            throw error;
        }
    }

    /**
     * Start camera stream and hand tracking
     * Emits 'started' event when camera is ready
     */
    async start() {
        if (!this.isInitialized) {
            throw new Error('[P0-SENSE] Must initialize before starting');
        }

        if (this.isRunning) {
            console.warn('[P0-SENSE] Already running');
            return;
        }

        try {
            // Request camera access
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'user',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });

            if (!this.videoElement) {
                throw new Error('[P0-SENSE] Video element not provided');
            }

            this.videoElement.srcObject = stream;
            
            // Wait for video to be ready
            await new Promise((resolve) => {
                this.videoElement.addEventListener('loadeddata', resolve, { once: true });
            });

            this.isRunning = true;
            this.eventTarget.dispatchEvent(new CustomEvent('started', { 
                detail: { timestamp: Date.now() } 
            }));
            
            console.log('[P0-SENSE] ✅ Camera started');
        } catch (error) {
            console.error('[P0-SENSE] ❌ Camera start failed:', error);
            this.eventTarget.dispatchEvent(new CustomEvent('error', { 
                detail: { error, timestamp: Date.now() } 
            }));
            throw error;
        }
    }

    /**
     * Process a single frame and extract hand data
     * Returns P0SensingSchema-compliant data
     */
    processFrame(timestamp) {
        if (!this.isRunning || !this.videoElement) {
            return null;
        }

        try {
            // Detect hands
            const results = this.handLandmarker.detectForVideo(this.videoElement, timestamp);
            
            // Extract index tip (landmark 8) from first detected hand
            if (results.landmarks && results.landmarks.length > 0) {
                const hand = results.landmarks[0];
                const indexTip = hand[8]; // Index finger tip
                
                // Calculate confidence from handedness
                const confidence = results.handedness && results.handedness.length > 0
                    ? results.handedness[0][0].score
                    : 0.5;

                // Emit sensing event
                const sensingData = {
                    timestamp: timestamp || Date.now(),
                    source: 'mediapipe-hand-8',
                    coords: {
                        x: indexTip.x,
                        y: indexTip.y,
                        z: indexTip.z
                    },
                    confidence: confidence,
                    tuning: 'smooth' // Default preset
                };

                this.eventTarget.dispatchEvent(new CustomEvent('sensing', { 
                    detail: sensingData 
                }));

                return sensingData;
            }

            return null;
        } catch (error) {
            console.error('[P0-SENSE] Frame processing error:', error);
            return null;
        }
    }

    /**
     * Stop hand tracking and camera stream
     */
    stop() {
        if (!this.isRunning) {
            return;
        }

        if (this.videoElement && this.videoElement.srcObject) {
            const tracks = this.videoElement.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            this.videoElement.srcObject = null;
        }

        this.isRunning = false;
        this.eventTarget.dispatchEvent(new CustomEvent('stopped', { 
            detail: { timestamp: Date.now() } 
        }));
        
        console.log('[P0-SENSE] Stopped');
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

// P0_VALIDATOR_ID: MEDIAPIPE_SENSOR_V20
