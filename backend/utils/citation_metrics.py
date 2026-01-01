# utils/citation_metrics.py
import numpy as np
from collections import defaultdict

def citation_velocity(papers):
    yearly = defaultdict(int)
    for p in papers:
        yearly[p["year"]] += p.get("citations", 0)

    years = sorted(yearly.keys())
    values = [yearly[y] for y in years]

    if len(values) < 2:
        return 0.0

    slope = np.polyfit(range(len(values)), values, 1)[0]
    return float(slope)

def obsolescence_risk(velocity):
    if velocity < -0.5:
        return "High"
    if velocity < 0:
        return "Medium"
    return "Low"
