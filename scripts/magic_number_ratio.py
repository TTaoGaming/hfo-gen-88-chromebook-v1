import re
import os

def analyze_magic_numbers(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Identify Tunable Parameters
    # We find the block between "parameters: {" and its closing brace (matching pairs).
    tunable_count = 0
    param_block = ""
    start_match = re.search(r'parameters:\s*\{', content)
    if start_match:
        content_after = content[start_match.end()-1:]
        brace_count = 0
        end_pos = 0
        for i, char in enumerate(content_after):
            if char == '{': brace_count += 1
            elif char == '}': brace_count -= 1
            if brace_count == 0:
                end_pos = i + 1
                break
        param_block = content_after[:end_pos]
        # Count keys that have literal values (not nested objects)
        tunable_count = len(re.findall(r'[\w]+:\s*[^\{,\n]+', param_block))
        
    print(f"Tunable Parameters Found: {tunable_count}")

    # 2. Identify Magic Numbers in Logic
    # We strip the parameters block from the content to avoid counting defaults as magic numbers.
    if param_block:
        logic_content = content.replace(param_block, '')
    else:
        logic_content = content
        
    # Strip CSS blocks
    logic_content = re.sub(r'<style[\s\S]*?</style>', '', logic_content)
    # Strip Schema definitions (they are metadata, not magic logic)
    # Aggressively find the block starting with "const NameSchema = " and ending with its closing ";"
    schemas = re.findall(r'const \w+Schema = [\s\S]*?;\n', logic_content)
    for schema in schemas:
        logic_content = logic_content.replace(schema, '')
        
    # Strip any other JSDoc or metadata blocks if needed
    logic_content = re.sub(r'/\*\*[\s\S]*?\*/', '', logic_content)
    # Strip comments
    logic_content = re.sub(r'//.*', '', logic_content)
    logic_content = re.sub(r'/\*[\s\S]*?\*/', '', logic_content)
    
    # Regex for float/int literals
    # Negative lookahead for '.' to avoid matching just part of a float
    # Matches: 1.5, 0.12, 10.0, 42, but not versions like 24.21 if surrounded by quotes or text
    number_pattern = r'(?<![\w.\'"])(-?\d+\.\d+|-?\d+)(?![\w.\'"])'
    
    all_numbers = re.finditer(number_pattern, logic_content)
    
    magic_numbers = []
    excluded_values = {'0', '1', '2', '-1', '0.5', '100', '255', '360', '0.0', '1.0', '-1.0'}
    
    for match in all_numbers:
        val = match.group(0)
        # Get context (30 chars before and after)
        start = max(0, match.start() - 30)
        end = min(len(logic_content), match.end() + 30)
        context = logic_content[start:end].replace('\n', ' ')
        
        # Heuristics for "Magic":
        # - Not a common constant
        # - Not part of a date or version (re-checked by regex)
        # - Not part of an array index like landmark[5] (actually indices can be magic too, but landmarks are well-known)
        
        if val in excluded_values:
            continue
            
        # Ignore common array indices for landmarks (0-20)
        if re.search(r'\[\s*' + re.escape(val) + r'\s*\]', context) and int(float(val)) < 21:
            continue

        # Ignore CSS pixel values if they seem layout-related (e.g. 1280, 720, 30px)
        if 'px' in context.lower() or 'width' in context.lower() or 'height' in context.lower():
            continue

        magic_numbers.append((val, context))

    # De-duplicate magic numbers by value and context roughly
    unique_magic = []
    seen = set()
    for val, ctx in magic_numbers:
        key = (val, ctx.strip())
        if key not in seen:
            unique_magic.append(key)
            seen.add(key)

    magic_count = len(unique_magic)
    
    print(f"Magic Numbers Found: {magic_count}")
    
    total = tunable_count + magic_count
    if total == 0:
        print("No numbers found.")
        return

    magic_pct = (magic_count / total) * 100
    tunable_pct = (tunable_count / total) * 100
    
    print(f"\n--- RESULTS for {os.path.basename(file_path)} ---")
    print(f"Tunable: {tunable_count} ({tunable_pct:.1f}%)")
    print(f"Magic:   {magic_count} ({magic_pct:.1f}%)")
    print(f"Target:  Tunable > 80%, Magic < 20%")
    
    if tunable_pct >= 80:
        print("✅ PASS: Architecture is sufficiently tunable.")
    else:
        print("❌ FAIL: Too many magic numbers. Decoupling required.")

    print("\n--- SAMPLE MAGIC NUMBERS ---")
    for val, ctx in unique_magic[:20]:
        print(f"  {val}  |  ...{ctx}...")

if __name__ == "__main__":
    import sys
    target_file = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v24_21.html"
    analyze_magic_numbers(target_file)
