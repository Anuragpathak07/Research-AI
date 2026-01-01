# models/method.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Method:
    name: str
    papers: List[str] = field(default_factory=list)
    first_seen_year: int = None
    last_seen_year: int = None
