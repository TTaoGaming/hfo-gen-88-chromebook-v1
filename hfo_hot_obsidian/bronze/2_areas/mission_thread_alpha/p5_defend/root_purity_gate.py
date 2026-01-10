#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
import os
import sys

# PORT-5-DEFEND: ROOT PURITY GATE (Hard Gate)
# Enforces the Law of Root Purity defined in ROOT_GOVERNANCE.md

AUTHORIZED_DIRS = {
    'hfo_cold_obsidian', 'hfo_hot_obsidian', '.github', '.vscode', 
    '.venv', 'scripts', '.git', '.husky', 'node_modules', 
    'reports', 'test-results', '.stryker-tmp'
}

AUTHORIZED_FILES = {
    'AGENTS.md', 'COLD_START.md', 'ROOT_GOVERNANCE.md', '.gitignore',
    '.env', '.pre-commit-config.yaml', 'pyproject.toml', 
    'requirements.txt', 'package.json', 'tsconfig.json', 'stryker.config.json'
}

def check_purity():
    root = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
    files = os.listdir(root)
    violations = []

    for f in files:
        if os.path.isdir(os.path.join(root, f)):
            if f not in AUTHORIZED_DIRS:
                violations.append(f"{f}/ (dir)")
        else:
            if f not in AUTHORIZED_FILES:
                # Allow markdown notes if they follow a pattern
                if f.startswith('ttao-notes') and f.endswith('.md'):
                    continue
                violations.append(f)

    if violations:
        print("🚨 [ROOT_PURITY_GATE]: ROOT POLLUTION DETECTED!")
        print(f"The following unauthorized files/dirs were found in the root: {', '.join(violations)}")
        print("Move them to scripts/, hfo_hot_obsidian/bronze/3_resources/, or appropriate folders.")
        return False

    print("✅ [ROOT_PURITY_GATE]: Root is pure.")
    return True

if __name__ == "__main__":
    if not check_purity():
        sys.exit(1)
