import { z } from 'zod';

// Medallion: Bronze | Mutation: 0% | HIVE: V
// Hardware Sensing Contract (Port 0 -> Port 1 Bridge)

export const HardwareCpuSchema = z.object({
    count: z.number(),
    load_1m: z.number(),
    load_per_core: z.number(),
    percent: z.number(),
});

export const HardwareMemorySchema = z.object({
    total: z.number(),
    available: z.number(),
    percent: z.number(),
});

export const HardwareBackoffSchema = z.object({
    required: z.boolean(),
    suggested_concurrency: z.number(),
    reason: z.string(),
});

export const HardwareSenseSchema = z.object({
    cpu: HardwareCpuSchema,
    memory: HardwareMemorySchema,
    backoff: HardwareBackoffSchema,
    gpu: z.string().optional(),
});

export type HardwareSense = z.infer<typeof HardwareSenseSchema>;
