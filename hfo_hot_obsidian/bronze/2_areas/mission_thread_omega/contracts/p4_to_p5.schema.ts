// Medallion: Bronze | Mutation: 0% | HIVE: I
// Zod 6.0 Contract: P4 (DISRUPT) → P5 (DEFEND)
// Schema for disruption telemetry and integrity validation

import { z } from 'zod';

/**
 * Pointer lock status enum
 */
export const PointerLockStatusSchema = z.enum([
    'locked',   // Hardware cursor successfully locked
    'unlocked', // No lock active
    'failed'    // Lock attempt failed
]);

/**
 * Suppression module status
 */
export const SuppressionStatusSchema = z.object({
    is_active: z.boolean(),
    native_events_blocked: z.number().int().nonnegative(),
    whitelisted_elements_count: z.number().int().nonnegative()
});

/**
 * Jitter dampener status
 */
export const JitterDampenerStatusSchema = z.object({
    deadzone_px: z.number().positive(),
    max_update_rate_hz: z.number().positive(),
    corrections_applied: z.number().int().nonnegative(),
    updates_blocked: z.number().int().nonnegative(),
    dampening_rate: z.string() // Formatted percentage
});

/**
 * Hardware locker status
 */
export const HardwareLockerStatusSchema = z.object({
    is_locked: z.boolean(),
    lock_target: z.string().nullable(),
    lock_attempts: z.number().int().nonnegative(),
    pointer_lock_element: z.string().nullable()
});

/**
 * Native rejector status
 */
export const NativeRejectorStatusSchema = z.object({
    is_active: z.boolean(),
    rejection_count: z.number().int().nonnegative(),
    rejection_rate_per_sec: z.string() // Formatted rate
});

/**
 * P4 to P5 contract: Disruption telemetry
 */
export const P4_TO_P5_SCHEMA = z.object({
    // Overall Port 4 Status
    port_status: z.enum(['online', 'degraded', 'offline']),
    
    // Module Telemetry
    suppressor: SuppressionStatusSchema,
    dampener: JitterDampenerStatusSchema,
    locker: HardwareLockerStatusSchema,
    rejector: NativeRejectorStatusSchema,
    
    // Aggregated Metrics
    total_disruptions: z.number().int().nonnegative(),
    disruption_effectiveness: z.number().min(0).max(1), // 0-1 ratio
    
    // Virtual Cursor Dominance
    virtual_cursor_active: z.boolean(),
    native_cursor_suppressed: z.boolean(),
    
    // Architectural Violations (SCREAM Protocol)
    violations_detected: z.number().int().nonnegative(),
    last_violation_reason: z.string().nullable(),
    
    // Metadata
    timestamp: z.number(),
    medallion: z.enum(['bronze', 'silver', 'gold'])
});

/**
 * Type inference for TypeScript usage
 */
export type P4ToP5Data = z.infer<typeof P4_TO_P5_SCHEMA>;

/**
 * Validation helper
 */
export function validateP4ToP5(data: unknown): P4ToP5Data {
    return P4_TO_P5_SCHEMA.parse(data);
}

/**
 * Safe validation (returns result object instead of throwing)
 */
export function safeValidateP4ToP5(data: unknown) {
    return P4_TO_P5_SCHEMA.safeParse(data);
}

/**
 * Integrity check: Validates that Port 4 is operating correctly
 */
export function checkP4Integrity(data: P4ToP5Data): { valid: boolean; issues: string[] } {
    const issues: string[] = [];

    // Check if suppressor is active when it should be
    if (data.virtual_cursor_active && !data.suppressor.is_active) {
        issues.push('Suppressor should be active when virtual cursor is active');
    }

    // Check if hardware lock is acquired when needed
    if (data.virtual_cursor_active && !data.locker.is_locked) {
        issues.push('Hardware lock should be acquired when virtual cursor is active');
    }

    // Check if native cursor is properly suppressed
    if (data.virtual_cursor_active && !data.native_cursor_suppressed) {
        issues.push('Native cursor should be suppressed when virtual cursor is active');
    }

    // Check disruption effectiveness
    if (data.disruption_effectiveness < 0.8) {
        issues.push(`Disruption effectiveness too low: ${data.disruption_effectiveness}`);
    }

    // Check for excessive violations
    if (data.violations_detected > 10) {
        issues.push(`Excessive violations detected: ${data.violations_detected}`);
    }

    return {
        valid: issues.length === 0,
        issues
    };
}
