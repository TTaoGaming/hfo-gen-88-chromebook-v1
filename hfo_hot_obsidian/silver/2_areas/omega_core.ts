// Medallion: Silver | Mutation: 0% | HIVE: E
// Thread: Omega | Generation: 1

import { z } from 'zod';

// --- PORT 1: CONTRACT DEFINITIONS ---
export const P1_HandLandmarksContract = z.object({
    id: z.number().default(0),
    landmarks: z.array(z.object({
        x: z.number(),
        y: z.number(),
        z: z.number()
    })).length(21),
    worldLandmarks: z.array(z.any()).optional(),
    handedness: z.string().default('Right')
});

export const P1_PhysicsInputContract = z.object({
    x: z.number(),
    y: z.number(),
    velocity: z.object({ x: z.number(), y: z.number() }).optional(),
    intent: z.enum(['IDLE', 'POINTER_READY', 'POINTER_COMMIT']).default('IDLE')
});

// --- PORT 0: SENSE (Mockable Sensing) ---
export const P0_SENSE = {
    read() {
        return {
            id: 0,
            landmarks: Array(21).fill({ x: 0.5, y: 0.5, z: 0 }),
            handedness: 'Right'
        };
    }
};

// --- PORT 1: FUSE (Boundary / Contract Enforcement) ---
export const P1_FUSE = {
    validateAndFuse(rawSensingData: any, config: { width: number, height: number }) {
        try {
            const validatedHand = P1_HandLandmarksContract.parse(rawSensingData);
            const indexTip = validatedHand.landmarks[8];
            return P1_PhysicsInputContract.parse({
                x: indexTip.x * config.width,
                y: indexTip.y * config.height,
                intent: 'POINTER_READY'
            });
        } catch (err) {
            return null;
        }
    }
};

// --- PORT 2: SHAPE (Logic only for testing) ---
// We keep the physics logic but decouple from Matter.js for raw mutation testing if needed
// Or we can import matter-js if it's available.
export const P2_SHAPE = {
    calculateForce(cursorPos: { x: number, y: number }, targetPos: { x: number, y: number }) {
        return {
            x: (targetPos.x - cursorPos.x) * 0.005,
            y: (targetPos.y - cursorPos.y) * 0.005
        };
    }
};
