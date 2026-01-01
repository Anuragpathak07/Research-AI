# pipelines/ingestion_pipeline.py
from agents.discovery_agent import DiscoveryAgent
from agents.extraction_agent import ExtractionAgent

class IngestionPipeline:
    def __init__(self):
        self.discovery_agent = DiscoveryAgent()
        self.extraction_agent = ExtractionAgent()

    def run(self, query, start_year=2015, end_year=None, max_results=50):
        papers = self.discovery_agent.fetch_papers(
            query=query,
            start_year=start_year,
            end_year=end_year,
            max_results=max_results
        )

        extracted_papers = self.extraction_agent.extract_entities(papers)

        return extracted_papers
