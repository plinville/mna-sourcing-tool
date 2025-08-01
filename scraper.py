from duckduckgo_search import DDGS

def scrape_candidates(keywords, num_results=10):
    with DDGS() as ddgs:
        results = ddgs.text(keywords, max_results=num_results)
        return [{
            "name": r["title"],
            "url": r["href"],
            "snippet": r["body"]
        } for r in results if all(k in r for k in ("title", "href", "body"))]
