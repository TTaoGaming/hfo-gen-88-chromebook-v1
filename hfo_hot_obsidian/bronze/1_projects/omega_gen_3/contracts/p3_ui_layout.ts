// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';

/**
 * P3 DELIVER: UI Layout Contract
 * Enforces the structure of the Golden Layout configuration
 * and UI component registry.
 */

export const UIComponentSchema = z.object({
    id: z.string(),
    type: z.enum(['panel', 'control', 'visualizer']),
    title: z.string(),
    state: z.record(z.any()).optional()
});

export const UILayoutSchema = z.object({
    theme: z.string().default('dark'),
    components: z.array(UIComponentSchema),
    config: z.record(z.any()) // Golden Layout Config Object
});

export type UIComponent = z.infer<typeof UIComponentSchema>;
export type UILayout = z.infer<typeof UILayoutSchema>;
