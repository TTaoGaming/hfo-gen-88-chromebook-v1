// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import * as fs from 'node:fs/promises';

const GEN6_URL =
  process.env.HFO_GEN6_URL ||
  process.env.HFO_GEN6_V9_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v10.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&flag-p3-dino-ready-edge=true&mode=dev';

const GOLDEN_MANIFEST_URL =
  process.env.HFO_GEN6_V9_REPLAY_MANIFEST_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/fixtures/replay/gen6_v9_dino_readiness_golden.json';

const STRICT_DIAG = String(process.env.HFO_DIAG_STRICT || '').toLowerCase() === 'true';
const FAIL_CLOSED = String(process.env.HFO_DIAG_FAIL_CLOSED || 'true').toLowerCase() === 'true';
const STRESS_REPEATS = Math.max(1, Number(process.env.HFO_DIAG_REPEATS || '20'));

async function installReplayPipelineDiag(hfoPage: any) {
  await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag = anyWindow.__hfoDiag || {};

    anyWindow.__hfoDiag.recognizeCalls = anyWindow.__hfoDiag.recognizeCalls || 0;
    anyWindow.__hfoDiag.fuseCalls = anyWindow.__hfoDiag.fuseCalls || 0;
    anyWindow.__hfoDiag.lastFuseCursorCount = anyWindow.__hfoDiag.lastFuseCursorCount ?? null;
    anyWindow.__hfoDiag.mockResultsAssignments = anyWindow.__hfoDiag.mockResultsAssignments || 0;
    anyWindow.__hfoDiag.lastMockResultsMeta = anyWindow.__hfoDiag.lastMockResultsMeta ?? null;
    anyWindow.__hfoDiag.mockPlayerCalls = anyWindow.__hfoDiag.mockPlayerCalls || 0;
    anyWindow.__hfoDiag.p1FsmEdgeEvents = anyWindow.__hfoDiag.p1FsmEdgeEvents || 0;

    // Wrap recognizeForVideo (if available).
    try {
      if (!anyWindow.__hfoDiag.recognizeWrapped) {
        const rec = anyWindow.systemState?.p0?.recognizer;
        if (rec && typeof rec.recognizeForVideo === 'function') {
          const orig = rec.recognizeForVideo.bind(rec);
          rec.recognizeForVideo = (...args: any[]) => {
            anyWindow.__hfoDiag.recognizeCalls = (anyWindow.__hfoDiag.recognizeCalls || 0) + 1;
            return orig(...args);
          };
          anyWindow.__hfoDiag.recognizeWrapped = true;
        }
      }
    } catch {
      // ignore
    }

    // Wrap P1Bridger.fuse to observe whether we're producing cursors.
    try {
      const bridger = (anyWindow as any).P1Bridger;
      if (bridger && typeof bridger.fuse === 'function' && !anyWindow.__hfoDiag.fuseWrapped) {
        const fuseOrig = bridger.fuse.bind(bridger);
        bridger.fuse = (...args: any[]) => {
          const cursors = fuseOrig(...args);
          anyWindow.__hfoDiag.fuseCalls = (anyWindow.__hfoDiag.fuseCalls || 0) + 1;
          anyWindow.__hfoDiag.lastFuseCursorCount = Array.isArray(cursors) ? cursors.length : null;
          return cursors;
        };
        anyWindow.__hfoDiag.fuseWrapped = true;
      }
    } catch {
      // ignore
    }

    // Intercept assignments to window.hfoMockResults so we can see if replay is actually setting it.
    try {
      if (!anyWindow.__hfoDiag.mockResultsWrapped) {
        let internalValue = anyWindow.hfoMockResults;
        Object.defineProperty(anyWindow, 'hfoMockResults', {
          configurable: true,
          enumerable: true,
          get() {
            return internalValue;
          },
          set(v) {
            internalValue = v;
            if (v) {
              anyWindow.__hfoDiag.mockResultsAssignments = (anyWindow.__hfoDiag.mockResultsAssignments || 0) + 1;
              anyWindow.__hfoDiag.lastMockResultsMeta = {
                hasReplayHands: Array.isArray(v.__hfoReplayHands),
                replayHandsLen: Array.isArray(v.__hfoReplayHands) ? v.__hfoReplayHands.length : null,
                landmarksLen: Array.isArray(v.landmarks) ? v.landmarks.length : null,
                gesturesLen: Array.isArray(v.gestures) ? v.gestures.length : null,
              };
            }
          },
        });
        anyWindow.__hfoDiag.mockResultsWrapped = true;
      }
    } catch {
      // ignore
    }

    // If a mock player exists, count its nextResults calls (higher priority than hfoMockResults in predictLoop).
    try {
      const mp = anyWindow.hfoMockPlayer;
      if (mp && typeof mp.nextResults === 'function' && !anyWindow.__hfoDiag.mockPlayerWrapped) {
        const nextOrig = mp.nextResults.bind(mp);
        mp.nextResults = (...args: any[]) => {
          anyWindow.__hfoDiag.mockPlayerCalls = (anyWindow.__hfoDiag.mockPlayerCalls || 0) + 1;
          return nextOrig(...args);
        };
        anyWindow.__hfoDiag.mockPlayerWrapped = true;
      }
    } catch {
      // ignore
    }

    // Subscribe to port effects to count p1 fsm_edge independently of rep.counts.
    try {
      if (!anyWindow.__hfoDiag.effectsSubscribed && typeof anyWindow.hfoPortsEffects?.subscribe === 'function') {
        anyWindow.hfoPortsEffects.subscribe((e: any) => {
          try {
            anyWindow.__hfoDiag.portEffects = anyWindow.__hfoDiag.portEffects || [];
            anyWindow.__hfoDiag.portEffects.push({ ts: Date.now(), e });
            if (anyWindow.__hfoDiag.portEffects.length > 200) {
              anyWindow.__hfoDiag.portEffects.splice(0, anyWindow.__hfoDiag.portEffects.length - 200);
            }
          } catch {
            // ignore
          }
          if (e?.port === 'p1' && e?.type === 'fsm_edge') {
            anyWindow.__hfoDiag.p1FsmEdgeEvents = (anyWindow.__hfoDiag.p1FsmEdgeEvents || 0) + 1;
          }
        });
        anyWindow.__hfoDiag.effectsSubscribed = true;
      }
    } catch {
      // ignore
    }
  });
}

