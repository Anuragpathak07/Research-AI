# services/citation_service.py
import numpy as np
from collections import defaultdict

class CitationService:
    def compute_velocity(self, papers):
        year_citations = defaultdict(list)

        for p in papers:
            if "citations" in p:
                year_citations[p["year"]].append(p["citations"])

        years = sorted(year_citations.keys())
        values = [sum(year_citations[y]) for y in years]

        if len(values) < 2:
            return 0.0

        slope = np.polyfit(range(len(values)), values, 1)[0]
        return float(slope)

    def classify_trend(self, slope):
        if slope > 0.3:
            return "Accelerating"
        elif slope < -0.3:
            return "Declining"
        return "Stable"
