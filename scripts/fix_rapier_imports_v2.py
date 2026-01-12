import os
import re

root_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/lib/rapier"

def fix_imports(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # This regex matches things like: from "./exports" (without extension)
    pattern = r'(from\s+["\'])(\.\/|\.\.\/)([^"\'.]+)(["\'])'
    
    def replacement(match):
        prefix = match.group(1)
        rel_path = match.group(2)
        target = match.group(3)
        suffix = match.group(4)
        
        # Determine the absolute path of the target
        target_abs = os.path.normpath(os.path.join(os.path.dirname(file_path), rel_path, target))
        
        if os.path.isdir(target_abs):
            # Target is a directory, use /index.js
            return f'{prefix}{rel_path}{target}/index.js{suffix}'
        else:
            # Target is not a directory, assume it's a file and use .js
            return f'{prefix}{rel_path}{target}.js{suffix}'

    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Fixed imports in {file_path}")

# First, revert the previous bad fix (some files might have .js.js now if I ran it twice, or just bad targets)
# Actually, I'll just run it once more with a more careful regex that skips existing .js
def fix_imports_v2(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Match imports like: from "./target" but NOT from "./target.js"
    # Negative lookahead for .js
    pattern = r'(from\s+["\'])(\.\/|\.\.\/)([^"\'\n]+?)(?<!\.js)(?=["\'])'
    
    def replacement(match):
        prefix = match.group(1)
        rel_path = match.group(2)
        target = match.group(3)
        # target might be "exports" or "dynamics"
        
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
            fix_imports_v2(os.path.join(root, file))
