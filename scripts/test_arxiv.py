import arxiv
search = arxiv.Search(query="Rapier.js", max_results=3)
for r in search.results():
    print(r.title)
