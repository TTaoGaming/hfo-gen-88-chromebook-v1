// Medallion: Bronze | Mutation: 0% | HIVE: V
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const gatewayCmd = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.venv/bin/python";
const gatewayArgs = ["/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_mcp_gateway_hub.py"];

async function run() {
  const transport = new StdioClientTransport({
    command: gatewayCmd,
    args: gatewayArgs,
  });

  const client = new Client({
    name: "hfo-mcp-gateway-e2e",
    version: "1.0.0",
  });

  await client.connect(transport);

  const tools = await client.listTools();
  console.log("TOOLS:", tools.tools.map(t => t.name).join(", "));

  const phase1 = await client.callTool({
    name: "observe_navigate",
    arguments: { query: "E2E truth check: phase1 observe+navigate" },
  });
  console.log("PHASE1:", JSON.stringify(phase1, null, 2));

  const phase2 = await client.callTool({
    name: "bridge_assimilate",
    arguments: { note: "E2E truth check: phase2 bridge+assimilate" },
  });
  console.log("PHASE2:", JSON.stringify(phase2, null, 2));

  const phase3 = await client.callTool({
    name: "shape_immunize",
    arguments: { note: "E2E truth check: phase3 shape+immunize", mode: "preflight" },
  });
  console.log("PHASE3:", JSON.stringify(phase3, null, 2));

  const phase4 = await client.callTool({
    name: "deliver_disrupt",
    arguments: { note: "E2E truth check: phase4 deliver+disrupt" },
  });
  console.log("PHASE4:", JSON.stringify(phase4, null, 2));

  const commit = await client.callTool({
    name: "commit",
    arguments: { message: "E2E truth check: gateway commit" },
  });
  console.log("COMMIT:", JSON.stringify(commit, null, 2));

  await client.close();
}

run().catch(err => {
  console.error("E2E failed:", err);
  process.exit(1);
});
