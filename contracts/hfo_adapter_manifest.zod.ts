// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: polymorphic adapter manifest.

import { z } from 'zod';

export const TargetPolicySchema = z.enum(['ACTIVE_APP_ONLY', 'ACTIVE_APP_OR_FALLBACK', 'GLOBAL']);

export const AdapterCapabilitySchema = z.enum([
  'pointer:w3c',
  'nematocyst:keyboard',
  'nematocyst:wheel',
  'intent:tool',
]);

export const AdapterManifestSchema = z.object({
  adapterId: z.string().min(1),
  title: z.string().min(1),

  // Where/how the adapter is mounted.
  kind: z.enum(['iframe', 'overlay', 'dom']).default('iframe'),
  entrypoint: z.string().optional(),

  // Routing and safety.
  targetPolicy: TargetPolicySchema.default('ACTIVE_APP_ONLY'),

  // What the adapter can accept/emit.
  capabilities: z.array(AdapterCapabilitySchema).default([]),

  // Optional: instruct P3 adapter selection when pointer is in play.
  pointerAdapter: z.enum(['standard', 'excalidraw']).optional(),
}).passthrough();

export type AdapterManifest = z.infer<typeof AdapterManifestSchema>;
