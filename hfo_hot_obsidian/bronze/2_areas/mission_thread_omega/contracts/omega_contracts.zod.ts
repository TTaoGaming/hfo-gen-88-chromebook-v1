import { z } from 'zod';

// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🛡️ Omega Mission: Zod 6.0 Interlock Contracts

/**
 * P0 -> P1: Cold Sensing Relay
 * Raw landmarks from MediaPipe index tip (Landmark 8)
 */
export const P0SensingSchema = z.object({
  timestamp: z.number(),
  source: z.literal('mediapipe-hand-8'),
  coords: z.object({
    x: z.number().min(0).max(1),
    y: z.number().min(0).max(1),
    z: z.number(), // Depth
  }),
  confidence: z.number().min(0).max(1),
  tuning: z.enum(['smooth', 'snappy']).default('smooth'), // Preset selection
});

/**
 * P1 -> P2: Physics Manifold Input
 * Stabilized and sanitized coordinates for Rapier
 */
export const P1PhysicsInputSchema = z.object({
  t: z.number(),
  target: z.object({
    x: z.number(),
    y: z.number(),
  }),
  velocity_hint: z.object({
    vx: z.number().optional(),
    vy: z.number().optional(),
  }),
});

/**
 * P2 -> P3: Digital Twin State
 * Output from Mass-Spring-Dampener physics
 */
export const P2DigitalTwinSchema = z.object({
  t: z.number(),
  position: z.object({
    x: z.number(),
    y: z.number(),
  }),
  velocity: z.object({
    vx: z.number(),
    vy: z.number(),
  }),
  is_stable: z.boolean(),
});

/**
 * P3 -> CONSUMER: W3C Pointer Event
 */
export const P3PointerEventSchema = z.object({
  type: z.enum(['pointerdown', 'pointermove', 'pointerup', 'pointercancel']),
  clientX: z.number(),
  clientY: z.number(),
  pressure: z.number(),
  pointerId: z.number(),
  timestamp: z.number(),
});
