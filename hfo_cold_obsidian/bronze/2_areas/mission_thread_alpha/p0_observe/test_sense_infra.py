#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
🧪 RED TEST: Sensing Infrastructure
Success/Failure Criteria for Local Repo Indexer and Doc Denaturizer.
"""

import unittest
import os
import sys

# Add the parent directory to path so we can import the upcoming tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestSenseInfra(unittest.TestCase):

    # --- Pillar 4: Local Repo Indexer (Greptile Alt) ---
    def test_indexer_finds_local_symbol(self):
        """
        SUCCESS: Indexer must find the 'octo_sense' function in octopus_search.py.
        """
        # We expect a function find_symbol(name) to exist in local_repo_indexer
        from local_repo_indexer import RepoIndexer
        indexer = RepoIndexer("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe")
        result = indexer.find_symbol("octo_sense")

        self.assertIsNotNone(result, "FAILED: Could not find 'octo_sense' symbol.")
        self.assertEqual(result['type'], 'function')

    def test_indexer_maps_dependencies(self):
        """
        SUCCESS: Indexer must detect that octopus_search.py depends on 'tavily'.
        """
        from local_repo_indexer import RepoIndexer
        indexer = RepoIndexer("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe")
        deps = indexer.get_dependencies("octopus_search.py")

        self.assertIn("tavily", deps, "FAILED: Dependency 'tavily' not found in octopus_search.py.")

    # --- Pillar 5: Doc Denaturizer (Context7 Alt) ---
    def test_denaturizer_strips_html(self):
        """
        SUCCESS: Denaturizer must return clean text, stripping <script> and <div> noise.
        """
        from doc_denaturizer import Denaturizer
        raw_html = "<html><body><nav>Menu</nav><h1>Target Title</h1><script>alert(1)</script><p>Content</p></body></html>"
        clean_text = Denaturizer.clean(raw_html)

        self.assertNotIn("<script>", clean_text)
        self.assertNotIn("Menu", clean_text, "FAILED: Did not strip navigation/boilerplate.")
        self.assertIn("Target Title", clean_text)
        self.assertIn("Content", clean_text)

    def test_denaturizer_handles_error(self):
        """
        FAILURE: Denaturizer must raise or return error status for invalid URLs.
        """
        from doc_denaturizer import Denaturizer
        with self.assertRaises(Exception):
            Denaturizer.fetch_and_clean("https://this-domain-does-not-exist-hfo.com")

if __name__ == "__main__":
    unittest.main()
