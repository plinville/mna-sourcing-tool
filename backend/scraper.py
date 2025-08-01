import pandas as pd
from duckduckgo_search import DDGS
from sentence_transformers import SentenceTransformer, util
import logging

logging.basicConfig(level=logging.INFO)

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_and_store_candidates(keywords, db, limit=5):
    """
    Perform a web search using DuckDuckGo and store candidate information in the database.
    """
    query = keywords
    logging.info(f"Searching for: {query}")

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=limit)
        data = []
        for r in results:
            name = r.get("title") or ""
            website = r.get("href") or ""
            summary = r.get("body") or ""
            if website:
                data.append({
                    "name": name,
                    "website": website,
                    "summary": summary
                })

    df = pd.DataFrame(data)

    # Ensure required columns are present
    for col in ["name", "website", "summary"]:
        if col not in df.columns:
            df[col] = ""

    # Drop duplicates
    df = df.drop_duplicates(subset="website")

    logging.info(f"Scraped {len(df)} candidates")
    if not df.empty:
        db.insert_candidates(df)
