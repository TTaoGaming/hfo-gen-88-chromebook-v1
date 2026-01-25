// Medallion: Bronze | Mutation: 0% | HIVE: V
import { z } from 'zod';

export const TripwireDirectionSchema = z.enum(['down', 'up']);
export const TripwireSensorPhaseSchema = z.enum(['begin', 'end']);

const Vec2Schema = z.object({ x: z.number(), y: z.number() });

export const TripwirePlanckSensorSchema = z
  .object({
    engine: z.literal('planck'),
    phase: TripwireSensorPhaseSchema,
    cursor: z.object({
      role: z.literal('cursor'),
      bodyId: z.string().min(1),
      fixtureId: z.string().min(1),
    }),
    band: z.object({
      role: z.literal('tripwire_band'),
      bodyId: z.string().min(1),
      fixtureId: z.string().min(1),
      bandKey: z.string().min(1),
    }),
    manifold: z
      .object({
        normal: Vec2Schema.optional(),
        points: z.array(Vec2Schema).optional(),
      })
      .optional(),
  })
  .strict();

// v15 target: richer, Planck-contact driven tripwire event.
export const TripwireCrossV15Schema = z
  .object({
    ts: z.string().min(1),
    now: z.number(),
    dt: z.number(),
    seq: z.string().nullable().optional(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.string(),
    readiness: z.number(),
    uiNormX: z.number(),
    uiNormY: z.number(),
    direction: TripwireDirectionSchema,
    vxUiNormPerS: z.number().optional(),
    vyUiNormPerS: z.number().optional(),
    speedUiNormPerS: z.number(),
    traceId: z.string().optional(),
    targetId: z.string().optional(),
    sensor: TripwirePlanckSensorSchema,
  })
  .strict();

// v17 lookahead: analytic TTC prediction (COMMIT-gated) for pre-arming downstream effects.
export const TripwireLookaheadV1Schema = z
  .object({
    ts: z.string().min(1),
    now: z.number(),
    dt: z.number(),
    seq: z.string().nullable().optional(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.string(),
    readiness: z.number(),
    uiNormX: z.number(),
    uiNormY: z.number(),
    direction: TripwireDirectionSchema,
    vxUiNormPerS: z.number().optional(),
    vyUiNormPerS: z.number().optional(),
    speedUiNormPerS: z.number(),
    bandY: z.number(),
    ttcMs: z.number(),
    lookaheadWindowMs: z.number(),
    traceId: z.string().optional(),
    targetId: z.string().optional(),
  })
  .strict();

export const P3TripwireInjectV1Schema = z
  .object({
    // Optional: allow timing assertions in deterministic replay tests.
    ts: z.string().min(1).optional(),
    now: z.number().optional(),
    adapterId: z.literal('dino-v1'),
    ok: z.boolean(),
    direction: TripwireDirectionSchema,
    payload: z
      .object({
        kind: z.literal('keyboard'),
        action: z.literal('keypress'),
        key: z.literal(' '),
        code: z.literal('Space'),
      })
      .strict(),
    reason: z.string().min(1),
  })
  .strict();

export const P3KeyboardActionV2Schema = z.enum(['keypress', 'keydown', 'keyup']);

export const P3TripwireInjectV2Schema = z
  .object({
    // Optional: allow timing assertions in deterministic replay tests.
    ts: z.string().min(1).optional(),
    now: z.number().optional(),
    adapterId: z.literal('dino-v1'),
    ok: z.boolean(),
    sensorId: z.string().min(1),
    direction: TripwireDirectionSchema,
    payload: z
      .object({
        kind: z.literal('keyboard'),
        action: P3KeyboardActionV2Schema,
        key: z.literal(' '),
        code: z.literal('Space'),
      })
      .strict(),
    reason: z.string().min(1),
  })
  .strict();

// --- GEN6 v21: Knuckle Tripwire (distance-based; uiNorm units) ---
// Purpose: validate the P2 knuckle tripwire_cross payload and keep velocity metadata ready for future use.
const Vec3Schema = z.object({ x: z.number(), y: z.number(), z: z.number().optional() });

export const KnuckleTripwireDistanceV21Schema = z
  .object({
    featureDistanceUiNorm: z.number(),
    rawDistanceUiNorm: z.number(),
    orientedDistanceUiNorm: z.number(),
    rawDistanceVelUiNormPerS: z.number().optional(),
    orientedDistanceVelUiNormPerS: z.number().optional(),
    featureDistanceVelUiNormPerS: z.number().optional(),
    barLenUiNorm: z.number().positive(),
    onDistanceUiNorm: z.number(),
    offDistanceUiNorm: z.number(),
  })
  .strict();

export const KnuckleTripwireCrossV21Schema = z
  .object({
    ts: z.string().min(1),
    sensorId: z.literal('knuckle'),
    now: z.number(),
    dt: z.number(),
    seq: z.number(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.string(),
    readiness: z.number(),
    uiNormX: z.number(),
    uiNormY: z.number(),
    direction: TripwireDirectionSchema,
    vxUiNormPerS: z.number(),
    vyUiNormPerS: z.number(),
    speedUiNormPerS: z.number(),
    traceId: z.string().optional(),
    targetId: z.string().optional(),
    sensor: z
      .object({
        engine: z.literal('knuckle'),
        phase: TripwireSensorPhaseSchema,
        bar: z.object({ a: Vec3Schema, b: Vec3Schema }).strict(),
        tip: Vec3Schema,
        distance: KnuckleTripwireDistanceV21Schema,
        feature: z.number(),
        rawFeature: z.number(),
      })
      .strict(),
  })
  .strict();

// --- GEN6 v22: TripPlane Lookahead (predictive; COMMIT-gated) ---
// Purpose: support snappy proprioception-first UX by compensating camera/Mediapipe latency.
// This is contract-first: v22 implementation should emit `p2:tripplane_lookahead` before a crossing.
export const TripplaneLookaheadV22Schema = z
  .object({
    ts: z.string().min(1),
    sensorId: z.literal('knuckle'),
    now: z.number(),
    dt: z.number(),
    seq: z.number(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.literal('COMMIT'),
    readiness: z.number(),
    uiNormX: z.number(),
    uiNormY: z.number(),
    // Predictive terms
    ttcMs: z.number().nonnegative(),
    lookaheadWindowMs: z.number().positive(),
    // Distance state at prediction time
    orientedDistanceUiNorm: z.number(),
    orientedDistanceVelUiNormPerS: z.number(),
    enterDistanceUiNorm: z.number(),
    exitDistanceUiNorm: z.number(),
    // Optional: endpoint extension / band params for easier triggering
    // NOTE: prefer per-end extensions for sword-like asymmetric tools.
    barExtensionUiNorm: z.number().optional(),
    barExtensionUiNormA: z.number().optional(),
    barExtensionUiNormB: z.number().optional(),
    bandThicknessUiNorm: z.number().optional(),
    traceId: z.string().optional(),
    targetId: z.string().optional(),
  })
  .strict();

// --- GEN6 v23: Commit Variants + Sword Meter (contract-first; RED→GREEN gate) ---
// Purpose:
// - Commit variants are an orthogonal layer atop base FSM (IDLE/READY/COMMIT/COAST).
// - Sword meter is a sticky leaky-bucket lock/unlock controlled by READY+Thumb_Up/Thumb_Down.

export const CommitVariantV23Schema = z.enum([
  'NONE',
  'COMMIT_POINTER_UP',
  'COMMIT_THUMBS_UP',
  'COMMIT_THUMBS_DOWN',
]);

// Canonical by-hand map used by spec/tests.
// Spec example uses keys like "hand0"; we also accept Left/Right for ergonomic UI layers.
export const CommitVariantByHandV23Schema = z.union([
  z.record(CommitVariantV23Schema),
  z
    .object({
      Left: CommitVariantV23Schema.optional(),
      Right: CommitVariantV23Schema.optional(),
    })
    .strict(),
]);

export const P2CommitVariantEventV23Schema = z
  .object({
    ts: z.string().min(1),
    now: z.number(),
    dt: z.number(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.string(),
    commitVariant: CommitVariantV23Schema,
    sourceCategory: z.string().min(1),
    confidence: z.number().min(0).max(1),
  })
  .strict();

export const SwordLockedByV23Schema = z
  .object({
    handIndex: z.number(),
    pointerId: z.number(),
  })
  .strict();

export const SwordMeterSnapshotV23Schema = z
  .object({
    // High-level (flattened) state for the active hand or aggregate.
    active: z.boolean(),
    locked: z.boolean(),
    meter01: z.number().finite(),

    // Required by v23 spec (for debugging + deterministic state transitions).
    lockedBy: SwordLockedByV23Schema,
    lastCommitVariant: CommitVariantV23Schema,

    // Visual posture knobs (optional until implementation lands).
    extensionFracA: z.number().optional(),
    extensionFracB: z.number().optional(),

    // Optional per-hand detail (future-proofing; still contractable).
    hands: z
      .object({
        Left: z
          .object({
            active: z.boolean(),
            locked: z.boolean(),
            meter01: z.number().finite(),
          })
          .strict()
          .optional(),
        Right: z
          .object({
            active: z.boolean(),
            locked: z.boolean(),
            meter01: z.number().finite(),
          })
          .strict()
          .optional(),
      })
      .strict()
      .optional(),
  })
  .strict();

export const P2SwordMeterEventV23Schema = z
  .object({
    ts: z.string().min(1),
    now: z.number(),
    dt: z.number(),
    handIndex: z.number(),
    pointerId: z.number(),
    fsmState: z.string(),
    active: z.boolean(),
    locked: z.boolean(),
    meter01: z.number().finite(),
    lockedBy: SwordLockedByV23Schema.optional(),
    lastCommitVariant: CommitVariantV23Schema.optional(),
    reason: z.string().min(1).optional(),
  })
  .strict();
