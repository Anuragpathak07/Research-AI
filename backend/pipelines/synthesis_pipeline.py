# pipelines/synthesis_pipeline.py
from collections import Counter

class SynthesisPipeline:
    def run(self, extracted_papers):
        method_counter = Counter()
        dataset_counter = Counter()
        metric_counter = Counter()
        years = []

        for p in extracted_papers:
            method_counter.update(p.get("methods", []))
            dataset_counter.update(p.get("datasets", []))
            metric_counter.update(p.get("metrics", []))
            years.append(p["year"])

        synthesis = {
            "methods": dict(method_counter),
            "datasets": dict(dataset_counter),
            "metrics": dict(metric_counter),
            "year_range": {
                "start": min(years) if years else None,
                "end": max(years) if years else None
            },
            "papers_analyzed": len(extracted_papers)
        }

        return synthesis
