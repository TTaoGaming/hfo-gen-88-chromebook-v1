// Medallion: Bronze | Mutation: 0% | HIVE: V

import { z } from 'zod';

// CloudEvents 1.0 envelope used for HFO blackboard JSONL lines.
// Includes W3C trace context fields and an append-only chained signature.

export const HfoBlackboardCloudEventSchema = z
    .object({
        // HFO convention
        phase: z.literal('CLOUDEVENT'),

        // CloudEvents 1.0 core
        specversion: z.literal('1.0'),
        id: z.string().min(1),
        source: z.string().min(1),
        type: z.string().min(1),
        time: z.string().min(1),
        datacontenttype: z.string().min(1),
        subject: z.string().min(1).optional(),
        dataschema: z.string().min(1).optional(),

        // Compatibility with existing blackboard purity tools
        timestamp: z.string().min(1),

        // W3C trace context (CloudEvents tracing extension + friendly ids)
        traceparent: z.string().regex(/^00-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$/i),
        tracestate: z.string().optional(),
        trace_id: z.string().regex(/^[0-9a-f]{32}$/i),
        span_id: z.string().regex(/^[0-9a-f]{16}$/i),
        parent_span_id: z.string().regex(/^[0-9a-f]{16}$/i).nullable().optional(),

        // Payload
        data: z.unknown(),

        // Chained signature added on append
        signature: z.string().regex(/^[0-9a-f]{64}$/i).optional(),
    })
    .strict();

export type HfoBlackboardCloudEvent = z.infer<typeof HfoBlackboardCloudEventSchema>;
