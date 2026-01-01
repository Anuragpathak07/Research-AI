# agents/gap_agent.py
class GapAgent:
    def detect_gaps(self, trajectories, extracted_papers):
        gaps = []

        method_counts = {}
        for p in extracted_papers:
            for m in p["methods"]:
                method_counts[m] = method_counts.get(m, 0) + 1

        for method, info in trajectories.items():
            count = method_counts.get(method, 0)

            if info["trajectory"] == "Rising" and count < 5:
                gaps.append({
                    "gap_title": f"Underexplored use of {method}",
                    "viability": "Future-Viable",
                    "reason": "Positive momentum with low paper volume",
                    "evidence": info
                })

            if info["trajectory"] == "Declining":
                gaps.append({
                    "gap_title": f"{method} nearing saturation",
                    "viability": "Likely Obsolete",
                    "reason": "Negative trend slope",
                    "evidence": info
                })

        return gaps
