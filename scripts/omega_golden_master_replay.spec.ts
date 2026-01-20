// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import path from 'node:path';

const REPLAY_URL =
  process.env.HFO_REPLAY_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v1.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Golden Master Replay: JSONL playback sanity', async ({ hfoPage }) => {
  const replayPath =
    process.env.HFO_REPLAY_PATH ||
    path.resolve(
      process.cwd(),
      'hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.mirrored.jsonl',
    );
  if (!replayPath) {
    throw new Error('HFO_REPLAY_PATH is required (path to telemetry JSONL).');
  }

  await hfoPage.goto(REPLAY_URL);
  await hfoPage.initHFO();

  const jsonlText = fs.readFileSync(replayPath, 'utf-8');

  const count = await hfoPage.evaluate((text) => {
    // @ts-ignore
    return window.hfoLoadReplayFromText ? window.hfoLoadReplayFromText(text) : 0;
  }, jsonlText);

  expect(count).toBeGreaterThan(0);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    window.hfoPlayer.loop = false;
    // @ts-ignore
    window.hfoPlayer.start();
  });

  const replayStatus = await hfoPage.evaluate(() => {
    // @ts-ignore
    const player = window.hfoPlayer;
    if (!player || typeof player.getNextFrame !== 'function') return { index: 0, hasFrame: false };
    const frame = player.getNextFrame();
    return { index: player.index ?? 0, hasFrame: !!frame };
  });

  expect(replayStatus.hasFrame).toBe(true);
  expect(replayStatus.index).toBeGreaterThan(0);
});