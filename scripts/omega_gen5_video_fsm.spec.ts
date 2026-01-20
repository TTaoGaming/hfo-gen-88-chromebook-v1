// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import path from 'node:path';

const GEN5_URL = 'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v1.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Gen5 video FSM sequence: IDLE→READY→COMMIT→IDLE', async ({ hfoPage }) => {
  const replayPath =
    process.env.HFO_REPLAY_PATH ||
    path.resolve(
      process.cwd(),
      'hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.mirrored.jsonl',
    );
  if (!replayPath) {
    throw new Error('HFO_REPLAY_PATH is required (path to mock JSONL).');
  }

  await hfoPage.goto(GEN5_URL);

  const jsonlText = fs.readFileSync(replayPath, 'utf-8');

  const count = await hfoPage.evaluate((text) => {
    // @ts-ignore
    return window.hfoMockPlayer ? window.hfoMockPlayer.loadFromText(text) : 0;
  }, jsonlText);

  expect(count).toBeGreaterThan(0);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    window.hfoMockPlayer.start();
    // @ts-ignore
    if (window.hfoStartMockReplay) window.hfoStartMockReplay();
  });

  const states = await hfoPage.evaluate(async () => {
    const timeline: string[] = [];
    let last = null;
    const start = performance.now();
    while (performance.now() - start < 6000) {
      // @ts-ignore
      const s = window.hfoState?.fsm?.currentState || 'UNKNOWN';
      if (s !== last) {
        timeline.push(s);
        last = s;
      }
      await new Promise((r) => setTimeout(r, 50));
    }
    return timeline;
  });

  console.log('FSM timeline:', states);

  expect(states).toContain('IDLE');
  expect(states).toContain('READY');
  expect(states).toContain('COMMIT');
  const idleIndex = states.indexOf('IDLE');
  const readyIndex = states.indexOf('READY');
  const commitIndex = states.indexOf('COMMIT');
  const lastIdleIndex = states.lastIndexOf('IDLE');

  expect(readyIndex).toBeGreaterThan(idleIndex);
  expect(commitIndex).toBeGreaterThan(readyIndex);
  expect(lastIdleIndex).toBeGreaterThan(commitIndex);
});
