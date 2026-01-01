# models/gap.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Gap:
    title: str
    viability: str           # Future-Viable | Time-Sensitive | Likely Obsolete
    reason: str
    evidence: Dict[str, Any]