async function writeFirstFailureBundle(testInfo: any, bundle: any) {
  const body = JSON.stringify(bundle, null, 2);
  await testInfo.attach('first_failure_bundle.json', {
    body: Buffer.from(body, 'utf-8'),
    contentType: 'application/json',
  });
  await fs.writeFile(testInfo.outputPath('first_failure_bundle.json'), body, 'utf-8');
}

test.beforeEach(async ({ hfoPage }) => {
  await hfoPage.addInitScript(() => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag = anyWindow.__hfoDiag || { acks: [], messages: [] };
    anyWindow.__hfoDiag.portEffects = [];

    const pushRing = (arr: any[], v: any, maxLen: number) => {
      try {
        arr.push(v);
        if (arr.length > maxLen) arr.splice(0, arr.length - maxLen);
      } catch {
        // ignore
      }
    };

    window.addEventListener('message', (event) => {
      try {
        const data = (event as any)?.data;
        if (!data || typeof data !== 'object') return;

        pushRing(anyWindow.__hfoDiag.messages, {
          ts: Date.now(),
          origin: (event as any)?.origin || null,
          type: data.type || null,
          payload: data.payload ?? null,
        }, 200);

        if (data.type === 'hfo:nematocyst:ack') {
          pushRing(anyWindow.__hfoDiag.acks, { ts: Date.now(), origin: (event as any)?.origin || null, payload: data.payload ?? null }, 200);
        }
      } catch {
        // ignore
      }
    });
  });
});

