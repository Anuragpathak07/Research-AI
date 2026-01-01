# api/discover.py
import requests
from flask import Blueprint, request, jsonify
from datetime import datetime
import feedparser
import traceback

discover_bp = Blueprint("discover", __name__)

ARXIV_API = "http://export.arxiv.org/api/query"

def fetch_arxiv(query, start_year, end_year, max_results):
    """Fetch papers from arXiv API"""
    try:
        # URL encode the query properly
        from urllib.parse import quote_plus
        search_query = f"all:{quote_plus(query)}"
        url = f"{ARXIV_API}?search_query={search_query}&start=0&max_results={max_results}"
        
        # Parse the feed
        feed = feedparser.parse(url)
        
        # Check for errors in the feed
        if feed.bozo and feed.bozo_exception:
            raise Exception(f"Feed parsing error: {feed.bozo_exception}")

        papers = []
        for entry in feed.entries:
            try:
                # Extract year from published date
                published = entry.get("published", "")
                if not published:
                    continue
                    
                year = int(published[:4])
                if start_year <= year <= end_year:
                    papers.append({
                        "paper_id": entry.get("id", ""),
                        "title": entry.get("title", "Untitled").replace("\n", " ").strip(),
                        "abstract": entry.get("summary", "").replace("\n", " ").strip(),
                        "authors": [a.name for a in entry.get("authors", [])],
                        "year": year,
                        "venue": "arXiv",
                        "url": entry.get("link", "")
                    })
            except (ValueError, KeyError, AttributeError) as e:
                # Skip entries with invalid data
                print(f"Warning: Skipping entry due to error: {e}")
                continue
                
        return papers
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
        print(traceback.format_exc())
        raise

@discover_bp.route("/", methods=["POST"])
def discover():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        if "query" not in data:
            return jsonify({"error": "Missing 'query' parameter"}), 400
        
        query = data["query"].strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        papers = fetch_arxiv(
            query,
            data.get("start_year", 2015),
            data.get("end_year", datetime.now().year),
            data.get("max_results", 50)
        )
        return jsonify(papers)
    except Exception as e:
        error_msg = str(e)
        print(f"Error in discover endpoint: {error_msg}")
        print(traceback.format_exc())
        return jsonify({"error": error_msg, "type": type(e).__name__}), 500
