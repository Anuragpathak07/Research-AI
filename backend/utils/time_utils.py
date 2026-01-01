# utils/time_utils.py
from datetime import datetime

def year_range(papers):
    years = [p["year"] for p in papers if "year" in p]
    if not years:
        return None, None
    return min(years), max(years)

def current_year():
    return datetime.now().year
