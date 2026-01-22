// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';
import fs from 'node:fs';

const parseMeta = (text: string) => {
  let fps = 30;
  let frames = 0;
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    const obj = JSON.parse(line);
    if (obj.type === 'meta') {
      if (obj.fps) fps = obj.fps;
    }
    if (obj.type === 'frame') frames += 1;
  }
  return { fps, frames };
};

test('Clip Replay FSM: IDLE→READY→COMMIT→IDLE + move right', async ({ hfoPage }) => {
  const jsonlPath = process.env.HFO_CLIP_JSONL;
  if (!jsonlPath) {
    throw new Error('HFO_CLIP_JSONL is required (path to mock results JSONL).');
  }

  const url = process.env.HFO_GEN5_URL || getActiveUrl('gen5_v1');
  await hfoPage.goto(url);
  await hfoPage.initHFO();

  const jsonlText = fs.readFileSync(jsonlPath, 'utf-8');
  const meta = parseMeta(jsonlText);

  await hfoPage.evaluate((text) => {
    // @ts-ignore
    return window.hfoLoadMockResultsFromText(text);
  }, jsonlText);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    window.__hfoTestLog = [];
    // @ts-ignore
    window.__hfoTestTimer = setInterval(() => {
      // @ts-ignore
      const hands = window.hfoState?.hands || [];
      const h0 = hands[0];
      // @ts-ignore
      const fsm = window.hfoState?.fsm?.currentState || 'IDLE';
      // @ts-ignore
      const x = h0?.screenX ?? null;
      // @ts-ignore
      window.__hfoTestLog.push({ t: performance.now(), fsm, x });
    }, 50);
  });

  await hfoPage.evaluate(() => {
    // @ts-ignore
    window.hfoMockResultsPlayer.start();
  });

  const durationMs = Math.ceil((meta.frames / meta.fps) * 1000) + 1000;
  await hfoPage.waitForTimeout(durationMs);

  const log = await hfoPage.evaluate(() => {
    // @ts-ignore
    clearInterval(window.__hfoTestTimer);
    // @ts-ignore
    return window.__hfoTestLog || [];
  });

  const sequence = log
    .map((e: any) => e.fsm)
    .filter((v: string, i: number, arr: string[]) => i === 0 || v !== arr[i - 1]);

  expect(sequence[0]).toBe('IDLE');
  expect(sequence).toContain('READY');
  expect(sequence).toContain('COMMIT');
  expect(sequence[sequence.length - 1]).toBe('IDLE');

  const commits = log.filter((e: any) => e.fsm === 'COMMIT' && typeof e.x === 'number');
  expect(commits.length).toBeGreaterThan(2);
  const moveRight = commits[commits.length - 1].x - commits[0].x;
  expect(moveRight).toBeGreaterThan(5);
});
