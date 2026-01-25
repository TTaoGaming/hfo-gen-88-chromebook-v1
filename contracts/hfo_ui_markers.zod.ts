// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: inspectable UI debug markers for deterministic BDD/visual tests.

import { z } from 'zod';

const FiniteNumber = z.number().finite();

export const UiPointSchema = z
  .object({
    x: FiniteNumber,
    y: FiniteNumber,
  })
  .strict();

// v23 Touch2D sword debug registry marker.
export const SwordTouch2dMarkerV23Schema = z
  .object({
    active: z.boolean(),
    locked: z.boolean(),

    endpointPinkyUiNorm: UiPointSchema,
    endpointIndexUiNorm: UiPointSchema,

    // Implementation convenience endpoints (A/B along bar axis).
    endpointAUiNorm: UiPointSchema,
    endpointBUiNorm: UiPointSchema,

    // Axis direction in UI normalized space (unit-ish; normalization tolerance is runtime).
    axisUiNorm: UiPointSchema,

    thicknessUiNorm: FiniteNumber,

    // Optional: expose base endpoints to allow deterministic extension measurement.
    baseEndpointAUiNorm: UiPointSchema.optional(),
    baseEndpointBUiNorm: UiPointSchema.optional(),
  })
  .strict();

// v23 Babylon marker: keep minimal; meshName is sufficient for deterministic presence checks.
export const SwordBabylonMarkerV23Schema = z
  .object({
    active: z.boolean(),
    locked: z.boolean(),
    meshName: z.string().min(1).optional(),
  })
  .strict();

export type UiPoint = z.infer<typeof UiPointSchema>;
export type SwordTouch2dMarkerV23 = z.infer<typeof SwordTouch2dMarkerV23Schema>;
export type SwordBabylonMarkerV23 = z.infer<typeof SwordBabylonMarkerV23Schema>;
