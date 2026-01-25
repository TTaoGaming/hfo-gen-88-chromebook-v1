// Medallion: Bronze | Mutation: 0% | HIVE: V
// Helper utilities for Gen6 v23 RED specs (automation + consistency).

import type { Page } from '@playwright/test';
import { safeEvaluate } from './omega_gen6_test_guards';
import { makeDataFabricFrame, makeFusionCursor } from './gen6_data_fabric_builders';

export type V23Frame = {
  now: number;
  dt: number;
  fsmState: 'IDLE' | 'READY' | 'COMMIT' | 'COAST';
  gesture: string;
  confidence: number;
  isPalmFacing: boolean;
  uiNormX?: number;
  uiNormY?: number;
};

export type V23Step = { now: number; dt: number; dataFabric: any };

export type ObjPath = Array<string | number>;

function getByPath(root: any, path: ObjPath): any {
  let cur = root;
  for (const key of path) {
    if (cur === null || cur === undefined) return null;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
    cur = (cur as any)[key as any];
  }
  return cur ?? null;
}

export function withFlags(url: string, flags: Record<string, string | number | boolean | null | undefined>): string {
  const out = new URL(url);
  for (const [key, value] of Object.entries(flags)) {
    if (value === null || value === undefined) continue;
    out.searchParams.set(key, String(value));
  }
  return out.toString();
}

export function buildStepsFromFrames(frames: V23Frame[], opts?: { handIndex?: number; pointerId?: number }): V23Step[] {
  const handIndex = Number(opts?.handIndex ?? 0);
  const pointerId = Number(opts?.pointerId ?? 0);

  return frames.map((f, i) => {
    const cursor = makeFusionCursor({
      handIndex,
      pointerId,
      fsmState: f.fsmState,
      gesture: f.gesture,
      confidence: Number(f.confidence),
      isPalmFacing: !!f.isPalmFacing,
      uiNormX: typeof f.uiNormX === 'number' ? f.uiNormX : 0.55,
      uiNormY: typeof f.uiNormY === 'number' ? f.uiNormY : 0.55,
      readinessScore: f.fsmState === 'READY' ? 1 : 0,
    });

    const dataFabric = makeDataFabricFrame({
      frameId: i + 1,
      systemTime: Number(f.now),
      cursors: [cursor],
    });

    return { now: Number(f.now), dt: Number(f.dt), dataFabric };
  });
}

export async function tickThreadCapture<TSnap>(
  page: Page,
  payload: {
    threadName: string;
    steps: V23Step[];
    capturePorts?: string[];
    snapPaths: ObjPath[];
  },
): Promise<{ hasThread: boolean; snap: TSnap; captured: Array<{ port: string; type: string; payload: any }> }> {
  return safeEvaluate(
    page,
    (arg: {
      threadName: string;
      steps: Array<{ now: number; dt: number; dataFabric: any }>;
      capturePorts?: string[];
      snapPaths: Array<Array<string | number>>;
    }) => {
      const w = window as any;

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const want = Array.isArray(arg.capturePorts) ? new Set(arg.capturePorts) : null;
      const unsub = w.hfoPortsEffects?.subscribe?.((entry: any) => {
        if (!entry?.port) return;
        if (want && !want.has(entry.port)) return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      });

      const thread = w[arg.threadName];
      const hasThread = !!thread?.tick;

      for (const s of arg.steps) {
        try {
          thread?.tick?.({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric });
        } catch {
          // ignore (RED-first)
        }
      }

      try { unsub?.(); } catch { /* ignore */ }

      const getByPathLocal = (root: any, path: Array<string | number>) => {
        let cur = root;
        for (const key of path) {
          if (cur === null || cur === undefined) return null;
          cur = cur[key as any];
        }
        return cur ?? null;
      };

      let snap: any = null;
      for (const p of (arg.snapPaths || [])) {
        snap = getByPathLocal(w, p);
        if (snap !== null && snap !== undefined) break;
      }
      return { hasThread, snap, captured };
    },
    {
      threadName: String(payload.threadName),
      steps: payload.steps,
      capturePorts: payload.capturePorts,
      snapPaths: payload.snapPaths,
    },
  );
}
