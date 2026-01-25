#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""PORT 5: PREFLIGHT AUDIT SENTRY

Validates that all local assets referenced in HTML files exist on the filesystem.
Prevents 404/ERR_CONNECTION_RESET by ensuring I/O readiness.
"""

import os
import re
import sys
from pathlib import Path

# Paths to audit
BASE_DIR = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
HTML_FILES = [
    BASE_DIR / "active_hfo_omega_entrypoint.html",
    BASE_DIR / "active_omega.html",
    BASE_DIR / "hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html",
    BASE_DIR / "hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11.html",
]

def audit_file(file_path):
    if not file_path.exists():
        print(f"❌ [P5-AUDIT-FAIL]: Target file missing: {file_path}")
        return False

    print(f"🔍 [P5-AUDIT]: Scanning {file_path.name}...")
    content = file_path.read_text()

    # Match src="./..." or href="./..."
    patterns = [
        r'src=["\']\./([^"\']+)["\']',
        r'href=["\']\./([^"\']+)["\']'
    ]

    missing_count = 0
    total_refs = 0

    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            total_refs += 1
            # Handle potential query params or hashes
            clean_path = match.split('?')[0].split('#')[0]
            # Check relative to the HTML file's directory
            asset_path = file_path.parent / clean_path

            if not asset_path.exists():
                print(f"  ❌ [MISSING]: {clean_path} (Resolved to: {asset_path})")
                missing_count += 1
            else:
                # print(f"  ✅ [FOUND]: {clean_path}")
                pass

    if missing_count > 0:
        print(f"🛑 [P5-AUDIT-FAIL]: {missing_count}/{total_refs} assets missing in {file_path.name}")
        return False
    else:
        print(f"✅ [P5-AUDIT-PASS]: All {total_refs} assets verified for {file_path.name}")
        return True

def main():
    success = True
    for html_file in HTML_FILES:
        if not audit_file(html_file):
            success = False

    if not success:
        sys.exit(1)
    print("✨ [P5-PREFLIGHT-COMPLETE]: All systems go.")

if __name__ == "__main__":
    main()
