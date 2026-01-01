# utils/scoring.py
import numpy as np

def momentum_score(years):
    if len(years) < 2:
        return 0.0
    counts = np.bincount([y - min(years) for y in years])
    slope = np.polyfit(range(len(counts)), counts, 1)[0]
    return float(slope)

def classify_momentum(score):
    if score > 0.3:
        return "Rising"
    if score < -0.3:
        return "Declining"
    return "Stable"
