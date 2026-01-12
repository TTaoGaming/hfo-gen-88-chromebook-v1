import os
import re

root_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/lib/rapier"

def fix_imports(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Match imports/exports like: from "./exports" or from './math'
    # But NOT from "./exports.js" or from "https://..."
    pattern = r'(from\s+["\'])(\.\/|\.\.\/)([^"\'.]+)(["\'])'
    new_content = re.sub(pattern, r'\1\2\3.js\4', content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Fixed imports in {file_path}")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".js"):
            fix_imports(os.path.join(root, file))
