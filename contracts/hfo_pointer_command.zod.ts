// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: transport-neutral pointer command stream (W3C-ish).

import { z } from 'zod';

export const PointerEventTypeSchema = z.enum([
  'pointerover',
  'pointerenter',
  'pointerdown',
  'pointermove',
  'pointerup',
  'pointercancel',
  'pointerout',
  'pointerleave',
]);

export const PointerCommandSchema = z.object({
  type: PointerEventTypeSchema,
  pointerId: z.number().int().min(1).default(1),
  isPrimary: z.boolean().default(true),
  pointerType: z.enum(['mouse', 'touch', 'pen']).default('touch'),

  // Viewport-space coordinates.
  clientX: z.number(),
  clientY: z.number(),

  // Button state.
  buttons: z.number().int().min(0).default(0),
  button: z.number().int().default(0),

  pressure: z.number().min(0).max(1).default(0),
  width: z.number().optional(),
  height: z.number().optional(),

  // Optional metadata for tracing.
  handIndex: z.number().int().min(0).optional(),
  reason: z.string().optional(),
});

export type PointerCommand = z.infer<typeof PointerCommandSchema>;
