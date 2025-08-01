import pandas as pd
from duckduckgo_search import DDGS
import datetime
from backend.database import CandidateDatabase

def search_and_store_candidates(keywords, db: CandidateDatabase, limit=10):
    query = keywords.strip()
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=limit):
            results.append({
                "name": r.get("title", ""),
                "website": r.get("href", ""),
                "description": r.get("body", ""),
                "retrieved_at": datetime.datetime.utcnow().isoformat(),
                "feedback": None,
                "ai_summary": None
            })

    df = pd.DataFrame(results)
    db.insert_candidates(df)
