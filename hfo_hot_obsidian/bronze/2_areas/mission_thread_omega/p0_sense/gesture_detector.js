// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🎯 PORT-0-SENSE: Gesture Detection Logic

/**
 * Gesture Detector
 * Analyzes hand landmarks to detect specific gestures
 * - Pinch: Thumb and index finger close together
 * - Fist: All fingers curled
 * - Open Hand: All fingers extended
 */

export class GestureDetector {
    constructor(config = {}) {
        this.config = {
            pinchThreshold: 0.05,  // Distance threshold for pinch
            fistThreshold: 0.15,   // Y-distance threshold for fist
            openThreshold: 0.25,   // Y-distance threshold for open hand
            ...config
        };
        
        this.lastGesture = null;
        this.eventTarget = new EventTarget();
    }

    /**
     * Calculate Euclidean distance between two landmarks
     */
    distance(landmark1, landmark2) {
        const dx = landmark1.x - landmark2.x;
        const dy = landmark1.y - landmark2.y;
        const dz = landmark1.z - landmark2.z;
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }

    /**
     * Detect pinch gesture
     * Pinch is detected when thumb tip (4) and index tip (8) are close
     */
    detectPinch(landmarks) {
        const thumbTip = landmarks[4];
        const indexTip = landmarks[8];
        const dist = this.distance(thumbTip, indexTip);
        return dist < this.config.pinchThreshold;
    }

    /**
     * Detect fist gesture
     * Fist is detected when all finger tips are below their MCP joints
     */
    detectFist(landmarks) {
        // Check if finger tips (8, 12, 16, 20) are below MCPs (5, 9, 13, 17)
        const fingers = [
            { tip: 8, mcp: 5 },   // Index
            { tip: 12, mcp: 9 },  // Middle
            { tip: 16, mcp: 13 }, // Ring
            { tip: 20, mcp: 17 }  // Pinky
        ];

        const allCurled = fingers.every(finger => {
            const tip = landmarks[finger.tip];
            const mcp = landmarks[finger.mcp];
            return tip.y > mcp.y - this.config.fistThreshold;
        });

        return allCurled;
    }

    /**
     * Detect open hand gesture
     * Open hand is detected when all finger tips are above their MCP joints
     */
    detectOpenHand(landmarks) {
        // Check if finger tips (8, 12, 16, 20) are above MCPs (5, 9, 13, 17)
        const fingers = [
            { tip: 8, mcp: 5 },   // Index
            { tip: 12, mcp: 9 },  // Middle
            { tip: 16, mcp: 13 }, // Ring
            { tip: 20, mcp: 17 }  // Pinky
        ];

        const allExtended = fingers.every(finger => {
            const tip = landmarks[finger.tip];
            const mcp = landmarks[finger.mcp];
            return tip.y < mcp.y - this.config.openThreshold;
        });

        return allExtended;
    }

    /**
     * Analyze hand landmarks and detect gesture
     * Returns gesture name and confidence
     */
    analyze(landmarks, timestamp = Date.now()) {
        if (!landmarks || landmarks.length < 21) {
            return { gesture: 'none', confidence: 0, timestamp };
        }

        let gesture = 'none';
        let confidence = 0;

        // Check gestures in priority order
        if (this.detectPinch(landmarks)) {
            gesture = 'pinch';
            confidence = 0.9;
        } else if (this.detectFist(landmarks)) {
            gesture = 'fist';
            confidence = 0.85;
        } else if (this.detectOpenHand(landmarks)) {
            gesture = 'open_hand';
            confidence = 0.8;
        }

        // Emit gesture change event
        if (gesture !== this.lastGesture) {
            this.lastGesture = gesture;
            this.eventTarget.dispatchEvent(new CustomEvent('gestureChange', {
                detail: { gesture, confidence, timestamp }
            }));
        }

        return { gesture, confidence, timestamp };
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

// P0_VALIDATOR_ID: GESTURE_DETECTOR_V20
