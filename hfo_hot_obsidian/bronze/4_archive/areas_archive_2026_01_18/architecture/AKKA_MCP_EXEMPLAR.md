# Medallion: Bronze | Mutation: 0% | HIVE: I

# 🏗️ HFO Master Class: Akka + MCP Enforcement

## 1. The Akka Actor (System 2: Logic)
In Akka, we don't say `agent.run()`. We send a **Message**.
If the `Commander` actor receives a `SENSE_COMPLETE` message, it *must* transition to the `FUSE` state.

```typescript
// Pseudocode for an Akka-style Actor implementation in HFO
class CommanderActor extends Actor {
  private state: State = "IDLE";

  onReceive(msg: Message) {
    switch(this.state) {
      case "IDLE":
        if (msg.type === "START_MISSION") {
          this.state = "READY";
          this.context.send("P0_SENSE", { command: "SEARCH_FS" });
        }
        break;
      case "READY":
        if (msg.type === "DATA_RECEIVED") {
          this.state = "COMMIT";
          // Akka Enforces: You CANNOT commit without data.
          this.process(msg.payload);
        }
        break;
    }
  }
}
```

## 2. The MCP Server (System 1: Connection)
Unlike CrewAI, where you pass a Python function name, MCP uses a **Schema**.
The AI asks the MCP Host: "What can you do?" The Host replies with a JSON definition.

```json
{
  "name": "duckdb_query",
  "description": "Execute SQL on the HFO telemetry DB",
  "inputSchema": {
    "type": "object",
    "properties": {
      "sql": { "type": "string" }
    },
    "required": ["sql"]
  }
}
```

## 3. Why CrewAI Fails the "Hard Enforcement" Test
- **CrewAI**: "You are an agent. Please follow these directions: Step 1, Step 2..." (Agent might hallucinate and skip to Step 4).
- **Akka/MCP**: The system **mechanically blocks** Step 4. If the `state` is not `STEP_3_COMPLETE`, the message for `STEP_4` is ignored or buffered.

## 4. The 8-Port Mapping
| Port | Role | Tool (2026) |
| :--- | :--- | :--- |
| **P0 SENSE** | Search/Ingest | MCP (Tavily/Local FS) |
| **P1 FUSE** | Schema Logic | Zod 6.0 |
| **P2 SHAPE** | Physics/State | Akka Persistence |
| **P3 DELIVER** | W3C Events | Akka Actors |
| **P7 NAVIGATE** | Orchestration | Akka Cluster Sharding |

---
*Spider Sovereign (Port 7) | Gen 88 Guidance*
