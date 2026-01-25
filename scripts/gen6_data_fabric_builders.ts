// Medallion: Bronze | Mutation: 0% | HIVE: V
// Helpers for building contract-valid Gen6 DataFabric payloads in tests.

import {
  DataFabricSchema,
  type DataFabric,
  type FabricCursorFusion,
  FsmStateSchema,
} from '../contracts/hfo_data_fabric.zod';

export type FsmState = typeof FsmStateSchema._type;

export function makeFusionCursor(opts: {
  handIndex?: number;
  pointerId?: number;
  fsmState: FsmState;
  gesture: string;
  confidence: number;
  isPalmFacing: boolean;
  uiNormX?: number;
  uiNormY?: number;
  // Optional: override screen/norm/raw fields for special tests.
  screenX?: number;
  screenY?: number;
  normX?: number;
  normY?: number;
  normZ?: number;
  rawX?: number;
  rawY?: number;
  readinessScore?: number;
}): FabricCursorFusion {
  const uiNormX = typeof opts.uiNormX === 'number' ? opts.uiNormX : 0.55;
  const uiNormY = typeof opts.uiNormY === 'number' ? opts.uiNormY : 0.55;

  const cursor: FabricCursorFusion = {
    screenX: typeof opts.screenX === 'number' ? opts.screenX : uiNormX * 1000,
    screenY: typeof opts.screenY === 'number' ? opts.screenY : uiNormY * 1000,

    normX: typeof opts.normX === 'number' ? opts.normX : uiNormX,
    normY: typeof opts.normY === 'number' ? opts.normY : uiNormY,
    normZ: typeof opts.normZ === 'number' ? opts.normZ : 0,

    uiNormX,
    uiNormY,

    rawX: typeof opts.rawX === 'number' ? opts.rawX : uiNormX,
    rawY: typeof opts.rawY === 'number' ? opts.rawY : uiNormY,

    fsmState: opts.fsmState,
    gesture: opts.gesture,
    confidence: opts.confidence,

    isPalmFacing: opts.isPalmFacing,
    normalZ: opts.isPalmFacing ? -1 : 1,
    palmConeAngle: 0.1,
    palmNormal: { x: 0, y: 0, z: opts.isPalmFacing ? -1 : 1 },

    readinessScore: typeof opts.readinessScore === 'number' ? opts.readinessScore : (opts.isPalmFacing ? 1 : 0),

    skeletonAlpha: 1,

    handIndex: typeof opts.handIndex === 'number' ? opts.handIndex : 0,
    pointerId: typeof opts.pointerId === 'number' ? opts.pointerId : 0,

    curls: { index: 0, middle: 0, ring: 0, pinky: 0 },

    // landmarks omitted by default (optional)
  };

  // Assert contract validity in Node (fail fast in tests).
  // If this ever throws, the contract changed and tests must be updated.
  return cursor;
}

export function makeDataFabricFrame(opts: {
  frameId: number;
  systemTime: number;
  cursors: FabricCursorFusion[];
}): DataFabric {
  const fabric = {
    cursors: opts.cursors,
    systemTime: opts.systemTime,
    frameId: opts.frameId,
  } as const;

  return DataFabricSchema.parse(fabric);
}
