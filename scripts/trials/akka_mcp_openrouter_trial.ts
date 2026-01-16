// Medallion: Bronze | Mutation: 0% | HIVE: I
/**
 * OMEGA TRIAL V1: Akka-style Actor + MCP + OpenRouter
 * Focus: Hard Enforcement and Standardized Tool Access (MCP).
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import * as dotenv from 'dotenv';

// Load environment variables from .env
dotenv.config();

const OPENROUTER_KEY = process.env.OPENROUTER_API_KEY;

if (!OPENROUTER_KEY) {
    console.error("❌ OPENROUTER_API_KEY not found in .env");
    process.exit(1);
}

/**
 * HFO Actor Substrate (Deterministic State Machine)
 * This replicates the Akka 'Hard Enforcement' logic.
 */
abstract class HFOActor {
    protected state: string = "IDLE";
    
    public async tell(msg: any) {
        console.log(`[STATE: ${this.state}] Handling message...`);
        // Enforcement: In a real actor, this would be an atomic check.
        await this.onReceive(msg);
    }

    protected abstract onReceive(msg: any): Promise<void>;
}

class CommanderP7 extends HFOActor {
    private model = "google/gemma-7b-it:free";

    protected async onReceive(msg: any) {
        if (this.state !== "IDLE") {
            console.error("❌ ENFORCEMENT BREACH: Actor is not in IDLE state.");
            return;
        }

        this.state = "NAVIGATING";
        console.log(`[P7_NAVIGATE] Task: ${msg.prompt}`);

        // Setup MCP Transport
        const transport = new StdioClientTransport({
            command: "npx",
            args: ["-y", "@stabgan/openrouter-mcp-multimodal"],
            env: { ...process.env, OPENROUTER_API_KEY: OPENROUTER_KEY }
        });

        const client = new Client({
            name: "HFO_Navigator_Trial",
            version: "1.0.0"
        }, {
            capabilities: {}
        });

        try {
            await client.connect(transport);
            
            // Call OpenRouter via MCP
            const response = await client.callTool({
                name: "chat",
                arguments: {
                    model: this.model,
                    messages: [{ role: "user", content: msg.prompt }]
                }
            });

            // Extract content from response
            const content = (response.content as any)[0].text;
            console.log("\n--- 🤖 OPENROUTER (GEMMA) RESPONSE ---");
            console.log(content);
            console.log("--------------------------------------\n");

            this.state = "IDLE"; // Reset state after success
            console.log("✅ Mission Success. State Reset to IDLE.");

        } catch (error) {
            console.error("❌ MCP/Actor Error:", error);
            this.state = "FAILED"; 
        } finally {
            // Transport usually stays open if we want to reuse, but for trial we finish.
        }
    }
}

// Execution
async function runTrial() {
    console.log("🚀 HFO Trial Run: Akka Logic + MCP Server + OpenRouter Integration");
    const commander = new CommanderP7();

    // Success Flow
    await commander.tell({ prompt: "Briefly explain why Akka is better than CrewAI for 'Hard Enforcement'." });
    process.exit(0);
}

runTrial();
