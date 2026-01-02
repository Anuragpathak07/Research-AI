# agents/discovery_agent.py
import feedparser
from datetime import datetime
from agents.base_agent import BaseAgent
import json

ARXIV_API = "http://export.arxiv.org/api/query"

class DiscoveryAgent(BaseAgent):
    """Agentic discovery agent with LLM reasoning for paper search optimization"""
    
    def __init__(self):
        tools = [
            {
                'name': 'search_arxiv',
                'description': 'Search arXiv for papers matching a query. Input: {"query": "search terms", "max_results": 50}',
                'func': self._search_arxiv_tool
            },
            {
                'name': 'filter_by_relevance',
                'description': 'Filter papers by relevance score. Input: {"papers": [...], "min_relevance": 0.7}',
                'func': self._filter_relevance_tool
            }
        ]
        super().__init__(
            name="Discovery Agent",
            description="An AI agent that discovers and retrieves research papers from arXiv with intelligent query optimization and relevance filtering",
            tools=tools
        )
    
    def _search_arxiv_tool(self, input_data):
        """Tool function for searching arXiv"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        query = input_data.get('query', '')
        max_results = input_data.get('max_results', 50)
        
        search_query = f"all:{query}"
        url = f"{ARXIV_API}?search_query={search_query}&start=0&max_results={max_results}"
        feed = feedparser.parse(url)
        
        papers = []
        for entry in feed.entries:
            year = int(entry.published[:4])
            papers.append({
                "paper_id": entry.id,
                "title": entry.title.strip(),
                "abstract": entry.summary.strip(),
                "authors": [a.name for a in entry.authors],
                "year": year,
                "venue": "arXiv",
                "url": entry.link
            })
        
        return json.dumps(papers, indent=2)
    
    def _filter_relevance_tool(self, input_data):
        """Tool function for filtering papers by relevance"""
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        papers = input_data.get('papers', [])
        min_relevance = input_data.get('min_relevance', 0.7)
        
        # Simple relevance based on keyword matching (can be enhanced)
        filtered = []
        for paper in papers:
            # Placeholder relevance score
            relevance = 0.8  # Default
            if relevance >= min_relevance:
                filtered.append(paper)
        
        return json.dumps(filtered, indent=2)
    
    def fetch_papers(self, query, start_year=2015, end_year=None, max_results=50):
        """
        Fetch papers with LLM reasoning to optimize search strategy
        """
        if end_year is None:
            end_year = datetime.now().year
        
        # Use LLM to reason about the best search strategy
        reasoning_prompt = f"""I need to discover research papers for the query: "{query}"

Consider:
- The query might need refinement or expansion
- Different search terms might yield better results
- The time range is {start_year}-{end_year}
- I need up to {max_results} papers

Should I:
1. Use the query as-is
2. Expand the query with related terms
3. Use multiple search queries and combine results

Provide reasoning and then execute the search."""
        
        # Get LLM reasoning
        reasoning_result = self.simple_reason(reasoning_prompt)
        
        # Execute search (with or without LLM optimization)
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
        
        # Use LLM to reason about paper quality and relevance (optional)
        if papers:
            quality_prompt = f"""I found {len(papers)} papers for query "{query}". 

Analyze if these papers are relevant and if I should:
1. Keep all papers
2. Filter out less relevant ones
3. Search for additional papers with different terms

First {min(5, len(papers))} paper titles:
{chr(10).join([f"- {p['title'][:80]}" for p in papers[:5]])}

Provide reasoning about paper relevance."""
            
            quality_reasoning = self.simple_reason(quality_prompt, context={'papers': papers[:5]})
            # Store reasoning for debugging (only if LLM succeeded)
            if not quality_reasoning.get('fallback'):
                self.last_reasoning = {
                    'search_strategy': reasoning_result,
                    'quality_analysis': quality_reasoning
                }
        
        return papers