test('Gen6 v9 diag: wrapper emits hfo:nematocyst:ack (direct postMessage)', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_URL);
  await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

  // Wait for wrapper document to be ready (inner runner may still be loading).
  await hfoPage.waitForFunction(() => {
    const iframe = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
    if (!iframe) return false;
    try {
      return iframe.contentDocument?.readyState === 'complete';
    } catch {
      return false;
    }
  }, null, { timeout: 20_000 });

  await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag.acks = [];

    const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
    const cw = wrapper?.contentWindow;
    if (!cw) throw new Error('Missing dino wrapper contentWindow');

    cw.postMessage(
      {
        type: 'hfo:nematocyst',
        payload: { kind: 'keyboard', action: 'keypress', key: ' ', code: 'Space' },
      },
      window.location.origin,
    );
  });

  await hfoPage.waitForFunction(() => {
    const anyWindow = window as any;
    return (anyWindow.__hfoDiag?.acks?.length || 0) > 0;
  }, null, { timeout: 10_000 });

  // Retry briefly until we observe an ok:true ack. If this never happens, that's strong evidence
  // of an inner-iframe readiness/focus race or of the wrong target receiving the message.
  const ok = await hfoPage.evaluate(async () => {
    const anyWindow = window as any;
    const wrapper = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
    const cw = wrapper?.contentWindow;
    if (!cw) throw new Error('Missing dino wrapper contentWindow');

    const send = () => {
      cw.postMessage(
        {
          type: 'hfo:nematocyst',
          payload: { kind: 'keyboard', action: 'keypress', key: ' ', code: 'Space' },
        },
        window.location.origin,
      );
    };

    const hasOkAck = () => (anyWindow.__hfoDiag.acks || []).some((a: any) => a?.payload?.ok);

    if (hasOkAck()) return true;

    const deadline = Date.now() + 5_000;
    while (Date.now() < deadline) {
      send();
      await new Promise((r) => setTimeout(r, 200));
      if (hasOkAck()) return true;
    }
    return false;
  });

  const acks = await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    return anyWindow.__hfoDiag.acks || [];
  });

  expect(acks.length, 'Expected at least one hfo:nematocyst:ack').toBeGreaterThan(0);
  expect(ok, `Expected an ok:true ack within retry window; got: ${JSON.stringify(acks.slice(-5))}`).toBe(true);
});

