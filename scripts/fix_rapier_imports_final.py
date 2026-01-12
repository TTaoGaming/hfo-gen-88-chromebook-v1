import os
import re

root_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/lib/rapier"

def fix_imports_final(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Matches: from "./target" or from './some/path'
    # Captures the lead quote, the relative path starter, and the actual target name
    pattern = r'(from\s+["\'])(\.\/|\.\.\/)([^"\'\n]+?)(?=["\'])'
    
    def replacement(match):
        prefix = match.group(1)
        rel_path = match.group(2)
        target = match.group(3)
        
        # If it already has an extension, don't touch it (except if it's .wasm and we want to change it)
        if target.endswith(".js") or target.endswith(".wasm") or target.endswith(".ts") or target.endswith(".json"):
            return match.group(0)
            
        target_abs = os.path.normpath(os.path.join(os.path.dirname(file_path), rel_path, target))
        
        if os.path.isdir(target_abs):
            return f'{prefix}{rel_path}{target}/index.js'
        else:
            return f'{prefix}{rel_path}{target}.js'

    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Fixed imports in {file_path}")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".js"):
            fix_imports_final(os.path.join(root, file))
