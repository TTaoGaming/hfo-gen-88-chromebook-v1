// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';

/**
 * P0 SENSE: Raw MediaPipe Landmark Data
 */
export const LandmarkSchema = z.object({
    x: z.number(),
    y: z.number(),
    z: z.number(),
    visibility: z.number().optional(),
});

export const MediaPipeHandSchema = z.array(LandmarkSchema); // 21 landmarks

export const P0SenseSchema = z.object({
    landmarks: z.array(MediaPipeHandSchema),
    worldLandmarks: z.array(MediaPipeHandSchema).optional(),
    gestures: z.array(z.array(z.object({
        categoryName: z.string(),
        score: z.number(),
    }))).optional(),
});

/**
 * P1 FUSE: Bridge Data (Coordinates mapped to Physics Manifold)
 */
export const PhysicsTargetSchema = z.object({
    x: z.number(), // Normalized 0-1
    y: z.number(), // Normalized 0-1
    velocity: z.object({
        x: z.number(),
        y: z.number(),
    }).optional(),
    pressure: z.number().default(0),
    isDown: z.boolean(),
});

export const P1FuseSchema = z.object({
    hands: z.array(PhysicsTargetSchema),
    timestamp: z.number(),
    systemState: z.enum(['IDLE', 'ACTIVE', 'ERROR']),
});

export type P0Sense = z.infer<typeof P0SenseSchema>;
export type P1Fuse = z.infer<typeof P1FuseSchema>;
