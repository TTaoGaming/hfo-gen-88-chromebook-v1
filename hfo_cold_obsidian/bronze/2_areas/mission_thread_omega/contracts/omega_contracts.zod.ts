import { z } from 'zod';

// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🛡️ Omega Mission: Zod 6.0 Interlock Contracts

/**
 * CloudEvents 1.0 Envelope (Formalized)
 */
export const CloudEventEnvelopeSchema = z.object({
    id: z.string().uuid().or(z.string()),
    source: z.string(),
    specversion: z.literal('1.0'),
    type: z.string(),
    datacontenttype: z.literal('application/json').optional(),
    dataschema: z.string().url().optional(),
    subject: z.string().optional(),
    time: z.string().datetime().optional(),
    data: z.any(),
    // W3C Trace Context
    traceparent: z.string().optional(),
    tracestate: z.string().optional(),
});

/**
 * P0 -> P1: Cold Sensing Relay
 * Raw landmarks from MediaPipe index tip (Landmark 8)
 */
export const P0SensingSchema = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.p0.sensing'),
    data: z.object({
        timestamp: z.number(),
        source: z.literal('mediapipe-hand-8'),
        coords: z.object({
            x: z.number().min(0).max(1),
            y: z.number().min(0).max(1),
            z: z.number(), // Depth
        }),
        confidence: z.number().min(0).max(1),
        tuning: z.enum(['smooth', 'snappy']).default('smooth'),
    }),
});

/**
 * P1 -> P2: Physics Manifold Input
 * Stabilized and sanitized coordinates for Rapier
 */
export const P1PhysicsInputSchema = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.p1.bridge'),
    data: z.object({
        t: z.number(),
        target: z.object({
            x: z.number(),
            y: z.number(),
        }),
        velocity_hint: z.object({
            vx: z.number().optional(),
            vy: z.number().optional(),
        }),
    }),
});

/**
 * P2 -> P3: Digital Twin State
 * Output from Mass-Spring-Dampener physics
 */
export const P2DigitalTwinSchema = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.p2.shape'),
    data: z.object({
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
    }),
});

/**
 * P3 -> CONSUMER: W3C Pointer Event
 */
export const P3PointerEventSchema = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.p3.deliver'),
    data: z.object({
        type: z.enum(['pointerdown', 'pointermove', 'pointerup', 'pointercancel']),
        clientX: z.number(),
        clientY: z.number(),
        pressure: z.number(),
        pointerId: z.number(),
        timestamp: z.number(),
    }),
});

/**
 * P1 OMEGA: One Euro Filter Tuning
 * Parameters for adaptive denoising (Denaturation)
 */
export const OneEuroFilterSchema = z.object({
    min_cutoff: z.number().describe('Minimum frequency cutoff (Hz)'),
    beta: z.number().describe('Speed coefficient'),
    d_cutoff: z.number().describe('Cutoff for derivative (Hz)'),
});

export const OmegaSettingsSchema = z.object({
    visualizeSkeleton: z.boolean(),
    activePreset: z.enum(['smooth', 'snappy']),
    filterParams: OneEuroFilterSchema,
});
