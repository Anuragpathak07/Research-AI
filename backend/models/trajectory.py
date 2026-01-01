# models/trajectory.py
from dataclasses import dataclass
from typing import List

@dataclass
class Trajectory:
    entity: str              # method / dataset / metric
    years: List[int]
    slope: float
    label: str               # Rising | Stable | Declining | Saturating
