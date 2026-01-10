// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

/**
 * V30 E2E: Full FSM Lifecycle & Menu Interaction Test
 * This test simulates the manual "Hunt & Commit" workflow using the bridge.
 */
test('V30 E2E: Simulate Gesture-to-Click on Tool Menu', async ({ hfoPage }) => {
  // 1. Load the workspace
  const url = getActiveUrl();
  await hfoPage.goto(url);

  // 1.5 Manually trigger physics
  await hfoPage.initHFO();

  // Wait for Hands to be initialized
  await hfoPage.waitForHand(0);

  // Wait for Excalidraw and the interactive canvas
  const frame = hfoPage.frameLocator('iframe#excalidraw-iframe');
  const canvas = frame.locator('canvas.interactive');
  await expect(canvas).toBeVisible({ timeout: 20000 });

  // 2. Locate a target menu item (e.g., the Rectangle tool)
  const rectTool = frame.locator('label[title*="Rectangle"]');
  await expect(rectTool).toBeVisible();

  // Get positions
  const iframeEl = hfoPage.locator('iframe#excalidraw-iframe');
  const iframeBox = await iframeEl.boundingBox();
  const box = await rectTool.boundingBox();
  if (!box || !iframeBox) throw new Error("Could not find box for Rectangle tool or iframe");

  // Normalize relative to the IFRAME
  const targetX = (box.x + box.width / 2 - iframeBox.x) / iframeBox.width;
  const targetY = (box.y + box.height / 2 - iframeBox.y) / iframeBox.height;

  console.log(`Targeting Rectangle tool (Normalized to Iframe): ${targetX.toFixed(3)}, ${targetY.toFixed(3)}`);

  // 3. Inject State: Move hand to tool and transition FSM to COMMITTED
  await hfoPage.evaluate(() => {
    // @ts-ignore
    window.hfoState.physics.p3Mirror = false;
  });

  await hfoPage.injectHand(0, {
    active: true,
    state: 'COMMITTED',
    event: 'pointerdown',
    cursors: { predictive: { x: targetX, y: targetY } }
  });

  // 4. Inject State: Release
  await hfoPage.injectHand(0, {
    state: 'RELEASING',
    event: 'pointermove'
  });

  await hfoPage.injectHand(0, {
    state: 'ARMED',
    event: 'pointerup'
  });

  // 5. Verification
  const isSelected = await rectTool.evaluate((el) => {
    const input = el.querySelector('input');
    return input ? input.checked : el.classList.contains('active');
  });

  console.log(`V30 E2E: Rectangle tool selected? ${isSelected}`);
  expect(isSelected).toBe(true);
});

test('V30 E2E: Structural Check for Same-Origin Drill', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  // Verify that we can read internal document properties (Requires Same-Origin)
  const canAccessDocument = await hfoPage.evaluate(() => {
    const iframe = document.getElementById('excalidraw-iframe') as HTMLIFrameElement;
    try {
      return !!iframe.contentDocument;
    } catch (e) {
      return false;
    }
  });

  expect(canAccessDocument).toBe(true);
  console.log("V30 E2E: Same-Origin Drill verified.");
});
