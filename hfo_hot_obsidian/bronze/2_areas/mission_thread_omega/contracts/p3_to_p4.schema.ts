// Medallion: Bronze | Mutation: 0% | HIVE: I
// Zod 6.0 Contract: P3 (DELIVER) → P4 (DISRUPT)
// Schema for FSM state and gesture data flowing into disruption layer

import { z } from 'zod';

/**
 * FSM State enum from Port 3
 */
export const FSMStateSchema = z.enum([
    'idle',      // No hand detected or no gesture
    'arming',    // Gesture detected but confidence below threshold
    'acquiring', // Gesture locked, building confidence
    'committed'  // High confidence, ready for event dispatch
]);

/**
 * Cursor position schema (normalized 0-1)
 */
export const CursorPositionSchema = z.object({
    x: z.number().min(0).max(1),
    y: z.number().min(0).max(1)
});

/**
 * P3 to P4 contract: Gesture FSM state + target identification
 */
export const P3_TO_P4_SCHEMA = z.object({
    // FSM State
    fsm_state: FSMStateSchema,
    
    // Gesture Recognition
    gesture: z.string(), // e.g., "Closed_Fist", "Open_Palm", "Pointing_Up"
    confidence: z.number().min(0).max(1),
    
    // Cursor Data (from P2)
    cursor_type: z.enum(['raw', 'smooth', 'snappy', 'spring', 'predictive']),
    cursor_position: CursorPositionSchema,
    
    // Target Element (for W3C event injection)
    target_element: z.string().nullable(), // CSS selector or null if none
    target_bounds: z.object({
        x: z.number(),
        y: z.number(),
        width: z.number(),
        height: z.number()
    }).nullable(),
    
    // Metadata
    timestamp: z.number(),
    frame_id: z.number().int().nonnegative()
});

/**
 * Type inference for TypeScript usage
 */
export type P3ToP4Data = z.infer<typeof P3_TO_P4_SCHEMA>;

/**
 * Validation helper
 */
export function validateP3ToP4(data: unknown): P3ToP4Data {
    return P3_TO_P4_SCHEMA.parse(data);
}

/**
 * Safe validation (returns result object instead of throwing)
 */
export function safeValidateP3ToP4(data: unknown) {
    return P3_TO_P4_SCHEMA.safeParse(data);
}