test('Gen6 v9 diag: dino iframe multiplicity + active reference snapshot', async ({ hfoPage }, testInfo) => {
  await hfoPage.goto(GEN6_URL);
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });

  const diag = await hfoPage.evaluate(() => {
    const iframes = Array.from(document.querySelectorAll('#dino-wrapper-iframe')) as HTMLIFrameElement[];
    const describeEl = (el: HTMLElement | null) => {
      if (!el) return null;
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return {
        id: el.id || null,
        tag: el.tagName,
        display: style.display,
        visibility: style.visibility,
        opacity: style.opacity,
        pointerEvents: style.pointerEvents,
        rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
      };
    };

    const anyWindow = window as any;
    const activeRef = anyWindow.systemState?.ui?.dinoWrapperIframe || null;

    return {
      iframeCount: iframes.length,
      iframes: iframes.map((f, idx) => {
        const overlay = f.parentElement as HTMLElement | null;
        const overlay2 = overlay?.parentElement as HTMLElement | null;
        return {
          idx,
          src: f.getAttribute('src'),
          overlay: describeEl(overlay),
          overlayParent: describeEl(overlay2),
        };
      }),
      activeRefPresent: !!activeRef,
      activeRefIsFirstQuerySelector: activeRef ? activeRef === iframes[0] : false,
      activeRefOwnerOverlayDisplay: activeRef ? window.getComputedStyle((activeRef as HTMLElement).parentElement as HTMLElement).display : null,
    };
  });

  await testInfo.attach('dino_iframe_snapshot.json', {
    body: Buffer.from(JSON.stringify(diag, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  if (STRICT_DIAG) {
    expect(diag.iframeCount, 'Expected exactly one #dino-wrapper-iframe (STRICT) to avoid reference contention').toBe(1);
    expect(diag.activeRefOwnerOverlayDisplay, 'Expected active dino iframe overlay to be visible').not.toBe('none');
  }
});

test('Gen6 v9 diag: replay seq01 correlates fsm_edge → dino_postMessage → ack', async ({ hfoPage }, testInfo) => {
  await hfoPage.goto(GEN6_URL);
  await hfoPage.waitForFunction(() => !!(window as any).hfoReplay, null, { timeout: 20_000 });

  // Some newer builds expose multiple app launchers (e.g. Touch2D/Dino).
  // Ensure Dino is active so the replay sequence can exercise the dino adapter path.
  const dinoBtn = hfoPage.locator('button:has-text("Dino")').first();
  if (await dinoBtn.isVisible()) {
    await dinoBtn.click();
  }

  // Ensure the runtime loop is actually processing frames (some builds gate on IGNITE).
  await hfoPage.initHFO();
  await installReplayPipelineDiag(hfoPage);
  await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

  const preSnap = await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    return {
      ts: Date.now(),
      frameId: Number(anyWindow.systemState?.dataFabric?.frameId || 0),
      predictLoopStarted: !!anyWindow.__hfoReplayPredictLoopStarted,
      p0Active: !!anyWindow.systemState?.parameters?.p0Active,
      hasPortsEffectsSubscribe: typeof anyWindow.hfoPortsEffects?.subscribe === 'function',
      diag: {
        recognizeCalls: Number(anyWindow.__hfoDiag?.recognizeCalls || 0),
        fuseCalls: Number(anyWindow.__hfoDiag?.fuseCalls || 0),
        lastFuseCursorCount: anyWindow.__hfoDiag?.lastFuseCursorCount ?? null,
        mockResultsAssignments: Number(anyWindow.__hfoDiag?.mockResultsAssignments || 0),
        lastMockResultsMeta: anyWindow.__hfoDiag?.lastMockResultsMeta ?? null,
        mockPlayerCalls: Number(anyWindow.__hfoDiag?.mockPlayerCalls || 0),
        p1FsmEdgeEvents: Number(anyWindow.__hfoDiag?.p1FsmEdgeEvents || 0),
      },
      readiness: Array.isArray(anyWindow.systemState?.p1?.readinessScores) ? [...anyWindow.systemState.p1.readinessScores] : null,
      fsmStates: Array.isArray(anyWindow.systemState?.p1?.fsmStates) ? [...anyWindow.systemState.p1.fsmStates] : null,
    };
  });

  const out = await hfoPage.evaluate(async (manifestUrl) => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag.acks = [];
    await anyWindow.hfoReplay.loadManifestUrl(manifestUrl);
    const rep = await anyWindow.hfoReplay.runSequence('seq01_basic_fill_then_drain');
    await new Promise((r) => setTimeout(r, 150));

    const ackOkCount = (anyWindow.__hfoDiag.acks || []).filter((a: any) => a?.payload?.ok).length;
    const ackTotal = (anyWindow.__hfoDiag.acks || []).length;

    return { rep, ackTotal, ackOkCount };
  }, GOLDEN_MANIFEST_URL);

  const postSnap = await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    return {
      ts: Date.now(),
      frameId: Number(anyWindow.systemState?.dataFabric?.frameId || 0),
      predictLoopStarted: !!anyWindow.__hfoReplayPredictLoopStarted,
      p0Active: !!anyWindow.systemState?.parameters?.p0Active,
      diag: {
        recognizeCalls: Number(anyWindow.__hfoDiag?.recognizeCalls || 0),
        fuseCalls: Number(anyWindow.__hfoDiag?.fuseCalls || 0),
        lastFuseCursorCount: anyWindow.__hfoDiag?.lastFuseCursorCount ?? null,
        mockResultsAssignments: Number(anyWindow.__hfoDiag?.mockResultsAssignments || 0),
        lastMockResultsMeta: anyWindow.__hfoDiag?.lastMockResultsMeta ?? null,
        mockPlayerCalls: Number(anyWindow.__hfoDiag?.mockPlayerCalls || 0),
        p1FsmEdgeEvents: Number(anyWindow.__hfoDiag?.p1FsmEdgeEvents || 0),
      },
      readiness: Array.isArray(anyWindow.systemState?.p1?.readinessScores) ? [...anyWindow.systemState.p1.readinessScores] : null,
      fsmStates: Array.isArray(anyWindow.systemState?.p1?.fsmStates) ? [...anyWindow.systemState.p1.fsmStates] : null,
    };
  });

  const runtime = {
    pre: preSnap,
    post: postSnap,
    frameDelta: Number(postSnap.frameId) - Number(preSnap.frameId),
  };

  await testInfo.attach('seq01_runtime_snapshot.json', {
    body: Buffer.from(JSON.stringify(runtime, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  await fs.writeFile(testInfo.outputPath('seq01_runtime_snapshot.json'), JSON.stringify(runtime, null, 2), 'utf-8');

  await testInfo.attach('seq01_report.json', {
    body: Buffer.from(JSON.stringify(out, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  const fsmEdge = Number(out.rep?.counts?.fsmEdge || 0);
  const dinoPostMessageOk = Number(out.rep?.counts?.dinoPostMessageOk || 0);
  const ackOkCount = Number(out.ackOkCount || 0);

  let failureStage: string | null = null;
  if (fsmEdge < 1) failureStage = runtime.frameDelta <= 0 ? 'p0_loop_not_advancing' : 'p1_edge_missing';
  else if (dinoPostMessageOk < 1) failureStage = 'p7_postmessage_missing';
  else if (ackOkCount < 1) failureStage = 'wrapper_ack_missing_or_not_ok';

  if (failureStage && FAIL_CLOSED) {
    const diagTail = await hfoPage.evaluate(() => {
      const anyWindow = window as any;
      return {
        acksLast: (anyWindow.__hfoDiag?.acks || []).slice(-25),
        messagesLast: (anyWindow.__hfoDiag?.messages || []).slice(-25),
        portEffectsLast: (anyWindow.__hfoDiag?.portEffects || []).slice(-50),
      };
    });

    await writeFirstFailureBundle(testInfo, {
      kind: 'gen6_v9_seq01_failure_bundle',
      stage: failureStage,
      runtime,
      repCounts: out.rep?.counts || {},
      ack: { total: Number(out.ackTotal || 0), ok: Number(out.ackOkCount || 0) },
      diagTail,
    });

    expect(
      failureStage,
      `FAIL_CLOSED: stage=${failureStage} counts=${JSON.stringify(out.rep?.counts || {})} ackOk=${ackOkCount} ackTotal=${Number(out.ackTotal || 0)}`,
    ).toBeNull();
  }

  // If we're not failing closed, keep the numeric assertions as signals in CI output.
  expect(fsmEdge, 'Expected at least one p1:fsm_edge for seq01').toBeGreaterThanOrEqual(1);
  expect(dinoPostMessageOk, 'Expected at least one p7:dino_postMessage ok for seq01').toBeGreaterThanOrEqual(1);
  expect(ackOkCount, 'Expected at least one hfo:nematocyst:ack with ok:true for seq01').toBeGreaterThanOrEqual(1);
});

test('Gen6 v9 diag: CV input availability snapshot (camera devices)', async ({ hfoPage }, testInfo) => {
  await hfoPage.goto(GEN6_URL);

  const snap = await hfoPage.evaluate(async () => {
    const url = new URL(window.location.href);
    const flagDisableCamera = url.searchParams.get('flag-disable-camera');

    const hasMediaDevices = !!(navigator.mediaDevices && navigator.mediaDevices.enumerateDevices);
    let devices: any[] = [];
    let enumerateError: any = null;

    if (hasMediaDevices) {
      try {
        devices = await navigator.mediaDevices.enumerateDevices();
      } catch (err: any) {
        enumerateError = { name: err?.name || null, message: err?.message || String(err) };
      }
    }

    const videoInputs = devices.filter((d: any) => d?.kind === 'videoinput');
    return {
      href: window.location.href,
      flagDisableCamera,
      hasMediaDevices,
      enumerateError,
      videoInputCount: videoInputs.length,
      videoInputs: videoInputs.map((d: any) => ({
        deviceId: d?.deviceId || null,
        label: d?.label || null,
        groupId: d?.groupId || null,
      })),
    };
  });

  await testInfo.attach('cv_input_snapshot.json', {
    body: Buffer.from(JSON.stringify(snap, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  await fs.writeFile(testInfo.outputPath('cv_input_snapshot.json'), JSON.stringify(snap, null, 2), 'utf-8');
});

test('Gen6 v9 diag: stress seq01 correlation (classify first failure)', async ({ hfoPage }, testInfo) => {
  // This is intentionally slow (each seq01 run sleeps ~2.5s). Scale timeout with repeats.
  test.setTimeout(60_000 + STRESS_REPEATS * 15_000);
  await hfoPage.goto(GEN6_URL);
  await hfoPage.waitForFunction(() => !!(window as any).hfoReplay, null, { timeout: 20_000 });

  const dinoBtn = hfoPage.locator('button:has-text("Dino")').first();
  if (await dinoBtn.isVisible()) {
    await dinoBtn.click();
  }

  await hfoPage.initHFO();
  await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

  await installReplayPipelineDiag(hfoPage);

  await hfoPage.evaluate(async (manifestUrl) => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag.acks = [];
    await anyWindow.hfoReplay.loadManifestUrl(manifestUrl);
  }, GOLDEN_MANIFEST_URL);

  const iterations: any[] = [];
  for (let i = 0; i < STRESS_REPEATS; i++) {
    const iter = await hfoPage.evaluate(async (seqName) => {
      const anyWindow = window as any;

      const snapshot = () => {
        const hasStartMockReplay = typeof anyWindow.hfoStartMockReplay === 'function';
        const predictLoopStarted = !!anyWindow.__hfoReplayPredictLoopStarted;
        const p0Active = !!anyWindow.systemState?.parameters?.p0Active;
        const hasPortsEffectsSubscribe = typeof anyWindow.hfoPortsEffects?.subscribe === 'function';
        const hasDinoIframe = !!document.querySelector('#dino-wrapper-iframe');
        const frameId = Number(anyWindow.systemState?.dataFabric?.frameId || 0);
        const recognizeCalls = Number(anyWindow.__hfoDiag?.recognizeCalls || 0);
        const fuseCalls = Number(anyWindow.__hfoDiag?.fuseCalls || 0);
        const lastFuseCursorCount = anyWindow.__hfoDiag?.lastFuseCursorCount ?? null;
        const mockResultsAssignments = Number(anyWindow.__hfoDiag?.mockResultsAssignments || 0);
        const lastMockResultsMeta = anyWindow.__hfoDiag?.lastMockResultsMeta ?? null;
        const mockPlayerCalls = Number(anyWindow.__hfoDiag?.mockPlayerCalls || 0);
        const mockPlayerIsPlaying = !!anyWindow.hfoMockPlayer?.isPlaying;
        const readiness = Array.isArray(anyWindow.systemState?.p1?.readinessScores) ? [...anyWindow.systemState.p1.readinessScores] : null;
        const fsmStates = Array.isArray(anyWindow.systemState?.p1?.fsmStates) ? [...anyWindow.systemState.p1.fsmStates] : null;
        return {
          hasStartMockReplay,
          predictLoopStarted,
          p0Active,
          hasPortsEffectsSubscribe,
          hasDinoIframe,
          frameId,
          recognizeCalls,
          fuseCalls,
          lastFuseCursorCount,
          mockResultsAssignments,
          lastMockResultsMeta,
          mockPlayerCalls,
          mockPlayerIsPlaying,
          readiness,
          fsmStates,
        };
      };

      const pre = snapshot();
      anyWindow.__hfoDiag.acks = [];
      const rep = await anyWindow.hfoReplay.runSequence(seqName);
      await new Promise((r) => setTimeout(r, 100));
      const post = snapshot();

      const acks = anyWindow.__hfoDiag.acks || [];
      return {
        pre,
        post,
        counts: rep?.counts || {},
        final: rep?.final || null,
        ackTotal: acks.length,
        ackOkCount: acks.filter((a: any) => a?.payload?.ok).length,
        ackLast5: acks.slice(-5),
      };
    }, 'seq01_basic_fill_then_drain');

    const fsmEdge = Number(iter?.counts?.fsmEdge || 0);
    const dinoPostMessageOk = Number(iter?.counts?.dinoPostMessageOk || 0);
    const ackOkCount = Number(iter?.ackOkCount || 0);
    const frameDelta = Number(iter?.post?.frameId || 0) - Number(iter?.pre?.frameId || 0);

    let failureStage: string | null = null;
    if (fsmEdge < 1) failureStage = frameDelta <= 0 ? 'p0_loop_not_advancing' : 'p1_edge_missing';
    else if (dinoPostMessageOk < 1) failureStage = 'p7_postmessage_missing';
    else if (ackOkCount < 1) failureStage = 'wrapper_ack_missing_or_not_ok';

    iterations.push({ i, ...iter, frameDelta, failureStage });
  }

  const failures = iterations.filter((it) => it.failureStage);
  const byStage = failures.reduce((acc: Record<string, number>, it: any) => {
    const k = String(it.failureStage || 'unknown');
    acc[k] = (acc[k] || 0) + 1;
    return acc;
  }, {});
  const out = {
    repeats: STRESS_REPEATS,
    failures: failures.length,
    firstFailure: failures[0] || null,
    byStage,
    iterations,
  };

  await testInfo.attach('stress_seq01_summary.json', {
    body: Buffer.from(JSON.stringify(out, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  await fs.writeFile(testInfo.outputPath('stress_seq01_summary.json'), JSON.stringify(out, null, 2), 'utf-8');

  expect(out.repeats).toBeGreaterThanOrEqual(1);
  if (out.failures > 0) {
    const firstStage = out.firstFailure?.failureStage || 'unknown';
    const hint = out.firstFailure?.failureStage === 'wrapper_ack_missing_or_not_ok'
      ? `ackLast5=${JSON.stringify(out.firstFailure?.ackLast5 || [])}`
      : '';

    testInfo.annotations.push({
      type: 'failure_observed',
      description: `Observed ${out.failures}/${out.repeats} failures; byStage=${JSON.stringify(out.byStage)}; firstFailureStage=${firstStage}`,
    });

    if (FAIL_CLOSED) {
      await writeFirstFailureBundle(testInfo, {
        kind: 'gen6_v9_stress_seq01_failure_bundle',
        repeats: out.repeats,
        failures: out.failures,
        byStage: out.byStage,
        firstFailure: out.firstFailure,
      });

      expect(
        out.failures,
        `FAIL_CLOSED: observed ${out.failures}/${out.repeats} failures; byStage=${JSON.stringify(out.byStage)}; first=${firstStage} ${hint}`,
      ).toBe(0);
    }
  }
});

test('Gen6 v9 diag: manual replay drive samples readiness + fsm_edge (bypass hfoReplay)', async ({ hfoPage }, testInfo) => {
  test.setTimeout(180_000);

  // Reduce GPU churn for this diagnostic (Babylon can trigger WebGL context loss on some systems).
  const lightUrl = GEN6_URL
    .replace('flag-engine-babylon=true&', '')
    .replace('flag-ui-excalidraw=true&', '');

  await hfoPage.goto(lightUrl);
  await hfoPage.initHFO();

  const out = await hfoPage.evaluate(async () => {
    const anyWindow = window as any;
    const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

    const dummyLandmarks = () => Array.from({ length: 21 }, (_, j) => ({
      x: 0.5 + (j % 5) * 0.002,
      y: 0.5 + Math.floor(j / 5) * 0.002,
      z: 0,
    }));

    const makeResults = (shouldFill: boolean) => ({
      landmarks: [dummyLandmarks()],
      gestures: [[{ categoryName: 'None', score: 1.0 }]],
      __hfoReplayHands: [{
        handIndex: 0,
        isFacingCamera: shouldFill,
        isCharging: shouldFill,
        hasConfidence: true,
        shouldFill,
      }],
    });

    // Force a known baseline.
    try { anyWindow.hfoPortsEffects?.clear?.(); } catch { }
    anyWindow.systemState.parameters.p0Active = true;
    anyWindow.systemState.parameters.landmarks.numHands = 1;
    anyWindow.systemState.p1.readinessScores[0] = 0;
    anyWindow.systemState.p1.fsmStates[0] = 'IDLE';
    anyWindow.systemState.fsm.primaryHandIndex = null;
    anyWindow.systemState.fsm.readyTriggerCooldownMs = 0;
    anyWindow.systemState.fsm.lastReadyTriggerTimes = [0];

    // Ensure loop is running.
    if (typeof anyWindow.hfoStartMockReplay === 'function') {
      anyWindow.hfoStartMockReplay();
    }

    const events: any[] = [];
    const off = anyWindow.hfoPortsEffects?.subscribe?.((e: any) => { if (e) events.push(e); }) || (() => { });

    // Step 1: fill.
    anyWindow.hfoMockResults = makeResults(true);
    await sleep(1200);
    const mid = {
      readiness: anyWindow.systemState.p1.readinessScores[0],
      fsm: anyWindow.systemState.p1.fsmStates[0],
    };

    // Step 2: drain.
    anyWindow.hfoMockResults = makeResults(false);
    await sleep(1200);
    const end = {
      readiness: anyWindow.systemState.p1.readinessScores[0],
      fsm: anyWindow.systemState.p1.fsmStates[0],
    };

    anyWindow.hfoMockResults = null;
    off();

    const fsmEdge = events.filter((e) => e?.port === 'p1' && e?.type === 'fsm_edge').length;
    const cooldownSuppressed = events.filter((e) => e?.port === 'p1' && e?.type === 'cooldown_suppressed').length;
    return {
      mid,
      end,
      counts: { fsmEdge, cooldownSuppressed },
      last10: events.slice(-10),
    };
  });

  await testInfo.attach('manual_replay_drive.json', {
    body: Buffer.from(JSON.stringify(out, null, 2), 'utf-8'),
    contentType: 'application/json',
  });

  // Diagnostic assertions: we expect fill to push to READY at least once.
  expect(out.counts.fsmEdge, `Expected at least one fsm_edge; got last10=${JSON.stringify(out.last10)}`).toBeGreaterThanOrEqual(1);
});
