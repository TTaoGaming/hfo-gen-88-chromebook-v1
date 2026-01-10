#!/usr/bin/env python3
import sys
import re
import subprocess
import os

def check_html_syntax(file_path):
    print(f"🔍 Checking {file_path}...")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract <script type="module"> contents
        scripts = re.findall(r'<script type="module">(.*?)</script>', content, re.DOTALL)
        
        for i, script in enumerate(scripts):
            # Use node --check to validate syntax
            # We wrap it in a try-catch block to handle the 'import' statements if node doesn't support them in --check
            # But node --check -e works for module syntax in recent versions if we specify --input-type=module
            process = subprocess.Popen(
                ['node', '--input-type=module', '--check'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=script)
            
            if process.returncode != 0:
                print(f"❌ Syntax Error in <script> block {i+1}:")
                print(stderr)
                return False
        
        print(f"✅ {file_path} syntax is valid.")
        return True
    except Exception as e:
        print(f"💥 Error reading file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: p5_syntax_gate.py <file_path>")
        sys.exit(1)
    
    success = True
    for arg in sys.argv[1:]:
        if not check_html_syntax(arg):
            success = False
    
    if not success:
        sys.exit(1)
