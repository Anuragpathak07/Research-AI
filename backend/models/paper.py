# models/paper.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Paper:
    paper_id: str
    title: str
    abstract: str
    authors: List[str]
    year: int
    venue: str
    url: str
    citations: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
