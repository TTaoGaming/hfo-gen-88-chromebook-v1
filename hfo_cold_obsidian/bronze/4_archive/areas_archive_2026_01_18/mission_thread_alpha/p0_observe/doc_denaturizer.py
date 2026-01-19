#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
📜 DOC DENATURIZER (Context7 Alt)
Strips HTML boilerplate to generate clean, LLM-ready documentation context.
"""

from bs4 import BeautifulSoup
import requests

class Denaturizer:
    @staticmethod
    def clean(html_content):
        """Standard denaturization: Strip scripts, styles, and nav elements."""
        soup = BeautifulSoup(html_content, "lxml")

        # 1. Remove obvious noise
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # 2. Extract text with preserved spacing
        text = soup.get_text(separator="\n")

        # 3. Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        clean_lines = [line for line in lines if line]

        return "\n".join(clean_lines)

    @classmethod
    def fetch_and_clean(cls, url):
        """Fetch a remote documentation page and denaturize it."""
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return cls.clean(response.text)

if __name__ == "__main__":
    # Test local
    sample = "<html><body><nav>Boilerplate</nav><h1>Title</h1><p>Doc Content</p></body></html>"
    print(Denaturizer.clean(sample))
