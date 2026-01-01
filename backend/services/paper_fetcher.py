# services/paper_fetcher.py
import feedparser
import requests

ARXIV_API = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper"

class PaperFetcher:
    def fetch_arxiv(self, query, max_results=50):
        url = f"{ARXIV_API}?search_query=all:{query}&start=0&max_results={max_results}"
        feed = feedparser.parse(url)

        papers = []
        for e in feed.entries:
            papers.append({
                "paper_id": e.id,
                "title": e.title.strip(),
                "abstract": e.summary.strip(),
                "authors": [a.name for a in e.authors],
                "year": int(e.published[:4]),
                "url": e.link
            })
        return papers

    def enrich_with_citations(self, paper_ids):
        enriched = {}
        for pid in paper_ids:
            resp = requests.get(
                f"{SEMANTIC_SCHOLAR_API}/{pid}",
                params={"fields": "citationCount,referenceCount,year"}
            )
            if resp.status_code == 200:
                enriched[pid] = resp.json()
        return enriched
