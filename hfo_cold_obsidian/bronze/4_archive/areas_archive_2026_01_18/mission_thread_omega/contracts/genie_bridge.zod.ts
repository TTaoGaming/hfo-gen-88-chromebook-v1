// Medallion: Bronze | Mutation: 88% | HIVE: I
// PORT 3: DELIVER | PIANO GENIE BRIDGE CONTRACT (Zod 6.0)

import { z } from "https://cdn.jsdelivr.net/npm/zod@3.22.4/+esm";

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
});

/**
 * GENIE_CURSOR_UPDATE
 * Contract for cross-domain pointer injection between HFO Host and Piano Genie Iframe
 */
export const GenieCursorUpdateSchema = z.object({
    type: z.literal("GENIE_CURSOR_UPDATE"),
    id: z.string().or(z.number()),
    x: z.number().min(0).max(1),
    y: z.number().min(0).max(1),
    active: z.boolean()
});

/**
 * P1 -> P3: Genie Bridge Event
 * Wrapped in CloudEvent envelope for HFO compatibility
 */
export const GenieBridgeEventSchema = CloudEventEnvelopeSchema.extend({
    type: z.literal("hfo.omega.v52.genie_update"),
    data: GenieCursorUpdateSchema
});

export type GenieCursorUpdate = z.infer<typeof GenieCursorUpdateSchema>;
export type GenieBridgeEvent = z.infer<typeof GenieBridgeEventSchema>;

// P5 Forensic Harness Hook
export const validateGenieMessage = (msg: unknown) => {
    return GenieBridgeEventSchema.safeParse(msg);
};
