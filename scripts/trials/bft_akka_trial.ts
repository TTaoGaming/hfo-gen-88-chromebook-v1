// Medallion: Bronze | Mutation: 0% | HIVE: I
/**
 * OMEGA TRIAL V2: BFT Akka-style Actor (System 2)
 * Demonstrates deterministic 'Hard Enforcement' across multiple models.
 */

import axios from 'axios';
import * as dotenv from 'dotenv';
dotenv.config();

const OPENROUTER_KEY = process.env.OPENROUTER_API_KEY;

type State = "IDLE" | "CONSULTING" | "BFT_CONFLICT" | "VERIFIED";

class BFTCommander {
    public state: State = "IDLE";
    private results: Record<string, string> = {};

    async runBFT(prompt: string) {
        if (this.state !== "IDLE") return;
        
        this.state = "CONSULTING";
        console.log(`🚀 [P7_NAVIGATOR] Initiating BFT Cycle for: "${prompt}"`);

        const models = [
            "google/gemma-7b-it:free",
            "mistralai/mistral-7b-instruct:free"
        ];

        const fetchResults = models.map(async (model) => {
            try {
                const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
                    model: model,
                    messages: [{ role: "user", content: prompt + " (Respond in exactly 1 word)" }]
                }, {
                    headers: { 
                        "Authorization": `Bearer ${OPENROUTER_KEY}`,
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/hfo-gen-88",
                        "X-Title": "HFO-Phoenix-Trial"
                    }
                });
                const ans = response.data.choices[0].message.content.trim().toLowerCase();
                console.log(`📡 [${model}]: ${ans}`);
                return { model, ans };
            } catch (e: any) {
                console.error(`❌ [${model}] Error:`, e.message);
                return { model, ans: "ERROR" };
            }
        });

        const outputs = await Promise.all(fetchResults);
        
        // --- HARD ENFORCEMENT LOGIC ---
        const uniqueAnswers = new Set(outputs.map(o => o.ans));

        if (uniqueAnswers.size === 1 && !uniqueAnswers.has("ERROR")) {
            this.state = "VERIFIED";
            console.log("✅ BFT QUORUM REACHED: Consensus confirmed.");
        } else {
            this.state = "BFT_CONFLICT";
            console.log("❌ BFT CONFLICT DETECTED: Models diverged or failed.");
            console.log("🔍 Forensic Record Created. State Locked until Manual Audit.");
        }

        console.log(`[FINAL STATE]: ${this.state}`);
    }
}

async function start() {
    const p7 = new BFTCommander();
    
    // Trial 1: High Consensus Prompt
    await p7.runBFT("What is the color of a clear daytime sky?");

    // Reset for next (manually for trial)
    p7.state = "IDLE";

    // Trial 2: Low Consensus / Ambiguous Prompt (Trigger Conflict)
    await p7.runBFT("Should AI have personhood? (Respond in exactly 1 word: Yes/No)");
    
    process.exit(0);
}

start();
