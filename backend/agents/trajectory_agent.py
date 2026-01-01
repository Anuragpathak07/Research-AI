# agents/trajectory_agent.py
from collections import defaultdict
import numpy as np

class TrajectoryAgent:
    def build_trajectories(self, extracted_papers):
        method_years = defaultdict(list)

        for p in extracted_papers:
            for m in p["methods"]:
                method_years[m].append(p["year"])

        trajectories = {}
        for method, years in method_years.items():
            years = sorted(years)
            counts = np.bincount([y - min(years) for y in years])
            slope = np.polyfit(range(len(counts)), counts, 1)[0]

            if slope > 0.3:
                label = "Rising"
            elif slope < -0.3:
                label = "Declining"
            else:
                label = "Stable"

            trajectories[method] = {
                "years": years,
                "slope": float(slope),
                "trajectory": label
            }

        return trajectories
