import re
import sys
import os
import json

# Medallion: Bronze | Mutation: 0% | HIVE: V
# P5-GOLDILOCKS-SENTINEL: Prevents "AI Theater" by enforcing 88-98% mutation score.

MIN_SCORE = 88.0
MAX_SCORE = 98.0

def calculate_mutation_score(report_data):
    """Calculates mutation score from Stryker JSON report data."""
    killed = 0
    survived = 0
    timeout = 0
    no_coverage = 0
    
    files = report_data.get("files", {})
    if not files:
        return 0.0

    for file_path, file_data in files.items():
        for mutant in file_data.get("mutants", []):
            status = mutant.get("status")
            if status in ["Killed", "CompileError"]:
                killed += 1
            elif status == "Survived":
                survived += 1
            elif status == "Timeout":
                timeout += 1
            elif status == "NoCoverage":
                no_coverage += 1
                
    detected = killed + timeout
    total = detected + survived + no_coverage
    
    if total == 0:
        return 0.0
    
    return (detected / total) * 100

def check_mutation_score(report_path):
    if not os.path.exists(report_path):
        print(f"ERROR: Mutation report not found at {report_path}")
        sys.exit(1)

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract app.report JSON - using a non-greedy match and looking for the end of the script
    match = re.search(r'app\.report = (\{.*?\});\s*function', content, re.DOTALL)
    if not match:
        # Try a different boundary if the first one fails
        match = re.search(r'app\.report = (\{.*?\});', content, re.DOTALL)
        
    if not match:
        print("ERROR: Could not find mutation data in HTML report.")
        sys.exit(1)
        
    try:
        report_data = json.loads(match.group(1))
        score = calculate_mutation_score(report_data)
    except Exception as e:
        print(f"ERROR: Failed to parse mutation data: {e}")
        # Print a bit of the match to help debug
        print(f"DEBUG: Match snippet: {match.group(1)[:100]}...")
        sys.exit(1)

    print(f"Sensed Mutation Score: {score:.2f}%")

    if score > MAX_SCORE:
        print(f"🛑 [P5-BREACH]: Mutation score {score:.2f}% exceeds {MAX_SCORE}% limit.")
        print("Reason: High probability of 'AI Theater' (Over-fitted tests/Reward Hacking).")
        sys.exit(1)

    if score < MIN_SCORE:
        print(f"⚠️ [P5-UNDERLINK]: Mutation score {score:.2f}% is below {MIN_SCORE}% threshold.")
        print("Reason: Insufficient test coverage for Medallion Bronze promotion.")
        sys.exit(1)

    print(f"✅ [P5-GOLDILOCKS]: Mutation score {score:.2f}% is within valid range [{MIN_SCORE}%, {MAX_SCORE}%].")
    sys.exit(0)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/mutation/mutation.html"
    check_mutation_score(path)
