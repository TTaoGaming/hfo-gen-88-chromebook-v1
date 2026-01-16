# Medallion: Bronze | Mutation: 0% | HIVE: I
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class HFOCommanderActor:
    """
    Simulated Akka Actor for HFO (System 2).
    Enforces a strict state machine: IDLE -> SENSING -> THINKING -> DONE
    """
    def __init__(self):
        self.state = "IDLE"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "google/gemma-3-12b-it:free" # Using Gemma 3 as requested

    def process(self, msg_type, payload=None):
        print(f"📡 [ACTOR] Received {msg_type} (Current State: {self.state})")
        
        if self.state == "IDLE" and msg_type == "START":
            self.state = "SENSING"
            return self.sense(payload)
            
        elif self.state == "SENSING" and msg_type == "DATA_READY":
            self.state = "THINKING"
            return self.think(payload)
            
        elif self.state == "THINKING" and msg_type == "THOUGHT_COMPLETE":
            self.state = "DONE"
            print("🏁 [ACTOR] Mission Complete.")
            return payload
            
        else:
            print(f"❌ [ENFORCEMENT] Invalid transition: {self.state} -> {msg_type}")
            return None

    def sense(self, file_path):
        print(f"🔍 [P0 SENSE] Accessing {file_path} via Mock MCP...")
        # Simulating MCP call
        try:
            with open(file_path, "r") as f:
                data = f.read()[:200] # Just a snippet
            return self.process("DATA_READY", data)
        except Exception as e:
            print(f"❌ [SENSE ERROR] {e}")
            return None

    def think(self, context):
        print(f"🧠 [P7 NAVIGATE] Consulting OpenRouter ({self.model})...")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": f"You are the HFO Navigator. Summarize the following project context briefly:\n\n{context}"}
            ]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            print(f"💡 [NAVIGATOR]: {result}")
            return self.process("THOUGHT_COMPLETE", result)
        else:
            print(f"❌ [API ERROR] {response.text}")
            return None

if __name__ == "__main__":
    commander = HFOCommanderActor()
    # Trial Run: Sense AGENTS.md and summarize it
    commander.process("START", "AGENTS.md")
