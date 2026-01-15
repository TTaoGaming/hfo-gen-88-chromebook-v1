#!/usr/bin/env python3
import sys
import re
import subprocess
import os

def check_html_logic(file_path):
    print(f"🧬 Auditing Logic for {file_path}...")
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract HFO_CONSTANTS
        hfo_match = re.search(r'const HFO_CONSTANTS = (\{.*?\});', content, re.DOTALL)
        hfo_constants = hfo_match.group(0) if hfo_match else "const HFO_CONSTANTS = {};"

        # Find ConfigSchema
        schema_start = content.find("const ConfigSchema = z.object({")
        if schema_start == -1:
            print("❌ MISSING: ConfigSchema not found.")
            return False
            
        # Find the end of ConfigSchema by counting braces
        brace_count = 0
        schema_end = -1
        for i in range(schema_start + 20, len(content)):
            if content[i] == '{': brace_count += 1
            if content[i] == '}': 
                brace_count -= 1
                if brace_count == 0:
                    # Look for the .default({}); part
                    search_limit = min(i + 100, len(content))
                    post_block = content[i+1:search_limit]
                    if ".default({});" in post_block:
                        schema_end = i + post_block.find(".default({});") + 13
                    else:
                        schema_end = i + 2
                    break
        
        schema_str = content[schema_start:schema_end]

        # Find systemState
        state_start = content.find("const systemState = {")
        if state_start == -1:
            state_start = content.find("let systemState = {")
            
        if state_start == -1:
            print("❌ MISSING: systemState not found.")
            return False

        brace_count = 0
        state_end = -1
        for i in range(state_start + 15, len(content)):
            if content[i] == '{': brace_count += 1
            if content[i] == '}': 
                brace_count -= 1
                if brace_count == 0:
                    state_end = i + 2
                    break
        
        state_str = content[state_start:state_end]

        eval_body = f"""
import {{ z }} from 'zod';
{hfo_constants}
{schema_str}
{state_str}
try {{
    ConfigSchema.parse(systemState.parameters || systemState);
    process.exit(0);
}} catch (err) {{
    console.error(JSON.stringify(err.errors, null, 2));
    process.exit(1);
}}
"""
        with open('temp_eval.js', 'w') as tmp: tmp.write(eval_body)
        process = subprocess.Popen(['node', 'temp_eval.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if os.path.exists('temp_eval.js'): os.remove('temp_eval.js')
        if process.returncode != 0:
            print(f"❌ Logic Error in {file_path}:")
            print(stderr or stdout)
            return False
        print(f"✅ {file_path} logic is valid (Schema Parity).")
        return True
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        check_html_logic(arg)
