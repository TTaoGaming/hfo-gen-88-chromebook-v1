// Medallion: Bronze | Mutation: 0% | HIVE: I
# 🐙 HFO Infrastructure: Local Sensing Pillars

## 🎯 Overview
To maintain the **Apex Mosaic Warfare** capability on hardware with intermittent connectivity or API limitations, we extend Port 0 (SENSE) with local semantic and scraping pillars.

## 🏗️ Para Structure: [Hot Bronze]

### Pillar 4: Local Repo Indexer (`local_repo_indexer.py`)
- **Role**: Emulates **Greptile**.
- **Logic**: Uses Python's `ast` (Abstract Syntax Trees) to parse workspace files.
- **Output**: Returns JSON mapping functions, classes, and cross-file imports.

### Pillar 5: Doc Denaturizer (`doc_denaturizer.py`)
- **Role**: Emulates **Context7**.
- **Logic**: Fetches documentation URLs and "denaturizes" them (strips CSS/JS/Boilerplate) using `BeautifulSoup4`.
- **Output**: Returns "LLM-Ready" Markdown context.

## 🧪 Success Criteria (TDD)
- [ ] Indexer detects `octo_sense` function in `octopus_search.py`.
- [ ] Indexer maps dependency `tavily` from `octopus_search.py`.
- [ ] Denaturizer strips `<nav>` and `<script>` from mock HTML.
- [ ] Denaturizer successfully handles invalid URLs with exceptions.

---
*Spider Sovereign | HFO Port 7 | Infrastructure Hardening*
