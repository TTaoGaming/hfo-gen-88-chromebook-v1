#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
📂 LOCAL REPO INDEXER (Greptile Alt)
Extracts semantic symbols and dependencies from local Python files.
"""

import ast
import os
import glob

class RepoIndexer:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def find_symbol(self, name):
        """Scan files for a specific function or class name."""
        files = glob.glob(os.path.join(self.root_dir, "*.py"))
        for file_path in files:
            with open(file_path, "r") as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name == name:
                            return {"type": "function", "file": file_path, "line": node.lineno}
                        if isinstance(node, ast.ClassDef) and node.name == name:
                            return {"type": "class", "file": file_path, "line": node.lineno}
                except Exception:
                    continue
        return None

    def get_dependencies(self, filename):
        """Find modules imported by a specific file."""
        file_path = os.path.join(self.root_dir, filename)
        if not os.path.exists(file_path):
            return []

        deps = []
        with open(file_path, "r") as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            deps.append(alias.name)
                    if isinstance(node, ast.ImportFrom):
                        deps.append(node.module)
            except Exception:
                pass
        return deps

if __name__ == "__main__":
    # Internal test CLI
    indexer = RepoIndexer(".")
    print(f"Index complete: {len(glob.glob('*.py'))} files found.")
