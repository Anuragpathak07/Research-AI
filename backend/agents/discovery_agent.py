# agents/discovery_agent.py
import feedparser
from datetime import datetime

ARXIV_API = "http://export.arxiv.org/api/query"

class DiscoveryAgent:
    def fetch_papers(self, query, start_year=2015, end_year=None, max_results=50):
        if end_year is None:
            end_year = datetime.now().year

        search_query = f"all:{query}"
        url = f"{ARXIV_API}?search_query={search_query}&start=0&max_results={max_results}"
        feed = feedparser.parse(url)

        papers = []
        for entry in feed.entries:
            year = int(entry.published[:4])
            if start_year <= year <= end_year:
                papers.append({
                    "paper_id": entry.id,
                    "title": entry.title.strip(),
                    "abstract": entry.summary.strip(),
                    "authors": [a.name for a in entry.authors],
                    "year": year,
                    "venue": "arXiv",
                    "url": entry.link
                })
        return papers
