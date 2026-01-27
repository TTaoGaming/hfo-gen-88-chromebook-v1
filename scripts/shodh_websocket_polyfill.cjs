/*
Medallion: Bronze | Mutation: 0% | HIVE: V
Provenance: Node preload shim to polyfill WebSocket for @shodh/memory-mcp under Node 20.
*/

try {
  // @shodh/memory-mcp expects a global WebSocket implementation.
  // Node 20 does not provide one by default.
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const { WebSocket } = require("ws");

  if (typeof globalThis.WebSocket === "undefined") {
    globalThis.WebSocket = WebSocket;
  }
} catch (err) {
  // Fail closed: if the polyfill can't be loaded, shodh-memory MCP should error
  // clearly rather than silently skipping streaming features.
  // eslint-disable-next-line no-console
  console.error("[shodh-websocket-polyfill] Failed to install WebSocket global:", err);
}
